"""Reviewed literal data for the Williams Cyclone (1988) curation.

Every table here is a transcription of a cited source and is quoted in full in the excerpts under
``evidence/excerpts/williams.cyclone.1988/``: the manual's Switch-Matrix, Lamp-Matrix and Solenoid tables and
the Switches, Lamps and Solenoids/Flashers parts lists, and the lamp, switch and coil name tables decoded from the
U27 game ROM by ``tools/cyclone_rom_name_tables.py`` (identical in the L-1, L-4 and L-5 ROMs). The curator and the
runtime-evidence builder read these literals; nothing here is inferred.
"""

from __future__ import annotations

MACHINE_ID = "williams.cyclone.1988"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
DRIVER_IDS = ("cycln_l5", "cycln_l4", "cycln_l1")
ROM_ARCHIVE_SHA256 = {
	"cycln_l5": "8e1af710ea8e9c8b606c14221dfd418d5debd126c44a98d6f1c1aa2ab90516ff",
	"cycln_l4": "2cc2625a8e5b44e46ab71a9848aa2679f842c2b42b91f9fb4fbab08baf9a41e3",
	"cycln_l1": "e2d5a524287d35f26257ab33bfc033729036f2efb5652193b122f2e4a700beba",
}
ROM_U27 = {
	"cycln_l5": ("cycl_u27.l5", "0e04287e7d874917dcdc622ebca3782d350317355d4f55494079ca314236b731"),
	"cycln_l4": ("cycl_u27.l4", "ed6852ebf5bf8525aae37c53a6b3206dab1ad52b771f56ec3c1e82cc5344d058"),
	"cycln_l1": ("cycl_u27.l1", "bd14e2a2fc4c11732d8cef5029198ea373e19a1928e68819a68aed3dca90d1d8"),
}

# ---------------------------------------------------------------- ROM name tables (U27, all three revisions)

