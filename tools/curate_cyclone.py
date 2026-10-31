#!/usr/bin/env python3
"""Deterministic, fail-closed curation of Williams Cyclone (1988, System 11B).

The reviewed manual tables and the ROM's own name tables live in ``cyclone_data.py``, the excerpts under
``evidence/excerpts/williams.cyclone.1988/``, the compact runtime evidence in ``evidence/runtime/system-11/`` and the
retained table's geometry in ``tools/seeds/williams/cyclone-1988-geometry.json``. Generation reads none of the
external roots, so ``--regenerate`` reproduces the definition, the knowledge note and the spatial reports byte for
byte and ``--check`` refuses any drift. ``--verify-evidence`` re-derives every retained artifact (manual, IPDB page,
script library, raw harness runs, table geometry and, when ``PINMAME_ROM_LIBRARY_ROOT`` is set, the ROM name
tables) from the configured roots; ``--write-extraction-manifest`` and ``--verify-extraction`` maintain the retained
table extraction's full-file manifest. An existing author-ready record is never overwritten by a partial one.

Cyclone is ``INITGAME(cycln, GEN_S11B, s11_dispS11b1, 12, FLIP_SWNO(57,58), 0,0)``: the A/C select relay is solenoid
12, so pinned PinMAME publishes the eight switched "A" loads at 1-8 and their "C" partners at 25-32; the cabinet
flipper buttons are copied into the lane-change switches 57 and 58; and no special-solenoid switch is declared, so
the ROM fires the jet bumpers and slingshots (17-21) itself through the PIA control lines.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.spatial import _item_point, _round_point  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402
from pinmame_flipper_column import (  # noqa: E402
	VPM_LIBRARY_SOURCE,
	VPM_LIBRARY_URI,
	VPM_S11_SHA256,
	flipper_column_inputs,
	flipper_column_relationships,
	vpm_staged_flipper_notes,
)
import cyclone_data as data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = data.MACHINE_ID
DEFINITION = Path("machines/partial/williams/cyclone-1988.json")
AUTHOR_READY = Path("machines/author-ready/williams/cyclone-1988.json")
GEOMETRY = Path("tools/seeds/williams/cyclone-1988-geometry.json")
KNOWLEDGE_SEED = Path("tools/seeds/williams/cyclone-1988-knowledge.md")
KNOWLEDGE = Path("knowledge/williams/cyclone-1988.md")
REPORT = Path("reports/spatial/williams/cyclone-1988.json")
REPORT_MD = Path("reports/spatial/williams/cyclone-1988.md")
RUNTIME = Path("evidence/runtime/system-11/cyclone-l5-service-and-mechanisms.json")
RUNTIME_L4 = Path("evidence/runtime/system-11/cyclone-l4-coil-test.json")
RUNTIME_L1 = Path("evidence/runtime/system-11/cyclone-l1-coil-test.json")
EXCERPTS = Path("evidence/excerpts") / MACHINE_ID
REVIEW_FOLDER = "cyclone-1988"
MANUAL_FOLDER = Path("by-machine") / MACHINE_ID / "ipdb-617"

CATALOG = f"pinmame.catalog.{data.PINMAME_REVISION[:12]}"
CORE = f"pinmame.core.{data.PINMAME_REVISION[:12]}"
PROFILE = "controller-profile.pinmame-system-11"
MANUAL = "manual.williams.cyclone.1988"
PARTS = "manual.williams.cyclone.1988.parts"
BULLETINS = "service-bulletin.williams.cyclone.1988"
IPDB = "ipdb.617"
ROM_TABLES = "rom-static.cyclone.u27-name-tables"
RUNTIME_SOURCE = "runtime.cyclone.l5-service-and-mechanisms"
RUNTIME_L4_SOURCE = "runtime.cyclone.l4-coil-test"
RUNTIME_L1_SOURCE = "runtime.cyclone.l1-coil-test"
SCRIPT = "vpx-script.cyclone.v1-5"
LIBRARY = VPM_LIBRARY_SOURCE
TABLE = "vpx-table.cyclone.v1-5"
EXTRACTION = "vpx-extraction.cyclone.v1-5"

MANUAL_FILENAME = "Williams_1988_Cyclone_Manual_Schematics.pdf"
PARTS_FILENAME = "Williams_1988_Cyclone_Parts_Manual.pdf"
PARTS_SHA256 = "1c35b842dc66c24b06f38b61c0387c6cd20f9eba7f806919171e4a73ac5ee54f"
BULLETINS_FILENAME = "Williams_1988_Cyclone_Service_Bulletin_Book_1989_includes_Cyclone_SS47_SS49_SS50_SS52.pdf"
BULLETINS_SHA256 = "c12614faa3efee725c0c6ff0e586087987eead49fa024fe1107e61654ea1599c"
MANUAL_SHA256 = "64ace9535ee54a52cd416d95235953626d14d4de6726b05bfa0c8d144f538817"
IPDB_PAGE = "machine-617.html"
IPDB_PAGE_SHA256 = "d0698171ac2f9a92b2f909dc22774e388f58d446684d84a76d74af1a62de1deb"
SCRIPT_SHA256 = "3b917d098d2756b7889d63de1e69f54f5f185d9ad6c343dcc3cf2bcbbc00086d"
SCRIPT_NAME = "Cyclone (Williams 1988) v1.5.vbs"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
RUNTIME_MANIFEST_SHA256 = "a483fe6e44935c183d9ee9970ae44b6f5bf967eeb748539f5468bbdc1b4648c0"
ROM_LIBRARY_VARIABLE = "PINMAME_ROM_LIBRARY_ROOT"

# excerpt key: (file, locator)
EXCERPT_FILES = {
	"switch-matrix": ("switch-matrix.md", "Manual & Schematics PDF page 34 (printed CYCLONE 30), Switch-Matrix Table and its wiring headings"),
	"lamp-matrix": ("lamp-matrix.md", "Manual & Schematics PDF page 31 (printed CYCLONE 27), Lamp-Matrix Table and its wiring headings"),
	"solenoid-table": ("solenoid-table.md", "Manual & Schematics PDF page 2, Solenoid Table and its notes"),
	"location-parts-lists": ("location-parts-lists.md", "Manual & Schematics PDF pages 40, 43, 44 and 45 (printed CYCLONE 36, 39, 40 and 41), Switches, Lamps and Solenoids/Flashers lists and the playfield underside boards and mechanisms"),
	"operation-and-diagnostics": ("operation-and-diagnostics.md", "Manual & Schematics PDF pages 2 (ROM and Jumper Table), 9 (Game Operation) and 30-35 (Test/Diagnostic Procedures and the A/C select relay note)"),
	"rom-name-tables": ("rom-name-tables.md", "U27 lamp, switch and coil-test name tables of cycln_l5, cycln_l4 and cycln_l1"),
	"pinmame-contract": ("pinmame-contract.md", "driver.c 2767-2769; s11games.c 33-36, 500-530; s11.c 66-69, 180-200, 371-372, 537-584, 611-623, 644-651, 727, 796-801, 875-881, 956-962; s11.h; gen.h; core.h; core.c 1832-1846, 2664-2670; memory.h 125"),
	"script-contract": ("script-contract.md", f"{SCRIPT_NAME} controller bindings"),
	"script-library": ("script-library.md", "s11.vbs lines 1 and 18-40, cabinet and flipper constants"),
	"service-bulletins": ("service-bulletins.md", "Service Bulletin Book PDF pages 7-12: SS47 (Mystery Wheel stepper control assembly and schematic), SS49 (post and ring at the Cyclone ramp), SS50 (Ferris wheel belt) and SS52 (Spookhouse ramp bracket)"),
	"parts-assemblies": ("parts-assemblies.md", "Parts Information Manual PDF pages 10, 13, 14, 15 and 17 (printed CYCLONE 8, 11, 12, 13 and 15): the top playfield panel and Mystery Wheel opto positioner boards, the jet bumper coil, Ferris wheel, kicker arm, kickbig and Mystery Wheel carousel assemblies"),
}
EXCERPT_DIGESTS = {
	"switch-matrix": "a78d4a39f07f3f21598719f7645e2c76b2af3dcafb4725e2196af77938aa8700",
	"lamp-matrix": "3f061d3f0a630d5a36410c43d3a7319db6eb60b0eea3ec1c2428244763c0bc0e",
	"solenoid-table": "f88763ec175a35bb652ea635c2e094af9ed1ae1ad8dbce0450e939e6f005b95e",
	"location-parts-lists": "58631384addf747b0a08d3ffd4c3bbc4de59b34a50479590d9d8631b9faf4062",
	"operation-and-diagnostics": "ff926844e3f8b18b3a1935d6d8d81673e7d48b50b69aeffd17b938df40ec33c4",
	"rom-name-tables": "bf7ded904f62a11598e335e0a941824421d10c534b8229d3fe8436cc093fe90c",
	"pinmame-contract": "4db36e6d89df5ca4815af0a710e0ab02a74f7d71580cac13f889192eeb12edc7",
	"script-contract": "2c4d551a1e36d4f97dcd2723122e35f8ea06ca29f217b1bd56e4f44214f87e86",
	"script-library": "90a380664f1de4f5602e7985f02d7a45294ecfd372315be8aa0f6cc4911cf06b",
	"service-bulletins": "c55db6cc9a0a557fd5f3503df0041b77248806eb4185b9052d84c4db1e21706d",
	"parts-assemblies": "c5b67a11e8a374125de870ca0582c0980e42b1dc33688d10883c1b78b5be470d",
}
MANUAL_EXCERPTS = ("switch-matrix", "lamp-matrix", "solenoid-table", "location-parts-lists", "operation-and-diagnostics")

FLIP_SWNO = (57, 58)
AC_RELAY = 12


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(label: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


def provenance(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


# ---------------------------------------------------------------- labels and per-address facts

SWITCH_LABELS = {address: data.SWITCH_MATRIX[address] for address in range(1, 65) if address not in data.UNUSED_SWITCHES}
# Construction asserted only where a part number, footnote or the parts list itself identifies it.
SWITCH_TYPES = {1: "tilt", 3: "button", 7: "tilt", 8: "button", 9: "tilt", 18: "opto", 41: "opto"}
DEDICATED_LABELS = {
	-7: ("Advance (Diagnostic)", "service.advance"), -6: ("Auto-Up/Manual-Down (Diagnostic)", "service.updown"),
	-5: ("CPU Diagnostic", "service.cpu-diag"), -4: ("Sound Diagnostic", "service.sound-diag"),
}
CABINET_SWITCH_ROLES = {
	1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin.right", 5: "cabinet.coin.center", 6: "cabinet.coin.left",
	7: "cabinet.slam-tilt", 8: "cabinet.service", 9: "cabinet.tilt", 41: "cabinet.backbox-toy",
}
# What the retained known-working script does with each switch (corpus script line numbers).
SWITCH_SCRIPT = {
	1: "vpmNudge.TiltSwitch = swTilt (line 67), which S11.VBS defines as 1, so the table's nudge tilt closes the plumb bob",
	10: "Outhole_Hit/unHit (lines 152-153) on the Outhole kicker, where the table creates its ball (lines 89-90)",
	11: "sw11_Hit pulses 11 (line 597) from an invisible trigger behind the drop target",
	13: "sw13_Hit/unHit (lines 595-596) on the sw13 kicker that solBoomerangKickout kicks (line 613)",
	17: "Sw17_Hit/UnHit (lines 647-648), commented 'Entrada ferris wheel'",
	18: "Sw18_Hit drops the Sw18 target and closes 18 (line 601); SpookHouseDropUp raises it and opens 18 (lines 603-609)",
	25: "ShooterLane_Hit/Unhit (lines 629-630)",
	31: "Sw31_Hit/UnHit (lines 649-657), commented 'Entrada rampa comet'",
	32: "Sw32_Hit/UnHit (lines 658-659), commented 'Score rampa comet', which also tilts the switch wire SwitchWire2",
	34: "Sw34_Hit/UnHit (lines 660-661), commented 'Score rampa cyclone', which also tilts SwitchWire1",
	59: "none: sw59_Hit (line 590) pulses 25, the shooter-lane switch, instead of 59, and no line of the script writes 59",
	60: "BumperIzquierda_Hit pulses 60 (line 538)",
	61: "BumperDerecha_Hit pulses 61 (line 539)",
	62: "BumperAbajo_Hit pulses 62 (line 540)",
	63: "LeftSlingShot_Slingshot pulses 63 (lines 545-546)",
	64: "RightSlingShot_Slingshot pulses 64 (lines 562-563)",
}
for _address in (14, 15, 16, 53, 54, 55, 56):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit/Unhit (lines 633-646)"
for _address in (19, 20, 21, 22, 23, 24):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit pulses {_address} (lines 583-589)"
for _address in (26, 27, 28, 29, 30):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit pulses {_address} (lines 667-671, the 'SkillShot' block)"
for _address in (35, 36, 37):
	SWITCH_SCRIPT[_address] = f"Sw{_address}_Hit pulses {_address} (lines 662-664) from a rubber"

SOLENOID_LABELS = {
	1: "Outhole Kicker", 2: "Unused Switched Drive 02A", 3: "Ball Shooter Kickbig", 4: "Boomerang Kickbig",
	5: "Center Drop Target Reset", 6: "Unused Switched Drive 06A", 7: "Knocker", 8: "Unused Switched Drive 08A",
	9: "Spins Mystery Wheel Flasher", 10: "Playfield G.I. Relay", 11: "Backglass G.I. Relay", 12: "Solenoid A/C Select Relay",
	13: "Mystery Wheel Stepper Coil B", 14: "Mystery Wheel Stepper Coil A", 15: "Boomerang Flashers", 16: "Ferris Wheel Motor Relay",
	17: "Left Jet Bumper", 18: "Left Kicker (Sling)", 19: "Right Jet Bumper", 20: "Right Kicker (Sling)", 21: "Bottom Jet Bumper",
	22: "Unused Special Drive 22",
	25: "Left Ferris Wheel + Jackpot Flashers", 26: "Right Ferris Wheel + Teeth Flashers", 27: "Top Middle + Left Eye Flashers",
	28: "Cats + Lower Fireworks Flashers", 29: "Ducks + Right Fireworks Flashers", 30: "Ferris Wheel Flashers",
	31: "Cyclone + Right Eye Flashers", 32: "Spook House + Left Fireworks Flashers",
}
UNUSED_SOLENOIDS = frozenset({2, 6, 8, 22})
SOLENOID_KIND = {
	1: "coil", 3: "coil", 4: "coil", 5: "coil", 7: "coil", 9: "flasher", 10: "gi", 11: "gi", 12: "relay", 13: "motor",
	14: "motor", 15: "flasher", 16: "motor", 17: "coil", 18: "coil", 19: "coil", 20: "coil", 21: "coil",
	**{address: "flasher" for address in range(25, 33)},
}
SOLENOID_CALLBACKS = {
	1: "SolCallback(1) = \"OutholeKick\" (line 127), which kicks the Outhole kicker (lines 146-151)",
	3: "SolCallback(3) = \"EMKicker\" (line 128), which kicks the KSalida kicker into play (lines 155-164)",
	4: "SolCallback(4) = \"solBoomerangKickout\" (line 129), which kicks the sw13 kicker (lines 611-616)",
	5: "SolCallback(5) = \"SpookHouseDropUp\" (line 130), which raises the Sw18 drop target and opens 18 (lines 603-609)",
	7: "SolCallback(7) = vpmSolSound \"Knocker\" (line 131), a sound only",
	10: "SolCallback(10) = \"SolGI\" (line 132): on turns every light of the GI and GI2 collections off and off turns them on (lines 323-333)",
	11: "SolCallback(11) = \"SolBackGenIllumin\" (line 133), relay sounds only (lines 185-191)",
	13: "the stepper cvpmMech mWheelMech's second phase, .Sol2 = 13 (lines 71-83), turning the backglass MysteryWheel image",
	14: "the stepper cvpmMech mWheelMech's first phase, .Sol1 = 14 (lines 71-83), turning the backglass MysteryWheel image",
	15: "SolCallback(15) = \"Flash15\" (line 134), commented 'boomerang flashers', lighting Flash15a/b/c (lines 193-203)",
	16: "SolCallback(16) = \"SolWheelDrive\" (line 135), which runs FWTimer: the RedWheel primitive turns one degree per tick and FerrisBlockedWall opens in four angle windows per turn (lines 755-779)",
	25: "SolCallback(25) = \"Flash25\" (line 137), commented 'pops left', lighting F25 and F25b (lines 205-213)",
	26: "SolCallback(26) = \"Flash26\" (line 138), commented 'pops right'",
	27: "SolCallback(27) = \"Flash27\" (line 139), commented 'backmiddle', lighting F27, F27b and the dome Flasher27p (lines 225-237)",
	28: "SolCallback(28) = \"Flash28\" (line 140), commented 'cats'",
	29: "SolCallback(29) = \"Flash29\" (line 141), commented 'ducks', lighting F29, F29b, F29c, F29d and the dome Flasher29p (lines 249-265)",
	30: "SolCallback(30) = \"Flash30\" (line 142), commented 'backleft/Ferris', lighting F30, F30b, F30c, F30d and the domes Flasher30p and Flasher30pb (lines 267-287)",
	31: "SolCallback(31) = \"Flash31\" (line 143), commented 'Cyclone Flasher', lighting F31, F31b and the dome Flasher31p (lines 289-301)",
	32: "SolCallback(32) = \"Flash32\" (line 144), commented 'SpookHouse', lighting F32, F32b and F32c (lines 305-315)",
}
SOLENOID_RUNTIME = {
	1: (
		"In the gameplay run, with the ball held on 10, Start (3) raised the enable 23 and the ROM kicked the outhole at "
		"15.58 s and again 2.09 s later, when the scenario opened 10; after the drain at 94.08 s it kicked 6.18 s later. "
		"With 10 held from power-up and no game started (run boot-held) it never fired, and after the tilted ball "
		"drained with 10 held it kicked every 2.04-2.06 s."
	),
	3: (
		"In the gameplay run it fired 1.07 s after the ball closed the kickbig switch 26. With 26 held from power-up "
		"(run boot-held) it fired every 3.1-3.3 s. The ROM also fires it about 0.13-0.23 s after 4 at power-up "
		"(2.55/2.68 s in run boot-baseline) and at two later points of the gameplay run (79.32/79.55 s and "
		"119.10/119.23 s); the runs do not establish what starts that pair."
	),
	4: (
		"In the gameplay run, with the ball held on 13 and the drop target held down (18), the ROM fired 5 twice and "
		"then this kickbig 5.25 s after 13 closed. With 13 held from power-up (run boot-held) it fired every "
		"1.55-1.67 s."
	),
	5: (
		"In the gameplay run the ROM pulsed it at 67.84 and 68.66 s while the ball sat in the boomerang kickbig (13) "
		"with the target held down (18), and twice more after the kickbig fired; with 18 still held it then stopped. It "
		"pulsed it again at the start of each later ball (100.37 and 110.14 s). With 18 held from power-up and no game "
		"started (run boot-held) it never fired."
	),
	9: (
		"In the gameplay run it flashed when the drop target went down (18) and repeatedly around the Score Spook "
		"House closure (11) that spun the Mystery Wheel. The retained script has no callback for it."
	),
	10: (
		"Pinned PinMAME types it as a reverse-acting #44 6.3 V AC bulb (\"Playfield GI output\"), so its modulated "
		"output is the brightness of the playfield G.I. the released relay feeds. In the gameplay run the ROM pulsed "
		"it as a light effect at coin-up, scoring and the playfield tilt."
	),
	11: (
		"Pinned PinMAME types it as a reverse-acting #44 6.3 V AC bulb (\"Backbox GI output\"). In the gameplay run the "
		"ROM pulsed it as a light effect at coin-up and scoring."
	),
	12: (
		"In the Coil Test the ROM pulses every C-side load (25-32) with it energized and 12 itself at step 12; in the "
		"gameplay run it energized it for the C-side flasher effects."
	),
	13: (
		"In the Mystery Wheel Test (runs wheel-test-*) the ROM raised 13 and 14 together and, while the wheel stepped, "
		"dropped each for single updates of about 17 ms in an interleaved pattern; in the gameplay run, after the Score "
		"Spook House switch (11) closed, it held 13 and 14 on together from 63.11 to 63.83 s. The stepper board takes "
		"them as two logic inputs, each steering one motor winding (service bulletin SS47), so a recreation reads them "
		"as levels, not as coil pulses; PinMAME's published solenoid state is too coarse to give the phase sequence. The "
		"Coil Test skips its step."
	),
	14: (
		"In the Mystery Wheel Test (runs wheel-test-*) the ROM raised 13 and 14 together and, while the wheel stepped, "
		"dropped each for single updates of about 17 ms in an interleaved pattern; in the gameplay run, after the Score "
		"Spook House switch (11) closed, it held 13 and 14 on together from 63.11 to 63.83 s. The stepper board takes "
		"them as two logic inputs, each steering one motor winding (service bulletin SS47), so a recreation reads them "
		"as levels, not as coil pulses; PinMAME's published solenoid state is too coarse to give the phase sequence. The "
		"Coil Test skips its step."
	),
	15: "In the gameplay run it flashed eight times while the ball sat in the boomerang kickbig (13), before the kickbig fired.",
	16: (
		"At power-up the ROM ran it from 2.33 to 11.77 s (run boot-baseline). In the gameplay run it ran from Start "
		"(15.33 s) until 88.92 s, 9.5 s after the last switch the scenario closed, and started again at 92.50 s with the "
		"next switch closure (53)."
	),
	17: "In the gameplay run the ROM fired it when the left jet bumper switch 60 closed.",
	18: "In the gameplay run the ROM fired it when the left kicker switch 63 closed.",
	19: "In the gameplay run the ROM fired it when the right jet bumper switch 61 closed.",
	20: "In the gameplay run the ROM fired it when the right kicker switch 64 closed.",
	21: "In the gameplay run the ROM fired it when the bottom jet bumper switch 62 closed.",
}
# The Solenoid Table's quantity suffix (b = backbox, p = playfield) per flasher circuit.
FLASHLAMP_QUANTITY = {25: (2, 1), 26: (1, 1), 27: (1, 1), 28: (1, 2), 29: (1, 2), 30: (0, 2), 31: (1, 1), 32: (1, 1), 9: (0, 1), 15: (0, 3)}
# Coil part numbers the parts manual's assembly listings give (excerpt parts-assemblies).
PARTS_MANUAL_COILS = {
	3: ("AE-24-900", "Shooter Lane kickbig (B-11051-R)"), 4: ("AE-26-1500", "Boomerang kickbig (B-11051-R)"),
	17: ("AE-23-800", "Jet Bumper Coil Assembly (B-9415-1)"), 18: ("AE-26-1500", "Kicker Arm Assembly (B-9463)"),
	19: ("AE-23-800", "Jet Bumper Coil Assembly (B-9415-1)"), 20: ("AE-26-1500", "Kicker Arm Assembly (B-9463)"),
	21: ("AE-23-800", "Jet Bumper Coil Assembly (B-9415-1)"),
}

VIRTUAL_SOLENOIDS = {
	23: ("Game-On / Special-Solenoid Enable", "used", "internal.game-on-enable", (
		"PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL (pinned s11.h S11_GAMEONSOL 23), set from PIA0 CB2 in pia0cb2_w; it "
		"gates the special solenoids 17-22 and the synthetic flipper outputs 45-48. It has no driver transistor and no Sol. "
		"No. of its own. In the gameplay run it rose at Start, fell at the first playfield-tilt closure (9, 103.71 s) and "
		"rose again for the next ball; the ROM also holds it while its diagnostic tests run. The retained script binds "
		"SolCallBack(23) = \"FastFlips.TiltSol\" (line 136)."
	)),
	24: ("Unassigned Solenoid Slot 24", "unused", "internal.unused-platform-slot", (
		"Unassigned platform gap between the special-solenoid enable (23) and the A/C-relay C-side bank (25-32); no System 11 "
		"driver populates it and no Cyclone run published it."
	)),
	45: ("Synthetic Lower Right Flipper Power", "used", "internal.synthetic-flipper", (
		"PinMAME's synthetic lower-right flipper power output (CORE_FIRSTLFLIPSOL = 45). The driver declares FLIP_SWNO(57,58) "
		"with no FLIP_SOL, so core_updateSw fabricates 45/46 from the right button bit at public 82 and 47/48 from the left bit "
		"at public 84 while the enable (23) is on; in the Switch Levels run holding 82 raised 45 and 46 and holding 84 raised "
		"47 and 48. The manual prints no driver for the flippers: the Solenoids/Flashers list names the FL 11630-50VDC coils "
		"without a Sol. No. The retained script binds SolCallback(sLRFlipper) and SolCallback(sLLFlipper) (lines 380-381) and "
		"also drives the same subs from the flipper keys through its FastFlips helper (lines 92-118)."
	)),
	46: ("Synthetic Lower Right Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-right flipper hold output; see address 45."),
	47: ("Synthetic Lower Left Flipper Power", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper power output; see address 45."),
	48: ("Synthetic Lower Left Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper hold output; see address 47."),
	49: ("PinMAME Simulator Ball-Shooter Channel", "unused", "internal.unused-platform-slot", (
		"Platform-wide simulator-only output (CORE_FIRSTSIMSOL = 49); the driver declares no simulator."
	)),
	50: ("Unassigned Solenoid Slot 50", "unused", "internal.unused-platform-slot", (
		"Unassigned gap below the custom-solenoid base (51). The driver declares no custSol, so MACHINE_INIT(s11) sizes "
		"coreGlobals.nSolenoids as CORE_FIRSTCUSTSOL - 1 + 0 = 50 and nothing above 50 is modelled."
	)),
}
UPPER_FLIPPER_NOTE = (
	"Platform generic upper-flipper address (CORE_FIRSTUFLIPSOL = 33). FLIP_SWNO(57,58) sets no upper FLIP_SW or FLIP_SOL "
	"bit and core_getSol serves 33-36 only for WPC and SAM generations, so it reads as always zero. Cyclone has two "
	"flippers: the playfield underside list names a lower right and a lower left flipper assembly and nothing else."
)
OVERLAY_NOTE = (
	"Platform sound-overlay range (37-44). The driver's gameSpecific1 is 0, so S11_SNDOVERLAY is unset and the sound byte is "
	"never diverted to a solenoid pattern. Unpopulated on this machine."
)

LAMP_LABELS = {address: data.LAMP_MATRIX[address] for address in range(1, 65)}

# ---------------------------------------------------------------- spatial

SPATIAL_REFS = (TABLE, SCRIPT, MANUAL)
PROJECTIONS = {
	("switch", 57): (
		"The Switches list gives the left lane-change switch its own part (B-9951-1) apart from the cabinet Flipper Button "
		"(SW-10A-48), and the switch drawing's (PDF 40) balloon 57 points at the left flipper's pivot, so it is placed "
		"at the table's LeftFlipper pivot; where on the flipper assembly the switch is mounted is not printed. A consumer "
		"drives 84, not 57."
	),
	("switch", 58): (
		"The Switches list gives the right lane-change switch its own part (B-9951) apart from the cabinet Flipper Button "
		"(SW-10A-48), and the switch drawing's (PDF 40) balloon 58 points at the right flipper's pivot, so it is placed "
		"at the table's RightFlipper pivot; where on the flipper assembly the switch is mounted is not printed. A consumer "
		"drives 82, not 58."
	),
	("solenoid", 4): (
		"The Boomerang Kickbig coil sits under the kickbig its switch 13 reports; the placement is the sw13 kicker the "
		"script both reads and kicks."
	),
	("solenoid", 5): (
		"The drop-target reset coil sits under the target; the placement is the Sw18 drop target it raises."
	),
	("solenoid", 16): (
		"The Ferris wheel motor is part of the C-11900 Ferris Wheel/Motor Assembly; the placement is the position of the "
		"table's RedWheel primitive, the wheel its FWTimer rotates. Where the motor sits in the assembly is not printed."
	),
}


def load_geometry(root: Path) -> dict[str, Any] | None:
	path = root / GEOMETRY
	return load_json(path) if path.is_file() else None


def anchors(geometry: dict[str, Any] | None, kind: str, address: int) -> list[str]:
	if geometry is None:
		return []
	return list(geometry["anchors"].get(kind, {}).get(str(address), []))


def located(identifier: str, role: str, names: list[str], geometry: dict[str, Any] | None) -> dict[str, Any] | None:
	if geometry is None or not names:
		return None
	bounds = geometry["bounds"]
	width, height = bounds["right"] - bounds["left"], bounds["bottom"] - bounds["top"]
	points = []
	for index, name in enumerate(names, 1):
		obj = geometry["objects"][name]
		suffix = f".{index}" if len(names) > 1 else ""
		points.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield",
			"x": _round_point((obj["x"] - bounds["left"]) / width), "y": _round_point((obj["y"] - bounds["top"]) / height),
			"provenance": provenance(*SPATIAL_REFS, status="observed"),
		})
	return {"status": "observed", "placements": points}


def placement_note(kind: str, address: int, names: list[str]) -> str:
	if (kind, address) in PROJECTIONS:
		return " Placement: " + PROJECTIONS[(kind, address)]
	if kind == "solenoid" and address == 10:
		return (
			f" Placement: the {len(names)} lights of the retained table's GI collection that model a bulb (is_bulb_light and "
			"show_bulb_mesh both set), which SolGI switches from this output; GILight32-34 and 36-38 and the GI2 plastic "
			"lights model no bulb and are left out. A table's G.I. grouping is not the machine's wiring, so the placements "
			"stay observed and no quantity is asserted."
		)
	if kind == "solenoid" and address in (29, 30, 31):
		dome = {29: "Flasher29p", 30: "Flasher30pb", 31: "Flasher31p"}[address]
		return (
			f" Placement: the table's light F{address}, which Flash{address} drives, under the flasher dome {dome} within "
			"2 units of it; it is one of the circuit's playfield bulbs."
		)
	return f" Placement: the retained table's {names[0]}, which the script binds to this address."


# ---------------------------------------------------------------- inputs

def switch_wiring(address: int) -> dict[str, Any]:
	column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
	transistor, drive_wire, drive = data.SWITCH_COLUMNS[column]
	return_wire, ret = data.SWITCH_ROWS[row]
	return {
		"board": "System 11B CPU board switch matrix", "drive_wire": drive_wire, "drive_connection": drive,
		"return_wire": return_wire, "return_connection": ret, "driver_transistor": f"column {transistor}",
	}


RUNTIME_SWITCH_NOTE = (
	" In the ROM's Switch Levels test (run switch-levels) holding public {address} at 1 alone made the player 1 and 2 "
	"displays show \"{name}\" and the player 3 display 06 {address:02d}, so the ROM reads it active at 1. pia4a_r returns "
	"core_getSwCol without inversion and the driver declares no inverted switch, so the contact the matrix sees is open "
	"at rest and closed when actuated."
)


def build_inputs(geometry: dict[str, Any] | None) -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role) in DEDICATED_LABELS.items():
		items.append({
			"id": f"switch.diagnostic-{abs(address)}", "label": label, "kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": address}, "availability": "used",
			"provenance": provenance(MANUAL, PROFILE, CORE, RUNTIME_SOURCE),
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "roles": [role], "normally_closed": False,
			"physical": {
				"location": "coin door and CPU board diagnostic switches", "switch_type": "button",
				"notes": (
					"System 11 diagnostic input on the keyboard port (pinned s11.h S11_SWADVANCE -7, S11_SWUPDN -6, "
					"S11_SWCPUDIAG -5, S11_SWSOUNDDIAG -4). The manual's Test/Diagnostic Procedures enter and step every test "
					"with the ADVANCE button and the AUTO-UP/MANUAL-DOWN switch; the retained runs do the same with -7 and -6."
				),
			},
			"spatial": na("cabinet_or_service", CORE, MANUAL),
		})
	for address in range(1, 65):
		column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
		identifier = f"switch.matrix-{address}"
		rom_name = data.ROM_SWITCH_NAMES[address]
		part, description = data.SWITCH_PARTS[address]
		notes = f"Printed switch-matrix column {column}, row {row}; the ROM's switch table names it \"{rom_name}\"."
		refs: tuple[str, ...] = (MANUAL, ROM_TABLES, RUNTIME_SOURCE, CORE)
		device: dict[str, Any] = {
			"id": identifier, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": address},
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": switch_wiring(address),
		}
		physical: dict[str, Any] = {}
		if address in data.UNUSED_SWITCHES:
			device["label"] = f"Not Used (Matrix Position {address})"
			device["availability"] = "unused"
			notes += (
				" The Switch-Matrix Table prints \"Not Used\" and the Switches list prints \"Not Used\" with no part number; no "
				"switch is fitted. The Switch Levels test still names a closure here, so the ROM scans the position."
			)
			if address == 2:
				notes += (
					" The ROM's name \"G. SCORE BOARD\" suggests a West German scoreboard switch, but no Cyclone source "
					"describes one, and the driver's gameSpecific1 is 0, so PinMAME does not copy the A/C relay into this "
					"address either."
				)
			device["spatial"] = na("unused", MANUAL, RUNTIME_SOURCE)
		else:
			device["label"] = SWITCH_LABELS[address]
			device["availability"] = "optional" if address == 5 else "used"
			device["normally_closed"] = False
			if description and description != device["label"]:
				notes += f" The Switches list prints \"{description}\"."
			if part and part not in ("Not Used", "Not Used (USA)"):
				physical["part_number"] = part
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if address == 5:
				notes += (
					" The Switches list prints its part as \"Not Used (USA)\": a domestic game ships without a centre coin "
					"mechanism, so the input is optional; the ROM still reads it as CENTER COIN SW."
				)
			if address == 8:
				notes += " The list's footnote: the part number is for the entire Diagnostic Switch Assembly, including the high-score reset switch."
			if address == 9:
				notes += (
					" The manual's Game Operation says actuating \"the playfield tilt switch\" loses the ball in play like the "
					"third plumb-bob closure, and in the gameplay run its first closure dropped the enable 23. It is a tilt "
					"contact (B-8306-1), not a ball sensor, so it takes no playfield placement."
				)
			if address == 18:
				notes += (
					" The Switches list identifies it as the C-11903-R 1-bank drop-target opto, listed again among the playfield "
					"underside boards as the 1-b Drop Target Opto Assembly; the matrix sees the opto board's output, not the beam. In the gameplay run the dropped target "
					"(18 = 1) flashed 9, and the ROM pulsed the reset (5) only after the ball reached the boomerang kickbig; the "
					"retained script closes 18 when the target drops and opens it when 5 raises it."
				)
			if address == 41:
				notes += (
					" The Switches list footnotes the part (5490-10159-00 Mystery Wheel Opto) as \"Part of Motor Control Assy, "
					"D-12046\", and the Switch-Matrix Table places it on the backbox insert board; the parts manual lists the "
					"5490-10159-00 Opto Interruptor Module as Opto 1 of the D-12045 Mystery Wheel Opto Positioner board, the "
					"stepper motor control assembly of the C-12036 carousel, and service bulletin SS47 lists D-12046 as a "
					"subassembly of that D-12045 Stepper Control Assembly, so both numbers name the same board. Its schematic "
					"draws the opto switching the matrix row and column pins through a transistor (Q9) rather than as a contact. In the Mystery Wheel Test the "
					"ROM shows \"H\" on the player 4 display while 41 is 0 and no \"H\" while it is 1 (runs wheel-test-41-0 and "
					"wheel-test-41-1); the manual says \"H\" means the home switch is open or the opto is interrupted. A rising "
					"edge of 41 restarted the step count (run wheel-test-reactive). The retained script's cvpmMech (.Length = 200, "
					".Steps = 360, lines 78-79) closes 41 while its reported position is 0-180 of 360, half a turn (line 80)."
				)
			if address in (57, 58):
				side, button = ("left", 84) if address == 57 else ("right", 82)
				notes += (
					f" The {side} Flipper Lane Change switch, a separate part from the cabinet Flipper Button (SW-10A-48). The "
					f"driver's FLIP_SWNO(57,58) without FLIP_SOL makes core_updateSw rewrite this address from PinMAME's flipper "
					f"column, public {button}, on every update, so a write to {address} lasts only until the next update: a "
					f"consumer drives {button}. In the Switch Levels run holding {button} alone showed \"{rom_name}\" with 06 "
					f"{address}, and so did holding {address} by rewriting it on every poll, which overrides the copy."
				)
			if address in (63, 64):
				notes += (
					" The Switches list prints no part number and footnotes \"Paired Kicker Actuating Sw: A-4834-H; B-8734-1\": "
					"the slingshot's own actuating switch, which has no matrix address."
				)
			if address in (60, 61, 62, 63, 64):
				coil = data_special = {60: 17, 61: 19, 62: 21, 63: 18, 64: 20}[address]
				notes += (
					f" Its coil is special solenoid {data_special}. The driver declares no special-solenoid switches "
					f"(sxx.ssSw is empty), so PinMAME never raises {coil} from this switch; in the gameplay run the ROM fired "
					f"{coil} itself, through setSSSol, when this switch closed."
				)
			if address in SWITCH_SCRIPT:
				notes += f" Retained script: {SWITCH_SCRIPT[address]}."
				refs = (MANUAL, ROM_TABLES, RUNTIME_SOURCE, SCRIPT, CORE)
			if address == 41:
				refs = (MANUAL, PARTS, BULLETINS, ROM_TABLES, RUNTIME_SOURCE, SCRIPT, CORE)
			if address not in FLIP_SWNO:
				notes += RUNTIME_SWITCH_NOTE.format(address=address, name=rom_name)
			else:
				notes += (
					" pia4a_r returns core_getSwCol without inversion and the driver declares no inverted switch, so the "
					"contact the matrix sees is open at rest and closed when actuated."
				)
			if address in CABINET_SWITCH_ROLES:
				device["roles"] = [CABINET_SWITCH_ROLES[address]]
				device["spatial"] = na("cabinet_or_service", MANUAL)
			else:
				names = anchors(geometry, "switch", address)
				spatial = located(identifier, "sensor", names, geometry)
				if spatial is not None:
					device["spatial"] = spatial
					notes += placement_note("switch", address, names)
		physical["notes"] = notes
		device["physical"] = physical
		device["provenance"] = provenance(*refs)
		items.append(device)

	column = flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP_SWNO(57,58)",
		core_refs=(CORE, PROFILE), button_refs=(SCRIPT, LIBRARY, RUNTIME_SOURCE),
		button_notes={
			side: (
				f"The retained known-working script drives it: Table1_KeyDown and Table1_KeyUp pass the {side} flipper key to "
				"S11.VBS vpmKeyDown/vpmKeyUp (script lines 110 and 117), which set "
				f"Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'}. In the Switch Levels run holding this address showed "
				f"\"{'LEFT FLIPPER' if side == 'left' else 'RIGHT FLIPPER'}\" with 06 {57 if side == 'left' else 58} and raised "
				f"the synthetic outputs {'47 and 48' if side == 'left' else '45 and 46'}. The physical counterpart is the {side} "
				f"cabinet Flipper Button (SW-10A-48), which fires the flipper coil through the flipper circuit."
			)
			for side in ("left", "right")
		},
		unused_notes=vpm_staged_flipper_notes(), unused_note_refs=(LIBRARY,),
	)
	for item in column:
		if item["availability"] == "used":
			item["normally_closed"] = False
	items.extend(column)
	items.append({
		"id": "switch.dip-0", "label": "Country Jumper W7", "kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": 0}, "availability": "used",
		"provenance": provenance(MANUAL, PROFILE, CORE, SCRIPT, RUNTIME_SOURCE),
		"aliases": [{"namespace": "pinmame.dip", "value": "0"}],
		"physical": {
			"location": "System 11B CPU board", "switch_type": "dip",
			"notes": (
				"System 11's single Country jumper, read as core_getDip(0)<<7 on PIA2 PA7, which pinned s11.c labels \"Jumper "
				"W7\". The manual's ROM and Jumper Table lists W7 among the CPU board's installed jumpers (W1, 2, 4, 5, 7, 8, 11, "
				"14, 16, 17, and 19). pia2a_r is an eight-bit handler, so only bit 0 of the host value reaches PA7: every "
				"retained run used 0 and the ROM ran its English service text. The retained script sets .DIP(0) = &H80 (line "
				"61), which shifts to 0x4000 and reaches PA7 as 0, the same as 0."
			),
		},
		"spatial": na("dip_switch", MANUAL),
	})
	return items


# ---------------------------------------------------------------- outputs

def output_id(address: int) -> str:
	if address in SOLENOID_LABELS:
		return f"device.{slug(SOLENOID_LABELS[address])}"
	if address in VIRTUAL_SOLENOIDS:
		return f"device.{slug(VIRTUAL_SOLENOIDS[address][0])}"
	return f"device.{slug(platform_label(address))}"


def platform_label(address: int) -> str:
	if 33 <= address <= 36:
		return f"Unused Upper Flipper Slot {address}"
	if 37 <= address <= 44:
		return f"Unused Sound Overlay Slot {address}"
	raise KeyError(address)


def coil_test_step(address: int) -> tuple[int, str] | None:
	"""The ROM's Coil Test step and name for a public solenoid address (runtime evidence pairs them)."""
	if 1 <= address <= 8:
		return address, data.ROM_COIL_STEPS[address][0]
	if 25 <= address <= 32:
		return address - 24, data.ROM_COIL_STEPS[address - 24][1]
	if 9 <= address <= 22 and address not in data.COIL_TEST_SKIPPED_STEPS:
		return address, data.ROM_COIL_STEPS[address][0].replace("ApC", "A/C")
	return None


