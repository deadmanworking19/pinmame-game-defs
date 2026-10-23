"""Reviewed Big Game (Stern, 1980) device data, kept apart from the builder so both stay readable.

Every number below was read from this game's own manual, schematic sheets, corrections sheet and instruction card, or observed in a
retained harness run; none is carried from a sister machine. Where a Stern MPU-200 board drawing is shared with other games, this game's own
copy of the sheet was read again.
"""

from __future__ import annotations

from typing import Any

# --- Drivers ---------------------------------------------------------------------------------------------------------

_SAME_HARDWARE = ("Identical INITGAME data to the production driver (GEN_STMPU200, seven-digit dispst7 displays, FLIP_SW(FLIP_L), no extra lamp columns, "
	"Stern ST300 sound board, input_ports_st), so the controller inventory is unchanged.")

DRIVERS: dict[str, tuple[str, str, str, str | None, str]] = {
	"biggame": (
		"Big Game", "1980", "Stern", None,
		"Production ROM set (U1, U2, U5 and U6) and the reference for this definition: GEN_STMPU200, seven-digit dispst7 displays, FLIP_SW(FLIP_L), Stern ST300 sound board. "
		"Every retained harness run boots this driver.",
	),
	"biggamfp": (
		"Big Game (Free Play)", "1980", "Stern", "biggame",
		"Free-play build of the production ROM: the same U1, U5 and U6 images and a free-play U2. " + _SAME_HARDWARE + " No harness run was made with it.",
	),
	"biggameb": (
		"Big Game (MOD rev. 7)", "2019", "Stern / Idleman", "biggame",
		"Community rules revision 7 for the same hardware. " + _SAME_HARDWARE + " It changes the rules in ROM only; the ROM was not available for a harness run.",
	),
	"biggamec": (
		"Big Game (MOD rev. 8)", "2020", "Stern / Idleman", "biggame",
		"Community rules revision 8 for the same hardware. " + _SAME_HARDWARE + " It changes the rules in ROM only; the ROM was not available for a harness run.",
	),
	"biggamed": (
		"Big Game (MOD rev. 9)", "2021", "Stern / Idleman", "biggame",
		"Community rules revision 9 for the same hardware. " + _SAME_HARDWARE + " It changes the rules in ROM only; the ROM was not available for a harness run.",
	),
	"biggamee": (
		"Big Game (MOD rev. 12)", "2023", "Stern / Idleman", "biggame",
		"Community rules revision 12 for the same hardware. " + _SAME_HARDWARE + " It changes the rules in ROM only; the ROM was not available for a harness run.",
	),
	"biggamef": (
		"Big Game (MOD rev. 13)", "2024", "Stern / Idleman", "biggame",
		"Community rules revision 13 for the same hardware. " + _SAME_HARDWARE + " It changes the rules in ROM only; the ROM was not available for a harness run.",
	),
}

# --- Cabinet and service inputs ---------------------------------------------------------------------------------------

SERVICE_SWITCHES: dict[int, dict[str, Any]] = {
	-7: {
		"id": "switch.self-test-button", "label": "Self Test button (coin door)", "roles": ["service.test"], "availability": "used",
		"location": "Inside the coin door",
		"notes": "The Self-Test button inside the coin door (manual Figure 1), wired from A4J3-1 (R) to A3J2-7 (Y-R) on the cabinet sheet. Public -7 drives the ROM's tests in the "
			"manual's order: in the retained runs the first press starts the burn-in, the fourth the solenoid test and the fifth the switch test.",
		"evidence": "manual-and-harness",
	},
	-6: {
		"id": "switch.cpu-diagnostic-button", "label": "CPU diagnostic input (MPU NMI)", "roles": ["service.diagnostic"], "availability": "optional",
		"location": "MPU module",
		"notes": "PinMAME routes public -6 to the CPU's NMI line (BY35_SWCPUDIAG). The manual names no button for it; the S33 MEMORY CLEAR pushbuttons are a separate contact "
			"(the remote memory-clear input), so the identity of the two is not assumed.",
		"evidence": "core",
	},
	-5: {
		"id": "switch.sound-diagnostic-button", "label": "Sound board diagnostic input", "roles": ["service.diagnostic"], "availability": "optional",
		"location": "Sound module",
		"notes": "PinMAME routes public -5 to the ST300 sound board's diagnostic input (BY35_SWSOUNDDIAG). The manual documents no such button on the B-605 sound board.",
		"evidence": "core",
	},
}

# --- Matrix switches ----------------------------------------------------------------------------------------------------
#
# Public address = strobe * 8 + return + 1 on the five-strobe by eight-return MPU matrix. ``cabinet`` rows are wired on the cabinet sheet
# (A4J3), the others on the playfield wiring diagram (A4J2).

STROBES = {
	0: ("W-R", "A4J2-1"), 1: ("BRN-W", "A4J2-2"), 2: ("W-BLU", "A4J2-3"), 3: ("W-Y", "A4J2-4"), 4: ("Y-R", "A4J2-5"),
}
RETURNS = {
	0: ("BRN", "A4J2-8"), 1: ("GREY", "A4J2-9"), 2: ("W-O", "A4J2-10"), 3: ("W-B", "A4J2-11"),
	4: ("W-G", "A4J2-12"), 5: ("W-BRN", "A4J2-13"), 6: ("BRN-Y", "A4J2-14"), 7: ("O", "A4J2-15"),
}
CABINET_RETURNS = {0: ("R-W", "A4J3-9"), 1: ("BRN-W", "A4J3-10"), 2: ("BLU", "A4J3-11"), 5: ("BLU-W", "A4J3-14"), 6: ("BLU-O", "A4J3-15"), 7: ("Y", "A4J3-16")}
CABINET_STROBE0 = ("R-Y", "A4J3-2")
# The cabinet sheet draws the CHUTE contacts on returns I1 and I2 without a series diode; every other drawn contact has one.
NO_DIODE_SWITCHES = {2, 3}

