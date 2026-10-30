"""Reviewed Space Shuttle (Williams, 1984) facts, read from this game's instruction manual.

Every row below is a transcription of a table retained as an excerpt under
evidence/excerpts/williams.space-shuttle.1984/. Matrix numbers are the public
PinMAME addresses: the ROM's own switch and solenoid tests display them (see the
runtime evidence). Labels are normalized; the literal printed cells stay in the
excerpts.
"""

MACHINE_ID = "williams.space-shuttle.1984"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
MANUAL_SHA256 = "c34624cea38e2df1ec98283aecae56abd37ea497208aa31668d631a9580ca239"
MANUAL_FILENAME = "Williams_1984_Space_Shuttle_Instruction_Manual_dated_Nov_3_1984_with_schematics.pdf"
ROM_SHA256 = {
	"sshtl_l7": "fb3d2b8c71823fb11eef70129f2450ac062286743f9c00324ab01162818abc24",
	"sshtl_l3": "6274b70f796b05be1db16c0c11fcda526f29e1fb5be5cf5b28b13e32c7c70fda",
}

# Switch drives and returns as the System 9 CPU schematic (16-8923) and the cabinet sheet wire them. The
# manual's Switch-Matrix Table prints the returns 1J10-1, -3, -4, -5, -6, -7, -8, -9 for rows 1-8, which is the
# schematic's order reversed and uses the key pin 1J10-4; the excerpt keeps the printed cells.
SWITCH_COLUMNS = [("GRN-BRN", "1J8-1"), ("GRN-RED", "1J8-2"), ("GRN-ORN", "1J8-3"), ("GRN-YEL", "1J8-4"),
                  ("GRN-BLK", "1J8-5"), ("GRN-BLU", "1J8-7"), ("GRN-VIO", "1J8-8"), ("GRN-GRY", "1J8-9")]
SWITCH_ROWS = [("WHT-BRN", "1J10-9"), ("WHT-RED", "1J10-8"), ("WHT-ORN", "1J10-7"), ("WHT-YEL", "1J10-6"),
               ("WHT-GRN", "1J10-5"), ("WHT-BLU", "1J10-3"), ("WHT-VIO", "1J10-2"), ("WHT-GRY", "1J10-1")]
SWITCH_ROWS_PRINTED = ["1J10-1", "1J10-3", "1J10-4", "1J10-5", "1J10-6", "1J10-7", "1J10-8", "1J10-9"]
# Lamp strobes and returns as the CPU schematic wires them (1J7-5 and 1J6-4 are key pins). The Lamp-Matrix
# Table prints column 4 on 1J7-5 and row 4 on 1J6-4; the excerpt keeps the printed cells.
LAMP_COLUMNS = [("YEL-BRN", "1J7-1"), ("YEL-RED", "1J7-2"), ("YEL-ORN", "1J7-3"), ("YEL-BLK", "1J7-4"),
                ("YEL-GRN", "1J7-6"), ("YEL-BLU", "1J7-7"), ("YEL-VIO", "1J7-8"), ("YEL-GRY", "1J7-9")]
LAMP_ROWS = [("RED-BRN", "1J6-1"), ("RED-BLK", "1J6-2"), ("RED-ORN", "1J6-3"), ("RED-YEL", "1J6-5"),
             ("RED-GRN", "1J6-6"), ("RED-BLU", "1J6-7"), ("RED-VIO", "1J6-8"), ("RED-GRY", "1J6-9")]