def solenoid_wiring(address: int) -> dict[str, Any]:
	row = data.solenoid_row(address)
	_desc, _kind, wire, cpu, playfield, driver, _part, _qty = data.SOLENOID_TABLE[row]
	if row.endswith(("A", "C")):
		a_cpu = data.SOLENOID_TABLE[row[:2] + "A"][3]
		wiring: dict[str, Any] = {
			"board": "System 11B CPU board through the D-11813 Aux Power Driver Board", "driver_transistor": driver,
			"drive_wire": wire, "drive_connection": playfield,
			"control_connection": a_cpu if row.endswith("A") else f"{a_cpu} (C side, through the A/C Select Relay)",
		}
		if row.endswith("C"):
			wiring["control_wire"] = cpu.strip("()")
		return wiring
	wiring = {"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": wire, "control_connection": cpu}
	if playfield:
		wiring["drive_connection"] = playfield
	return wiring


def build_outputs(geometry: dict[str, Any] | None) -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in list(range(1, 23)) + list(range(25, 33)):
		row = data.solenoid_row(address)
		description, sol_type, _wire, _cpu, _playfield, driver, part, quantity = data.SOLENOID_TABLE[row]
		list_part, list_description = data.SOLENOID_LIST[row]
		identifier = output_id(address)
		label = SOLENOID_LABELS[address]
		printed = f"\"{description}\"" if description else "a blank description"
		notes = f"Solenoid Table row {row} ({printed}, type {sol_type}"
		notes += f", part {part}" if part else ", no part"
		notes += f", quantity {quantity})." if quantity else ")."
		if list_description != description or list_part != part:
			if not (list_description or list_part):
				notes += " The Solenoids/Flashers list leaves the row blank."
			else:
				notes += f" The Solenoids/Flashers list prints \"{list_description}\""
				notes += f" with part \"{list_part}\"." if list_part else " with no part."
		if row.endswith(("A", "C")):
			pair = int(row[:2])
			notes += (
				f" Switched pair {pair:02d}A/{pair:02d}C on driver {driver}: the A load is pulsed with the A/C Select Relay (12) "
				f"released and the C load with it energized (the manual's A/C relay note). Pinned updsol publishes the A load "
				f"at {pair} and the C load at {pair + 24}."
			)
		step = coil_test_step(address)
		if step is not None:
			notes += (
				f" The ROM's Coil Test (run coil-test) pulses this address at step {step[0]:02d} while the player 1 and 2 "
				f"displays show \"{step[1]}\"."
			)
		refs: tuple[str, ...] = (MANUAL, ROM_TABLES, RUNTIME_SOURCE, CORE)
		physical: dict[str, Any] = {}
		roles: list[str] = []
		spatial: dict[str, Any] | None = None
		if address in UNUSED_SOLENOIDS:
			notes += (
				" No load is fitted: the Solenoid Table leaves the row's description and part cells blank while still printing "
				"its wire, pins and driver, the Solenoids/Flashers list leaves the row blank, and the ROM's own coil-test record "
				"reads NOT USED. The only state any run published here is that Coil Test pulse, the ROM stepping every driver."
			)
			physical["notes"] = notes
			items.append({
				"id": identifier, "label": label, "kind": "coil", "binding": {"group": "pinmame.output.solenoid", "device": address},
				"availability": "unused", "provenance": provenance(*refs),
				"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": row}],
				"physical": physical, "wiring": solenoid_wiring(address), "spatial": na("unused", MANUAL, RUNTIME_SOURCE),
			})
			continue
		kind = SOLENOID_KIND[address]
		if part and not part.startswith("#"):
			physical["part_number"] = part
		if address in PARTS_MANUAL_COILS:
			physical["part_number"], assembly = PARTS_MANUAL_COILS[address]
			if physical["part_number"] != part:
				notes += (
					f" The Solenoid Table prints its coil as {part}, while the Solenoids/Flashers list and the parts manual's "
					f"{assembly} listing give {physical['part_number']}; the part number follows the two that agree, which also "
					"give both kickers AE-26-1500 and all three jet bumpers AE-23-800. The Solenoid Table's 20 and 21 part cells "
					"are swapped."
				)
			else:
				notes += f" The parts manual's {assembly} listing gives the same coil."
		if address in FLASHLAMP_QUANTITY:
			backbox, playfield_count = FLASHLAMP_QUANTITY[address]
			physical["quantity"] = backbox + playfield_count
			if backbox:
				notes += (
					f" Of its {backbox + playfield_count} bulbs, {backbox} {'is' if backbox == 1 else 'are'} in the backbox (the "
					f"table's \"b\") and {playfield_count} on the playfield (\"p\"); only playfield bulbs take placements."
				)
		if 9 <= address <= 16:
			notes += " Every controlled output 9-16 shows one 50 ms pulse about 0.26 s after power-up, before the ROM initializes PIA0; it is a property of the port, not a drive."
		if 17 <= address <= 21:
			notes += (
				f" Special #{address - 16}: the driver declares no special-solenoid switch, so PinMAME publishes it only when "
				"the ROM drives its PIA control line (setSSSol, WMS order), as the Coil Test and gameplay runs show. The "
				"retained table's VPX bumper or slingshot fires on its own and the script has no callback for it."
			)
		if address == 7:
			notes += " The Solenoid Table and the list place the knocker (or a ticket dispenser) in the backbox."
			roles = ["cabinet.knocker"]
			spatial = na("cabinet_or_service", MANUAL)
		elif address == 9:
			notes += (
				" The Solenoid Table names it the Spook House Bonus Flasher, while the Solenoids/Flashers list (\"Spins Mystery "
				"Wheel (pf)\") and the ROM's coil-test name (\"SPIN M.W. FLASHER\") agree on the Spins Mystery Wheel flasher; the "
				"label follows the two that agree. Pinned PinMAME types it as a #89 bulb."
			)
		elif address == 10:
			notes += (
				" The relay (5580-09555-01 on the C-11998-1 relay board under the playfield, the list's footnote) switches the "
				"playfield general illumination; energized means G.I. off. The manual prints no G.I. bulb count or layout."
			)
			roles = ["gi.playfield"]
		elif address == 11:
			notes += (
				" The relay (5580-09555-01) switches the backglass general illumination; its drive leaves through the backbox "
				"connector 6J3-1. Energized means G.I. off."
			)
			roles = ["gi.backbox"]
			spatial = na("cabinet_or_service", MANUAL)
		elif address == 12:
			notes += (
				" The A/C select relay (5580-09555-01, the list's footnote: \"In backbox on Aux Power Driver Bd, D-11813\"). "
				"Pinned PinMAME publishes its own state here and, while it is set, moves the low solenoid byte to 25-32. The "
				"driver's gameSpecific1 is 0, so no switch mirrors it."
			)
			roles = ["internal.ac-select-relay"]
			spatial = na("internal_nonvisual", MANUAL, CORE)
		elif address in (13, 14):
			other = 14 if address == 13 else 13
			notes += (
				f" One of the two stepper outputs of the backbox Mystery Wheel, with {other}; the drive leaves through the "
				"backbox connector board (6J2). The Solenoid Table's part cell prints 14-7948/D-12045, and the parts manual "
				"lists D-12045 as the Mystery Wheel Opto Positioner board (\"Control Assy, Stepper Motor\" in the C-12036 "
				"Carousel Assembly), which carries transistors Q1-Q9 and the home opto. Service bulletin SS47's schematic draws "
				"that board taking two logic inputs, input A and input B, each steering one winding of the two-winding stepper "
				"motor; which of 13 and 14 reaches which input is not printed. The Solenoid Table prints 13 as Coil B and 14 as Coil "
				"A, while the Solenoids/Flashers list prints 13 as Coil A and 14 as Coil B. The letter decides which winding each "
				"output steers, and so the wheel's direction for a given phase sequence; the label follows the Solenoid Table, "
				"which carries the wiring. The retained script's stepper model (cvpmMech with vpmMechStepSol, .Sol1 = 14 and "
				".Sol2 = 13, lines 75-77) does not settle the letters: pinned mech.c moves a two-step-solenoid mech whenever "
				"either input changes (dir = sol != last), so swapping the two slots gives the same motion. The playfield "
				f"connection cell \"6J2-3 (B'box Conn Bd)\" is printed for 13 and \"6J2-4\" for 14. See the Mystery Wheel "
				"mechanism."
			)
			roles = ["cabinet.backbox-toy"]
			spatial = na("cabinet_or_service", MANUAL)
		elif address == 15:
			notes += " Three #1251 lamps on the playfield at the boomerang loop; pinned PinMAME types the output as a #89 bulb."
		elif address == 16:
			notes += (
				" The output energizes a relay (5580-12145-01 on the C-11902-1 relay board under the playfield, the list's "
				"footnote) that switches the Ferris wheel motor (14-7941-3, C-11900 Ferris Wheel/Motor Assembly). The matrix "
				"has no Ferris wheel position switch. See the Ferris wheel mechanism."
			)
		if address in SOLENOID_RUNTIME:
			notes += " " + SOLENOID_RUNTIME[address]
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
			refs = (MANUAL, ROM_TABLES, RUNTIME_SOURCE, SCRIPT, CORE)
		elif not 17 <= address <= 21:
			notes += " The retained script has no callback for this address."
		if spatial is None:
			names = anchors(geometry, "solenoid", address)
			role = "emitter" if kind in ("flasher", "gi", "lamp") else "effect"
			spatial = located(identifier, role, names, geometry)
			if spatial is not None:
				notes += placement_note("solenoid", address, names)
		if address in PARTS_MANUAL_COILS or address in (13, 14, 16):
			refs = (*refs, PARTS)
		if address in (13, 14):
			refs = (*refs, BULLETINS)
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": row}]
		if 17 <= address <= 22:
			aliases.append({"namespace": "manual.special-solenoid", "value": f"Special #{address - 16}"})
		device: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "binding": {"group": "pinmame.output.solenoid", "device": address},
			"availability": "used", "provenance": provenance(*refs), "aliases": aliases, "physical": physical,
			"wiring": solenoid_wiring(address),
		}
		if roles:
			device["roles"] = roles
		if spatial is not None:
			device["spatial"] = spatial
		items.append(device)
	for address in [23, 24, *range(33, 51)]:
		if address in VIRTUAL_SOLENOIDS:
			label, availability, role, notes = VIRTUAL_SOLENOIDS[address]
		elif address <= 36:
			label, availability, role, notes = platform_label(address), "unused", "internal.unused-platform-slot", UPPER_FLIPPER_NOTE
		else:
			label, availability, role, notes = platform_label(address), "unused", "internal.unused-platform-slot", OVERLAY_NOTE
		refs = (PROFILE, CORE)
		if availability == "used":
			refs = (PROFILE, CORE, RUNTIME_SOURCE, SCRIPT) if address in (23, 45) else (PROFILE, CORE, RUNTIME_SOURCE)
		items.append({
			"id": output_id(address), "label": label, "kind": "virtual", "binding": {"group": "pinmame.output.solenoid", "device": address},
			"availability": availability, "provenance": provenance(*refs),
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}], "roles": [role], "physical": {"notes": notes},
			"spatial": na("virtual", CORE),
		})
	for address in range(1, 65):
		column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
		column_q, column_wire, column_pin = data.LAMP_COLUMNS[column]
		row_q, row_wire, row_pin = data.LAMP_ROWS[row]
		identifier = f"lamp.matrix-{address}"
		notes = (
			f"Printed lamp-matrix column {column}, row {row}. In the Single Lamps test (run single-lamps) designator "
			f"{address:02d} blinks this address alone while the player 1 and 2 displays show the ROM's name "
			f"\"{data.ROM_LAMP_NAMES[address]}\"."
		)
		if data.LAMP_LIST[address] != data.LAMP_MATRIX[address]:
			notes += f" The Lamps list prints \"{data.LAMP_LIST[address]}\"."
		device = {
			"id": identifier, "label": LAMP_LABELS[address], "kind": "lamp", "binding": {"group": "pinmame.output.lamp", "device": address},
			"availability": "used", "provenance": provenance(MANUAL, ROM_TABLES, RUNTIME_SOURCE, CORE),
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}],
			"wiring": {
				"board": "System 11B CPU board lamp matrix", "drive_wire": column_wire, "drive_connection": column_pin,
				"return_wire": row_wire, "return_connection": row_pin, "driver_transistor": f"column {column_q}, row {row_q}",
			},
		}
		if address in data.BACKGLASS_LAMPS:
			if 33 <= address <= 48:
				notes += (
					" One of the sixteen lamps of the backbox Mystery Wheel, spaced 22.5 degrees apart clockwise from top dead "
					"centre (33) as the Lamp-Matrix Table prints them; the table's heading lists 33-48 and 55-64 as backglass lamps."
				)
				device["roles"] = ["cabinet.backbox-toy"]
			else:
				notes += " A backglass lamp: the Lamp-Matrix Table lists 33-48 and 55-64 as backglass lamps."
				device["roles"] = ["cabinet.backglass"]
			device["spatial"] = na("cabinet_or_service", MANUAL)
		else:
			if 27 <= address <= 32:
				notes += (
					" The Lamps drawing's balloon 27-32 points above the rear rail, at the panel standing at the top of the "
					"playfield; the retained table also models the COMET lamps there, on its back panel."
				)
			notes += (
				" A playfield lamp. It has no placement: no retained Cyclone table models a bulb for it (the lights vpmMapLights "
				"binds to the lamps model none), so no table marks its socket."
			)
		physical: dict[str, Any] = {"notes": notes}
		if address == 9:
			physical["notes"] += (
				" The Lamp-Matrix Table marks this cell alone with a boxed 2 and the legend \"Two Lamps\", so the address "
				"drives two bulbs."
			)
			physical["quantity"] = 2
		device["physical"] = physical
		items.append(device)
	return items