# address -> spec. ``printed`` is the Switch Identification table's text (manual page 18), ``matrix`` the playfield or cabinet sheet's cell.
SWITCHES: dict[int, dict[str, Any]] = {
	1: {"id": "switch.coin-chute-1", "label": "Coin chute 1", "type": "other", "cabinet": True, "roles": ["cabinet.coin.1"],
		"printed": "CHUTE", "matrix": "CHUTE",
		"notes": "SW-1 of the coin-door drawing on the Switch Identification page: the middle chute of the US three-chute door (the German door puts SW-1 at the hinge). The location page lists it as `1 * LEFT CHUTE` and refers to that drawing. "
			"Cabinet sheet return A4J3-9, printed `(R-W)`; the credit tables call switch 1 `WIRE COLOR BLUE` and switch 3 `RED-WHITE`, the reverse of the cabinet sheet's colours for returns A4J3-9 and A4J3-11, a wire-colour disagreement that does not change the address. "
			"A coin on it adds one credit in the retained gameplay run."},
	2: {"id": "switch.coin-chute-2", "label": "Coin chute 2", "type": "other", "cabinet": True, "roles": ["cabinet.coin.2"],
		"printed": "CHUTE", "matrix": "CHUTE",
		"notes": "SW-2 of the coin-door drawing: the chute at the hinge side of the US three-chute door. Return A4J3-10 (BRN-W), the colour the credit table also prints for switch 2. A coin on it adds one credit in the retained gameplay run."},
	3: {"id": "switch.coin-chute-3", "label": "Coin chute 3", "type": "other", "cabinet": True, "roles": ["cabinet.coin.3"],
		"printed": "CHUTE", "matrix": "CHUTE",
		"notes": "SW-3 of the coin-door drawing, the chute farthest from the hinge. Return A4J3-11, printed `(BLU)` on the cabinet sheet (the credit table says RED-WHITE). A coin on it adds two credits in the retained gameplay run."},
	4: {"id": "switch.left-spinner", "label": "Left spinning target", "type": "other", "pulse": True,
		"printed": "SPIN-TARGET (LEFT)", "matrix": "SP.T. (LEFT)",
		"notes": "The outer of the two spinning targets on the wire that spans the left loop (location drawing leader 4; Spin Target Ass'y A-563-11, target and wire 14A-7-10). Each rotation closes the contact once. "
			"The manual: the left spinner lites when X is lit; it scored 2,000 per closure in the retained gameplay run while card X was selected."},
	5: {"id": "switch.right-spinner", "label": "Right spinning target", "type": "other", "pulse": True,
		"printed": "SPIN-TARGET (RIGHT)", "matrix": "SP.T. (RIGHT)",
		"notes": "The inner of the two spinning targets on the same wire, beside the top-left drop bank (location drawing leader 5). The manual: it lites when B-I-G is made; it scored 100 per closure in the retained run before B-I-G was made."},
	6: {"id": "switch.credit-button", "label": "Credit button", "type": "button", "cabinet": True, "roles": ["cabinet.start"],
		"printed": "CREDIT BUTTON", "matrix": "CREDIT",
		"notes": "Coin-door credit (start) button. In the retained gameplay run it starts a game from credits and decrements the credit display."},
	7: {"id": "switch.tilt", "label": "Tilt (roll tilt and pendulum)", "type": "tilt", "cabinet": True, "quantity": 2, "roles": ["cabinet.tilt"],
		"printed": "TILTS", "matrix": "TILT",
		"notes": "Shared matrix position for two normally open tilt contacts: the location page lists `7 ROLL-TILT` and `7 PENDULUM`, and the cabinet sheet draws two contacts in parallel on return A4J3-15 (BLU-O) with a capacitor across them. "
			"The installation page counts three normally open tilt switches (plumb bob, ball tilt and a panel tilt on the bottom of the playfield panel); the location page puts the tilt board on 8, so the panel tilt is not counted here. "
			"Closing public 7 in play drops the flipper-enable output 19 and lights TILT (lamp 61) in the retained gameplay run."},
	8: {"id": "switch.slam", "label": "Slam (door, tilt board and playfield)", "type": "tilt", "cabinet": True, "roles": ["cabinet.slam-tilt"],
		"printed": "SLAM & VIB. TILTS", "matrix": "SLAM",
		"notes": "Shared matrix position for the slam contacts. The location page lists `8 TILT BOARD` and `8 DOOR & PLAYFIELD VIB.`; the operating text says there is a slam switch on the front door, one on the tilt board and one on the playfield, and that an operator may fit more. "
			"The cabinet sheet draws one SLAM contact on return A4J3-16 (Y). Because operators may add contacts, no quantity is asserted. In the retained slam run, closing public 8 in play ends the game and the ROM repeats its power-up initialisation."},
	9: {"id": "switch.top-thumper-bumper", "label": "Top thumper bumper", "type": "leaf", "pulse": True,
		"printed": "TOP THUMPER", "matrix": "TOP THUMP.",
		"notes": "Closing it in play scores 1,000 (3-ball setting), changes the card selection and fires public output 1 in the retained gameplay run. The feature text calls the top bumper `SWS-#11` once and `SW-#9` once; the switch table, the matrix sheet, the location drawing and the run all put it on 9."},
	10: {"id": "switch.lower-left-thumper-bumper", "label": "Lower left thumper bumper", "type": "leaf", "pulse": True,
		"printed": "LOWER LEFT THUMPER", "matrix": "LOWER-L. THUMP.",
		"notes": "Closing it scores 1,000 and fires public output 2 in the retained gameplay run."},
	11: {"id": "switch.lower-right-thumper-bumper", "label": "Lower right thumper bumper", "type": "leaf", "pulse": True,
		"printed": "LOWER RIGHT THUMPER", "matrix": "RIGHT THUMP.",
		"notes": "Closing it scores 1,000 and fires public output 3 in the retained gameplay run."},
	12: {"id": "switch.left-slingshot", "label": "Left slingshot", "type": "leaf", "pulse": True,
		"printed": "LEFT SLING-SHOT", "matrix": "L. SLING SHOT",
		"notes": "Closing it scores 10, changes the card selection and fires public output 4 in the retained gameplay run."},
	13: {"id": "switch.right-slingshot", "label": "Right slingshot", "type": "leaf", "pulse": True,
		"printed": "RIGHT SLING-SHOT", "matrix": "R.SLING SHOT",
		"notes": "Closing it scores 10, changes the card selection and fires public output 5 in the retained gameplay run."},
	14: {"id": "switch.top-left-drop-target-3", "label": "Top left drop target 3", "type": "leaf", "drop": True,
		"printed": "TOP LEFT DROP TARGET (3)", "matrix": "LEFT D.T. #3",
		"notes": "Target 3 of the top-left three-bank (bank 1A, D-580-3D-1), nearest the top thumper. Closed while the target is down. In the retained gameplay run it scores 500 and spots number 3 on the selected cards X and Z (lamps 19 and 43)."},
	15: {"id": "switch.top-left-drop-target-2", "label": "Top left drop target 2", "type": "leaf", "drop": True,
		"printed": "TOP LEFT DROP TARGET (2)", "matrix": "LEFT D.T. #2",
		"notes": "Target 2 of the top-left three-bank. Closed while down; spots number 2 (lamps 3 and 27 in the retained run)."},
	16: {"id": "switch.top-left-drop-target-1", "label": "Top left drop target 1", "type": "leaf", "drop": True,
		"printed": "TOP LEFT DROP TARGET (1)", "matrix": "LEFT D.T. #1",
		"notes": "Target 1 of the top-left three-bank. Closed while down; spots number 1 (lamps 50 and 12). Closed last, it completes the bank and the ROM fires public output 7, the bank reset, in the retained run."},
	17: {"id": "switch.top-left-lane", "label": "Top left roll-over lane (B)", "type": "leaf",
		"printed": "TOP LEFT ROLL-OVER WIRE", "matrix": "TOP L. R.O.W.",
		"notes": "Left of the three top lanes, lettered B. Scores 500, lights B (lamp 42) and changes the card selection in the retained gameplay run."},
	18: {"id": "switch.top-middle-lane", "label": "Top middle roll-over lane (I)", "type": "leaf",
		"printed": "TOP MID. ROLL-OVER WIRE", "matrix": "TOP MID. R.O.W.",
		"notes": "Middle top lane, lettered I. Scores 500 and lights I (lamp 26); the manual says it scores 5,000 when BIG is lit (lamp 6, `TOP R.O.W. \"I\" 5,000`)."},
	19: {"id": "switch.top-right-lane", "label": "Top right roll-over lane (G)", "type": "leaf",
		"printed": "TOP RIGHT ROLL-OVER WIRE", "matrix": "TOP R. R.O.W.",
		"notes": "Right top lane, lettered G. Scores 500 and lights G (lamp 10); completing B-I-G lit lamps 6 and 30 in the retained gameplay run."},
	20: {"id": "switch.standup-target-g", "label": "Stand-up target G", "type": "leaf", "pulse": True,
		"printed": "STAND-UP TARGET \"G\"", "matrix": "S.U.\"G\"",
		"notes": "Upper of the two stand-up targets on the left (Target Ass'y A-461-1). Scores 500 and lights the second G (lamp 57). The matrix sheet draws a capacitor across the contact."},
	21: {"id": "switch.standup-target-a", "label": "Stand-up target A", "type": "leaf", "pulse": True,
		"printed": "STAND-UP TARGET \"A\"", "matrix": "S.U.\"A\"",
		"notes": "Lower of the two stand-up targets on the left. Scores 500 and lights A (lamp 41). The matrix sheet draws a capacitor across the contact."},
	22: {"id": "switch.top-right-drop-target-6", "label": "Top right drop target 6", "type": "leaf", "drop": True,
		"printed": "TOP RIGHT DROP TARGET (6)", "matrix": "TOP-R. D.T. #6",
		"notes": "Target 6 of the top-right three-bank (bank 1B, D-580-3D-2). Closed while down; spots number 6 (lamps 4 and 44 in the retained run)."},
	23: {"id": "switch.top-right-drop-target-5", "label": "Top right drop target 5", "type": "leaf", "drop": True,
		"printed": "TOP RIGHT DROP TARGET (5)", "matrix": "TOP-R. D.T. #5",
		"notes": "Target 5 of the top-right three-bank. Closed while down; spots number 5 (lamps 51 and 28)."},
	24: {"id": "switch.top-right-drop-target-4", "label": "Top right drop target 4", "type": "leaf", "drop": True,
		"printed": "TOP RIGHT DROP TARGET (4)", "matrix": "TOP-R. D.T. #4",
		"notes": "Target 4 of the top-right three-bank, nearest the top thumper. Closed while down; spots number 4 (lamps 35 and 58). Closed last, it completes the bank and the ROM fires public output 8, the bank reset."},
	25: {"id": "switch.center-roll-over-button", "label": "Center roll-over button", "type": "button",
		"printed": "MIDDLE ROLL-OVER BUTTON", "matrix": "CENTER R.O.B.",
		"notes": "Star roll-over button (4B-275) between cards X and Y. Scores 5,000 and changes the card selection (manual and retained run). The matrix sheet draws a capacitor across the contact."},
	26: {"id": "switch.top-left-roll-over-button", "label": "Top left roll-over button", "type": "button",
		"printed": "TOP LEFT ROLL-OVER BUTTON", "matrix": "TOP LEFT ROB",
		"notes": "Star roll-over button above the top-left drop bank. The manual says it scores 100, and 3,000 when BIG is made; the playfield art beside it prints 500 and 5000 when lit, and it scored 5,000 in the retained run after B-I-G was made. The matrix sheet draws a capacitor across the contact."},
	27: {"id": "switch.left-side-lane", "label": "Left center side lane", "type": "leaf",
		"printed": "MIDDLE LEFT ROLL-OVER BUTTON", "matrix": "CENTER LEFT R.O.W.",
		"notes": "Roll-over in the left side lane beside the G and A stand-ups (feature text: `LEFT CENTER SIDE LANE`). The switch table calls it a roll-over button, but the matrix sheet draws a roll-over wire form (R.O.W.), "
			"the location drawing a wire slot and the playfield-parts drawing a W7 roll-over wire (A-149) there, while the drawing's five 4B-275 buttons are elsewhere; it is recorded as a wire. "
			"Scores 5,000; awards the extra ball when BIG-GAME is made and the special the second time (manual)."},
	28: {"id": "switch.right-return-lane", "label": "Right return lane (E)", "type": "leaf",
		"printed": "RIGHT RETURN LANE", "matrix": "R. RETURN LANE",
		"notes": "Right inlane, lettered E. Scores 5,000 and lights E (lamp 9) in the retained gameplay run."},
	29: {"id": "switch.left-return-lane", "label": "Left return lane (M)", "type": "leaf",
		"printed": "LEFT RETURN LANE", "matrix": "L. RETURN LANE",
		"notes": "Left inlane, lettered M. Scores 5,000. In the retained run it was the last letter of B-I-G-G-A-M-E, so the letters cleared and lamp 53 (LEFT S.U. TARG. 5,000) lit."},
	30: {"id": "switch.lower-right-drop-target-9", "label": "Lower right drop target 9", "type": "leaf", "drop": True,
		"printed": "LOWER RIGHT DROP TARGET (9)", "matrix": "LOW. R. D.T. #9",
		"notes": "Target 9, the lowest of the lower-right three-bank (bank 1C, D-580-3D-3) beside the right lane. Closed while down; spots number 9 (lamps 52 and 59)."},
	31: {"id": "switch.lower-right-drop-target-8", "label": "Lower right drop target 8", "type": "leaf", "drop": True,
		"printed": "LOWER RIGHT DROP TARGET (8)", "matrix": "LOW. R. D.T. #8",
		"notes": "Target 8 of the lower-right three-bank. Closed while down; spots number 8 (lamps 36 and 60)."},
	32: {"id": "switch.lower-right-drop-target-7", "label": "Lower right drop target 7", "type": "leaf", "drop": True,
		"printed": "LOWER RIGHT DROP TARGET (7)", "matrix": "LOW. R. D.T. #7",
		"notes": "Target 7, the highest of the lower-right three-bank. Closed while down; spots number 7 (lamps 20 and 11). Closed last, it completes the bank and the ROM fires public output 9, the bank reset."},
	33: {"id": "switch.outhole", "label": "Out-hole", "type": "leaf", "initial_active": True,
		"printed": "OUT-HOLE", "matrix": "OUT-HOLE",
		"notes": "Single-ball out-hole below the flippers. The known-working scripts start the game with the ball on it; the ROM repeats the out-hole kick and the three bank resets while it stays closed."},
	34: {"id": "switch.saucer", "label": "Top eject pocket (saucer)", "type": "leaf",
		"printed": "SAUCER, EJECT.", "matrix": "SAUCER",
		"notes": "Switch under the top-left eject pocket at the end of the left loop. Held closed while a ball sits in it; the ROM answers with public output 10, the saucer eject (retained run). "
			"Scores 5,000 for each lit letter and an additional 35,000 when BIG-GAME is made (manual); 35,000 in the retained run with the letters already collected."},
	35: {"id": "switch.right-outlane", "label": "Right outlane", "type": "leaf",
		"printed": "RIGHT OUT-LANE", "matrix": "RIGHT OUTLANE",
		"notes": "Right outlane, the extra-ball lane (manual; lamp 38). Scored 10,000 in the retained gameplay run."},
	36: {"id": "switch.left-outlane", "label": "Left outlane", "type": "leaf",
		"printed": "LEFT OUT-LANE", "matrix": "LEFT OUTLANE",
		"notes": "Left outlane, the special lane (lamp 22, SPECIAL OUTLANE). Scored 10,000 in the retained gameplay run."},
	37: {"id": "switch.top-10-point-switches", "label": "Top 10-point switches (two)", "type": "leaf", "pulse": True, "quantity": 2,
		"printed": "TOP TWO 10-PTS.", "matrix": "TOP(2) 10 PTS.",
		"notes": "Two contacts on one address: the switch table prints `TOP TWO 10-PTS.`, the matrix sheet `TOP(2) 10 PTS.`, and the location drawing has two leaders numbered 37 that end on the guides either side of the top lanes. Each closure scores 10."},
	38: {"id": "switch.top-right-roll-over-button", "label": "Top right roll-over button", "type": "button",
		"printed": "TOP RIGHT R.O. BUTTON", "matrix": "TOP-R. R.O.B.",
		"notes": "Highest of the three star roll-over buttons down the right side. Scores 100, and 2,000 when Z is lit (manual); 2,000 in the retained run with card Z selected. The matrix sheet draws a capacitor across the contact."},
	39: {"id": "switch.right-middle-roll-over-button", "label": "Right middle roll-over button", "type": "button",
		"printed": "TOP RIGHT MID. R.O. BUTTON", "matrix": "R. MID. R.O.B.",
		"notes": "Middle of the three right-side star roll-over buttons. Scores 100, and 2,000 when Z is lit. The matrix sheet draws a capacitor across the contact."},
	40: {"id": "switch.right-lower-roll-over-button", "label": "Right lower roll-over button", "type": "button",
		"printed": "TOP RIGHT LOWER R.O. BUTTON", "matrix": "R. LOWER R.O.B.",
		"notes": "Lowest of the three right-side star roll-over buttons. Scores 100, and 2,000 when Z is lit. The matrix sheet draws a capacitor across the contact."},
}

