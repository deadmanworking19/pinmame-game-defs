"""Device tables for the Stern NBA (2009) definition.

Stern's public NBA document is a partial parts book (the Blue and Pink pages), so the game's own
service tests are the source that names every address: each literal below was read from the
retained ROM test frames (``evidence/excerpts/stern.nba.2009/rom-service-tests.md``), the parts
book excerpts beside it, the retained harness summaries under ``evidence/runtime/sam/`` or the
pinned PinMAME ``sam.c``. The builders turn the tables into schema-shaped inputs and outputs;
``curate_nba.py`` owns the source records, mechanisms and artifact writes.
"""

from __future__ import annotations

import re
from typing import Any


MANUAL = "manual.stern-nba.2009-parts"
CORE = "pinmame.core.46e1a01a0f73"
CATALOG = "pinmame.catalog.46e1a01a0f73"
SCRIPT = "vpx.script.nba-2020-embedded"
TABLE = "vpx.table.nba-2020"
ROM = "rom.stern-nba.nba-802"
IPDB = "ipdb.nba.5442"
RT_SWITCH = "runtime.nba.nba-802.switch-test-sweep"
RT_COIL = "runtime.nba.nba-802.coil-test-sweep"
RT_LAMP = "runtime.nba.nba-802.lamp-test-sweep"
RT_BOOT = "runtime.nba.nba-802.boot-start"
RT_PLAY = "runtime.nba.nba-802.gameplay-probe"
RT_POPS = "runtime.nba.nba-802.bumper-sling-probe"
RT_FASTFLIP = "runtime.nba.nba-802.fast-flip-diagnostic"

# The pop-bumper sides are disputed between the ROM's names and the parts book (curate_nba.py's
# conflict.pop-bumper-sides); every device it touches carries conflicted provenance.
BUMPER_SIDE_SWITCHES = {31, 32}
BUMPER_SIDE_COILS = {10, 11}
BUMPER_SIDE_LAMPS = {61, 62}


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def aliases(namespace: str, value: int | str, manual_value: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(value)}]
	if manual_value is not None:
		result.append({"namespace": "manual.address", "value": manual_value})
	return result


# --------------------------------------------------------------------------------------------
# Switch matrix
# --------------------------------------------------------------------------------------------

# The ROM's switch test prints two wire colours under every matrix switch: the first is shared by
# each run of 16 consecutive switches, the second by every switch at the same position in its run.
MATRIX_DRIVE_WIRE = ["GRN-BLU", "GRN-VIO", "GRN-GRY", "GRN-WHT"]
MATRIX_RETURN_WIRE = ["BRN-BLK", "BRN", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BLK", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-WHT"]

