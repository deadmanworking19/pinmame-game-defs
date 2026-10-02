"""Reviewed Quicksilver (Stern, 1980) device data, kept apart from the builder so both stay readable.

Every number below was read from this game's own sheets or observed in a retained harness run; none is carried from a sister
machine. Raw retained-table coordinates are stored (VPX units, Quicksilver (Stern 1980) VPW 1.0) and normalized by the
builder, so a reviewer can check a placement against ``external:pinmame-review-artifacts/quicksilver-1980/vpw-geometry.tsv`` by eye.
"""

from __future__ import annotations

from typing import Any

# --- Drivers ---------------------------------------------------------------------------------------------------------

DRIVERS: dict[str, tuple[str, str, str, str | None, str]] = {
	"quicksil": (
		"Quicksilver", "1980", "Stern", None,
		"Production ROM and the reference for this definition: GEN_STMPU200, seven-digit dispst7 displays, FLIP_SW(FLIP_L), Stern ST300 sound board. "
		"The harness runs retained with this definition boot this driver.",
	),
	"quicksfp": (
		"Quicksilver (Free Play)", "1980", "Stern", "quicksil",
		"Free-play build of the production ROM: the same init data, the same U1/U2/U5 game ROMs and a free-play U6, so the I/O inventory is identical. "
		"A harness run with this driver was not made; the identity rests on the pinned driver declaration.",
	),
	"quicksib": (
		"Quicksilver (Free Play & modified rules rev. 07D)", "2021", "Stern / Idleman", "quicksil",
		"Community rules revision (spinner counters and drop-sweep awards) for the same hardware: identical INITGAME data, display layout, flipper setting and sound board. "
		"It changes rules in ROM only, so the physical inventory is unchanged; the ROM was not available for a harness run.",
	),
	"quicksic": (
		"Quicksilver (Free Play & modified rules rev. 8.1)", "2024", "Stern / slochar", "quicksil",
		"Community rules revision 8.1 for the same hardware: identical INITGAME data, display layout, flipper setting and sound board. It is the driver the "
		"retained VPW 1.0 table binds (cGameName = \"quicksic\"); its rules differ from the production ROM, the hardware does not.",
	),
}

# --- Cabinet and service inputs ---------------------------------------------------------------------------------------

SERVICE_SWITCHES: dict[int, dict[str, Any]] = {
	-7: {
		"id": "switch.self-test-button", "label": "Self Test button (coin door)", "roles": ["service.button"],
		"notes": "The Self-Test button inside the coin door. Public -7 starts the ROM's diagnostics; a harness run retained with this definition drives it.",
		"availability": "used", "evidence": "manual-and-harness",
	},
	-6: {
		"id": "switch.cpu-diagnostic-button", "label": "CPU diagnostic button (MPU)", "roles": ["service.diagnostic"],
		"notes": "PinMAME routes public -6 to the CPU's NMI line (BY35_SWCPUDIAG). The manual's MPU pushbutton `S33 MEMORY CLEAR` sits on the MPU module and is the "
			"likely physical counterpart, but no source ties S33 to the NMI line, so the identity of the two is recorded here as an inference.",
		"availability": "optional", "evidence": "core",
	},
	-5: {
		"id": "switch.sound-diagnostic-button", "label": "Sound board diagnostic button", "roles": ["service.diagnostic"],
		"notes": "PinMAME routes public -5 to the sound board's diagnostic input (BY35_SWSOUNDDIAG). The manual documents no such button for the ST300 sound module.",
		"availability": "optional", "evidence": "core",
	},
}

# --- Playfield and cabinet matrix switches ------------------------------------------------------------------------------
#
# Public address = (strobe * 8) + return + 1 on the five-strobe by eight-return MPU matrix; the ROM's stuck-switch display shows the
# same number for every address 1-40 (retained run quicksilver stuck-switch). ``cabinet`` rows are wired on the cabinet sheet (A4J3), the
# others on the playfield sheet (A4J2).

STROBES = {
	0: ("W-R", "A4J2-1"), 1: ("BRN-W", "A4J2-2"), 2: ("W-BLU", "A4J2-3"), 3: ("W-Y", "A4J2-4"), 4: ("Y-R", "A4J2-5"),
}
RETURNS = {
	0: ("BRN", "A4J2-8"), 1: ("GREY", "A4J2-9"), 2: ("W-O", "A4J2-10"), 3: ("W-B", "A4J2-11"),
	4: ("W-G", "A4J2-12"), 5: ("W-BRN", "A4J2-13"), 6: ("BRN-Y", "A4J2-14"), 7: ("O", "A4J2-15"),
}
CABINET_RETURNS = {0: ("BLU", "A4J3-9"), 1: ("BRN-W", "A4J3-10"), 2: ("R-W", "A4J3-11"), 5: ("BLU-W", "A4J3-14"), 6: ("BLU-O", "A4J3-15"), 7: ("Y", "A4J3-16")}
CABINET_STROBE0 = ("R-Y", "A4J3-2")

