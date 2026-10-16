"""Reviewed Sorcerer (Williams, 1985) facts, read from this game's instruction manual.

Every row below is a transcription of a table retained as an excerpt under
evidence/excerpts/williams.sorcerer.1985/. Matrix numbers are the public
PinMAME addresses: the ROM's own switch and solenoid tests display them (see the
runtime evidence). Labels are normalized; the literal printed cells stay in the
excerpts.
"""

MACHINE_ID = "williams.sorcerer.1985"
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
MANUAL_SHA256 = "a21c55a9ddd7790eca35bef3b79061bffdb896d76395be29b0f3fad99899322c"
MANUAL_FILENAME = "Williams_1985_Sorcerer_Instruction_Manual_with_schematics.pdf"
ROM_SHA256 = {
	"sorcr_l1": "c28da13a9890f1501e74e1e1a39a1c1c8f213939ea65bb05737d9d8df4ad9c0a",
	"sorcr_l2": "a9c2a21dc660c5b81f373a233e22a3ff1adb1c88b357525d471328e348f5492f",
}

SWITCH_COLUMNS = [("GRN-BRN", "1J8-1"), ("GRN-RED", "1J8-2"), ("GRN-ORN", "1J8-3"), ("GRN-YEL", "1J8-4"),
                  ("GRN-BLK", "1J8-5"), ("GRN-BLU", "1J8-7"), ("GRN-VIO", "1J8-8"), ("GRN-GRY", "1J8-9")]
SWITCH_ROWS = [("WHT-BRN", "1J10-9"), ("WHT-RED", "1J10-8"), ("WHT-ORN", "1J10-7"), ("WHT-YEL", "1J10-6"),
               ("WHT-GRN", "1J10-5"), ("WHT-BLU", "1J10-3"), ("WHT-VIO", "1J10-2"), ("WHT-GRY", "1J10-1")]
LAMP_COLUMNS = [("YEL-BRN", "1J7-1"), ("YEL-RED", "1J7-2"), ("YEL-ORN", "1J7-3"), ("YEL-BLK", "1J7-4"),
                ("YEL-GRN", "1J7-6"), ("YEL-BLU", "1J7-7"), ("YEL-VIO", "1J7-8"), ("YEL-GRY", "1J7-9")]
LAMP_ROWS = [("RED-BRN", "1J6-1"), ("RED-BLK", "1J6-2"), ("RED-ORN", "1J6-3"), ("RED-YEL", "1J6-5"),
             ("RED-GRN", "1J6-6"), ("RED-BLU", "1J6-7"), ("RED-VIO", "1J6-8"), ("RED-GRY", "1J6-9")]