# number: (label, pulse, roles, switch_type, part number, location, ROM switch-test name, note)
# pulse follows the retained script's controller-facing behaviour (vpmTimer.PulseSw = True,
# Controller.Switch held, saucer, trough and drop-target objects = False).
SWITCHES: dict[int, tuple[str, bool, tuple[str, ...], str, str, str, str, str]] = {
	1: ("Left 4-bank target 1 (top)", True, (), "unknown", "", "Left side of the playfield", "L. 4-BANK (TOP)", "One of four stand-up targets in the left bank, numbered 1-4 from the rear."),
	2: ("Left 4-bank target 2", True, (), "unknown", "", "Left side of the playfield", "LEFT 4-BANK #2", ""),
	3: ("Left 4-bank target 3", True, (), "unknown", "", "Left side of the playfield", "LEFT 4-BANK #3", ""),
	4: ("Left 4-bank target 4 (bottom)", True, (), "unknown", "", "Left side of the playfield", "L. 4-BANK (BOT)", ""),
	5: ("Right 3-bank target (top)", True, (), "unknown", "", "Right side of the playfield", "R. 3-BANK (TOP)", "One of three stand-up targets in the right bank."),
	6: ("Right 3-bank target (middle)", True, (), "unknown", "", "Right side of the playfield", "R. 3-BANK (MID)", ""),
	7: ("Right 3-bank target (bottom)", True, (), "unknown", "", "Right side of the playfield", "R. 3-BANK (BOT)", ""),
	8: ("Right ramp entrance", True, (), "unknown", "", "Right ramp", "R. RAMP ENTRANCE", "The retained table models it as a gate switch it pulses. The parts book lists two opto transceiver assemblies (500-6775-01) on the steel ramp 511-5208-00 and two roll-under switch assemblies (515-6556-04-GE) plus two opto transceivers on the left plastic ramp 500-7158-00, without saying which switch each one is, so the contact type stays unknown."),
	9: ("Right eject", False, ("ball.position",), "unknown", "", "Right eject hole", "RIGHT EJECT", "The ball rests on it until coil Q20 kicks it out. The parts book's 30-degree eject page (500-6511-01-ND) carries a micro-switch eject switch assembly 500-6520-01, but that page's callouts (coil Q26, switch 45) are generic, so which NBA eject it is stays unsettled."),
	10: ("Captive ball", True, (), "unknown", "", "Captive-ball lane, upper left", "CAPTIVE BALL", "The retained table models a captive ball striking a target it pulses."),
	11: ("MV(P) drop target", False, ("position.down",), "opto", "520-5252-03", "3-bank drop target assembly 500-7029-03-00", "MV(P) DROP TARGET", "Third target of the MVP bank. The assembly carries the slotted opto PCB 520-5252-03 (one interrupter per target); the switch reads closed while the target is down."),
	12: ("M(V)P drop target", False, ("position.down",), "opto", "520-5252-03", "3-bank drop target assembly 500-7029-03-00", "M(V)P DROP TARGET", "Second target of the MVP bank on the slotted opto PCB 520-5252-03."),
	13: ("(M)VP drop target", False, ("position.down",), "opto", "520-5252-03", "3-bank drop target assembly 500-7029-03-00", "(M)VP DROP TARGET", "First target of the MVP bank on the slotted opto PCB 520-5252-03."),
	14: ("Left orbit", True, (), "unknown", "", "Left orbit lane", "LEFT ORBIT", ""),
	15: ("Tournament start button", False, ("cabinet.tournament-start",), "button", "180-5174-00", "Cabinet front, yellow square tournament button 500-6587-06-TL", "TOURNAMENT START", "Microswitch of the tournament button assembly, lit by lamp 2."),
	16: ("Start button", False, ("cabinet.start",), "button", "180-5174-00", "Cabinet front, green round start button 500-6388-44-TL", "START BUTTON", "Microswitch of the start button assembly, lit by lamp 1."),
	18: ("Trough 4 (left)", False, ("ball.position",), "microswitch", "180-5119-02", "4-ball trough assembly 500-6318-24-ND, below playfield", "TROUGH #4 (L)", "One of the three trough micro switches the parts book prints as SW. 18, 19 and 20."),
	19: ("Trough 3", False, ("ball.position",), "microswitch", "180-5119-02", "4-ball trough assembly 500-6318-24-ND", "TROUGH #3", ""),
	20: ("Trough 2", False, ("ball.position",), "microswitch", "180-5119-02", "4-ball trough assembly 500-6318-24-ND", "TROUGH #2", ""),
	21: ("Trough 1 (right)", False, ("ball.position",), "opto", "515-0173-00 / 515-0174-00", "4-ball trough assembly 500-6318-24-ND, dual opto boards", "TROUGH #1 (R)", "The parts book prints SW. 21 on the dual opto transmitter and receiver boards (515-0173-00 / 515-0174-00); the switch reads closed while a ball blocks the beam."),
	22: ("Trough jam", False, ("ball.position",), "opto", "515-0173-00 / 515-0174-00", "4-ball trough assembly 500-6318-24-ND, dual opto boards", "TROUGH JAM", "Second beam of the same dual opto board pair (SW. 22 in the parts book). The retained script pulses it as the up-kicker serves a ball; a physical beam stays blocked for as long as a ball sits in it."),
	23: ("Shooter lane", False, ("ball.position",), "unknown", "180-5157-00", "Shooter lane switch assembly 500-6096-00", "SHOOTER LANE", "The parts book's autoplunger page prints it as SW. 23. The auto-launch coil Q2 fires the ball resting on it."),
	24: ("Left outlane", False, (), "unknown", "", "Left outlane", "LEFT OUTLANE", ""),
	25: ("Left return lane", False, (), "unknown", "", "Left return lane", "LEFT RETURN LANE", ""),
	26: ("Left slingshot", True, (), "leaf", "180-5054-00", "Left slingshot assembly 500-5849-00-ND (two switches per assembly)", "LEFT SLINGSHOT", "The parts book prints LEFT SW. 26 (Qty. 2) on the slingshot page: two stack switches in parallel."),
	27: ("Right slingshot", True, (), "leaf", "180-5054-00", "Right slingshot assembly 500-5849-00-ND (two switches per assembly)", "RIGHT SLINGSHOT", "The parts book prints RIGHT SW. 27 (Qty. 2): two stack switches in parallel."),
	28: ("Right return lane", False, (), "unknown", "", "Right return lane", "RIGHT RETURN LANE", ""),
	29: ("Right outlane", False, (), "unknown", "", "Right outlane", "RIGHT OUTLANE", ""),
	30: ("Top pop bumper", True, (), "leaf", "180-5015-04", "Top pop bumper, below playfield", "TOP POP BUMPER", "Bumper stack (blade) switch with spoon actuator (switch assembly 515-6459-09/R). The ROM pairs it with coil Q9 and lamp 60."),
	31: ("Left pop bumper", True, (), "leaf", "180-5015-04", "Pop bumper, below playfield", "LEFT POP BUMPER", "Bumper stack (blade) switch with spoon actuator. The ROM pairs it with coil Q10 and lamp 61, and its service tests call all three LEFT POP BUMPER; the parts book's bumper page prints RIGHT SW. 31 and lamp 61 (RIGHT) instead (conflict.pop-bumper-sides)."),
	32: ("Right pop bumper", True, (), "leaf", "180-5015-04", "Pop bumper, below playfield", "RIGHT POP BUMPER", "Bumper stack (blade) switch with spoon actuator. The ROM pairs it with coil Q11 and lamp 62, and its service tests call all three RIGHT POP BUMPER; the parts book's bumper page prints LEFT SW. 32 and lamp 62 (LEFT) instead (conflict.pop-bumper-sides)."),
	33: ("Left ramp enter", True, (), "unknown", "", "Left ramp entrance", "LEFT RAMP ENTER", "See switch 8 for the ramp switch hardware the parts book lists without addresses."),
	34: ("Basket opto", True, (), "opto", "", "Magna-hoop basket", "BASKET OPTO", "The ROM names it an opto. The retained table pulses it as a ball passes through the hoop and releases the ball its backboard magnet holds."),
	35: ("Left eject", False, ("ball.position",), "unknown", "", "Left eject hole", "LEFT EJECT", "The ball rests on it until coil Q4 kicks it out; see switch 9 for the eject hardware pages."),
	36: ("Right orbit", True, (), "unknown", "", "Right orbit lane", "RIGHT ORBIT", ""),
	37: ("Right ramp exit", True, (), "unknown", "", "Right ramp exit", "R. RAMP EXIT", "The retained table models it as a gate switch it pulses; see switch 8 for the ramp switch hardware."),
	47: ("Pop bumper target", True, (), "unknown", "", "Pop bumper area", "POP BUMPER TARGET", "The retained table models a stand-up target it pulses."),
}
ROM_UNUSED_SWITCH_NAME = "SWITCH #{n}"
UNUSED_SWITCHES = [n for n in range(1, 65) if n not in SWITCHES]
INITIAL_ACTIVE = {18, 19, 20, 21}
SCRIPT_SWITCHES = set(SWITCHES) - {15, 16}


