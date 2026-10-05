"""Build the reviewed Stern Family Guy (2007) machine definition.

Deterministic and side-effect free until ``--write`` is passed. The device tables live in
``family_guy_devices.py``; the recreation note is the seed
``tools/seeds/stern/family-guy-2007-knowledge.md``. Excerpts under
``evidence/excerpts/stern.family-guy.2007/`` and the compact runtime summaries under
``evidence/runtime/sam/family-guy-*.json`` are committed inputs: this script digests them into
the source records and refuses to run when one is missing or changed.

Usage::

	python tools/curate_family_guy.py --check    # fail if the committed artifacts drift
	python tools/curate_family_guy.py --write    # regenerate the definition and knowledge note
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_bytes

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
	sys.path.insert(0, str(TOOLS))

import drawing_callouts  # noqa: E402
import family_guy_devices as dev  # noqa: E402
import family_guy_spatial as spatial  # noqa: E402
from family_guy_devices import CATALOG, CORE, IPDB, MANUAL, ROM, RT_BOOT, RT_COIL, RT_DEDICATED, RT_EM_CLOSED, RT_EM_OPEN, RT_LAMP, RT_SWITCH, SCRIPT, TABLE, provenance  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "stern.family-guy.2007"
DEFINITION_PATH = ROOT / "machines/partial/stern/family-guy-2007.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/family-guy-2007.md"
KNOWLEDGE_SEED = ROOT / "tools/seeds/stern/family-guy-2007-knowledge.md"
CALLOUT_PATH = ROOT / "tools/seeds/stern/family-guy-2007-callouts.json"
AUDIT_PATH = ROOT / "reports/spatial/stern/family-guy-2007.json"
CALLOUTS = "review.family-guy-drawing-callouts-2026-10-02"
EXCERPT_ROOT = ROOT / "evidence/excerpts/stern.family-guy.2007"
RUNTIME_ROOT = ROOT / "evidence/runtime/sam"
BULLETIN = "bulletin.stern-family-guy-170"
SCRIPT_CORPUS = "vpx.script.family-guy-1.0-corpus"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"

MANUAL_SHA256 = "2bbcfa34ad70ab90c0fadabaf825850cecae58c8028af9aaabf8be1ad01979cd"
BULLETIN_SHA256 = "b26b97f9117513b44b78dbfc1c6e32aa7cb762313a7e6b836a512fbbf629ece0"
TABLE_SHA256 = "159558a39efd5a784bf0e587e9f07563e4fcd92765eeda02c9abc8bad015e2ff"
SCRIPT_SHA256 = "c7b201acb74a329913b159db88315c422b8dcead0ba4bb30b61785ed1785f8db"
IPDB_SHA256 = "092f65a5dcfa97c5eaf36341479b9f546a8353c95c07b81aa7bcc676a497c446"
ROM_ARCHIVE_SHA256 = ""  # filled from the committed runtime summary at build time

CATALOG_JSON = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG_JSON["drivers"] if driver["id"].startswith("fg_")}
SWEEP_DRIVERS = ("fg_300ai", "fg_400a", "fg_800al", "fg_1100al")


def sha256_file(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt(identifier: str, filename: str, locator: str, method: str = "mixed", reviewed: bool = False, transcribed_by: str = "curator, 2026-10-02") -> dict[str, Any]:
	path = EXCERPT_ROOT / filename
	if not path.is_file():
		raise FileNotFoundError(f"missing excerpt {path}")
	return {"id": identifier, "locator": locator, "method": method, "path": path.relative_to(ROOT).as_posix(), "reviewed": reviewed, "sha256": sha256_file(path), "transcribed_by": transcribed_by}


def runtime_summary(name: str) -> dict[str, Any]:
	path = RUNTIME_ROOT / name
	if not path.is_file():
		raise FileNotFoundError(f"missing runtime summary {path}")
	return json.loads(path.read_text(encoding="utf-8"))


def runtime_source(identifier: str, filename: str, locator: str, excerpts: list[dict[str, Any]] | None = None) -> dict[str, Any]:
	summary = runtime_summary(filename)
	raw = summary["runtime"]["raw_runs"][0]
	source = {
		"id": identifier, "kind": "runtime_scenario", "uri": f"internal:evidence/runtime/sam/{filename}",
		"revision": PINMAME_REVISION, "sha256": raw["sha256"], "locator": locator, "license": "NOASSERTION",
		"attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
	}
	if excerpts:
		source["excerpts"] = excerpts
	return source


def sources() -> list[dict[str, Any]]:
	boot = runtime_summary("family-guy-fg_1200ag-boot-start.json")
	rom_sha = boot["runtime"]["rom_archive_sha256"]
	result: list[dict[str, Any]] = [
		{"attribution": "PinMAME contributors", "id": CATALOG, "kind": "pinmame_catalog", "license": "BSD-3-Clause", "locator": "PinmameGetGames fg_ driver records and clone graph (root fg_1200ag).", "revision": PINMAME_REVISION, "uri": "https://github.com/vpinball/pinmame"},
		{"attribution": "PinMAME contributors", "id": CORE, "kind": "pinmame_core", "license": "BSD-3-Clause", "locator": "src/wpc/sam.c: INITGAME(fg, GEN_SAM, sam_dmd128x32, SAM_8COL, SAM_GAME_FG) and the fg_* driver family (root fg_1200ag); the SAM_GAME_FG block that publishes the mini-playfield LED board 520-5264-00 at lamp addresses 81-128; the Family Guy output typing (solenoids 18-21 and 25-32, mini-playfield LEDs); the fastflip address of the fg_1200 family; the public switch, lamp and GI conversions shared by every S.A.M. game.", "revision": PINMAME_REVISION, "uri": "https://github.com/vpinball/pinmame"},
		{
			"acquired_at": "2026-10-02T00:00:00Z", "attribution": "Stern Pinball, Inc.", "id": MANUAL, "kind": "manual", "license": "NOASSERTION", "original_filename": "FG_FIND_IT_IN_FRONT.pdf", "rights": "NOASSERTION",
			"sha256": MANUAL_SHA256, "source_id": "Stern_Pinball_Family_Guy_Manual", "uri": "https://archive.org/download/Stern_Pinball_Family_Guy_Manual/FG_FIND_IT_IN_FRONT.pdf",
			"locator": "Internet Archive item Stern_Pinball_Family_Guy_Manual (uploader wouterdevlieger@gmail.com; details https://archive.org/details/Stern_Pinball_Family_Guy_Manual), 170-page Stern Pinball Service Game Manual, January 2008, v12.0+ (IPDB 5219 lists the same manual). The PDF's text layer is unusable; every cell was read from renders. Switch/lamp/dedicated grids and the DR.5/DR.7/DR.9 location drawings: PDF pages 7, 9, 10, 11, 23. Test text: 39-41. Parts and assemblies: 68-69, 72-73, 90-118. Wiring and PCBs: 120-131, 133-135, 159-169.",
			"excerpts": [
				excerpt("excerpt.family-guy.switch-matrix", "manual-switch-matrix.md", "PDF pages 7 and 23: switch matrix grid 1-64, dedicated switches D-1 to D-24, DIP switch D-25 to D-32"),
				excerpt("excerpt.family-guy.lamp-matrix", "manual-lamp-matrix.md", "PDF pages 9 and 23: lamp matrix grid 1-80 and lamp-location legend"),
				excerpt("excerpt.family-guy.coil-chart", "manual-coil-chart.md", "PDF pages 10, 11, 39 and 41: coils detailed chart table Q1-Q32, location legend, coil and Stewie motor test text"),
				excerpt("excerpt.family-guy.gi-and-flippers", "manual-gi-and-flippers.md", "PDF pages 92-94, 123 and 127: general illumination circuits, flipper circuit and flipper assemblies"),
				excerpt("excerpt.family-guy.mini-playfield-led-board", "manual-mini-playfield-led-board.md", "PDF pages 166-167 (and PinMAME sam.c): mini-playfield LED board 520-5264-00 nets and lamp addresses"),
				excerpt("excerpt.family-guy.assemblies", "manual-assemblies.md", "PDF pages 3, 17, 29-30, 68-69, 72-73, 90-118, 169-170: assembly parts, switch types, instruction card and the auxiliary (ticket/meter) driver board"),
			],
		},
		{
			"acquired_at": "2026-10-02T00:00:00Z", "attribution": "Stern Pinball Inc.", "id": BULLETIN, "kind": "service_bulletin", "license": "NOASSERTION", "original_filename": "sb170.pdf", "rights": "NOASSERTION",
			"sha256": BULLETIN_SHA256, "source_id": "Stern_Pinball_Service_Bulletin_170", "uri": "https://archive.org/download/Stern_Pinball_Service_Bulletin_170/sb170.pdf",
			"locator": "Stern Service Bulletin 170 (February 21, 2007, Internet Archive item Stern_Pinball_Service_Bulletin_170): starting with Family Guy, factory firmware limits North American games to 60 Hz line voltage and export games to 50 or 60 Hz; a firmware measure, not a hardware change.",
		},
		{"acquired_at": "2026-10-02T00:00:00Z", "attribution": "Internet Pinball Database", "id": IPDB, "kind": "human_review", "license": "NOASSERTION", "locator": "IPDB 5219 \"Family Guy\" (Stern, manufactured 2007, model I-0093, S.A.M. board system): five flippers, three pop bumpers, a 4-bank and a solitary drop target, nine stand-up targets, two captive balls, two Newton balls, a spinning target, an up-post between the flippers, the Stewie mini-playfield; the Stewie figure rotates to face his mini-pinball machine and Meg bobs up and down. Fetched through the Wayback id_ form; page SHA-256 " + IPDB_SHA256 + ".", "sha256": IPDB_SHA256, "uri": "https://www.ipdb.org/machine.cgi?id=5219"},
		{
			"attribution": "Table authors credited in the script; Ninuzzu", "id": TABLE, "kind": "vpx_table", "license": "NOASSERTION", "known_working": False,
			"locator": "Family Guy (Stern 2007).vpx from the user's VPX archive (40,579,072 bytes, extracted with vpxtool git:v0.33.3). Its info.json header names \"Shrek (Stern 2008)\" by Ninuzzu, but the playfield art, objects and script are Family Guy (cGameName fg_1200af); the header is a stale carry-over from the Shrek table it was built from. Playfield bounds left 0, top 0, right 952, bottom 2115. A reconstruction with known defects (see the knowledge note): bumper objects are bound to the reverse of the manual's switch order, and it has no objects for several playfield switches.",
			"sha256": TABLE_SHA256, "uri": "external:vpx-sources/stern/family-guy-2007/source/Family Guy (Stern 2007).vpx",
		},
		{
			"attribution": "Table authors credited in the script", "id": SCRIPT, "kind": "vpx_script", "license": "NOASSERTION",
			"locator": "Embedded Script stream of the exact retained table, extracted with vpxtool extractvbs (1,449 lines, cGameName \"fg_1200af\", LoadVPM sam.vbs 3.43). Used only for controller-facing behaviour: which public switches it pulses (vpmTimer.PulseSw) or holds (Controller.Switch), the SolCallback list for Q1-Q6, Q12-Q13, Q15-Q32, the commented-out bumper and sling callbacks, and the NFadeL lamp bindings 3-70 and LED bindings. It is a reconstruction, not a verified-working table: several bindings contradict the factory manual and are recorded as table defects on the affected devices.",
			"sha256": SCRIPT_SHA256, "uri": "external:vpx-sources/stern/family-guy-2007/source/Family Guy (Stern 2007).vbs",
		},
		{
			"attribution": "Table authors credited in the script; jsm174/vpx-standalone-scripts contributors", "id": SCRIPT_CORPUS, "kind": "vpx_script", "license": "NOASSERTION",
			"locator": "Pinned corpus script Family Guy 1.0 (jsm174/vpx-standalone-scripts revision 15d112648a1b94b9f59eb8b3c335d57283653c50, also the sverrewl/vpxtable_scripts Family Guy 1.0 script): a later, VPW-style revision of the same lineage with the same SolCallback list, the same Bumper1->32, Bumper2->31, Bumper3->30 pulses and the same Controller.Switch(35) assertion in its CastleGuard routines. It shares ancestry with the retained table, so it supplements and never corroborates it. The recorded SHA-256 is that of the 176,332-byte LF blob at the pinned revision. The corresponding VPX table is not retained.",
			"sha256": "d2657cbbbccbb211a5fc815d9eb2ceedb19a4d87b00be26d586824f886647042", "uri": "https://github.com/jsm174/vpx-standalone-scripts/blob/15d112648a1b94b9f59eb8b3c335d57283653c50/Family%20Guy%201.0/Family%20Guy%201.0.vbs", "revision": "15d112648a1b94b9f59eb8b3c335d57283653c50",
		},
		{
			"attribution": "Stern Pinball game code; ROM bytes remain external", "id": ROM, "kind": "rom_static_analysis", "license": "NOASSERTION", "revision": "V12.0 English/German",
			"locator": "Read-only user-authorized archive fg_1200ag.zip (members FG120ag.bin CRC d9734f94, fg120ai.bin, fg120al.bin, fg120af.bin; FGreadme.txt). Member CRCs of the retained zips for fg_1000*, fg_1100*, fg_1200ag/ai/al, fg_300ai, fg_400a, fg_400ag, fg_700af/al and fg_800al match pinned sam.c; the retained fg_1200af.zip holds a different dump (CRC 83cdeafa) and fg_200a has no retained ROM.",
			"sha256": rom_sha, "uri": "external:vpinmame-roms/fg_1200ag.zip",
		},
	]
	result.append({
		"id": CALLOUTS, "kind": "human_review", "uri": "internal:" + CALLOUT_PATH.relative_to(ROOT).as_posix(), "sha256": sha256_file(CALLOUT_PATH),
		"locator": "2026-10-02 factory location-drawing callout check of DR.5 (switches) and DR.7 (lamps), PDF pages 7 and 9: every numbered box transcribed independently on the retained 200 dpi renders, verifier corrections recorded with their reasons, per-page control and callout fits; a table placement whose own box lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). The DR.9 coil page was transcribed too but cannot be fitted (its only top-down view is an inset cut off at the page edge showing three bumpers), so no coil or flasher placement is checked. Reads, overlays and generator are retained under review-artifacts with a pinned manifest.",
		"license": "NOASSERTION", "attribution": "PinMAME game definitions contributors",
	})
	result.append(runtime_source(RT_SWITCH, "family-guy-fg_1200ag-switch-test-sweep.json", "Fresh-NVRAM fg_1200ag switch test: every matrix switch 1-64 held for 1.2 s; the ROM prints its own name and wire colours for the switch it reads closed. Names are transcribed in the ROM service-test excerpt.", [excerpt("excerpt.family-guy.rom-service-tests", "rom-service-tests.md", "ROM switch, dedicated-switch, coil and lamp test names transcribed from the retained DMD frames", transcribed_by="curator, 2026-10-02; frames read visually and re-read by the runtime builder's OCR cross-check")]))
	result.append(runtime_source(RT_DEDICATED, "family-guy-fg_1200ag-dedicated-switch-sweep.json", "Fresh-NVRAM fg_1200ag switch test: public 65-72, 81-88 and -7 to -4 held for 1.2 s each."))
	result.append(runtime_source(RT_COIL, "family-guy-fg_1200ag-coil-test-sweep.json", "Fresh-NVRAM fg_1200ag Single Coil Test: 35 selector positions each fired once; every fired position is paired with the public solenoid addresses that changed."))
	result.append(runtime_source(RT_LAMP, "family-guy-fg_1200ag-lamp-test-sweep.json", "Fresh-NVRAM fg_1200ag Single Lamp Test: all 80 selector positions; every position is paired with the public lamp addresses that changed."))
	result.append(runtime_source(RT_BOOT, "family-guy-fg_1200ag-boot-start.json", "fg_1200ag boot, six coins and Start with trough switches 18-21 and mini-trough 55 closed: observes the 128x32 DMD, GI 0, the Stewie homing pulses on solenoid 20, the synthetic game-on solenoid 33 and the LED-board lamp channels 81-125."))
	result.append(runtime_source(RT_EM_CLOSED, "family-guy-fg_1200ag-evil-monkey-probe-closed.json", "fg_1200ag probe with Evil Monkey switch 35 closed by the scenario after the ROM has booted (the booted snapshot still reads 0) and before the coins and Start: six coins, Start, a modelled ball in and out of the shooter lane, the Chris target (switch 3) hit, switch 35 opened and closed. Q19 (public solenoid 19) never changes."))
	result.append(runtime_source(RT_EM_OPEN, "family-guy-fg_1200ag-evil-monkey-probe-open.json", "The same probe with Evil Monkey switch 35 left open from the scenario's start through the coins and Start: Q19 changes repeatedly from Start until switch 35 is closed, and not afterwards."))
	for driver in SWEEP_DRIVERS:
		for kind, filename in (("switch", f"family-guy-{driver}-switch-test-sweep.json"), ("coil", f"family-guy-{driver}-coil-test-sweep.json"), ("lamp", f"family-guy-{driver}-lamp-test-sweep.json")):
			if (RUNTIME_ROOT / filename).is_file():
				result.append(runtime_source(f"runtime.family-guy.{driver}.{kind}-test-sweep", filename, f"Fresh-NVRAM {driver} {kind} test sweep with the same scenario as the fg_1200ag run, retained to compare the ROM's names and public addresses across firmware."))
	return result


def driver_records() -> list[dict[str, Any]]:
	selected: list[dict[str, Any]] = []
	for driver_id, source in sorted(DRIVERS.items()):
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = variant_note(driver_id)
		selected.append(record)
	return selected


def variant_note(driver_id: str) -> str:
	base = "Firmware revision and/or language of the same 2007 Family Guy machine; PinMAME initializes every fg_ driver with the same game data (S.A.M. generation, 128x32 DMD, eight lamp columns, SAM_GAME_FG mini-playfield LED board)."
	if driver_id in {"fg_300ai", "fg_400a", "fg_800al", "fg_1100al", "fg_1200ag"}:
		return base + " Its switch, coil and lamp test names and public addresses were exercised in the retained harness sweeps and match the V12.0 firmware, apart from the optional ticket-dispenser auxiliary coils listed by older firmware (see the knowledge note)."
	if driver_id == "fg_200a":
		return base + " No ROM for this driver is retained, so it was not run; its I/O contract rests on the shared PinMAME initialization and on the older firmware that was run."
	if driver_id == "fg_1200af":
		return base + " The retained zip for this driver holds a different dump from the pinned CRC, so it was not run; its contract rests on the shared initialization and on the sibling languages that were."
	return base + " It was not run itself; its contract rests on the shared initialization and on the firmware revisions that were."


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources_: tuple[str, ...], positions: list[dict[str, Any]] | None = None, status: str = "validated", assembly: str | None = None) -> dict[str, Any]:
	result: dict[str, Any] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources_, status=status)}
	if positions is not None:
		result["positions"] = positions
	if assembly:
		result["assembly_part_number"] = assembly
	return result


def mechanisms() -> list[dict[str, Any]]:
	o, s, d = dev.output_id, dev.switch_id, dev.dedicated_id
	common = (MANUAL, CORE, RT_SWITCH, RT_COIL)
	script = common + (SCRIPT,)
	return [
		mechanism("mechanism.trough", "Four-ball trough and shooter lane", "kicker", [o(1), o(2)], [s(n) for n in (18, 19, 20, 21, 22, 23)],
			"Four balls rest on trough switches 18-21 (the machine will not play without all four; an extra mini-pinball sits on the mini-playfield). Q1 lifts the right-most ball, whose position 21 is a blocked dual-OPTO beam, through jam opto 22 into the shooter lane, momentarily closing shooter switch 23. The player plunges the ball by hand with the ball shooter (plunger) assembly, or Q2 (autoplunger) fires it; the manual's Ball Trough Test describes SELECT ejecting the ball at position 21 to the up-kicker, the shooter lane and the playfield, and says switch 22 is the stacking opto that notes additional balls when more than five are used. Keep per-position occupancy and the jam beam rather than a count.", script, assembly="500-6318-14-ND"),
		mechanism("mechanism.ball-saver-post", "Ball saver (Death) up/down post", "gate", [o(12), o(4)], [s(1), s(2)],
			"An up/down post between the lower flippers. The manual states that when energized the post prevents the ball draining between the lower flippers. Q12 raises it and Q4 (the 32-1800 mini-coil of the post's latch assembly) lowers it; blade switches 1 (up) and 2 (down) report its two positions, and lamp 69 shows the post. The instruction card says hitting the Death 1-bank drop target raises the post. The retained script asserts switch 1 when it raises the post and switch 2 when it lowers it but runs a three-second timer of its own that the manual does not describe.", script, [{"id": "position.up", "label": "Post up", "sensors": [s(1)]}, {"id": "position.down", "label": "Post down", "sensors": [s(2)]}], assembly="500-7022-00"),
		mechanism("mechanism.fart-drop-targets", "F-A-R-T 4-bank drop target", "drop_target_bank", [o(3)], [s(n) for n in (44, 45, 46, 47)],
			"Four drop targets F, A, R, T with one OPTO interrupter each (PCB 520-5252-04, switches 44-47). A target interrupts its beam while down; Q3 raises the whole bank (24-940 coil). Lamps 35-38 spell the same letters; the instruction card says hitting the F-A-R-T targets advances Fart Multiball.", script, [{"id": "position.up", "label": "Bank up", "sensors": []}, {"id": "position.down", "label": "Target down", "sensors": [s(n) for n in (44, 45, 46, 47)]}], assembly="500-7029-04"),
		mechanism("mechanism.death-drop-target", "Death 1-bank drop target", "drop_target_bank", [o(6)], [s(9)],
			"One drop target with an OPTO interrupter (PCB 520-5252-01, switch 9); Q6 resets it. Lamp 41 marks it. The instruction card says hitting it raises the ball saver post.", script, [{"id": "position.up", "label": "Target up", "sensors": []}, {"id": "position.down", "label": "Target down", "sensors": [s(9)]}], assembly="500-7029-01"),
		mechanism("mechanism.tv-eject", "TV eject scoop", "kicker", [o(13)], [s(13)],
			"A scoop with a vertical up-kicker: the ball closes scoop switch 13 and Q13 (23-800) ejects it. Lamps 29-31 (TV, Pinball, Multiball) are the scoop's features, and the instruction card says to shoot the TV scoop after spelling P-I-N-B-A-L-L to start Stewie Pinball on the mini-playfield.", script, assembly="500-7028-00"),
		mechanism("mechanism.clam-eject", "Clam eject (vertical up-kicker)", "kicker", [o(5)], [s(64)],
			"An eject hole whose ball closes switch 64 and is kicked out by the vertical up-kicker Q5 (27-1500). Lamp 62 (Drunken Clam / mystery) is its feature.", script, assembly="500-6846-01"),
		mechanism("mechanism.evil-monkey-gate", "Evil Monkey latch gate (left ramp)", "gate", [o(19)], [s(35), s(33)],
			"The left plastic ramp carries a latch gate with a trip coil (Q19, 32-1250) and a roller microswitch (35). The instruction card says shooting the Chris target (switch 3, upper left) lowers the Evil Monkey target and advances the Evil Monkey award, and collecting all five awards starts Crazy Chris. Switch 33 (Left ramp made) is the roll-under switch of the ramp's exit gate. Harness probes of fg_1200ag show the ROM re-firing Q19 from game start for as long as public 35 reads open and never firing it when 35 starts closed, so a closed switch 35 is the state the ROM drives Q19 toward; opening switch 35 after the game had started did not make it fire Q19 again within four seconds, and hitting the Chris target (switch 3) fired the back-panel flasher Q27 rather than Q19 in that state. What Q19 does to the physical target and what the Chris-target award does to the latch are not documented or observed, so the latch geometry stays unproven.", script + (RT_EM_CLOSED, RT_EM_OPEN), status="observed", assembly="500-6590-01-ND"),
		mechanism("mechanism.stewie-figure", "Stewie rotating figure", "toy", [o(20)], [],
			"A stepper motor (511-5043-00) on controller PCB 511-5045-00, driven by Q20 through the ROM, turns the Stewie figure to face the Stewie mini-pinball machine (IPDB). The motor has no position switch: the ROM's Stewie Motor Test (F.G. icon) homes it against the raised stop of the motor mounting bracket by pulsing enough steps in one direction and then the opposite direction, and the retained boot-start run shows the ROM pulsing Q20 during power-up.", common + (RT_BOOT,), assembly="500-7030-00"),
		mechanism("mechanism.meg-popper", "Meg shake", "toy", [o(22)], [],
			"A mini-coil (Q22, 27-950) moves the Meg figurine so that it bobs up and down (IPDB). No switch reports it.", common, assembly="500-7031-00"),
		mechanism("mechanism.beer-can", "Brian beer can", "toy", [], [s(49)],
			"A spring-returned beer can with the Brian figurine; a ball hit closes switch 49. Lamps 48-52 (Collect Beers, Giggity Giggity, Happy Hour, Remember When, Lard Multiball) and flasher Q28 belong to it.", script, assembly="500-7025-00"),
		mechanism("mechanism.mini-playfield", "Stewie mini-playfield", "other", [o(17), o(18), o(21)], [s(n) for n in (50, 51, 52, 53, 54, 55)],
			"An upper mini-playfield with its own 5/8 in. mini-pinball. Q21 (27-950) is the mini-playfield shooter: the ball rests on mini-trough opto 55, is shot up the mini-shooter ramp and plays through mini right orbit 52, mini left orbit 53 and mini ramp 54 (all mini OPTO transceiver pairs), past the mini Meg 50 and mini Peter 51 stand-ups, and between two mini-flippers Q17 and Q18 that operate with the lower flipper buttons. Lamp 68 is Mini Shoot Again. The mini-pinball must be installed for the game to start (manual page 3). The 22 LEDs spelling BRIAN, CHRIS, LOIS, MEG and PETER are on the separate LED board (lamps 81-125).", script, assembly="500-7018-00"),
		mechanism("mechanism.flippers", "Lower flippers and upper left flipper", "other", [o(15), o(16), o(14)], [d(n) for n in (9, 10, 11, 12, 13)],
			"Q15 and Q16 drive the lower left and right flippers with end-of-stroke switches D-10 and D-12 (normally closed, opening about 1/16 in. as the coil is energized); Q14 drives the upper-left mini flipper bat, which has no EOS switch. The left and right cabinet buttons are double-stacked: half-way operates the lower flipper (D-9, D-11) and a full press also operates the upper flipper (D-13 for the left). No upper-right flipper is fitted (D-15 printed NOT USED). The manual specifies a 40 ms kick at +50 VDC and then 1 ms pulses every 12 ms while the button is held, with a new 40 ms pulse if the EOS contact closes again.", common + (RT_DEDICATED,)),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", [o(9), o(10), o(11)], [s(32), s(31), s(30)],
			"Bottom, right and top pop bumpers pair coil Q9 with switch 32, Q10 with 31 and Q11 with 30 (the factory names agree: BOTTOM, RIGHT, TOP). Lamp 61 is the white LED module on the bottom bumper.", common + (SCRIPT,), assembly="515-6459-04-ND"),
		mechanism("mechanism.slingshots", "Slingshots", "other", [o(7), o(8)], [s(26), s(27)],
			"Left slingshot Q7 with switch 26 and right slingshot Q8 with switch 27; each assembly carries two stack switches.", common + (SCRIPT,), assembly="500-5849-02-ND"),
		mechanism("mechanism.orbits-and-lanes", "Orbits, lanes, spinner and fixed targets", "other", [], [s(n) for n in (3, 4, 5, 6, 7, 8, 10, 15, 16, 24, 25, 28, 29, 39, 40, 41, 42, 43, 48, 57)],
			"The remaining playfield switches at their enumerated addresses: the Newton ball rollovers 6 and 7, the left orbit stand-up 3, right 2-bank stand-ups 4 and 5, the Pirate and Meg stand-ups, the 3-bank stand-ups 41-43, outlanes and return lanes 24, 25, 28 and 29, the death return 40, the right orbit 57 and its spinner 39, and the sneak ramp 48. Their contacts are momentary: use the pulse flag recorded on each switch.", common + (SCRIPT,)),
		mechanism("mechanism.optional-devices", "Optional coin meter, token dispenser or knocker", "other", [o(24)], [d(5), d(19)],
			"Coil Q24 (5 V) is optional: the manual says a coin meter, token dispenser or knocker is wired there when required, and the optional ticket dispenser reports a notch on dedicated switch D-19. The retained boot-start run observes public solenoid 24 pulsing as coins are credited, which is consistent with a credit-sound knocker or meter output.", common + (RT_BOOT, RT_DEDICATED), status="observed"),
	]


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Family Guy", "manufacturer": "Stern", "year": 2007, "kind": "physical_pinball", "ipdb_id": 5219, "opdb_id": "G5LW9-MQ6N5"},
		"coverage": {
			"status": "partial",
			"missing": ["mechanism_behavior", "spatial_placement"],
			"dimensions": {"address_enumeration": "validated", "catalog_identity": "validated", "mechanisms": "observed", "physical_wiring": "validated", "recreation_knowledge": "validated", "semantic_naming": "validated", "spatial_placement": "observed", "variant_coverage": "validated"},
		},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(), "inputs": dev.inputs(), "outputs": dev.outputs(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance(CORE, RT_BOOT)}],
		"mechanisms": mechanisms(), "relationships": [], "sources": sources(),
		"knowledge": {"path": "knowledge/stern/family-guy-2007.md", "status": "complete"}, "conflicts": [],
	}
	spatial.attach(definition, spatial.load_seed())
	drawing_callouts.apply_to_definition(definition, json.loads(CALLOUT_PATH.read_text(encoding="utf-8")), CALLOUTS)
	return definition


CALLOUT_PAGE_KINDS = {"pdf-7": "switch", "pdf-9": "lamp"}


def callout_check(definition: dict[str, Any]) -> dict[str, Any]:
	"""The drawing callout check's report record, recomputed from the committed seed."""
	seed = json.loads(CALLOUT_PATH.read_text(encoding="utf-8"))
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition))
	return drawing_callouts.summary(seed, decisions, CALLOUT_PATH.relative_to(ROOT).as_posix(), sha256_file(CALLOUT_PATH))