# address: (normalized label, literal matrix cell, switch-location item function, assembly, switch type, location)
SWITCHES = {
	1: ("Plumb Bob Tilt", "Plumb-Tilt", "Plumb tilt", "A-8476", "tilt", "cabinet"),
	2: ("Ball Roll Tilt", "Ball-Roll Tilt", "Ball Roll Tilt", "B-6572", "tilt", "cabinet"),
	3: ("Credit Button", "Credit Button", "Credit Button", "B-8536", "button", "cabinet"),
	4: ("Right Coin Switch", "Right Coin", "Right Coin Switch", "5647-10141-00", "leaf", "cabinet"),
	5: ("Center Coin Switch", "Center Coin", "Center Coin Switch", "BLANK FOR DOMESTIC", "leaf", "cabinet"),
	6: ("Left Coin Switch", "Left Coin", "Left Coin Switch", "5647-10141-00", "leaf", "cabinet"),
	7: ("Slam Tilt", "Slam Tilt", "Slam Tilt", "SW-1A-127", "tilt", "cabinet"),
	8: ("High Score Reset", "High-Score Reset", "High Score Reset", "5647-09957-00", "button", "cabinet"),
	9: ("Left Spinner S", "Left Spinner S", "Left Spinner, \"S\"", "B-8307", "leaf", "playfield"),
	10: ("SORCERER Target O", "O", "\"O\" Target", "A-9267", "leaf", "playfield"),
	11: ("SORCERER Target R", "R", "\"R\" Target", "A-9267", "leaf", "playfield"),
	12: ("SORCERER Target C", "C", "\"C\" Target", "A-9267", "leaf", "playfield"),
	13: ("SORCERER Target E (first)", "E", "\"E\" Target", "A-9267", "leaf", "playfield"),
	14: ("SORCERER Target R (second)", "R", "\"R\" Target", "A-9267", "leaf", "playfield"),
	15: ("SORCERER Target E (second)", "E", "\"E\" Target", "A-9267", "leaf", "playfield"),
	16: ("Right Spinner R", "Right Spinner R", "Right Spinner, \"R\"", "B-8307", "leaf", "playfield"),
	17: ("Top Lane A", "A", "\"A\"", "B-8410", "leaf", "playfield"),
	18: ("Top Lane B", "B", "\"B\"", "B-8410", "leaf", "playfield"),
	19: ("Top Lane C", "C", "\"C\"", "B-8410", "leaf", "playfield"),
	20: ("Top Lane D", "D", "\"D\"", "B-8410", "leaf", "playfield"),
	21: ("Left Jet Bumper", "Left Jet", "Left Jet Bumper", "B-8316", "leaf", "playfield"),
	22: ("Lower Jet Bumper", "Lower Jet", "Lower Jet Bumper", "B-8316", "leaf", "playfield"),
	23: ("Right Jet Bumper", "Right Jet", "Right Jet Bumper", "B-8316", "leaf", "playfield"),
	24: ("Left Drain (Outlane)", "Left Drain", "Left Drain", "B-8410", "leaf", "playfield"),
	25: ("Right Drain (Outlane)", "Right Drain", "Right Drain", "B-8410", "leaf", "playfield"),
	26: ("Left Flipper Return Lane", "Left Flpr Ret.", "Left Flipper Return", "B-8410", "leaf", "playfield"),
	27: ("Right Flipper Return Lane", "Right Flpr Ret.", "Right Flipper Return", "B-8410", "leaf", "playfield"),
	28: ("Outhole", "Outhole", "Outhole", "A-10417", "leaf", "playfield"),
	29: ("Ball Ramp 1 (Trough)", "Ramp 1", "Ramp 1", "B-8642", "leaf", "playfield"),
	30: ("Ball Ramp 2 (Trough, Eject Position)", "Ramp 2", "Ramp 2", "A-8659", "leaf", "playfield"),
	31: ("Shooter Lane", "Shooter Lane SW", "Shooter Lane", "B-8677", "leaf", "playfield"),
	32: ("Left Kicker (Slingshot)", "Left Kicker SW", "Left Kicker", "B-8284", "leaf", "playfield"),
	33: ("Right Kicker (Slingshot)", "Right Kicker", "Right Kicker", "B-8284", "leaf", "playfield"),
	34: ("Left Drop Target", "Left Drop-Tgt", "Left Drop Target", "A-9417", "leaf", "playfield"),
	35: ("Center Drop Target", "Center Drop-Tgt", "Center Drop Target", "A-9417", "leaf", "playfield"),
	36: ("Right Drop Target", "Right Drop-Tgt", "Right Drop Target", "A-9417", "leaf", "playfield"),
	37: ("Multi-Ball Lock (Ramp Eject)", "Multi-Ball Ramp", "Ramp Eject for MULTIBALL", "A-10590", "leaf", "playfield"),
	38: ("Multi-Ball Ramp Switch", "Multi Ball SW", "Ramp Switch for MULTIBALL", "A-8659", "leaf", "playfield"),
	39: ("Lower Right Switch", "Lower Right SW", "Lower Right Switch", "A-4834-K", "leaf", "playfield"),
	40: ("Lower Left Switch", "Lower Left SW", "Lower Left Switch", "A-4834-K", "leaf", "playfield"),
	42: ("Upper Left Switch", "UPR-L Switch", "Upper Left Switch", "A-4834-K", "leaf", "playfield"),
	43: ("Lamp Shift Lane", "Lane Switch", "Lamp Shift", "A-4834-J", "leaf", "playfield"),
	44: ("Lane Change (Right Flipper)", "Lane Change", "Lane Change", "B-9951", "leaf", "playfield"),
	45: ("Playfield Tilt", "Play-Field Tilt", "Playfield Tilt", "B-8306", "tilt", "playfield"),
}
UNUSED_SWITCHES = frozenset({41, *range(46, 65)})
CABINET_SWITCHES = frozenset(range(1, 9))
SPECIAL_SWITCH_SOLENOIDS = {32: 17, 33: 18, 21: 19, 22: 20, 23: 21}

