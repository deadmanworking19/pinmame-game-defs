"""Device tables for the Stern Family Guy (2007) definition.

Every literal below was read from the retained manual excerpts under
``evidence/excerpts/stern.family-guy.2007/``, the ROM's own service tests (retained runs
summarised in ``evidence/runtime/sam/``), or the pinned PinMAME ``sam.c``. The builders turn the
tables into schema-shaped inputs, outputs and mechanisms; ``curate_family_guy.py`` owns the
source records and the artifact writes.
"""

from __future__ import annotations

import re
from typing import Any


MANUAL = "manual.stern-family-guy.2007-service"
CORE = "pinmame.core.8371478a7640"
CATALOG = "pinmame.catalog.8371478a7640"
SCRIPT = "vpx.script.family-guy-2020-embedded"
TABLE = "vpx.table.family-guy-2020"
ROM = "rom.stern-family-guy.fg-1200ag"
IPDB = "ipdb.family-guy.5219"
RT_SWITCH = "runtime.family-guy.fg-1200ag.switch-test-sweep"
RT_DEDICATED = "runtime.family-guy.fg-1200ag.dedicated-switch-sweep"
RT_COIL = "runtime.family-guy.fg-1200ag.coil-test-sweep"
RT_LAMP = "runtime.family-guy.fg-1200ag.lamp-test-sweep"
RT_BOOT = "runtime.family-guy.fg-1200ag.boot-start"
RT_EM_CLOSED = "runtime.family-guy.fg-1200ag.evil-monkey-probe-closed"
RT_EM_OPEN = "runtime.family-guy.fg-1200ag.evil-monkey-probe-open"
TICKET_SOURCES = (MANUAL,) + tuple(f"runtime.family-guy.{driver}.coil-test-sweep" for driver in ("fg_300ai", "fg_400a", "fg_800al", "fg_1100al"))


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

MATRIX_RETURN = [
	("IC-U22A", "WHT-BRN", "J6-P9"), ("IC-U22B", "WHT-RED", "J6-P8"), ("IC-U22C", "WHT-ORG", "J6-P7"), ("IC-U22D", "WHT-YEL", "J6-P6"),
	("IC-U16A", "WHT-GRN", "J6-P5"), ("IC-U16B", "WHT-BLU", "J6-P3"), ("IC-U16C", "WHT-VIO", "J6-P2"), ("IC-U16D", "WHT-GRY", "J6-P1"),
	("IC-U36A", "TAN-BLK", "J12-P9"), ("IC-U36B", "TAN-RED", "J12-P8"), ("IC-U36C", "TAN-ORG", "J12-P7"), ("IC-U36D", "TAN-YEL", "J12-P6"),
	("IC-U40A", "TAN-GRN", "J12-P4"), ("IC-U40B", "TAN-BLU", "J12-P3"), ("IC-U40C", "TAN-VIO", "J12-P2"), ("IC-U40D", "TAN-WHT", "J12-P1"),
]
MATRIX_DRIVE = [("Q1", "GRN-BRN", "J1-P1"), ("Q2", "GRN-RED", "J1-P3"), ("Q3", "GRN-ORG", "J1-P4"), ("Q4", "GRN-YEL", "J1-P5")]