# address -> spec. ``positions`` are raw (x, y) retained-table coordinates; ``table`` names the objects they come from.
SWITCHES: dict[int, dict[str, Any]] = {
	1: {"id": "switch.coin-chute-1", "label": "Coin chute 1 (nearest the door hinge)", "type": "other", "cabinet": True, "roles": ["cabinet.coin.1"],
		"notes": "SW-1 in the manual's three-chute door drawing, the chute nearest the hinge. A coin on it adds a credit in the retained gameplay run."},
	2: {"id": "switch.coin-chute-2", "label": "Coin chute 2 (center)", "type": "other", "cabinet": True, "roles": ["cabinet.coin.2"],
		"notes": "SW-2, the middle chute. A coin on it adds a credit in the retained gameplay run."},
	3: {"id": "switch.coin-chute-3", "label": "Coin chute 3 (farthest from the door hinge)", "type": "other", "cabinet": True, "roles": ["cabinet.coin.3"],
		"notes": "SW-3, the chute farthest from the hinge. A coin on it adds a credit in the retained gameplay run."},
	4: {"id": "switch.right-spinner", "label": "Right spinner", "type": "other", "pulse": True,
		"table": "Spinner sw4", "positions": [(769.023, 625.529)],
		"notes": "Spinning target on the right side below the right-arc standups (Spin Target Assembly 14A-7-13). Each completed rotation closes the contact once; the retained gameplay run scores 200 per closure. "
			"The matrix sheet calls the position RIGHT S.T."},
	5: {"id": "switch.left-spinner", "label": "Left spinner", "type": "other", "pulse": True,
		"table": "Spinner sw5", "positions": [(141.881, 773.001)],
		"notes": "Spinning target on the left side above the kick-out hole. The matrix sheet calls the position LEFT S.T.; the retained gameplay run scores 200 per closure."},
	6: {"id": "switch.credit-button", "label": "Credit button", "type": "button", "cabinet": True, "roles": ["cabinet.start"],
		"notes": "Coin-door credit button. In the retained gameplay run it starts a game from credits and decrements the credit display."},
	7: {"id": "switch.tilt", "label": "Tilt (plumb bob, ball roll and panel tilt)", "type": "tilt", "cabinet": True, "quantity": 3, "roles": ["cabinet.tilt"],
		"notes": "Shared matrix position for the pendulum (plumb bob), the roll (ball) tilt and the panel tilt, all adjusted as normally open on installation (manual page 2). The location sheet lists ROLL TILT and PENDULUM for 7. "
			"Closing public 7 in play drops the flipper-enable output 19 in the retained gameplay run."},
	8: {"id": "switch.slam", "label": "Slam (door and tilt board; playfield contact not confirmed)", "type": "tilt", "cabinet": True, "roles": ["cabinet.slam-tilt"],
		"notes": "Shared matrix position for the slam contacts. The location sheet (manual page 17) lists two, TILT BOARD and DOOR V.B. The operating text (manual page 5) says there is a slam switch on the front door, one on the tilt board and one on the playfield. No retained source settles whether a playfield slam contact was fitted at the factory: the location drawing (page 17) draws none, but the text states one, so the quantity is deliberately left unstated rather than recorded as 2 or 3. Every contact shares public address 8, so a recreation that wires the door and tilt-board contacts and treats a playfield contact as optional behaves identically at the controller."},
	9: {"id": "switch.right-pop-bumper", "label": "Right pop bumper", "type": "leaf", "pulse": True,
		"table": "Bumper Bumper1", "positions": [(536.269, 495.384)],
		"notes": "Printed RIGHT POP BUMPER at 9 (matrix: RIGHT THUMP.). Closing it in play scores 1000 and fires public output 1 in the retained gameplay run."},
	10: {"id": "switch.left-pop-bumper", "label": "Left pop bumper", "type": "leaf", "pulse": True,
		"table": "Bumper Bumper2", "positions": [(319.156, 484.721)],
		"notes": "Printed LEFT POP BUMPER at 10 (matrix: LEFT THUMP.). Closing it scores 1000 and fires public output 2 in the retained gameplay run."},
	11: {"id": "switch.bottom-pop-bumper", "label": "Bottom pop bumper", "type": "leaf", "pulse": True,
		"table": "Bumper Bumper3", "positions": [(480.112, 727.874)],
		"notes": "Printed BOTTOM POP BUMPER at 11 (matrix: LOWER THUMP.). Closing it scores 1000 and fires public output 3 in the retained gameplay run."},
	12: {"id": "switch.left-slingshot", "label": "Left slingshot", "type": "leaf", "pulse": True,
		"table": "Wall LeftSlingShot", "positions": [(229.946, 1402.196)],
		"notes": "Printed LEFT SLINGSHOT at 12. Closing it scores 10 and fires public output 4 in the retained gameplay run. The retained VPW 1.0 script pulses 20 from this slingshot instead, a defect of that script "
			"(the corpus 1.0 script and the older retained table pulse 12), which has no effect on the machine."},
	13: {"id": "switch.right-slingshot", "label": "Right slingshot", "type": "leaf", "pulse": True,
		"table": "Wall RightSlingShot", "positions": [(634.144, 1401.022)],
		"notes": "Printed RIGHT SLINGSHOT at 13. Closing it scores 10 and fires public output 5 in the retained gameplay run. The retained VPW 1.0 script pulses 21 from this slingshot instead, a defect of that script."},
	14: {"id": "switch.bottom-left-standup", "label": "Bottom left stand-up target", "type": "leaf", "pulse": True,
		"table": "HitTarget sw14", "positions": [(172.313, 592.768)], "notes": "Left-arc stand-up, lowest of three (matrix: L. LOWER S.U.). Scores 500 in the retained gameplay run."},
	15: {"id": "switch.center-left-standup", "label": "Center left stand-up target", "type": "leaf", "pulse": True,
		"table": "HitTarget sw15", "positions": [(155.302, 497.447)], "notes": "Left-arc stand-up, middle of three (matrix: L. MID. S.U.). Scores 500."},
	16: {"id": "switch.top-left-standup", "label": "Top left stand-up target", "type": "leaf", "pulse": True,
		"table": "HitTarget sw16", "positions": [(163.677, 404.796)], "notes": "Left-arc stand-up, highest of three (matrix: L. TOP S.U.). Scores 500."},
	17: {"id": "switch.top-lane-q", "label": "Top roll-over lane Q (left)", "type": "leaf", "pulse": False,
		"table": "Trigger sw17", "positions": [(257.338, 255.169)], "notes": "Leftmost of the four top lanes (matrix: TOP L. R.O.W., a roll-over wire form), lettered Q. Scores 500."},
	18: {"id": "switch.top-lane-u", "label": "Top roll-over lane U", "type": "leaf", "pulse": False,
		"table": "Trigger sw18", "positions": [(357.420, 258.857)], "notes": "Second top lane, lettered U (matrix: TOP R.O.W.). Scores 500."},
	19: {"id": "switch.top-lane-i", "label": "Top roll-over lane I", "type": "leaf", "pulse": False,
		"table": "Trigger sw19", "positions": [(457.151, 258.154)], "notes": "Third top lane, lettered I (matrix: TOP R.O.W). Scores 500."},
	20: {"id": "switch.top-lane-c", "label": "Top roll-over lane C (right)", "type": "leaf", "pulse": False,
		"table": "Trigger sw20", "positions": [(557.350, 256.750)], "notes": "Rightmost top lane, lettered C (matrix: TOP R. R.O.W.). Scores 500. "
			"The retained VPW 1.0 script also pulses this address from its left slingshot, a defect of that script."},
	21: {"id": "switch.center-drop-target-1", "label": "Center drop target 1 (highest)", "type": "leaf", "pulse": False, "drop": True,
		"table": "Wall sw21", "positions": [(347.678, 889.623)], "notes": "Highest target of the slanted four-target center bank (matrix: CENTER HIGHEST D.T.). Closed while the target is down."},
	22: {"id": "switch.center-drop-target-2", "label": "Center drop target 2", "type": "leaf", "pulse": False, "drop": True,
		"table": "Wall sw22", "positions": [(368.773, 936.197)], "notes": "Second target of the center bank (matrix: CENTER D.T.). Closed while down."},
	23: {"id": "switch.center-drop-target-3", "label": "Center drop target 3", "type": "leaf", "pulse": False, "drop": True,
		"table": "Wall sw23", "positions": [(390.327, 981.822)], "notes": "Third target of the center bank (matrix: CENTER D.T.). Closed while down."},
	24: {"id": "switch.center-drop-target-4", "label": "Center drop target 4 (lowest)", "type": "leaf", "pulse": False, "drop": True,
		"table": "Wall sw24", "positions": [(411.842, 1028.408)], "notes": "Lowest target of the center bank (matrix: CENTER D.T. LOWEST). Closing the fourth target in the retained gameplay run fires public output 7, the bank reset."},
	25: {"id": "switch.right-standup-top", "label": "Right stand-up target (top)", "type": "leaf", "pulse": True,
		"table": "HitTarget sw25", "positions": [(724.404, 399.820)], "notes": "Highest of the three right-arc stand-ups (matrix: TOP RIGHT S.U.). Scores 500."},
	26: {"id": "switch.right-standup-middle", "label": "Right stand-up target (middle)", "type": "leaf", "pulse": True,
		"table": "HitTarget sw26", "positions": [(728.418, 478.956)], "notes": "Middle right-arc stand-up (matrix: R. S.U.). Scores 500."},
	27: {"id": "switch.right-standup-bottom", "label": "Right stand-up target (bottom)", "type": "leaf", "pulse": True,
		"table": "HitTarget sw27", "positions": [(708.864, 558.451)], "notes": "Lowest right-arc stand-up (matrix: RIGHT S.U. BOTTOM). Scores 500."},
	28: {"id": "switch.special-roll-over", "label": "Special roll-over button", "type": "button", "pulse": False,
		"table": "Trigger sw28", "positions": [(694.946, 285.462)], "notes": "Star roll-over button just inside the top-right ball gate (matrix: RIGHT R.O.B.). Scores 1000 in the retained gameplay run."},
	29: {"id": "switch.kick-out-hole", "label": "Kick-out hole", "type": "leaf", "pulse": False,
		"table": "Trigger sw29", "positions": [(77.787, 894.426)], "notes": "Switch under the left-edge kick-out hole (matrix: KICKOUT HOLE). Held closed while a ball sits in the hole; closing it fires public output 9, the eject, in the retained gameplay run."},
	30: {"id": "switch.right-drop-target-1", "label": "Right drop target 1 (highest)", "type": "leaf", "pulse": False, "drop": True,
		"table": "Wall sw30", "positions": [(810.010, 715.873)], "notes": "Highest target of the three-target right bank beside the right rail (matrix: RIGHT D.T. TOP). Closed while down."},
	31: {"id": "switch.right-drop-target-2", "label": "Right drop target 2", "type": "leaf", "pulse": False, "drop": True,
		"table": "Wall sw31", "positions": [(809.494, 768.687)], "notes": "Middle target of the right bank (matrix: RIGHT D.T. MIDDLE). Closed while down."},
	32: {"id": "switch.right-drop-target-3", "label": "Right drop target 3 (lowest)", "type": "leaf", "pulse": False, "drop": True,
		"table": "Wall sw32", "positions": [(809.306, 818.233)], "notes": "Lowest target of the right bank (matrix: RIGHT D.T. LOWER). Closing the third target in the retained gameplay run fires public output 8, the bank reset."},
	33: {"id": "switch.outhole", "label": "Out-hole", "type": "leaf", "pulse": False, "initial_active": True,
		"table": "Kicker Drain", "positions": [(408.982, 1896.422)], "notes": "Single-ball out-hole at the bottom centre between the flippers. The known-working tables start the game with the ball on this switch."},
	34: {"id": "switch.left-outlane", "label": "Left outside lane", "type": "leaf", "pulse": False,
		"table": "Trigger sw34", "positions": [(57.345, 1445.936)], "notes": "Left outlane (matrix: LEFT OUT-LANE). Scores 25,000 in the retained gameplay run."},
	35: {"id": "switch.right-outlane", "label": "Right outside lane", "type": "leaf", "pulse": False,
		"table": "Trigger sw35", "positions": [(804.366, 1445.885)], "notes": "Right outlane (matrix: RIGHT OUT-LANE). Scores 25,000 in the retained gameplay run."},
	36: {"id": "switch.left-return-lane", "label": "Left return lane", "type": "leaf", "pulse": False,
		"table": "Trigger sw36", "positions": [(129.100, 1409.236)], "notes": "Left inlane (matrix: L. RETURN LANE). Scores 5000."},
	37: {"id": "switch.right-return-lane", "label": "Right return lane", "type": "leaf", "pulse": False,
		"table": "Trigger sw37", "positions": [(733.782, 1401.902)], "notes": "Right inlane (matrix: R. RETURN LANE). Scores 5000."},
	38: {"id": "switch.ten-point-bounce", "label": "10 point bounce switches (rebound rubbers)", "type": "leaf", "pulse": True, "quantity": 4,
		"table": "Wall sw38e, sw38d, sw38c, sw38b", "positions": [(635.860, 187.206), (394.455, 889.227), (443.821, 1001.226), (785.492, 1121.983)],
		"notes": "The matrix sheet prints `(4) 10-PT. SWITCHES` and the location drawing has four leader ends: one at the top right beside the ball gate, two at the ends of the center drop-target bank and one at the lower right. "
			"The retained table models five rubbers (sw38a-sw38e); sw38a at the far left is not on the factory location drawing and is not placed. Each closure scores 10."},
	39: {"id": "switch.ten-point-roll-over", "label": "10 point roll-over button", "type": "button", "pulse": False,
		"table": "Trigger sw39", "positions": [(616.339, 83.720)], "notes": "Round roll-over button at the top of the arch (matrix: TOP R.O.B.; the self-test table prints `(NO-SHF)`). Scores 10."},
	40: {"id": "switch.lane-standup", "label": "Lane stand-up target", "type": "leaf", "pulse": True,
		"table": "HitTarget sw40", "positions": [(799.820, 1013.491)], "notes": "Lone stand-up on the right side wall (matrix: LONE S.U.). Scores 500."},
}