# address: (literal function, solenoid type, wire, CPU connection, playfield/cabinet connection, transistor, part)
SOLENOIDS = {
	1: ("Outhole", "controlled", "GRY-BRN", "1J11-1", "8P3-1", "Q47", "SA-23-850-DC"),
	2: ("Ramp Eject", "controlled", "GRY-RED", "1J11-3", "8P3-2", "Q48", "SG1-23-850-DC"),
	3: ("Multi-Ball Eject", "controlled", "GRY-ORN", "1J11-4", "8P3-3", "Q49", "SG1-23-850-DC"),
	4: ("3-Bank Drop Target", "controlled", "GRY-YEL", "1J11-5", "8P3-4", "Q50", "SA-3-23-850-DC"),
	5: ("Demon Background", "controlled", "GRY-GRN", "1J11-6", "8P3-5", "Q39", "#63 Flashlamp"),
	6: ("3-Bank Flash", "controlled", "GRY-BLU", "1J11-7", "8P3-6", "Q40", "#63 Flashlamp"),
	7: ("SORCERER Bank", "controlled", "GRY-VIO", "1J11-8", "8P3-7", "Q41", "#63 Flashlamp"),
	8: ("Flash Eyes (cabinet)", "controlled", "GRY-BLK", "1J11-9", "8P3-8", "Q42", "5580-08994-00"),
	9: ("Not Used", "controlled", "BRN-BLK", "1J12-1", "8P3-9", "Q54", None),
	10: ("Not Used", "controlled", "BRN-RED", "1J12-2", "8P3-10", "Q55", None),
	11: ("General Illumination", "controlled", "BRN-ORN", "1J12-4", "3P7-1", "Q56", "5580-09555-00"),
	12: ("Not Used", "controlled", "BRN-YEL", "1J12-5", "8P3-12", "Q57", None),
	13: ("Not Used", "controlled", "BRN-GRN", "1J12-6", "8P3-13", "Q58", None),
	14: ("Not Used", "controlled", "BRN-BLU", "1J12-7", "8P3-14", "Q59", "SA-4-23-850-DC"),
	15: ("Bell", "controlled", "BRN-VIO", "1J12-8", "7P1-17", "Q60", "SM-29-1000-DC"),
	16: ("Coin-Lockout Coil", "controlled", "BRN-GRY", "1P12-9", "7P1-18, 7P2-4", "Q61", "SM-35-4000-DC"),
	17: ("Left Kicker", "special #1", "BLU-BRN", "1J19-7", "8P3-17", "Q75", "SG1-23-850-DC"),
	18: ("Right Kicker", "special #2", "BLU-RED", "1J19-4", "8P3-18", "Q77", "SG1-23-850-DC"),
	19: ("Left Jet-Bumper", "special #3", "BLU-ORN", "1J19-3", "8P3-19", "Q79", "SG1-23-850-DC"),
	20: ("Lower Jet-Bumper", "special #4", "BLU-YEL", "1J19-6", "8P3-20", "Q81", "SG1-23-850-DC"),
	21: ("Right Jet-Bumper", "special #5", "BLU-GRN", "1J19-8", "8P3-21", "Q83", "SG1-23-850-DC"),
	22: ("Not Used", "special #6", "BLU-BLK", "1J19-9", "8P3-22", "Q85", None),
}
# Note 1 of the solenoid table: special-switch connections for 17-21.
SPECIAL_SWITCH_WIRING = {17: ("ORN-BRN", "1J18-5", "8P3-24"), 18: ("ORN-RED", "1J18-3", "8P3-25"),
                         19: ("ORN-BLK", "1J18-2", "8P3-26"), 20: ("ORN-YEL", "1J18-4", "8P3-27"),
                         21: ("ORN-GRN", "1J18-8", "8P3-28")}
UNUSED_SOLENOIDS = frozenset({9, 10, 12, 13, 14, 22})