def switch_id(number: int) -> str:
	label = SWITCHES[number][0] if number in SWITCHES else f"Unused matrix switch {number}"
	return f"switch.{number}-{slug(label)}"


def matrix_wires(number: int) -> tuple[str, str]:
	run, position = divmod(number - 1, 16)
	return MATRIX_DRIVE_WIRE[run], MATRIX_RETURN_WIRE[position]


def matrix_switch(number: int) -> dict[str, Any]:
	spec = SWITCHES.get(number)
	drive_wire, return_wire = matrix_wires(number)
	label = spec[0] if spec else f"Unused matrix switch {number}"
	sources = [RT_SWITCH, CORE]
	if spec:
		if spec[4] or "parts book" in spec[7]:
			sources.insert(0, MANUAL)
		if number in SCRIPT_SWITCHES:
			sources.append(SCRIPT)
		if number in {26, 27, 30, 31, 32}:
			sources.append(RT_POPS)
		if number in {9, 11, 12, 13, 14, 18, 19, 20, 21, 23, 34, 35}:
			sources.append(RT_PLAY)
	physical: dict[str, Any] = {"switch_type": spec[3] if spec else "unknown"}
	if spec:
		if spec[4]:
			physical["part_number"] = spec[4]
		physical["location"] = spec[5]
		note = f"The ROM's switch test prints \"{spec[6]}\" with the wire colours {drive_wire} / {return_wire}. {spec[7]}".strip()
		note += " normally_closed is false: the public bit is active-high (pinned PinMAME's samswitch_r complements the matrix word on its way to the CPU's active-low port), the ROM's switch test reports a held public 1 as the closed switch, and the retained gameplay probes play a game with every unpressed switch at 0."
		physical["notes"] = note
	else:
		physical["notes"] = f"The ROM's switch test prints its generic name \"{ROM_UNUSED_SWITCH_NAME.format(n=number)}\" (wire colours {drive_wire} / {return_wire}), the retained table binds nothing to it and the parts book lists no hardware for it."
	result: dict[str, Any] = {
		"id": switch_id(number), "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": False, "pulse": spec[1] if spec else False,
		"availability": "used" if spec else "unused", "physical": physical,
		"wiring": {"board": "CPU/Sound board switch matrix", "drive_wire": drive_wire, "return_wire": return_wire},
		"provenance": provenance(*sources, status="conflicted" if number in BUMPER_SIDE_SWITCHES else "validated"),
	}
	if spec and spec[2]:
		result["roles"] = list(spec[2])
	if number in INITIAL_ACTIVE:
		result["initial_active"] = True
	return result


# --------------------------------------------------------------------------------------------
# Dedicated switches and DIP switch
# --------------------------------------------------------------------------------------------