# Flipper buttons: PinMAME synthetic switches 81-84 (FLIP_SW(FLIP_L)): lower right 82, lower left 84; 81/83 are the unused upper positions.
FLIPPER_BUTTONS = {
	82: ("switch.lower-right-flipper-button", "Lower right flipper button", "flipper.lower.right.button", "R", "A3J2-1"),
	84: ("switch.lower-left-flipper-button", "Lower left flipper button", "flipper.lower.left.button", "BLU", "A3J2-2"),
}
UNUSED_FLIPPER_POSITIONS = {81: ("switch.upper-right-flipper-position", "Upper right flipper button position (not fitted)"), 83: ("switch.upper-left-flipper-position", "Upper left flipper button position (not fitted)")}

# --- Solenoids ----------------------------------------------------------------------------------------------------------
#
# public address -> physical service number (SDU Q position). Derived from the retained self-test run: the ROM energizes the
# nineteen solenoids in physical order, and the public addresses fire in this order: 2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18.

SELF_TEST_ORDER = (2, 1, 6, 7, 3, 4, 5, 8, 11, 12, 14, 13, 9, 10, 19, 15, 17, 20, 18)
PHYSICAL_TO_PUBLIC = {number: address for number, address in enumerate(SELF_TEST_ORDER, start=1)}

