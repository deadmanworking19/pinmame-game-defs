"""Reviewed Nine Ball (Stern, 1980) device data, kept apart from the builder so both stay readable.

Every number below was read from this game's own manual and four-sheet schematic set, or observed in a retained harness run; none is
carried from a sister machine. Where a Stern MPU-200 board drawing is shared with other games, this game's own copy of the sheet was read.
"""

from __future__ import annotations

from typing import Any

# --- Drivers ---------------------------------------------------------------------------------------------------------

_SAME_HARDWARE = ("Identical INITGAME data to the production driver (GEN_STMPU200, seven-digit dispst7 displays, FLIP_SW(FLIP_L), no extra lamp columns, "
	"Stern ST300 sound board, input_ports_st), so the controller inventory is unchanged.")

DRIVERS: dict[str, tuple[str, str, str, str | None, str]] = {
	"nineball": (
		"Nine Ball", "1980", "Stern", None,
		"Production ROM set (U1, U2, U5 and U6) and the reference for this definition: GEN_STMPU200, seven-digit dispst7 displays, FLIP_SW(FLIP_L), Stern ST300 sound board. "
		"Every diagnostic and gameplay harness run boots this driver.",
	),
	"ninebafp": (
		"Nine Ball (Free Play)", "1980", "Stern", "nineball",
		"Free-play build of the production ROM: the same U1 and U5 images and free-play U2 and U6. " + _SAME_HARDWARE + " A retained harness run of it fires the same public "
		"outputs as nineball for the slingshots, pop bumper, top dead bumper, kick-out hole and flipper buttons; its drain and tilt responses are not attributed, "
		"because the run's unmodelled knock-down targets keep the ROM retrying public 9 through them.",
	),
	"ninebala": (
		"Nine Ball (Ball handling MOD beta18)", "2020", "Stern / Idleman", "nineball",
		"Community ball-handling modification (beta 18) for the same hardware. " + _SAME_HARDWARE + " It changes the ROM program only; no ROM set for it is in the authorized library, so no harness run was made.",
	),
	"ninebalb": (
		"Nine Ball (modified rules rev. 85)", "2007", "Stern / Oliver", "nineball",
		"Community rules revision 85 in one 32 KB ROM image for the same hardware. " + _SAME_HARDWARE + " The PinMAME source notes that a two-ball multiball flashes the 2X "
		"multiplier and doubles all scores, a three-ball multiball flashes 4X and quadruples them, the self test is incomplete and it is free play only. In a retained harness run "
		"it fires the same public outputs as nineball for the slingshots, pop bumper, top dead bumper and flipper buttons, but it ejects the kick-out hole at once, and it leaves "
		"the coin lockout (public 18) de-energized after the power-up pulse.",
	),
	"ninebalc": (
		"Nine Ball (Ball handling MOD beta19)", "2021", "Stern / Idleman", "nineball",
		"Community ball-handling modification (beta 19) for the same hardware. " + _SAME_HARDWARE + " It changes the ROM program only; no ROM set for it is in the authorized library, so no harness run was made.",
	),
	"ninebald": (
		"Nine Ball (Gameplay MOD beta21)", "2021", "Stern / Idleman", "nineball",
		"Community gameplay modification (beta 21) for the same hardware. " + _SAME_HARDWARE + " It changes the ROM program only; no ROM set for it is in the authorized library, so no harness run was made.",
	),
}

# --- Cabinet and service inputs ---------------------------------------------------------------------------------------

SERVICE_SWITCHES: dict[int, dict[str, Any]] = {
	-7: {
		"id": "switch.self-test-button", "label": "Self Test button (coin door)", "roles": ["service.test"], "availability": "used",
		"location": "Inside the coin door",
		"notes": "The Self-Test button the manual's game self-diagnostic tests use. Public -7 drives the ROM's tests in the manual's order: in the retained runs the first accepted press starts "
			"the burn-in, the second the lamp test, the third the display test, the fourth the solenoid test and the fifth the switch test. In the retained solenoid-test run the ROM ignored "
			"the first press, made 27 s into the run, so that scenario repeats the press until the burn-in's first solenoid pulse appears.",
		"evidence": "manual-and-harness",
	},
	-6: {
		"id": "switch.cpu-diagnostic-button", "label": "CPU diagnostic input (MPU NMI)", "roles": ["service.diagnostic"], "availability": "optional",
		"location": "MPU module",
		"notes": "PinMAME routes public -6 to the CPU's NMI line (BY35_SWCPUDIAG). The manual names no button for it; the S33 memory-clear pushbutton is a separate contact, so the identity of "
			"the two is not assumed.",
		"evidence": "core",
	},
	-5: {
		"id": "switch.sound-diagnostic-button", "label": "Sound board diagnostic input", "roles": ["service.diagnostic"], "availability": "optional",
		"location": "Sound module",
		"notes": "PinMAME routes public -5 to the ST300 sound board's diagnostic input (BY35_SWSOUNDDIAG). The manual documents no such button on the C-605 sound board.",
		"evidence": "core",
	},
}

# --- Matrix switches ----------------------------------------------------------------------------------------------------
#
# Public address = strobe * 8 + return + 1 on the five-strobe by eight-return MPU matrix. The Switch I.D. page prints every row's strobe, wire and
# jack; the playfield sheet prefixes the MPU's J2 with A4.

STROBES = {0: ("W-R", "A4J2-1"), 1: ("BRN-W", "A4J2-2"), 2: ("W-BLU", "A4J2-3"), 3: ("W-Y", "A4J2-4"), 4: ("Y-R", "A4J2-5")}
CABINET_STROBE0 = ("R-Y", "J3-3")
RETURNS = {
	0: ("BRN", "A4J2-8"), 1: ("GREY", "A4J2-9"), 2: ("W-O", "A4J2-10"), 3: ("W-B", "A4J2-11"),
	4: ("W-G", "A4J2-12"), 5: ("W-BRN", "A4J2-13"), 6: ("BRN-Y", "A4J2-14"), 7: ("O", "A4J2-15"),
}
CABINET_RETURNS = {0: ("BLU", "J3-9"), 1: ("BRN-W", "J3-10"), 2: ("R-W", "J3-11"), 5: ("BLU-W", "J3-14"), 6: ("BLU-O", "J3-15"), 7: ("Y", "J3-16")}
NO_DIODE_SWITCHES = {1, 2, 3}
CAPACITOR_SWITCHES = {4, 17, 35}

