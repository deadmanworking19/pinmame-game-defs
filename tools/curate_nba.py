"""Build the reviewed Stern NBA (2009) machine definition.

Deterministic and side-effect free until ``--write`` is passed. The device tables live in
``nba_devices.py`` and the spatial placements in ``nba_spatial.py``; the recreation note is the seed
``tools/seeds/stern/nba-2009-knowledge.md``. Excerpts under ``evidence/excerpts/stern.nba.2009/``
and the compact runtime summaries under ``evidence/runtime/sam/nba-*.json`` are committed inputs:
this script digests them into the source records and refuses to run when one is missing or changed.

Usage::

	python tools/curate_nba.py --check    # fail if the committed artifacts drift
	python tools/curate_nba.py --write    # regenerate the definition, knowledge note and spatial report
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_bytes

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
	sys.path.insert(0, str(TOOLS))

import nba_devices as dev  # noqa: E402
import nba_spatial as spatial  # noqa: E402
from nba_devices import CATALOG, CORE, IPDB, MANUAL, ROM, RT_BOOT, RT_COIL, RT_FASTFLIP, RT_LAMP, RT_PLAY, RT_POPS, RT_SWITCH, SCRIPT, TABLE, provenance  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "stern.nba.2009"
DEFINITION_PATH = ROOT / "machines/partial/stern/nba-2009.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/nba-2009.md"
KNOWLEDGE_SEED = ROOT / "tools/seeds/stern/nba-2009-knowledge.md"
AUDIT_PATH = ROOT / "reports/spatial/stern/nba-2009.json"
EXCERPT_ROOT = ROOT / "evidence/excerpts/stern.nba.2009"
RUNTIME_ROOT = ROOT / "evidence/runtime/sam"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"

MANUAL_SHA256 = "f74e8c1c8ad5c724d51b8f472b9163ee2f5de685558f99686863e35e4d268243"
TABLE_SHA256 = "ae322910ad7f74f984e0216c5bf05cd0984ab727bff455f13992d5afb708eb58"
SCRIPT_SHA256 = "c903c5acfe44d5db0d0477845abc7d223955435713c5f65e23dff005dc9db9ce"
IPDB_SHA256 = "c568a8cdbfa26d9009f5c600b4cd2594fab5146b2b969bcce27a2722e4a7f95f"
FASTFLIP_RUN_SHA256 = "23659cef818fbfb042917f94f4a188fbac7c5d1238902cd9548bf69b53d6ec51"

# acquired_at of each retained artifact: the table copy's creation time in the working root, the
# script's extraction time, the IPDB capture's retention time, and each harness run.json's write time.
TABLE_ACQUIRED_AT = "2026-10-30T18:44:21Z"
SCRIPT_ACQUIRED_AT = "2026-10-30T18:44:31Z"
IPDB_ACQUIRED_AT = "2026-10-30T19:36:18Z"
FASTFLIP_RUN_AT = "2026-10-30T19:12:07Z"
RUN_AT = {
	"nba-nba_802-boot-start.json": "2026-10-30T18:57:54Z", "nba-nba_801-boot-start.json": "2026-10-30T18:57:54Z",
	"nba-nba_802-gameplay-probe.json": "2026-10-30T19:00:57Z", "nba-nba_801-gameplay-probe.json": "2026-10-30T19:00:57Z",
	"nba-nba_802-bumper-sling-probe.json": "2026-10-30T19:15:59Z",
	"nba-nba_802-switch-test-sweep.json": "2026-10-30T18:47:45Z", "nba-nba_802-coil-test-sweep.json": "2026-10-30T18:47:15Z", "nba-nba_802-lamp-test-sweep.json": "2026-10-30T18:46:56Z",
	"nba-nba_801-switch-test-sweep.json": "2026-10-30T19:01:24Z", "nba-nba_801-coil-test-sweep.json": "2026-10-30T19:00:54Z", "nba-nba_801-lamp-test-sweep.json": "2026-10-30T19:00:35Z",
	"nba-nba_700-switch-test-sweep.json": "2026-10-30T19:04:54Z", "nba-nba_700-coil-test-sweep.json": "2026-10-30T19:04:23Z", "nba-nba_700-lamp-test-sweep.json": "2026-10-30T19:04:04Z",
	"nba-nba_600-switch-test-sweep.json": "2026-10-30T19:08:23Z", "nba-nba_600-coil-test-sweep.json": "2026-10-30T19:07:53Z", "nba-nba_600-lamp-test-sweep.json": "2026-10-30T19:07:34Z",
	"nba-nba_500-switch-test-sweep.json": "2026-10-30T19:11:53Z", "nba-nba_500-coil-test-sweep.json": "2026-10-30T19:11:23Z", "nba-nba_500-lamp-test-sweep.json": "2026-10-30T19:11:04Z",
}

CATALOG_JSON = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG_JSON["drivers"] if driver["id"].startswith("nba_")}
OLDER_DRIVERS = ("nba_801", "nba_700", "nba_600", "nba_500")
VERSIONS = {"nba_802": "V8.02", "nba_801": "V8.01", "nba_700": "V7.0", "nba_600": "V6.0", "nba_500": "V5.0"}


def sha256_file(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt(identifier: str, filename: str, locator: str, method: str = "manual", reviewed: bool = False, transcribed_by: str = "curator, 2026-10-30") -> dict[str, Any]:
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
		"id": identifier, "kind": "runtime_scenario", "uri": f"internal:evidence/runtime/sam/{filename}", "acquired_at": RUN_AT[filename],
		"revision": PINMAME_REVISION, "sha256": raw["sha256"], "locator": locator, "license": "NOASSERTION",
		"attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
	}
	if excerpts:
		source["excerpts"] = excerpts
	return source


def sources() -> list[dict[str, Any]]:
	boot = runtime_summary("nba-nba_802-boot-start.json")
	rom_sha = boot["runtime"]["rom_archive_sha256"]
	result: list[dict[str, Any]] = [
		{"attribution": "PinMAME contributors", "id": CATALOG, "kind": "pinmame_catalog", "license": "BSD-3-Clause", "locator": "PinmameGetGames nba_ driver records and clone graph (root nba_802; clones nba_500, nba_600, nba_700, nba_801).", "revision": PINMAME_REVISION, "uri": "https://github.com/vpinball/pinmame"},
		{"attribution": "PinMAME contributors", "id": CORE, "kind": "pinmame_core", "license": "BSD-3-Clause", "locator": "src/wpc/sam.c: INITGAME(nba, GEN_SAM, sam_dmd128x32, SAM_2COL, SAM_NO_AUX) and the five SAM1_ROM32MB nba_ ROM declarations (lines 3088-3094); the nba_ output typing that makes solenoids 13-14, 19, 23 and 25-32 #89 bulbs (lines 1492-1497); samlocals.fastflipaddr 0x010609be for nba_802 only (lines 1707-1708) and the VBLANK handler that publishes it as solenoid 33 (lines 2258-2268); samswitch_r (line 426) and the public switch, lamp, GI and DIP conversions shared by every S.A.M. game.", "revision": PINMAME_REVISION, "uri": "https://github.com/vpinball/pinmame"},
		{
			"acquired_at": "2026-10-30T18:41:53Z", "attribution": "Stern Pinball, Inc.", "id": MANUAL, "kind": "manual", "license": "NOASSERTION", "original_filename": "NBA-Manual.pdf", "rights": "NOASSERTION",
			"sha256": MANUAL_SHA256, "source_id": "stern", "uri": "https://wp.sternpinball.com/wp-content/uploads/2018/11/NBA-Manual.pdf",
			"locator": "Stern Pinball's NBA partial manual as published on its manuals page https://www.sternpinball.com/manuals/ and linked from IPDB 5442 as a \"Partial Manual ('Pink' and 'Blue' pages only)\": 33 scanned pages without a text layer (9,950,207 bytes). It holds only the parts book: the Blue Pages (Major Assemblies & Ramps, printed b1-b17 = PDF pages 1-17) and the Pink Pages (Parts Identification, printed p1-p16 = PDF pages 18-33). It has no switch, lamp or coil table, no location drawings and no wiring or schematic pages. Every cell was read from 300 dpi renders.",
			"excerpts": [
				excerpt("excerpt.nba.manual-blue-pages", "manual-blue-pages.md", "PDF pages 1-17 (printed b1-b17): optional kits, ball shooter and autoplunger, 4-ball trough, flippers, slingshots, spinning disk, steel ramp, 40-degree kicker, 3-bank drop target, plastic ramp, bumpers, Magna-hoop, lift-ramp up post, 30-degree eject and back panel"),
				excerpt("excerpt.nba.manual-pink-pages", "manual-pink-pages.md", "PDF pages 18-33 (printed p1-p16): backbox, cabinet parts and switches, coin door, playfield parts, rubbers, sockets and bulbs"),
			],
		},
		{"acquired_at": IPDB_ACQUIRED_AT, "attribution": "Internet Pinball Database", "id": IPDB, "kind": "human_review", "license": "NOASSERTION", "locator": "IPDB 5442 \"NBA\" (Stern Pinball, 2009, 4 players, Stern S.A.M. Board System): flippers (2), pop bumpers (3), slingshots (2), standup targets (9), 3-bank drop targets (1), captive ball (1), spinning disc (1), 2- and 3-ball multiball, a trajectory up-kicker that sends the ball airborne towards the hoop and a ramp-on-a-ramp that elevates to send a fast ball airborne towards the hoop; a large basketball hemisphere that glows. Designer John Borg's note: he added the free throw kicker that shoots the ball through the air at the backboard, the lift flap assembly in the plastic ramp, the spinning disc and the wire ramp / divert mechanism. Fetched as the Wayback Machine's 2024 id_ capture of https://www.ipdb.org/machine.cgi?id=5442; page SHA-256 " + IPDB_SHA256 + ", retained under the working root's review-artifacts/nba-2009/ipdb/.", "sha256": IPDB_SHA256, "uri": "https://www.ipdb.org/machine.cgi?id=5442"},
		{
			"acquired_at": TABLE_ACQUIRED_AT, "attribution": "Bambi Plattfuss (VPX recreation, with help of Team PP, JPJ, Chucky, DJrobx, Arngrim and Vogldiance)", "id": TABLE, "kind": "vpx_table", "license": "NOASSERTION",
			"locator": "NBA (Stern 2009).vpx, table version 1.2 released 08.08.2020, from the user's VPX archive (55,160,832 bytes; extracted with vpxtool git:v0.33.3 into a 570-file extraction sealed by the working root's vpx-sources/stern/nba-2009/manifest.json). Script cGameName nba_802. Playfield bounds left 0, top 0, right 952, bottom 2115. The project has not verified it as known-working; it names its pop-bumper objects the other way round from the ROM (conflict.pop-bumper-sides) and models the trough in its script.",
			"sha256": TABLE_SHA256, "uri": "external:vpx-sources/stern/nba-2009/source/NBA (Stern 2009).vpx",
		},
		{
			"acquired_at": SCRIPT_ACQUIRED_AT, "attribution": "Bambi Plattfuss and the contributors credited in the script", "id": SCRIPT, "kind": "vpx_script", "license": "NOASSERTION",
			"locator": "Embedded Script stream of the exact retained table, extracted with vpxtool extractvbs (1,213 lines, cGameName \"nba_802\", LoadVPM \"03000000\", \"SAM.VBS\", 3.50; it differs from the extraction's script.vbs only in how four comment lines' non-ASCII characters are decoded). Used for controller-facing behaviour only: which public switches it pulses (vpmTimer.PulseSw) or holds (Controller.Switch), its cvpmTrough, cvpmSaucer, cvpmDropTarget and cvpmImpulseP objects, the SolCallback and SolModCallback lists (Q8-Q11, Q17, Q18 and Q22 commented out or empty), InitVpmFFlipsSAM, and the FadeLamp bindings 3-64.",
			"sha256": SCRIPT_SHA256, "uri": "external:vpx-sources/stern/nba-2009/source/NBA (Stern 2009).vbs",
		},
		{
			"attribution": "Stern Pinball game code; ROM bytes remain external", "id": ROM, "kind": "rom_static_analysis", "revision": "V8.02 U.S.A. English",
			"locator": "Read-only user-authorized archive nba_802.zip (member nba_802.bin, CRC ba681dac). The archives nba_801.zip (nba_v8-01_a.bin, CRC 0f8b146e), nba_700.zip (nba_v7-0_a.bin, CRC 15ece43b), nba_600.zip (nba_v6-0a.bin, CRC af2fbcf4) and nba_500.zip (nba_v5-0_a.bin, CRC 01b0c27a) hold the CRCs pinned sam.c declares. The ROM's own service tests are the definition's naming source; they are read from the harness frames, not from static analysis.",
			"sha256": rom_sha, "uri": "external:vpinmame-roms/nba_802.zip",
		},
	]
	result.append(runtime_source(RT_SWITCH, "nba-nba_802-switch-test-sweep.json", "Fresh-NVRAM nba_802 switch test: every matrix switch 1-64, dedicated 65-72 and 81-88 and -7 to -4 held for 1.2 s; the ROM prints the name, LAST SW line and wire colours of the switch it reads closed.", [excerpt("excerpt.nba.rom-service-tests", "rom-service-tests.md", "ROM switch, dedicated-switch, coil and lamp test names and wire colours transcribed from the retained DMD frames of all five firmware revisions")]))
	result.append(runtime_source(RT_COIL, "nba-nba_802-coil-test-sweep.json", "Fresh-NVRAM nba_802 Single Coil Test: 40 selector positions (#1-#32, then wrapping) each fired once and paired with the public solenoid addresses that changed."))
	result.append(runtime_source(RT_LAMP, "nba-nba_802-lamp-test-sweep.json", "Fresh-NVRAM nba_802 Single Lamp Test: 82 selector positions (lamps 1-80, then wrapping); every position lights its own public lamp."))
	result.append(runtime_source(RT_BOOT, "nba-nba_802-boot-start.json", "nba_802 boot, four coins and Start with trough switches 18-21 closed: observes the 128x32 DMD, GI 0, the attract-mode lamps, the trough up-kicker Q1 and the optional coil Q24 pulsing once per coin."))
	result.append(runtime_source(RT_PLAY, "nba-nba_802-gameplay-probe.json", "nba_802 gameplay probe: coins and Start, a served and plunged ball, the left orbit, both flipper buttons, a ball in each eject hole (35 and 9), the three MVP drop targets going down and back up, and the basket opto; each step lists the public solenoids that changed and the lamps that turned on."))
	result.append(runtime_source(RT_POPS, "nba-nba_802-bumper-sling-probe.json", "nba_802 probe that hits each pop bumper switch (30, 31, 32) and slingshot switch (26, 27) twice, in two passes of opposite order: each bumper switch fires its own coil and lamp (30: Q9, lamp 60; 31: Q10, lamp 61; 32: Q11, lamp 62) and each slingshot switch its own coil (26: Q17; 27: Q18)."))
	result.append({
		"id": RT_FASTFLIP, "kind": "runtime_scenario", "uri": "external:pinmame-review-artifacts/nba-2009/diagnostics/fastflip-getter-nba_802", "acquired_at": FASTFLIP_RUN_AT, "revision": PINMAME_REVISION, "sha256": FASTFLIP_RUN_SHA256,
		"locator": "nba_802 gameplay probe re-run under a diagnostic wrapper that reads game RAM at sam.c's fast-flip address 0x010609be and PinmameGetSolenoid(33) after every output poll, with a Family Guy boot run on the same emulator build for comparison; the logs are transcribed in the excerpt.",
		"license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
		"excerpts": [excerpt("excerpt.nba.fast-flip-diagnostic", "fast-flip-diagnostic.md", "Diagnostic log fastflip-word.json of the retained run, the run's envelope and the Family Guy comparison run", method="manual")],
	})
	result.append(runtime_source("runtime.nba.nba-801.boot-start", "nba-nba_801-boot-start.json", "nba_801 boot with the same switches, coins and Start as the nba_802 run."))
	result.append(runtime_source("runtime.nba.nba-801.gameplay-probe", "nba-nba_801-gameplay-probe.json", "nba_801 gameplay probe with the same scenario as the nba_802 run."))
	for driver in OLDER_DRIVERS:
		for kind in ("switch", "coil", "lamp"):
			result.append(runtime_source(f"runtime.nba.{driver.replace('_', '-')}.{kind}-test-sweep", f"nba-{driver}-{kind}-test-sweep.json", f"Fresh-NVRAM {driver} ({VERSIONS[driver]}) {kind} test sweep with the same scenario as the nba_802 run, retained to compare the ROM's names and public addresses across firmware."))
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
	text = f"Firmware revision {VERSIONS[driver_id]} (U.S.A., English) of the same 2009 NBA machine; PinMAME initializes every nba_ driver with the same game data (S.A.M. generation, 128x32 DMD, SAM_2COL lamp matrix, no auxiliary board). The retained switch, coil and lamp test sweeps of all five revisions show the same test frames, pixel for pixel, and fire the same public solenoids."
	stem = f"runtime.nba.{driver_id.replace('_', '-')}"
	text += f" This revision's sweeps are sources {stem}.switch-test-sweep, {stem}.coil-test-sweep and {stem}.lamp-test-sweep."
	if driver_id == "nba_801":
		text += f" Its boot and gameplay probes ({stem}.boot-start, {stem}.gameplay-probe) repeat the nba_802 scenarios and change the same public solenoids at every step, except that in two of the drop-target reset steps the last MVP reset pulse or basketball flash falls on the other side of the step boundary."
	if driver_id == "nba_802":
		return text + " Only nba_802 has a fast-flip RAM address in pinned sam.c, so only it publishes the synthetic game-on solenoid 33."
	return text + " Pinned sam.c gives it no fast-flip RAM address, so public solenoid 33 stays 0 on it."


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
		mechanism("mechanism.trough", "Four-ball trough, shooter lane and autoplunger", "kicker", [o(1), o(2)], [s(n) for n in (18, 19, 20, 21, 22, 23)],
			"Four balls rest in the trough assembly 500-6318-24-ND on micro switches 18, 19 and 20 and on the beam of the dual opto boards at position 21, the right-hand end where the up-kicker sits (the ROM names 18 TROUGH #4 (L) and 21 TROUGH #1 (R)). Q1 (26-1200) lifts the right-most ball past the jam beam 22 into the shooter lane, where it rests on switch 23 (shooter lane switch 180-5157-00). The player plunges it with the ball shooter assembly, or the autoplunger Q2 (24-940) fires it. In the retained gameplay probes the ROM pulsed Q1 at Start and did not fire Q2 for the first ball while switch 23 was closed. Keep per-position occupancy rather than a count.", script + (RT_PLAY,), assembly="500-6318-24-ND"),
		mechanism("mechanism.left-eject", "Left eject (switch 35, Q4)", "kicker", [o(4)], [s(35)],
			"An eject hole: a ball closes switch 35 and Q4 kicks it out. In the retained gameplay probe the ROM pulsed Q4 and energized the basket magnet Q3 while switch 35 was closed, which agrees with IPDB's trajectory up-kicker that sends the ball airborne towards the hoop; the retained table models this hole as that kicker (a 55-degree kick towards the Magna-hoop). The parts book lists a 40-degree long-throw kicker 500-7157-01 (27-1400 coil) and a 30-degree eject 500-6511-01-ND (24-940 coil) without saying which hole each one serves.", script + (RT_PLAY, IPDB), status="observed"),
		mechanism("mechanism.right-eject", "Right eject (switch 9, Q20)", "kicker", [o(20)], [s(9)],
			"An eject hole: a ball closes switch 9 and Q20 kicks it out. In the retained gameplay probe the ROM pulsed Q20 while switch 9 was closed and flashed Q19, Q27 and Q31. The retained table kicks it out flat.", script + (RT_PLAY,), status="observed"),
		mechanism("mechanism.mvp-drop-targets", "M-V-P 3-bank drop target", "drop_target_bank", [o(7)], [s(13), s(12), s(11)],
			"Three drop targets M, V, P, from the rear: (M)VP switch 13, M(V)P 12 and MV(P) 11, each on its own interrupter of the slotted opto PCB 520-5252-03. A target's switch reads closed while it is down; Q7 (24-940) raises the whole bank. Lamps 57-59 spell the same letters. In the retained gameplay probe the ROM fired Q7 and the shaker Q8 after the third target went down and kept pulsing Q7 for as long as the switches still read down.", script + (RT_PLAY,), [{"id": "position.up", "label": "Bank up", "sensors": []}, {"id": "position.down", "label": "Target down", "sensors": [s(13), s(12), s(11)]}], assembly="500-7029-03-00"),
		mechanism("mechanism.magna-hoop", "Magna-hoop basket magnet", "other", [o(3)], [s(34)],
			"The Magna-hoop assembly 500-7162-00 carries a magnet and connector assembly 511-5221-00 behind its backboard plastic (IPDB photo: 'Electromagnet Behind Hoop Backboard'); basket opto 34 sees a ball pass through the hoop. The ROM energized Q3 with the left eject Q4 in the retained gameplay probe. How long the magnet holds a ball and what releases it are not documented; the retained table holds the ball at the backboard until it reaches switch 34.", script + (RT_PLAY, IPDB), status="observed", assembly="500-7162-00"),
		mechanism("mechanism.ramp-diverter", "Ramp diverter (Q5)", "diverter", [o(5)], [],
			"The ROM names Q5 RAMP DIVERTER. The parts book lists one diverter assembly 515-6596-00-A9 on the left plastic ramp 500-7158-00, and IPDB's designer note mentions a wire ramp / divert mechanism. Which ramp exits its positions select is not documented; the retained table swaps two walls on the left side of the playfield.", script + (IPDB,), status="observed"),
		mechanism("mechanism.basket-diverter", "Basket diverter (Q12)", "diverter", [o(12)], [],
			"The ROM names Q12 BASKET DIVERTER. IPDB's designer note mentions a lift flap assembly in the plastic ramp (the ramp-on-a-ramp that sends a fast ball airborne towards the hoop), and the parts book lists an up-post assembly 500-7161-00 titled 'LIFT RAMP' with a 26-1200 coil; neither ties a coil number to them. The retained table rotates a flap into the ball's path near the top centre while Q12 is energized.", script + (IPDB,), status="observed"),
		mechanism("mechanism.orbit-post", "Orbit up/down post (Q21)", "gate", [o(21)], [],
			"The ROM names Q21 ORBIT UP/DOWN POST and drives it as a held output: in the retained probes it changes state once at a time (after the ball leaves the shooter lane, after a flipper press, at the first pop-bumper hit). The retained table raises a post across the orbit while Q21 is energized. The physical post assembly is not identified in the partial parts book.", script + (RT_PLAY, RT_POPS), status="observed"),
		mechanism("mechanism.spinning-disk", "Spinning disk", "motorized", [o(6), o(22)], [],
			"A motorized disk in the centre of the playfield: spinning disk assembly 500-7144-01 with motor 511-5190-00 and disk/hub weldment 515-7714-00 under an adhesive art pad. Q6 is the motor and Q22 the SPINNING DISK MOTOR RELAY: the ROM's coil test energizes Q22 together with Q6 and Q22 alone, and in the retained bumper probe the ROM switched Q6 and Q22 on and off together. What the relay switches (for example motor direction or supply) is not documented, so the disk's direction and speed control are unknown.", common + (RT_POPS, SCRIPT), status="observed", assembly="500-7144-01"),
		mechanism("mechanism.captive-ball", "Captive ball", "other", [], [s(10)],
			"IPDB lists one captive ball; switch 10 (CAPTIVE BALL) reports a hit and flash Q30 and lamp 22 (captive ball arrow) belong to it. The retained table models a captive ball striking a target in the upper left.", script + (IPDB,), status="observed"),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", [o(9), o(10), o(11)], [s(30), s(31), s(32)],
			"Three pop bumpers with 26-1200 coils Q9-Q11, stack switches 180-5015-04 and white wedge-base LED modules. The retained probe pairs switch 30 with Q9 and lamp 60 (TOP), 31 with Q10 and lamp 61 and 32 with Q11 and lamp 62; every hit also runs the shaker Q8 and flashes Q31. The ROM names 31/Q10/61 LEFT and 32/Q11/62 RIGHT, the parts book the reverse (conflict.pop-bumper-sides).", common + (RT_POPS, SCRIPT), status="conflicted"),
		mechanism("mechanism.slingshots", "Slingshots", "other", [o(17), o(18)], [s(26), s(27)],
			"Left slingshot Q17 with switch 26 and right slingshot Q18 with switch 27 (23-800 coils, assembly 500-5849-00-ND with two stack switches 180-5054-00 each). The retained probe shows each switch firing its own coil and the slingshot flash Q32.", common + (RT_POPS, SCRIPT), assembly="500-5849-00-ND"),
		mechanism("mechanism.flippers", "Lower flippers", "other", [o(15), o(16)], [d(9), d(10), d(11), d(12)],
			"Q15 (23-1500) drives the left flipper assembly 500-6543-15-ND and Q16 (23-900) the right assembly 500-6543-05-ND, each with a power (EOS) switch 180-5149-00 on dedicated D-10 / D-12. The cabinet buttons are single-stack switches on D-9 / D-11; no upper flipper is fitted. In the retained gameplay probe each held button made the ROM energize its own flipper coil.", common + (RT_PLAY,)),
		mechanism("mechanism.lanes-and-targets", "Lanes, orbits, ramps and stand-up targets", "other", [], [s(n) for n in (1, 2, 3, 4, 5, 6, 7, 8, 14, 24, 25, 28, 29, 33, 36, 37, 47)],
			"The remaining playfield switches at their enumerated addresses: the left 4-bank (1-4, rear to front) and right 3-bank (5-7) stand-up targets, the pop-bumper target 47, the left and right orbits (14, 36), the right ramp entrance and exit (8, 37), the left ramp entrance (33), and the outlanes and return lanes (24, 25, 28, 29). Use the pulse flag recorded on each switch; the parts book lists ramp opto transceivers and roll-under switches without addresses.", script),
		mechanism("mechanism.optional-devices", "Optional shaker motor and optional coil", "other", [o(8), o(24)], [],
			"The ROM names Q8 SHAKER MOTOR (OPTIONAL) and drives it on every pop-bumper hit and the MVP bank reset in the retained probes; the parts book lists no shaker. Q24 OPTIONAL COIL is skipped by the coil test but pulsed for about 130 ms once per coin in the retained runs, as a coin meter or knocker would be; the parts book lists an optional +12 V meter that was not included with this machine.", common + (RT_BOOT, RT_PLAY, RT_POPS), status="observed"),
	]


def conflicts() -> list[dict[str, Any]]:
	return [{
		"id": "conflict.pop-bumper-sides",
		"path": "inputs[binding.device=31|32]; outputs[binding.group=pinmame.output.solenoid,binding.device=10|11]; outputs[binding.group=pinmame.output.lamp,binding.device=61|62]",
		"description": "Which of the two lower pop bumpers is switch 31, coil Q10 and lamp 61, and which is switch 32, Q11 and lamp 62. The ROM's switch, coil and lamp tests name 31, Q10 and 61 LEFT POP BUMPER and 32, Q11 and 62 RIGHT POP BUMPER, and the bumper probe shows each switch firing its own coil and lamp. The parts book's bumper page (printed b13, a page whose title, 'Left, Right & Bottom Bumper', is generic) prints 'LAMPS 60 (TOP) 61 (RIGHT) 62 (LEFT)' and the switch callout 'TOP / RIGHT / LEFT' beside 'SW. 30 / SW. 31 / SW. 32'. The retained table agrees with the ROM on the lamps (l61a on the left bumper, l62a on the right) but places its bumper objects as the parts book does (sw31 on the right, sw32 on the left) and plays its LeftJet sound on sw31. A recreation needs to know which side each address is. The definition labels and places them by the ROM's names. Resolution path: close the left lower pop bumper's switch on a physical NBA in switch test and read the number the display prints, or find Stern's NBA switch and lamp location drawings; an owner could settle it in a minute.",
		"source_refs": [ROM, RT_SWITCH, RT_POPS, MANUAL, TABLE, SCRIPT],
	}]


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "NBA", "manufacturer": "Stern", "year": 2009, "kind": "physical_pinball", "ipdb_id": 5442, "opdb_id": "G5K19-MBRlz"},
		"coverage": {
			"status": "partial",
			"missing": ["mechanism_behavior", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {"address_enumeration": "validated", "catalog_identity": "validated", "mechanisms": "observed", "physical_wiring": "observed", "recreation_knowledge": "observed", "semantic_naming": "conflicted", "spatial_placement": "observed", "variant_coverage": "validated"},
		},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(), "inputs": dev.inputs(), "outputs": dev.outputs(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance(CORE, RT_BOOT), "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(CORE, MANUAL)}}],
		"mechanisms": mechanisms(), "relationships": [], "sources": sources(),
		"knowledge": {"path": "knowledge/stern/nba-2009.md", "status": "partial"}, "conflicts": conflicts(),
	}
	spatial.attach(definition, spatial.load_seed())
	return definition


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
		"located_placements": len(placements),
		"validated_placements": sum(pl["provenance"]["status"] == "validated" for pl in placements),
		"candidate_placements": sum(pl["provenance"]["status"] == "candidate" for pl in placements),
		"missing_spatial_ids": missing,
		"candidate_spatial_ids": [x["id"] for group in groups for x in definition[group] if (x.get("spatial") or {}).get("status") == "candidate"],
		"unresolved_conflict_ids": [x["id"] for x in definition["conflicts"] if x.get("status", "unresolved") == "unresolved"],
		"projection_classes": {
			"exact_named_vpx_object_center": "observed: the table's swN targets, triggers, gates, walls and kickers, and its pop bumpers (placed by the ROM's side names and conflicted)",
			"insert_light_candidate": "candidate only: the 51 used lamps among 3-59, 63 and 64 carry the centre of the table's insert Light lN, a render light that draws the playfield image on an insert wall or ring surface and sits on no bulb (is_bulb_light and show_bulb_mesh false). Such a light never makes a socket on its own, so these lamps stay unplaced (candidate_spatial_ids) until a bulb object or a location drawing places their sockets. The bumper lamps 60-62 sit at their bulb lights, observed for 60 and conflicted for 61 and 62 with the pop-bumper sides; the start and tournament button lamps are cabinet devices",
			"coil_mechanism_anchor": "observed effect anchor on the mechanism object the coil drives (flippers, kickers, bumpers, sling walls, the drop-target bank mean, the diverter walls' mean, the RampDiverter primitive, the ODiv wall, the turntable); the coil body is not modelled",
			"flasher_bulb_light": "observed emitter on one bulb light per lamp at a dome primitive or under an insert (F14a/b, F23, F25a-F28a, F29, F30a, F32a/b); VPX Flasher sprites are never used",
			"manual_drawing_projection": "not available: the partial parts book has no location drawings",
			"cabinet_or_service": "not applicable", "virtual_or_unused": "not applicable"},
		"reason": "Stern's public NBA document has no location drawings, so no placement can be checked against the factory, and the retained table is the only coordinate source. It has no objects for the trough sensors 18-22, models no bulb for the back-panel flashes Q13 and Q19, for the three pop-bumper flash lamps Q31 or for the 51 insert lamps (whose coordinates are kept only as candidates), and has no per-bulb G.I. wiring to check; the pop-bumper sides are also conflicted. Location drawings, a second table or measured placements are needed before author readiness.",
	}


def knowledge_text() -> str:
	return KNOWLEDGE_SEED.read_text(encoding="utf-8")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--check", action="store_true")
	group.add_argument("--write", action="store_true")
	args = parser.parse_args()
	definition = build()
	artifacts = {
		DEFINITION_PATH: canonical_bytes(definition),
		KNOWLEDGE_PATH: knowledge_text().encode("utf-8"),
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
	print("nba artifacts are current")


if __name__ == "__main__":
	main()