ROM_SWITCH_NAMES = {
	1: "PLUMB TILT", 2: "G. SCORE BOARD", 3: "CREDIT BUTTON", 4: "RIGHT COIN SW.", 5: "CENTER COIN SW.", 6: "LEFT COIN SW.",
	7: "SLAM TILT", 8: "HI.SCORE RESET", 9: "PLAYFLD. TILT", 10: "OUTHOLE", 11: "SCORE SPOOK H.", 12: "NOT USED",
	13: "BOMERNG. KICKER", 14: "TOP LANE 1", 15: "TOP LANE 2", 16: "TOP LANE 3", 17: "FERRIS WHEEL", 18: "C. DROP TARGET",
	19: "DUCKS TOP", 20: "DUCKS MIDDLE", 21: "DUCKS BOTTOM", 22: "B. TOSS TOP", 23: "B. TOSS MIDDLE", 24: "B. TOSS BOTTOM",
	25: "SHOOTER LANE", 26: "SHUTTLE KICKER", 27: "SHUTTLE BOT 25K", 28: "SHUTTLE 100K", 29: "SHUTTLE 25K",
	30: "SHUTTLE TOP  5K", 31: "ENTER COMET", 32: "SCORE COMET", 33: "NOT USED", 34: "SCORE CYCLONE", 35: "10 PT. R. BOT.",
	36: "10 PT. R. MID.", 37: "10 PT. R. TOP", 38: "NOT USED", 39: "NOT USED", 40: "NOT USED", 41: "M. WHEEL H. OPTO",
	**{address: "NOT USED" for address in range(42, 53)},
	53: "LEFT OUTLANE", 54: "RIGHT OUTLANE", 55: "LEFT RETURN", 56: "RIGHT RETURN", 57: "LEFT FLIPPER", 58: "RIGHT FLIPPER",
	59: "SPOT B. TOSS", 60: "LEFT JET", 61: "RIGHT JET", 62: "BOTTOM JET", 63: "LEFT KICKER", 64: "RIGHT KICKER",
}
ROM_LAMP_NAMES = {
	1: "HOLD", 2: "BONUS", 3: "DOUBLE", 4: "SCORES", 5: "CYCLONE 50K", 6: "CYCLONE 100K", 7: "CYCLONE GATEBON.",
	8: "RIDE COMET", 9: "FERRIS WHEEL", 10: "ADVANCE X", 11: "DUCKS 25K", 12: "DUCKS 50K", 13: "DUCKS LIT EX.B.",
	14: "TOP LANE 1", 15: "TOP LANE 2", 16: "TOP LANE 3", 17: "RIDE AGAIN", 18: "SPINS M. WHEEL", 19: "DUCKS TOP",
	20: "DUCKS MIDDLE", 21: "DUCKS BOTTOM", 22: "B. TOSS TOP", 23: "B. TOSS MIDDLE", 24: "B. TOSS BOTTOM",
	25: "LEFT OUTLANE", 26: "RIGHT OUTLANE", 27: "COMET 20K", 28: "COMET 40K", 29: "COMET 60K", 30: "COMET 80K",
	31: "COMET 100K", 32: "COMET MILLION", 33: "M. WHEEL TOP   1", 34: "M. WHEEL 2", 35: "M. WHEEL 3", 36: "M. WHEEL 4",
	37: "M. WHEEL RIGHT 5", 38: "M. WHEEL 6", 39: "M. WHEEL 7", 40: "M. WHEEL 8", 41: "M. WHEEL BOTTOM9", 42: "M. WHEEL 10",
	43: "M. WHEEL 11", 44: "M. WHEEL 12", 45: "M. WHEEL LEFT 13", 46: "M. WHEEL 14", 47: "M. WHEEL 15", 48: "M. WHEEL 16",
	49: "2 X", 50: "7 X", 51: "6 X", 52: "5 X", 53: "4 X", 54: "3 X", 55: "BACKGLS. MYSTERY", 56: "BACKGLS. WHEEL",
	57: "BACKGLS. 0.5 MIL.", 58: "BACKGLS. 1.0 MIL.", 59: "BACKGLS. 1.5 MIL.", 60: "BACKGLS. 2.0 MIL.",
	61: "BACKGLS. 2.5 MIL.", 62: "BACKGLS. 3.0 MIL.", 63: "BACKGLS. 3.5 MIL.", 64: "BACKGLS. 4.0 MIL.",
}
# Coil-test step -> (first record, second record); the second names the C-side load of an A/C pair.
ROM_COIL_STEPS = {
	1: ("OUTHOLE", "L.FERRIS JACKPOT"), 2: ("NOT USED", "R.FERRIS C. TEETH"), 3: ("SHUTTLE KICKER", "BCK. MID. L. EYE"),
	4: ("BOMERNG. KICKER", "CATS F.L. B. FIREW."), 5: ("C. DROP TARGET", "DUCK F.L. R. FIREW."), 6: ("NOT USED", "FERRIS FLASHER"),
	7: ("KNOCKER", "TOP RIT. R. EYE"), 8: ("NOT USED", "SPOOK H. L. FIREW."), 9: ("SPIN M.W. FLASHER", ""),
	10: ("PLAYFLD. G.I.", ""), 11: ("BACKBOX G.I.", ""), 12: ("ApC SELECT", ""), 13: ("BOMERNG. 1251", ""),
	14: ("BOMERNG. 1251", ""), 15: ("BOMERNG. 1251", ""), 16: ("FERRIS WHEEL", ""), 17: ("LEFT JET", ""),
	18: ("LEFT KICKER", ""), 19: ("RIGHT JET", ""), 20: ("RIGHT KICKER", ""), 21: ("BOTTOM JET", ""), 22: ("NOT USED", ""),
}
# The coil test steps over 13 and 14 (the Mystery Wheel stepper coils, which the Mystery Wheel Test drives instead).
COIL_TEST_SKIPPED_STEPS = (13, 14)