# address -> spec. ``printed`` is the Switch I.D. table's description (manual PDF page 18), ``matrix`` the playfield sheet's cell (None where the
# sheet draws the contact without a label).
SWITCHES: dict[int, dict[str, Any]] = {
	1: {"id": "switch.coin-chute-1", "label": "Coin chute 1 (left)", "type": "other", "cabinet": True, "roles": ["cabinet.coin.1"], "printed": "CHUTE (LEFT)", "matrix": None,
		"notes": "Left coin chute. The location page lists `1 *LEFT CHUTE` among the switches not on the playfield, and the credit table calls it `SWITCH No. 1 (BLU) LEFT CHUTE`, the colour the Switch I.D. prints."},
	2: {"id": "switch.coin-chute-2", "label": "Coin chute 2 (center)", "type": "other", "cabinet": True, "roles": ["cabinet.coin.2"], "printed": "CHUTE (CENTER)", "matrix": None,
		"notes": "Center coin chute (`2 *CENTER CHUTE`; credit table `SWITCH No. 2 (BRN-WHITE) CENTER CHUTE`)."},
	3: {"id": "switch.coin-chute-3", "label": "Coin chute 3 (right)", "type": "other", "cabinet": True, "roles": ["cabinet.coin.3"], "printed": "CHUTE (RIGHT)", "matrix": None,
		"notes": "Right coin chute (`3 *RIGHT CHUTE`; credit table `SWITCH No. 3 (RED-WHITE) RIGHT CHUTE`, the Switch I.D.'s R-W)."},
	4: {"id": "switch.loop-roll-under", "label": "Loop roll-under", "type": "leaf", "pulse": True, "printed": "LOOP ROLL UNDER", "matrix": "LOOP ROLL UNDER",
		"notes": "The roll-under gate at the entrance of the top-left loop (playfield parts `Roll-Under Gate Assembly A-791`; location drawing leader 4). The manual: scores 3,000 and advances the loop target value; "
			"in the retained gameplay run it lit the next loop-value lamp."},
	5: {"id": "switch.spinner", "label": "Spinner", "type": "other", "pulse": True, "printed": "SPINNER", "matrix": "SPINNER",
		"notes": "The spinning target on the right side (`Spin Target Assembly A-792`; location drawing leader 5). Each rotation closes the contact once; each spin scores 100 or the highest lit spinner value (manual)."},
	6: {"id": "switch.credit-button", "label": "Credit (start) button", "type": "button", "cabinet": True, "roles": ["cabinet.start"], "printed": "CREDIT (START)BUTTON", "matrix": None,
		"notes": "Coin-door credit button. In the retained runs it starts a game from credits."},
	7: {"id": "switch.tilt", "label": "Tilt (roll tilt and pendulum)", "type": "tilt", "cabinet": True, "quantity": 2, "roles": ["cabinet.tilt"], "printed": "TILT", "matrix": None,
		"notes": "Shared matrix position for two normally open tilt contacts: the location page lists `7 ROLL-TILT` and `7 PENDULUM`, the installation page's ball tilt and plumb bob tilt. The installation "
			"page names a third normally open tilt switch, the `Panel tilt on bottom of playfield panel`; the location page lists no third contact on 7 and puts a `TILT BOARD` contact on the slam position 8, "
			"so whether the panel tilt is wired to 7 or is that slam contact is not settled by the manual, and only the two contacts the location page lists are counted. Closing public 7 in play "
			"drops the flipper enable output 19, fires the kick-out hole coil (8) and lights TILT (lamp 61) in the retained gameplay run."},
	8: {"id": "switch.slam", "label": "Slam (door and tilt board)", "type": "tilt", "cabinet": True, "roles": ["cabinet.slam-tilt"], "printed": "SLAM", "matrix": None,
		"notes": "Shared matrix position for the slam contacts: the location page lists `8 TILT BOARD` and `8 DOOR`, and the operating text says there is a slam switch on the front door and one on the tilt board and that an operator may add more, "
			"so no quantity is asserted. In the retained slam run, closing public 8 in play ends the game and the ROM repeats its power-up initialisation of the continuous outputs."},
	33: {"id": "switch.outhole", "label": "Outhole (right trough position)", "type": "leaf", "initial_active": True, "printed": "OUTHOLE", "matrix": "OUTHOLE",
		"notes": "Rightmost of the three trough switches under the apron (location drawing `37 36 33`, left to right), where a ball rests on the outhole kicker. The manual: entering the outhole collects the bonus. "
			"The known-working scripts start with three balls in the trough (33, 36 and 37 closed); the ROM repeats the outhole kick and the bank resets while 33 stays closed at a serve."},
	34: {"id": "switch.kick-out-hole", "label": "Left lane kick-out hole", "type": "leaf", "printed": "LFT. LANE KICK-OUT HOLE", "matrix": "L. LANE K-O-H HOLE",
		"notes": "Switch in the kick-out hole at the foot of the left lock lane (location drawing leader 34, below 38 and 39). The manual: spots all numbers, advances bonus by spotting the lit object and captures "
			"the ball after object 5 is lit. In the retained kick-out-spot run, with object 5 unlit, the ROM knocked down drop targets 7 to 1 one at a time, firing each target's coil only after the previous "
			"target's switch closed, then fired the kick-out (public 8), reset the eight-bank (17) and knocked the made object 1 down again. In the retained lock-lane run, with object 5 lit, it knocked down "
			"7, 6 and 5, kept the ball and served the next one from the outhole (7). Once the lane is full it fires public 8 each time 34 closes, three times in all, to release the three balls."},
	35: {"id": "switch.advance-spinner-target", "label": "Advance-spinner-to-end stand-up target", "type": "leaf", "pulse": True, "printed": "ADVANCE SPINNER TO END", "matrix": "ADV. SPINNER TO END",
		"notes": "Stand-up target at the top of the playfield (location drawing leader 35; `Stand-Up Target A-721-L1`). The manual: scores 7,000 and advances the spinner to its top value; the retained gameplay run lit all four spinner lamps."},
	36: {"id": "switch.middle-outhole", "label": "Middle trough position", "type": "leaf", "initial_active": True, "printed": "MID. OUTHOLE SWITCH", "matrix": "MID. OUTHOLE SW.",
		"notes": "Middle of the three trough switches under the apron; closed while a ball waits there."},
	37: {"id": "switch.left-outhole", "label": "Left trough position", "type": "leaf", "initial_active": True, "printed": "LFT. OUTHOLE SWITCH", "matrix": "L. OUTHOLE SW.",
		"notes": "Leftmost of the three trough switches under the apron; closed while a ball waits there. With 33 and 36 occupied, a drained ball stops here; in the retained game-over run, "
			"closing it in play ended the ball and the ROM fired the outhole kicker (7) and the bank resets (3, 4 and 17) to serve the next ball."},
	38: {"id": "switch.left-lane-middle", "label": "Left lane middle switch", "type": "leaf", "printed": "LFT. LANE MID. SWITCH", "matrix": "L. LANE MID. SW.",
		"notes": "Middle switch of the left lock lane, above the kick-out hole (location drawing leader 38), closed by a second ball resting behind the one held in the hole. The manual: spots all numbers, "
			"advances bonus by spotting the lit object (6-8) and captures the ball when another is captured in the kick-out hole. In the retained lock-lane run, with a ball held on 34, its closure made the "
			"ROM knock down drop targets 7 and 6 and serve the third ball from the outhole (7)."},
	39: {"id": "switch.left-lane-top", "label": "Left lane top switch", "type": "leaf", "printed": "LFT. LANE TOP SWITCH", "matrix": "L. LANE TOP SW.",
		"notes": "Top switch of the left lock lane (location drawing leader 39), closed by a third ball resting behind the other two. The manual: spots all numbers, advances bonus by spotting the lit object "
			"(6-8) and releases all three balls into play. In the retained lock-lane run, with balls on 34 and 38, its closure made the ROM knock down drop target 7, reset and re-knock the made objects 1-7, "
			"and then fire the kick-out hole (8) once for each of the three balls as each dropped onto 34."},
	40: {"id": "switch.shooter-lane", "label": "Ball shooter lane switch", "type": "leaf", "printed": "BALL SHOOTER LANE SWITCH", "matrix": "BALL SHOOTER LANE SW.",
		"notes": "Shooter-lane rollover; the manual: determines whether a ball is in the ball shooter lane."},
}
_DROP_ROWS = {1: 988, 2: 545, 3: 932, 4: 600, 5: 874, 6: 655, 7: 818, 8: 708}
for _object in range(1, 9):
	_bank = "lower" if _object % 2 else "upper"
	SWITCHES[8 + _object] = {
		"id": f"switch.drop-target-{_object}", "label": f"Drop target {_object} ({_bank} left four-bank)", "type": "leaf", "drop": True,
		"printed": f"DROP TARGET #{_object}", "matrix": f"D.T. #{_object}",
		"notes": f"Object {_object} of the left eight-target bank, which is two four-target banks on one reset coil: the feature text lists 10, 12, 14 and 16 as the upper left 4 bank and 9, 11, 13 and 15 "
			f"as the lower left 4 bank, and the location drawing numbers them 10, 12, 14, 16 and 15, 13, 11, 9 from the top. This target is in the {_bank} bank. Closed while the target is down. "
			+ ("It has an individual knock-down coil (public " + str(16 - _object) + "), with which the ROM spots it." if _object < 8 else "It is the one target of the eight with no knock-down coil (the parts list counts seven programmable drop-target coils)."),
	}