# Flipper buttons: PinMAME synthetic switches 81-84 (FLIP_SW(FLIP_L)): right 82, left 84; 81/83 are the generic upper positions.
FLIPPER_BUTTONS = {
	82: ("switch.right-flipper-button", "Right flipper button (both right flippers)", "flipper.button.right", "R", "A3J2-1"),
	84: ("switch.left-flipper-button", "Left flipper button (both left flippers)", "flipper.button.left", "BLU", "A3J2-2"),
}
UNUSED_FLIPPER_POSITIONS = {
	81: ("switch.upper-right-flipper-position", "Upper right flipper button position (no separate button)"),
	83: ("switch.upper-left-flipper-position", "Upper left flipper button position (no separate button)"),
}

# --- Solenoids ----------------------------------------------------------------------------------------------------------
#
# The ROM's own solenoid test pulses physical drivers 1-19 in order and shows each number on the player displays; the public addresses that
# fire are, in that order: 2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18 (retained solenoid-test run).

SELF_TEST_ORDER = (2, 1, 6, 7, 3, 4, 5, 8, 11, 12, 14, 13, 9, 10, 19, 15, 17, 20, 18)
PHYSICAL_TO_PUBLIC = {number: address for number, address in enumerate(SELF_TEST_ORDER, start=1)}

