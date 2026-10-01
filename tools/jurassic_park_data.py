"""Literal factory and ROM tables for Data East Jurassic Park (1993).

Every table below was read from the retained factory manual's rendered pages
(Data_East_1993_Jurassic_Park_Manual.pdf, 103 PDF pages; printed page = PDF page - 4) or from
the ROM's own service-test displays in the retained fresh-state runs. Printed spelling is kept
literally, including the misprints the notes on each device call out. OCR only found pages.
"""
from __future__ import annotations

# PDF 30 / printed page 26: switch matrix chart. (drive wire, drive connection, driver transistor)
SWITCH_COLUMNS = (
    ("GRN-BRN", "CN8-1", "Q55"), ("GRN-RED", "CN8-2", "Q54"), ("GRN-ORN", "CN8-3", "Q53"),
    ("GRN-YEL", "CN8-4", "Q52"), ("GRN-BLK", "CN8-5", "Q51"), ("GRN-BLU", "CN8-7", "Q50"),
    ("GRN-VIO", "CN8-8", "Q49"), ("GRN-GRY", "CN8-9", "Q48"),
)
# (return wire, return connection). The printed rows skip CN10-4 and the printed columns skip CN8-6:
# the CPU board's keyed pins (PDF 51 connector blocks), not missing switches.
SWITCH_ROWS = (
    ("WHT-BRN", "CN10-9"), ("WHT-RED", "CN10-8"), ("WHT-ORN", "CN10-7"), ("WHT-YEL", "CN10-6"),
    ("WHT-GRN", "CN10-5"), ("WHT-BLU", "CN10-3"), ("WHT-VIO", "CN10-2"), ("WHT-GRY", "CN10-1"),
)
# Matrix-chart names, address 1..64 in column-major order, as printed.
SWITCH_NAMES = (
    "Plumb Tilt", "4th Coin", "Credit Button", "Right Coin", "Center Coin", "Left Coin",
    "Slam Tilt", "Not Used",
    "Trough #1 Left", "Trough #2", "Trough #3", "Trough #4", "Trough #5", "Trough #6",
    "Trough #7 Right", "Shooter Lane",
    "Outer Loop Low", "Outer Loop Top", "Inner Loop Low", "Inner Loop Top", "Right Outlane",
    "Right Return", "Left Return", "Left Outlane",
    "Spitter Target #1 Bottom", "Spitter Target #2 Middle", "Spitter Target #3 Top", "Not Used",
    "Raptor Pit", "Not Used", "T.Rex Right", "T.Rex Left",
    "Right Ramp Enter", "Right Ramp Exit", "Left Scoop", "T.Rex Center", "Center Scoop",
    "Herrerasaurus Low", "Herrerasaurus Top", "Brachiasaurus Low",
    "Launch Trigger", "Smart Bomb Button", "Left Slingshot", "Right Slingshot",
    "Top Turbo Bumper", "Left Turbo Bumper", "Right Turbo Bumper", "Mosquito Captive Ball",
    "Baryonyx Target", "Gallimimus Target", "Not Used", "Triceritops Target",
    "Brachiasaurus Top", "Not Used", "T.Rex Saucer Eject", "Right Saucer Eject",
    "T.Rex Top (Up)", "T.Rex Bottom (Down)", "T.Rex Trough", "Right Scoop Trough",
    "Right VUK", "Not Used", "Left Flipper", "Right Flipper",
)
# PDF 31 / printed page 27: switch part numbers. "-" is the printed dash for no part.
SWITCH_PARTS = (
    "See Cabinet", "-", "500-5097-02", "180-5024-00", "180-5024-00", "180-5024-00", "180-5022-00", "-",
    "180-5119-00", "180-5119-00", "180-5119-00", "180-5119-00", "180-5119-00", "180-5119-00",
    "180-5119-00", "180-5100-01",
    "500-5142-00", "500-5142-00", "500-5142-00", "500-5142-00", "500-5142-00", "500-5142-00",
    "515-5138-00", "515-5138-00",
    "180-5114-02", "180-5114-02", "180-5114-02", "-", "180-5100-01", "-", "180-5040-00", "180-5040-00",
    "180-5087-00", "180-5117-00", "180-5116-00", "180-5123-00", "500-5442-01", "180-5120-02",
    "180-5120-02", "180-5120-04",
    "180-5111-00", "515-5825-00", "180-5054-00", "180-5054-00", "180-5015-01", "180-5015-01",
    "180-5015-01", "180-5114-08",
    "180-5120-02", "180-5120-04", "-", "180-5120-04", "180-5120-04", "-", "180-5027-00", "180-5027-00",
    "180-5040-00", "180-5040-00", "180-5057-00", "180-5057-00", "180-5064-00", "-", "180-5048-01",
    "180-5022-00",
)
# Printed asterisks 01-07 mark the coin-door and cabinet switches ("See Cabinet" for the tilt).
CABINET_SWITCHES = frozenset(range(1, 8))