# ---------------------------------------------------------------- mechanisms

def build_mechanisms() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[int], sensors: list[int], behavior: str, *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": [output_id(a) for a in actuators],
			"sensors": [f"switch.matrix-{s}" for s in sensors], "behavior": behavior, "provenance": provenance(*refs),
		}
		if assembly:
			record["assembly_part_number"] = assembly
		return record

	m = (MANUAL, RUNTIME_SOURCE, SCRIPT, CORE)
	i = (MANUAL, IPDB, RUNTIME_SOURCE, SCRIPT, CORE)
	mechanisms = [
		mechanism(
			"mechanism.outhole", "Outhole kicker and shooter lane", "kicker", [1], [10, 25],
			"A drained ball rests on the outhole switch (10, 17-1067) and the Outhole Kicker (1, AE-23-800) kicks it out; the "
			"ball is served to the shooter lane, whose switch (25, 5647-12073-04) it rests on until plunged. The matrix has no "
			"ball-trough switch and the Solenoid Table no ball-release coil, so the outhole kick is the only serve the CPU "
			"controls; the playfield underside drawing labels a ball trough area. In the gameplay run Start raised the enable 23 "
			"and the ROM kicked the outhole, repeated the kick 2.09 s later while 10 stayed closed, and after the drain kicked "
			"6.18 s later, once the bonus count had run; with 10 held from power-up and no game started it never fired.",
			*m,
		),
		mechanism(
			"mechanism.shooter-skill-shot", "Shooter channel skill shot and shooter-lane kickbig", "kicker", [3], [30, 29, 28, 27, 26],
			"IPDB: \"Shooter channel has elevated skill shot to drop ball to a kicker which propels ball into play.\" The "
			"plunged ball climbs the elevated shooter channel past the Shuttle switches 5K (30, topmost), 25K (29, upper), 100K "
			"(28) and 25K (27, lower) and drops into the Shuttle 10K kickbig (26, 5647-12133-01), from which the Ball Shooter "
			"Kickbig (3, AE-24-900; B-11051-R Shooter Lane Kickbig on a B-11052 mounting) kicks it into play. In the gameplay run "
			"the ROM fired 3 1.07 s after 26 closed, and with 26 held from power-up it fired every 3.1-3.3 s. The retained table "
			"models the channel with the triggers sw26-sw30 in a line on the right and the KSalida kicker below them.",
			MANUAL, PARTS, IPDB, RUNTIME_SOURCE, SCRIPT, CORE, assembly="B-11051-R with B-11052",
		),
		mechanism(
			"mechanism.center-drop-target", "Spook House drop target", "drop_target_bank", [5], [18],
			"A single drop target in the centre of the playfield (C-11903-R 1-b Drop Target Opto Assembly; the ROM's C. DROP "
			"TARGET), reset by the Drop Target coil (5, AE-23-800). IPDB: \"The drop target guards a cellar hole which feeds the "
			"scoop.\" Knocking it down (18 = 1) flashed the Spins Mystery Wheel flasher (9) in the gameplay run; the ROM raised "
			"it only once the ball had passed the cellar hole (11) and reached the boomerang kickbig (13), pulsing 5 twice "
			"before and twice after the kickbig fired, and again at the start of each later ball.",
			*i, assembly="C-11903-R",
		),
		mechanism(
			"mechanism.boomerang", "Spook House cellar hole and boomerang kickbig", "kicker", [4], [11, 13],
			"Behind the drop target a cellar hole takes the ball past the Score Spook House switch (11, 5647-12073-01) to the "
			"Boomerang Kickbig (13, 5647-12073-09), from which the kickbig coil (4, AE-26-1500; B-11051-R Boomerang Kickbig on a "
			"B-11052 mounting) kicks it round the B-11984 Boomerang Loop Assembly. The three #1251 Boomerang Flashers (15) light "
			"the loop. In the gameplay run 11 spun the Mystery Wheel (13 and 14 from 63.11 to 63.83 s); with the ball held on "
			"13 the ROM flashed 15 eight times, pulsed the drop-target reset twice and fired 4 5.25 s after 13 closed. With 13 "
			"held from power-up it fired 4 every 1.55-1.67 s. Service bulletin SS52 (October 1988) places the Spookhouse Ramp "
			"at the left middle of the playfield, secured to the bottom of the playfield below the Spookhouse entrance hole, "
			"with a cushion plate (A-12222) inside under the entrance, and adds a Ramp Support Bracket (A-12407) at its end "
			"against breakage. The retained table kicks the ball from its sw13 kicker.",
			MANUAL, PARTS, BULLETINS, IPDB, RUNTIME_SOURCE, SCRIPT, CORE, assembly="B-11051-R with B-11052 and B-11984",
		),
		mechanism(
			"mechanism.ferris-wheel", "Rotating Ferris wheel", "motorized", [16], [17],
			"IPDB lists a \"Rotating playfield Ferris wheel\" among the notable features and a Ferris Wheel toy, and notes that "
			"\"The Ferris wheel on the playfield carries the ball for a portion of its rotation.\" The C-11900 "
			"Ferris Wheel/Motor Assembly stands at the top left of the playfield (the retained table's RedWheel); the parts "
			"manual lists the Ferris wheel (03-8124) and its cover, turned through a drive belt (03-8145) and pulley (03-8086) "
			"by the 14-7941-3 motor of the B-11571-2 Motor Assembly. A relay (5580-12145-01 on the C-11902-1 relay board, "
			"solenoid 16) switches the motor; the ball enters at the Ferris Wheel Entrance "
			"switch (17, 5647-12073-10). The matrix has no position switch, so the ROM runs the motor without feedback. At "
			"power-up the ROM ran the motor from 2.33 to 11.77 s; in the gameplay run it ran it from Start until 9.5 s after "
			"the last switch closure and restarted it with the next closure. The retained table turns its RedWheel primitive one "
			"degree per FWTimer tick while 16 is on, opens FerrisBlockedWall in four angle windows per turn, and carries a "
			"ball that reaches Trigger2 on an arc (lines 711-723 and 755-779). Service bulletin SS50 (July 1988) traces a wheel "
			"that does not turn properly to an over-lubricated belt and pulleys slipping, names a white pulley, a metal "
			"Ferris wheel bracket, a ball-support bar under the wheel and a two-cavity power plug on the motor. How the "
			"physical wheel takes and releases the ball is not printed in the manuals or bulletins.",
			MANUAL, PARTS, BULLETINS, IPDB, RUNTIME_SOURCE, SCRIPT, TABLE, CORE, assembly="C-11900",
		),
		mechanism(
			"mechanism.mystery-wheel", "Backbox Mystery Wheel", "motorized", [13, 14], [41],
			"IPDB: \"Mechanical backbox animation (ferris wheel revolves).\" The parts manual's Mystery Wheel Carousel Assembly "
			"(C-12036) is a carousel wheel (03-8161) on a motor and connector assembly (B-12088) with a stepper motor control "
			"assembly (D-12045), the Mystery Wheel Opto Positioner board that carries the opto interruptor module "
			"(5490-10159-00, Opto 1) and transistors Q1-Q9; service bulletin SS47 lists its D-12046 subassembly and draws its "
			"schematic. The CPU's outputs 13 and 14 reach the board as two logic inputs (input A and input B), each steering "
			"one winding of the two-winding stepper motor through a comparator-driven transistor bridge, so their levels, not "
			"pulses, set the motor's phase; which output feeds which input is not printed (the Solenoid Table prints their "
			"part as 14-7948/D-12045). The opto reports at switch 41, and the sixteen lamps 33-48 sit round the wheel at "
			"22.5-degree steps. The manual's Mystery Wheel Test (08) shows the last known position on the player 2 display, the "
			"home state (\"H\") and the step count (1-200, up to 256 with a failed home switch) on player 4, and the error count "
			"on player 3; the wheel stops on the next counterclockwise position when the home switch works. In the retained "
			"runs the ROM raised 13 and 14 together, dropped each briefly in turn while stepping, counted to 256 and "
			"reported errors with 41 held at either level, "
			"showed \"H\" only with 41 at 0, and restarted its count on a rising edge of 41. In the gameplay run the Score Spook "
			"House switch (11) held 13 and 14 on together for 0.72 s. The retained script models the wheel as a cvpmMech stepper (Sol1 14, "
			"Sol2 13; .Length = 200 and .Steps = 360, so pinned mech.c wraps its position at 200 and reports it on a "
			"360-position scale) with 41 closed over reported positions 0-180; the physical home flag's width and the motor's "
			"steps per turn are not printed.",
			MANUAL, PARTS, BULLETINS, IPDB, RUNTIME_SOURCE, SCRIPT, CORE, assembly="C-12036",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other", [17, 19, 21], [60, 61, 62],
			"Three jet bumpers (B-9414-1 above the playfield, B-9415-1 coil assembly with the AE-23-800 coil beneath it, "
			"SW-11A-37 switches): Left (17, switch 60), Right (19, switch 61) and Bottom (21, switch 62), special solenoids 1, 3 "
			"and 5. The driver maps no special-solenoid switch, so in PinMAME the ROM fires each coil after reading its switch; "
			"the gameplay run showed each pair.",
			MANUAL, PARTS, RUNTIME_SOURCE, SCRIPT, CORE, assembly="B-9414-1/B9415-1",
		),
		mechanism(
			"mechanism.slingshots", "Left and right kickers (slingshots)", "other", [18, 20], [63, 64],
			"Two B-9463 kicker arm assemblies with AE-26-1500 coils (the parts manual): Left (18, scoring switch 63) and Right "
			"(20, scoring switch 64), special solenoids 2 and 4. The Switches list footnotes a paired kicker actuating switch "
			"(A-4834-H; B-8734-1) with no matrix address. In PinMAME the ROM fires each coil after reading its scoring switch, "
			"as the gameplay run showed.",
			MANUAL, PARTS, RUNTIME_SOURCE, SCRIPT, CORE, assembly="B-9463",
		),
		mechanism(
			"mechanism.flippers", "Two flippers with lane-change switches", "other", [], [57, 58],
			"Two lower flippers (C-11626-L-4 and C-11626-R-4, FL 11630-50VDC coils) fired from the cabinet Flipper Buttons "
			"(SW-10A-48) through the flipper circuit, so no Sol. No. is printed and PinMAME fabricates 45-48 from the buttons at "
			"public 82 and 84. Each flipper has a Flipper Lane Change switch (57 left, B-9951-1; 58 right, B-9951) whose "
			"drawing balloon points at the flipper; core_updateSw copies them from 84 and 82.",
			*m, assembly="C-11626-L-4 with C-11626-R-4",
		),
		mechanism(
			"mechanism.ramps", "Comet and Cyclone ramps", "other", [], [31, 32, 34],
			"The clear Comet ramp has an entry switch (31, SW-1A-171) and a scoring switch (32, 5647-12133-04) with RIDE THE "
			"COMET (8) on the ramp, while the COMET value lamps 27-32 stand above the rear rail; the clear Cyclone ramp has a "
			"scoring switch (34, 5647-12133-07). IPDB counts two ramps. Service bulletin SS49 (July 1988) adds a red post "
			"(03-8044-9) and a 2\" rubber ring (23-6305) stretched between two red posts by the \"Ken's Vending\" plastic, "
			"to stop balls sticking between the playfield plastic and the Cyclone ramp; machines built or serviced after it "
			"carry them. The retained script tilts a switch-wire primitive at 32 and 34.",
			MANUAL, BULLETINS, IPDB, RUNTIME_SOURCE, SCRIPT, CORE,
		),
		mechanism(
			"mechanism.targets-and-lanes", "Ducks, Ball Toss, top lanes, outlanes and rubber switches", "other", [],
			[14, 15, 16, 19, 20, 21, 22, 23, 24, 35, 36, 37, 53, 54, 55, 56, 59],
			"Three Duck targets (19-21, B-12039-5) and three Ball Toss targets (22-24, B-11696-5) with a Spot Ball Toss target "
			"(59, B-12001-4); the 1-2-3 gate lanes at the top (14-16, 5647-12073-10, lamps 14-16); left and right outlanes "
			"(53, 54) and return lanes (55, 56); and three 10-point rubber switches on the right (35-37, B-4834-K). The "
			"retained script never writes 59: its sw59_Hit pulses 25 instead.",
			*m,
		),
		mechanism(
			"mechanism.general-illumination", "Playfield and backglass G.I. relays", "other", [10, 11], [],
			"Two relays (5580-09555-01) switch the general illumination: 10 the playfield's (on the C-11998-1 relay board under "
			"the playfield) and 11 the backglass's. Energizing either turns its G.I. off; pinned PinMAME types both as "
			"reverse-acting 6.3 V AC G.I. outputs.",
			MANUAL, RUNTIME_SOURCE, SCRIPT, CORE,
		),
		mechanism(
			"mechanism.ac-select", "Solenoid A/C select relay", "other", [12], [],
			"The A/C Select Relay (12) on the D-11813 Aux Power Driver Board switches each of the eight switched drivers (Q22-Q25, "
			"Q30-Q33) between its A load, while it is released, and its C load, while it is energized. Pinned PinMAME publishes "
			"the C loads separately at 25-32.",
			MANUAL, RUNTIME_SOURCE, CORE,
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other", [7], [],
			"The A-side load of pair 07 (7, AE-26-1200) is the knocker in the backbox; the Solenoid Table allows a ticket "
			"dispenser in its place.",
			MANUAL, RUNTIME_SOURCE, SCRIPT, CORE,
		),
	]
	relationships = flipper_column_relationships(
		flip_swno=FLIP_SWNO, matrix_ids={57: "switch.matrix-57", 58: "switch.matrix-58"}, refs=(CORE, RUNTIME_SOURCE),
	)
	return mechanisms, relationships