SWITCHES.update({
	17: {"id": "switch.top-dead-bumper", "label": "Top dead bumper", "type": "leaf", "pulse": True, "printed": "TOP DEAD BUMPER", "matrix": "TOP DEAD BUMPER",
		"notes": "Passive (dead) bumper at the upper right (`Dead Bumper A-578-2`; IPDB `Passive bumper (1)`). The manual: scores 500 and spots the lit object when the bumper is lit; "
			"in the retained gameplay run it fired object 1's knock-down coil (public 15)."},
	18: {"id": "switch.center-bank-left-target", "label": "Center three-bank left target", "type": "leaf", "drop": True, "printed": "TOP 3 BANK LFT. TARGET", "matrix": "TOP L. D.T.",
		"notes": "Left target of the center (top) three-target drop bank; an outer target for the WOW award (manual)."},
	19: {"id": "switch.center-bank-middle-target", "label": "Center three-bank middle target", "type": "leaf", "drop": True, "printed": "TOP 3 BANK MID. TARGET", "matrix": "TOP. MID. D.T.",
		"notes": "Middle target of the center three-target drop bank."},
	20: {"id": "switch.center-bank-right-target", "label": "Center three-bank right target", "type": "leaf", "drop": True, "printed": "TOP 3 BANK RT. TARGET", "matrix": "TOP R. D.T.",
		"notes": "Right target of the center three-target drop bank; an outer target for the WOW award (manual)."},
	21: {"id": "switch.loop-drop-target", "label": "Loop drop target", "type": "leaf", "drop": True, "printed": "LOOP DROP TARGET", "matrix": "LOOP D.T.",
		"notes": "Single drop target at the exit of the top-left loop (`1 Drop Target C-383-3`; location drawing leader 21). The manual: collects and resets the loop value. "
			"In the retained gameplay run its closure fires the loop target reset (public 20)."},
	22: {"id": "switch.right-bank-top-target", "label": "Right three-bank top target", "type": "leaf", "drop": True, "printed": "RT. 3 BANK TOP TARGET", "matrix": "R. TOP D.T.",
		"notes": "Top target of the right three-target drop bank; an outer target for the WOW award (manual)."},
	23: {"id": "switch.right-bank-middle-target", "label": "Right three-bank middle target", "type": "leaf", "drop": True, "printed": "RT. 3 BANK MID TARGET", "matrix": "R. MID. D.T.",
		"notes": "Middle target of the right three-target drop bank."},
	24: {"id": "switch.right-bank-bottom-target", "label": "Right three-bank bottom target", "type": "leaf", "drop": True, "printed": "RT. 3 BANK BOTTOM TARGET", "matrix": "R. BOT. D.T.",
		"notes": "Bottom target of the right three-target drop bank; an outer target for the WOW award (manual: the right bank's outer target is printed as 22 only)."},
	25: {"id": "switch.right-outlane", "label": "Right outlane", "type": "leaf", "printed": "RIGHT OUTLANE", "matrix": "R. OUTLANE",
		"notes": "The manual: scores 3,000, and collects and resets the loop value when lit."},
	26: {"id": "switch.left-outlane", "label": "Left outlane", "type": "leaf", "printed": "LEFT OUTLANE", "matrix": "L. OUTLANE",
		"notes": "The manual: scores 3,000, and collects and resets the loop value when lit; in the retained gameplay run the loop-value lamps reset to 10K."},
	27: {"id": "switch.right-return-lane", "label": "Right return lane", "type": "leaf", "printed": "RT. RETURN LANE", "matrix": "R. RETURN LANE",
		"notes": "The manual: scores 500, and spots the lit object and advances the bonus when lit; in the retained gameplay run it fired object 1's knock-down coil (public 15)."},
	28: {"id": "switch.left-return-lane", "label": "Left return lane", "type": "leaf", "printed": "LFT. RETURN LANE", "matrix": "L. RETURN LANE",
		"notes": "The manual: scores 500, and spots the lit object and advances the bonus when lit; in the retained gameplay run it fired object 1's knock-down coil (public 15)."},
	29: {"id": "switch.right-slingshot", "label": "Right slingshot", "type": "leaf", "pulse": True, "printed": "RIGHT SLINGSHOT", "matrix": "R. SLING SHOT",
		"notes": "Scores 10 (manual); the ROM fires public 1, the right slingshot coil, in the retained gameplay runs."},
	30: {"id": "switch.left-slingshot", "label": "Left slingshot", "type": "leaf", "pulse": True, "printed": "LEFT SLINGSHOT", "matrix": "L. SLING SHOT",
		"notes": "Scores 10 (manual); the ROM fires public 2, the left slingshot coil, in the retained gameplay runs."},
	31: {"id": "switch.pop-bumper", "label": "Pop bumper", "type": "leaf", "pulse": True, "printed": "POP BUMPER", "matrix": "POP BUMPER",
		"notes": "The single thumper bumper (`Thumper Bumper J-26-1200`). The manual: scores 100 or the highest lit spinner value; the ROM fires public 5, the pop bumper coil, in the retained gameplay runs."},
	32: {"id": "switch.left-lane-lower", "label": "Left lane lower switch", "type": "leaf", "printed": "LFT. LANE LOWER SWITCH", "matrix": "L. LANE LOW. SW.",
		"notes": "Rollover in the lower left lane beside the eight-target bank (location drawing leader 32). The manual: scores 3,000 and advances the loop target value; in the retained gameplay run it lit the next loop-value lamp."},
})