# ROM Active Switch Test: the name shown while each address is held closed, wire colours and
# number (runtime/active-switch-test). Addresses 63/64 are reached through the host flipper buttons.
ROM_SWITCH_NAMES = (
    "PLUMB TILT", "4TH COIN", "CREDIT BUTTON", "RIGHT COIN", "CENTER COIN", "LEFT COIN",
    "SLAM TILT", "NOT USED",
    "TROUGH #1 LEFT", "TROUGH #2 M-L-L", "TROUGH #3 MID LFT", "TROUGH #4 MIDDLE",
    "TROUGH #5 MID RGT", "TROUGH #6 M-R-R", "TROUGH #7 RIGHT", "SHOOTER LANE",
    "OUTER LOOP LOW", "OUTER LOOP TOP", "INNER LOOP LOW", "INNER LOOP TOP", "RIGHT OUTLANE",
    "RIGHT RETURN", "LEFT RETURN", "LEFT OUTLANE",
    "SPITTER #1 BOTTOM", "SPITTER #2 MIDDLE", "SPITTER #3 TOP", "NOT USED", "RAPTOR PIT",
    "NOT USED", "T-REX RIGHT", "T-REX LEFT",
    "RIGHT RAMP ENTER", "RIGHT RAMP EXIT", "LEFT SCOOP", "T-REX CENTER", "MIDDLE SCOOP",
    "HERRERASAURUS LOW", "HERRERASAURUS TOP", "BRACHIASAURUS LOW",
    "LAUNCH BUTTON", "SMART MISSILE", "LEFT SLINGSHOT", "RIGHT SLINGSHOT",
    "TOP TURBO BUMPER", "LEFT TURBO BUMPER", "RIGHT TURBO BUMPER", "CAPTIVE BALL",
    "BARYONYX", "GALLIMIMUS", "NOT USED", "TRICERATOPS", "BRACHIASAURUS TOP", "NOT USED",
    "T-REX EJECT", "TOP RIGHT EJECT", "T-REX UP", "T-REX DOWN", "T-REX TROUGH", "RIGHT SCOOP",
    "RIGHT VUK", "NOT USED", "LEFT FLIPPER", "RIGHT FLIPPER",
)