# ---------------------------------------------------------------- sources

def excerpt_records(root: Path = ROOT) -> dict[str, dict[str, Any]]:
	records = {}
	for key, (filename, locator) in EXCERPT_FILES.items():
		path = EXCERPTS / filename
		record: dict[str, Any] = {
			"id": f"excerpt.cyclone.{key}", "locator": locator, "path": path.as_posix(), "sha256": EXCERPT_DIGESTS[key],
			"method": "manual", "transcribed_by": "curator, read from the rendered pages", "reviewed": True,
		}
		if key == "rom-name-tables":
			record.update(method="mixed", transcribed_by="tools/cyclone_rom_name_tables.py, checked against the Switch Levels, Single Lamps and Coil Test displays")
		elif key in ("pinmame-contract", "script-contract", "script-library"):
			record.update(method="manual", transcribed_by="curator, copied verbatim from the pinned source")
		records[key] = record
	return records


def build_sources(root: Path, geometry: dict[str, Any] | None) -> list[dict[str, Any]]:
	excerpts = excerpt_records(root)
	runtime = load_json(root / RUNTIME)
	harness = f"external:pinmame-review-artifacts/{REVIEW_FOLDER}/harness"
	sources: list[dict[str, Any]] = [
		{
			"id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": data.PINMAME_REVISION,
			"locator": "Pinned PinmameGetGames catalog records cycln_l5 (root), cycln_l4 and cycln_l1 (clones of cycln_l5)",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/tree/{data.PINMAME_REVISION}", "revision": data.PINMAME_REVISION,
			"locator": (
				"src/wpc/driver.c lines 2767-2769 (cycln drivers); src/wpc/s11games.c INITGAME macro (lines 33-36) and the "
				"Cyclone block (lines 500-530: INITGAME(cycln, GEN_S11B, s11_dispS11b1, 12, FLIP_SWNO(57,58), 0,0) and the three "
				"ROM sets); src/wpc/s11.c s11_dispS11a, the special-solenoid loop, pia2a_r (Jumper W7), setSSSol, updsol, "
				"pia0cb2_w, the setSSSol PIA handlers, pia4a_r, the diagnostic keys, output sizing and the cycln_ output-type "
				"block; s11.h; gen.h; core.h; core.c core_updateSw's FLIP_SWNO copy and synthetic flipper outputs, core_getDip"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors", "excerpts": [excerpts["pinmame-contract"]],
		},
		{
			"id": PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
			"locator": (
				"System 11 sequential switch and lamp matrices, the diagnostic inputs -7 to -4, the Country jumper, the A/C mux "
				"alias bank, the special solenoids, the sound-overlay range, synthetic flipper outputs and the 81-88 flipper column"
			),
			"license": "MIT", "attribution": "pinmame-game-defs curation",
		},
		{
			"id": MANUAL, "kind": "manual",
			"uri": f"https://web.archive.org/web/20240406112543id_/https://www.ipdb.org/files/617/{MANUAL_FILENAME}",
			"original_filename": MANUAL_FILENAME, "sha256": MANUAL_SHA256, "acquired_at": "2026-10-31T06:29:53Z", "source_id": "ipdb.617",
			"locator": (
				"IPDB machine 617 (Williams Cyclone, model 564; machine page https://www.ipdb.org/machine.cgi?id=617, resource "
				f"https://www.ipdb.org/files/617/{MANUAL_FILENAME}) downloaded through the Internet Archive capture "
				"20240406112543 because IPDB is Cloudflare-gated: the 66-page Williams CYCLONE Instruction Manual 16-564-101 "
				"(February 1988) with schematics, image-only scans with no text layer; a Windows OCR pass was used only to "
				"find pages. The printed folio \"CYCLONE n\" is PDF page n + 4. PDF 2 ROM and Jumper Table and Solenoid Table; "
				"PDF 9 Game Operation; PDF 30-35 Test/Diagnostic Procedures with the Lamp-Matrix Table (PDF 31) and the "
				"Switch-Matrix Table (PDF 34); PDF 40, 43, 44 and 45 the Switches, Lamps and Solenoids/Flashers lists and the "
				"playfield underside boards. Retained at external:pinmame-manuals/by-machine/williams.cyclone.1988/ipdb-617/, "
				"with 300 dpi renders of every page in the sibling rendered-native/manual/. Exact pages in the excerpts."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Pinball Database",
			"excerpts": [excerpts[key] for key in MANUAL_EXCERPTS],
		},
		{
			"id": PARTS, "kind": "manual",
			"uri": f"https://web.archive.org/web/20240406112543id_/https://www.ipdb.org/files/617/{PARTS_FILENAME}",
			"original_filename": PARTS_FILENAME, "sha256": PARTS_SHA256, "acquired_at": "2026-10-31T06:30:00Z", "source_id": "ipdb.617",
			"locator": (
				"IPDB machine 617 (resource "
				f"https://www.ipdb.org/files/617/{PARTS_FILENAME}) downloaded through the Internet Archive capture "
				"20240406112543: the 22-page Williams CYCLONE Parts Information Manual 16-564-102 (March 1988), image-only scans; "
				"a Windows OCR pass was used only to find pages. The printed folio \"CYCLONE n\" is PDF page n + 2. PDF 10 the Top "
				"P'fld Panel (D-12047) and Mystery Wheel Opto Positioner (D-12045) boards; PDF 13 the Jet Bumper Coil Assembly; "
				"PDF 14 the Ferris Wheel Assembly; PDF 15 the Kicker Arm and kickbig assemblies; PDF 17 the Mystery Wheel "
				f"Carousel Assembly. Retained at external:pinmame-manuals/{MANUAL_FOLDER.as_posix()}/, with 200 dpi renders of every "
				"page in the sibling rendered-native/parts/."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Pinball Database",
			"excerpts": [excerpts["parts-assemblies"]],
		},
		{
			"id": BULLETINS, "kind": "service_bulletin",
			"uri": f"https://web.archive.org/web/20240406112543id_/https://www.ipdb.org/files/617/{BULLETINS_FILENAME}",
			"original_filename": BULLETINS_FILENAME, "sha256": BULLETINS_SHA256, "acquired_at": "2026-10-31T06:30:03Z", "source_id": "ipdb.617",
			"locator": (
				f"IPDB machine 617 (resource https://www.ipdb.org/files/617/{BULLETINS_FILENAME}) downloaded through the "
				"Internet Archive capture 20240406112543: a 34-page Williams service bulletin book whose PDF pages 7-12 (book "
				"pages 5-10) are the Cyclone bulletins SS47 (July 27, 1988, the Mystery Wheel stepper control assembly D-12045 "
				"and its schematic), SS49 (July 25, 1988, an added post and ring at the Cyclone ramp), SS50 (July 25, 1988, "
				"Ferris wheel belt and pulleys) and SS52 (October 13, 1988, Spookhouse ramp support bracket). Image-only scans; "
				"a Windows OCR pass was used only to find pages. Retained at "
				f"external:pinmame-manuals/{MANUAL_FOLDER.as_posix()}/, with 300 dpi renders of every page in the sibling "
				"rendered-native/bulletins/."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Pinball Database",
			"excerpts": [excerpts["service-bulletins"]],
		},
		{
			"id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=617", "sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-10-31T06:29:05Z",
			"locator": (
				"IPDB machine 617 through the Internet Archive capture https://web.archive.org/web/20230517161009id_/https://www.ipdb.org/machine.cgi?id=617, "
				f"retained as external:pinmame-manuals/{MANUAL_FOLDER.as_posix()}/{IPDB_PAGE}: Cyclone, Williams, February 24, "
				"1988, model number 564, Williams System 11B, 9,408 units; notable features flippers (2), pop bumpers (3), ramps (2), "
				"drop target (1), scoop (1), ball kicker (1), rotating playfield Ferris wheel (1); \"Shooter channel has elevated "
				"skill shot to drop ball to a kicker which propels ball into play. The drop target guards a cellar hole which feeds "
				"the scoop. Mini-post screw between flippers. Mechanical backbox animation (ferris wheel revolves).\"; toy: Ferris "
				"Wheel; design by Barry Oursler. Notes: \"The Ferris wheel on the playfield carries the ball for a portion of its "
				"rotation.\" and \"Included in this listing are three pictures of a game for the Japanese market, coined for yen. "
				"The backbox has a spinning light show instead of the mechanical spinning wheel. We do not know how many of these "
				"were made.\" Production Run Records: start Feb-24-1988, end Aug-11-1988, quantity 9408."
			),
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database",
		},
		{
			"id": ROM_TABLES, "kind": "rom_static_analysis", "uri": "internal:tools/cyclone_rom_name_tables.py",
			"sha256": data.ROM_U27["cycln_l5"][1],
			"locator": (
				"The lamp, switch and coil-test name tables of the U27 game ROMs of cycln_l5 (cycl_u27.l5, SHA-256 "
				f"{data.ROM_U27['cycln_l5'][1]}), cycln_l4 (cycl_u27.l4, {data.ROM_U27['cycln_l4'][1]}) and cycln_l1 "
				f"(cycl_u27.l1, {data.ROM_U27['cycln_l1'][1]}), decoded by tools/cyclone_rom_name_tables.py from the local "
				"archives: 14-byte records, the switch table read in place and the lamp and coil names through the ROM's own "
				"pointer tables. The three decode to identical text at identical offsets. No ROM bytes are reproduced."
			),
			"license": "NOASSERTION", "attribution": "Decoded locally from the user-authorized ROM corpus; ROM bytes remain external",
			"excerpts": [excerpts["rom-name-tables"]],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME.as_posix()}", "sha256": sha256(root / RUNTIME),
			"revision": data.PINMAME_REVISION,
			"locator": (
				"Compact evidence recomputed by tools/cyclone_runtime_evidence.py from nine LibPinMAME harness runs of cycln_l5, "
				"each in a newly created state directory with its own NVRAM initialization: the Coil Test, the Single Lamps test "
				"stepped through designators 01-64, the Switch Levels test over public 1-64 and 81-88, three Mystery Wheel Test "
				"runs (41 held at 0, held at 1, and one closure), two power-up probes and a scripted gameplay run. Library "
				f"SHA-256 {data.LIBRARY_SHA256}, ROM archive {data.ROM_ARCHIVE_SHA256['cycln_l5']}; raw runs under {harness}, "
				f"manifest SHA-256 {runtime['source']['sha256']}; every cited display frame is pinned in "
				"tools/seeds/williams/cyclone-1988-display-frames.json."
			),
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation; ROM bytes and NVRAM excluded",
		},
		{
			"id": RUNTIME_L4_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_L4.as_posix()}", "sha256": sha256(root / RUNTIME_L4),
			"revision": data.PINMAME_REVISION,
			"locator": f"The cycln_l4 Coil Test run (ROM archive {data.ROM_ARCHIVE_SHA256['cycln_l4']}), retained beside the L-5 runs under {harness}.",
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation; ROM bytes and NVRAM excluded",
		},
		{
			"id": RUNTIME_L1_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_L1.as_posix()}", "sha256": sha256(root / RUNTIME_L1),
			"revision": data.PINMAME_REVISION,
			"locator": f"The cycln_l1 Coil Test run (ROM archive {data.ROM_ARCHIVE_SHA256['cycln_l1']}), retained beside the L-5 runs under {harness}.",
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation; ROM bytes and NVRAM excluded",
		},
		{
			"id": SCRIPT, "kind": "vpx_script", "known_working": True,
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/{quote(SCRIPT_NAME, safe='/')}",
			"revision": VPXTABLE_SCRIPTS_REVISION, "original_filename": SCRIPT_NAME, "sha256": SCRIPT_SHA256,
			"locator": (
				"Pinned script-corpus copy of the Cyclone table script (1,023 lines; \"Cyclone VP9 by melon. December 2009. Build "
				"For VPX by Sliderpoint 2017\", with a Thalamus 2018-07-24 note). cGameName \"cycln_l5\" (line 42), LoadVPM "
				"\"00990300\", \"S11.VBS\", 1.91 (line 44), HandleMechanics = 0 and .DIP(0) = &H80 (lines 57-61), the Mystery "
				"Wheel cvpmMech (lines 71-83), the solenoid callbacks (lines 127-144 and 380-381) and the switch handlers. It is "
				"the retained table's embedded script apart from indentation, text encoding, the Thalamus comment block (lines "
				"7-11) and line 20 (UseSolenoids = 1 against True), so the embedded script's line numbers are five lower from line "
				"12 on. Runtime authority for the bindings in the excerpt."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "melon; Sliderpoint; Thalamus",
			"excerpts": [excerpts["script-contract"]],
		},
		{
			"id": LIBRARY, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"Retained machine-neutral s11.vbs (VBS v3.61) for the table's LoadVPM \"00990300\", \"S11.VBS\", 1.91: the cabinet "
				"constants (swTilt = 1) and the flipper-column buttons swLRFlip = 82 and swLLFlip = 84."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "VPinMAME script library contributors",
			"excerpts": [excerpts["script-library"]],
		},
	]
	if geometry is not None:
		table = geometry["table"]
		bounds = geometry["bounds"]
		sources += [
			{
				"id": TABLE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{table['path']}",
				"original_filename": Path(table["path"]).name, "sha256": table["sha256"], "acquired_at": "2026-10-31T06:35:46Z",
				"locator": (
					"Retained copy of the Cyclone VPX table v1.5 (melon's VP9 table, built for VPX by Sliderpoint) from the "
					"contributor's table archive, which runs cycln_l5. Its embedded script (SHA-256 "
					f"{table['embedded_script_sha256']}) is the pinned corpus script without the corpus copy's Thalamus comment block "
					"and with UseSolenoids = True, apart from indentation and text encoding. "
					f"Exact playfield bounds left={bounds['left']} top={bounds['top']} right={bounds['right']} bottom={bounds['bottom']}. "
					"Geometry authority for the script-bound objects; neither of the two other retained Cyclone tables models a "
					"lamp bulb either."
				),
				"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "melon; Sliderpoint",
			},
			{
				"id": EXTRACTION, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{table['extraction']}", "sha256": table["manifest_sha256"],
				"acquired_at": "2026-10-31T06:36:43Z",
				"locator": (
					f"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool/: "
					f"{table['file_count']} files, {table['total_bytes']} bytes, produced with vpxtool git:v0.33.3 from the retained "
					"table on 2026-10-31T06:36:43Z (tools/build_external_evidence_manifest.py, game cycln_l5)."
				),
				"license": "NOASSERTION", "attribution": "vpxtool extraction",
			},
		]
	return sources


# ---------------------------------------------------------------- definition

DRIVER_NOTES = {
	"cycln_l5": (
		"Production L-5 game ROMs (cycl_u26.l5, cycl_u27.l5), the known-working script's cGameName. All three drivers select "
		"the same cyclnGameData (GEN_S11B, s11_dispS11b1, A/C relay 12, FLIP_SWNO(57,58)) and the same U21/U22 and U4/U19 sound "
		"ROMs; only the U26 and U27 game ROMs differ. Every service, mechanism and gameplay run was made on this ROM."
	),
	"cycln_l4": (
		"Earlier L-4 game ROMs (cycl_u26.l4, cycl_u27.l4) on the same game data and sound ROMs. Its U27 name tables decode to "
		"the L-5 text at the same offsets, and its Coil Test steps the same 28 pulses with the same names (runtime evidence)."
	),
	"cycln_l1": (
		"Earliest L-1 game ROMs (cycl_u26.l1, cycl_u27.l1) on the same game data and sound ROMs. Its U27 name tables decode to "
		"the L-5 text at the same offsets, and its Coil Test steps the same 28 pulses with the same names (runtime evidence)."
	),
}


def build_drivers(root: Path) -> list[dict[str, Any]]:
	catalog = load_json(root / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items = []
	for driver_id in sorted(data.DRIVER_IDS):
		record = by_id[driver_id]
		item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		item["physical_compatibility"] = "identical"
		item["variant_notes"] = DRIVER_NOTES[driver_id]
		items.append(item)
	return items


def displays() -> list[dict[str, Any]]:
	result = []
	for index, start, identifier, label in (
		(0, 1, "display.player-1", "Player 1 display, seven 16-segment alphanumeric characters"),
		(1, 9, "display.player-2", "Player 2 display, seven 16-segment alphanumeric characters"),
		(2, 21, "display.player-3", "Player 3 display, seven 7-segment digits"),
		(3, 29, "display.player-4", "Player 4 display, seven 7-segment digits"),
	):
		result.append({
			"id": identifier, "label": label, "kind": "segment", "controller_index": index, "segment_start": start, "width": 7, "height": 1,
			"physical_location": "cabinet_or_service", "provenance": provenance(CORE, MANUAL, RUNTIME_SOURCE),
			"spatial": na("cabinet_or_service", CORE, MANUAL),
		})
	return result


def build_definition(root: Path = ROOT) -> dict[str, Any]:
	geometry = load_geometry(root)
	runtime = load_json(root / RUNTIME)
	for path in (RUNTIME, RUNTIME_L4, RUNTIME_L1):
		if load_json(root / path)["source"]["sha256"] != RUNTIME_MANIFEST_SHA256:
			raise RuntimeError(f"Cyclone runtime evidence cites an unexpected raw-run manifest: {path}")
	if runtime["runtime"]["game"] != "cycln_l5":
		raise RuntimeError("Cyclone L-5 runtime evidence names another driver")
	if set(SWITCH_LABELS) | data.UNUSED_SWITCHES != set(range(1, 65)):
		raise RuntimeError("Cyclone switch inventory is incomplete")
	inputs = build_inputs(geometry)
	outputs = build_outputs(geometry)
	mechanisms, relationships = build_mechanisms()
	missing = [] if geometry is not None and geometry.get("complete") else ["spatial_placement"]
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Cyclone", "manufacturer": "Williams", "year": 1988, "kind": "physical_pinball",
			"model_number": "564", "ipdb_id": 617, "opdb_id": "G4O2b-MJpn4",
			**({"playfield": geometry["playfield"] | {"provenance": provenance(TABLE, status="observed")}} if geometry is not None else {}),
		},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
		"coverage": {
			"status": "partial" if missing else "author_ready", "missing": missing,
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
				"physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated",
				"recreation_knowledge": "validated", "display_inventory": "validated", "diagnostic_enumeration": "validated",
				"runtime_observation": "validated", "causal_exercise": "validated", "emulator_normalization": "validated",
				"spatial_placement": "validated" if not missing else ("observed" if geometry is not None else "unknown"),
			},
		},
		"drivers": build_drivers(root), "inputs": inputs, "outputs": outputs, "displays": displays(),
		"mechanisms": mechanisms, "relationships": relationships, "sources": build_sources(root, geometry),
		"knowledge": {"path": KNOWLEDGE.as_posix(), "status": "complete"}, "conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Cyclone device identifiers are not unique: {duplicates}")
	return definition