# Solenoid Identification table (manual page 20), by printed number.
PRINTED_SOLENOIDS = {
	1: "LOWER LEFT THUMPER", 2: "TOP THUMPER", 3: "KNOCKER", 4: "LEFT DROP TARGET", 5: "LOWER RIGHT THUMPER", 6: "LEFT SLING-SHOT", 7: "RIGHT SLING-SHOT",
	8: "UPPER RIGHT DROP TARGET", 9: "OUT-HOLE", 10: "OPEN", 11: "OPEN", 12: "OPEN", 13: "LOWER RIGHT DROP TARGET", 14: "SAUCER-EJECT",
	15: "FLIPPERS (RIGHT & LEFT)", 16: "OPEN", 17: "OPEN", 18: "OPEN", 19: "COIN LOCK-OUT",
}

SOLENOIDS: dict[int, dict[str, Any]] = {
	1: {"id": "device.top-thumper-bumper", "label": "Top thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "G-R", "conn": "A3J2-4", "anchor": "bumper-top",
		"notes": "Printed solenoid 2 (TOP THUMPER), fired by the ROM when the top thumper switch (public 9) closes."},
	2: {"id": "device.lower-left-thumper-bumper", "label": "Lower left thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "W-O", "conn": "A3J2-9", "anchor": "bumper-lower-left",
		"notes": "Printed solenoid 1 (LOWER LEFT THUMPER; the Solenoid Driver Schematic's J2 table calls it LEFT THUMPER), fired when switch 10 closes."},
	3: {"id": "device.lower-right-thumper-bumper", "label": "Lower right thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "Y-BLU", "conn": "A3J2-10", "anchor": "bumper-lower-right",
		"notes": "Printed solenoid 5 (LOWER RIGHT THUMPER; the Solenoid Driver Schematic calls it RIGHT THUMPER), fired when switch 11 closes."},
	4: {"id": "device.left-slingshot", "label": "Left slingshot", "kind": "coil", "part": "J-27-1500", "wire": "B-BLU", "conn": "A3J2-11", "anchor": "sling-left",
		"notes": "Printed solenoid 6, fired when the left slingshot switch (public 12) closes."},
	5: {"id": "device.right-slingshot", "label": "Right slingshot", "kind": "coil", "part": "J-27-1500", "wire": "O-W", "conn": "A3J2-12", "anchor": "sling-right",
		"notes": "Printed solenoid 7, fired when the right slingshot switch (public 13) closes."},
	6: {"id": "device.knocker", "label": "Knocker", "kind": "coil", "part": "N-26-1200", "wire": "B-Y", "conn": "A3J2-5", "cabinet": True, "roles": ["cabinet.knocker"],
		"notes": "Printed solenoid 3; the solenoid location page lists `3- KNOCKER` among the solenoids not on the playfield, and Figure 1 draws it in the cabinet. The Solenoid Driver Schematic prints `KNOCKER (B-Y)` on J2 pin 5 and the cabinet sheet `A3J2-5 (B-Y)`."},
	7: {"id": "device.top-left-bank-reset", "label": "Top left drop-target bank reset", "kind": "coil", "part": "B-27-2300", "wire": "BRN-Y", "conn": "A3J1-5", "anchor": "bank-top-left",
		"notes": "Printed solenoid 4 (LEFT DROP TARGET; the playfield sheet `LEFT 3-BANK D. TARG.`). Fired at game start, after every drain and when the bank's last target closes in the retained gameplay run."},
	8: {"id": "device.top-right-bank-reset", "label": "Top right drop-target bank reset", "kind": "coil", "part": "B-27-2300", "wire": "B-Y", "conn": "A3J5-10", "anchor": "bank-top-right",
		"notes": "Printed solenoid 8 (UPPER RIGHT DROP TARGET; the Solenoid Driver Schematic `TOP R. DROP TARG. (B-Y)`, the playfield sheet `TOP R. 3-BANK D. TARG.`). Fired at game start, after every drain and when the bank's last target closes."},
	9: {"id": "device.lower-right-bank-reset", "label": "Lower right drop-target bank reset", "kind": "coil", "part": "B-27-2300", "wire": "O-B", "conn": "A3J5-12", "anchor": "bank-lower-right",
		"notes": "Printed solenoid 13 (LOWER RIGHT DROP TARGET; the Solenoid Driver Schematic `LOW-R. DR. TARG. (O-B)`, the playfield sheet `3-BANK D. TARG. LOWER R.` on `A3-J5-12 (O-B)`). Fired at game start, after every drain and when the bank's last target closes."},
	10: {"id": "device.saucer-eject", "label": "Saucer eject", "kind": "coil", "part": "J-28-2300", "wire": "B", "conn": "A3J5-11", "anchor": "saucer",
		"notes": "Printed solenoid 14 (SAUCER-EJECT; parts list `Saucer Eject J-28-2300`). Fires when the saucer switch (public 34) closes in the retained gameplay run."},
	11: {"id": "device.out-hole-kicker", "label": "Out-hole kicker", "kind": "coil", "part": "J-26-1000", "wire": "O-R", "conn": "A3J5-9", "anchor": "outhole",
		"notes": "Printed solenoid 9 (OUT-HOLE; parts list `Outhole Kicker (1) J-26-1000`). Fired when a game starts and after every drain; the ROM repeats the kick while the out-hole switch (public 33) stays closed."},
	12: {"id": "device.unused-solenoid-10", "label": "Unused solenoid driver 10", "kind": "coil", "phys": 10, "unused": True,
		"notes": "Printed OPEN. The Solenoid Driver Schematic prints OPEN on J5 pins 15, 13, 14 and 8 for the momentary drivers 10, 11, 12 and 16."},
	13: {"id": "device.unused-solenoid-12", "label": "Unused solenoid driver 12", "kind": "coil", "phys": 12, "unused": True, "notes": "Printed OPEN."},
	14: {"id": "device.unused-solenoid-11", "label": "Unused solenoid driver 11", "kind": "coil", "phys": 11, "unused": True, "notes": "Printed OPEN."},
	15: {"id": "device.unused-solenoid-16", "label": "Unused solenoid driver 16", "kind": "coil", "phys": 16, "unused": True, "notes": "Printed OPEN."},
	17: {"id": "device.unused-continuous-driver-17", "label": "Unused continuous driver 17", "kind": "relay", "phys": 17, "unused": True,
		"notes": "Printed OPEN in the Solenoid Identification table, and the parts list names no relay. The Solenoid Driver Schematic wires its transistor (Q17, input PB4 on J4 pin 11, [Y-W]) to J5 pin 7 and labels the line "
			"`GEN. ILLUM. RELAY`, but no relay appears anywhere else in this game's documents: the playfield sheet feeds `GEN. ILLUM` straight from A2J1-8 (6 VAC) to A2J1-1, and the transformer and wiring sheets take the backbox "
			"general illumination straight from the transformer. The ROM drives the output only in the power-up initialisation pulse it gives all four continuous lines and in its own burn-in and solenoid tests; it stays off "
			"in attract mode, play, drain, tilt, game over and slam in the retained runs. With the manual and the parts list against the one label, it stays unused, as the same kind of solenoid-sheet label does on Star Gazer. "
			"Award events (replay, special, extra ball) were not exercised, because PinMAME's default option switches disable those awards."},
	18: {"id": "device.coin-lockout", "label": "Coin lock-out coil", "kind": "coil", "part": "C-36-5300", "wire": "Y-W", "conn": "A3J2-8", "cabinet": True, "roles": ["cabinet.coin-door"],
		"notes": "Printed solenoid 19 (COIN LOCK-OUT), a continuous output: the ROM energizes it from the end of the power-up test in the retained runs, as the operating text says. The cabinet sheet and the Solenoid Driver Schematic both print J2 pin 8 [Y-W]."},
	19: {"id": "device.flipper-enable-relay", "label": "Flipper enable relay", "kind": "relay", "wire": "Y-W", "conn": "A3J3-5", "internal": True, "roles": ["internal.flipper-enable"],
		"notes": "Printed solenoid 15 (FLIPPERS (RIGHT & LEFT)), a continuous output through driver Q15 (input PB6, `FLIPPER DISABLE`) and the `FLIPPER ENABLE RELAY` (CR20, 43 VDC, J3 pin 5 `To A2J3-8 [Y-W]`). "
			"The ROM raises it when a game starts, drops it when a tilt closes switch 7 and at game over in the retained runs."},
	20: {"id": "device.continuous-driver-18", "label": "Continuous driver 18 (no documented load)", "kind": "relay", "phys": 18, "availability": "unknown",
		"notes": "Printed OPEN in the Solenoid Identification table, and the Solenoid Driver Schematic wires its transistor (Q18, input PB7 on J4 pin 10, [Y-R]) only to pins marked N/U (J5 pin 3, J2 pin 15 and J3 pin 9). "
			"The ROM nevertheless drives it outside the diagnostics: in attract mode it holds public 20 on for about 1.5 s each time the four player displays flash `7777777` (retained runs). "
			"Nothing in this game's documents explains that output, so availability stays unknown rather than unused."},
}

