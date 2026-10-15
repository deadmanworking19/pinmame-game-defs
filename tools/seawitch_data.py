"""Reviewed Seawitch facts, read from this game's retained factory sheets.

Numbers in the lamp rows are LDA connector pins, not public addresses. The
decoder-to-SCR and connector-to-SCR maps below are separate transcriptions.
Coordinate candidates live in the pinned geometry seed and confer no socket
identity on an insert overlay or GI glow.
"""

MACHINE_ID = "stern.seawitch.1980"
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591"
ROM_SHA256 = "bbed2206f4b5bb00362f6dc4aa0d5b00b9635af6c1ade127f498f7a066dad88b"
TABLE_SHA256 = "cb91d8d726d8a451ba6f158e49e459812e8dca888b896e72dca69168d616e434"
SCRIPT_SHA256 = "a3483e9c4e00c68add7135cd0f3a0dbe216a418d17b9c4f02177da27f1239031"
EXTRACTION_SHA256 = "100d0867cede09c9f0de22de094c548585ad66c571402b8574f6f6fcb79af961"
EXTRACTION_FILES = 853
EXTRACTION_BYTES = 29758977
TABLE_WIDTH, TABLE_HEIGHT = 956, 1979
EXTRACTION_RELATIVE = "stern/seawitch-1980/archive-2.0.0/extracted"
TABLE_RELATIVE = "stern/seawitch-1980/archive-2.0.0/Seawitch (Stern 1980)2.0.0.vpx"

# Manual PDF p18. Six deliberately unfitted positions still have a ROM switch
# test number; recognition in that test is not physical fitment.
SWITCH_LABELS = [
    "Coin chute 1", "Coin chute 2", "Coin chute 3", "Top roll-over button",
    "Spinning target", "Credit button", "Roll and pendulum tilts", "Slam and vibration tilts",
    "Top thumper", "Left thumper", "Not used 11", "Left slingshot",
    "Right slingshot", "Right thumper", "Not used 15", "Not used 16",
    "Stand-up target top right", "Stand-up target top left", "Stand-up target top left middle", "Stand-up target top left low",
    "Center bank target 1", "Center bank target 2", "Center bank target 3", "Center bank target 4",
    "Runway roll-over button", "Not used 26", "Not used 27", "Not used 28",
    "Top right bank target 1", "Top right bank target 2", "Top right bank target 3", "Top right bank target 4",
    "Out-hole", "Left outlane", "Right outlane", "Left return lane", "Right return lane",
    "Left bank target 1", "Left bank target 2", "Left bank target 3",
]
UNUSED_SWITCHES = {11, 15, 16, 26, 27, 28}
CABINET_SWITCHES = {1, 2, 3, 6, 7, 8}
STROBES = [("W-R", 1), ("BRN-W", 2), ("W-BLU", 3), ("W-Y", 4), ("Y-R", 5)]
RETURNS = [("BRN", 8), ("GREY", 9), ("W-O", 10), ("W-B", 11), ("W-G", 12), ("W-BRN", 13), ("BRN-Y", 14), ("O", 15)]
CABINET_RETURNS = {1: ("BLU", 9), 2: ("BRN-W", 10), 3: ("R-W", 11), 6: ("BLU-W", 14), 7: ("BLU-O", 15), 8: ("Y", 16)}