# number: (label, pulse, roles, switch_type, part number, location, ROM switch-test name, note)
# pulse follows the retained script's controller-facing behaviour (vpmTimer.PulseSw = True,
# Controller.Switch held = False); a switch the script does not bind takes the class default
# and says so in its note.
SWITCHES: dict[int, tuple[str, bool, tuple[str, ...], str, str, str, str, str]] = {
	1: ("Ball saver post up", False, (), "leaf", "180-5010-04", "Up/Down death post assembly 500-7022-00, below playfield", "BALL SAVER UP", "Switch of the Up/Down death post assembly (item 10 of the assembly, two blade switches with 1-1/4 in. actuators). The retained script asserts it when it raises the post and clears it when it lowers it."),
	2: ("Ball saver post down", False, (), "leaf", "180-5010-04", "Up/Down death post assembly 500-7022-00, below playfield", "BALL SAVER DOWN", "Second blade switch of the Up/Down death post assembly. The retained script asserts it when it lowers the post."),
	3: ("Left orbit stand-up (Chris target)", True, (), "leaf", "515-5162-08", "Upper left, below playfield", "LEFT ORBIT S/U", "The instruction card calls this the Chris target (upper left): hitting it lowers the Evil Monkey target. Stack-switch stand-up target assembly 515-5162-08 (180-5133-00 stack switch with a 1 in. square white target)."),
	4: ("Right 2-bank bottom stand-up", True, (), "leaf", "515-5162-08", "Right side, below playfield", "R. 2-BANK BOTTOM", ""),
	5: ("Right 2-bank top stand-up", True, (), "leaf", "515-5162-08", "Right side, below playfield", "R. 2-BANK TOP", ""),
	6: ("Left Newton ball rollover", False, (), "leaf", "500-6227-01", "Left Newton captive-ball rollover, below playfield", "LT NEWTON ROLLOVER", "Rollover switch, standard force, left-mount style. The instruction card says to hit the captive balls to spell P-I-N-B-A-L-L."),
	7: ("Right Newton ball rollover", False, (), "leaf", "500-6227-02", "Right Newton captive-ball rollover, below playfield", "RT NEWTON ROLLOVER", "Rollover switch, standard force, right-mount style."),
	8: ("Pirate stand-up target", True, (), "leaf", "515-5967-04", "Below playfield", "PIRATE TARGET", "Stack switch 180-5132-00 with a 1/2 in. narrow green target."),
	9: ("Death 1-bank drop target", False, ("position.down",), "opto", "520-5252-01", "1-bank drop target assembly 500-7029-01, below playfield", "1-BANK DROP TARGET", "Slotted OPTO interrupter PCB (520-5252-01) on the 1-bank drop-target assembly; hit it to raise the ball saver post (instruction card)."),
	10: ("Meg stand-up target", True, (), "leaf", "515-5162-08", "Left side, below playfield", "MEG TARGET", ""),
	13: ("TV eject (scoop)", False, ("ball.position",), "microswitch", "180-5183-00", "Scoop and vertical up-kicker assembly 500-7028-00", "TV EJECT", "Happ #95-1128-00 scoop switch; the diode is on a playfield terminal strip (DOTS)."),
	15: ("Tournament Start", False, ("cabinet.tournament-start",), "button", "180-5119-03", "Cabinet front molding", "TOURNAMENT START", "Optional tournament start button, lit by lamp 2."),
	16: ("Start button", False, ("cabinet.start",), "button", "180-5174-00", "Cabinet front, red round start button", "START BUTTON", "Microswitch of the start-button assembly 500-6388-02, lit by lamp 1."),
	18: ("Trough 4 (left)", False, ("ball.position",), "microswitch", "180-5119-02", "4-ball trough assembly 500-6318-14-ND, below playfield", "TROUGH #4 (L)", "Roller-actuator Lite-Force microswitch."),
	19: ("Trough 3", False, ("ball.position",), "microswitch", "180-5119-02", "4-ball trough assembly 500-6318-14-ND", "TROUGH #3", "Roller-actuator Lite-Force microswitch."),
	20: ("Trough 2", False, ("ball.position",), "microswitch", "180-5119-02", "4-ball trough assembly 500-6318-14-ND", "TROUGH #2", "Roller-actuator Lite-Force microswitch."),
	21: ("Trough 1 (right, up-kicker opto)", False, ("ball.position",), "opto", "515-0173-00 / 515-0174-00", "4-ball trough assembly 500-6318-14-ND, dual OPTO boards", "TROUGH #1 (R)", "Printed \"VUK OPTO\". Dual OPTO transmitter and receiver boards (TX 515-0173-00, RX 515-0174-00); the receiver output is a closed switch when the beam is blocked."),
	22: ("Trough jam (stack opto)", False, ("ball.position",), "opto", "515-0173-00 / 515-0174-00", "4-ball trough assembly 500-6318-14-ND, dual OPTO boards", "TROUGH JAM", "Printed \"STACK OPTO\"; the second beam of the same dual OPTO board pair. The retained script pulses it as a served ball crosses; a physical stack opto is sustained while a fifth ball stacks."),
	23: ("Shooter lane", False, ("ball.position",), "unknown", "180-5157-00", "Shooter lane switch assembly 500-6096-00", "SHOOTER LANE", "The manual's Ball Trough Test text says the trough up-kicker ejects a ball into the shooter lane, momentarily closing this switch, before the autoplunger fires it onto the playfield."),
	24: ("Left outlane", False, (), "leaf", "500-6227-02", "Below playfield", "LEFT OUTLANE", ""),
	25: ("Left return lane", False, (), "leaf", "500-6227-02", "Below playfield", "LEFT RETURN", ""),
	26: ("Left slingshot", True, (), "leaf", "180-5054-00", "Left slingshot assembly 500-5849-02-ND (two switches per assembly)", "LEFT SLING", "Dual stack (blade) switches; only one of the two carries a diode."),
	27: ("Right slingshot", True, (), "leaf", "180-5054-00", "Right slingshot assembly 500-5849-02-ND (two switches per assembly)", "RIGHT SLING", "Dual stack (blade) switches; only one of the two carries a diode."),
	28: ("Right return lane", False, (), "leaf", "500-6227-01", "Below playfield", "RIGHT RETURN", ""),
	29: ("Right outlane", False, (), "leaf", "500-6227-01", "Below playfield", "RIGHT OUTLANE", "The grid prints the part number as 500-6227--01 (double hyphen); the parts page lists 500-6227-01 for switches 6, 28 and 29."),
	30: ("Top pop bumper", True, (), "leaf", "180-5015-04", "Top pop bumper, below playfield", "TOP BUMPER", "Stack (blade) switch with spoon actuator in switch assembly 515-6459-09."),
	31: ("Right pop bumper", True, (), "leaf", "180-5015-04", "Right pop bumper, below playfield", "RIGHT BUMPER", "Stack (blade) switch with spoon actuator in switch assembly 515-6459-09."),
	32: ("Bottom pop bumper", True, (), "leaf", "180-5015-04", "Bottom pop bumper, below playfield", "BOTTOM BUMPER", "Stack (blade) switch with spoon actuator in switch assembly 515-6459-09."),
	33: ("Left ramp made", True, (), "unknown", "180-5087-00", "Left ramp exit gate, above and below playfield", "LEFT RAMP MADE", "Roll-under wire-gate switch (180-5087-00). The retained script pulses it from the left gate's hit event."),
	35: ("Evil Monkey", False, (), "microswitch", "180-5119-02", "Latch gate housing and trip coil assembly 500-6590-01-ND on the left ramp, above playfield", "EVIL MONKEY", "Roller-actuator Lite-Force microswitch in the latch-gate housing whose trip coil is Q19. In the retained harness probes the ROM fires Q19 repeatedly from game start while public 35 reads open and never fires it when 35 reads closed, so a closed switch 35 is the state Q19 is driving toward; what happens physically on the target when Q19 is energized is not documented. The retained script likewise asserts 35 from its Q19 callback and clears it on the ball's hit."),
	39: ("Right orbit spinner", True, (), "leaf", "180-5010-04", "Right orbit spinner assembly, above playfield", "RIGHT ORBIT SPINNER", "Switch with a 1-1/4 in. actuator blade."),
	40: ("Death return (inner lane)", False, (), "leaf", "500-6227-02", "Left inner lane, below playfield", "DEATH RETURN", "Rollover switch, right-mount style."),
	41: ("3-bank stand-up bottom", True, (), "leaf", "515-5162-08", "Below playfield", "3 BANK BOT", ""),
	42: ("3-bank stand-up middle", True, (), "leaf", "515-5162-08", "Below playfield", "3 BANK MID", ""),
	43: ("3-bank stand-up top", True, (), "leaf", "515-5162-08", "Below playfield", "3 BANK TOP", ""),
	44: ("F-A-R-T drop target F", False, ("position.down",), "opto", "520-5252-04", "4-bank drop target assembly 500-7029-04, below playfield", "(F)ART", "Slotted OPTO interrupter PCB 520-5252-04 (four H21A1 interrupters, one per target)."),
	45: ("F-A-R-T drop target A", False, ("position.down",), "opto", "520-5252-04", "4-bank drop target assembly 500-7029-04", "F(A)RT", "Slotted OPTO interrupter PCB 520-5252-04."),
	46: ("F-A-R-T drop target R", False, ("position.down",), "opto", "520-5252-04", "4-bank drop target assembly 500-7029-04", "FA(R)T", "Slotted OPTO interrupter PCB 520-5252-04."),
	47: ("F-A-R-T drop target T", False, ("position.down",), "opto", "520-5252-04", "4-bank drop target assembly 500-7029-04", "FAR(T)", "Slotted OPTO interrupter PCB 520-5252-04."),
	48: ("Sneak ramp", False, (), "microswitch", "180-5183-00", "Flat ramp (sneak lanes), below playfield", "SNEAK RAMP", "Happ #95-1128-00 switch on the flat ramp assembly."),
	49: ("Beer can (Brian)", True, (), "microswitch", "180-5189-00", "Beer can (Brian) assembly 500-7025-00", "BEER CAN", "Switch actuated by the spring-returned beer can; the retained script pulses it on the ball's hit."),
	50: ("Mini Meg target", True, (), "other", "511-5081-00", "Mini-playfield stand-up, below mini-playfield", "MINI MEG TARGET", "Mechanical stand-up switch with diode; the 2008-and-later production run replaced the earlier piezo sensor PCB with it (manual note, PDF page 115)."),
	51: ("Mini Peter target", True, (), "other", "511-5081-00", "Mini-playfield stand-up, below mini-playfield", "MINI PETER TARGET", "Mechanical stand-up switch with diode; replaced the earlier piezo sensor PCB in the 2008-and-later production run."),
	52: ("Mini right orbit", False, (), "opto", "500-6775-00", "Mini-playfield", "MINI RIGHT ORBIT", "Mini OPTO transceiver pair on playfield OPTO amplifier PCB 520-5239-01 (switches 52 and 53 share one amplifier board)."),
	53: ("Mini left orbit", False, (), "opto", "500-6775-00", "Mini-playfield", "MINI LEFT ORBIT", "Mini OPTO transceiver pair on playfield OPTO amplifier PCB 520-5239-01 (shared with switch 52)."),
	54: ("Mini ramp", False, (), "opto", "500-6775-00", "Mini-playfield plastic ramp", "MINI RAMP", "Mini OPTO transceiver pair on playfield OPTO amplifier PCB 520-5239-01 (switches 54 and 55 share one amplifier board)."),
	55: ("Mini trough (mini shooter)", False, ("ball.position",), "opto", "500-6775-01", "Mini-playfield shooter assembly 500-7023-00", "MINI TROUGH", "Mini OPTO transceiver pair (15 in. leads) on amplifier PCB 520-5239-01, shared with switch 54."),
	57: ("Right orbit", False, (), "leaf", "500-6227-02", "Below playfield", "RIGHT ORBIT", "Rollover switch, right-mount style."),
	64: ("Clam eject", False, ("ball.position",), "microswitch", "180-5209-00", "Eject / vertical up-kicker assembly 500-6846-01", "CLAM EJECT", "Simulated-roller actuator switch (Omron); the diode is on a playfield terminal strip (DOTS)."),
}
DOTS_SWITCHES = {13, 64}
ROM_UNUSED_SWITCH_NAMES = "the ROM's switch test prints its generic name \"SWITCH #{n}\""
# Matrix cells the manual prints as NOT USED (the ROM names each one generically).
UNUSED_SWITCHES = [n for n in range(1, 65) if n not in SWITCHES]
INITIAL_ACTIVE = {18, 19, 20, 21, 55}