FLIPPERS = {
	46: {"id": "device.right-flippers", "label": "Right flippers (lower and upper)", "wire": "O", "conn": "A3J1-9", "button_wire": "R", "button_conn": "A3J2-1", "side": "right", "power": 45},
	48: {"id": "device.left-flippers", "label": "Left flippers (lower and upper)", "wire": "G", "conn": "A3J1-8", "button_wire": "BLU", "button_conn": "A3J2-2", "side": "left", "power": 47},
}

# --- Lamps -------------------------------------------------------------------------------------------------------------------
#
# Public lamp address = 16 * k + a + 1 for decoder U<k+1> output S<a>; each output line's resistor R<n> ends at SCR Q<n>. Both tables below are this
# game's Lamp Driver Schematic (12B-432-S-121, BIG GAME, 11-15-79).

DECODER = {
	0: [14, 12, 13, 8, 9, 10, 11, 4, 1, 2, 3, 7, 16, 5, 6],
	1: [29, 27, 28, 35, 34, 22, 26, 25, 24, 17, 23, 21, 15, 18, 19],
	2: [36, 38, 44, 49, 48, 37, 32, 20, 42, 41, 40, 39, 33, 30, 31],
	3: [57, 50, 51, 54, 55, 60, 59, 58, 56, 46, 52, 53, 47, 43, 45],
}
LAMP_TO_Q = {16 * k + a + 1: q for k, qs in DECODER.items() for a, q in enumerate(qs)}

# jack -> {pin: SCR}. The J1 rows that carry Q24 and Q23 print pin numbers that collide with other J1 rows (see the excerpt). Q24's flat-topped
# figure is read as pin 5, where the lamp list prints its one load ("M"); Q23's J1 pin is left out, because no lamp-list row uses it.
LDA_CONNECTORS = {
	"J1": {18: 14, 19: 12, 17: 13, 23: 8, 14: 9, 15: 10, 16: 11, 28: 4, 24: 1, 25: 2, 26: 3, 27: 7, 1: 29, 9: 27, 8: 28, 3: 35, 2: 34, 10: 22,
		7: 26, 6: 25, 5: 24, 11: 17, 13: 20, 12: 21},
	"J2": {21: 3, 13: 7, 22: 16, 16: 5, 14: 6, 8: 23, 12: 21, 23: 15, 20: 18, 15: 19, 11: 33, 6: 30, 2: 31, 9: 40, 4: 39, 5: 52, 10: 47, 7: 43, 1: 45, 3: 53},
	"J3": {26: 36, 25: 38, 19: 44, 17: 49, 16: 48, 23: 37, 27: 32, 21: 42, 20: 41, 22: 40, 24: 39, 1: 57, 12: 50, 15: 51, 11: 54, 9: 55, 3: 60, 4: 59,
		2: 58, 10: 56, 18: 46, 13: 52, 14: 53},
}

# The Lamp Driver Schematic's typed list, in printed order: description | wire | jack | pin. The playfield wiring diagram's list is the same rows
# without GAME OVER, HIGH SCORE TO DATE, MATCH and TILT, and prints `PUR` where this list prints `-PUR-`.
LAMP_LIST_TEXT = """"B"|W-O|J3|20
"I"|B-O|J1|11
"G"|PUR-B|J1|25
"G"|GREY-B|J3|10
"A"|B-G|J3|21
"M"|BLU-O|J1|5
"E"|BRN-BLU|J1|24
BONUS, RESERVE|R-Y|J3|25
BONUS, EXTRA (2K/LINE)|G-R|J3|1
EXTRA BALL|BLU-W|J2|7
EXTRA BALL, OUT-LANE|W-GREY|J3|23
GAME OVER|GREY-W|J2|11
HIGH SCORE TO DATE|GREY-O|J2|22
LEFT BANK-TARG. 25,000|BLACK|J3|26
LEFT S.U. TARG. 5,000|W-R|J3|9
LOWER R. BANK-TARG. 25,000|BRN-B|J1|18
MATCH|GREY-Y|J2|1
RIGHT SPIN. TARG. 1,000|O-G|J2|20
TOP R.O.W. "I" 5,000|GREY-Y|J1|15
TOP R. BANK TARG. 25,000|BLU-R|J1|1
SHOOT AGAIN|GREY-R|J2|23
SPECIAL|-Y-|J2|6
SPECIAL OUTLANE|GREY-BLU|J1|10
TILT|GREY-B|J2|10
"X" & LEFT SPIN. TARG.|R-B|J3|16
"X-1"|G-R|J3|12
"X-2"|-PUR-|J1|17
"X-3"|G-B|J1|8
"X-4"|B-R|J3|19
"X-5"|W-B|J3|15
"X-6"|BLU-W|J1|23
"X-7"|R-G|J1|3
"X-8"|Y-BLU|J3|17
"X-9"|WHITE|J3|11
"Y"|PUR-W|J1|2
"Y-1"|W-BLU|J1|13
"Y-2"|BRN-R|J1|6
"Y-3"|Y-B|J3|2
"Y-4"|R-W|J3|4
"Y-5"|BLACK|J1|16
"Y-6"|Y-G|J1|7
"Y-7"|B-W|J1|28
"Y-8"|GREEN|J3|3
"Y-9"|O-W|J3|27
"Z" & R. 1,000 WHEN LIT|GREY-O|J1|14
"Z-1"|GREY-G|J2|13
"Z-2"|PUR-BLU|J2|8
"Z-3"|GREY|J2|9
"Z-4"|R-BLU|J3|18
"Z-5"|W-Y|J2|12
"Z-6"|PUR-B|J2|4
"Z-7"|GREY-R|J2|21
"Z-8"|B-W|J2|3
"Z-9"|B-Y|J2|5
2X|GREY-G|J1|19
3X|GREY|J1|9"""
LAMP_LIST = [tuple(row.split("|")) for row in LAMP_LIST_TEXT.splitlines()]
BACKBOX_ROWS = {"GAME OVER", "HIGH SCORE TO DATE", "MATCH", "TILT"}