DEDICATED_DEVICES = [65, 66, 67, 68, 69, 70, 71, 72, 84, 83, 82, 81, 88, 87, 86, 85, -7, -6, -5, -4, -3, -2, -1, 0]
DEDICATED_LABELS = [
	"Left coin slot", "Center coin slot / bill validator", "Right coin slot", "Fourth coin slot", "Fifth coin slot", "Unused dedicated switch D6", "Unused dedicated switch D7", "Unused dedicated switch D8",
	"Left flipper button", "Left flipper end-of-stroke", "Right flipper button", "Right flipper end-of-stroke", "Unused upper left flipper button D13", "Unused dedicated switch D14", "Unused upper right flipper button D15", "Unused dedicated switch D16",
	"Pendulum tilt", "Slam tilt", "Ticket notch", "Unused dedicated switch D20", "Coin-door Back button", "Coin-door Minus button", "Coin-door Plus button", "Coin-door Select button",
]
DEDICATED_TYPES = ["button", "button", "button", "button", "button", "unknown", "unknown", "unknown", "button", "leaf", "button", "leaf", "unknown", "unknown", "unknown", "unknown", "tilt", "tilt", "unknown", "unknown", "button", "button", "button", "button"]
DEDICATED_AVAILABILITY = ["used", "used", "used", "optional", "optional", "unused", "unused", "unused", "used", "used", "used", "used", "unused", "unused", "unused", "unused", "used", "optional", "optional", "unused", "used", "used", "used", "used"]
DEDICATED_PARTS = ["180-5024-01", "180-5024-01", "180-5024-01", "", "", "", "", "", "180-5160-01", "180-5149-00", "180-5160-01", "180-5149-00", "", "", "", "", "", "", "", "", "", "", "", ""]
DEDICATED_LOCATIONS = ["Coin door", "Coin door", "Coin door", "Coin door (if used)", "Coin door (if used)", "", "", "", "Cabinet side, left single-stack flipper switch", "Left flipper assembly 500-6543-15-ND", "Cabinet side, right single-stack flipper switch", "Right flipper assembly 500-6543-05-ND", "", "", "", "", "Cabinet, plumb-bob tilt", "Coin door (if fitted)", "Ticket dispenser (if fitted)", "", "Coin door service-button bracket 535-6860-04", "Coin door service-button bracket 535-6860-04", "Coin door service-button bracket 535-6860-04", "Coin door service-button bracket 535-6860-04"]
# What the ROM's switch test printed while the public address was held: (name, LAST SW line, wire colours).
DEDICATED_ROM_TEXT: dict[int, tuple[str, str, str]] = {
	65: ("LEFT COIN SLOT", "D-1", "PNK-BRN / BLK"), 66: ("CENTER COIN SLOT", "D-2", "PNK-RED / BLK"), 67: ("RIGHT COIN SLOT", "D-3", "PNK-ORG / BLK"), 68: ("FOURTH COIN SLOT", "D-4", "PNK-YEL / BLK"),
	69: ("FIFTH COIN SLOT", "D-5", "PNK-GRN / BLK"), 70: ("DEDICATED SW. #6", "D-6", "PNK-BLU / BLK"), 71: ("DEDICATED SW. #7", "D-7", "PNK-VIO / BLK"), 72: ("DEDICATED SW. #8", "D-8", "PNK-GRY / BLK"),
	81: ("RIGHT FLIPPER E.O.S.", "D-12", "GRY / BLK"), 82: ("RIGHT FLIPPER E.O.S.", "D-12", "GRY / BLK"), 83: ("LEFT FLIPPER E.O.S.", "D-10", "GRY-BLU / BLK"), 84: ("LEFT FLIPPER E.O.S.", "D-10", "GRY-BLU / BLK"),
	85: ("DEDICATED SW. #16", "D-16", "GRY-BLK / BLK"), 86: ("DEDICATED SW. #16", "D-16", "GRY-BLK / BLK"), 87: ("DEDICATED SW. #14", "D-14", "GRY-BLU / BLK"), 88: ("DEDICATED SW. #14", "D-14", "GRY-BLU / BLK"),
	-7: ("TILT PENDULUM", "D-17", "LGN-BRN / BLK"), -6: ("SLAM TILT", "D-18", "LGN-YEL / BLK"), -5: ("TICKET NOTCH", "D-19", "LGN-ORG / BLK"), -4: ("DEDICATED SW. #20", "D-20", "LGN-YEL / BLK"),
}
DEDICATED_ROLES = {65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth", 84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos", -7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "service.ticket", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter"}
# Button bits whose test frame shows the EOS of their pair (samswitch_r copies the button into the EOS bit).
BUTTON_SHOWS_EOS = {84: 83, 82: 81, 88: 87, 86: 85}


def dedicated_id(number: int) -> str:
	return f"switch.d{number}-{slug(DEDICATED_LABELS[number - 1])}"


def dedicated_switch(number: int) -> dict[str, Any]:
	index = number - 1
	device = DEDICATED_DEVICES[index]
	availability = DEDICATED_AVAILABILITY[index]
	notes: list[str] = []
	rom = DEDICATED_ROM_TEXT.get(device)
	if rom and device in BUTTON_SHOWS_EOS:
		notes.append(f"Holding public {device} makes the ROM's switch test show \"{rom[0]}\" / LAST SW. {rom[1]} and mark both bits of the pair: pinned PinMAME's samswitch_r copies this button bit into the EOS bit of public {BUTTON_SHOWS_EOS[device]} as the CPU reads the dedicated word, so the test never names the button itself.")
	elif rom:
		notes.append(f"The ROM's switch test prints \"{rom[0]}\" / LAST SW. {rom[1]} with the wire colours {rom[2]}.")
	if number in {9, 11}:
		notes.append("The parts book lists two single-stack flipper switch assemblies 500-6889-01 (stack 180-5160-01) and no double-stack assembly (500-6890-01, quantity 0).")
	if number in {10, 12}:
		notes.append(f"The parts book's {'left' if number == 10 else 'right'} flipper page prints \"DEDICATED SW. D-{number}\" beside item 3, the \"Power (EOS / End-of-Stroke) Switch\" 180-5149-00. normally_closed is true: this Stern part is the flipper's normally closed power contact, which the crank opens at the end of the stroke; NBA's partial manual has no flipper circuit page that draws it. PinMAME synthesizes this public bit from the flipper coil state and from the button bit, so it does not report the physical contact's rest state.")
	if number in {13, 14, 15, 16}:
		notes.append("No upper flipper is fitted: the parts book lists no double-stack flipper switch (quantity 0) and no upper flipper assembly, and the ROM prints only a generic DEDICATED SW. name for this bit.")
	if number in {6, 7, 8, 20}:
		notes.append("Generic name only; the parts book lists no hardware for it.")
	if number in {1, 2, 3}:
		notes.append("The parts book lists a two-chute US coin door (501-5018-172, \"2-Cht $V Up-Stk.\") with two coin switches 180-5024-01; which two of D-1 to D-3 they occupy is not printed.")
	if number in {4, 5}:
		notes.append("Not fitted to the US coin door the parts book lists; used only by doors with more coin slots.")
	if number == 17:
		notes.append("Plumb-bob tilt: hanger wire, weight and contact wire form (parts book item 25); the contact closes when the bob touches the wire.")
	if number == 18:
		notes.append("The parts book lists no slam-tilt switch. normally_closed is false: the retained gameplay probes hold public -6 at 0 throughout a game without a slam tilt, so the ROM reads an open contact as rest.")
	if number == 19:
		notes.append("The parts book lists no ticket dispenser.")
	if number >= 21:
		notes.append("One of the four push-button service switches on the coin door's bracket 535-6860-04 (one black 180-5192-00, two red 180-5192-02 and one 180-5192-04); the parts book does not say which button is which function. PinMAME publishes them as public -3 to 0 (Back, Minus, Plus, Select).")
	sources = [MANUAL, CORE]
	if rom:
		sources.append(RT_SWITCH)
	if device in {84, 82, -6}:
		sources.append(RT_PLAY)
	physical: dict[str, Any] = {"switch_type": DEDICATED_TYPES[index]}
	if DEDICATED_PARTS[index]:
		physical["part_number"] = DEDICATED_PARTS[index]
	if DEDICATED_LOCATIONS[index]:
		physical["location"] = DEDICATED_LOCATIONS[index]
	physical["notes"] = " ".join(notes)
	result: dict[str, Any] = {
		"id": dedicated_id(number), "label": DEDICATED_LABELS[index], "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{number}"),
		"normally_closed": number in {10, 12}, "pulse": number in {1, 2, 3, 4, 5, 19}, "availability": availability, "physical": physical,
		"provenance": provenance(*sources),
	}
	if rom and device not in BUTTON_SHOWS_EOS:
		result["wiring"] = {"board": "CPU/Sound board dedicated-switch input", "drive_wire": rom[2].split(" / ")[0], "return_wire": rom[2].split(" / ")[1]}
	if device in DEDICATED_ROLES and availability in {"used", "optional"}:
		result["roles"] = [DEDICATED_ROLES[device]]
	return result