def callout_sentence(check: dict[str, Any]) -> str:
	rest: dict[str, list[int]] = {}
	for item in check["not_validated"].values():
		rest.setdefault(CALLOUT_PAGE_KINDS[item["page"]], []).append(int(item["label"]))
	parts = [f"{kind}{'es' if kind == 'switch' else 's'} {', '.join(str(n) for n in sorted(numbers))}" for kind, numbers in sorted(rest.items())]
	left = f" The checked placements that stay observed, each with a note on its device: {'; '.join(parts)}." if parts else ""
	return (f"A factory location-drawing callout check validates {check['validated']} of the {check['checked']} table placements it covers: "
	        "every numbered box on DR.5 and DR.7 was transcribed independently, each page was fitted against its jet-bumper and flipper-pivot "
	        "controls and against its other boxes, and a placement validates when its own box lands within 0.07 normalized under both fits "
	        f"(`{check['seed']}`).{left}")


def audit(definition: dict[str, Any]) -> dict[str, Any]:
	seed = spatial.load_seed()
	groups = ("inputs", "outputs", "displays")
	missing = [x["id"] for group in groups for x in definition[group] if x.get("availability", "used") in {"used", "optional"} and "spatial" not in x]
	placements = [pl for group in groups for x in definition[group] for pl in (x.get("spatial") or {}).get("placements", [])]
	return {
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID, "promotion": "partial",
		"table_sha256": seed["table_sha256"], "extraction_manifest_sha256": seed["table_manifest_sha256"],
		"coordinates": "x=raw_x/952, y=raw_y/2115; six-decimal repository helper values; player view, y rear to apron",
		"source_seed_sha256": sha256_file(spatial.SEED_PATH), "manual_sha256": MANUAL_SHA256, "embedded_script_sha256": SCRIPT_SHA256,
		"located_observations": len(placements),
		"validated_placements": sum(pl["provenance"]["status"] == "validated" for pl in placements),
		"missing_spatial_ids": missing,
		"unresolved_conflict_ids": [x["id"] for x in definition["conflicts"]],
		"projection_classes": {
			"exact_named_vpx_object_center": "observed, and validated where drawing_callout_check agrees: the table's swN triggers, walls, targets and kickers, the Bumper1-3 pop bumpers and the lN lights",
			"coil_mechanism_anchor": "observed effect anchor on the mechanism object the coil drives (flipper pivots, kickers, drop-target banks, the death post wall); the coil body is not modelled and the DR.9 page is not fitted",
			"flasher_bulb_light": "observed emitter on the table's F23 and F29-F32 lights; Q25-Q28 have no retained table object",
			"led_board_letter": "observed emitter on the table's LEDn object lying on the same printed letter of the mini-playfield art; the table binds some of them under the wrong names (device notes)",
			"manual_drawing_projection": "not used for coordinates; the factory DR.5 and DR.7 boxes validate table placements (drawing_callout_check)",
			"cabinet_or_service": "not applicable", "virtual_or_unused": "not applicable"},
		"drawing_callout_check": callout_check(definition),
		"reason": "The retained table is a defective reconstruction (reversed pop-bumper bindings, swapped BRIAN/CHRIS LEDs, no objects for the trough sensors 18-22 or the back-panel flashers Q25-Q28, no GI) and the DR.9 coil/flash page could not be fitted; the Evil Monkey latch gate is also unresolved. A second, correct table or measured placements are needed before author readiness.",
	}