SOLENOIDS: dict[int, dict[str, Any]] = {
	1: {"id": "device.right-thumper-bumper", "label": "Right thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "G-BLU", "conn": "A3J2-4",
		"table": "Bumper Bumper1", "positions": [(536.269, 495.384)],
		"notes": "Solenoid 2 of the printed list (RIGHT THUMPER), driven by the ROM when the right pop bumper switch (public 9) closes."},
	2: {"id": "device.left-thumper-bumper", "label": "Left thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "G-O", "conn": "A3J2-9",
		"table": "Bumper Bumper2", "positions": [(319.156, 484.721)],
		"notes": "Solenoid 1 of the printed list (LEFT THUMPER), driven when the left pop bumper switch (public 10) closes."},
	3: {"id": "device.lower-thumper-bumper", "label": "Lower thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "G-Y", "conn": "A3J2-10",
		"table": "Bumper Bumper3", "positions": [(480.112, 727.874)],
		"notes": "Solenoid 5 of the printed list (LOWER THUMPER; the matrix and switch lists call it the bottom/lower bumper), driven when the bottom pop bumper switch (public 11) closes."},
	4: {"id": "device.left-slingshot", "label": "Left slingshot", "kind": "coil", "part": "J-26-1500", "wire": "G-R", "conn": "A3J2-11",
		"table": "Wall LeftSlingShot", "positions": [(229.946, 1402.196)],
		"notes": "Solenoid 6 of the printed list, driven when the left slingshot switch (public 12) closes."},
	5: {"id": "device.right-slingshot", "label": "Right slingshot", "kind": "coil", "part": "J-26-1500", "wire": "R-Y", "conn": "A3J2-12",
		"table": "Wall RightSlingShot", "positions": [(634.144, 1401.022)],
		"notes": "Solenoid 7 of the printed list, driven when the right slingshot switch (public 13) closes."},
	6: {"id": "device.knocker", "label": "Knocker", "kind": "coil", "part": "N-26-1200", "wire": "G-B", "conn": "A3J2-5", "cabinet": True, "roles": ["cabinet.knocker"],
		"notes": "Solenoid 3 of the printed list; the location drawing's `NOT ON PLAYFIELD` note names it. The Solenoid Driver Schematic prints `KNOCKER (G-B)` on J2 pin 5; the cabinet sheet prints the wire as `A3J2-5 (B-Y)`."},
	7: {"id": "device.center-bank-reset", "label": "Center drop-target bank reset", "kind": "coil", "part": "B-27-2300", "wire": "B-BLU", "conn": "A3J1-5",
		"table": "Wall sw21..sw24", "positions": [(379.655, 959.012)],
		"projection": "Projected onto the center four-target drop bank it resets (the mean of the retained table's own target walls sw21-sw24); the reset coil sits under the bank and has no object of its own.",
		"notes": "Solenoid 4 of the printed list (CENTER BANK TARGET). Fired by the ROM at game start and when the fourth center target closes in the retained gameplay run."},
	8: {"id": "device.right-bank-reset", "label": "Right drop-target bank reset", "kind": "coil", "part": "B-27-2300", "wire": "B-O", "conn": "A3J5-10",
		"table": "Wall sw30..sw32", "positions": [(809.603, 767.598)],
		"projection": "Projected onto the right three-target drop bank it resets (the mean of the retained table's own target walls sw30-sw32).",
		"notes": "Solenoid 8 of the printed list (RIGHT BANK TARGET). The playfield sheet prints the pin as `A3J5-12 (D-O)`; the Solenoid Driver Schematic places `R. DR. TARGET (B-O)` on J5 pin 10, which is the reading used. "
			"Fired at game start and when the third right target closes in the retained gameplay run."},
	9: {"id": "device.kick-out-hole-eject", "label": "Kick-out hole eject", "kind": "coil", "part": "J-28-2300", "wire": "B-Y", "conn": "A3J5-12",
		"table": "Trigger sw29", "positions": [(77.787, 894.426)],
		"notes": "Solenoid 13 of the printed list (KICK-OUT HOLE, parts list EJECT HOLE). Fires when the kick-out hole switch (public 29) closes, and once at game start."},
	10: {"id": "device.out-hole-kicker", "label": "Out-hole kicker", "kind": "coil", "part": "JX-26-1200", "wire": "B-G", "conn": "A3J5-11",
		"table": "Kicker Drain", "positions": [(408.982, 1896.422)],
		"notes": "Solenoid 14 of the printed list (OUT-HOLE). The playfield sheet prints the out-hole wire as `A3J1-5 (B-G)`, a pin that is also printed for the center bank; the Solenoid Driver Schematic places `OUT-HOLE (B-G)` on J5 pin 11, which is the reading used. "
			"The ROM repeats the kick while the out-hole switch (public 33) stays closed."},
	11: {"id": "device.unused-solenoid-9", "label": "Unused solenoid driver 9", "kind": "coil", "phys": 9, "unused": True,
		"notes": "Printed OPEN. The Solenoid Driver Schematic lists five OPEN J5 pins (8, 9, 13, 14, 15) for the momentary drivers 9-12 and 16 without saying which pin belongs to which driver."},
	12: {"id": "device.unused-solenoid-10", "label": "Unused solenoid driver 10", "kind": "coil", "phys": 10, "unused": True, "notes": "Printed OPEN."},
	13: {"id": "device.unused-solenoid-12", "label": "Unused solenoid driver 12", "kind": "coil", "phys": 12, "unused": True, "notes": "Printed OPEN."},
	14: {"id": "device.unused-solenoid-11", "label": "Unused solenoid driver 11", "kind": "coil", "phys": 11, "unused": True, "notes": "Printed OPEN."},
	15: {"id": "device.unused-solenoid-16", "label": "Unused solenoid driver 16", "kind": "coil", "phys": 16, "unused": True, "notes": "Printed OPEN."},
	17: {"id": "device.unused-continuous-driver-17", "label": "Unused continuous driver 17", "kind": "relay", "phys": 17, "unused": True,
		"notes": "Printed OPEN. The Solenoid Driver Schematic wires its transistor (Q17, input PB4 on J4 pin 11, [Y-W]) to a pin marked N/U on J5 pin 7."},
	18: {"id": "device.coin-lockout", "label": "Coin lock-out coil", "kind": "coil", "part": "C-36-5300", "wire": "Y-W", "conn": "A3J2-8", "cabinet": True, "roles": ["cabinet.coin-door"],
		"notes": "Solenoid 19 of the printed list (COIN LOCK-OUT), a continuous output: the ROM energizes it from power-up in the retained runs. The cabinet sheet and the Solenoid Driver Schematic both print J2 pin 8 [Y-W]."},
	19: {"id": "device.flipper-enable-relay", "label": "Flipper enable relay", "kind": "relay", "wire": "Y-W", "conn": "A3J3-5", "internal": True, "roles": ["internal.flipper-enable"],
		"notes": "Solenoid 15 of the printed list (FLIPPERS (2)), a continuous output through the driver Q15 and the `FLIPPER ENABLE RELAY` coil (CR20, 43 VDC, J3 pin 5 `To A2J3-8 [Y-W]`). The ROM raises it when a game starts and drops it when a tilt closes switch 7 in the retained gameplay run."},
	20: {"id": "device.unused-continuous-driver-18", "label": "Unused continuous driver 18", "kind": "relay", "phys": 18, "unused": True,
		"notes": "Printed OPEN. The Solenoid Driver Schematic wires its transistor (Q18, input PB7 on J4 pin 10, [Y-R]) to a pin marked N/U on J2 pin 15."},
}