def dip_switch(number: int) -> dict[str, Any]:
	note = "Position of the eight-position CPU/Sound board DIP switch that pinned PinMAME exposes for every S.A.M. game. NBA's partial parts book prints no DIP table, so the settings each position selects are not documented here."
	return {
		"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number),
		"availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board", "notes": note},
		"provenance": provenance(CORE),
	}


def inputs() -> list[dict[str, Any]]:
	items = [matrix_switch(number) for number in range(1, 65)]
	items.extend(dedicated_switch(number) for number in range(1, 25))
	items.extend(dip_switch(number) for number in range(1, 9))
	return items


# --------------------------------------------------------------------------------------------
# Coils, motors and flash lamps
# --------------------------------------------------------------------------------------------

# address: (label, kind, availability, ROM name, power wire, control wire, part number, quantity, note)
COILS: dict[int, tuple[str, str, str, str, str, str, str, int, str]] = {
	1: ("Trough up-kicker", "coil", "used", "TROUGH UP-KICKER", "YEL-VIO", "BRN-BLK", "26-1200 (090-5044-ND)", 1, "The parts book's trough page prints the coil as Q1. It lifts the right-most trough ball past the jam opto 22 into the shooter lane."),
	2: ("Auto launch", "coil", "used", "AUTO LAUNCH", "YEL-VIO", "BRN-RED", "24-940 (090-5036-ND)", 1, "Autoplunger coil (parts book Q2) that fires the ball resting on shooter-lane switch 23."),
	3: ("Basket magnet", "magnet", "used", "BASKET MAGNET", "YEL-VIO", "BRN-ORG", "511-5221-00", 1, "The magnet and connector assembly of the Magna-hoop assembly 500-7162-00 behind the basket's backboard plastic."),
	4: ("Left eject", "coil", "used", "LEFT EJECT", "YEL-VIO", "BRN-YEL", "", 1, "Kicks the ball out of the left eject (switch 35). The parts book carries a 40-degree long-throw kicker 500-7157-01 (27-1400 coil) and a 30-degree eject 500-6511-01-ND (24-940 coil) without saying which eject each one is."),
	5: ("Ramp diverter", "coil", "used", "RAMP DIVERTER", "YEL-VIO", "BRN-GRN", "", 1, "The parts book lists one diverter assembly (515-6596-00-A9) on the left plastic ramp; whether it is this diverter or the basket diverter Q12 is not printed."),
	6: ("Spinning disk motor", "motor", "used", "SPINNING DISK MOTOR", "BRN", "BRN-BLU", "511-5190-00", 1, "Motor of the spinning disk assembly 500-7144-01 (disk/hub weldment 515-7714-00 under an adhesive art pad) in the centre of the playfield. The ROM's coil test energizes public 22 (the motor relay) together with it."),
	7: ("MVP 3-bank drop target reset", "coil", "used", "3-BANK DROP TARGET", "YEL-VIO", "BRN-VIO", "24-940 (090-5036-ND)", 1, "Reset coil of the 3-bank drop target assembly 500-7029-03-00 (parts book Q7)."),
	8: ("Shaker motor (optional)", "motor", "optional", "SHAKER MOTOR (OPTIONAL)", "RED-WHT", "BRN-GRY", "", 1, "The ROM names it optional and the parts book lists no shaker motor. The retained probes show the ROM driving it on every pop-bumper hit and on the MVP bank reset, so a fitted shaker runs then."),
	9: ("Top pop bumper", "coil", "used", "TOP POP BUMPER", "YEL-VIO", "BLU-BRN", "26-1200 (090-5044-ND)", 1, "One of the bumper coils the parts book prints as Q9-Q11. The retained probe shows the ROM firing it when switch 30 closes."),
	10: ("Left pop bumper", "coil", "used", "LEFT POP BUMPER", "YEL-VIO", "BLU-RED", "26-1200 (090-5044-ND)", 1, "One of the bumper coils Q9-Q11. The retained probe shows the ROM firing it when switch 31 closes; the bumper's side is disputed (conflict.pop-bumper-sides)."),
	11: ("Right pop bumper", "coil", "used", "RIGHT POP BUMPER", "YEL-VIO", "BLU-ORG", "26-1200 (090-5044-ND)", 1, "One of the bumper coils Q9-Q11. The retained probe shows the ROM firing it when switch 32 closes; the bumper's side is disputed (conflict.pop-bumper-sides)."),
	12: ("Basket diverter", "coil", "used", "BASKET DIVERTER", "YEL-VIO", "BLU-YEL", "", 1, "The retained table models it as a ramp flap that swings into the ball's path while energized."),
	13: ("Flash: backboard", "flasher", "used", "FLASH: BACKBOARD (X2)", "ORG", "BLU-GRN", "", 2, "The ROM names two lamps. Its two and the basketball flash Q19's three add up to the five #89 socket and bulb assemblies 519-5101-00-HF the parts book lists on the back panel 500-7160-00, which also carries the basketball; the parts book does not tie those sockets to addresses."),
	14: ("Flash: left ramp", "flasher", "used", "FLASH: LEFT RAMP (X2)", "ORG", "BLU-BLK", "", 2, "The ROM names two lamps."),
	15: ("Left flipper", "coil", "used", "LEFT FLIPPER", "GRY-YEL", "ORG-GRY", "23-1500 (090-5062-ND)", 1, "Left flipper assembly 500-6543-15-ND; the parts book prints the coil as \"Left, Q15\"."),
	16: ("Right flipper", "coil", "used", "RIGHT FLIPPER", "BLU-YEL", "ORG-VIO", "23-900 (090-5020-30)", 1, "Right flipper assembly 500-6543-05-ND; the parts book prints the coil as \"Right, Q16\"."),
	17: ("Left slingshot", "coil", "used", "LEFT SLINGSHOT", "BRN", "VIO-BRN", "23-800 (090-5001-ND)", 1, "Slingshot assembly 500-5849-00-ND; the parts book prints \"Left, 17\". The retained probe shows the ROM firing it when switch 26 closes."),
	18: ("Right slingshot", "coil", "used", "RIGHT SLINGSHOT", "BRN", "VIO-RED", "23-800 (090-5001-ND)", 1, "The parts book prints \"Right,18\". The retained probe shows the ROM firing it when switch 27 closes."),
	19: ("Flash: basketball", "flasher", "used", "FLASH: BASKETBALL (X3)", "ORG", "VIO-ORG", "", 3, "The ROM names three lamps; see Q13 for the back panel's five #89 sockets and its basketball 545-5734-01-A9."),
	20: ("Right eject", "coil", "used", "RIGHT EJECT", "BRN", "VIO-WHT", "", 1, "Kicks the ball out of the right eject (switch 9); see Q4 for the eject hardware pages."),
	21: ("Orbit up/down post", "coil", "used", "ORBIT UP/DOWN POST", "BRN", "VIO-GRN", "", 1, "The retained table raises a post across the orbit while it is energized and drops it when released. The parts book's only up-post assembly is \"UP POST ASSEMBLY - LIFT RAMP - NBA\" 500-7161-00 (26-1200 coil), which it does not tie to an address."),
	22: ("Spinning disk motor relay", "relay", "used", "SPINNING DISK MOTOR RELAY", "BRN", "VIO-BLU", "", 1, "The ROM's coil test energizes it on its own and together with the disk motor Q6. What the relay switches is not documented."),
	23: ("Flash: left side", "flasher", "used", "FLASH: LEFT SIDE", "ORG", "VIO-BLK", "", 1, ""),
	24: ("Optional coil", "coil", "optional", "OPTIONAL COIL", "RED", "VIO-GRY", "", 1, "The ROM names it OPTIONAL COIL and its coil test changes no public solenoid when it is selected. In the retained probes the ROM pulses public 24 for about 130 ms once per inserted coin, as a coin meter or knocker would be driven; the parts book lists an optional meter (G-0053-013-102) that was not included with the machine, and the retained table plays a knocker sound on it."),
	25: ("Flash: left ramp arrow", "flasher", "used", "FLASH: LEFT RAMP ARROW", "ORG", "BLK-BRN", "", 1, ""),
	26: ("Flash: left eject arrow", "flasher", "used", "FLASH: LEFT EJECT ARROW", "ORG", "BLK-RED", "", 1, ""),
	27: ("Flash: right eject arrow", "flasher", "used", "FLASH: RIGHT EJECT ARROW", "ORG", "BLK-ORG", "", 1, ""),
	28: ("Flash: right ramp arrow", "flasher", "used", "FLASH: RIGHT RAMP ARROW", "ORG", "BLK-YEL", "", 1, ""),
	29: ("Flash: right side", "flasher", "used", "FLASH: RIGHT SIDE", "ORG", "BLK-GRN", "", 1, ""),
	30: ("Flash: captive ball", "flasher", "used", "FLASH: CAPTIVE BALL", "ORG", "BLK-BLU", "", 1, ""),
	31: ("Flash: pop bumpers", "flasher", "used", "FLASH: POP BUMPER (X3)", "ORG", "BLK-VIO", "", 3, "The ROM names three lamps. The retained probe shows the ROM flashing it on every pop-bumper hit."),
	32: ("Flash: slingshots", "flasher", "used", "FLASH: SLINGSHOT (X2)", "ORG", "BLK-GRY", "", 2, "The ROM names two lamps, one per slingshot. The retained probe shows the ROM flashing it on every slingshot hit."),
}
SCRIPT_COILS = {1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}
PINMAME_BULB_TYPED = {13, 14, 19, 23, 25, 26, 27, 28, 29, 30, 31, 32}