def switch_id(number: int) -> str:
	label = SWITCHES[number][0] if number in SWITCHES else f"Unused matrix switch {number}"
	return f"switch.{number}-{slug(label)}"


def matrix_switch(number: int) -> dict[str, Any]:
	spec = SWITCHES.get(number)
	drive_index, return_index = divmod(number - 1, 16)
	drive_q, drive_wire, drive_pin = MATRIX_DRIVE[drive_index]
	return_ic, return_wire, return_pin = MATRIX_RETURN[return_index]
	label = spec[0] if spec else f"Unused matrix switch {number}"
	sources = [MANUAL, RT_SWITCH, CORE]
	if spec and number not in {15, 16}:
		sources.append(SCRIPT)
	if number == 35:
		sources.extend([RT_EM_CLOSED, RT_EM_OPEN])
	physical: dict[str, Any] = {"switch_type": spec[3] if spec else "unknown"}
	if spec:
		physical["part_number"] = spec[4]
		physical["location"] = spec[5]
		note = f"Manual name \"{_manual_name(number)}\"; the ROM's switch test prints \"{spec[6]}\" with the wire colours {drive_wire} / {return_wire}. {spec[7]}".strip()
		if number in DOTS_SWITCHES:
			note += " Printed D.O.T.S.: the switch's diode is on a playfield terminal strip (PDF page 126)."
		note += " normally_closed is false: the public bit is active-high (pinned PinMAME's samswitch_r complements the matrix word on its way to the CPU's active-low port, and the ROM treats a held public 1 as the active reading in its switch test)."
		physical["notes"] = note
	else:
		physical["notes"] = f"Printed NOT USED in the manual's grid; {ROM_UNUSED_SWITCH_NAMES.format(n=number)} and no hardware is listed."
	result: dict[str, Any] = {
		"id": switch_id(number), "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": False, "pulse": spec[1] if spec else False,
		"availability": "used" if spec else "unused", "physical": physical,
		"wiring": {"board": "CPU/Sound board switch matrix", "driver_transistor": drive_q, "drive_wire": drive_wire, "drive_connection": drive_pin, "return_wire": return_wire, "return_connection": return_pin, "return_component": return_ic},
		"provenance": provenance(*sources),
	}
	if spec and spec[2]:
		result["roles"] = list(spec[2])
	if number in INITIAL_ACTIVE:
		result["initial_active"] = True
	return result


_MANUAL_NAMES = {
	1: "BALL SAVER UP", 2: "BALL SAVER DOWN", 3: "LEFT ORBIT STAND-UP", 4: "RIGHT 2-BANK BOTTOM", 5: "RIGHT 2-BANK TOP", 6: "LEFT NEWTON ROLLOVER", 7: "RIGHT NEWTON ROLLOVER",
	8: "PIRATE [STAND-UP] TARGET", 9: "1-BANK DROP TARGET", 10: "MEG [STAND-UP] TARGET", 13: "TV EJECT", 15: "TOURNAMENT START", 16: "START BUTTON",
	18: "(4-BALL) TROUGH #4 (L)", 19: "(4-BALL) TROUGH #3", 20: "(4-BALL) TROUGH #2", 21: "(VUK OPTO) TROUGH #1 (R)", 22: "(STACK OPTO) TROUGH JAM", 23: "SHOOTER LANE",
	24: "LEFT OUTLANE", 25: "LEFT RETURN [LANE]", 26: "LEFT SLING", 27: "RIGHT SLING", 28: "RIGHT RETURN [LANE]", 29: "RIGHT OUTLANE", 30: "TOP BUMPER", 31: "RIGHT BUMPER", 32: "BOTTOM BUMPER",
	33: "LEFT RAMP MADE", 35: "EVIL MONKEY", 39: "RIGHT ORBIT SPINNER", 40: "DEATH RETURN [INNER LT.]", 41: "3 BANK [STAND-UP] BOTTOM", 42: "3 BANK [STAND-UP] MIDDLE", 43: "3 BANK [STAND-UP] TOP",
	44: "( F ) ART [4-BANK DROP TGT.]", 45: "F ( A ) RT [4-BANK DROP TGT.]", 46: "FA ( R ) T [4-BANK DROP TGT.]", 47: "FAR ( T ) [4-BANK DROP TGT.]", 48: "SNEAK RAMP", 49: "BEER CAN ( BRIAN )",
	50: "MINI MEG TARGET [STAND-UP]", 51: "MINI PETER TARGET [STAND-UP]", 52: "MINI RIGHT ORBIT", 53: "MINI LEFT ORBIT", 54: "MINI RAMP", 55: "MINI TROUGH", 57: "RIGHT ORBIT", 64: "CLAM EJECT",
}


def _manual_name(number: int) -> str:
	return _MANUAL_NAMES[number]


# --------------------------------------------------------------------------------------------
# Dedicated switches and DIP switch
# --------------------------------------------------------------------------------------------