FLIPPERS = {
	46: {"id": "device.right-flipper", "label": "Right flipper", "wire": "O", "conn": "A3J1-9", "button_wire": "R", "button_conn": "A3J2-1",
		"table": "Flipper RightFlipper", "positions": [(591.922, 1656.452)], "side": "right", "power": 45},
	48: {"id": "device.left-flipper", "label": "Left flipper", "wire": "G", "conn": "A3J1-8", "button_wire": "BLU", "button_conn": "A3J2-2",
		"table": "Flipper LeftFlipper", "positions": [(270.058, 1656.347)], "side": "left", "power": 47},
}

# --- Lamps -------------------------------------------------------------------------------------------------------------------
#
# public lamp address = 16 * k + a + 1 for decoder U<k+1> output S<a>; the SCR number comes from the retained schematic's resistor labels.
# ``pins`` are the connector pins the sheets print; ``light`` is the retained VPW table's InsertLamps light number (TimerInterval).

DECODER = {
	0: [14, 12, 13, 8, 9, 10, 11, 4, 1, 2, 3, 7, 16, 5, 6],
	1: [29, 27, 28, 35, 34, 22, 26, 25, 24, 17, 23, 21, 15, 18, 19],
	2: [36, 38, 44, 49, 48, 37, 32, 20, 42, 41, 40, 39, 33, 30, 31],
	3: [57, 50, 51, 54, 55, 60, 59, 58, 56, 46, 52, 53, 47, 43, 45],
}
LAMP_TO_Q = {16 * k + a + 1: q for k, qs in DECODER.items() for a, q in enumerate(qs)}