# public address -> (id, label). The curator checks each against the printed row its SCR reaches.
LAMP_NAMES: dict[int, tuple[str, str]] = {
	1: ("lamp.lower-right-bank-25000", "Lower right bank targets 25,000"),
	2: ("lamp.card-bonus-2x", "Card bonus multiplier 2X"),
	3: ("lamp.card-x-2", "Card X number 2"),
	4: ("lamp.card-x-6", "Card X number 6"),
	5: ("lamp.card-z-and-right-roll-overs-2000", "Card Z selected (and the right roll-over buttons' value)"),
	6: ("lamp.top-middle-lane-5000", "Top middle lane (I) 5,000"),
	7: ("lamp.card-y-5", "Card Y number 5"),
	8: ("lamp.card-y-7", "Card Y number 7"),
	9: ("lamp.letter-e", "Letter E (right return lane and eject-pocket lane)"),
	10: ("lamp.letter-g-big", "Letter G of BIG (top right lane and eject-pocket lane)"),
	11: ("lamp.card-z-7", "Card Z number 7"),
	12: ("lamp.card-z-1", "Card Z number 1"),
	13: ("lamp.high-score-to-date", "High score to date (backbox)"),
	17: ("lamp.top-right-bank-25000", "Top right bank targets 25,000"),
	18: ("lamp.card-bonus-3x", "Card bonus multiplier 3X"),
	19: ("lamp.card-x-3", "Card X number 3"),
	20: ("lamp.card-x-7", "Card X number 7"),
	21: ("lamp.card-y", "Card Y selected"),
	22: ("lamp.special-outlane", "Special (left outlane)"),
	23: ("lamp.card-y-6", "Card Y number 6"),
	24: ("lamp.card-y-2", "Card Y number 2"),
	25: ("lamp.letter-m", "Letter M (left return lane and eject-pocket lane)"),
	26: ("lamp.letter-i", "Letter I (top middle lane and eject-pocket lane)"),
	27: ("lamp.card-z-2", "Card Z number 2"),
	28: ("lamp.card-z-5", "Card Z number 5"),
	29: ("lamp.shoot-again", "Shoot again"),
	30: ("lamp.right-spinner-1000", "Right spinning target 1,000"),
	33: ("lamp.top-left-bank-25000", "Top left bank targets 25,000"),
	34: ("lamp.reserve-bonus", "27,000 reserve bonus"),
	35: ("lamp.card-x-4", "Card X number 4"),
	36: ("lamp.card-x-8", "Card X number 8"),
	37: ("lamp.card-x-and-left-spinner", "Card X selected (and the left spinning target's value)"),
	38: ("lamp.extra-ball-outlane", "Extra ball (right outlane)"),
	39: ("lamp.card-y-9", "Card Y number 9"),
	40: ("lamp.card-y-1", "Card Y number 1"),
	41: ("lamp.letter-a", "Letter A (stand-up target A and eject-pocket lane)"),
	42: ("lamp.letter-b", "Letter B (top left lane and eject-pocket lane)"),
	43: ("lamp.card-z-3", "Card Z number 3"),
	44: ("lamp.card-z-6", "Card Z number 6"),
	45: ("lamp.game-over", "Game over (backbox)"),
	46: ("lamp.special-side-lane", "Special (left side lane)"),
	49: ("lamp.extra-score-per-line", "Extra score when lit, for each completed line"),
	50: ("lamp.card-x-1", "Card X number 1"),
	51: ("lamp.card-x-5", "Card X number 5"),
	52: ("lamp.card-x-9", "Card X number 9"),
	53: ("lamp.left-standups-5000", "Left stand-up targets 5,000"),
	54: ("lamp.card-y-8", "Card Y number 8"),
	55: ("lamp.card-y-4", "Card Y number 4"),
	56: ("lamp.card-y-3", "Card Y number 3"),
	57: ("lamp.letter-g-game", "Letter G of GAME (stand-up target G and eject-pocket lane)"),
	58: ("lamp.card-z-4", "Card Z number 4"),
	59: ("lamp.card-z-9", "Card Z number 9"),
	60: ("lamp.card-z-8", "Card Z number 8"),
	61: ("lamp.tilt", "Tilt (backbox)"),
	62: ("lamp.extra-ball-side-lane", "Extra ball (left side lane)"),
	63: ("lamp.match", "Match (backbox)"),
}
# public address -> SCR, for the four SCRs that have no row in either list and that the ROM drives only in its own self-test sweeps.
UNUSED_LAMPS = {14: 5, 15: 6, 31: 19, 47: 31}
# The seven letter lamps light two inserts each: the letter at its own lane or target and the letter in the eject-pocket lane's B-I-G-G-A-M-E column.
TWO_INSERT_LAMPS = {9, 10, 25, 26, 41, 42, 57}

# --- Option switches -------------------------------------------------------------------------------------------------------
#
# `BIG GAME SWITCH ASSIGNMENT` (manual page 11) and the adjustment pages 12-15, with the two settings the March 1980 corrections sheet reverses.

DIPS: dict[int, str] = {
	1: "Coin chute No. 2 credits per coin, selector bit 1 (switches 1-5)",
	2: "Coin chute No. 2 credits per coin, selector bit 2",
	3: "Coin chute No. 2 credits per coin, selector bit 3",
	4: "Coin chute No. 2 credits per coin, selector bit 4",
	5: "Coin chute No. 2 credits per coin, selector bit 5",
	6: "High score feature (OFF = extra ball, ON = replay)",
	7: "Balls per game (OFF = 3, ON = 5)",
	8: "Background sound (corrected: ON = off, OFF = on)",
	9: "Coin chute No. 3 credits per coin, selector bit 1 (switches 9-13)",
	10: "Coin chute No. 3 credits per coin, selector bit 2",
	11: "Coin chute No. 3 credits per coin, selector bit 3",
	12: "Coin chute No. 3 credits per coin, selector bit 4",
	13: "Coin chute No. 3 credits per coin, selector bit 5",
	14: "Not used (N/U)",
	15: "High game to date feature, selector bit 1 (novelty, 1, 2 or 3 free games)",
	16: "High game to date feature, selector bit 2",
	17: "Extra ball bypass (OFF = no extra ball, ON = award extra ball)",
	18: "Maximum credits, selector bit 1 (10, 15, 25 or 40)",
	19: "Maximum credits, selector bit 2",
	20: "Credit display (ON = yes, OFF = no)",
	21: "Match feature (ON = on, OFF = off)",
	22: "Special replay limit (corrected: ON = 1 per ball, OFF = 1 per game)",
	23: "Card selection order (ON = X, Y, Z repeating; OFF = X, Y, Z, XY, Z, YZ, X, XZ repeating)",
	24: "Not used (N/U)",
	25: "Extra line 5,000 score lites on ball, selector bit 1 (2nd to 5th)",
	26: "Extra line 5,000 score lites on ball, selector bit 2",
	27: "Coin chute No. 1 credits per coin, selector bit 1 (switches 27-30)",
	28: "Coin chute No. 1 credits per coin, selector bit 2",
	29: "Coin chute No. 1 credits per coin, selector bit 3",
	30: "Coin chute No. 1 credits per coin, selector bit 4",
	31: "Special award, selector bit 1 (no award, extra ball, 100,000 points or replay)",
	32: "Special award, selector bit 2",
}
UNUSED_DIPS = {14, 24}

DISPLAYS = (
	("display.player-1-score", "Player 1 score, seven digits", 0, 1, 7),
	("display.player-2-score", "Player 2 score, seven digits", 1, 9, 7),
	("display.player-3-score", "Player 3 score, seven digits", 2, 17, 7),
	("display.player-4-score", "Player 4 score, seven digits", 3, 25, 7),
	("display.credits", "Credits, two digits", 4, 35, 2),
	("display.match-ball-in-play", "Match and ball in play, two digits", 5, 38, 2),
)

# --- Retained table geometry ---------------------------------------------------------------------------------------------
#
# Raw object centres of the retained `Big Game (Stern 1980) - redbone(MOD) v1.2.0.vpx` (vpxtool 0.33.3 extraction), in VPX units; the curator
# normalizes them by the table's own bounds (left 0, top 0, right 1093, bottom 2115). Walls use the mean of their drag points. Every value is
# re-read from the extraction by the retained-evidence test.