# ---------------------------------------------------------------- spatial report

SPATIAL_BLOCKERS = [
	"Playfield lamps 1-32 and 49-54 have no placement: none of the three retained Cyclone tables models a lamp bulb. "
	"vpmMapLights binds every lamp to insert-overlay lights (lNa, lNa1) that set no bulb mesh, and the COMET lamps 27-32 "
	"sit on the table's back panel above the playfield. A table that models the insert bulbs, or the manual's lamp "
	"drawing (PDF 43) measured balloon by balloon, would place them.",
	"Flasher circuits 9 (Spins Mystery Wheel), 15 (Boomerang, three #1251 lamps), 25, 26, 27, 28 and 32 have no "
	"placement, and 29 and 30 have one of their two playfield bulbs placed: the retained tables light these through "
	"lights with no flasher dome on the playfield (27's dome Flasher27p and 30's Flasher30p stand on the back panel above "
	"the playfield), and 9 has no light at all.",
	"No placement has been checked against the manual's numbered switch (PDF 40), lamp (PDF 43) and solenoid (PDF 44) "
	"drawings with a callout check, so every table placement stays observed.",
	"Solenoid 10 (playfield G.I.): the placements are the 32 bulb-modelling lights of the table's GI collection; the "
	"manual prints no G.I. bulb count or layout, so they stay observed without a quantity.",
]