# Raw VPW light centers (x, y), by light number.
LIGHTS = {
	1: (492.6, 1149.7), 2: (459.5, 1349.4), 3: (332.5, 1201.4), 4: (180.5, 1085.2), 5: (398.7, 1426.3), 7: (605.0, 1059.9), 8: (656.0, 834.1),
	9: (405.9, 67.1), 11: (433.0, 1589.0), 12: (559.4, 143.6), 14: (129.2, 1292.6), 15: (57.0, 1343.4), 17: (534.6, 1200.2), 18: (406.2, 1352.8),
	19: (372.2, 1151.0), 20: (223.5, 1127.2), 21: (469.2, 1425.5), 22: (213.2, 577.1), 23: (613.5, 1002.1), 24: (640.5, 431.1), 28: (456.9, 144.0),
	30: (735.0, 1288.9), 31: (805.8, 1339.4), 33: (543.0, 1260.9), 34: (353.4, 1320.5), 35: (430.9, 1132.3), 36: (262.5, 1085.8), 37: (397.7, 1496.5),
	38: (196.7, 493.6), 39: (632.6, 949.2), 40: (678.0, 504.6), 44: (354.9, 143.6), 46: (665.0, 739.2), 47: (632.5, 343.0), 49: (515.1, 1319.6),
	50: (326.8, 1264.7), 51: (433.4, 1244.8), 52: (292.0, 1041.2), 53: (467.9, 1496.7), 54: (204.7, 419.6), 55: (653.6, 897.7), 56: (647.0, 586.0),
	59: (752.0, 1054.5), 60: (255.3, 142.8), 62: (180.8, 841.0),
}