def output_id(address: int) -> str:
	return f"device.{address}-{slug(COILS[address][0])}"


def make_output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, Any] | None = None, wiring: dict[str, Any] | None = None, stable_id: str | None = None, status: str = "validated") -> dict[str, Any]:
	namespace = {"pinmame.output.lamp": "pinmame.lamp", "pinmame.output.gi": "pinmame.gi"}.get(group, "pinmame.solenoid")
	result: dict[str, Any] = {"id": stable_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance(*sources, status=status)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


GAME_ON_NOTE = (
	"PinMAME's synthetic S.A.M. game-on state, not a driver-board transistor. sam.c's VBLANK handler reads game RAM at samlocals.fastflipaddr (0x010609be, set for nba_802 only) and publishes public solenoid 33 while that value is 1; nba_500, nba_600, nba_700 and nba_801 have no fast-flip address, so on them it stays 0. "
	"A retained diagnostic run of the gameplay probe on nba_802 read that RAM word and PinmameGetSolenoid(33) after every output poll: both turn on about 40 ms after Start and stay on through play (fast-flip diagnostic excerpt). The pinned LibPinMAME build never reports public 33 through its OnSolenoidUpdated callback, though, so the harness traces record no event for it (the same build reports none for Family Guy, whose older-build trace does); a consumer that only listens for solenoid callbacks never receives it, and one that polls the solenoid state does. "
	"The retained table runs core sam.vbs fast flips (InitVpmFFlipsSAM), which bind SolCallback(33) to switch flipper control between the ROM's Q15/Q16 and direct button flips."
)


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, kind, availability, rom_name, power, control, part, quantity, note) in COILS.items():
		physical: dict[str, Any] = {"quantity": quantity}
		if part:
			physical["part_number"] = part
		sentences = [f"The ROM's Single Coil Test shows \"{rom_name}\" with the wire colours {power} / {control}" + (" and its SELECT fires no public solenoid." if address == 24 else f" and fires public solenoid {address}" + (" and 22." if address == 6 else "."))]
		if note:
			sentences.append(note)
		if address in PINMAME_BULB_TYPED:
			sentences.append("Pinned PinMAME types this output as a #89 bulb for every nba_ driver, so the values it publishes are the integrated brightness of a flash lamp.")
		physical["notes"] = " ".join(sentences)
		sources = ((MANUAL,) if part or "parts book" in note else ()) + (RT_COIL, CORE)
		if address in SCRIPT_COILS:
			sources += (SCRIPT,)
		if address in {8, 9, 10, 11, 17, 18, 31, 32}:
			sources += (RT_POPS,)
		if address in {4, 7, 20, 24}:
			sources += (RT_PLAY,)
		wiring = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "power_wire": power, "control_wire": control}
		status = "conflicted" if address in BUMPER_SIDE_COILS else "validated"
		items.append(make_output(address, label, kind, availability, sources, manual_address=f"Q{address}", physical=physical, wiring=wiring, stable_id=output_id(address), status=status))
	items.append(make_output(33, "PinMAME S.A.M. game-on state", "virtual", "used", (CORE, RT_FASTFLIP, SCRIPT), physical={"notes": GAME_ON_NOTE}, stable_id="virtual.game-on"))
	for address in range(51, 67):
		items.append(make_output(address, f"Unused S.A.M. auxiliary compatibility address {address}", "virtual", "unused", (CORE,), physical={"notes": "Public custom-solenoid space of the S.A.M. platform. NBA is initialized with SAM_NO_AUX, so no auxiliary write path drives it and it stays 0."}, stable_id=f"virtual.aux-{address}"))
	return items