def build_report(definition: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
	records = [*definition["inputs"], *definition["outputs"], *definition["displays"]]
	geometry = load_geometry(root)
	return {
		"format": "pinmame-spatial-blockers" if definition["coverage"]["status"] == "partial" else "pinmame-spatial-audit",
		"version": 1, "machine_id": MACHINE_ID,
		"coordinate_convention": "x=0 left, x=1 right; y=0 rear/backglass, y=1 apron; normalized VPX/player view",
		"geometry_seed": GEOMETRY.as_posix() if geometry is not None else None,
		"geometry_seed_sha256": sha256(root / GEOMETRY) if geometry is not None else None,
		"located": [
			{"id": r["id"], "label": r["label"], "binding": r["binding"], "placements": r["spatial"]["placements"]}
			for r in records if isinstance(r.get("spatial"), dict) and "placements" in r["spatial"]
		],
		"unplaced": [{"id": r["id"], "label": r["label"], "binding": r.get("binding")} for r in records if "spatial" not in r],
		"not_applicable": [
			{"id": r["id"], "reason": r["spatial"]["reason"]}
			for r in records if isinstance(r.get("spatial"), dict) and r["spatial"].get("status") == "not_applicable"
		],
		"projections": [{"kind": kind, "address": address, "disclosure": text} for (kind, address), text in sorted(PROJECTIONS.items())] if geometry is not None else [],
		"excluded_objects": [
			"Insert-overlay lights lNa and lNa1 that vpmMapLights binds to the playfield lamps: no bulb mesh",
			"Lights L27-L32 and the COMET overlays on the back panel, and l57-l64 on the backglass, above or behind the playfield",
			"GILight32-34, GILight36-38 and the GI2 plastic lights: GI-collection lights that model no bulb",
			"Flasher domes Flasher27p and Flasher30p and their lights on the back panel at y < 0, off the playfield plane",
			"Lights F25, F25b, F26, F28, F29b-F29d, F30b-F30d, F31b, F32-F32c and Flash15a-c: no flasher dome or bulb",
		],
		"blockers": SPATIAL_BLOCKERS,
		"readiness": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"], "unresolved_conflicts": 0},
	}


def render_report(report: dict[str, Any]) -> str:
	lines = [
		"# Cyclone (Williams, 1988) spatial evidence", "",
		f"**Decision: {report['readiness']['status']}.** Missing: {', '.join(report['readiness']['missing']) or 'nothing'}.", "",
		report["coordinate_convention"] + ".", "",
	]
	if report["geometry_seed"]:
		lines += [f"Geometry seed `{report['geometry_seed']}` SHA-256 `{report['geometry_seed_sha256']}`.", ""]
	lines += [
		"A placement is the centre of the table object the known-working script binds to the address: a trigger, kicker, hit "
		"target, rubber, bumper, slingshot wall or flipper for a switch; the bumpers, slingshot walls and kickers for their "
		"coils; a light under a modelled flasher dome for a flasher; and the bulb-modelling lights of the GI collection for "
		"the playfield G.I. Lights with no bulb or dome mark no socket and take no placement.", "",
		"## Blockers", "",
	]
	lines += [f"- {b}" for b in report["blockers"]]
	lines += ["", "## Placed devices", "", "| Device | Binding | Placements |", "| --- | --- | --- |"]
	lines += [
		f"| `{r['id']}` | {r['binding']['group']} {r['binding']['device']} | "
		+ "; ".join(f"({p['x']}, {p['y']}) {p['provenance']['status']}" for p in r["placements"]) + " |"
		for r in report["located"]
	]
	if report["projections"]:
		lines += ["", "## Projections", ""] + [f"- {p['kind']} {p['address']}: {p['disclosure']}" for p in report["projections"]]
	lines += ["", "## Excluded table objects", ""] + [f"- {item}" for item in report["excluded_objects"]]
	lines += ["", "## Unplaced devices", "", "| Device | Label |", "| --- | --- |"]
	lines += [f"| `{r['id']}` | {r['label']} |" for r in report["unplaced"]]
	lines.append("")
	return "\n".join(lines)


# ---------------------------------------------------------------- products

def verify_excerpts(root: Path = ROOT) -> None:
	for key, (filename, _locator) in EXCERPT_FILES.items():
		path = root / EXCERPTS / filename
		if not path.is_file() or sha256(path) != EXCERPT_DIGESTS[key]:
			raise RuntimeError(f"Cyclone excerpt missing or changed: {path}")


def products(root: Path = ROOT) -> dict[Path, bytes]:
	verify_excerpts(root)
	definition = build_definition(root)
	errors = validate_machine(definition, root)
	if errors:
		raise RuntimeError("Invalid Cyclone definition: " + "; ".join(errors))
	report = build_report(definition, root)
	path = AUTHOR_READY if definition["coverage"]["status"] == "author_ready" else DEFINITION
	return {
		path: canonical_bytes(definition), KNOWLEDGE: (root / KNOWLEDGE_SEED).read_bytes(),
		REPORT: canonical_bytes(report), REPORT_MD: render_report(report).encode("utf-8"),
	}


def check(root: Path = ROOT) -> None:
	result = products(root)
	stale = DEFINITION if AUTHOR_READY in result else AUTHOR_READY
	if (root / stale).exists():
		raise RuntimeError(f"Cyclone has a stale opposing-status record: {stale}")
	for path, payload in result.items():
		if not (root / path).is_file() or (root / path).read_bytes() != payload:
			raise RuntimeError(f"Cyclone deterministic artifact missing or drifted: {path}")
	print("Cyclone definition, knowledge note, excerpts and spatial reports match the deterministic curator.")


def generate(root: Path = ROOT) -> None:
	result = products(root)
	if AUTHOR_READY not in result and (root / AUTHOR_READY).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Cyclone record with a partial one")
	for path, payload in result.items():
		(root / path).parent.mkdir(parents=True, exist_ok=True)
		(root / path).write_bytes(payload)
	if AUTHOR_READY in result and (root / DEFINITION).exists():
		(root / DEFINITION).unlink()


# ---------------------------------------------------------------- external evidence

def configured_root(name: str) -> Path:
	value = os.environ.get(name)
	if not value:
		raise RuntimeError(f"{name} must be configured")
	return Path(value).expanduser().resolve()


def object_point(extraction: Path, obj: dict[str, Any]) -> tuple[float, float]:
	value = load_json(extraction / obj["file"])[obj["type"]]
	if obj["type"] == "Rubber":
		points = value["drag_points"]
		return (sum(p["x"] for p in points) / len(points), sum(p["y"] for p in points) / len(points))
	x, y, method = _item_point(obj["type"], value)
	if method != obj["method"]:
		raise RuntimeError(f"Cyclone geometry method changed for {obj['file']}")
	return (x, y)


def verify_extraction(vpx: Path, root: Path = ROOT) -> dict[str, Any]:
	from build_external_evidence_manifest import build_manifest, check_manifest

	geometry = load_geometry(root)
	if geometry is None:
		raise RuntimeError("Cyclone geometry seed is missing")
	table = geometry["table"]
	extraction = vpx / table["extraction"]
	if sha256(vpx / table["path"]) != table["sha256"] or sha256(extraction / "script.vbs") != table["embedded_script_sha256"]:
		raise RuntimeError("Cyclone retained table or embedded script changed")
	manifest = build_manifest(extraction, "cycln_l5")
	actual = (check_manifest(extraction, "cycln_l5"), len(manifest["files"]), sum(f["size"] for f in manifest["files"]))
	if actual != (table["manifest_sha256"], table["file_count"], table["total_bytes"]):
		raise RuntimeError("Cyclone table extraction changed")
	return geometry


def verify_geometry(vpx: Path, root: Path = ROOT) -> None:
	geometry = verify_extraction(vpx, root)
	extraction = vpx / geometry["table"]["extraction"]
	gamedata = load_json(extraction / "gamedata.json")
	if {key: gamedata[key] for key in ("left", "top", "right", "bottom")} != geometry["bounds"]:
		raise RuntimeError("Cyclone table bounds changed")
	for name, obj in geometry["objects"].items():
		path = extraction / obj["file"]
		if sha256(path) != obj["file_sha256"] or object_point(extraction, obj) != (obj["x"], obj["y"]):
			raise RuntimeError(f"Cyclone geometry object drifted: {name}")
		if obj["type"] == "Light":
			value = load_json(path)["Light"]
			if (bool(value.get("is_bulb_light")) and bool(value.get("show_bulb_mesh"))) != obj["bulb"]:
				raise RuntimeError(f"Cyclone light bulb flags drifted: {name}")
	for name in geometry["anchors"]["solenoid"]["10"]:
		if not geometry["objects"][name]["bulb"]:
			raise RuntimeError(f"Cyclone G.I. placement {name} models no bulb")
	collections = load_json(extraction / "collections.json")
	gi = next(item["items"] for item in collections if item["name"] == "GI")
	if not set(geometry["anchors"]["solenoid"]["10"]) <= set(gi):
		raise RuntimeError("Cyclone G.I. placements are not in the table's GI collection")
	for light, dome in geometry["domes"].items():
		a, b = geometry["objects"][light], geometry["objects"][dome]
		if abs(a["x"] - b["x"]) > 2.5 or abs(a["y"] - b["y"]) > 2.5:
			raise RuntimeError(f"Cyclone flasher light {light} is not under its dome {dome}")


def verify_rom_tables(rom_root: Path, root: Path = ROOT) -> None:
	import cyclone_rom_name_tables as tables

	results = {name: tables.decode_set(rom_root / f"{name}.zip") for name in tables.SETS}
	if tables.render_markdown(results).encode("utf-8") != (root / EXCERPTS / "rom-name-tables.md").read_bytes():
		raise RuntimeError("Cyclone ROM name-table excerpt does not match the decoded ROMs")
	reference = results["cycln_l5"]
	if {entry["index"]: entry["text"] for entry in reference["switches"]} != data.ROM_SWITCH_NAMES:
		raise RuntimeError("Cyclone ROM switch names differ from cyclone_data")
	if {entry["index"]: entry["text"] for entry in reference["lamps"]} != data.ROM_LAMP_NAMES:
		raise RuntimeError("Cyclone ROM lamp names differ from cyclone_data")
	if {c["step"]: (c["first"]["text"], c["second"]["text"]) for c in reference["coils"]} != data.ROM_COIL_STEPS:
		raise RuntimeError("Cyclone ROM coil-test names differ from cyclone_data")
	for name, result in results.items():
		if (result["rom_archive_sha256"], result["member"], result["member_sha256"]) != (data.ROM_ARCHIVE_SHA256[name], *data.ROM_U27[name]):
			raise RuntimeError(f"Cyclone ROM archive changed: {name}")


def verify_evidence(root: Path = ROOT) -> None:
	verify_excerpts(root)
	manuals = configured_root("PINMAME_MANUALS_ROOT")
	review = configured_root("PINMAME_REVIEW_ARTIFACTS_ROOT")
	vpx = configured_root("PINMAME_VPX_SOURCES_ROOT")
	folder = manuals / MANUAL_FOLDER
	retained = (MANUAL_FILENAME, PARTS_FILENAME, BULLETINS_FILENAME, IPDB_PAGE)
	if tuple(sha256(folder / name) for name in retained) != (MANUAL_SHA256, PARTS_SHA256, BULLETINS_SHA256, IPDB_PAGE_SHA256):
		raise RuntimeError("Cyclone retained manuals or IPDB page changed")
	if sha256(review / "vpm-script-libs" / "s11.vbs") != VPM_S11_SHA256:
		raise RuntimeError("Retained s11.vbs changed")
	import cyclone_runtime_evidence as runtime

	manifest_bytes, evidence, pins = runtime.build(review)
	runtime.check_pins(pins)
	if hashlib.sha256(manifest_bytes).hexdigest() != RUNTIME_MANIFEST_SHA256:
		raise RuntimeError("Cyclone raw harness runs differ from the pinned manifest")
	for game, path in runtime.EVIDENCE_PATHS.items():
		if canonical_bytes(evidence[game]) != (root / path.relative_to(runtime.ROOT)).read_bytes():
			raise RuntimeError(f"Cyclone raw runtime evidence disagrees with the compact evidence: {path.name}")
	verify_geometry(vpx, root)
	rom_root = os.environ.get(ROM_LIBRARY_VARIABLE)
	if rom_root:
		verify_rom_tables(Path(rom_root), root)
	print(
		"Cyclone retained manuals, IPDB page, script library, raw runs, frame pins and table geometry match the pinned evidence"
		+ (", and so do the ROM name tables." if rom_root else f"; set {ROM_LIBRARY_VARIABLE} to re-decode the ROM name tables.")
	)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="refuse drift between the curator and every product")
	mode.add_argument("--regenerate", action="store_true", help="write the definition, knowledge note and spatial reports")
	mode.add_argument("--verify-evidence", action="store_true", help="re-derive the retained evidence from the configured roots")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="write the retained table extraction's full-file manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="verify the retained table extraction against its pinned manifest")
	args = parser.parse_args()
	if args.check:
		check()
	elif args.verify_evidence:
		verify_evidence()
	elif args.write_extraction_manifest:
		from build_external_evidence_manifest import write_manifest

		geometry = load_geometry(ROOT)
		if geometry is None:
			raise RuntimeError("Cyclone geometry seed is missing")
		print(write_manifest(configured_root("PINMAME_VPX_SOURCES_ROOT") / geometry["table"]["extraction"], "cycln_l5"))
	elif args.verify_extraction:
		verify_extraction(configured_root("PINMAME_VPX_SOURCES_ROOT"))
		print("Cyclone retained table extraction matches its pinned manifest.")
	else:
		generate()


if __name__ == "__main__":
	main()