# pub -> (id suffix, label, pins [(jack, pin)], wire, light number or None, extra)
LAMPS: dict[int, dict[str, Any]] = {
	1: dict(id="lamp.bonus-1000", label="Bonus 1,000", pins=[("J1", 18)], wire="BRN-B", light=1),
	2: dict(id="lamp.bonus-5000", label="Bonus 5,000", pins=[("J1", 19)], wire="GREY-G", light=2),
	3: dict(id="lamp.bonus-9000", label="Bonus 9,000", pins=[("J1", 17)], wire="PURPLE", light=3),
	4: dict(id="lamp.center-bank-5000", label="Center bank target 5,000", pins=[("J1", 23)], wire="BLU-W", light=4,
		notes="Printed `5,000 CENTER DR. TARG.`."),
	5: dict(id="lamp.bonus-2x", label="Bonus 2X", pins=[("J1", 14)], wire="GREY-O", light=5),
	6: dict(id="lamp.unlisted-scr-q10", label="Unlisted lamp driver SCR Q10 (fitment unresolved)", pins=[], wire=None, light=None, availability="unknown",
		notes="No lamp list prints a load for this driver (the connector table puts SCR Q10 on J1 pin 15), but the ROM does not leave it dark: in the retained gameplay run it keeps toggling in the attract-mode lamp pattern "
			"(39 lamps, every one of them a listed lamp except this one) after the power-up flash has ended, unlike the five unlisted addresses that only the power-up flash and the self-test drive. "
			"The ROM's drive and the sheets' silence cannot both be explained from retained evidence, so the fitment stays unknown."),
	7: dict(id="lamp.right-bank-2x", label="Right bank target 2X", pins=[("J1", 16)], wire="BLACK", light=7),
	8: dict(id="lamp.right-bank-25000", label="Right bank target 25,000", pins=[("J1", 28)], wire="B-W", light=8),
	9: dict(id="lamp.flashing-extra-ball", label="Flashing extra ball", pins=[("J1", 24)], wire="BRN-BLU", light=9,
		notes="The flashing QUICK extra-ball insert at the top of the playfield (instruction card: spotting Q-U-I-C-K, then hitting the flashing target awards an extra ball)."),
	10: dict(id="lamp.top-rollover-divider-4", label="Top roll-over divider 4 (of 5, left to right)", pins=[("J1", 25)], wire="PUR-B", light=None, no_light="The retained table models no light for the five top dividers."),
	11: dict(id="lamp.shoot-again", label="Shoot again", pins=[("J1", 26), ("J2", 21)], wire="GREY-R", light=11, quantity=2, location="playfield and backbox",
		notes="One SCR (Q3) reaches both printed pins: the playfield wiring list prints J1 pin 26 and the Lamp Driver Schematic's list prints J2 pin 21, and the connector table shows Q3 on both. "
			"The playfield insert is placed; the backbox copy (the retained table's `sa` light) is the second bulb."),
	12: dict(id="lamp.top-lane-c", label="Top roll-over lane C lamp", pins=[("J2", 13)], wire="GREY-G", light=12),
	13: dict(id="lamp.high-score-to-date", label="High score to date", pins=[("J2", 22)], wire="GREY-O", light=None, backbox=True,
		notes="Backbox lamp; absent from the playfield wiring list, printed on the Lamp Driver Schematic's list."),
	14: dict(id="lamp.left-return-lanes", label="Left return lanes", pins=[("J2", 16)], wire="BLACK", light=14),
	15: dict(id="lamp.left-special", label="Left special", pins=[("J2", 14)], wire="WHITE", light=15),
	17: dict(id="lamp.bonus-2000", label="Bonus 2,000", pins=[("J1", 1)], wire="BLU-R", light=17),
	18: dict(id="lamp.bonus-6000", label="Bonus 6,000", pins=[("J1", 9)], wire="GREY", light=18),
	19: dict(id="lamp.bonus-10000", label="Bonus 10,000", pins=[("J1", 8)], wire="G-B", light=19),
	20: dict(id="lamp.center-bank-10000", label="Center bank target 10,000", pins=[("J1", 3)], wire="R-G", light=20),
	21: dict(id="lamp.bonus-3x", label="Bonus 3X", pins=[("J1", 2)], wire="PUR-W", light=21),
	22: dict(id="lamp.standup-l", label="Left stand-up target lamp L (SILVER)", pins=[("J1", 10)], wire="GREY-Y", light=22),
	23: dict(id="lamp.right-bank-3x", label="Right bank target 3X", pins=[("J1", 7)], wire="Y-G", light=23),
	24: dict(id="lamp.standup-v", label="Right stand-up target lamp V (SILVER)", pins=[("J1", 6)], wire="BRN-R", light=24),
	25: dict(id="lamp.unused-scr-q24", label="Unused lamp driver SCR Q24", pins=[], wire=None, light=None, availability="unused"),
	26: dict(id="lamp.top-rollover-divider-3", label="Top roll-over divider 3 (of 5, left to right)", pins=[("J1", 11)], wire="B-O", light=None, no_light="The retained table models no light for the five top dividers."),
	27: dict(id="lamp.unused-scr-q23", label="Unused lamp driver SCR Q23", pins=[], wire=None, light=None, availability="unused"),
	28: dict(id="lamp.top-lane-i", label="Top roll-over lane I lamp", pins=[("J2", 12)], wire="W-Y", light=28),
	29: dict(id="lamp.unused-scr-q15", label="Unused lamp driver SCR Q15", pins=[], wire=None, light=None, availability="unused"),
	30: dict(id="lamp.right-return-lanes", label="Right return lanes", pins=[("J2", 20)], wire="O-G", light=30),
	31: dict(id="lamp.right-special", label="Right special", pins=[("J2", 15)], wire="ORANGE", light=31),
	33: dict(id="lamp.bonus-3000", label="Bonus 3,000", pins=[("J3", 26)], wire="BLACK", light=33),
	34: dict(id="lamp.bonus-7000", label="Bonus 7,000", pins=[("J3", 25)], wire="R-Y", light=34),
	35: dict(id="lamp.bonus-20000", label="Bonus 20,000", pins=[("J3", 19)], wire="B-R", light=35),
	36: dict(id="lamp.center-bank-15000", label="Center bank target 15,000", pins=[("J3", 17)], wire="Y-BLU", light=36),
	37: dict(id="lamp.bonus-4x", label="Bonus 4X", pins=[("J3", 16)], wire="R-B", light=37),
	38: dict(id="lamp.standup-i", label="Left stand-up target lamp I (SILVER)", pins=[("J3", 23)], wire="W-GREY", light=38),
	39: dict(id="lamp.right-bank-4x", label="Right bank target 4X", pins=[("J3", 27)], wire="O-W", light=39),
	40: dict(id="lamp.standup-e", label="Right stand-up target lamp E (SILVER)", pins=[("J1", 13)], wire="W-BLU", light=40),
	41: dict(id="lamp.unused-scr-q42", label="Unused lamp driver SCR Q42", pins=[], wire=None, light=None, availability="unused"),
	42: dict(id="lamp.top-rollover-divider-2", label="Top roll-over divider 2 (of 5, left to right)", pins=[("J3", 20)], wire="W-O", light=None, no_light="The retained table models no light for the five top dividers."),
	43: dict(id="lamp.unused-scr-q40", label="Unused lamp driver SCR Q40", pins=[], wire=None, light=None, availability="unused"),
	44: dict(id="lamp.top-lane-u", label="Top roll-over lane U lamp", pins=[("J2", 4)], wire="PUR-B", light=44),
	45: dict(id="lamp.game-over", label="Game over", pins=[("J2", 11)], wire="O-G", light=None, backbox=True,
		notes="Backbox lamp, named by the Lamp Driver Schematic's list and by the known-working script (Controller.Lamp(45))."),
	46: dict(id="lamp.right-spinner", label="Right spinner", pins=[("J2", 6)], wire="YELLOW", light=46,
		notes="The right spinner's lamp. Instruction card: the spinner's value increases when the ball enters the opposite return lane and the lamp must be re-lit after hitting the spinner."),
	47: dict(id="lamp.top-special", label="Top special", pins=[("J2", 2)], wire="GREEN", light=47,
		notes="Next to the special roll-over button (switch 28) at the top right."),
	49: dict(id="lamp.bonus-4000", label="Bonus 4,000", pins=[("J3", 1)], wire="G-R", light=49),
	50: dict(id="lamp.bonus-8000", label="Bonus 8,000", pins=[("J3", 12)], wire="B-Y", light=50),
	51: dict(id="lamp.super-bonus", label="Super bonus", pins=[("J3", 15)], wire="W-B", light=51, notes="Presumably the 75,000 bonus step of the instruction card, which lights after the 20,000 step; no source ties the lamp to that amount by name."),
	52: dict(id="lamp.center-bank-20000", label="Center bank target 20,000", pins=[("J3", 11)], wire="WHITE", light=52),
	53: dict(id="lamp.bonus-5x", label="Bonus 5X", pins=[("J3", 9)], wire="W-R", light=53),
	54: dict(id="lamp.standup-s", label="Left stand-up target lamp S (SILVER)", pins=[("J3", 3)], wire="GREEN", light=54),
	55: dict(id="lamp.right-bank-5x", label="Right bank target 5X", pins=[("J3", 4)], wire="R-W", light=55),
	56: dict(id="lamp.standup-r", label="Right stand-up target lamp R (SILVER)", pins=[("J3", 2)], wire="Y-B", light=56),
	57: dict(id="lamp.top-rollover-divider-5", label="Top roll-over divider 5 (of 5, right)", pins=[("J3", 10)], wire="GREY-B", light=None, no_light="The retained table models no light for the five top dividers."),
	58: dict(id="lamp.top-rollover-divider-1", label="Top roll-over divider 1 (of 5, left)", pins=[("J3", 18)], wire="R-BLU", light=None, no_light="The retained table models no light for the five top dividers."),
	59: dict(id="lamp.standup-k", label="Lane stand-up target lamp K (QUICK)", pins=[("J2", 5)], wire="B-Y", light=59),
	60: dict(id="lamp.top-lane-q", label="Top roll-over lane Q lamp", pins=[("J2", 3)], wire="B-W", light=60),
	61: dict(id="lamp.tilt", label="Tilt", pins=[("J2", 10)], wire="GREY-B", light=None, backbox=True,
		notes="Backbox lamp, named by the Lamp Driver Schematic's list and by the known-working script (Controller.Lamp(61))."),
	62: dict(id="lamp.left-spinner", label="Left spinner", pins=[("J2", 7)], wire="BLU-W", light=62,
		notes="The playfield list prints jack J2 pin 6 for both spinner lamps; the Lamp Driver Schematic's copy strikes the left spinner's 6 out by hand and writes 7, which is the pin used. The two retained tables place this lamp beside the left spinner."),
	63: dict(id="lamp.match", label="Match", pins=[("J2", 1)], wire="GREY-Y", light=None, backbox=True,
		notes="Backbox lamp, named by the Lamp Driver Schematic's list and by the known-working script (Controller.Lamp(63))."),
}