# address: (normalized label, literal matrix cell, switch-location item function, assembly, switch type, location)
SWITCHES = {
	1: ("Plumb Bob Tilt", "Plumb-Tilt", "Plumb Tilt", "A-8476", "tilt", "cabinet"),
	2: ("Ball Roll Tilt", "Ball-Roll Tilt", "Ball Roll Tilt", "B-8537", "tilt", "cabinet"),
	3: ("Credit Button", "Credit Button", "Credit Button", "B-8536", "button", "cabinet"),
	4: ("Right Coin Switch", "Right Coin", "Right Coin Switch", "5647-10141-00", "leaf", "cabinet"),
	5: ("Center Coin Switch", "Center Coin", "Center Coin Switch", "Blank for Domestic", "leaf", "cabinet"),
	6: ("Left Coin Switch", "Left Coin", "Left Coin Switch", "5647-10141-00", "leaf", "cabinet"),
	7: ("Slam Tilt", "Slam Tilt", "Slam Tilt", "SW-1A-127", "tilt", "cabinet"),
	8: ("High Score Reset", "High-Score Reset", "High Score Reset", "5641-09369-00", "button", "cabinet"),
	9: ("Outhole", "Outhole", "Outhole", "A-10417", "leaf", "playfield"),
	10: ("Ball Ramp Top (Trough)", "Top Ball Ramp", "Upper Left Ball Ramp", "5647-09957-00", "other", "playfield"),
	11: ("Ball Ramp Middle (Trough)", "Middle Ball Ramp", "Center Ball Ramp", "5647-09957-00", "other", "playfield"),
	12: ("Ball Ramp Lower (Trough, Release Position)", "Lower Ball Ramp", "Lower Right Ball Ramp", "H-8659", "leaf", "playfield"),
	13: ("Right Outlane", "Right Outlane", "Right Outlane", "B-8677", "leaf", "playfield"),
	14: ("Left Flipper Return Lane", "Left Flipper Ret", "Left Flipper Return Lane", "B-8410", "leaf", "playfield"),
	15: ("Right Flipper Return Lane", "Right Flipper Ret", "Right Flipper Return Lane", "B-8677", "leaf", "playfield"),
	16: ("Left Eject Hole", "Left Eject-Hole", "Left Eject Hole", "A-9381-L", "leaf", "playfield"),
	17: ("SHUTTLE Target S", "S Target", "\"S\" Target", "A-9618", "leaf", "playfield"),
	18: ("SHUTTLE Target H", "H Target", "\"H\" Target", "A-9618", "leaf", "playfield"),
	19: ("SHUTTLE Target U", "U Target", "\"U\" Target", "A-9618", "leaf", "playfield"),
	20: ("SHUTTLE T Drop Target", "T Drop Tgt", "\"T\" Target", "A-9613", "leaf", "playfield"),
	21: ("SHUTTLE Target T", "T Target", "\"T\" Target", "A-9618", "leaf", "playfield"),
	22: ("SHUTTLE Target L", "L Target", "\"L\" Target", "A-9618", "leaf", "playfield"),
	23: ("SHUTTLE Target E", "E Target", "\"E\" Target", "A-9618", "leaf", "playfield"),
	24: ("Right Eject Hole", "Right Eject Hole", "Right Eject Hole", "A-9381-R", "leaf", "playfield"),
	25: ("Left Jet Bumper", "Left Jet", "Left Jet Bumper", "B-8928", "leaf", "playfield"),
	26: ("Right Jet Bumper", "Right Jet", "Right Jet Bumper", "B-8928", "leaf", "playfield"),
	27: ("Lower Jet Bumper", "Lower Jet", "Bottom Jet Bumper", "B-8928", "leaf", "playfield"),
	28: ("Left Outlane", "Left Outlane", "Left Outlane", "B-8410", "leaf", "playfield"),
	29: ("Top Lane U", "U Lane", "\"U\" Lane", "B-8410", "leaf", "playfield"),
	30: ("Top Lane S", "S Lane", "\"S\" Lane", "B-8410", "leaf", "playfield"),
	31: ("Top Lane A", "A Lane", "\"A\" Lane", "B-8410", "leaf", "playfield"),
	32: ("Long Ramp Upper Switch", "Ramp (Upper SW)", "Long Ramp Upper Switch", "B-8410-1", "leaf", "playfield"),
	33: ("Left Drop Target", "Left Drop-Tgt", "Left Drop Target", "A-9417", "leaf", "playfield"),
	34: ("Center Drop Target", "Center Drop-Tgt", "Center Drop Target", "A-9417", "leaf", "playfield"),
	35: ("Right Drop Target", "Right Drop-Tgt", "Right Drop Target", "A-9417", "leaf", "playfield"),
	36: ("Ball Shooter Lane", "Ball-Shooter Lane", "Ball Shooter Switch", "B-8677", "leaf", "playfield"),
	37: ("Spinner", "Spinner", "Spinner", "B-8307", "leaf", "playfield"),
	38: ("Ramp Bull's-Eye Target", "Ramp Bull's-eye", "Ramp Bulls Eye", "A-10618", "leaf", "playfield"),
	39: ("Left Kicker (Slingshot)", "Left Kicker", "Left Kicker", "B-8284", "leaf", "playfield"),
	40: ("Right Kicker (Slingshot)", "Right Kicker", "Right Kicker", "B-8284", "leaf", "playfield"),
	41: ("Lane Change (Right Flipper)", "Flipper (Lane Chg)", "Right Flipper Lane Change", "B-9951", "leaf", "playfield"),
	42: ("Bottom Left Standup", "Bot-L Standup Sw", "Bottom Left Standup Switch", "B-4834-K", "leaf", "playfield"),
	43: ("Left Lower Standup", "Mid-L Lwr S/U Sw", "Left Lower Standup Switch", "B-4834-K", "leaf", "playfield"),
	44: ("Left Upper Standup", "Mid-L Upr S/U Sw", "Left Upper Standup Switch", "B-4834-K", "leaf", "playfield"),
	45: ("Long Ramp Lower Switch", "Ramp (Lower Sw)", "Long Ramp Lower Switch", "A-10594", "leaf", "playfield"),
	46: ("Center Standup", "Center Standup Sw", "Center Standup Switch", "A-4834-J", "leaf", "playfield"),
	47: ("Upper Right Standup", "Upr-R Standup Sw", "Upper Right Standup Switch", "A-4834-J", "leaf", "playfield"),
	48: ("Lower Right Standup", "Lwr-R Standup Switch", "Lower Right Standup Switch", "B-4834-K", "leaf", "playfield"),
	49: ("Playfield Tilt", "Play-Field Tilt", "Playfield Tilt", "B-8306", "tilt", "playfield"),
}
UNUSED_SWITCHES = frozenset(range(50, 65))
CABINET_SWITCHES = frozenset(range(1, 9))
# PinMAME's sxx.ssSw for sshtl: matrix switch -> special solenoid it publishes (s11games.c INITGAMEFULL).
PINMAME_SPECIAL_SWITCH_SOLENOIDS = {39: 17, 40: 18, 27: 19, 26: 20, 25: 21}
# The manual's physical pairing: special solenoid -> the matrix switch on the same device
# (solenoid table, solenoid and switch location drawings, playfield special-switch wiring diagram).
PHYSICAL_SPECIAL_SWITCH = {17: 39, 18: 40, 19: 25, 20: 27, 21: 26}