# ---------------------------------------------------------------- Switch-Matrix Table (PDF 34, printed 30)

SWITCH_COLUMNS = {
	1: ("Q45", "GRN-BRN", "1J8-1"), 2: ("Q49", "GRN-RED", "1J8-2"), 3: ("Q44", "GRN-ORN", "1J8-3"), 4: ("Q48", "GRN-YEL", "1J8-4"),
	5: ("Q43", "GRN-BLK", "1J8-5"), 6: ("Q47", "GRN-BLU", "1J8-7"), 7: ("Q42", "GRN-VIO", "1J8-8"), 8: ("Q46", "GRN-GRY", "1J8-9"),
}
SWITCH_ROWS = {
	1: ("WHT-BRN", "1J10-9"), 2: ("WHT-RED", "1J10-8"), 3: ("WHT-ORN", "1J10-7"), 4: ("WHT-YEL", "1J10-6"),
	5: ("WHT-GRN", "1J10-5"), 6: ("WHT-BLU", "1J10-3"), 7: ("WHT-VIO", "1J10-2"), 8: ("WHT-GRY", "1J10-1"),
}
SWITCH_MATRIX = {
	1: "Plumb Bob Tilt", 2: "Not Used", 3: "Credit Button", 4: "Right Coin Chute", 5: "Center Coin Chute", 6: "Left Coin Chute",
	7: "Slam Tilt", 8: "High-Score Reset", 9: "Playfield Tilt", 10: "Outhole", 11: "Score Spook House", 12: "Not Used",
	13: "Boomerang Kickbig", 14: "1 Lane", 15: "2 Lane", 16: "3 Lane", 17: "Ferris Wheel Entrance", 18: "Drop Target (center)",
	19: "Ducks (top)", 20: "Ducks (middle)", 21: "Ducks (bottom)", 22: "Ball Toss (top)", 23: "Ball Toss (middle)",
	24: "Ball Toss (bottom)", 25: "Ball Shooter Lane", 26: "Shuttle 10K (kickbig)", 27: "Shuttle 25K (bottom)", 28: "Shuttle 100K",
	29: "Shuttle 25K", 30: "Shuttle 5K (top)", 31: "Enter COMET Ramp", 32: "Score COMET Ramp", 33: "Not Used",
	34: "Score CYCLONE", 35: "10 pt (R. Bottom)", 36: "10 pt (R. Middle)", 37: "10 pt (R. Top)", 38: "Not Used",
	39: "Not Used", 40: "Not Used", 41: "Mystery Wheel Opto \"Home\" (Insert bd)", **{address: "Not Used" for address in range(42, 53)},
	53: "Left Outlane Ex. Ball", 54: "Right Outlane Ex. Ball", 55: "Left Return Lane", 56: "Right Return Lane",
	57: "Left Flipper Lane Change", 58: "Right Flipper Lane Change", 59: "Spot Ball Toss", 60: "Left Jet Bumper",
	61: "Right Jet Bumper", 62: "Bottom Jet Bumper", 63: "Left Kicker", 64: "Right Kicker",
}
# Switches parts list (PDF 40, printed 36): address -> (part number, description). "" is a blank cell.
SWITCH_PARTS = {
	1: ("A-8476", "Plumb Bob Tilt"), 2: ("Not Used", ""), 3: ("SW-1A-126", "Credit Button"), 4: ("27-1092", "R Coin Chute (USA)"),
	5: ("Not Used (USA)", "Center Coin Chute"), 6: ("27-1092", "L Coin Chute (USA)"), 7: ("27-1066", "Slam Tilt"),
	8: ("27-1008", "High Score Reset*"), 9: ("B-8306-1", "Playfield Tilt"), 10: ("17-1067", "Outhole"),
	11: ("5647-12073-01", "Score Spook House"), 12: ("Not Used", ""), 13: ("5647-12073-09", "Boomerang Kickbig"),
	14: ("5647-12073-10", "1 Gate/Lane"), 15: ("5647-12073-10", "2 Gate/Lane"), 16: ("5647-12073-10", "3 Gate/Lane"),
	17: ("5647-12073-10", "Ferris Wheel Entrance"), 18: ("C-11903-R", "1-bank Dr Tgt Opto"), 19: ("B-12039-5", "Duck target (top)"),
	20: ("B-12039-5", "Duck target (mid)"), 21: ("B-12039-5", "Duck target (bottom)"), 22: ("B-11696-5", "Ball Toss target (top)"),
	23: ("B-11696-5", "Ball Toss target (mid)"), 24: ("B-11696-5", "Ball Toss target (bottom)"),
	25: ("5647-12073-04", "Ball Shooter Lane"), 26: ("5647-12133-01", "Shuttle 10K (kickbig)"),
	27: ("5647-12073-10", "Shuttle 25K (lower)"), 28: ("5647-12073-10", "Shuttle 100K"), 29: ("5647-12073-10", "Shuttle 25K (upper)"),
	30: ("5647-12073-10", "Shuttle 5K (topmost)"), 31: ("SW-1A-171", "Enter Comet Ramp"), 32: ("5647-12133-04", "Score Comet Ramp"),
	33: ("Not Used", ""), 34: ("5647-12133-07", "Score Cyclone (ramp)"), 35: ("B-4834-K", "10 pt (bottom right)"),
	36: ("B-4834-K", "10 pt (mid right)"), 37: ("B-4834-K", "10 pt (top right)"), 38: ("Not Used", ""), 39: ("Not Used", ""),
	40: ("Not Used", ""), 41: ("5490-10159-00", "Mystery Wheel Opto**"), **{address: ("Not Used", "") for address in range(42, 53)},
	53: ("5647-12073-10", "Left Outlane (drain)"), 54: ("5647-12073-10", "Right Outlane (drain)"),
	55: ("5647-12073-10", "Left Return Lane"), 56: ("5647-12073-10", "Right Return Lane"), 57: ("B-9951-1", "L Flipper Lane Change"),
	58: ("B-9951", "R Flipper Lane Change"), 59: ("B-12001-4", "Score Ball Toss Tgt"), 60: ("SW-11A-37", "Jet Bumper (left)"),
	61: ("SW-11A-37", "Jet Bumper (right)"), 62: ("SW-11A-37", "Jet Bumper (bottom)"), 63: ("", "Left Kicker***"),
	64: ("", "Right Kicker***"),
}
UNUSED_SWITCHES = frozenset({2, 12, 33, 38, 39, 40} | set(range(42, 53)))