# --- Option switches -------------------------------------------------------------------------------------------------------

DIPS: dict[int, str] = {
	1: "Coin chute 1 credits per coin, selector bit 1 (see the credit catalog)",
	2: "Coin chute 1 credits per coin, selector bit 2",
	3: "Coin chute 1 credits per coin, selector bit 3",
	4: "Coin chute 1 credits per coin, selector bit 4",
	5: "Add-a-ball memory (ON = 3 or 5, OFF = 1 only)",
	6: "High score feature award (ON = replay, OFF = extra ball)",
	7: "Balls per game (ON = 5, OFF = 3)",
	8: "Maximum add-a-balls (ON = 5, OFF = 3)",
	9: "Coin chute 2 credits per coin, selector bit 1",
	10: "Coin chute 2 credits per coin, selector bit 2",
	11: "Coin chute 2 credits per coin, selector bit 3",
	12: "Coin chute 2 credits per coin, selector bit 4",
	13: "Five-ball extra-ball flashing lite (ON = start over each ball, OFF = retain)",
	14: "Background sound (ON = on, OFF = off)",
	15: "High game to date feature, selector bit 1 (code 0-3)",
	16: "High game to date feature, selector bit 2 (code 0-3)",
	17: "QUICK extra ball per game (ON = once, OFF = open ended)",
	18: "Maximum credits, selector bit 1 (10, 15, 25 or 40)",
	19: "Maximum credits, selector bit 2 (10, 15, 25 or 40)",
	20: "Credit display (ON = yes, OFF = no)",
	21: "Match feature (ON = yes, OFF = no)",
	22: "QUICK extra ball (ON = yes, OFF = no)",
	23: "Special lite alternation, selector bit 1 (code 0, 3, 2 or 1)",
	24: "Special lite alternation, selector bit 2 (code 0, 3, 2 or 1)",
	25: "Coin chute 3 credits per coin, selector bit 1",
	26: "Coin chute 3 credits per coin, selector bit 2",
	27: "Coin chute 3 credits per coin, selector bit 3",
	28: "Coin chute 3 credits per coin, selector bit 4",
	29: "QUICK SILVER special (ON = start fresh each ball, OFF = carry over)",
	30: "Special replay limit (ON = 1 per game, OFF = 1 per ball)",
	31: "Special award, selector bit 1 (none, extra ball, 100K, replay)",
	32: "Special award, selector bit 2 (none, extra ball, 100K, replay)",
}

DISPLAYS = (
	("display.player-1-score", "Player 1 score, seven digits", 0, 1, 7),
	("display.player-2-score", "Player 2 score, seven digits", 1, 9, 7),
	("display.player-3-score", "Player 3 score, seven digits", 2, 17, 7),
	("display.player-4-score", "Player 4 score, seven digits", 3, 25, 7),
	("display.credits", "Credits, two digits", 4, 35, 2),
	("display.match-ball-in-play", "Match and ball in play, two digits", 5, 38, 2),
)