# Schematic PDF p10, U2 decoder output S0..S14 reaches Q positions below.
# Public address is S+1. The physical test numbers are the Q positions.
PUBLIC_TO_Q = [2, 1, 5, 6, 7, 3, 4, 8, 13, 14, 9, 10, 12, 11, 16]
PUBLIC_TO_Q += [17, 19, 15, 18]  # public 17,18,19,20 (PIA PB4,PB5,PB6,PB7)
SOLENOID_ADDRESSES = [*range(1, 16), *range(17, 21)]
# Q, literal physical identity, connector on A3, wire, part number, anchor.
COILS = [
    (1, "Left thumper", "J2-9", "G-O", "J-26-1200", "Bumper2"),
    (2, "Top thumper", "J2-4", "G-BLU", "J-26-1200", "Bumper1"),
    (3, "Knocker", "J2-5", "B-Y", "N-26-1200", None),
    (4, "Center bank target reset", "J1-5", "B-BLU", "B-27-2300", "sw22"),
    (5, "OPEN", "J2-10", None, None, None),
    (6, "Left slingshot", "J2-11", "G-R", "J-27-1700", "LeftSlingShot"),
    (7, "Right slingshot", "J2-12", "R-Y", "J-27-1700", "RightSlingShot"),
    (8, "Left bank target reset", "J5-10", "B-O", "B-27-2300", "sw39"),
    (9, "Right thumper", "J5-9", "R-BLU", "J-26-1200", "Bumper3"),
    (10, "OPEN", "J5-15", None, None, None),
    (11, "OPEN", "J5-14", None, None, None),
    (12, "OPEN", "J5-13", None, None, None),
    (13, "Top right bank target reset", "J5-12", "B-Y", "B-27-2300", "sw30"),
    (14, "Out-hole kicker", "J5-11", "B-G", "JX-26-1100", "Drain"),
    (15, "Flipper enable relay", "J1-8 / J1-9", None, None, None),
    (16, "OPEN", "J5-8", None, None, None),
    (17, "OPEN", "J5-7", None, None, None),
    (18, "OPEN", "J2-15", None, None, None),
    (19, "Coin lockout", "J2-8", "Y-W", "C-36-5300", None),
]

# Schematic PDF p9, independently read decoder output -> resistor -> SCR.
# U3/U4 print S12..S14 ABOVE S0; preserve that distinction in the excerpt.
DECODER_SCRS = [
    [14, 12, 13, 8, 9, 10, 11, 4, 1, 2, 3, 7, 16, 5, 6],
    [29, 27, 28, 35, 34, 22, 26, 25, 24, 17, 23, 21, 15, 18, 19],
    [36, 38, 44, 49, 48, 37, 32, 20, 42, 41, 40, 39, 33, 30, 31],
    [57, 50, 51, 54, 55, 60, 59, 58, 56, 46, 52, 53, 47, 43, 45],
]
# Each line is jack: pin=SCR. Multiple connector branches are not extra bulbs.
LDA_CONNECTORS = {
    "J1": {18:14, 19:12, 17:13, 23:8, 14:9, 15:10, 16:11, 28:4, 24:1, 25:2, 26:3, 27:7,
           1:29, 9:27, 8:28, 3:35, 2:34, 10:22, 7:26, 6:25, 5:24, 11:17, 13:20, 4:23, 12:21},
    "J2": {21:3, 13:7, 22:16, 16:5, 14:6, 8:23, 12:21, 23:15, 20:18, 15:19, 11:33, 6:30, 2:31,
           9:40, 4:39, 5:52, 10:47, 7:43, 1:45, 3:53},
    "J3": {26:36, 25:38, 19:44, 17:49, 16:48, 23:37, 27:32, 21:42, 20:41, 22:40, 24:39, 1:57,
           12:50, 15:51, 11:54, 9:55, 3:60, 4:59, 2:58, 10:56, 18:46, 13:52, 14:53},
}