# ---------------------------------------------------------------- Lamp-Matrix Table (PDF 31, printed 27) and Lamps list (PDF 43)

LAMP_COLUMNS = {
	1: ("Q66", "YEL-BRN", "1J7-1"), 2: ("Q64", "YEL-RED", "1J7-2"), 3: ("Q62", "YEL-ORN", "1J7-3"), 4: ("Q60", "YEL-BLK", "1J7-4"),
	5: ("Q58", "YEL-GRN", "1J7-6"), 6: ("Q56", "YEL-BLU", "1J7-7"), 7: ("Q54", "YEL-VIO", "1J7-8"), 8: ("Q52", "YEL-GRY", "1J7-9"),
}
LAMP_ROWS = {
	1: ("Q80", "RED-BRN", "1J6-1"), 2: ("Q81", "RED-BLK", "1J6-2"), 3: ("Q82", "RED-ORN", "1J6-3"), 4: ("Q83", "RED-YEL", "1J6-5"),
	5: ("Q84", "RED-GRN", "1J6-6"), 6: ("Q85", "RED-BLU", "1J6-7"), 7: ("Q86", "RED-VIO", "1J6-8"), 8: ("Q87", "RED-GRY", "1J6-9"),
}
LAMP_MATRIX = {
	1: "HOLD", 2: "BONUS", 3: "DOUBLE", 4: "SCORES", 5: "CYCLONE 50K", 6: "CYCLONE 100K", 7: "CYCLONE Gate Bonus",
	8: "RIDE THE COMET (on ramp)", 9: "W/L SCORE FERRIS WHEEL BONUS", 10: "ADV. \"X\"", 11: "Balloon 25K (Ducks)",
	12: "Balloon 50K (Ducks)", 13: "Balloon LITES EX. BALL (Ducks)", 14: "1 (Gate Lane)", 15: "2 (Gate Lane)", 16: "3 (Gate Lane)",
	17: "RIDE AGAIN", 18: "SPINS MYSTERY WHEEL", 19: "Ducks (top)", 20: "Ducks (mid)", 21: "Ducks (bottom)", 22: "Ball Toss (top)",
	23: "Ball Toss (mid)", 24: "Ball Toss (bottom)", 25: "EXTRA BALL Left Outlane", 26: "EXTRA BALL Right Outlane",
	27: "COMET 20K", 28: "COMET 40K", 29: "COMET 60K", 30: "COMET 80K", 31: "COMET 100K", 32: "COMET 1 Million",
	33: "Mystery Wheel ( tdc-top dead center)", 34: "Mystery Wheel (22-1/2 deg rt of tdc)", 35: "Mystery Wheel (45 deg rt of tdc)",
	36: "Mystery Wheel (67-1/2 deg rt of tdc)", 37: "Mystery Wheel (90 deg rt of tdc)", 38: "Mystery Wheel (112-1/2 deg rt of tdc)",
	39: "Mystery Wheel (135 deg rt of tdc)", 40: "Mystery Wheel (157-1/2 deg rt of tdc)", 41: "Mystery Wheel (180 deg from tdc)",
	42: "Mystery Wheel (157-1/2 deg left of tdc)", 43: "Mystery Wheel (135 deg left of tdc)",
	44: "Mystery Wheel (112-1/2 deg left of tdc)", 45: "Mystery Wheel (90 deg left of tdc)",
	46: "Mystery Wheel (67-1/2 deg left of tdc)", 47: "Mystery Wheel (45 deg left of tdc)",
	48: "Mystery Wheel (22-1/2 deg left of tdc)", 49: "2X", 50: "7X", 51: "6X", 52: "5X", 53: "4X", 54: "3X",
	55: "MYSTERY (Backglass)", 56: "WHEEL (Backglass)", 57: "500,000 Bonus (Backglass)", 58: "1,000,000 Bonus (Backglass)",
	59: "1,500,000 Bonus (Backglass)", 60: "2,000,000 Bonus (Backglass)", 61: "2,500,000 Bonus (Backglass)",
	62: "3,000,000 Bonus (Backglass)", 63: "3,500,000 Bonus (Backglass)", 64: "4,000,000 Bonus (Backglass)",
}
LAMP_LIST = {
	1: "HOLD", 2: "BONUS", 3: "DOUBLE", 4: "SCORES", 5: "CYCLONE 50K", 6: "CYCLONE 100K", 7: "CYCLONE Gate Bonus",
	8: "RIDE THE COMET (on ramp)", 9: "W/L SCORE FERRIS WHEEL BONUS", 10: "ADV. \"X\"", 11: "25K Balloon (Ducks)",
	12: "50K Balloon (Ducks)", 13: "LITES EX. BALL Balloon (Ducks)", 14: "1 (Gate Lane)", 15: "2 (Gate Lane)", 16: "3 (Gate Lane)",
	17: "RIDE AGAIN", 18: "SPINS MYSTERY WHEEL", 19: "Ducks (top)", 20: "Ducks (mid)", 21: "Ducks (bottom)", 22: "Ball Toss (top)",
	23: "Ball Toss (mid)", 24: "Ball Toss (bottom)", 25: "EXTRA BALL (L Outlane)", 26: "EXTRA BALL (R Outlane)",
	27: "COMET 20K", 28: "COMET 40K", 29: "COMET 60K", 30: "COMET 80K", 31: "COMET 100K", 32: "COMET 1 MILLION",
	33: "Mystery Wheel (top)", 34: "Mystery Wheel (r of top 1)", 35: "Mystery Wheel (r of top 2)", 36: "Mystery Wheel (r of top 3)",
	37: "Mystery Wheel (right)", 38: "Mystery Wheel (below right 1)", 39: "Mystery Wheel (below right 2)",
	40: "Mystery Wheel (below right 3)", 41: "Mystery Wheel (bottom)", 42: "Mystery Wheel (l of bottom 1)",
	43: "Mystery Wheel (l of bottom 2)", 44: "Mystery Wheel (l of bottom 3)", 45: "Mystery Wheel (left)",
	46: "Mystery Wheel (above left 1)", 47: "Mystery Wheel (above left 2)", 48: "Mystery Wheel (above left 3)",
	49: "2X", 50: "7X", 51: "6X", 52: "5X", 53: "4X", 54: "3X", 55: "MYSTERY (backglass)", 56: "WHEEL (backglass)",
	57: "500,000 Bonus (backglass)", 58: "1,000,000 Bonus (backglass)", 59: "1,500,000 Bonus (backglass)",
	60: "2,000,000 Bonus (backglass)", 61: "2,500,000 Bonus (backglass)", 62: "3,000,000 Bonus (backglass)",
	63: "3,500,000 Bonus (backglass)", 64: "4,000,000 Bonus (backglass)",
}
# The Lamp-Matrix Table: "Backglass Lamps: 33 - 48 and 55 - 64".
BACKGLASS_LAMPS = frozenset(set(range(33, 49)) | set(range(55, 65)))