DEDICATED_DEVICES = [65, 66, 67, 68, 69, 70, 71, 72, 84, 83, 82, 81, 88, 87, 86, 85, -7, -6, -5, -4, -3, -2, -1, 0]
DEDICATED_LABELS = [
	"Left coin slot", "Center coin slot / bill validator", "Right coin slot", "Fourth coin slot", "Fifth coin slot (if used)", "Unused dedicated switch D6", "Unused dedicated switch D7", "Unused dedicated switch D8",
	"Left flipper button", "Left flipper end-of-stroke", "Right flipper button", "Right flipper end-of-stroke", "Upper left flipper button", "Unused dedicated switch D14", "Unused upper right flipper button D15", "Unused dedicated switch D16",
	"Pendulum tilt", "Slam tilt", "Ticket notch", "Unused dedicated switch D20", "Coin-door Back button", "Coin-door Minus button", "Coin-door Plus button", "Coin-door Select button",
]
DEDICATED_TYPES = ["button", "button", "button", "button", "button", "unknown", "unknown", "unknown", "button", "leaf", "button", "leaf", "button", "unknown", "unknown", "unknown", "tilt", "tilt", "microswitch", "unknown", "button", "button", "button", "button"]
DEDICATED_AVAILABILITY = ["used", "used", "used", "optional", "optional", "unused", "unused", "unused", "used", "used", "used", "used", "used", "unused", "unused", "unused", "used", "optional", "optional", "unused", "used", "used", "used", "used"]
DEDICATED_PARTS = ["180-5204-00", "180-5204-00", "180-5204-00", "180-5204-00", "", "", "", "", "180-5164-01", "180-5149-00", "180-5160-01", "180-5149-00", "180-5164-01", "", "180-5164-01", "", "", "502-5032-00", "180-5119-02", "", "180-5192-04", "180-5192-02", "180-5192-02", "180-5192-00"]
DEDICATED_LOCATIONS = ["Coin door", "Coin door", "Coin door", "Coin door", "Coin door (if used)", "", "", "", "Cabinet side, inside the left double-stack flipper switch", "Left flipper assembly", "Cabinet side, inside the right double-stack flipper switch", "Right flipper assembly", "Cabinet side, inside the upper-left double-stack flipper switch", "", "", "", "Cabinet, plumb-bob tilt", "Coin door (optional kit)", "Below playfield (if used)", "", "Coin door", "Coin door", "Coin door", "Coin door"]
DEDICATED_ROM_NAMES = {1: "LEFT COIN SLOT", 2: "CENTER COIN SLOT", 3: "RIGHT COIN SLOT", 4: "FOURTH COIN SLOT", 5: "FIFTH COIN SLOT", 6: "DEDICATED SW. #6", 7: "L. POST SAVE", 8: "R. POST SAVE", 10: "LEFT FLIPPER E.O.S.", 12: "RIGHT FLIPPER E.O.S.", 14: "U.L. FLIPPER E.O.S.", 16: "U.R. FLIPPER E.O.S.", 17: "TILT PENDULUM", 18: "SLAM TILT", 19: "TICKET NOTCH", 20: "DEDICATED SW. #20"}
DEDICATED_ROLES = {65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth", 84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos", 88: "flipper.upper.left.button", -7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "service.ticket", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter"}
DEDICATED_WIRES = [
	("IC-U2", "PNK-BRN", "J2-P2"), ("IC-U2", "PNK-RED", "J2-P3"), ("IC-U2", "PNK-ORG", "J2-P4"), ("IC-U2", "PNK-YEL", "J2-P6"), ("IC-U2", "PNK-GRN", "J2-P7"), ("IC-U2", "PNK-BLU", "J2-P8"), ("IC-U2", "PNK-VIO", "J2-P9"), ("IC-U2", "PNK-GRY", "J2-P10"),
	("IC-U4", "GRY-BRN", "J3-P1"), ("IC-U4", "GRY-RED", "J3-P2"), ("IC-U4", "GRY-ORG", "J3-P4"), ("IC-U4", "GRY-YEL", "J3-P5"), ("IC-U4", "GRY-GRN", "J3-P6"), ("IC-U4", "GRY-BLU", "J3-P7"), ("IC-U4", "GRY-VIO", "J3-P8"), ("IC-U4", "GRY-BLK", "J3-P9"),
	("IC-41", "LGN-BRN", "J13-P1"), ("IC-41", "LGN-RED", "J13-P3"), ("IC-41", "LGN-ORG", "J13-P4"), ("IC-41", "LGN-YEL", "J13-P5"), ("IC-41", "LGN-BLK", "J13-P6"), ("IC-41", "LGN-BLU", "J13-P7"), ("IC-41", "LGN-VIO", "J13-P8"), ("IC-41", "LGN-GRY", "J13-P9"),
]
DEDICATED_GROUNDS = [("BLK", "J2-P1/11 and J3-P10")] * 8 + [("BLK", "J3-P10")] * 8 + [("BLK", "J13-P10")] * 8


def dedicated_id(number: int) -> str:
	return f"switch.d{number}-{slug(DEDICATED_LABELS[number - 1])}"


def dedicated_switch(number: int) -> dict[str, Any]:
	index = number - 1
	device = DEDICATED_DEVICES[index]
	availability = DEDICATED_AVAILABILITY[index]
	ic, wire, pin = DEDICATED_WIRES[index]
	notes = [f"Manual name for D-{number}: see the dedicated-switch table of the switch-matrix excerpt."]
	if availability == "unused":
		notes.append("Printed NOT USED in the manual.")
	rom_name = DEDICATED_ROM_NAMES.get(number)
	if rom_name:
		notes.append(f"The ROM's switch test prints \"{rom_name}\" for public {device} with the wire colours {wire} / BLK.")
	sources = [MANUAL, CORE]
	if number in DEDICATED_ROM_NAMES:
		sources.append(RT_DEDICATED)
	normally_closed = number in {10, 12}
	if number in {10, 12}:
		notes.append("Normally closed: the manual's flipper circuit page draws it N.C. and states the EOS switch opens about 1/16 in. when the flipper is energized. PinMAME synthesizes this public bit from the flipper coil's state, so it rests at 0 in the emulator whatever the contact does; never infer the physical rest state from the public level.")
	if number in {9, 11, 13}:
		notes.append("Drawn normally open on the manual's flipper circuit page; the cabinet buttons are double-stacked, half-way pressing operates the lower flippers and full pressing operates the lower and upper flippers.")
	if number == 13:
		notes.append("The upper-left flipper (coil Q14) carries no end-of-stroke switch: its parts list prints a plastic spacer where the lower assemblies carry the EOS switch.")
	if number == 15:
		notes.append("Printed \"NOT USED\"; the same row prints part 180-5164-01 greyed out. The ROM's switch test names public 86 as D-16 \"U.R. FLIPPER E.O.S.\" after it is held, a generic S.A.M. name (samswitch_r copies the button bit D-15 into the EOS bit); this machine fits no upper-right flipper (IPDB lists five flippers: two lower, one upper left, two mini).")
	if number in {14, 16}:
		notes.append("Printed NOT USED. The ROM's switch test names the address as an upper-flipper EOS (a generic S.A.M. firmware name; samswitch_r copies the flipper button bit into the EOS bit of an upper pair, which the core does not otherwise drive); no such switch is fitted.")
	if number in {7, 8}:
		notes.append("Printed NOT USED in the manual; the ROM's generic S.A.M. firmware names these addresses \"L. POST SAVE\" and \"R. POST SAVE\". This machine's ball saver post is driven by matrix switches 1 and 2, so no hardware is listed here.")
	if number == 18:
		notes.append("Normally open: the coin-door wiring page draws the optional slam-tilt switch as an open contact and the glossary defines a slam tilt as a switch which closes when the game is slammed.")
	if number == 17:
		notes.append("Plumb-bob tilt: the hanger-wire bracket (535-5221-00) and contact wire form (535-7563-01) in the cabinet; the contact closes when the bob touches the wire.")
	if number == 5:
		notes.append("Fifth coin slot, printed \"IF USED\".")
	if number in {1, 2, 3}:
		notes.append("Coin-door switch.")
	physical: dict[str, Any] = {"switch_type": DEDICATED_TYPES[index]}
	if DEDICATED_PARTS[index]:
		physical["part_number"] = DEDICATED_PARTS[index]
	if DEDICATED_LOCATIONS[index]:
		physical["location"] = DEDICATED_LOCATIONS[index]
	physical["notes"] = " ".join(notes[1:]) if len(notes) > 1 else "Printed NOT USED in the manual."
	result: dict[str, Any] = {
		"id": dedicated_id(number), "label": DEDICATED_LABELS[index], "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{number}"),
		"normally_closed": normally_closed, "pulse": number in {1, 2, 3, 4, 5, 19}, "availability": availability, "physical": physical,
		"wiring": {"board": "CPU/Sound board dedicated-switch input", "drive_wire": wire, "drive_connection": pin, "return_wire": DEDICATED_GROUNDS[index][0], "return_connection": DEDICATED_GROUNDS[index][1], "return_component": ic},
		"provenance": provenance(*sources),
	}
	if device in DEDICATED_ROLES and availability in {"used", "optional"}:
		result["roles"] = [DEDICATED_ROLES[device]]
	return result


def dip_switch(number: int) -> dict[str, Any]:
	note = "Position of the eight-position CPU/Sound board DIP switch SW1 (located between connectors J3 and J13). Positions 1-7 select the country and pricing option (pages 5 and 27 of the manual); position 8 ON with 1-7 OFF reboots from the boot EPROM to update game code."
	return {
		"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"),
		"availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board, between connectors J3 and J13", "notes": note},
		"provenance": provenance(MANUAL, CORE),
	}


def inputs() -> list[dict[str, Any]]:
	items = [matrix_switch(number) for number in range(1, 65)]
	items.extend(dedicated_switch(number) for number in range(1, 25))
	items.extend(dip_switch(number) for number in range(1, 9))
	return items