# --------------------------------------------------------------------------------------------
# Lamps
# --------------------------------------------------------------------------------------------

# The ROM's lamp test prints two wire colours per lamp: the first by position within each row of
# eight, the second by row.
LAMP_COLUMN_WIRE = ["VIO-BLK", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "GRY-BLK"]
LAMP_ROW_WIRE = ["BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY", "BLK-WHT", "RED"]

# lamp: (label, ROM lamp-test name)
LAMPS: dict[int, tuple[str, str]] = {
	1: ("Start button", "START BUTTON"), 2: ("Tournament start button", "TOURNAMENT START BUTTON"), 3: ("Shoot again", "SHOOT AGAIN"), 4: ("Left outlane", "LEFT OUTLANE"),
	5: ("Left return lane", "LEFT RETURN LANE"), 6: ("Right return lane", "RIGHT RETURN LANE"), 7: ("Right outlane", "RIGHT OUTLANE"), 9: ("Fire", "FIRE"),
	10: ("Fast break", "FAST BREAK"), 12: ("Rebound (12)", "REBOUND"), 13: ("All Star (13)", "ALL STAR"), 14: ("All (S)tar", "ALL (S)TAR"), 15: ("All S(T)ar", "ALL S(T)AR"), 16: ("All St(A)r", "ALL ST(A)R"),
	17: ("All Sta(R)", "ALL STA(R)"), 18: ("(A)ll Star", "(A)LL STAR"), 19: ("A(L)l Star", "A(L)L STAR"), 20: ("Al(L) Star", "AL(L) STAR"), 21: ("Left loop arrow", "L. LOOP ARROW"), 22: ("Captive ball arrow", "CAPTIVE BALL ARROW"),
	23: ("Left ramp arrow", "L. RAMP ARROW"), 24: ("Left ramp basketball", "L. RAMP BASKETBALL"), 25: ("Left eject basketball", "L. EJECT BASKETBALL"), 26: ("Left eject arrow", "L. EJECT ARROW"), 27: ("Right eject arrow", "R. EJECT ARROW"),
	28: ("Multiball", "MULTIBALL"), 30: ("Right ramp arrow", "R. RAMP ARROW"), 31: ("Right ramp basketball", "R. RAMP BASKETBALL"), 32: ("Right loop arrow", "R. LOOP ARROW"), 33: ("Rebound (33)", "REBOUND"),
	35: ("Triple double", "TRIPLE DOUBLE"), 36: ("NBA Finals", "NBA FINALS"), 37: ("Super Star", "SUPER STAR"), 39: ("All Star (39)", "ALL STAR"), 40: ("NB(A)", "NB(A)"), 41: ("3 Point Shootout", "3 POINT SHOOTOUT"),
	42: ("Slam Dunk", "SLAM DUNK"), 43: ("Skills Challenge", "SKILLS CHALLENGE"), 44: ("H-O-R-S-E", "H-O-R-S-E"), 45: ("Mystery", "MYSTERY"), 46: ("Shooting Stars", "SHOOTING STARS"), 47: ("(N)BA", "(N)BA"),
	48: ("N(B)A", "N(B)A"), 49: ("(F)ire", "(F)IRE"), 50: ("F(I)re", "F(I)RE"), 51: ("Fi(R)e", "FI(R)E"), 52: ("Fir(E)", "FIR(E)"), 54: ("Super Star arrow", "SUPER STAR ARROW"),
	57: ("(M)VP", "(M)VP"), 58: ("M(V)P", "M(V)P"), 59: ("MV(P)", "MV(P)"), 60: ("Top pop bumper", "TOP POP BUMPER"), 61: ("Left pop bumper", "LEFT POP BUMPER"), 62: ("Right pop bumper", "RIGHT POP BUMPER"),
	63: ("Special", "SPECIAL"), 64: ("Extra ball", "EXTRA BALL"),
}
LAMP_UNUSED = [n for n in range(1, 81) if n not in LAMPS]
BUMPER_LAMPS = {60: ("TOP", 30, 9), 61: ("LEFT", 31, 10), 62: ("RIGHT", 32, 11)}