TABLE_WIDTH, TABLE_HEIGHT = 1093.0, 2115.0

OBJECTS: dict[str, tuple[str, float, float, str]] = {
	"sw4": ("Spinner", 105.97303, 613.8587, "Spinner.sw4.json"),
	"sw5": ("Spinner", 237.98723, 585.23645, "Spinner.sw5.json"),
	"Bumper1": ("Bumper", 592.4978, 573.2616, "Bumper.Bumper1.json"),
	"Bumper2": ("Bumper", 495.63977, 830.86426, "Bumper.Bumper2.json"),
	"Bumper3": ("Bumper", 691.8742, 792.125, "Bumper.Bumper3.json"),
	"LeftSlingshot": ("Wall", 194.70985000000002, 1390.2094, "Wall.LeftSlingshot.json"),
	"RightSlingshot": ("Wall", 801.122145, 1391.2150000000001, "Wall.RightSlingshot.json"),
	"sw14": ("HitTarget", 410.9239, 514.22235, "HitTarget.sw14.json"),
	"sw15": ("HitTarget", 375.9087, 565.0753, "HitTarget.sw15.json"),
	"sw16": ("HitTarget", 340.96442, 615.7311, "HitTarget.sw16.json"),
	"sw17": ("Trigger", 523.3721, 296.7718, "Trigger.sw17.json"),
	"sw18": ("Trigger", 621.1961, 297.3794, "Trigger.sw18.json"),
	"sw19": ("Trigger", 723.8807, 296.16425, "Trigger.sw19.json"),
	"sw20": ("HitTarget", 107.749146, 898.79376, "HitTarget.sw20.json"),
	"sw21": ("HitTarget", 107.749146, 957.8433, "HitTarget.sw21.json"),
	"sw22": ("HitTarget", 824.7185, 642.6622, "HitTarget.sw22.json"),
	"sw23": ("HitTarget", 813.1606, 582.46533, "HitTarget.sw23.json"),
	"sw24": ("HitTarget", 800.8002, 527.08417, "HitTarget.sw24.json"),
	"sw25": ("Trigger", 493.2196, 1125.9215, "Trigger.sw25.json"),
	"sw26": ("Trigger", 284.05237, 386.3172, "Trigger.sw26.json"),
	"sw27": ("Trigger", 48.384186, 931.33386, "Trigger.sw27.json"),
	"RightInlane": ("Trigger", 882.1079, 1401.385, "Trigger.RightInlane.json"),
	"LeftInlane": ("Trigger", 110.28987, 1404.3005, "Trigger.LeftInlane.json"),
	"sw30": ("HitTarget", 914.11664, 1041.4761, "HitTarget.sw30.json"),
	"sw31": ("HitTarget", 900.3117, 983.6872, "HitTarget.sw31.json"),
	"sw32": ("HitTarget", 886.50653, 926.2189, "HitTarget.sw32.json"),
	"Drain": ("Kicker", 609.7293, 2072.825, "Kicker.Drain.json"),
	"sw34": ("Kicker", 226.03802, 284.7403, "Kicker.sw34.json"),
	"RightOutlane": ("Trigger", 945.9349, 1414.5536, "Trigger.RightOutlane.json"),
	"LeftOutlane": ("Trigger", 48.041576, 1399.5382, "Trigger.LeftOutlane.json"),
	"sw37": ("Wall", 454.517165, 206.68982499999998, "Wall.sw37.json"),
	"sw37a": ("Wall", 800.3689325, 209.711835, "Wall.sw37a.json"),
	"sw38": ("Trigger", 863.70514, 387.00076, "Trigger.sw38.json"),
	"sw39": ("Trigger", 942.99744, 529.1798, "Trigger.sw39.json"),
	"sw40": ("Trigger", 937.52875, 689.13116, "Trigger.sw40.json"),
	"LeftFlipper": ("Flipper", 332.93555, 1754.5626, "Flipper.LeftFlipper.json"),
	"LeftFlipper1": ("Flipper", 210.12186, 1638.458, "Flipper.LeftFlipper1.json"),
	"RightFlipper": ("Flipper", 653.7246, 1754.563, "Flipper.RightFlipper.json"),
	"RightFlipper1": ("Flipper", 778.8231, 1638.4575, "Flipper.RightFlipper1.json"),
	"BallRelease": ("Kicker", 957.2603, 1808.2727, "Kicker.BallRelease.json"),
	"l1": ("Light", 782.3528, 1009.6625, "Light.l1.json"),
	"l2": ("Light", 417.27368, 1635.5374, "Light.l2.json"),
	"l3": ("Light", 345.36945, 1089.7943, "Light.l3.json"),
	"l4": ("Light", 403.3969, 1148.2119, "Light.l4.json"),
	"l5": ("Light", 494.50958, 1254.782, "Light.l5.json"),
	"l6": ("Light", 244.85243, 692.64, "Light.l6.json"),
	"l7": ("Light", 644.42725, 1089.7019, "Light.l7.json"),
	"l8": ("Light", 702.17725, 1148.2119, "Light.l8.json"),
	"l9": ("Light", 883.9157, 1276.5869, "Light.l9.json"),
	"l10": ("Light", 720.9394, 171.26675, "Light.l10.json"),
	"l11": ("Light", 495.28705, 1344.1721, "Light.l11.json"),
	"l12": ("Light", 552.4821, 1403.977, "Light.l12.json"),
	"l17": ("Light", 712.03326, 603.3456, "Light.l17.json"),
	"l18": ("Light", 558.74695, 1632.2876, "Light.l18.json"),
	"l19": ("Light", 403.34198, 1090.0443, "Light.l19.json"),
	"l20": ("Light", 289.20184, 1206.4619, "Light.l20.json"),
	"l21": ("Light", 644.9374, 994.4478, "Light.l21.json"),
	"l22": ("Light", 48.53491, 1296.7437, "Light.l22.json"),
	"l23": ("Light", 701.9374, 1089.9519, "Light.l23.json"),
	"l24": ("Light", 587.7972, 1206.8319, "Light.l24.json"),
	"l25": ("Light", 107.25317, 1278.2437, "Light.l25.json"),
	"l26": ("Light", 620.3632, 173.76677, "Light.l26.json"),
	"l27": ("Light", 552.9821, 1344.6996, "Light.l27.json"),
	"l28": ("Light", 438.28705, 1461.9496, "Light.l28.json"),
	"l32": ("Light", 224.83894, 927.9823, "Light.l32.json"),
	"l33": ("Light", 469.37167, 633.8456, "Light.l33.json"),
	"l34": ("Light", 494.41708, 994.6877, "Light.l34.json"),
	"l35": ("Light", 288.95184, 1148.9894, "Light.l35.json"),
	"l36": ("Light", 345.34198, 1206.2119, "Light.l36.json"),
	"l37": ("Light", 346.52695, 997.20795, "Light.l37.json"),
	"l38": ("Light", 947.5407, 1298.3384, "Light.l38.json"),
	"l39": ("Light", 587.9171, 1148.7119, "Light.l39.json"),
	"l40": ("Light", 644.67725, 1206.2118, "Light.l40.json"),
	"l41": ("Light", 178.0101, 969.90344, "Light.l41.json"),
	"l42": ("Light", 521.78705, 170.26678, "Light.l42.json"),
	"l43": ("Light", 438.03705, 1403.9221, "Light.l43.json"),
	"l44": ("Light", 494.4272, 1461.4221, "Light.l44.json"),
	"l46": ("Light", 66.66785, 1067.6658, "Light.l46.json"),
	"l47": ("Light", 489.89868, 1730.7474, "Light.l47.json"),
	"l48": ("Light", 160.5101, 718.64, "Light.l48.json"),
	"l49": ("Light", 493.2603, 1565.5913, "Light.l49.json"),
	"l50": ("Light", 288.95184, 1089.4619, "Light.l50.json"),
	"l51": ("Light", 345.67438, 1148.1844, "Light.l51.json"),
	"l52": ("Light", 403.3969, 1206.4344, "Light.l52.json"),
	"l53": ("Light", 201.59601, 149.0935, "Light.l53.json"),
	"l54": ("Light", 588.28705, 1089.4619, "Light.l54.json"),
	"l55": ("Light", 644.5472, 1148.4619, "Light.l55.json"),
	"l56": ("Light", 702.17725, 1206.7119, "Light.l56.json"),
	"l57": ("Light", 178.08896, 885.2457, "Light.l57.json"),
	"l58": ("Light", 438.3145, 1344.9496, "Light.l58.json"),
	"l59": ("Light", 494.75958, 1403.9496, "Light.l59.json"),
	"l60": ("Light", 552.4821, 1462.1996, "Light.l60.json"),
	"l62": ("Light", 65.01013, 780.31116, "Light.l62.json"),
	"l64": ("Light", 872.77936, 782.43024, "Light.l64.json"),
	"l65": ("Light", 102.47103, 96.09358, "Light.l65.json"),
	"l66": ("Light", 66.93171, 136.80423, "Light.l66.json"),
	"l67": ("Light", 65.22102, 189.53456, "Light.l67.json"),
	"l68": ("Light", 65.240685, 242.03456, "Light.l68.json"),
	"l69": ("Light", 65.240685, 295.78455, "Light.l69.json"),
	"l70": ("Light", 63.201347, 348.49524, "Light.l70.json"),
	"l71": ("Light", 64.24068, 403.24527, "Light.l71.json"),
	"l72": ("Light", 620.9394, 95.26679, "Light.l72.json"),
}