# Flipper buttons: PinMAME synthetic switches 81-84 (FLIP_SW(FLIP_L)): right 82, left 84; 81/83 are the generic upper positions.
FLIPPER_BUTTONS = {
	82: ("switch.right-flipper-button", "Right flipper button", "flipper.button.right", "R", "SDU J2-1"),
	84: ("switch.left-flipper-button", "Left flipper button", "flipper.button.left", "BLU", "SDU J2-2"),
}
UNUSED_FLIPPER_POSITIONS = {
	81: ("switch.upper-right-flipper-position", "Upper right flipper button position (no separate button)"),
	83: ("switch.upper-left-flipper-position", "Upper left flipper button position (no separate button)"),
}

# --- Solenoids ----------------------------------------------------------------------------------------------------------
#
# The ROM's own solenoid test pulses drivers 1-19 in order and shows each number on the player displays; the public addresses that fire are, in
# that order (retained solenoid-test run):
SELF_TEST_ORDER = (2, 1, 6, 7, 3, 4, 5, 8, 11, 12, 14, 13, 9, 10, 19, 15, 17, 20, 18)
PHYSICAL_TO_PUBLIC = {number: address for number, address in enumerate(SELF_TEST_ORDER, start=1)}

# `NINE BALL SOLENOID` identification table (manual PDF page 20): I.D. -> (transistor, jack, wire, description).
PRINTED_SOLENOIDS: dict[int, tuple[str, str, str, str]] = {
	1: ("Q1", "J2-9", "G-O", "LEFT SLINGSHOT"), 2: ("Q2", "J2-4", "G-BLU", "RIGHT SLINGSHOT"), 3: ("Q3", "J2-5", "G-B", "KNOCKER"), 4: ("Q4", "J1-5", "B-BLU", "OUTHOLE"),
	5: ("Q5", "J2-10", "G-Y", "RIGHT DROP BANK"), 6: ("Q6", "J2-11", "G-R", "TOP DROP BANK"), 7: ("Q7", "J2-12", "R-Y", "POP BUMPER"),
	8: ("Q8", "J5-10", "B-O", "LEFT LANE KICK-OUT HOLE"), 9: ("Q9", "J5-9", "R-BLU", "DROP TARGET #5"), 10: ("Q10", "J5-15", "O-W", "DROP TARGET #4"),
	11: ("Q11", "J5-14", "O-B", "DROP TARGET #2"), 12: ("Q12", "J5-13", "O-G", "DROP TARGET #3"), 13: ("Q13", "J5-12", "B-Y", "DROP TARGET #7"),
	14: ("Q14", "J5-11", "B-G", "DROP TARGET #6"), 15: ("Q15", "J3-5", "Y-W", "FLIPPER ENABLE-RELAY"), 16: ("Q16", "J5-8", "G-W", "DROP TARGET #1"),
	17: ("Q17", "J5-7", "O-R", "LEFT DROP BANK RESET"), 18: ("Q18", "J5-3", "R-W", "LOOP DROP TARGET"), 19: ("Q19", "J2-8", "Y-W", "COIN LOCK-OUT"),
}