# --------------------------------------------------------------------------------------------
# Coils and flash lamps
# --------------------------------------------------------------------------------------------

CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLK", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-WHT", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J9-P1", "J9-P2", "J9-P4", "J9-P5", "J9-P6", "J9-P7", "J9-P8", "J9-P9", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]

# address: (label, kind, availability, part number or bulb, note)
COILS: dict[int, tuple[str, str, str, str, str]] = {
	1: ("Trough up-kicker", "coil", "used", "26-1200 (090-5044-ND)", "Lifts the right-most trough ball through the jam opto 22 toward the shooter lane switch 23; the ball-trough test fires it once per SELECT."),
	2: ("Auto launch", "coil", "used", "24-940 (090-5036-ND)", "Autoplunger coil assembly 500-6092-02-ND that fires the shooter-lane ball onto the playfield."),
	3: ("4-bank drop target reset", "coil", "used", "24-940 (090-5036-ND)", "Resets the four F-A-R-T drop targets."),
	4: ("Ball saver post down", "coil", "used", "32-1800 (090-5031-00-ND)", "The mini-coil of the death post's latch-and-frame assembly 515-7595-00-ND (Up/Down death post assembly 500-7022-00)."),
	5: ("Clam eject", "coil", "used", "27-1500 (090-5004-ND)", "Vertical up-kicker (VUK) that ejects the ball held on the Clam eject switch 64."),
	6: ("1-bank drop target reset", "coil", "used", "24-940 (090-5036-ND)", "Resets the Death 1-bank drop target."),
	7: ("Left slingshot", "coil", "used", "27-1500 (090-5004-ND)", ""),
	8: ("Right slingshot", "coil", "used", "27-1500 (090-5004-ND)", ""),
	9: ("Bottom pop bumper", "coil", "used", "26-1200 (090-5044-ND)", ""),
	10: ("Right pop bumper", "coil", "used", "26-1200 (090-5044-ND)", ""),
	11: ("Top pop bumper", "coil", "used", "26-1200 (090-5044-ND)", ""),
	12: ("Ball saver post up", "coil", "used", "26-1200 (090-5044-ND)", "Raises the death post; when energized the up/down post keeps the ball from draining between the lower flippers."),
	13: ("TV eject", "coil", "used", "23-800 (090-5001-ND)", "Scoop and vertical up-kicker that ejects the ball held on TV eject switch 13."),
	14: ("Upper left flipper", "coil", "used", "23-1500 (090-5062-ND)", "Mini-flipper bat assembly 500-6543-35-NDM. Fused 3 A on the playfield; driven with the left cabinet button's full press."),
	15: ("Left flipper", "coil", "used", "23-1100 (090-5030-ND)", "Fused 3 A on the playfield (GRY-YEL feed)."),
	16: ("Right flipper", "coil", "used", "23-1100 (090-5030-ND)", "Fused 3 A on the playfield (BLU-YEL feed)."),
	17: ("Left mini-flipper", "coil", "used", "27-950 (090-5046-01-ND)", "Left flipper of the Stewie mini-playfield; operates with the lower flipper buttons."),
	18: ("Right mini-flipper", "coil", "used", "27-950 (090-5046-01-ND)", "Right flipper of the Stewie mini-playfield."),
	19: ("Evil Monkey gate trip coil", "coil", "used", "32-1250 (515-6916-01-ND)", "Trip coil of the latch gate housing 500-6590-01-ND on the left ramp (manual name \"EVIL MONKEY (LEFT RAMP GATE)\"). The retained probes show the ROM re-firing it from game start until switch 35 reads closed (about forty transitions in the first seconds of play) and not firing it at all when 35 starts closed."),
	20: ("Stewie motor drive", "motor", "used", "Stepper motor 511-5043-00", "5 V stepper motor and controller PCB 511-5045-00 that turns the Stewie figure; absent from the Single and Cycling Coil Tests and exercised by the ROM's own Stewie Motor Test (F.G. icon)."),
	21: ("Mini-trough (mini-playfield shooter)", "coil", "used", "27-950 (090-5046-01-ND)", "Mini-playfield shooter and mini-kicker assembly 500-7023-00 that serves the mini-pinball."),
	22: ("Meg shake", "coil", "used", "27-950 (090-5046-01-ND)", "Meg popper assembly: a mini-coil that moves the Meg figurine."),
	23: ("Flash: lower left", "flasher", "used", "#89 bulb (165-5000-89)", "Yellow flash lamp (colour printed beside the starburst on the location drawing)."),
	24: ("Optional 5 V coil", "coil", "optional", "Opt. 5 V", "Optional coil: the manual says a coin meter, token dispenser or knocker is wired here when required; the retained known-working script binds a knocker sound to it."),
	25: ("Flash: back panel left (blue)", "flasher", "used", "#89 bulb (165-5000-89)", "Back-panel flasher behind a blue light cover."),
	26: ("Flash: back panel center (red)", "flasher", "used", "#89 bulb (165-5000-89)", "Back-panel flasher behind a red light cover."),
	27: ("Flash: back panel right (clear)", "flasher", "used", "#89 bulb (165-5000-89)", "Back-panel flasher behind a clear light cover."),
	28: ("Flash: beer can (Brian)", "flasher", "used", "#89 bulb (165-5000-89)", ""),
	29: ("Flash: Meg", "flasher", "used", "#89 bulb (165-5000-89)", ""),
	30: ("Flash: right orbit (spinner)", "flasher", "used", "#89 bulb (165-5000-89)", ""),
	31: ("Flash: pop bumpers", "flasher", "used", "#89 bulb (165-5000-89)", ""),
	32: ("Flash: lower right", "flasher", "used", "#89 bulb (165-5000-89)", "Yellow flash lamp (colour printed beside the starburst on the location drawing)."),
}
PINMAME_PWM_TYPED = {18, 19, 20, 21}


def output_id(address: int) -> str:
	return f"device.{address}-{slug(COILS[address][0])}"