def lamp_wires(address: int) -> tuple[str, str]:
	row, column = divmod(address - 1, 8)
	return LAMP_COLUMN_WIRE[column], LAMP_ROW_WIRE[row]


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 81):
		first, second = lamp_wires(address)
		wiring = {"board": "I/O Power Driver board lamp matrix", "drive_wire": first, "return_wire": second}
		if address in LAMPS:
			label, rom_name = LAMPS[address]
			physical: dict[str, Any] = {"quantity": 1}
			notes = [f"The ROM's Single Lamp Test prints \"{rom_name}\" with the wire colours {first} / {second}."]
			sources: tuple[str, ...] = (RT_LAMP, CORE)
			if address in {1, 2}:
				physical.update({"part_number": "165-5002-00", "location": "Cabinet front start button" if address == 1 else "Cabinet front tournament button"})
				notes.append("#555 clear wedge-base bulb inside the button assembly (parts book item 3S / 4T), with its lamp diode on a terminal strip under the button.")
				sources = (MANUAL,) + sources
			elif address in BUMPER_LAMPS:
				side, switch, coil = BUMPER_LAMPS[address]
				physical.update({"part_number": "112-5024-08", "location": "Pop bumper cap, above the playfield"})
				notes.append(f"White 6.3 V wedge-base LED module in the bumper's wedge socket 077-5206-00, with its diode on a playfield terminal strip (parts book bumper page, item 1 and its DOTS note). The retained probe shows the ROM lighting it when switch {switch} closes, together with coil Q{coil}.")
				if address != 60:
					notes.append(f"The parts book's bumper callout prints lamp {address} ({'RIGHT' if address == 61 else 'LEFT'}) instead of the ROM's {side} (conflict.pop-bumper-sides).")
				sources = (MANUAL,) + sources + (SCRIPT, RT_POPS)
			else:
				sources = sources + (SCRIPT,)
			physical["notes"] = " ".join(notes)
			status = "conflicted" if address in BUMPER_SIDE_LAMPS else "validated"
			items.append(make_output(address, label, "lamp", "used", sources, group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring=wiring, stable_id=f"lamp.{address}-{slug(label)}", status=status))
		else:
			label = f"Unused lamp {address}"
			physical = {"notes": f"The ROM's Single Lamp Test prints \"NOT USED\" for this address (wire colours {first} / {second}) and the retained table binds no light to it."}
			items.append(make_output(address, label, "lamp", "unused", (RT_LAMP, CORE), group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring=wiring, stable_id=f"lamp.{address}-{slug(label)}"))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	notes = (
		"PinMAME publishes one aggregate general-illumination channel (public GI 0) for every S.A.M. game; the retained boot-start run shows it on from power-up. "
		"NBA's partial parts book prints no G.I. circuit table: it lists seven clear socket and bulb assemblies 519-5000-00-HF on the back panel 500-7160-00 beside the five #89 flash lamps, and its bulb pages list #44, #555 and LED bulbs without quantities for this game."
	)
	return [make_output(0, "General illumination", "gi", "used", (MANUAL, CORE, RT_BOOT), group="pinmame.output.gi", manual_address="GI-0", physical={"location": "Playfield and back panel", "notes": notes}, stable_id="gi.master")]


def outputs() -> list[dict[str, Any]]:
	return solenoid_outputs() + lamp_outputs() + gi_outputs()