# Entire game-specific lamp list from schematic PDF p9, including source-literal
# spelling and colours. Last row is separately printed at the bottom of the list.
LAMP_ROWS_TEXT = """BLUE LEFT SIDE|BROWN-B|J1|18
BLUE RIGHT SIDE|B-R|J3|19
BLUE 2nd. LEFT SIDE|BLU-R|J1|1
BLUE 2nd. RIGHT SIDE|G-B|J1|8
BLUE 3rd. LEFT SIDE|BLACK|J3|26
BLUE 3rd. RIGHT SIDE|PURPLE|J1|17
BLUE 4th. LEFT SIDE|G-R|J3|1
BLUE 4th. RIGHT SIDE|O-R|J3|12
BLUE 5th. LEFT SIDE|GREY-G|J1|19
BLUE 5th. RIGHT SIDE|B-Y|J3|25
BLUE ROLL-OVER SWITCH LITE (TOP)|BROWN|J1|9
DOUBLE LOOP VALUE|BLUE-W|J1|23
BONUS--1,000|GREY-O|J1|14
BONUS--2,000|PURPLE-W|J1|2
BONUS--3,000|R-B|J3|16
BONUS--4,000|W-R|J3|9
BONUS--5,000|GREY-Y|J1|15
BONUS--6,000|GREY-BLU|J1|10
BONUS--7,000|W-GREY|J3|23
BONUS--8,000|W-BLU|J3|3
BONUS--9,000|R-G|J1|3
BONUS--10,000|Y-BLU|J3|17
BONUS--20,000|WHITE|J3|11
BOTTOM LITE 1-EXTRA BALL|GREY-G|J2|12
BOTTOM DROP TARGET (LAST TAR.) 10,000|B-W|J2|3
DROP TARGET INCREASE (MIDDLE)|PUR-B|J1|25
DROP TARGET INCREASE (BOTTOM)|W-Y|J2|13
GAME OVER|GREY-W|J2|11
HIGH SCORE TO DATE|GREY-O|J2|22
LEFT SPECIAL|W-O|J3|20
LEFT RETURN|BRN-BLU|J1|24
LITE EXTRA BALL B-1|B-Y|J2|5
LITE EXTRA BALL B-2|GREY|J2|9
LITE EXTRA BALL B-3|PUR-BLU|J2|8
MATCH|GREY-Y|J2|1
MIDDLE DROP TARGET (LAST TAR.) 10,000|R-BLU|J3|18
MIDDLE LITE 2-EXTRA BALL|B-O|J1|11
RIGHT RETURN|BLU-O|J1|5
RIGHT SPECIAL|PUR-B|J2|4
RUNWAY SPECIAL|YELLOW|J2|6
SHOOT AGAIN (INSERT)|GREY-R|J2|21
SPINNER, TOP|YEL-G|J3|2
SPINNER, 2nd. TOP|W-BLU|J1|13
SPINNER, 2nd. BOTTOM|BRN-R|J1|6
SPINNER, BOTTOM|B-W|J1|28
STAND-UP BOTTOM|B-G|J1|16
STAND-UP LEFT|Y-G|J1|7
STAND-UP RIGHT|O-W|J3|27
STAND-UP TOP|R-W|J3|4
TARGETS INCREASE|O-B|J2|16
TOP DROP LITE 3-EXTRA BALL|O-G|J2|20
TOP DROP TARGET 10,000|BLU-W|J2|7
TILT|GREY-B|J2|10
1X|BLUE-R|J2|14
2X|Y-BLU|J2|15
4X|R-BLU|J2|2
SHOOT AGAIN (PLAYFIELD)|GREY-R|J1|26"""
LAMP_ROWS = [tuple(row.split("|")) for row in LAMP_ROWS_TEXT.splitlines()]

DIPS = {
    **{n: "Coin chute 2 pricing bit %d" % n for n in range(1, 5)},
    5: "Not used S5", 6: "High score award (OFF extra ball, ON replay)",
    7: "Balls per game (OFF 3, ON 5)", 8: "Special threshold and multiplier reset",
    **{n: "Coin chute 1 pricing bit %d" % (n-8) for n in range(9, 13)},
    13: "Not used S13", 14: "Background sound", 15: "High game to date award bit 1", 16: "High game to date award bit 2",
    17: "Special alternation", 18: "Maximum credits bit 1", 19: "Maximum credits bit 2", 20: "Credit display", 21: "Match feature",
    22: "Special award limit", 23: "Extra ball alternation bit 1", 24: "Extra ball alternation bit 2",
    **{n: "Coin chute 3 pricing bit %d" % (n-24) for n in range(25, 29)},
    29: "Minimum added extra balls", 30: "Maximum added extra balls", 31: "Special award bit 1", 32: "Special award bit 2",
}