def coil_wiring(address: int) -> dict[str, Any]:
	wiring: dict[str, Any] = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": CONTROL_WIRE[address - 1], "control_connection": CONTROL_CONNECTION[address - 1]}
	if address <= 13:
		wiring.update({"power_wire": "YEL-VIO", "power_connection": "J10-P9/10", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 14:
		wiring.update({"power_wire": "BLU-YEL via 3 A fuse from RED-YEL", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 15:
		wiring.update({"power_wire": "GRY-YEL via 3 A fuse from RED-YEL", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 16:
		wiring.update({"power_wire": "BLU-YEL via 3 A fuse from RED-YEL", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address in {17, 18, 19, 21, 22}:
		wiring.update({"power_wire": "BROWN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif address == 20:
		wiring.update({"power_wire": "RED", "power_connection": "J16-P4/8", "nominal_voltage_v": 5, "voltage_type": "dc"})
	elif address == 24:
		wiring.update({"power_wire": "RED", "power_connection": "J16-P4>8", "nominal_voltage_v": 5, "voltage_type": "dc"})
	else:
		wiring.update({"power_wire": "ORANGE", "power_connection": "J6-P10", "nominal_voltage_v": 20, "voltage_type": "dc"})
	return wiring


def make_output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, Any] | None = None, wiring: dict[str, Any] | None = None, stable_id: str | None = None) -> dict[str, Any]:
	namespace = {"pinmame.output.lamp": "pinmame.lamp", "pinmame.output.gi": "pinmame.gi", "physical.output.ticket": "manual.service-output"}.get(group, "pinmame.solenoid")
	result: dict[str, Any] = {"id": stable_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance(*sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	rom_names = COIL_ROM_NAMES
	for address, (label, kind, availability, part, note) in COILS.items():
		physical: dict[str, Any] = {"part_number": part, "quantity": 1}
		sentences = []
		if note:
			sentences.append(note)
		if address in rom_names:
			sentences.append(f"The ROM's Single Coil Test shows \"{rom_names[address]}\" for this coil and fires public solenoid {address} when SELECT is pressed.")
		elif address == 20:
			sentences.append("The retained boot-start run shows public solenoid 20 pulsing during power-up (the ROM homes the Stewie stepper).")
		if address == 3:
			sentences.append("The ROM's coil test prints the control wire as BRN-BLK for this coil; the manual's coil chart prints BRN-ORG at J8-P4 and the structured wiring follows the manual's chart (a wiring-detail difference, not a device disagreement).")
		if address in PINMAME_PWM_TYPED:
			sentences.append("Pinned PinMAME types public solenoids 18-21 as #89 bulb outputs (the Family Guy entry of sam.c copies the Avengers typing); this coil/motor is not a bulb, so graded PWM-style values published at this address are an emulator artifact.")
		if address in {25, 26, 27}:
			sentences.append("Three back-panel flashers (Q25-Q27) sit behind the blue, red and clear light covers 6B, 6R and 6C of back panel assembly 500-7032-00.")
		if kind == "flasher":
			sentences.append("The manual's flash-lamp test covers Q23 and Q25-Q32 on this game.")
		physical["notes"] = " ".join(sentences) if sentences else "Coil as listed in the manual's coils chart."
		sources = (MANUAL, RT_COIL, CORE, SCRIPT) if address in SCRIPT_COILS else (MANUAL, RT_COIL, CORE)
		if address == 19:
			sources = sources + (RT_EM_CLOSED, RT_EM_OPEN)
		items.append(make_output(address, label, kind, availability, sources, manual_address=f"Q{address}", physical=physical, wiring=coil_wiring(address), stable_id=output_id(address)))
	items.append(make_output(33, "PinMAME S.A.M. game-on state", "virtual", "used", (CORE, RT_BOOT), physical={"notes": "Synthetic S.A.M. fast-flip game-on state that pinned PinMAME publishes on public solenoid 33 (sam.c SAM_FASTFLIPSOL) for the fg_1200 family: the retained boot-start run observes it asserted at game start. It is not a driver-board transistor."}, stable_id="virtual.game-on"))
	for address, label, test_name in ((33, "Ticket advance", "AUX 1: TICKET ADVANCE"), (35, "Ticket enable", "AUX 3: TICKET ENABLE")):
		items.append(make_output(address, f"{label} (optional ticket dispenser)", "coil", "optional", TICKET_SOURCES, group="physical.output.ticket", manual_address=f"#{address}", stable_id=f"output.ticket.{address}.{slug(label)}", physical={"notes": (
			f"Optional output of the auxiliary (3X transistor) driver PCB 520-5068-01 in the backbox, which the manual's coin/ticket meter and ticket dispenser wiring diagram (PDF pages 169-170) shows driving the ticket dispenser and meters. The coil test of the older firmware (V3.00, V4.00, V8.00 and V11.0) lists it as \"{test_name} #{address}\" after Q32 and the retained sweeps fire it without changing any public solenoid; the V12.0 test omits it. It is a physical service identity: pinned PinMAME publishes nothing for it (public solenoid 33 is the synthetic game-on state and public 51-66 are unused compatibility addresses), so a consumer has no runtime state for it. The auxiliary board has a third transistor (AUX 2, #34) that no retained source names.")}))
	for address in range(51, 67):
		items.append(make_output(address, f"Unused S.A.M. auxiliary compatibility address {address}", "virtual", "unused", (CORE,), physical={"notes": "Public custom-solenoid space of the S.A.M. platform; Family Guy declares no custom solenoids, and its manual describes auxiliary coils only as optional positions #33-#35 of the coil test. The older firmware's Single Coil Test lists #33 and #35, which are kept as the physical ticket outputs below; the V12.0 test lists neither."}, stable_id=f"virtual.aux-{address}"))
	return items


SCRIPT_COILS = {1, 2, 3, 4, 5, 6, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}
COIL_ROM_NAMES = {
	1: "TROUGH UP-KICKER", 2: "AUTO LAUNCH", 3: "4-BANK DROP TARGET", 4: "BALL SAVER DOWN", 5: "CLAM EJECT", 6: "1-BANK DROP TARGET", 7: "LEFT SLINGSHOT", 8: "RIGHT SLINGSHOT",
	9: "BOTTOM BUMPER", 10: "RIGHT BUMPER", 11: "TOP BUMPER", 12: "BALL SAVER UP", 13: "TV EJECT", 14: "UPPER LEFT FLIPPER", 15: "LEFT FLIPPER", 16: "RIGHT FLIPPER",
	17: "LEFT MINI FLIPPER", 18: "RIGHT MINI FLIPPER", 19: "EVIL MONKEY", 21: "MINI TROUGH", 22: "MEG SHAKE", 23: "FLASH: LOWER LEFT",
	25: "FLASH: BACK LEFT", 26: "FLASH: BACK CENTER", 27: "FLASH: BACK RIGHT", 28: "FLASH: BEER CAN", 29: "FLASH: MEG", 30: "FLASH: RIGHT ORBIT", 31: "FLASH: POPS", 32: "FLASH: LOWER RIGHT",
}


# --------------------------------------------------------------------------------------------
# Lamps
# --------------------------------------------------------------------------------------------

LAMP_COLUMN = [("IC-U17", "YEL-BRN", "J13-P9"), ("IC-U16", "YEL-RED", "J13-P8"), ("IC-U15", "YEL-ORG", "J13-P7"), ("IC-U14", "YEL-BLK", "J13-P6"), ("IC-U13", "YEL-GRN", "J13-P5"), ("IC-U12", "YEL-BLU", "J13-P4"), ("IC-U11", "YEL-VIO", "J13-P3"), ("IC-U10", "YEL-GRY", "J13-P1")]
LAMP_ROW = [("Q33", "RED-BRN", "J12-P1"), ("Q34", "RED-BLK", "J12-P2"), ("Q35", "RED-ORG", "J12-P3"), ("Q36", "RED-YEL", "J12-P4"), ("Q37", "RED-GRN", "J12-P5"), ("Q38", "RED-BLU", "J12-P6"), ("Q39", "RED-VIO", "J12-P8"), ("Q40", "RED-GRY", "J12-P9"), ("Q41", "RED-WHT", "J12-P10"), ("Q42", "RED", "J12-P11")]

LAMPS: dict[int, str] = {
	1: "Start button", 2: "Tournament Start button", 3: "Family Peter", 4: "Family Lois", 5: "Family Brian", 6: "Family Chris", 7: "Family Meg", 8: "Family Stewie",
	9: "Pinball P", 10: "Pinball I", 11: "Pinball N", 12: "Pinball B", 13: "Pinball A", 14: "Pinball L (first)", 15: "Pinball L (second)", 16: "Left outlane",
	17: "Left return (2x Lois)", 18: "Raise death (left inner)", 19: "Good Old Boys", 20: "Super Griffins", 21: "Chicken Fight", 22: "Sexy Party", 23: "Ipecac Contest", 24: "By right sling (1)",
	25: "By right sling (2)", 26: "By right sling (3)", 27: "Right return (2x Meg)", 28: "Right outlane (special)", 29: "TV (scoop)", 30: "Pinball (scoop)", 31: "Multiball (scoop)", 32: "Meg jackpot",
	33: "Pirate stand-up", 34: "Right Newton jackpot", 35: "FART T", 36: "FART R", 37: "FART A", 38: "FART F", 39: "Left orbit Chris", 40: "Left orbit jackpot",
	41: "Death (1-bank drop target)", 42: "Skill shot", 43: "200K to left ramp", 44: "300K to left ramp", 45: "400K to left ramp", 46: "500K to left ramp", 47: "Crazy Chris", 48: "Collect beers (beer can)",
	49: "Giggity giggity (beer can)", 50: "Happy hour (beer can)", 51: "Remember when (beer can)", 52: "Lard multiball (beer can)", 53: "Extra ball (left Newton)", 54: "Left Newton jackpot", 55: "Evil Monkey jackpot", 56: "3-bank top (X stand-up)",
	57: "3-bank middle (X stand-up)", 58: "3-bank bottom (X stand-up)", 59: "Not used 59", 60: "Not used 60", 61: "Bottom bumper", 62: "Drunken Clam (mystery)", 63: "Stewie (stand-up x2)", 64: "Shoot again",
	65: "Right orbit Lois", 66: "Right orbit jackpot", 67: "Spinner (Lois)", 68: "Mini shoot again", 69: "Ball saver post", 70: "Stewie spot light", 71: "Not used 71", 72: "Not used 72",
	73: "Not used 73", 74: "Not used 74", 75: "Not used 75", 76: "Not used 76", 77: "Not used 77", 78: "Not used 78", 79: "Not used 79", 80: "Not used 80",
}
LAMP_UNUSED = {59, 60, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80}
LAMP_ROM_NAMES = {
	1: "START BUTTON", 2: "TOURNAMENT START BUTTON", 3: "FAMILY PETER", 4: "FAMILY LOIS", 5: "FAMILY BRIAN", 6: "FAMILY CHRIS", 7: "FAMILY MEG", 8: "FAMILY STEWIE",
	9: "(P)INBALL", 10: "P(I)NBALL", 11: "PI(N)BALL", 12: "PIN(B)ALL", 13: "PINB(A)LL", 14: "PINBA(L)L", 15: "PINBAL(L)", 16: "LEFT OUTLANE",
	17: "LEFT RETURN", 18: "RAISE DEATH", 19: "GOOD OLD BOYS", 20: "SUPER GRIFFINS", 21: "CHICKEN FIGHT", 22: "SEXY PARTY", 23: "IPECAC CONTEST", 24: "(1)",
	25: "(2)", 26: "(3)", 27: "RIGHT RETURN", 28: "RIGHT OUTLANE", 29: "TV", 30: "PINBALL", 31: "MULTIBALL", 32: "MEG JACKPOT",
	33: "PIRATE", 34: "RIGHT NEWTON JACKPOT", 35: "FAR(T)", 36: "FA(R)T", 37: "F(A)RT", 38: "(F)ART", 39: "LEFT ORBIT CHRIS", 40: "LEFT ORBIT JACKPOT",
	41: "DEATH", 42: "SKILL SHOT", 43: "200K", 44: "300K", 45: "400K", 46: "500K", 47: "CRAZY CHRIS", 48: "COLLECT BEERS",
	49: "GIGGITY GIGGITY", 50: "HAPPY HOUR", 51: "REMEMBER WHEN", 52: "LARD MULTIBALL", 53: "EXTRA BALL", 54: "LEFT NEWTON JACKPOT", 55: "EVIL MONKEY JACKPOT", 56: "3 BANK TOP",
	57: "3 BANK MID", 58: "3 BANK BOT", 59: "NOT USED #59", 60: "NOT USED #60", 61: "BOTTOM BUMPER", 62: "MYSTERY", 63: "STEWIE", 64: "SHOOT AGAIN",
	65: "RIGHT ORBIT LOIS", 66: "RIGHT ORBIT JACKPOT", 67: "SPINNER", 68: "MINI SHOOT AGAIN", 69: "BALL SAVER POST", 70: "STEWIE SPOT LIGHT", 71: "NOT USED #71", 72: "NOT USED #72",
	73: "NOT USED #73", 74: "NOT USED #74", 75: "NOT USED #75", 76: "NOT USED #76", 77: "NOT USED #77", 78: "NOT USED #78", 79: "NOT USED #79", 80: "NOT USED #80",
}
# Printed bulb legend: #555 wedge in the first lamp column of rows 1-9 and lamp 3, #CM86 for lamp 2, white LED for 61, #44 otherwise.
LAMP_555 = {1, 3, 9, 17, 25, 33, 41, 49, 57, 65}
LAMP_ABOVE_PLAYFIELD = {61, 68, 70}


def lamp_part(address: int) -> tuple[str, str]:
	if address == 2:
		return "165-5103-00", "#CM86 clear mini-wedge bulb (printed legend \"#CM86 Clear\")"
	if address == 61:
		return "112-5024-08", "white LED module on a wedge base (printed \"LED WB WHT\")"
	if address in LAMP_555:
		return "165-5002-00", "#555 clear wedge-base bulb"
	return "165-5000-44-HF", "#44 clear heavy-filament bayonet bulb"


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 81):
		label = LAMPS[address]
		availability = "unused" if address in LAMP_UNUSED else "used"
		column = (address - 1) % 8
		row = (address - 1) // 8
		ic, drive_wire, drive_pin = LAMP_COLUMN[column]
		transistor, return_wire, return_pin = LAMP_ROW[row]
		physical: dict[str, Any] = {}
		if availability == "used":
			part, bulb = lamp_part(address)
			physical = {"part_number": part, "quantity": 1}
			notes = [f"Manual name \"{_MANUAL_LAMP_NAMES.get(address, label.upper())}\"; the ROM's Single Lamp Test prints \"{LAMP_ROM_NAMES[address]}\" with the wire colours {drive_wire} / {return_wire}.", f"Printed bulb: {bulb}."]
			if address in {1, 2}:
				physical["location"] = "Cabinet front start button" if address == 1 else "Cabinet front-molding tournament start button"
				notes.append("Cabinet lamp; it has no box on the playfield lamp-location drawing.")
				if address == 2:
					notes.append("The lamp grid prints 165-5103-00 for this bulb while the cabinet parts list (PDF page 68, item 11T) prints the CM86 / 086 6.3V mini-wedge-base clear bulb as 165-5002-01: a part-number disagreement between two printed pages that does not change the device.")
			elif address in LAMP_ABOVE_PLAYFIELD:
				physical["location"] = "Mini-playfield (above the mini-playfield)" if address == 68 else "Above the playfield"
			else:
				physical["location"] = "Below the playfield (insert lamp)"
			if address in {61, 70}:
				notes.append("Printed D.O.T.S.: the lamp's diode is on a playfield terminal strip (PDF page 126).")
			physical["notes"] = " ".join(notes)
		else:
			physical["notes"] = f"Printed NOT USED in the manual's lamp grid; the ROM's lamp test still steps through the address and prints \"{LAMP_ROM_NAMES[address]}\"."
		wiring = {"board": "I/O Power Driver board lamp matrix", "driver_transistor": transistor, "drive_wire": drive_wire, "drive_connection": drive_pin, "return_wire": return_wire, "return_connection": return_pin, "return_component": ic, "nominal_voltage_v": 18, "voltage_type": "dc"}
		sources = (MANUAL, RT_LAMP, CORE) if address in LAMP_UNUSED or address in {1, 2, 59, 60} else (MANUAL, RT_LAMP, CORE, SCRIPT)
		items.append(make_output(address, label, "lamp", availability, sources, group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring=wiring, stable_id=f"lamp.{address}-{slug(label)}"))
	return items


_MANUAL_LAMP_NAMES = {
	16: "LEFT OUTLANE [NOT SPECIAL]", 17: "LEFT RETURN [2X LOIS]", 18: "RAISE DEATH [LEFT INNER]", 24: "( 1 ) [BY RT. SLING]", 25: "( 2 ) [BY RT. SLING.]", 26: "( 3 ) [BY RT. SLING]", 27: "RT RETURN [2X MEG]", 28: "RT. OUTLANE [SPECIAL]",
	29: "TV [SCOOP]", 30: "PINBALL [SCOOP]", 31: "MULTIBALL [SCOOP]", 33: "PIRATE [STAND-UP]", 34: "RT. NEWTON JACKPOT", 35: "FAR ( T ) [4-BNK DRP/TRG]", 36: "FA ( R ) T [4-BNK DRP/TRG]", 37: "F ( A ) RT [4-BNK DRP/TRG]", 38: "( F ) ART [4-BNK DRP/TRG]",
	41: "DEATH [1-BNK DRP/TRG]", 43: "200K [TO LEFT RAMP]", 44: "300K [TO LEFT RAMP]", 45: "400K [TO LEFT RAMP]", 46: "500K [TO LEFT RAMP]", 47: "CRAZY CHRIS [TO LEFT RAMP]", 48: "COLLECT BEERS [BEER CAN]",
	49: "GIGGITY GIGGITY [BEER CAN]", 50: "HAPPY HOUR [BEER CAN]", 51: "REMEMBER WHEN [BEER CAN]", 52: "LARD MULTIBALL [BEER CAN]", 53: "EXTRA BALL [LEFT NEWTON]", 56: "3-BANK TOP [ 'X' STAND-UP]", 57: "3-BANK MID [ 'X' STAND-UP]", 58: "3-BANK BOT [ 'X' STAND-UP]",
	62: "DRUNKEN CLAM [MYSTERY]", 63: "STEWIE [STAND-UP X2]", 67: "SPINNER [LOIS]",
	9: "( P ) INBALL", 10: "P ( I ) NBALL", 11: "PI ( N ) BALL", 12: "PIN ( B ) ALL", 13: "PINB ( A ) LL", 14: "PINBA ( L ) L", 15: "PINBAL ( L )",
}


# --------------------------------------------------------------------------------------------
# Mini-playfield LED letters (board 520-5264-00)
# --------------------------------------------------------------------------------------------

# lamp address: (LED reference, letter, family member, resistor, latch bit, column)
LEDS: dict[int, tuple[str, str, str, str, int, str]] = {
	97: ("LED24", "N", "Brian", "R1", 0, "A"), 98: ("LED23", "M", "Meg", "R6", 1, "A"), 99: ("LED22", "E", "Meg", "R5", 2, "A"), 100: ("LED21", "G", "Meg", "R4", 3, "A"),
	121: ("LED48", "S", "Chris", "R1", 0, "B"), 122: ("LED47", "I", "Chris", "R6", 1, "B"), 123: ("LED46", "R", "Chris", "R5", 2, "B"), 124: ("LED45", "H", "Chris", "R4", 3, "B"), 125: ("LED44", "C", "Chris", "R2", 4, "B"),
	89: ("LED16", "E (first)", "Peter", "R13", 0, "A"), 90: ("LED15", "T", "Peter", "R12", 1, "A"), 91: ("LED14", "E (second)", "Peter", "R11", 2, "A"), 92: ("LED13", "R", "Peter", "R10", 3, "A"), 114: ("LED39", "P", "Peter", "R12", 1, "B"),
	81: ("LED8", "A", "Brian", "R20", 0, "A"), 82: ("LED7", "I", "Brian", "R19", 1, "A"), 83: ("LED6", "R", "Brian", "R18", 2, "A"), 84: ("LED5", "B", "Brian", "R17", 3, "A"),
	105: ("LED32", "S", "Lois", "R20", 0, "B"), 106: ("LED31", "I", "Lois", "R19", 1, "B"), 107: ("LED30", "O", "Lois", "R18", 2, "B"), 108: ("LED29", "L", "Lois", "R17", 3, "B"),
}
LED_COLOURS = {5: "amber", 6: "amber", 7: "amber", 8: "amber", 24: "amber", 44: "amber", 45: "amber", 46: "amber", 47: "amber", 48: "amber", 13: "white", 14: "white", 15: "white", 16: "white", 39: "white", 21: "yellow", 22: "yellow", 23: "yellow", 29: "yellow", 30: "yellow", 31: "yellow", 32: "yellow"}
LED_PARTS = {"amber": "Omron LA E65B", "white": "Omron LW 67C", "yellow": "Omron LY E65B"}
# Published by PinMAME's 520-5264-00 model but with no LED on the board: latch bit 4 of column A (101), and the unfitted bits of group 2 column B (113, 115, 116).
LED_LIVE_UNFITTED = {101, 113, 115, 116}


def led_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(81, 129):
		if address in LEDS:
			ref, letter, member, resistor, bit, column = LEDS[address]
			number = int(ref[3:])
			colour = LED_COLOURS[number]
			label = f"Mini-playfield {member} letter {letter} ({ref})"
			physical = {"part_number": LED_PARTS[colour], "quantity": 1, "location": f"Stewie mini-playfield, letter {letter} of {member.upper()} on LED board 511-5046-00", "notes": f"{colour.capitalize()} LED {ref} on the mini-playfield LED board (schematic 520-5264-00). Reading of the board's nets: resistor {resistor}, latch bit {bit}, LED column {column}. Public lamp {address} is the PinMAME output of that bit and column (sam.c SAM_GAME_FG block); the retained runs of fg_1200ag drive exactly this set of 22 addresses. Pinned PinMAME types these outputs as LED pulses (8 ms over 16 ms)."}
			sources = (MANUAL, CORE, RT_LAMP, RT_BOOT)
			state_availability = "used"
		else:
			label = f"Unused mini-playfield LED matrix position {address}"
			if address in LED_LIVE_UNFITTED:
				text = "A bit position PinMAME's 520-5264-00 model publishes (it passes the latch mask) but where the board has no LED: the schematic gives the resistor line of this bit no load on this column, and no retained run drives it."
			else:
				text = "Outside the bits PinMAME's 520-5264-00 model publishes (latch masks 0x0F, 0x0F and 0x1F), so the address is always zero."
			physical = {"notes": text}
			sources = (CORE, MANUAL)
			state_availability = "unused"
		items.append(make_output(address, label, "lamp", state_availability, sources, group="pinmame.output.lamp", manual_address=None, physical=physical, wiring={"board": "Mini-playfield LED board 511-5046-00 (520-5264-00)"} if address in LEDS else None, stable_id=f"lamp.{address}-{slug(label)}"))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	notes = (
		"PinMAME publishes one aggregate GI channel (public GI 0), the on/off state of the G.I. relay RLY1 that switches the 5.7 VAC feed of all four general-illumination circuits. "
		"The manual lists four fused circuits on connector J15: circuit 1 (F1, BRN-WHT to WHT-BRN) is NOT USED and carries no bulbs; circuit 2 (F2, YELLOW to WHT-YEL) feeds 13 #44 and 3 #555 spot lights on the left side above the playfield; "
		"circuit 3 (F3, GREEN to WHT-GRN) feeds 10 #44 yellow bulbs on the back panel plus 2 #555 bulbs on the coin door; circuit 4 (F4, VIOLET to WHT-VIO) feeds 8 #44 and 10 #555 spot lights above the playfield. "
		"The manual notes G.I. bulb quantities may change during production. The retained boot-start run shows GI 0 on at power-up."
	)
	return [make_output(0, "General illumination", "gi", "used", (MANUAL, CORE, RT_BOOT), group="pinmame.output.gi", manual_address="GI-0", physical={"location": "Playfield spot lights, back panel and coin door", "notes": notes}, stable_id="gi.master")]


def outputs() -> list[dict[str, Any]]:
	return solenoid_outputs() + lamp_outputs() + led_outputs() + gi_outputs()