# address: (literal function, wire, CPU connection, playfield/cabinet connection, printed transistor, part)
SOLENOIDS = {
	1: ("Outhole", "GRY-BRN", "1P11-1", "8P3-1", "Q47", "SA-23-850-DC"),
	2: ("Ball-Ramp Release", "GRY-RED", "1P11-3", "8P3-2", "Q46", "SG 1-23-850-DC"),
	3: ("Left Eject-Hole", "GRY-ORN", "1P11-4", "8P3-3", "Q49", "SG 1-23-850-DC"),
	4: ("Right Eject-Hole", "GRY-YEL", "1P11-5", "8P3-4", "Q50", "SG 1-23-850-DC"),
	5: ("\"T\" Drop-Target", "GRY-GRN", "1P11-6", "8P3-5", "Q39", "SA 5-24-750-DC"),
	6: ("3-Bank Drop-Target", "GRY-BLU", "1P11-7", "8P3-6", "Q40", "SA 3-23-850-DC"),
	7: ("Up Post", "GRY-VIO", "1P11-8", "8P3-7", "Q41", "SG-23-850-DC"),
	8: ("Down Post", "GRY-BLK", "1P11-9", "8P3-8", "Q42", "SM-29-1100-DC"),
	9: ("Space Flash-Lamps", "BRN-BLK", "1P12-1", "8P3-9", "Q54", None),
	10: ("Shuttle Flash-Lamps", "BRN-RED", "1P12-2", "8P3-10", "Q55", None),
	11: ("General Illumination", "BRN-ORN", "1P12-4", "3P7-1", "Q56", "5580-09555-00"),
	12: ("Not Used", "BRN-YEL", "1P12-5", "8P3-12", "Q57", None),
	13: ("Gate", "BRN-GRN", "1P12-6", "8P3-13", "Q58", "SZ-35-4000-DC"),
	14: ("Insert Flash-Lamps", "BRN-BLU", "1P12-7", "8P3-14", "Q59", None),
	15: ("Bell", "BRN-VIO", "1P12-8", "7P1-17", "Q60", "SM-29-1000-DC"),
	16: ("Coin-Lockout Coil", "BRN-GRY", "1P12-9", "7P1-18, 7P2-4", "Q61", "SM-35-4000-DC"),
	17: ("Left Kicker", "BLU-BRN", "1P-19-7", "8P3-17", "Q75", "SG1-23-850-DC"),
	18: ("Right Kicker", "BLU-RED", "1P-19-4", "8P3-18", "Q77", "SG1-23-850-DC"),
	19: ("Left Jet-Bumper", "BLU-ORN", "1P-19-3", "8P3-19", "Q79", "SG1-23-850-DC"),
	20: ("Lower Jet-Bumper", "BLU-YEL", "1P-19-6", "8P3-20", "Q81", "SG1-23-850-DC"),
	21: ("Right Jet-Bumper", "BLU-GRN", "1P-19-8", "8P3-12", "Q83", "SG1-23-850-DC"),
	22: ("Not Used", "BLU-BLK", "1P-19-9", "8P3-22", "Q85", None),
}
# Where the playfield-solenoid wiring diagram (PDF 17) differs from the table's cell, the diagram's reading.
SOLENOID_DIAGRAM = {2: ("transistor", "Q48"), 21: ("playfield", "8P3-21")}
UNUSED_SOLENOIDS = frozenset({12, 22})
# Note 1 of the solenoid table (printed connector 2P1) against the special-switch inputs the playfield
# wiring diagram draws on the CPU board (1J18/1P18) and the playfield plug 8P3.
SPECIAL_SWITCH_WIRING = {17: ("ORN-BRN", "2P1-5", "1J18-5", "8P3-24", "8SW65 Left Kicker"),
                         18: ("ORN-RED", "2P1-7", "1J18-3", "8P3-25", "8SW66 Right Kicker"),
                         19: ("ORN-BLK", "2P1-8", "1J18-2", "8P3-26", "8SW67 Left Jet Bumper"),
                         20: ("ORN-YEL", "2P1-6", "1J18-4", "8P3-27", "8SW68 Lower Jet Bumper"),
                         21: ("ORN-GRN", "2P1-2", "1J18-8", "8P3-28", "8SW69 Right Jet Bumper")}