# ---------------------------------------------------------------- Solenoid Table (PDF 2) and Solenoids/Flashers list (PDF 44)

# Solenoid Table row -> (description, type, wire colour, CPU board pin, playfield/cabinet connection, driver, part/lamp, qty).
# A C row's CPU cell prints only a second wire colour in parentheses; the A and C rows share the A row's CPU pin and the
# braced playfield cell.
SOLENOID_TABLE = {
	"01A": ("Outhole Kicker", "Switched", "Vio-Brn", "1P11-1", "8P3-1 (via 5J1-9, Aux Pwr Drvr Bd.)", "Q33", "AE-23-800", ""),
	"01C": ("L F Wheel (p) & Jackpot (b) Flashers", "Switched", "Blk-Brn", "(Gry-Brn)", "8P3-1 (via 5J1-9, Aux Pwr Drvr Bd.)", "Q33", "#89 flashlamps", "2b,1p"),
	"02A": ("", "Switched", "Vio-Red", "1P11-3", "8P3-2 (via 5J1-7, Aux Pwr Drvr Bd.)", "Q25", "", ""),
	"02C": ("R F Wheel (p) & Teeth (b) Flashers", "Switched", "Blk-Red", "(Gry-Red)", "8P3-2 (via 5J1-7, Aux Pwr Drvr Bd.)", "Q25", "#89 flashlamps", "1b,1p"),
	"03A": ("Ball Shooter Kickbig", "Switched", "Vio-Orn", "1P11-4", "8P3-3 (via 5J1-6, Aux Pwr Drvr Bd.)", "Q32", "AE-24-900", ""),
	"03C": ("Top mid (p) & L Eye (b) Flashers", "Switched", "Blk-Orn", "(Gry-Orn)", "8P3-3 (via 5J1-6, Aux Pwr Drvr Bd.)", "Q32", "#89 flashlamps", "1b,1p"),
	"04A": ("Boomerang Kickbig", "Switched", "Vio- Yel", "1P11-5", "8P3-4 (via 5J1-5, Aux Pwr Drvr Bd.)", "Q24", "AE-26-1500", ""),
	"04C": ("Cats (p) & lwr Fireworks (b) Flashers", "Switched", "Blk-Yel", "(Gry-Yel)", "8P3-4 (via 5J1-5, Aux Pwr Drvr Bd.)", "Q24", "#89 flashlamps", "1b,2p"),
	"05A": ("Drop Target", "Switched", "Vio-Grn", "1P11-6", "8P3-5 (via 5J1-4, Aux Pwr Drvr Bd.)", "Q31", "AE-23-800", ""),
	"05C": ("Ducks (p) & R Fireworks (b) Flashers", "Switched", "Blk-Grn", "(Gry-Grn)", "8P3-5 (via 5J1-4, Aux Pwr Drvr Bd.)", "Q31", "#89 flashlamps", "1b,2p"),
	"06A": ("", "Switched", "Vio-Blu", "1P11-7", "8P3-6 (via 5J1-3, Aux Pwr Drvr Bd.)", "Q23", "", ""),
	"06C": ("Ferris Wheel (p) Flashers", "Switched", "Blk-Blu", "(Gry-Blu)", "8P3-6 (via 5J1-3, Aux Pwr Drvr Bd.)", "Q23", "#89 flashlamps", "2p"),
	"07A": ("Knocker /Ticket Dispenser (b'box)", "Switched", "Vio-Blk", "1P11-8", "8P3-7 (via 5J1-2, Aux Pwr Drvr Bd.)", "Q30", "AE-26-1200", ""),
	"07C": ("Cyclone (p) & R Eye (b) Flashers", "Switched", "Blk-Vio", "(Gry-Vio)", "8P3-7 (via 5J1-2, Aux Pwr Drvr Bd.)", "Q30", "#89 flashlamps", "1b,1p"),
	"08A": ("", "Switched", "Vio-Gry", "1P11-9", "8P3-8 (via 5J1-1, Aux Pwr Drvr Bd.)", "Q22", "", ""),
	"08C": ("Spook H'se (p) & L F'works (b) Flashers", "Switched", "Blk-Gry", "(Gry-Blk)", "8P3-8 (via 5J1-1, Aux Pwr Drvr Bd.)", "Q22", "#89 flashlamps", "1b,1p"),
	"09": ("Spook House Bonus Flasher (p)", "Contrld", "Brn-Blk", "1P12-1", "8P3-9 (via 5J2-9)", "Q17", "#89 flashlamps", "1p"),
	"10": ("Playfield Gen Illumin Relay (p)", "Contrld", "Brn-Red", "1P12-2", "8P3-10 (via 5J2-8)", "Q9", "5580-09555-01", ""),
	"11": ("Backglass Gen Illumin Relay (b)", "Contrld", "Brn-Orn", "1P12-4", "6J3-1 (via 5J2-6)", "Q16", "5580-09555-01", ""),
	"12": ("Solenoid A/C Select Relay (b)", "Contrld", "Brn-Yel", "1P12-5", "8P3-12 (via 5J2-5)", "Q8", "5580-09555-01", ""),
	"13": ("Mystery Wheel (b) Coil B", "Contrld", "Brn-Grn", "1P12-6", "6J2-3 (B'box Conn Bd)", "Q15", "14-7948/D-12045", ""),
	"14": ("Mystery Wheel (b) Coil A", "Contrld", "Brn-Blu", "1P12-7", "6J2-4 (B'box Conn Bd)", "Q7", "14-7948/D-12045", ""),
	"15": ("Boomerang Flashers (p)", "Contrld", "Brn-Vio", "1P12-8", "8P3-15 (via 5J2-2)", "Q14", "#1251 lamps", "3p"),
	"16": ("Ferris Wheel Motor/Relay (p)", "Contrld", "Brn-Gry", "1P12-9", "8P3-16 (via 5J2-1)", "Q6", "14-7941-3/5580-12145-01", ""),
	"17": ("Left Jet Bumper", "Specl #1", "Blu-Brn", "1P19-7", "8P3-17 (via 5J3-7)", "Q75", "AE-23-800", ""),
	"18": ("Left Kicker (\"sling\")", "Specl #2", "Blu-Red", "1P19-4", "8P3-18 (via 5J3-6)", "Q71", "AE-26-1500", ""),
	"19": ("Right Jet Bumper", "Specl #3", "Blu-Orn", "1P19-3", "8P3-19 (via 5J3-3)", "Q73", "AE-23-800", ""),
	"20": ("Right Kicker (\"sling\")", "Specl #4", "Blu-Yel", "1P19-6", "8P3-20 (via 5J3-4)", "Q69", "AE-23-800", ""),
	"21": ("Bottom Jet Bumper", "Specl #5", "Blu-Grn", "1P19-8", "8P3-21 (via 5J3-2)", "Q77", "AE-26-1500", ""),
	"22": ("", "Specl #6", "Blu-Blk", "1P19-9", "", "Q79", "", ""),
}
# Solenoids/Flashers parts list (PDF 44): row -> (part number, description); "" is a blank cell.
SOLENOID_LIST = {
	"01A": ("AE-23-800", "Outhole Kicker"), "01C": ("#89 Flashlamp", "L F. Wheel (pf) & Jackpot (bb)"),
	"02A": ("", ""), "02C": ("#89 Flashlamp", "R F. Wheel (pf) & Teeth (bb)"),
	"03A": ("AE-24-900", "Ball Shooter Kickbig"), "03C": ("#89 Flashlamp", "Top mid (pf) & L Eye (bb)"),
	"04A": ("AE-26-1500", "Boomerang Kickbig"), "04C": ("#89 Flashlamp", "Cats (pf) & lwr Fireworks (bb)"),
	"05A": ("AE-23-800", "Drop Target"), "05C": ("#89 Flashlamp", "Ducks (pf) & R Fireworks (bb)"),
	"06A": ("", ""), "06C": ("#89 Flashlamp", "Ferris Wheel (pf)"),
	"07A": ("AE-26-1200", "Knocker (Ticket Dispenser)"), "07C": ("#89 Flashlamp", "Cyclone (pf) & R Eye (bb)"),
	"08A": ("", ""), "08C": ("#89 Flashlamp", "Sp'k Hse (pf) & L F'works (bb)"),
	"09": ("#89 Flashlamp", "Spins Mystery Wheel (pf)"), "10": ("5580-09555-01", "P'field General Illumin Relay*"),
	"11": ("5580-09555-01", "B'glass Gen. Illumin. Relay *"), "12": ("5580-09555-01", "Solenoid A/C Select Relay**"),
	"13": ("", "Mystery Wheel (bb) Coil A"), "14": ("", "Mystery Wheel (bb) Coil B"), "15": ("#1251 Flashlamp", "Boomerang Flasher"),
	"16": ("5580-12145-01", "Ferris Wheel Motor/Relay***"), "17": ("AE-23-800", "Left Jet Bumper"),
	"18": ("AE-26-1500", "Left Kicker (\"Sling\")"), "19": ("AE-23-800", "Right Jet Bumper"),
	"20": ("AE-26-1500", "Right Kicker (\"Sling\")"), "21": ("AE-23-800", "Bottom Jet Bumper"), "22": ("", ""),
}


def solenoid_row(address: int) -> str:
	"""The printed Solenoid Table row of a public solenoid address (pinned updsol: A 1-8, C 25-32)."""
	if 1 <= address <= 8:
		return f"{address:02d}A"
	if 25 <= address <= 32:
		return f"{address - 24:02d}C"
	if 9 <= address <= 22:
		return f"{address:02d}"
	raise KeyError(address)