def verify_external() -> None:
	manuals, reviews = os.environ.get("PINMAME_MANUALS_ROOT"), os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	drawing_callouts.verify_retained(json.loads(CALLOUT_PATH.read_text(encoding="utf-8")), ROOT, Path(manuals) if manuals else None, Path(reviews) if reviews else None)


def knowledge_text(definition: dict[str, Any]) -> str:
	return KNOWLEDGE_SEED.read_text(encoding="utf-8").replace("{CALLOUT_CHECK}", callout_sentence(callout_check(definition)))


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--check", action="store_true")
	group.add_argument("--write", action="store_true")
	args = parser.parse_args()
	verify_external()
	definition = build()
	artifacts = {
		DEFINITION_PATH: canonical_bytes(definition),
		KNOWLEDGE_PATH: knowledge_text(definition).encode("utf-8"),
		AUDIT_PATH: canonical_bytes(audit(definition)),
	}
	if args.write:
		for path, wanted in artifacts.items():
			write_bytes(path, wanted)
		print("wrote " + ", ".join(str(path.relative_to(ROOT)) for path in artifacts))
		return
	problems = [str(path.relative_to(ROOT)) for path, wanted in artifacts.items() if not path.is_file() or path.read_bytes() != wanted]
	if problems:
		raise SystemExit("drift in: " + ", ".join(problems))
	print("family guy artifacts are current")


if __name__ == "__main__":
	main()