# public address -> spec. ``object`` is the drop-target object a knock-down coil spots.
SOLENOIDS: dict[int, dict[str, Any]] = {
	1: {"id": "device.right-slingshot", "label": "Right slingshot", "kind": "coil", "part": "J-26-1600", "anchor": "RightSlingShot",
		"notes": "Fired when the right slingshot switch (public 29) closes in the retained gameplay runs."},
	2: {"id": "device.left-slingshot", "label": "Left slingshot", "kind": "coil", "part": "J-26-1600",
		"notes": "Fired when the left slingshot switch (public 30) closes in the retained gameplay runs."},
	3: {"id": "device.right-bank-reset", "label": "Right three-bank reset", "kind": "coil", "part": "B-27-2300",
		"notes": "Raises the right three-target drop bank. Fired at game start, after every drain, and once both three-banks are completely down (manual note 3 and the retained gameplay run)."},
	4: {"id": "device.center-bank-reset", "label": "Center (top) three-bank reset", "kind": "coil", "part": "B-27-2300",
		"notes": "Raises the center (top) three-target drop bank. Fired at game start, after every drain, and once both three-banks are completely down (manual note 3 and the retained gameplay run)."},
	5: {"id": "device.pop-bumper", "label": "Pop bumper", "kind": "coil", "part": "J-26-1200",
		"notes": "Fired when the pop bumper switch (public 31) closes in the retained gameplay runs. The retained script's callback for it is commented out; the table's bumper fires on its own hit."},
	6: {"id": "device.knocker", "label": "Knocker", "kind": "coil", "cabinet": True, "roles": ["cabinet.knocker"],
		"notes": "In the cabinet; no parts-list part number is printed for it."},
	7: {"id": "device.outhole-kicker", "label": "Outhole kicker", "kind": "coil", "part": "J-26-1200",
		"notes": "Kicks the ball resting on the outhole (public 33) into the shooter lane. Fired when a game starts and after every drain; the ROM repeats the kick while 33 stays closed (retained runs)."},
	8: {"id": "device.kick-out-hole", "label": "Left lane kick-out hole", "kind": "coil", "part": "J-28-2300",
		"notes": "Ejects the kick-out hole (switch 34); the parts list's `Lane Kicker` coil. In the retained runs it fires once the ROM has finished spotting the targets for an uncaptured ball there, "
			"three times to release the full lock lane after switch 39 closes, on a tilt, at game over, and in the power-up initialisation and after a slam."},
	9: {"id": "device.drop-target-7-knock-down", "label": "Drop target 7 knock-down coil", "kind": "coil", "part": "C1-34-3400", "object": 7},
	10: {"id": "device.drop-target-6-knock-down", "label": "Drop target 6 knock-down coil", "kind": "coil", "part": "C1-34-3400", "object": 6},
	11: {"id": "device.drop-target-5-knock-down", "label": "Drop target 5 knock-down coil", "kind": "coil", "part": "C1-34-3400", "object": 5},
	12: {"id": "device.drop-target-4-knock-down", "label": "Drop target 4 knock-down coil", "kind": "coil", "part": "C1-34-3400", "object": 4},
	13: {"id": "device.drop-target-3-knock-down", "label": "Drop target 3 knock-down coil", "kind": "coil", "part": "C1-34-3400", "object": 3},
	14: {"id": "device.drop-target-2-knock-down", "label": "Drop target 2 knock-down coil", "kind": "coil", "part": "C1-34-3400", "object": 2},
	15: {"id": "device.drop-target-1-knock-down", "label": "Drop target 1 knock-down coil", "kind": "coil", "part": "C1-34-3400", "object": 1},
	17: {"id": "device.eight-bank-reset", "label": "Left eight-target bank reset", "kind": "coil", "part": "B-24-1600",
		"notes": "A continuous-section driver (Q17, PIA PB4) used as a pulsed coil: it raises all eight left drop targets. Fired at game start, after every drain, and in the power-up pulse the ROM gives "
			"all four continuous lines (retained runs). Each time the lit object is made, the ROM fires it within about 35 ms of the target's switch closing and then re-knocks every object made so far, lowest "
			"first, with the individual knock-down coils (retained lock-lane run)."},
	18: {"id": "device.coin-lockout", "label": "Coin lock-out coil", "kind": "coil", "part": "C-36-5300", "cabinet": True, "roles": ["cabinet.coin-door"],
		"notes": "A continuous output (Q19, PIA PB5): the ROM energizes it from about 8.7 s after power-up in the retained runs and keeps it on in attract mode and play."},
	19: {"id": "device.flipper-enable-relay", "label": "Flipper enable relay", "kind": "relay", "internal": True, "roles": ["internal.flipper-enable"],
		"notes": "A continuous output through driver Q15 (PIA PB6, `FLIPPER DISABLE`) to the `FLIPPER ENABLE RELAY` (CR20, 43 VDC, J3 pin 5 `To A2J3-8 [Y-W]`). The ROM raises it when a game starts and drops it "
			"on a tilt and at game over (retained runs)."},
	20: {"id": "device.loop-drop-target-reset", "label": "Loop drop target reset", "kind": "coil",
		"notes": "A continuous-section driver (Q18, PIA PB7) used as a pulsed coil: it raises the single loop drop target (the solenoid table's `LOOP DROP TARGET`, the SDU sheet's `LOOP D.T.`). In the retained "
			"gameplay run, with the target held down, the ROM pulsed it about 2.6 s after switch 21 closed and once more about 1.3 s after the target was raised; it also pulsed once about 2.0 s after the "
			"right slingshot closure, about 4.2 s after the left outlane collected the loop value, which the run does not explain, and in the power-up pulse. The parts list names no coil for the single "
			"target, and its `Stand-Up Target J-26-1200` row matches no driver in the solenoid table, so no part number is asserted."},
}
for _address, _spec in SOLENOIDS.items():
	if "object" in _spec:
		_spec["notes"] = (f"Knocks down drop target {_spec['object']} (switch {8 + _spec['object']}) of the left bank, one of the seven `Drop Target (Programmable)` coils C1-34-3400. "
			f"In the retained kick-out-spot run the ROM fires it and waits for switch {8 + _spec['object']} to close before it fires the next target's coil; in the retained lock-lane run, once object "
			f"{_spec['object']} has been made or spotted, the ROM fires this coil again after every eight-bank reset to put the target back down.")

FLIPPERS = {
	46: {"id": "device.right-flipper", "label": "Right flipper", "wire": "O", "conn": "A3J1-9", "button_wire": "R", "button_conn": "SDU J2-1", "side": "right", "power": 45, "object": "RightFlipper"},
	48: {"id": "device.left-flipper", "label": "Left flipper", "wire": "G", "conn": "A3J1-8", "button_wire": "BLU", "button_conn": "SDU J2-2", "side": "left", "power": 47, "object": "LeftFlipper"},
}

# --- Lamps -------------------------------------------------------------------------------------------------------------------
#
# Public lamp address = 16 * k + a + 1 for decoder U<k+1> output S<a>; each output line's resistor R<n> ends at SCR Q<n> (the LDA-100 Lamp Driver
# schematic 12B-431S-128, sheet 4 of this game's set; its typed lamp list belongs to another game, so only the board's own wiring is read from it).
# The sheet crosses U2 S7/S8 to Q25/Q24 and U3/U4 S9 to Q41/Q46, and the retained lock-lane run confirms both crossings.