# address: (normalized label, literal matrix cell, lamp-location item function, assembly, location)
LAMPS = {
	1: ("Game Over", "Game Over Lamp", "Game Over", "A-8262", "backbox"),
	2: ("Match", "Match", "Match", "A-8262", "backbox"),
	3: ("Tilt", "Tilt", "Tilt", "A-8262", "backbox"),
	4: ("High Score to Date", "High-Score-To-Date", "High Score to Date", "A-8262", "backbox"),
	5: ("Shoot Again (Backglass)", "Shoot Again (Insert)", "Shoot Again (Backglass}", "A-8262", "backbox"),
	6: ("Ball in Play", "Ball-In-Play", "Ball-in-Play", "A-8262", "backbox"),
	7: ("Shoot Again (Playfield)", "Shoot Again (Pfld)", "Shoot Again (Playfield)", "A-8265", "playfield"),
	8: ("Playfield Special", "Play-field Special", "Special", "A-8265", "playfield"),
	9: ("SORCERER S", "S", "\"S\"", "B-9558-41", "playfield"),
	10: ("SORCERER O", "O", "\"O\"", "B-8445", "playfield"),
	11: ("SORCERER R (first)", "R", "\"R\"", "B-8445", "playfield"),
	12: ("SORCERER C", "C", "\"C\"", "B-8445", "playfield"),
	13: ("SORCERER E (first)", "E", "\"E\"", "B-8443", "playfield"),
	14: ("SORCERER R (second)", "R", "\"R\"", "B-8443", "playfield"),
	15: ("SORCERER E (second)", "E", "\"E\"", "B-8443", "playfield"),
	16: ("SORCERER R (third)", "R", "\"R\"", "A-8265", "playfield"),
	17: ("Top Lane A", "A", "\"A\"", "A-8265", "playfield"),
	18: ("Top Lane B", "B", "\"B\"", "A-8265", "playfield"),
	19: ("Top Lane C", "C", "\"C\"", "A-8265", "playfield"),
	20: ("Top Lane D", "D", "\"D\"", "A-8265", "playfield"),
	21: ("Extra Ball", "Extra Ball", "Extra Ball", "A-8265", "playfield"),
	# The manual prints 22 Bonus Hold Over and 23 Demon (matrix, list and drawing); the ROM, the manual's
	# own rules and the known-working script make 22 the Demon lamp and 23 Bonus Hold Over.
	22: ("Demon", "Bonus Hold Over", "Bonus Hold Over", "A-8265", "playfield"),
	23: ("Bonus Hold Over", "Demon", "DEMON", "A-8265", "playfield"),
	24: ("Left Drain", "Left Drain", "Left Drain", "A-8265", "playfield"),
	25: ("Right Drain", "Right Drain", "Right Drain", "A-8265", "playfield"),
	26: ("Left Flipper Return", "Left Flipper Ret.", "Left Flipper Return", "A-8265", "playfield"),
	27: ("Right Flipper Return", "Right Flipper Ret.", "Right Flipper Return", "A-8265", "playfield"),
	28: ("All Scores 2X", "All Scores 2X", "2X", "B-9558-42", "playfield"),
	29: ("All Scores 3X", "All Scores 3X", "3X", "B-9558-42", "playfield"),
	30: ("All Scores 5X", "All Scores 5X", "5X", "B-9558-42", "playfield"),
	31: ("Light Below S", "Light Below \"S\"", "Light Below \"S\"", "B-9558-41", "playfield"),
	32: ("Light Below R", "Light Below \"R\"", "Light Below \"R\"", "A-8265", "playfield"),
	33: ("Bonus 1", "1", "\"1\"", "B-9558-41", "playfield"),
	34: ("Bonus 2", "2", "\"2\"", "B-9558-21", "playfield"),
	35: ("Bonus 3", "3", "\"3\"", "B-9558-21", "playfield"),
	36: ("Bonus 4", "4", "\"4\"", "B-9558-21", "playfield"),
	37: ("Bonus 5", "5", "\"5\"", "B-9558-21", "playfield"),
	38: ("Bonus 6", "6", "\"6\"", "B-9558-39", "playfield"),
	39: ("Bonus 7", "7", "\"7\"", "B-9558-39", "playfield"),
	40: ("Bonus 8", "8", "\"8\"", "B-9558-39", "playfield"),
	41: ("Bonus 9", "9", "\"9\"", "B-9558-39", "playfield"),
	42: ("Bonus 10", "10", "\"10\"", "B-8445", "playfield"),
	43: ("Bonus 20", "20", "\"20\"", "B-8445", "playfield"),
	44: ("Bonus 30", "30", "\"30\"", "B-8445", "playfield"),
	45: ("Bonus 40", "40", "\"40\"", "A-8265", "playfield"),
	46: ("Bonus 50", "50", "\"50\"", "A-8265", "playfield"),
	47: ("Lock", "Lock", "Lock", "A-8265", "playfield"),
	48: ("Release", "Release", "Release", "A-8265", "playfield"),
	49: ("Bonus Multiplier 2X", "2X", "2X", "B-9558-21", "playfield"),
	50: ("Bonus Multiplier 4X", "4X", "4X", "B-9558-21", "playfield"),
	51: ("Bonus Multiplier 6X", "6X", "6X", "B-9558-21", "playfield"),
	52: ("Bonus Multiplier 8X", "8X", "8X", "B-9558-21", "playfield"),
	53: ("Left Drop Target", "Left Drop-Tgt", "Left Drop Target", "A-8449", "playfield"),
	54: ("Center Drop Target", "Center Drop-Tgt", "Center Drop Target", "A-8449", "playfield"),
	55: ("Right Drop Target", "Right Drop-Tgt", "Right Drop Target", "A-8449", "playfield"),
	56: ("Backglass Effect 56", "Backglass Effect", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	57: ("Backglass Effect 57", "Backglass Effect", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	58: ("Backglass Effect 58", "Backglass Effect", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	59: ("Backglass Effect 59", "Backglass Effect", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	60: ("Backglass Effect 60", "Backglass Effect", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	61: ("Backglass SORCERER Art 61", "Backglass SORCERER art", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	62: ("Backglass SORCERER Art 62", "Backglass SORCERER art", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	63: ("Backglass SORCERER Art 63", "Backglass SORCERER art", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
	64: ("Backglass SORCERER Art 64", "Backglass SORCERER art", "GENERAL ILLUMINATION (56-64)", None, "backbox"),
}