# PDF 32 / printed page 28: lamp matrix chart. (drive wire, drive connection, driver transistor)
LAMP_COLUMNS = (
    ("YEL-BRN", "CN7-1", "Q71"), ("YEL-RED", "CN7-2", "Q70"), ("YEL-ORN", "CN7-3", "Q69"),
    ("YEL-BLK", "CN7-4", "Q68"), ("YEL-GRN", "CN7-6", "Q67"), ("YEL-BLU", "CN7-7", "Q66"),
    ("YEL-VIO", "CN7-8", "Q65"), ("YEL-GRY", "CN7-9", "Q64"),
)
# (return wire, return connection, return transistor)
LAMP_ROWS = (
    ("RED-BRN", "CN6-1", "Q72"), ("RED-BLK", "CN6-2", "Q73"), ("RED-ORN", "CN6-3", "Q74"),
    ("RED-YEL", "CN6-5", "Q75"), ("RED-GRN", "CN6-6", "Q76"), ("RED-BLU", "CN6-7", "Q77"),
    ("RED-VIO", "CN6-8", "Q78"), ("RED-GRY", "CN6-9", "Q79"),
)
# Matrix-chart names, address 1..64, as printed (the printed 6 is the single word "Map").
LAMP_NAMES = (
    "Visitor Center X2", "\"T\" Arch", "Brachiasaurus Map", "Spitter Map", "Herrerasaurus Map",
    "Map", "Triceratop Map", "Gallimimus",
    "Credit Button", "Mosquito X2", "Electric Fence", "Spitter Attack", "2 Ball Grid",
    "System Boot", "Raptor Rampage", "Light Extra Ball",
    "Left Scoop Bottom", "Left Scoop Top", "Helo X2", "Raptor Multi-Million", "Feed T.Rex",
    "Bone Buster", "Escape Isla Nubar", "Stampede",
    "Spitter #1 Bottom", "Spitter #2", "Spitter #3", "Boat Dock X2", "Jackpot Loop", "Jackpot Map",
    "Top Turbo Bumper", "Right Turbo Bumper",
    "Center Scoop Bottom", "Center Scoop Top", "Advance X", "Triceratop", "T-Rex Map",
    "Herrerasaurus Low", "Herrerasaurus Top", "Brachiasaurus Low",
    "C", "H", "A", "O", "S", "Gate X2", "\"R\" Arch", "\"C\" Arch",
    "Baryonyx Target", "#2", "2 Ball Play Arrow", "Raptor Pit 5 Milion", "Raptor Pit Jackpot",
    "Raptor Pit Danger", "Outlanes Special X2", "Shoot Again",
    "Right Scoop Bottom", "Right Scoop Top", "Brachiasaurus Top", "\"X\" Arch", "Egg",
    "Left Turbo Bumper", "Extra Ball Arrow", "Smart Bomb X2",
)
# PDF 33 / printed page 29: the lamp-location list's own spelling where it differs from the matrix.
LAMP_LIST_NAMES = {
    1: "Visitor Center (2 Bulbs)", 7: "Triceratops Map", 10: "Mosquito (2 Bulbs)",
    16: "Lite Extra Ball", 17: "Left Scoop Bottom", 18: "Left scoop Top", 19: "Helo (2 Bulbs)",
    20: "Raptor Multi-Million", 28: "Boat Dock (2 Bulbs)", 36: "Triceritops", 46: "Gate (2 Bulbs)",
    49: "Baryonyx Target", 52: "Raptor Pit 5 Million", 55: "Outlanes Special (2 Bulbs)",
    64: "Smart Bomb (2 Bulbs)",
}
# "(2 Bulbs)" in the printed list.
TWO_BULB_LAMPS = frozenset({1, 10, 19, 28, 46, 55, 64})
# Lamps the printed list does not mark but the location drawing shows twice (37) and the ROM names X2.
DRAWING_TWO_BULB_LAMPS = frozenset({37})