DECODER = {
	0: [14, 12, 13, 8, 9, 10, 11, 4, 1, 2, 3, 7, 16, 5, 6],
	1: [29, 27, 28, 35, 34, 22, 26, 25, 24, 17, 23, 21, 15, 18, 19],
	2: [36, 38, 44, 49, 48, 37, 32, 20, 42, 41, 40, 39, 33, 30, 31],
	3: [57, 50, 51, 54, 55, 60, 59, 58, 56, 46, 52, 53, 47, 43, 45],
}
LAMP_TO_Q = {16 * k + a + 1: q for k, qs in DECODER.items() for a, q in enumerate(qs)}

# `NINE BALL LDA LIGHT LOCATION` (schematic sheet 2, the playfield wiring diagram), in printed order: description | wire | jack | pin | transistor.
LAMP_LIST_TEXT = """BONUS TARGET 1|R-BLU|J3|18|Q46
BONUS TARGET 2|W-O|J3|20|Q41
BONUS TARGET 3|B-O|J1|11|Q17
BONUS TARGET 4|PUR-B|J1|25|Q2
BONUS TARGET 5 & CAPTURE BALL|GREY-B|J3|10|Q56
BONUS TARGET 6|B-G|J3|21|Q42
BONUS TARGET 7|BLU-O|J1|5|Q24
BONUS TARGET 8 & LFT. BANK|BRN-BLU|J1|24|Q1
BONUS TARGET 9|O|J1|14|Q9
DROP TARGET 1|BRN-B|J1|18|Q14
DROP TARGET 2|BLU-R|J1|1|Q29
DROP TARGET 3|B|J3|26|Q36
DROP TARGET 4|R-G|J3|1|Q57
DROP TARGET 5|GREY-G|J1|19|Q12
DROP TARGET 6|GREY|J1|9|Q27
DROP TARGET 7|R-Y|J3|25|Q38
DROP TARGET 8|G-R|J3|12|Q50
GAME OVER|O-G|J2|11|Q33
HIGH SCORE TO DATE|GREY-O|J2|22|Q16
L. BANK 7000 & R. OUTLANE|O-BLU|J2|23|Q15
L. RETURN LANE & SPOT NO.|BLU-W|J2|7|Q43
LOOP 10K|R-W|J3|4|Q59
LOOP 20K|B-W|J1|28|Q4
LOOP 30K|BRN-R|J1|6|Q25
LOOP 40K|W-BLU|J1|13|Q20
LOOP 177K|Y-B|J3|2|Q58
MATCH|GREY-Y|J2|1|Q45
MULTIPLIER 1X|B|J1|16|Q11
MULTIPLIER 2X|Y-G|J1|7|Q26
MULTIPLIER 4X|O-W|J3|27|Q32
R. BANK BOTTOM WOW|G-R|J2|14|Q6
R. BANK TOP WOW|G-W|J2|15|Q19
R. BANK 7000 & L. OUTLANE|G|J2|21|Q3
R. RETURN LANE & SPOT NO.|Y|J2|6|Q30
SHOOT AGAIN|GREY-R|J2|8|Q23
SPECIAL TARGET 2|PUR-W|J1|2|Q34
SPECIAL TARGET 3|R-B|J3|16|Q48
SPECIAL TARGET 4|B-O|J3|9|Q55
SPECIAL TARGET 5|GREY-Y|J1|15|Q10
SPECIAL TARGET 6|GREY-B|J1|10|Q22
SPECIAL TARGET 7|O-B|J3|23|Q37
SPECIAL TARGET 8|R|J3|3|Q60
SPINNER 1|GREY-G|J2|13|Q7
SPINNER 2|W-R|J2|12|Q21
SPINNER 3|PUR-B|J2|4|Q39
SPINNER 4|B-W|J2|3|Q53
SUPER BONUS|B|J2|16|Q5
TILT|GREY-BLU|J2|10|Q47
TOP DEAD BUMPER|O|J2|20|Q18
TOP BANK L. WOW|W-BLU|J2|9|Q40
TOP BANK R. WOW|G-B|J2|2|Q31
WOW TARGET 1|PUR|J1|17|Q13
WOW TARGET 2|W-O|J1|8|Q28
WOW TARGET 3|B-R|J3|19|Q44
WOW TARGET 4|W-B|J3|15|Q51
WOW TARGET 5|BLU-W|J1|23|Q8
WOW TARGET 6|G-O|J1|3|Q35
WOW TARGET 7|Y-BLU|J3|17|Q49
WOW TARGET 8|W|J3|11|Q54
1-8 LITES SPECIAL|B-Y|J2|5|Q52"""
LAMP_LIST = [tuple(row.split("|")) for row in LAMP_LIST_TEXT.splitlines()]
BACKBOX_ROWS = {"GAME OVER", "HIGH SCORE TO DATE", "MATCH", "TILT"}
# Rows naming two features on one output; the bulb count of each is not asserted.
TWO_FEATURE_ROWS = {"BONUS TARGET 5 & CAPTURE BALL", "BONUS TARGET 8 & LFT. BANK", "L. BANK 7000 & R. OUTLANE", "R. BANK 7000 & L. OUTLANE", "L. RETURN LANE & SPOT NO.", "R. RETURN LANE & SPOT NO."}