# address: (normalized label, literal matrix cell, lamp-location item function, assembly, location)
LAMPS = {
	1: ("Game Over", "Game-Over", "Game Over", "A-8271", "backbox"),
	2: ("Match", "Match", "Match", "A-8271", "backbox"),
	3: ("Tilt", "Tilt", "Tilt", "A-8271", "backbox"),
	4: ("High Score to Date", "High-Score-To-Date", "High-Score-To-Date", "A-8271", "backbox"),
	5: ("Shoot Again (Backglass)", "Shoot Again X2 (Insert)", "Shoot Again", "A8271 & A-8262", "backbox"),
	6: ("Ball in Play", "Ball-In-Play", "ball-In-Play", "A-8271", "backbox"),
	7: ("Up Post", "Up Post X2", "Up Post", "A-8882", "playfield"),
	8: ("Release Multi-Ball", "Release Multiball w/l", "Release", "A-8265", "playfield"),
	9: ("Bonus Multiplier 2X", "2X", "2X", "B-8443", "playfield"),
	10: ("Bonus Multiplier 3X", "3X", "3X", "B-8443", "playfield"),
	11: ("Bonus Multiplier 4X", "4X", "4X", "B-8443", "playfield"),
	12: ("Bonus Multiplier 5X", "5X", "5X", "B-8443", "playfield"),
	13: ("Bonus Multiplier 6X", "6X", "6X", "B-8443", "playfield"),
	14: ("Bonus Multiplier 7X", "7X", "7X", "B-8443", "playfield"),
	15: ("Flipper Return Lanes", "Flipper-Return Lns", "Flipper Return Lanes", "A-8265", "playfield"),
	16: ("Left Lock", "Left Lock", "Left Lock", "A-8265", "playfield"),
	17: ("SHUTTLE S", "S", "\"S\"", "B-8443", "playfield"),
	18: ("SHUTTLE H", "H", "\"H\"", "B-8443", "playfield"),
	19: ("SHUTTLE U", "U", "\"U\"", "B-8443", "playfield"),
	20: ("SHUTTLE T (Drop Target)", "T", "\"T\"", "A-8449", "playfield"),
	21: ("SHUTTLE T", "T", "\"T\"", "B-8443", "playfield"),
	22: ("SHUTTLE L", "L", "\"L\"", "B-8443", "playfield"),
	23: ("SHUTTLE E", "E", "\"E\"", "B-8443", "playfield"),
	24: ("Right Lock", "Right Lock", "Right Lock", "A-8265", "playfield"),
	25: ("Left Jet Bumper", "L/Jet Bumper", "Left Jet Bumper", "24-6416 & 24-6549", "playfield"),
	26: ("Right Jet Bumper", "R/Jet Bumper", "Right Jet Bumper", "24-6416", "playfield"),
	27: ("Bottom Jet Bumper", "Bot Jet Bumper", "Bottom Bumper", "24-6416", "playfield"),
	28: ("Gate Open", "Gate Open", "Gate Open", "A-8265", "playfield"),
	29: ("Top Lane U", "U Lane", "\"U\" Lane", "B-9558-40", "playfield"),
	30: ("Top Lane S", "S Lane", "\"S\" Lane", "B-9558-40", "playfield"),
	31: ("Top Lane A", "A Lane", "\"A\" Lane", "B-9558-40", "playfield"),
	32: ("Bonus Holdover", "Bonus Holdover", "Bonus Holdover", "A-8265", "playfield"),
	33: ("Spinner 1,000", "Spinner 1000", "Spinner 1,000", "A-8265", "playfield"),
	34: ("Spinner 2,000", "Spinner 2000", "Spinner 2,000", "A-8449", "playfield"),
	35: ("Spinner 4,000", "Spinner 4000", "Spinner 4,000", "A-8449", "playfield"),
	36: ("Extra Ball When Lit", "Ex Ball When Lit", "Extra Ball When Lit", "A-8265", "playfield"),
	37: ("Shoot Again (Playfield)", "Shoot Again (Pl)", "Shoot Again", "A-8265", "playfield"),
	38: ("Stop & Score X2 (Backglass)", "Stop & Score X2 (Insrt)", "Stop & Score", "A-8271 & A-8262", "backbox"),
	39: ("Tail Engine (Backglass)", "Insrt Tail Eng", "Insert Panel", "A-8271", "backbox"),
	40: ("Tail Engine X2 (Backglass)", "Insrt Tail Eng X2", "Insert Panel", "A-8271", "backbox"),
	41: ("Outlane Shuttle Arrow", "Outlane X2 Shut Arrow", "Outlane Shuttle Arrow", "A-8265", "playfield"),
	42: ("Shuttle 20,000", "Shuttle 20,000", "Shuttle 20,000", "B-9558-21", "playfield"),
	43: ("Shuttle 50,000", "Shuttle 50,000", "Shuttle 50,000", "B-9558-21", "playfield"),
	44: ("Shuttle 100,000", "Shuttle 100,000", "Shuttle 100,000", "B-9558-21", "playfield"),
	45: ("50,000 and Bonus Holdover", "50,000 Bonus H/O", "50,000 & Bonus H/Over", "B-9558-21", "playfield"),
	46: ("100,000 and Outlanes", "100,000 + Out-Lns", "100,000 + Outlanes", "B-8443", "playfield"),
	47: ("Extra Ball", "Extra Ball", "Extra Ball", "B-8443", "playfield"),
	48: ("Scores Special", "Scores Special", "Scores Special", "B-8443", "playfield"),
	49: ("Stop & Score X2 (Playfield)", "Stop & Score X2 Plfd", "Stop & Score", "A-8265", "playfield"),
	50: ("Bonus 1,000", "Bonus 1,000", "1,000 Bonus", "B-9558-33", "playfield"),
	51: ("Bonus 2,000", "Bonus 2,000", "2,000 Bonus", "B-9558-32", "playfield"),
	52: ("Bonus 3,000", "Bonus 3,000", "3,000 Bonus", "B-9558-33", "playfield"),
	53: ("Bonus 4,000", "Bonus 4,000", "4,000 Bonus", "B-9558-33", "playfield"),
	54: ("Bonus 5,000", "Bonus 5,000", "5,000 Bonus", "B-9558-32", "playfield"),
	55: ("Bonus 6,000", "Bonus 6,000", "6,000 Bonus", "B-9558-33", "playfield"),
	56: ("Bonus 7,000", "Bonus 7,000", "7,000 Bonus", "B-9558-33", "playfield"),
	57: ("Bonus 8,000", "Bonus 8,000", "8,000 Bonus", "B-9558-32", "playfield"),
	58: ("Bonus 9,000", "Bonus 9,000", "9,000 Bonus", "B-9558-33", "playfield"),
	59: ("Bonus 10,000", "Bonus 10,000", "10,000 Bonus", "B-9558-33", "playfield"),
	60: ("Bonus 20,000", "Bonus 20,000", "20,000 Bonus", "B-9558-32", "playfield"),
	61: ("Bonus 30,000", "Bonus 30,000", "30,000 Bonus", "B-9558-33", "playfield"),
	62: ("Bonus 40,000", "Bonus 40,000", "40,000 Bonus", "B-9558-33", "playfield"),
	63: ("Bonus 50,000", "Bonus 50,000", "50,000 Bonus", "B-9558-32", "playfield"),
	64: ("Bonus 60,000", "Bonus 60,000", "60,000 Bonus", "B-9558-33", "playfield"),
}
# Lamp-location assembly cells printed as something other than the part number: a ditto mark repeating the
# nearest assembly above, or a 'See NN' reference to the first lamp of the same bonus-ladder column.
LAMP_ASSEMBLY_PRINTED = {
	2: '"', 3: '"', 4: '"', 10: '"', 11: '"', 12: '"', 13: '"', 14: '"', 16: '"', 18: '"',
	19: '"', 22: '"', 23: '"', 27: '"', 30: '"', 31: '"', 33: '"', 35: '"', 37: '"', 40: '"',
	43: '"', 44: '"', 45: '"', 47: '"', 48: '"', 53: "See 50", 54: "See 51", 55: "See 52", 56: "See 50", 57: "See 51",
	58: "See 52", 59: "See 50", 60: "See 51", 61: "See 52", 62: "See 50", 63: "See 51", 64: "See 52",
}
# Lamps the playfield lamp-location drawing shows twice (two sockets on one matrix address).
TWIN_LAMPS = {15: ("left", "right"), 41: ("left", "right")}