# ROM single-lamp test: the lamp name shown beside each matrix number (runtime/lamp-test).
ROM_LAMP_NAMES = (
    "VISITOR CENTER X2", "\"T\" ARCH", "BRACHIOSAURUS - MAP", "SPITTER - MAP",
    "HERRERASAURUS - MAP", "BARYONYX - MAP", "TRICERATOPS - MAP", "GALLIMIMUS - MAP",
    "CREDIT BUTTON", "MOSQUITO X2", "ELECTRIC FENCE", "SPITTER ATTACK", "TWO BALL - GRID",
    "SYSTEM BOOT", "RAPTOR RAMPAGE", "LIGHT EXTRA BALL",
    "LEFT SCOOP BOT", "LEFT SCOOP TOP", "HELIPAD X2", "MOSQUITO MULTI MIL.", "FEED T-REX",
    "BONE BUSTING", "ESCAPE ISLA NUBLAR", "STAMPEDE",
    "SPITTER #1 BOTTOM", "SPITTER #2 MIDDLE", "SPITTER #3 TOP", "BOAT DOCK X2", "JACKPOT LOOP",
    "JACKPOT RAMP", "TOP TURBO BUMPER", "RIGHT TURBO BUMPER",
    "MIDDLE SCOOP BOT", "MIDDLE SCOOP TOP", "ADVANCE X", "TRICERATOPS", "PLFD T-REX X2",
    "HERRERASAURUS LOW", "HERRERASAURUS TOP", "BRACHIASAURUS LOW",
    "CHAOS \"C\"", "CHAOS \"H\"", "CHAOS \"A\"", "CHAOS \"O\"", "CHAOS \"S\"", "GATE LIGHTS X2",
    "ARCH \"R\"", "ARCH \"E\"",
    "BARYONYX", "GALLIMIMUS", "TWO BALL PLAY ARROW", "RAPTOR PIT 5 MIL", "RAPTOR PIT JACKPOT",
    "RAPTOR PIT DANGER", "OUT LANES SPECIAL X2", "SHOOT AGAIN",
    "RIGHT SCOOP BOT", "RIGHT SCOOP TOP", "BRACHIASAURUS TOP", "ARCH \"X\"", "DINO EGG",
    "LEFT TURBO BUMPER", "EXTRA BALL ARROW", "SMART MISSILE X2",
)
# Reconciled device labels where the printed matrix name is blank, a bare placeholder or a misprint
# that the ROM test and the playfield artwork settle (notes on each device give the evidence).
LAMP_LABEL_OVERRIDES = {
    6: "Baryonyx Map", 20: "Multi Mosquito Millions", 30: "Jackpot Ramp", 48: "\"E\" Arch",
    50: "Gallimimus Target",
}

# PDF 34-35 / printed pages 30-31: CPU Controlled Auxiliary Solenoids table (17-22) and flippers.
AUX_COILS = (
    # coil, printed name, control wire, control connection, power wire, power connection, transistor, type
    (17, "Top Turbo Bumper", "BLU-BRN", "CPU CN19-7", "RED", "PS CN3-6", "Q11", "23-800"),
    (18, "Left Turbo Bumper", "BLU-RED", "CPU CN19-4", "RED", "PS CN3-6", "Q9", "23-800"),
    (19, "Right Turbo Bumper", "BLU-ORN", "CPU CN19-3", "RED", "PS CN3-6", "Q8", "23-800"),
    (20, "Left Slingshot", "BLU-YEL", "CPU CN19-6", "RED", "PS CN3-6", "Q10", "23-800"),
    (21, "Right Slingshot", "BLU-GRN", "CPU CN19-8", "RED", "PS CN3-6", "Q12", "23-800"),
    (22, "Shaker Motor (See Schematic)", "BLU-BLK", "CPU CN19-9", "VIO-YEL", "J7-3", "Q13", "23-800"),
)
FLIPPER_CHART = (
    # coil, part, flipper GND (CPU to flip switch), flip switch to flip PCB, power lines, coil type, power input
    ("Left Flipper", "090-5020-30", "ORN-GRY CPU CN19-2", "BLU-GRY CN1-9", "GRY-YEL CN2-4,5",
     "23-900", "BLK-WHT 50VDC / GRY, GRY-GRN 8VAC"),
    ("Right Flipper", "090-5020-30", "ORN-VIO CPU CN19-1", "BLU-VIO CN1-1", "BLU-YEL CN2-7,8",
     "23-900", "BLK-WHT 50VDC / GRY, GRY-GRN 8VAC"),
    ("Upper Right Flipper", "090-5041-00", "ORN-VIO CPU CN19-1", "GRY-VIO CN1-12", "BLK-YEL CN2-1,2",
     "25-1800", "BLK-WHT 50VDC / GRY, GRY-GRN 8VAC"),
)