def _lamp_identity(description: str) -> tuple[str, str]:
	"""A stable id and a readable label for one printed LDA row."""
	special = {
		"BONUS TARGET 5 & CAPTURE BALL": ("lamp.bonus-5-and-capture-ball", "Bonus object 5 and capture ball"),
		"BONUS TARGET 8 & LFT. BANK": ("lamp.bonus-8-and-left-bank", "Bonus object 8 and left bank"),
		"L. BANK 7000 & R. OUTLANE": ("lamp.left-bank-7000-and-right-outlane", "Left bank 7,000 and right outlane"),
		"R. BANK 7000 & L. OUTLANE": ("lamp.right-bank-7000-and-left-outlane", "Right bank 7,000 and left outlane"),
		"L. RETURN LANE & SPOT NO.": ("lamp.left-return-lane-spot-number", "Left return lane spots number"),
		"R. RETURN LANE & SPOT NO.": ("lamp.right-return-lane-spot-number", "Right return lane spots number"),
		"R. BANK BOTTOM WOW": ("lamp.right-bank-bottom-wow", "Right bank bottom WOW"),
		"R. BANK TOP WOW": ("lamp.right-bank-top-wow", "Right bank top WOW"),
		"TOP BANK L. WOW": ("lamp.center-bank-left-wow", "Center (top) bank left WOW"),
		"TOP BANK R. WOW": ("lamp.center-bank-right-wow", "Center (top) bank right WOW"),
		"LOOP 177K": ("lamp.loop-top-value", "Loop top value (printed 177K)"),
		"1-8 LITES SPECIAL": ("lamp.one-to-eight-lites-special", "1-8 lites special"),
		"HIGH SCORE TO DATE": ("lamp.high-score-to-date", "High score to date (backbox)"),
		"GAME OVER": ("lamp.game-over", "Game over (backbox)"),
		"MATCH": ("lamp.match", "Match (backbox)"),
		"TILT": ("lamp.tilt", "Tilt (backbox)"),
	}
	if description in special:
		return special[description]
	words = description.lower().replace(" ", "-")
	if description.startswith("BONUS TARGET"):
		return f"lamp.bonus-{description.split()[-1]}", f"Bonus object {description.split()[-1]}"
	if description.startswith(("DROP TARGET", "WOW TARGET", "SPECIAL TARGET")):
		kind = {"DROP": "drop target", "WOW": "WOW", "SPECIAL": "special"}[description.split()[0]]
		return f"lamp.{words}", f"{kind[0].upper() + kind[1:]} object {description.split()[-1]}"
	if description.startswith("LOOP"):
		return f"lamp.{words}", f"Loop value {description.split()[-1]}"
	if description.startswith("MULTIPLIER"):
		return f"lamp.{words}", f"Bonus multiplier {description.split()[-1]}"
	if description.startswith("SPINNER"):
		return f"lamp.{words}", f"Spinner value {description.split()[-1]}"
	return f"lamp.{words}", description.title()


# --- Option switches -------------------------------------------------------------------------------------------------------
#
# `NINE BALL SWITCH ASSIGNMENTS` (manual PDF page 11) and the adjustment pages (PDF pages 12-15).
DIPS: dict[int, str] = {
	**{n: f"Coin chute No. 1 credits per coin, selector bit {n} (switches 1-4)" for n in range(1, 5)},
	5: "Add-a-ball (ON = add-a-ball, OFF = off)",
	6: "High score feature (ON = replay, OFF = extra ball)",
	7: "Balls per game (ON = 5, OFF = 3)",
	8: "Background sound (PDF page 11: ON = on, OFF = off; PDF page 13 prints sound off with switch 8 ON)",
	**{n: f"Coin chute No. 2 credits per coin, selector bit {n - 8} (switches 9-12)" for n in range(9, 13)},
	13: "Spot number target lite (ON = liberal, OFF = conservative)",
	14: "Multiplier step-up (ON = one three-bank, OFF = both three-banks)",
	15: "High score to date feature, selector bit 1",
	16: "High score to date feature, selector bit 2",
	17: "Three-bank targets that advance the spinner value (ON = the two outside targets, OFF = the center targets, as PDF page 11 prints and the ROM confirms; PDF page 14 prints the reverse)",
	18: "Maximum credits, selector bit 1 (10, 15, 25 or 40)",
	19: "Maximum credits, selector bit 2",
	20: "Credit display (ON = on, OFF = off)",
	21: "Match feature (ON = on, OFF = off)",
	22: "WOW and special award, selector bit 1 (chart with switches 23 and 24)",
	23: "WOW and special award, selector bit 2",
	24: "WOW and special award, selector bit 3",
	**{n: f"Coin chute No. 3 credits per coin, selector bit {n - 24} (switches 25-28)" for n in range(25, 29)},
	29: "Eight-bank WOW lites on when object 8 or object 9 is hit (ON = 8 ball, OFF = 9 ball)",
	30: "Super bonus lites on when object 8 or object 9 is hit (ON = 8 ball, OFF = 9 ball)",
	31: "Three-bank WOW lites on at multiplier (ON = 6X, OFF = 7X)",
	32: "Special limit (ON = one or more per ball, OFF = one per ball)",
}

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
# Raw object centres of the retained `Nine Ball (Stern 1980).vpx` (vpxtool git:v0.33.3 extraction), in VPX units; the curator normalizes them by the
# table's own bounds (left 0, top 0, right 952, bottom 1927). Walls use the mean of their drag points. The retained-evidence test re-reads each
# value from the extraction.

TABLE_WIDTH, TABLE_HEIGHT = 952.0, 1927.0