# Matrix switch -> the table object(s) its known-working script binds, plus what kind of point it is.
SWITCH_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	4: (["sw4"], None), 5: (["sw5"], None), 9: (["Bumper1"], None), 10: (["Bumper2"], None), 11: (["Bumper3"], None),
	12: (["LeftSlingshot"], "Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position."),
	13: (["RightSlingshot"], "Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position."),
	14: (["sw14"], None), 15: (["sw15"], None), 16: (["sw16"], None), 17: (["sw17"], None), 18: (["sw18"], None), 19: (["sw19"], None),
	20: (["sw20"], None), 21: (["sw21"], None), 22: (["sw22"], None), 23: (["sw23"], None), 24: (["sw24"], None),
	25: (["sw25"], None), 26: (["sw26"], None), 27: (["sw27"], None), 28: (["RightInlane"], None), 29: (["LeftInlane"], None),
	30: (["sw30"], None), 31: (["sw31"], None), 32: (["sw32"], None),
	33: (["Drain"], "Placed on the table's Drain kicker, its ball-collection proxy below the apron; the out-hole switch itself is not modelled. The shooter-lane BallRelease kicker is the virtual serve destination and is not used."),
	34: (["sw34"], None), 35: (["RightOutlane"], None), 36: (["LeftOutlane"], None),
	37: (["sw37", "sw37a"], "One placement per contact, each at the mean of the drag points of the rubber wall the script pulses (sw37 left of the top lanes, sw37a right of them)."),
	38: (["sw38"], None), 39: (["sw39"], None), 40: (["sw40"], None),
}
# Each side's end-of-stroke contacts are placed on the two flipper pivots of that side (lower, upper).
DIRECT_OBJECTS = {1: ["LeftFlipper", "LeftFlipper1"], 2: ["RightFlipper", "RightFlipper1"]}
# Solenoid -> object(s) and, for a projection, why. A bank reset is placed at the mean of its own three targets.
SOLENOID_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	1: (["Bumper1"], None), 2: (["Bumper2"], None), 3: (["Bumper3"], None),
	4: (["LeftSlingshot"], "Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	5: (["RightSlingshot"], "Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	7: (["sw14", "sw15", "sw16"], "Projected onto the top-left bank it resets: the mean of the table's own three target objects. The reset coil sits under the bank and has no object."),
	8: (["sw22", "sw23", "sw24"], "Projected onto the top-right bank it resets: the mean of the table's own three target objects."),
	9: (["sw30", "sw31", "sw32"], "Projected onto the lower-right bank it resets: the mean of the table's own three target objects."),
	10: (["sw34"], None),
	11: (["Drain"], "Placed on the table's Drain kicker, the ball-collection proxy where the ball enters the out-hole; the out-hole coil is not modelled."),
}
FLIPPER_OBJECTS = {46: ["RightFlipper", "RightFlipper1"], 48: ["LeftFlipper", "LeftFlipper1"]}

# Public lamp -> the light object(s) at the insert(s) its printed row names (or, where no row names an insert, the one the script binds), and a note
# where the retained script binds the number differently.
LAMP_OBJECTS: dict[int, list[str]] = {
	1: ["l1"], 2: ["l2"], 3: ["l3"], 4: ["l4"], 5: ["l5", "l64"], 6: ["l72"], 7: ["l7"], 8: ["l8"], 9: ["l9", "l71"], 10: ["l10", "l67"], 11: ["l11"], 12: ["l12"],
	17: ["l17"], 18: ["l18"], 19: ["l19"], 20: ["l20"], 21: ["l21"], 22: ["l22"], 23: ["l23"], 24: ["l24"], 25: ["l25", "l70"], 26: ["l26", "l66"], 27: ["l27"], 28: ["l28"],
	29: ["l47"], 30: ["l6"], 33: ["l33"], 34: ["l34"], 35: ["l35"], 36: ["l36"], 37: ["l37", "l48"], 38: ["l38"], 39: ["l39"], 40: ["l40"],
	41: ["l41", "l69"], 42: ["l42", "l65"], 43: ["l43"], 44: ["l44"], 46: ["l46"], 49: ["l49"], 50: ["l50"], 51: ["l51"], 52: ["l52"], 53: ["l32", "l53"],
	54: ["l54"], 55: ["l55"], 56: ["l56"], 57: ["l57", "l68"], 58: ["l58"], 59: ["l59"], 60: ["l60"], 62: ["l62"],
}
LAMP_TABLE_NOTES: dict[int, str] = {
	5: ("The second placement is the `100 / 2.000 WHEN LIT` insert beside the right roll-over buttons (table light l64), which the row's `R. 1,000 WHEN LIT` names. The retained script binds that light "
		"to lamp 34 (the reserve bonus) instead, a defect of the table: in the retained gameplay run the right roll-over buttons scored their lit 2,000 while card Z (this lamp) was on and lamp 34 was off."),
	6: ("Placed on the `5.000 WHEN LIT` insert above the middle top lane (table light l72), which the row `TOP R.O.W. \"I\" 5,000` names. The retained script does not drive that light from lamp 6; it lights it "
		"itself whenever lamps 10, 26 and 42 (B, I, G) are all on, the condition under which the ROM turns lamp 6 on, and it binds lamp 6 to the two spinner inserts instead (lights l6 and l48), a defect of the table."),
	30: ("Placed on the `100 OR 1000 WHEN LIT` insert beside the right spinning target (table light l6), which the row `RIGHT SPIN. TARG. 1,000` names; the retained script binds that light to lamp 6. "
		"The script binds lamp 30 to l30, a glow under the top-left roll-over button (not a bulb light), which is not placed; no printed row names a lamp at that button."),
	37: ("The second placement is the `200 OR 2000 WHEN LIT` insert beside the left spinning target (table light l48), which the row `\"X\" & LEFT SPIN. TARG.` names. The retained script binds that light to lamp 6, "
		"a defect of the table: in the retained gameplay run the left spinner scored its lit 2,000 while card X (this lamp) was on and lamp 6 was off."),
	53: ("The first placement is the stand-up targets' `5,000` insert the row names (table light l32). The second is the `15.000 WHEN LIT` insert beside the eject pocket (table light l53), which no printed row "
		"names; it rests on the retained script's binding of lamp 53 alone, which the ROM does not contradict (the pocket's extra award comes with this lamp), so the bulb quantity is not asserted."),
	29: "Placed on the playfield's SHOOT AGAIN insert between the flippers (table light l47); the script also writes this number to a backglass text box, and the backglass prints SHOOT AGAIN.",
}