# PDF 35 / printed page 31: coil / flash-lamp schematic. Drives 1-8 switch two loads each through
# the PPB board's left/right relay (public 10): the left set are coils, the right set flash lamps.
# (drive, printed coil name, ROM coil name, CPU transistor, CPU CN11 pin, control wire (CPU -> PPB J1),
#  coil lead wire, flash-lamp lead wire, printed bulb text for the right set, ROM flash-lamp name)
LR_DRIVES = (
    (1, "Top Eject", "TOP RGT EJECT", "Q46", "CN11-1", "GRY-BRN", "VIO-BRN", "BLK-BRN",
     "(3) RAPTOR PIT (1) INSERT", "FL: 2-RAPTOR 1-INS"),
    (2, "Ball Release", "BALL RELEASE", "Q45", "CN11-3", "GRY-RED", "VIO-RED", "BLK-RED",
     "(3) PLFD RIGHT SIDE (1) INSERT", "FL: 3-R SIDE 1-INS"),
    (3, "Auto Launch", "AUTO LAUNCH 50V", "Q44", "CN11-4", "GRY-ORG", "WHT-ORG / VIO-ORG", "BLK-ORG",
     "(4) ORBIT SHOT", "FL: 4-ORBIT"),
    (4, "Left Scoop", "LEFT SCOOP", "Q43", "CN11-5", "GRY-YEL", "VIO-YEL", "BLK-YEL",
     "(3) UPPER RIGHT PLFD (1) UPPER RIGHT CORNER", "FL: TOP RGT. RMP 1.3.5"),
    (5, "Right VUK", "RIGHT VUK 50V", "Q42", "CN11-6", "GRY-GRN", "WHT-GRN / VIO-GRN", "BLK-GRN",
     "(3) UPPER RIGHT PLFD (1) UPPER LEFT CORNER", "FL: TOP LFT. RMP 2.4.6"),
    (6, "Diverter", "RAMP DIVERTER", "Q41", "CN11-7", "GRY-BLU", "VIO-BLU", "BLK-BLU",
     "(3) LEFT SIDE PLFD (1) INSERT", "FL: 3-L SIDE 1-INS"),
    (7, "Dino Eject", "T-REX EJECT", "Q40", "CN11-8", "GRY-VIO", "VIO-BLK", "BLK-VIO",
     "(4) TURBO BUMPER", "FL: 3-POPS 1-TREX"),
    (8, "Knocker", "KNOCKER", "Q39", "CN11-9", "GRY-BLK", "VIO-GRY", "BLK-GRY",
     "(1) MOSQUITO (1) PLFD (2) TOP DISPLAY", "FL: 1-MSQ 1-PFD 2-TOP"),
)
# Drives 9-16 (CPU CN12): (drive, printed name, ROM name, transistor, CPU connection, wire, what it switches)
DIRECT_DRIVES = (
    (9, "Raptor Pit", "RAPTOR PIT 50V", "Q30", "CPU CN12-1", "WHT/BRN",
     "Raptor-pit kicker coil through PPB board Q4 (TIP security), +50 VDC at J7-3"),
    (10, "L/R Coil Relay", "(not named by the cycle test)", "Q29", "CPU CN12-2", "BLK-RED",
     "PPB left/right coil relay (J7 terminals 9 and 7); +32 V from PS CN3-5"),
    (11, "G.I. Relay", "RELAY: G.I. RELAY", "Q28", "CPU CN12-4", "BRN-ORG",
     "K-1 general-illumination relay on the power-supply board (PS CN7-1/3)"),
    (12, "Motor (Left/Right) select", "RELAY: MOTOR L/R", "Q27", "CPU CN12-5", "BRN-YEL",
     "(LEFT/RIGHT) BRN/YEL input of the bi-directional relay board 520-5066-00 for the T-Rex rotation motor"),
    (13, "Dino Mouth", "COIL: T-REX MOUTH", "Q26", "CPU CN12-6", "BRN-GRN",
     "T-Rex jaw coil, RED supply (+32 V)"),
    (14, "Motor Up/Down", "RELAY: MOTOR UP/DWN", "Q25", "CPU CN12-7", "BRN-BLU",
     "relay board 520-5010-00 switching 28 VAC (from BR2) to the T-Rex up/down motor"),
    (15, "Motor On/Off", "RELAY: MOTOR ON/OFF", "Q24", "CPU CN12-8", "BRN-VIO",
     "28 VAC feed of the T-Rex rotation motor through bi-directional relay 520-5066-00"),
    (16, "Lockout", "COIL: LOCK OUT", "Q23", "CPU CN12-9", "BRN-GRY",
     "trough lock-out coil, RED supply (+32 V)"),
)
# ROM CYCLING COILS / FLASHERS test: the name shown for each public solenoid address.
ROM_COIL_NAMES = {
    1: "COIL: TOP RGT EJECT", 2: "COIL: BALL RELEASE", 3: "COIL: AUTO LAUNCH 50V",
    4: "COIL: LEFT SCOOP", 5: "COIL: RIGHT VUK 50V", 6: "COIL: RAMP DIVERTER",
    7: "COIL: T-REX EJECT", 8: "COIL: KNOCKER", 9: "COIL: RAPTOR PIT 50V",
    11: "RELAY: G.I. RELAY", 12: "RELAY: MOTOR L/R", 13: "COIL: T-REX MOUTH",
    14: "RELAY: MOTOR UP/DWN", 15: "RELAY: MOTOR ON/OFF", 16: "COIL: LOCK OUT",
    17: "COIL: TOP TURBO", 18: "COIL: LEFT TURBO", 19: "COIL: RIGHT TURBO",
    20: "COIL: LEFT SLING", 21: "COIL: RIGHT SLING", 22: "COIL: SHAKER MOTOR",
    25: "FL: 2-RAPTOR 1-INS", 26: "FL: 3-R SIDE 1-INS", 27: "FL: 4-ORBIT",
    28: "FL: TOP RGT. RMP 1.3.5", 29: "FL: TOP LFT. RMP 2.4.6", 30: "FL: 3-L SIDE 1-INS",
    31: "FL: 3-POPS 1-TREX", 32: "FL: 1-MSQ 1-PFD 2-TOP",
}
# Coil part numbers from the unique-parts assembly pages (PDF 41-47), the higher authority for part
# numbers than the schematic's generic "23-840" print. (assembly, coil printed there, coil part)
ASSEMBLY_COILS = {
    1: ("500-5664-00", "24-940", "090-5636-02"),   # Ball Eject Assy (Saucer)
    2: ("500-5683-00", "23-800", "090-5001-00"),   # 6 Ball Switch Assembly item 9, the release coil
    13: ("500-5667-00", "25-1240", "090-5034-00"),  # Dino Assembly item 29, the jaw coil
    16: ("500-5684-00", "25-1240", "090-5034-00"),  # Lock Ball Assembly item 23
    5: ("500-5116-04", "23-800", "090-5001-01"),   # Super VUK
    3: ("500-5477-00", "23-800", "090-5001-01"),   # Ball Launch Assy
    4: ("515-5772-00", "23-800", "090-5001-01"),   # Double Scoop Sub-Assembly
    6: ("500-5661-00", "27-1500", "090-5004-02"),  # Diverter Plunger & Crank Arm Assy
    7: ("500-5665-00", "27-1500", "090-5004-02"),  # Ball Eject Assy (Dino)
    8: ("500-5081-00", "23-800", "090-5001-01"),   # Kickback & Knocker Assembly
    9: ("500-5081-00", "23-800", "090-5001-01"),   # Kickback Assy at the raptor pit (printed page 33 item 1)
    17: ("500-5227-00", "23-800", "090-5001-00"),  # Turbo Bumper
    18: ("500-5227-00", "23-800", "090-5001-00"),
    19: ("500-5227-00", "23-800", "090-5001-00"),
    20: ("500-5226-00", "23-800", "090-5001-02"),  # Slingshot Assembly
    21: ("500-5226-00", "23-800", "090-5001-02"),
}

# T-Rex test (PDF 29 / printed page 25): the ROM prints ON or OFF beside each label.
TREX_TEST_LABELS = {57: "TOP SWITCH", 58: "BOTTOM SWITCH", 36: "CENTER SWITCH", 31: "RIGHT SWITCH", 32: "LEFT SWITCH"}
# Laser Kick Test: a closure of the key fires the coil (runtime/laser-kick-test).
LASER_KICK_PAIRS = {29: 9, 35: 4, 55: 7, 56: 1, 61: 5}