OBJECTS: dict[str, tuple[str, float, float, str]] = {
	"sw4": ("Trigger", 109.81481, 130.05557, "Trigger.sw4.json"),
	"sw5": ("Spinner", 757.26245, 904.1872, "Spinner.sw5.json"),
	"sw9": ("HitTarget", 135.6974, 988.5332, "HitTarget.sw9.json"),
	"sw10": ("HitTarget", 136.4875, 545.274, "HitTarget.sw10.json"),
	"sw11": ("HitTarget", 135.6974, 932.82965, "HitTarget.sw11.json"),
	"sw12": ("HitTarget", 136.4875, 600.1873, "HitTarget.sw12.json"),
	"sw13": ("HitTarget", 135.6974, 874.7555, "HitTarget.sw13.json"),
	"sw14": ("HitTarget", 136.09244, 655.49615, "HitTarget.sw14.json"),
	"sw15": ("HitTarget", 135.69742, 818.4592, "HitTarget.sw15.json"),
	"sw16": ("HitTarget", 136.29001, 708.82947, "HitTarget.sw16.json"),
	"sw17": ("Bumper", 732.8535, 290.3511, "Bumper.sw17.json"),
	"sw18": ("HitTarget", 372.07608, 277.42203, "HitTarget.sw18.json"),
	"sw19": ("HitTarget", 421.59045, 250.03108, "HitTarget.sw19.json"),
	"sw20": ("HitTarget", 469.34903, 223.69365, "HitTarget.sw20.json"),
	"sw21": ("HitTarget", 210.43135, 306.45245, "HitTarget.sw21.json"),
	"sw22": ("HitTarget", 747.91974, 410.16278, "HitTarget.sw22.json"),
	"sw23": ("HitTarget", 760.5618, 463.89114, "HitTarget.sw23.json"),
	"sw24": ("HitTarget", 773.2039, 516.56635, "HitTarget.sw24.json"),
	"sw25": ("Trigger", 804.7189, 1346.5385, "Trigger.sw25.json"),
	"sw26": ("Trigger", 56.12226, 1340.9921, "Trigger.sw26.json"),
	"sw27": ("Trigger", 732.9054, 1344.5197, "Trigger.sw27.json"),
	"sw28": ("Trigger", 126.86625, 1341.8396, "Trigger.sw28.json"),
	"RightSlingShot": ("Wall", 627.0163383333334, 1342.6207000000002, "Wall.RightSlingShot.json"),
	"LeftSlingShot": ("Wall", 235.878365, 1341.8467833333334, "Wall.LeftSlingShot.json"),
	"sw31": ("Bumper", 531.1482, 464.45074, "Bumper.sw31.json"),
	"sw32": ("Trigger", 55.05768, 910.35406, "Trigger.sw32.json"),
	"sw34": ("Kicker", 54.351166, 605.33923, "Kicker.sw34.json"),
	"sw35": ("HitTarget", 462.4783, 141.18526, "HitTarget.sw35.json"),
	"sw38": ("Trigger", 55.313957, 547.7241, "Trigger.sw38.json"),
	"sw1": ("Trigger", 55.321045, 507.95975, "Trigger.sw1.json"),
	"sw40": ("Trigger", 899.4787, 1634.8495, "Trigger.sw40.json"),
	"LeftFlipper": ("Flipper", 254.60306, 1574.7891, "Flipper.LeftFlipper.json"),
	"RightFlipper": ("Flipper", 602.0973, 1575.941, "Flipper.RightFlipper.json"),
	"Drain": ("Kicker", 484.03406, 1830.4049, "Kicker.Drain.json"),
	"BallRelease": ("Kicker", 819.3616, 1648.802, "Kicker.BallRelease.json"),
}
# The 25 bulb-filament primitives of the table's general illumination, each with a GI_<n> bulb light within 16 VPX units of its centre.
GI_BULBS: dict[str, tuple[float, float, str]] = {
	"BulbFil1": (224.15204, 1406.8408, "GI_19"), "BulbFil2": (631.8726, 1414.5675, "GI_20"), "BulbFil3": (181.77061, 1254.8218, "GI_18"),
	"BulbFil4": (675.5185, 1261.9558, "GI_21"), "BulbFil5": (61.35942, 1120.3706, "GI_17"), "BulbFil6": (797.7556, 1121.49, "GI_22"),
	"BulbFil7": (802.8425, 787.0396, "GI_24"), "BulbFil8": (792.7397, 685.9794, "GI_25"), "BulbFil9": (820.5714, 442.97455, "GI_11"),
	"BulbFil10": (824.4421, 351.58353, "GI_10"), "BulbFil11": (813.7645, 236.74577, "GI_9"), "BulbFil12": (725.6051, 34.998676, "GI_6"),
	"BulbFil13": (832.5296, 71.398575, "GI_8"), "BulbFil14": (242.71434, 53.27015, "GI_1"), "BulbFil15": (323.77234, 179.38023, "GI_2"),
	"BulbFil16": (421.09006, 161.49713, "GI_3"), "BulbFil17": (136.64308, 51.709587, "GI_7"), "BulbFil18": (169.71037, 216.40092, "GI_4"),
	"BulbFil19": (49.268856, 335.7705, "GI_5"), "BulbFil20": (100.8644, 558.3792, "GI_12"), "BulbFil21": (100.6563, 620.66876, "GI_13"),
	"BulbFil22": (100.21506, 833.51385, "GI_14"), "BulbFil23": (99.86117, 901.7621, "GI_15"), "BulbFil24": (100.08821, 970.18726, "GI_16"),
	"BulbFil25": (802.5832, 1025.6893, "GI_23"),
}

# Matrix switch -> the table object(s) placed for it, and the note for a projection or a defective binding.
SWITCH_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	4: (["sw4"], None), 5: (["sw5"], None),
	**{address: ([f"sw{address}"], None) for address in range(9, 25) if address != 17},
	17: (["sw17"], None),
	25: (["sw25"], None), 26: (["sw26"], None), 27: (["sw27"], None), 28: (["sw28"], None),
	29: (["RightSlingShot"], "Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own hit event."),
	30: (["LeftSlingShot"], "Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own hit event."),
	31: (["sw31"], None), 32: (["sw32"], None), 34: (["sw34"], None), 35: (["sw35"], None),
	38: (["sw38"], "The retained script mis-binds the lock lane: trigger `sw38`, in the middle of the lane where the manual's switch drawing puts 38, writes switch 39, so that table never closes 38. "
		"Placed on trigger `sw38`, whose position and name agree with the drawing; the binding is a defect of the table."),
	39: (["sw1"], "The retained table has no trigger bound to 39 at the top of the lock lane: its `sw39` handler has no object, and the trigger there is named `sw1` and has no handler. "
		"Placed on that trigger, at the top of the lane where the manual's switch drawing puts 39; a projection resting on the drawing, not on a script binding."),
	40: (["sw40"], None),
}
# Each side's end-of-stroke contact is placed on that side's flipper pivot.
DIRECT_OBJECTS = {1: "LeftFlipper", 2: "RightFlipper"}
# Solenoid -> object(s) and, for a projection, why.
SOLENOID_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	1: (["RightSlingShot"], "Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	2: (["LeftSlingShot"], "Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	3: (["sw22", "sw23", "sw24"], "Projected onto the right three-bank it resets: the mean of the table's own three target objects. The reset coil sits under the bank and has no object."),
	4: (["sw18", "sw19", "sw20"], "Projected onto the center three-bank it resets: the mean of the table's own three target objects."),
	5: (["sw31"], None),
	8: (["sw34"], None),
	**{address: ([f"sw{24 - address}"], f"Placed on the drop target it knocks down (table `sw{24 - address}`); the coil sits behind the target and has no object.") for address in range(9, 16)},
	17: ([f"sw{n}" for n in range(9, 17)], "Projected onto the eight-target bank it resets: the mean of the table's own eight target objects."),
	20: (["sw21"], "Placed on the loop drop target it raises (table `sw21`); the coil sits under the target and has no object."),
}
