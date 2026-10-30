"""Self-contained deterministic curator for Data East RoboCop (1989)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pinmame_game_defs.coverage import build_coverage_report, build_curation_queue, render_coverage_markdown, render_curation_queue_markdown, write_coverage_report
from pinmame_game_defs.jsonio import content_sha256, load_json, write_text
from pinmame_game_defs.registry import rebuild_catalog
from pinmame_flipper_column import (
	VPM_CORE_SHA256,
	VPM_DE_LIBRARY_SOURCE,
	VPM_DE_LIBRARY_URI,
	VPM_DE_SHA256,
	flipper_column_inputs,
	flipper_column_relationships,
	vpm_staged_flipper_notes,
)


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
PINMAME_SHORT = PINMAME_REVISION[:12]
MACHINE_ID = "data-east.robocop.1989"
MACHINE_PATH = Path("machines/partial/data-east/robocop-1989.json")
AUTHOR_READY_PATH = Path("machines/author-ready/data-east/robocop-1989.json")
SEED_PATH = Path("tools/seeds/data-east/robocop-1989.json")
SPATIAL_JSON_PATH = Path("reports/spatial/data-east/robocop-1989.json")
SPATIAL_MD_PATH = Path("reports/spatial/data-east/robocop-1989.md")
KNOWLEDGE_PATH = Path("knowledge/data-east/robocop-1989.md")
RUNTIME_EVIDENCE_PATH = Path("evidence/runtime/data-east/robocop-service-walk.json")
READINGS_PATH = Path("tools/seeds/data-east/robocop-1989-service-readings.json")
MANIFEST_PATH = Path("tools/seeds/data-east/robocop-1989-extraction-manifest.json")
EXCERPT_DIR = Path("evidence/excerpts/data-east.robocop.1989")

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_SHORT}"
CORE_SOURCE = f"pinmame.core.{PINMAME_SHORT}"
MANUAL_SOURCE = "manual.data-east.robocop.1989"
TABLE_SOURCE = "vpx-table.robocop-drakkon-mod-1.2"
SCRIPT_SOURCE = "vpx-script.robocop-drakkon-mod-1.2"
EXTRACTION_SOURCE = "vpx-extraction.robocop-drakkon-mod-1.2"
RENDER_SOURCE = "human-review.robocop-manual-renders"
RUNTIME_SOURCE = "runtime.robocop.service-walk"
# (left, right) in the driver's own FLIP1516 = FLIP_SWNO(15,16) macro order.
FLIP_SWNO = (15, 16)

MANUAL_FILENAME = "Data_East_1989_Robocop_English_Manual.pdf"
MANUAL_SHA256 = "951b39a17f851a2f2e38d79dfc09e5f9b435d03fdbe16d4d45a3e314a7b69af8"
TABLE_FILENAME = "Robocop (Data East 1989)_drakkon(mod_1.2).vpx"
TABLE_SHA256 = "e6f5545be1155856bd684f13e3910c378f7d6f3689425e3696b7329eb65e8ab8"
SCRIPT_SHA256 = "00abf00a3f2e9cc3977e1053765902071a7caf381407b58ad09c4bef8abe3dd8"
MANIFEST_ALGORITHM = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
MANIFEST_CONTENT_SHA256 = "e230a9c97228769664678d14038ee9bfb99d2f65567cf8440534638d0a24ae3a"
MANIFEST_SHA256 = "5c415cb2b5f01b156fb31af6896e4ca58a97beb1636dfb2ba5d6c4148db0f476"
RIGHT = 952.0
BOTTOM = 2256.0

SWITCH_DRIVES = ["GRN-BRN", "GRN-RED", "GRN-ORN", "GRN-YEL", "GRN-BLK", "GRN-BLU", "GRN-VIO", "GRN-GRY"]
SWITCH_DRIVE_CODES = [51, 52, 53, 54, 50, 56, 57, 58]
SWITCH_DRIVE_TRANSISTORS = ["Q55", "Q54", "Q53", "Q52", "Q51", "Q50", "Q49", "Q48"]
SWITCH_RETURNS = ["WHT-BRN", "WHT-RED", "WHT-ORN", "WHT-YEL", "WHT-GRN", "WHT-BLU", "WHT-VIO", "WHT-GRY"]
SWITCH_RETURN_CODES = [91, 92, 93, 94, 95, 96, 97, 98]
LAMP_DRIVES = ["YEL-BRN", "YEL-RED", "YEL-ORN", "YEL-BLK", "YEL-GRN", "YEL-BLU", "YEL-VIO", "YEL-GRY"]
LAMP_DRIVE_CODES = [41, 42, 43, 40, 45, 46, 47, 48]
LAMP_DRIVE_TRANSISTORS = ["Q71", "Q70", "Q69", "Q68", "Q67", "Q66", "Q65", "Q64"]
LAMP_RETURNS = ["RED-BRN", "RED-BLK", "RED-ORN", "RED-YEL", "RED-GRN", "RED-BLU", "RED-VIO", "RED-GRY"]
LAMP_RETURN_CODES = [21, 20, 23, 24, 25, 26, 27, 28]
LAMP_RETURN_TRANSISTORS = ["Q72", "Q73", "Q74", "Q75", "Q76", "Q77", "Q78", "Q79"]

# Printed switch-matrix cells (printed page 20, PDF page 24).
SWITCH_MATRIX_LABELS = {
	1: "Plumb Tilt", 2: "Not Used", 3: "Credit Button", 4: "Right Coin", 5: "Center Coin", 6: "Left Coin", 7: "Slam Tilt", 8: "Not Used",
	9: "Not Used", 10: "Outhole", 11: "Trough #1", 12: "Trough #2", 13: "Trough #3", 14: "Shooter Lane", 15: "Left EOS", 16: "Right EOS",
	17: "Laser Kick", 18: "Left Return", 19: "Right Outlane", 20: "Right Return", 21: "Left Slingshot", 22: "Right Slingshot", 23: "Right Trap Ball", 24: "Not Used",
	25: "2 Lane", 26: "0 Lane", 27: "9 Lane", 28: "Left Eject", 29: "Center Eject", 30: "Right Eject", 31: "Left Ramp", 32: "Right Ramp",
	33: "Green Target 1 (Left)", 34: "Green Target 2", 35: "Green Target 3", 36: "Green Target 4 (Right)", 37: "10 Point Top", 38: "10 Point Bottom", 39: "Not Used", 40: "Not Used",
	41: "Yellow Target 1 (Left)", 42: "Yellow Target 2", 43: "Yellow Target 3 (Right)", 44: "Spinner", 45: "VUK", 46: "Left Turbo Bumper", 47: "Center Turbo Bumper", 48: "Right Turbo Bumper",
}
for _number in range(49, 65):
	SWITCH_MATRIX_LABELS[_number] = "Not Used"

# Printed switch part-number list (printed page 21, PDF page 25), literal descriptions.
SWITCH_LIST = {
	1: ("Plumb Tilt", "500-5023-00"), 2: ("Not Used", None), 3: ("Credit Button", "500-5097-00"), 4: ("Right Coin", "180-5024-00"),
	5: ("Center Coin", "180-5024-00"), 6: ("Left Coin", "180-5024-00"), 7: ("SlamTilt", "180-5022-00"), 8: ("Not Used", None), 9: ("Not Used", None),
	10: ("Out Hole", "180-5011-00"), 11: ("Trough #1", "180-5009-00"), 12: ("Trough #2", "180-5009-00"), 13: ("Trough #3", "180-5010-00"),
	14: ("Shooter Lane", "500-5143-00"), 15: ("Left Flip. Instant Info.; Left EOS", "See Solid State Flipper Board"),
	16: ("Right Flip. Instant Info.; Right EOS", "See Solid State Flipper Board"), 17: ("Left Outlane", "500-5142-00"),
	18: ("Left Return Lane", "500-5142-00"), 19: ("Right Outlane", "500-5142-00"), 20: ("Right Return Lane", "500-5142-00"),
	21: ("Left Slingshot Trigger Sw.; Left Slingshot Point Sw.", "180-5054-00 / 180-5055-00"),
	22: ("Right Slingshot Trigger Sw.; Right Slingshot Point Sw.", "180-5054-00 / 180-5055-00"),
	23: ("Right Trap Ball", "500-5035-02"), 24: ("Not Used", None), 25: ("2 Lane", "500-5142-00"), 26: ("O Lane", "500-5142-00"),
	27: ("9Lane", "500-5142-00"), 28: ("Left Eject", "515-5079-00"), 29: ("Top Eject", "515-5079-00"), 30: ("Right Eject", "515-5079-00"),
	31: ("Left Ramp", "180-5010-01"), 32: ("Right Ramp", "180-5010-01"), 33: ("Green Target 1", "500-5103-14"), 34: ("Green Target 2", "500-5103-14"),
	35: ("Green Target 3", "500-5103-14"), 36: ("Green Target 4", "500-5103-14"), 37: ("10 Point Top", "500-5069-00"), 38: ("10 Point Bottom", "500-5069-00"),
	39: ("Not Used", None), 40: ("Not Used", None), 41: ("Yellow Target 1", "500-5103-16"), 42: ("Yellow Target 2", "500-5103-16"),
	43: ("Yellow Target 3", "500-5103-16"), 44: ("Spinner", "500-5193-00"), 45: ("Vertical Up Kicker", "180-5041-00"),
	46: ("Left Turbo Bumper", "180-5036-00"), 47: ("Center Turbo Bumper", "180-5036-00"), 48: ("Right Turbo Bumper", "180-5036-00"),
}
CABINET_SWITCHES = {1, 3, 4, 5, 6, 7}

SWITCH_LABELS = {
	**{number: label for number, label in SWITCH_MATRIX_LABELS.items()},
	15: "Left Flipper Button (FLIP1516 copy)", 16: "Right Flipper Button (FLIP1516 copy)", 29: "Top Eject",
}

RAW_SWITCH_POINTS = {
	10: (448.0, 2156.0), 14: (911.25, 2000.625), 17: (58.5, 1831.0), 18: (128.0, 1673.5), 19: (821.75, 1727.875), 20: (758.0, 1669.5),
	21: (220.356675, 1656.495075), 22: (666.60631, 1645.305), 23: (918.0624, 951.4416),
	25: (388.75, 410.75), 26: (490.75, 401.75), 27: (591.25, 397.25), 28: (62.75, 447.625), 29: (300.75, 201.125), 30: (849.75, 222.125),
	31: (107.0, 372.5), 32: (576.0, 209.0),
	33: (142.3044, 1217.245), 34: (158.897, 1155.44), 35: (175.3141, 1091.3951), 36: (190.941, 1029.3707),
	41: (432.4131, 927.5693), 42: (483.6888, 952.759), 43: (535.1227, 976.8683), 44: (218.5, 777.75), 45: (95.0, 906.5),
	46: (425.0, 621.5), 47: (530.0, 828.5), 48: (637.5, 622.5),
}
SWITCH_OBJECTS = {
	10: "Drain kicker (Drain_Hit adds the ball to bsTrough, whose entry switch is 10)", 14: "sw14 trigger", 17: "sw17 trigger", 18: "sw18 trigger",
	19: "sw19 trigger", 20: "sw20 trigger", 21: "LeftSlingShot wall (centroid of its four drag points)", 22: "RightSlingShot wall (centroid of its four drag points)",
	23: "sw23 hit target", 25: "sw25 trigger", 26: "sw26 trigger", 27: "sw27 trigger", 28: "sw28 saucer kicker", 29: "sw29 saucer kicker",
	30: "sw30 saucer kicker", 31: "sw31 ramp trigger", 32: "sw32 ramp trigger", 33: "sw33 hit target", 34: "sw34 hit target",
	35: "sw35 hit target", 36: "sw36 hit target", 41: "sw41 hit target", 42: "sw42 hit target", 43: "sw43 hit target", 44: "sw44 spinner",
	45: "sw45 kicker", 46: "Bumper1", 47: "Bumper2", 48: "Bumper3",
}

LAMP_MATRIX_LABELS = [
	"Green Target 4", "Green Target 3", "Green Target 2", "Green Target 1", "Green Sight 4", "Green Sight 3", "Green Sight 2", "Green Sight 1",
	"Yellow Target 1", "Yellow Target 2", "Yellow Target 3", "Yellow Sight 3", "Yellow Sight 2", "Yellow Sight 1", "ROBOCOP Mask", "Right Outlane",
	"Eject robocOp", "Eject robocoP", "Trapball Top", "Relite Laser Kick", "Right Extra Ball", "Red Trap Ball", "Red Sight", "Right Return",
	"Eject Robocop", "Eject rObocop", "Eject roBocop", "Eject robOcop", "Eject roboCop", "Spinner Green", "Spinner Yellow", "Spinner Red",
	"Bottom Special", "2x Mult.", "3x Mult.", "Bonus Hold", "4x Mult.", "5x Mult.", "Bottom Target Practice", "Extra Ball",
	"Back Red", "Back Yellow", "Back Green", "Left Return", "Laser Kick Outlane", "Left Outlane", "ROBOCOP Green", "ROBOCOP Orange",
	"2 Lane", "0 Lane", "9 Lane", "Ball Guide 1", "Ball Guide 2", "Ball Guide 3", "Ball Guide 4", "Not Used",
	"Arrest Emil", "Arrest Bodd", "Arrest Jones", "ED 209 1 Meg", "Ramp Special", "Ramp Jackpot", "ED 209 Left", "ED 209 Right",
]
# Printed lamp-description list (printed page 23, PDF page 27), literal.
LAMP_LIST_LABELS = [
	"Green Target 4", "Green Target 3", "Green Target 2", "Green Target 1", "Green Sight 4", "Green Sight 3", "Green Sight 2", "Green Sight 1",
	"Yellow Target 1", "Yellow Target 2", "Yellow Target 3", "Yellow Sight 3", "Yellow Sight 2", "Yellow Sight 1", "ROBOCOP Mask", "Right Outlane",
	"Eject robocOp", "Eject robocoP", "Trap Ball Top", "Relite Laser Kick", "Right Extra Ball", "Red Trap Ball", "Red Sight", "Right Return",
	"Eject Robocop", "Eject rObocop", "Eject roBocop", "Eject robOcop", "Eject roboCop", "Spinner Green", "Spinner Yellow", "Spinner Red",
	"Bottom Special", "2X Multiplier", "3X Multiplier", "Bonus Hold", "4X Multiplier", "5X Multiplier", "Bottom Target Practice", "Extra Ball",
	"Back Panel Red", "Back Panel Yellow", "Back Panel Green", "Left Return", "Laser Kick Outlane", "Left Outlane", "ROBOCOP Green", "ROBOCOP Orange",
	"2 Lane", "0 Lane", "9 Lane", "Ball Guide 1", "Ball Guide 2", "Ball Guide 3", "Ball Guide 4", "Not Used",
	"Arrest Emil", "Arrest Boddecker", "Arrest Jones", "ED 209 Million", "Ramp Special", "Ramp Jackpot", "ED 209 Left", "ED 209 Right",
]
BACK_PANEL_LAMPS = {41, 42, 43}
UNLOCATED_LAMPS = {44, 63, 64}

RAW_LAMP_POINTS = {
	1: (250.0, 1095.125), 2: (231.25, 1167.875), 3: (211.25, 1245.5), 4: (187.7495, 1319.9375), 5: (299.25, 1162.75), 6: (275.75, 1240.25),
	7: (253.0, 1319.0), 8: (227.75, 1397.5), 9: (429.5, 1019.9375), 10: (486.25, 1046.625), 11: (542.25, 1067.875), 12: (540.25, 1162.75),
	13: (484.0, 1137.75), 14: (427.75, 1111.25), 15: (439.5, 1370.8125), 16: (823.25, 1565.3125), 17: (824.875, 964.5), 18: (805.5, 1028.4375),
	19: (895.75, 1018.375), 20: (862.375, 1106.9375), 21: (778.875, 1109.9375), 22: (755.25, 1339.0), 23: (710.5, 1401.0), 24: (756.875, 1543.8125),
	25: (899.375, 640.1875), 26: (896.125, 709.0), 27: (880.75, 770.9375), 28: (862.625, 836.5), 29: (844.0, 901.3125), 30: (265.5, 963.75),
	31: (249.375, 884.0625), 32: (232.875, 806.3125), 33: (306.625, 1774.6875), 34: (339.5, 1811.625), 35: (387.0, 1832.25), 36: (443.75, 1825.75),
	37: (500.0, 1833.125), 38: (546.75, 1813.875), 39: (583.375, 1771.1875), 40: (438.25, 2014.3125), 44: (127.625, 1552.3125),
	45: (57.5, 1690.75), 46: (58.625, 1571.9375), 47: (438.0, 1575.0), 48: (438.0, 1575.0), 49: (384.625, 270.4375), 50: (487.625, 260.4375),
	51: (587.5, 249.0625), 52: (334.5, 410.75), 53: (438.5, 401.25), 54: (539.5, 391.25), 55: (639.5, 379.25), 57: (711.0, 909.0),
	58: (686.0, 999.0), 59: (660.0, 1090.0), 60: (635.0, 1187.0), 61: (608.0, 1278.0), 62: (584.0, 1369.0), 63: (167.625, 572.875), 64: (309.625, 509.375),
}
LAMP_OBJECTS = {44: "L24a", 52: "Light44", 53: "Light46", 54: "Light48", 55: "Light50"}

SPECIAL_DE_PERMUTATION = (3, 4, 5, 1, 0, 2)
SPECIAL_PIA_HANDLER_TO_PRINTED = {0: 6, 1: 5, 2: 2, 3: 3, 4: 1, 5: 4}
SPECIAL_PUBLIC_TO_PRINTED = {17 + SPECIAL_DE_PERMUTATION[handler]: printed for handler, printed in SPECIAL_PIA_HANDLER_TO_PRINTED.items()}
SPECIAL_PRINTED = {
	1: ("Right Turbo Bumper", "Q8", "BLU-ORN", "CPU CN19-3", "ORN-BLK", "CPU CN18-2"),
	2: ("Center Turbo Bumper", "Q9", "BLU-RED", "CPU CN19-4", "ORN-RED", "CPU CN18-3"),
	3: ("Left Slingshot", "Q10", "BLU-YEL", "CPU CN19-6", "ORN-YEL", "CPU CN18-4"),
	4: ("Left Turbo Bumper", "Q11", "BLU-BRN", "CPU CN19-7", "ORN-BRN", "CPU CN18-5"),
	5: ("Right Slingshot", "Q12", "BLU-GRN", "CPU CN19-8", "ORN-GRN", "CPU CN18-8"),
	6: ("Unused SP6 Driver", "Q13", None, "CPU CN19-9", None, "CPU CN18-9"),
}
SPECIAL_SWITCHES = {1: 48, 2: 47, 3: 21, 4: 46, 5: 22}

# (printed device, transistor, drive wire, part or bulbs)
DRIVER_ROWS = {
	1: ("Jackpot Flash", "Q46", "GRY-BRN", "(3) No.89 + (1) No.906"), 25: ("Outhole", "Q46", "GRY-BRN", "23-840"),
	2: ("Special Flash", "Q45", "GRY-RED", "(1) No.906"), 26: ("Trough", "Q45", "GRY-RED", "23-840"),
	3: ("ED209 1 MEG", "Q44", "GRY-ORN", "(2) #89 + (1) #906"), 27: ("Middle Eject", "Q44", "GRY-ORN", "27-1300"),
	4: ("Jones Flash", "Q43", "GRY-YEL", "(1) #89 + (1) #906"), 28: ("Ball Guide Eject", "Q43", "GRY-YEL", "27-1300"),
	5: ("Bodd Flash", "Q42", "GRY-GRN", "(1) #89 + (1) #906"), 29: ("Right Eject", "Q42", "GRY-GRN", "27-1300"),
	6: ("Emil Flash", "Q41", "GRY-BLU", "(1) #89 + (1) #906"), 30: ("Vertical Up Kicker", "Q41", "GRY-BLU", "23-800"),
	7: ("Left Middle", "Q40", "GRY-VIO", "(3) #89 + (1) #906"), 31: (None, "Q40", "GRY-VIO", None),
	8: ("Top Left", "Q39", "GRY-BLK", "(1) #906"), 32: (None, "Q39", "GRY-BLK", None),
	9: ("Middle Blue", "Q30", "BRN-BLK", "(2) #89 + (2) #906"), 10: ("Left/Right Coil Relay K1 (PPB)", "Q29", "BLK-RED", "K1"),
	11: ("General Illum. Relay K1 (PS board)", "Q28", "BRN-ORN", "K1"), 12: ("Middle Red", "Q27", "BRN-YEL", "(2) #89 + (2) #906"),
	13: ("Right Blue", "Q26", "BRN-GRN", "(2) #89 + (2) #906"), 14: ("Ramp Red", "Q25", "BRN-BLU", "(1) #89 + (3) #906"),
	15: ("Ramp Blue", "Q24", "BRN-VIO", "(1) #89 + (3) #906"), 16: ("Laserkick", "Q23", "WHT-GRY", "23-800"),
}
SOLENOID_LABELS = {
	1: "Jackpot Flash", 2: "Special Flash", 3: "ED 209 1 Meg Flash", 4: "Jones Flash", 5: "Bodd Flash", 6: "Emil Flash", 7: "Left Middle Flash", 8: "Top Left Flash",
	9: "Middle Blue Flash", 10: "A/B Coil Relay K1", 11: "General Illumination Relay K1", 12: "Middle Red Flash", 13: "Right Blue Flash", 14: "Ramp Red Flash",
	15: "Ramp Blue Flash", 16: "Laser Kick", **{public: SPECIAL_PRINTED[printed][0] for public, printed in SPECIAL_PUBLIC_TO_PRINTED.items()},
	24: "Unused Solenoid 24", 25: "Outhole Kicker", 26: "Trough Eject", 27: "Left (Middle) Eject", 28: "Top (Ball Guide) Eject", 29: "Right Eject",
	30: "Vertical Up Kicker", 31: "Unfitted Mux Branch R07", 32: "Unfitted Mux Branch R08", 20: "Unfitted Special-Solenoid Driver SP6",
	45: "Synthetic Right Flipper Power", 46: "Synthetic Right Flipper Hold", 47: "Synthetic Left Flipper Power", 48: "Synthetic Left Flipper Hold",
	49: "Simulation Ball Shooter", 50: "Reserved Solenoid 50",
}
for _number in range(33, 45):
	SOLENOID_LABELS[_number] = f"Inert Solenoid Address {_number}"
FLASH_OUTPUTS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15)
# Schematic bulb totals, and the bulbs the coil-location page's separate "Backbox Flash lamps" inset assigns to each output.
FLASH_TOTALS = {1: 4, 2: 1, 3: 3, 4: 2, 5: 2, 6: 2, 7: 4, 8: 1, 9: 4, 12: 4, 13: 4, 14: 4, 15: 4}
FLASH_BACKBOX = {1: 3, 3: 2, 4: 1, 5: 1, 6: 1, 7: 3, 9: 2, 12: 2, 13: 2, 14: 1, 15: 1}
RAW_FLASH_POINTS = {
	1: [("F62", 583.125, 1368.25)], 2: [("F61", 609.375, 1277.125)], 3: [("F60", 634.125, 1185.375)], 4: [("F59", 660.125, 1090.125)],
	5: [("F58", 686.125, 999.625)], 6: [("F57", 711.375, 908.125)], 7: [("F7", 108.0, 1035.0), ("F7a", 108.0, 1057.0)], 8: [("F8", 170.0, 273.0)],
	9: [("F9", 325.875, 1301.125), ("F9a", 311.0, 1354.25), ("F9b", 341.0, 1246.25)],
	12: [("F12", 479.375, 1213.125), ("F12a", 440.5, 1195.75), ("F12b", 529.0, 1236.25)],
	13: [("F13", 630.375, 1503.125), ("F13a", 601.0, 1540.25), ("F13b", 663.0, 1461.25)],
	14: [("F14", 751.125, 767.8125), ("F14a", 773.75, 641.5625), ("F14b", 794.625, 512.9375)],
	15: [("F15", 762.5, 705.3125), ("F15a", 785.75, 577.6875), ("F15b", 793.5, 448.8125)],
}
COIL_EFFECT_POINTS = {
	16: ("KickBack plunger", (57.75, 1945.375)), 25: ("Drain kicker", (448.0, 2156.0)), 26: ("BallRelease kicker", (837.125, 1973.625)),
	27: ("sw28 saucer", (62.75, 447.625)), 28: ("sw29 saucer", (300.75, 201.125)), 29: ("sw30 saucer", (849.75, 222.125)), 30: ("sw45 kicker", (95.0, 906.5)),
	17: ("Bumper3", (637.5, 622.5)), 18: ("LeftSlingShot wall centroid", (220.356675, 1656.495075)), 19: ("Bumper1", (425.0, 621.5)),
	21: ("RightSlingShot wall centroid", (666.60631, 1645.305)), 22: ("Bumper2", (530.0, 828.5)),
}
# The GI collection the table's solenoid 11 callback switches, less the four objects it also binds to lamps 52-55.
RAW_GI_POINTS = [
	("Light7", 839.5, 1347.5), ("Light49", 638.25, 379.75), ("Light47", 537.75, 391.75), ("Light67", 334.25, 411.25), ("Light35", 837.75, 615.375),
	("Light36", 842.75, 475.875), ("Light37", 830.25, 352.375), ("Light39", 693.0, 335.25), ("Light38", 754.25, 250.5), ("Light54", 910.0, 169.125),
	("Light53", 65.0, 169.125), ("Light52", 200.5, 283.125), ("Light40", 146.0, 753.5), ("Light41", 126.5, 666.5), ("Light42", 236.5, 548.625),
	("Light34", 821.25, 738.875), ("Light8", 937.5, 863.0), ("Light10", 49.5, 1309.75), ("Light13", 151.0, 1006.625), ("Light11", 99.0, 1212.625),
	("Light12", 127.0, 1098.625), ("Light5", 213.0, 1741.75), ("Light4", 149.5, 1828.0), ("Light1", 732.5, 1818.5), ("Light2", 669.0, 1729.25),
	("Light3", 711.5, 1584.75), ("Light6", 169.5, 1590.5), ("Light43", 252.0, 482.625), ("Light45", 437.75, 401.75), ("Light51", 142.5, 346.75),
	("Light80", 488.5, 1179.0), ("F2", 530.0, 828.5), ("F3", 637.5, 623.25), ("F1", 425.5, 621.75), ("Light14", 821.0, 740.5),
	("Light9", 840.0, 616.5), ("Light15", 843.0, 475.5), ("Light16", 831.0, 352.5), ("Light17", 496.5, 902.625),
	("LeftFlipperLight", 281.75, 1922.625), ("RightFlipperLight", 597.75, 1923.0), ("Light18", 438.8025, 441.1742), ("Light19", 540.2504, 428.86172),
	("Light20", 640.66595, 414.711), ("Light21", 335.63367, 451.6138),
]


def readings() -> dict:
	return json.loads((ROOT / READINGS_PATH).read_bytes())


def excerpt_switch_matrix() -> str:
	rows = [
		"# RoboCop switch matrix transcription", "",
		"Source: PDF pages 24-25, printed pages 20-21. Read from 300 dpi renders; the PDF text layer is noisy OCR and was used only to locate the pages and as a second reading.", "",
		"Printed drive headers: " + ", ".join(f"`{wire} ({code}) {transistor}`" for wire, code, transistor in zip(SWITCH_DRIVES, SWITCH_DRIVE_CODES, SWITCH_DRIVE_TRANSISTORS)) + ".", "",
		"Printed return headers: " + ", ".join(f"`{wire} ({code})`" for wire, code in zip(SWITCH_RETURNS, SWITCH_RETURN_CODES)) + ".", "",
		"| Row / return | " + " | ".join(SWITCH_DRIVES) + " |",
		"| --- | " + " | ".join("---" for _ in SWITCH_DRIVES) + " |",
	]
	for row, return_wire in enumerate(SWITCH_RETURNS):
		cells = [f"{column * 8 + row + 1} {SWITCH_MATRIX_LABELS[column * 8 + row + 1]}" for column in range(8)]
		rows.append("| " + return_wire + " | " + " | ".join(cells) + " |")
	rows.extend([
		"", "Printed footnote: `(*) 2 DIGIT NUMBER IN PARENTHESES INDICATES RESISTOR/WIRE COLOR CODE NUMBER DISPLAYED DURING DIAGNOSTICS.`", "",
		"## Printed switch part numbers and locations", "",
		"The list prints one row per address; two-line cells are joined here with `;`.", "",
	])
	for number in range(1, 49):
		description, part = SWITCH_LIST[number]
		mark = "*" if number in CABINET_SWITCHES else ""
		rows.append(f"- {number:02d}{mark}: {description}" + (f" — `{part}`" if part else ""))
	rows.extend(["- 49: Not Used Thru 64", "", "Printed footnote: `*INDICATES CABINET SWITCHES.`", ""])
	return "\n".join(rows)


def excerpt_lamp_matrix() -> str:
	rows = [
		"# RoboCop lamp matrix transcription", "",
		"Source: PDF pages 26-27, printed pages 22-23. Read from 300 dpi renders; the PDF text layer was a locator and second reading only.", "",
		"Printed drive headers: " + ", ".join(f"`{wire} ({code}) {transistor}`" for wire, code, transistor in zip(LAMP_DRIVES, LAMP_DRIVE_CODES, LAMP_DRIVE_TRANSISTORS)) + ".", "",
		"Printed return headers: " + ", ".join(f"`{wire} ({code}) {transistor}`" for wire, code, transistor in zip(LAMP_RETURNS, LAMP_RETURN_CODES, LAMP_RETURN_TRANSISTORS)) + ".", "",
		"| Row / return | " + " | ".join(LAMP_DRIVES) + " |",
		"| --- | " + " | ".join("---" for _ in LAMP_DRIVES) + " |",
	]
	for row, return_wire in enumerate(LAMP_RETURNS):
		cells = [f"{column * 8 + row + 1} {LAMP_MATRIX_LABELS[column * 8 + row]}" for column in range(8)]
		rows.append("| " + return_wire + " | " + " | ".join(cells) + " |")
	rows.extend(["", "## Printed lamp description list (printed page 23)", ""])
	for number, label in enumerate(LAMP_LIST_LABELS, start=1):
		rows.append(f"- {number:02d}: {label}")
	rows.extend([
		"", "Printed footnote: `*Indicates Insert Lamp`; no row in the list carries an asterisk.", "",
		"## Printed lamp location drawing (printed page 23)", "",
		"The drawing places 41, 42 and 43 in a row of three circles drawn above the playfield's top arch, outside the playfield outline: the back panel. "
		"It locates every other used lamp on the playfield plan except 44, 63 and 64, which appear nowhere on the page; 56 is not used. "
		"47 and 48 are drawn as two separate circles one above the other at the lower center.", "",
	])
	return "\n".join(rows)


def excerpt_coils() -> str:
	rows = [
		"# RoboCop coil, flash, relay, flipper and special-solenoid transcription", "",
		"Source: PDF pages 28-29, printed pages 24-25. Read from 300 dpi renders, the coil schematic re-rendered at 600 dpi.", "",
		"## Coil schematic (printed page 25)", "",
		"The A/B bank pairs share one TIP122 driver and CN-11 wire; side R carries no R07 or R08 branch.", "",
		"| Printed driver | Transistor | Wire | Device | Type / bulbs |", "| --- | --- | --- | --- | --- |",
	]
	for number in list(range(1, 9)) + list(range(25, 33)) + list(range(9, 17)):
		device, transistor, wire, part = DRIVER_ROWS[number]
		printed = f"SIDE L {number:02d}" if number <= 8 else (f"SIDE R {number - 24:02d}" if number >= 25 else f"{number:02d}")
		rows.append(f"| {printed} | {transistor} | {wire} | {device or 'no branch printed'} | {part or '—'} |")
	rows.extend([
		"", "Output 16 drives the Laserkick 23-800 coil through `Q5 TIP36C`, `BRN-GRY`, `+50V`.", "",
		"## Switch-triggered solenoids (printed page 24)", "",
		"| Printed | Device | Control | Trigger | Transistor | Coil |", "| --- | --- | --- | --- | --- | --- |",
	])
	for printed, (device, transistor, control, control_pin, trigger, trigger_pin) in SPECIAL_PRINTED.items():
		rows.append(f"| SP{printed} | {'NOT USED' if printed == 6 else device} | {(control + ' ') if control else ''}{control_pin} | {(trigger + ' ') if trigger else ''}{trigger_pin} | {transistor} | {'—' if printed == 6 else '23-800'} |")
	rows.extend([
		"", "Every SP row prints power `RED PS CN3-6` (written once and repeated for SP2-SP5; printed again on SP6).", "",
		"## Flippers (printed page 24)", "",
		"| Flipper | CPU | Flipper board | Power | Coil |", "| --- | --- | --- | --- | --- |",
		"| Left Flipper | ORN-GRY CPU CN19-2 | BLU-GRY CN1-8 | GRY-YEL CN2-1,2 | 22-900 |",
		"| Right Flipper | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLU-YEL CN2-3,4 | 22-900 |", "",
		"Power input: `BLK-WHT 50VDC`; `GRY,GRY GRN 8VAC`.", "",
		"## ROBOCOP COIL PART NUMBER CHART (printed page 24)", "",
		"| Quantity used | Coil type | Data East Pinball part number |", "| --- | --- | --- |",
		"| 6 | 23-800 | 090-5001-00 |", "| 3 | 27-1300 | 090-5003-00 |", "| 2 | 23-840 | 090-5005-00 |", "| 2 | 22-900 | 090-5020-20 |", "",
		"The schematic itself draws seven 23-800 coils (Vertical Up Kicker, Laserkick and SP1-SP5) against the chart's six; both readings are kept.", "",
		"## Coil location drawing (printed page 24)", "",
		"Callouts on the playfield plan: `L08` top left; `R04` top center; `R05` top right; `R03` upper left; `R06` at the left kicker; `L07` left; "
		"`L06`, `L05`, `L04`, `L03`, `L02`, `L01` top to bottom down the center-right ladder; `12` and `09` center; `13` lower center right; "
		"`15`, `14`, `15`, `14`, `15`, `14` alternating up the right ramp; `16` lower left outlane; `R02` and `R01` at the trough below the flippers. "
		"No flipper, slingshot or turbo-bumper callout is printed.", "",
		"The separate `Backbox Flash lamps` inset prints nineteen bulb circles labelled `L09`, `L09`, `L07`, `L01`, `L07`, `L01`, `L07`, `L01`, `13`, `13` "
		"(top row), `15`, `L03`, `14`, `L03` (middle row) and `12`, `12`, `L06`, `L04`, `L05` (bottom row). `L09` is printed with an L prefix although output 9 "
		"is a direct driver.", "",
	])
	return "\n".join(rows)


def excerpt_mechanisms() -> str:
	return """# RoboCop mechanism-construction transcription

Source: PDF page 31, printed page 27, `Playfield Top Parts`. Read from a 200 dpi render; the PDF text layer was a second reading only.

The whole 75-item list follows. The page prints the fractions in items 3-5, 57, 58 and 75 as stacked superscript/subscript numerals; they are written here inline. The item-number callouts on the page's playfield drawing are not transcribed.

| Item | Description | Part Number |
| --- | --- | --- |
| 1 | Red Mini Lamp - ED 209 (2)* | 165-5005-02 |
| 2 | Acorn Cap Nuts (27)* | 240-5006-00 |
| 3 | 5/8 " Hex Spacer (2) | 254-5008-02 |
| 4 | 7/8 " Hex Spacer (2) | 254-5008-05 |
| 5 | 1/2 " Hex Spacer (3) | 254-5008-03 |
| 6 | Ball Deflector Spring | 265-5010-00 |
| 7 | Ball Trough Eject Assy. | 500-5012-00 |
| 8 | Slingshot Assy. (2) | 500-5077-00 |
| 9 | 3 Bank S.U. Tgt. Assy | 500-5103-16 |
| 10 | Turbo Bumper Assy. (3) | 500-5034-10 |
| 11 | Playfield Eject Assy. (3) | 500-5051-02 |
| 12 | Vertical Up Kicker | 500-5067-00 |
| 13 | 10 Point S.U. Switch (2) | 500-5069-00 |
| 14 | Laser Kick Assy. | 500-5080-00 |
| 15 | Outhole Kicker Assy. | 500-5082-00 |
| 16 | Right Side Ball Guide | 500-5149-00 |
| 17 | Ball Guide -VUK | 500-5151-00 |
| 18 | Laser Kick Ball Guide | 500-5150-00 |
| 19 | Center Top Ball Guide | 500-5152-00 |
| 20 | Left Top Ball Guide | 500-5153-00 |
| 21 | Left of Spinner Ball Guide | 500-5154-00 |
| 22 | Right Flipper Assembly | 500-5177-01 |
| 23 | Left Flipper Assembly | 500-5177-02 |
| 24 | Playfield Complete Assy. | 505-6004-06 |
| 25 | Flipper Bat and Shaft (2) | 515-5133-02 |
| 26 | Left Catch Ramp Assy.* | 515-5207-00 |
| 27 | Right Ramp Assy. * | 515-5208-00 |
| 28 | 4 Bank S.U. Tgt. Assy. | 515-5211-14 |
| 29 | Spinning Target | 515-5236-00 |
| 30 | Machine Mini Post (2) | 530-5005-00 |
| 31 | Top Thread. Bump. Post (4) | 530-5007-00 |
| 32 | Grooved Metal Stand Off (9) | 530-5035-02 |
| 33 | Bumper Post | 530-5057-00 |
| 34 | Outlane Adjustment Plate | 535-5091-02 |
| 35 | One Way Gate Mtg.Brkt. | 535-5210-00 |
| 36 | One Way Gate Mtg.Brkt. | 535-5210-01 |
| 37 | Spin.Tgt. Support Bracket | 535-5249-00 |
| 38 | VUK Ball Stop Brkt. | 535-5273-00 |
| 39 | ROBOCOP Btm.Ball Gd. Wr. | 535-5300-06 |
| 40 | Right Drain Ball Guide Wire | 535-5300-12 |
| 41 | ROBOCOP Top Ball Gd. Wr.2 | 535-5300-14 |
| 42 | Boot-a-Ball Guide Wire | 535-5300-15 |
| 43 | Wire Gate (2) | 535-5307-05 |
| 44 | Spin. Sw. Actuator Wire | 535-5319-00 |
| 45 | Shooter Lane Wire Ramp | 535-5349-00 |
| 46 | VUK Left Flip. Feed Ramp | 535-5355-00 |
| 47 | Top Left Ball Guide Wire | 535-5362-00 |
| 48 | Right Eject Ball Guide | 535-5363-00 |
| 49 | Rt. Of Spinner Ball Gd. Wire | 535-5364-00 |
| 50 | Left Flip. Ball Return Guide | 535-5406-01 |
| 51 | Right Flip. Ball Return Guide | 535-5407-01 |
| 52 | Right Eject Ball Stop Brkt. | 535-5749-00 |
| 53 | Shooter Lane Sd. Rail Guard | 535-5795-00 |
| 54 | Bracket under Right Ramp | 535-5815-00 |
| 55 | 2 Sided Clear Ball Guide (2) | 545-5011-01 |
| 56 | 1 Sided Clear Ball Guide (2) | 545-5012-01 |
| 57 | 1 1/16" Clear Post (8) | 545-5013-01 |
| 58 | 1 1/16" Red Post (13) | 545-5013-02 |
| 59 | Turbo Bumper Cap (3) | 545-5035-35 |
| 60 | Spinning Target Washer (2) * | 545-5037-00 |
| 61 | Red Mini-Mars (Twist In) | 545-5059-02 |
| 62 | Yellow Eject Playfield Insert | 545-5060-06 |
| 63 | Plastic ED 209* | 545-5152-00 |
| 64 | Robocop Decal Sheet* | 820-5020-XX |
| 65 | Left Catch Arrow Sticker* | 820-5030-00 |
| 66 | Spinner Decal Front* | 820-5206-01 |
| 67 | Spinner Decal Back* | 820-5206-02 |
| 68 | Turbo Bumper Decal (3) | 820-5306-00 |
| 69 | Playfield Protective Mylar | 820-5807-00 |
| 70 | Screened Playfield | 830-5106-00 |
| 71 | Screened Plastics | 830-5406-XX |
| 72 | Bottom Arch | 830-5506-01 |
| 73 | Shooter Guage | 830-5506-02 |
| 74 | Ramp Sw. Act. Wire (2)* | 535-5361-00 |
| 75 | 1 1/16 " Blue Post (7)* | 545-5013-05 |

The page footnote reads `* Indicates Not Shown`.

The list prints no assembly for the right trap ball. The manual's only records of it are switch 23 `Right Trap Ball` (part `500-5035-02`) and lamps 19 `Trap Ball Top` and 22 `Red Trap Ball`.

The list prints no drop-target bank, diverter, magnet or motor.
"""


def excerpt_vpm() -> str:
	return f"""# Data East RoboCop (1989) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`{SCRIPT_SHA256}`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256
`{VPM_DE_SHA256}`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `{VPM_CORE_SHA256}`). Read from the files.

`script.vbs` line 102 loads the library and line 135 leaves keyboard handling to the script:

```vbscript
LoadVPM "01560000", "DE.VBS", 3.46
       .HandleKeyboard=0
```

`de.vbs` lines 33-36:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 86
Const swULFlip       = 88
```

`de.vbs` `vpmKeyDown` (line 62) sets the lower flipper switches from the cabinet keys (lines 67 and 73), and `vpmKeyUp` (line 94) clears them the same way with `= False` (lines 99 and 105):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The table's key handling, with the flipper and library lines:

```vbscript
Sub Table1_KeyDown(ByVal Keycode)   ' line 259
	If keycode=RightFlipperKey Then Controller.Switch(15)=1   ' line 260
	If keycode=LeftFlipperKey Then Controller.Switch(16)=1   ' line 261
...
	If vpmKeyDown(keycode)Then Exit Sub   ' line 286
...
Sub Table1_KeyUp(ByVal Keycode)   ' line 290
	If keycode=RightFlipperKey Then Controller.Switch(15)=0   ' line 292
    If keycode=LeftFlipperKey Then Controller.Switch(16)=0   ' line 293
...
	If vpmKeyUp(keycode)Then Exit Sub   ' line 309
```

The trailing `' line NNN` markers above are added here to give the location and are not in the script.

Lines 260-261 and 292-293 write 15 from the right key and 16 from the left, the reverse of the driver's `FLIP1516 = FLIP_SWNO(15,16)`. Those writes have no effect: `core_updateSw` overwrites 15 and 16 from the cabinet-button bits 84 and 82 on every update, and lines 286 and 309 write those bits through `vpmKeyDown`/`vpmKeyUp`.

The script never calls `vpmInit`, `NoUpperLeftFlipper` or `NoUpperRightFlipper` and never names a staged flipper key.
"""


EXCERPTS = {
	EXCERPT_DIR / "switch-matrix.md": excerpt_switch_matrix(),
	EXCERPT_DIR / "lamp-matrix.md": excerpt_lamp_matrix(),
	EXCERPT_DIR / "coil-and-flipper.md": excerpt_coils(),
	EXCERPT_DIR / "mechanism-construction.md": excerpt_mechanisms(),
	EXCERPT_DIR / "vpm-script-library-flippers.md": excerpt_vpm(),
}
EXCERPT_LOCATORS = {
	"switch-matrix.md": "PDF pages 24-25, printed pages 20-21",
	"lamp-matrix.md": "PDF pages 26-27, printed pages 22-23",
	"coil-and-flipper.md": "PDF pages 28-29, printed pages 24-25",
	"mechanism-construction.md": "PDF page 31, printed page 27",
}


def sha256_text(value: str) -> str:
	return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def provenance(status: str, *source_refs: str) -> dict[str, object]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def aliases(namespace: str, number: int | str, manual: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(number)}]
	if manual is not None:
		result.append({"namespace": "manual.address", "value": manual})
	return result


def not_applicable(reason: str, status: str, *source_refs: str) -> dict[str, object]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(status, *source_refs)}


def norm(point: tuple[float, float]) -> tuple[float, float]:
	x, y = point
	if not (0.0 <= x <= RIGHT and 0.0 <= y <= BOTTOM):
		raise ValueError(f"out-of-bounds retained point: {point}")
	return round(x / RIGHT, 6), round(y / BOTTOM, 6)


def located(device_id: str, points: list[tuple[float, float]], role: str, status: str, *source_refs: str) -> dict[str, object]:
	placements = []
	for index, raw in enumerate(points, start=1):
		x, y = norm(raw)
		placements.append({"id": f"{device_id}.placement-{index}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(status, *source_refs)})
	return {"status": status, "placements": placements}


def rom_switch_name(number: int) -> str:
	return readings()["switch_test"][str(number)]


def switch_input(number: int) -> dict[str, object]:
	matrix_label = SWITCH_MATRIX_LABELS[number]
	unused = matrix_label == "Not Used"
	device_id = f"switch.matrix-{number}"
	column, row = divmod(number - 1, 8)
	rom = "LEFT FLIPPER" if number == 15 else ("RIGHT FLIPPER" if number == 16 else rom_switch_name(number))
	code = f"{SWITCH_RETURN_CODES[row]}-{SWITCH_DRIVE_CODES[column]}"
	physical: dict[str, object] = {
		"notes": (
			f"Manual matrix column {column + 1}, row {row + 1}, printed cell '{matrix_label}'; the part list prints "
			f"'{SWITCH_LIST.get(number, ('Not Used', None))[0] if number <= 48 else 'Not Used'}'. The ROM's own Switch Test names this address "
			f"'{rom}' with wire code {code} (retained runtime evidence). Every matrix contact rests open: the ROM's Active Switch test shows NONE "
			"with all public switches at 0."
		),
	}
	if number <= 48 and SWITCH_LIST[number][1] and number not in (15, 16):
		physical["part_number"] = SWITCH_LIST[number][1]
	if number in CABINET_SWITCHES:
		physical["location"] = "cabinet"
	if number in (15, 16):
		button = 84 if number == 15 else 82
		side = "left" if number == 15 else "right"
		physical["notes"] += (
			f" The manual prints the {side} flipper's Instant Info button and end-of-stroke contact here. FLIP1516 publishes the {side} cabinet-button "
			f"state at this address: with keyboard handling off core_updateSw rewrites it on every update from PinMAME's flipper column, public {button} "
			f"({'CORE_SWLLFLIPBUTBIT' if number == 15 else 'CORE_SWLRFLIPBUTBIT'}), and the ROM's Switch Test names the held {side} flipper key "
			f"'{rom}' at this address. A consumer drives {button}, not this address. The retained script also writes this address from the "
			f"{'right' if number == 15 else 'left'} flipper key (script lines {'260/292' if number == 15 else '261/293'}), the opposite side; "
			"core_updateSw overwrites that write, so it has no effect (excerpt vpm-script-library-flippers)."
		)
	if number == 17:
		physical["notes"] += " The part list names this switch 'Left Outlane' where the matrix and the ROM name it Laser Kick; both denote the left-outlane rollover in front of the Laser Kick."
	if number in (28, 29, 30):
		physical["notes"] += {
			28: " The ROM names this saucer MID EJECT and the coil schematic calls its kicker Middle Eject; the matrix and part list call it Left Eject. All denote the upper-left saucer the coil location drawing marks R03.",
			29: " The matrix prints Center Eject, the part list and the ROM Top Eject; the coil schematic calls its kicker Ball Guide Eject. All denote the top saucer the coil location drawing marks R04.",
			30: " The coil location drawing marks its kicker R05 at the top right.",
		}[number]
	if number in (37, 38):
		physical["notes"] += " The retained table has no object or handler for this switch, so it is never closed in that recreation; the manual's playfield parts list prints the two 10 Point S.U. Switches (500-5069-00) but the drawing does not register their positions."
	if number == 46:
		physical["notes"] += " Bumper1, the left turbo bumper, pulses this address. The retained table's Bumper3 handler, the right turbo bumper, also pulses 46 instead of 48 — a defect in that table."
	if number == 48:
		physical["notes"] += " The retained table never closes this address: its right turbo bumper (Bumper3) pulses 46. The candidate placement is Bumper3's center, matched by position and by the manual's switch name."
	if number in (11, 12, 13):
		physical["notes"] += " The retained table models the trough as a cvpmBallStack (InitSw 10, 13, 12, 11) with no physical object for this switch."
	source_refs = [MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE, SCRIPT_SOURCE]
	result: dict[str, object] = {
		"id": device_id, "label": f"Unused Switch {number}" if unused else SWITCH_LABELS[number], "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number}, "aliases": aliases("pinmame.switch", number, str(number)),
		"availability": "unused" if unused else "used", "physical": physical,
		"wiring": {"board": "CPU Board", "drive_wire": SWITCH_DRIVES[column], "return_wire": SWITCH_RETURNS[row]},
		"provenance": provenance("validated", *source_refs),
	}
	roles = {
		1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin", 7: "cabinet.slam-tilt",
		10: "ball.position", 11: "ball.position", 12: "ball.position", 13: "ball.position", 14: "ball.position", 17: "ball.position",
		15: "flipper.lower.left.button", 16: "flipper.lower.right.button", 28: "ball.position", 29: "ball.position", 30: "ball.position", 45: "ball.position",
	}
	if number not in (15, 16):
		result["normally_closed"] = False
	if number in (11, 12, 13):
		result["initial_active"] = True
	if number in roles:
		result["roles"] = [roles[number]]
	if unused:
		result["spatial"] = not_applicable("unused", "validated", MANUAL_SOURCE, RUNTIME_SOURCE)
	elif number in CABINET_SWITCHES or number in (15, 16):
		result["spatial"] = not_applicable("cabinet_or_service", "validated", MANUAL_SOURCE, CORE_SOURCE)
	elif number in RAW_SWITCH_POINTS:
		status = "candidate" if number == 48 else "observed"
		result["spatial"] = located(device_id, [RAW_SWITCH_POINTS[number]], "sensor", status, TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	return result


def diagnostic_inputs() -> list[dict[str, object]]:
	result = []
	for device, suffix, label, role, note in [
		(-7, "7", "Black Button / Step", "service.advance", "The ROM steps its tests on this input in the retained service walk."),
		(-6, "6", "Green Button / Forward-Reverse", "service.adjust", "The manual calls it the FORWARD/REVERSE push-button; each press toggles the direction (the retained walk presses it once to reach Switch Test in reverse and once to step the Lamp Test forward). Its contact construction and the level PinMAME publishes for it are not settled by any retained source."),
	]:
		result.append({
			"id": f"switch.diagnostic-{suffix}", "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": device},
			"aliases": [{"namespace": "pinmame.switch", "value": str(device)}], "availability": "used", "roles": [role],
			"physical": {"location": "coin door", "notes": f"Shared Data East service-door input declared by DE_COMPORTS. {note}"},
			"spatial": not_applicable("cabinet_or_service", "validated", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		})
	result.append({
		"id": "dip.jumper-w7", "label": "Jumper W7 (function undocumented)", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": 0},
		"aliases": [{"namespace": "pinmame.dip", "value": "0"}], "availability": "used",
		"physical": {"notes": "Pinned Data East input ports expose one W7 jumper; the retained manual does not document a RoboCop-specific function."},
		"spatial": not_applicable("dip_switch", "candidate", CORE_SOURCE, MANUAL_SOURCE), "provenance": provenance("candidate", CORE_SOURCE, MANUAL_SOURCE),
	})
	return result


def lamp_output(number: int) -> dict[str, object]:
	device_id = f"lamp.matrix-{number}"
	column, row = divmod(number - 1, 8)
	label = LAMP_LIST_LABELS[number - 1]
	rom = readings()["lamp_test"][str(number)]
	code = f"{LAMP_RETURN_CODES[row]}-{LAMP_DRIVE_CODES[column]}"
	unused = number == 56
	physical: dict[str, object] = {
		"notes": (
			f"Manual matrix prints '{LAMP_MATRIX_LABELS[number - 1]}'; the lamp list prints '{label}'. The ROM's own Lamp Test names this address "
			f"'{rom}' with wire code {code} (retained runtime evidence)."
		),
	}
	if not unused:
		physical["quantity"] = 1
	result: dict[str, object] = {
		"id": device_id, "label": "Unused Lamp 56" if unused else label, "kind": "lamp", "binding": {"group": "pinmame.output.lamp", "device": number},
		"aliases": aliases("pinmame.lamp", number, str(number)), "availability": "unused" if unused else "used", "physical": physical,
		"wiring": {"board": "CPU Board", "drive_wire": LAMP_DRIVES[column], "return_wire": LAMP_RETURNS[row], "driver_transistor": f"{LAMP_DRIVE_TRANSISTORS[column]} / {LAMP_RETURN_TRANSISTORS[row]}"},
		"provenance": provenance("validated", MANUAL_SOURCE, RUNTIME_SOURCE, SCRIPT_SOURCE),
	}
	if unused:
		physical["notes"] += " The manual prints no lamp here and the ROM names the address NONE; its Lamp Test still steps it, which explains the only state PinMAME publishes."
		result["spatial"] = not_applicable("unused", "validated", MANUAL_SOURCE, RUNTIME_SOURCE)
		return result
	obj = LAMP_OBJECTS.get(number, f"L{number}")
	if number in BACK_PANEL_LAMPS:
		physical["location"] = "back panel"
		physical["notes"] += (
			" The manual's lamp location drawing places this lamp in the row of three above the playfield's top arch, on the back panel. The retained "
			f"script binds it to apron-area Light L{number} and its LSample_Timer mirrors it onto Flasher F{number}; those are presentation proxies, not the socket. "
			"The back panel stands at the rear of the playfield inside the cabinet, so the lamp is a playfield-area device; no retained source registers "
			"its position on that panel, and it carries no placement."
		)
		return result
	physical["notes"] += f" The retained script binds it to Light {obj} (Set Lights({number})={obj})."
	if number in UNLOCATED_LAMPS:
		physical["notes"] += " The manual's lamp location drawing does not show this lamp."
	if number in (63, 64):
		physical["notes"] += " The playfield parts list prints 'Red Mini Lamp - ED 209 (2)', which fits the two ED 209 lamps; that pairing is an inference from the names."
	if number in (47, 48):
		physical["notes"] += " The manual draws 47 and 48 as two circles one above the other; the retained table puts both Lights at one center."
	if 52 <= number <= 55:
		physical["notes"] += f" {obj} is also a member of the table's GI collection, so the table's solenoid 11 callback switches it too; the physical machine fits it to the lamp matrix only."
	result["spatial"] = located(device_id, [RAW_LAMP_POINTS[number]], "emitter", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	return result


def solenoid_output(number: int) -> dict[str, object]:
	device_id = "coil.game-on" if number == 23 else f"coil.driver-{number}"
	if number == 23:
		return {
			"id": device_id, "label": "Game On / Flipper and Special-Solenoid Enable", "kind": "control_signal",
			"binding": {"group": "pinmame.output.solenoid", "device": 23}, "aliases": aliases("pinmame.solenoid", 23), "availability": "used",
			"physical": {"notes": "System 11 public Game On state enables the flipper and special-solenoid circuits; the retained walk sees it rise as the ROM enters its tests."},
			"spatial": not_applicable("internal_nonvisual", "validated", CORE_SOURCE), "provenance": provenance("validated", CORE_SOURCE, RUNTIME_SOURCE),
		}
	label = SOLENOID_LABELS[number]
	coil_test = readings()["coil_test"].get(str(number))
	unknown = number in (20, 31, 32)
	unused = number in {24} | set(range(33, 45)) | {49, 50}
	if number in FLASH_OUTPUTS:
		kind = "flasher"
	elif number == 10:
		kind = "relay"
	elif number == 11:
		kind = "gi"
	elif number in {20, 24} | set(range(31, 51)):
		kind = "virtual"
	else:
		kind = "coil"
	if 1 <= number <= 8:
		manual_number = f"SIDE L {number:02d}"
	elif 9 <= number <= 16:
		manual_number = f"{number:02d}"
	elif 17 <= number <= 22:
		manual_number = f"SP{SPECIAL_PUBLIC_TO_PRINTED[number]}"
	elif 25 <= number <= 32:
		manual_number = f"SIDE R {number - 24:02d}"
	else:
		manual_number = None
	physical: dict[str, object] = {"notes": f"Public solenoid {number}." + (f" Manual printed address {manual_number}." if manual_number else "")}
	source_refs = [CORE_SOURCE, SCRIPT_SOURCE]
	status = "validated"
	if number in DRIVER_ROWS:
		device, transistor, wire, part = DRIVER_ROWS[number]
		physical["notes"] += f" The coil schematic prints '{device or 'no branch'}' on {transistor}, wire {wire}."
		if coil_test:
			physical["notes"] += f" The ROM's Coil Auto test fires it as '{coil_test['name']}' and prints bank code {coil_test['bank_code']} (retained runtime evidence)."
			source_refs = [MANUAL_SOURCE, RUNTIME_SOURCE, *source_refs]
		if part and number not in FLASH_OUTPUTS and part != "K1":
			physical["part_number"] = part
	if number in FLASH_OUTPUTS:
		total = FLASH_TOTALS[number]
		backbox = FLASH_BACKBOX.get(number, 0)
		physical["quantity"] = total
		physical["location"] = "playfield and backbox" if backbox else "playfield"
		physical["notes"] += (
			f" Bulbs: {DRIVER_ROWS[number][3]}, {total} in all. The coil location page's backbox inset assigns {backbox} of them to the backbox"
			f"{'' if backbox else ' (none)'}, leaving {total - backbox} on the playfield, where the drawing places this output's callout"
			f"{'s' if number in (14, 15) else ''}. The retained table drives {len(RAW_FLASH_POINTS[number])} playfield light object"
			f"{'s' if len(RAW_FLASH_POINTS[number]) != 1 else ''} ({', '.join(name for name, _, _ in RAW_FLASH_POINTS[number])}); they are presentation consumers, not a socket survey."
		)
	if number == 10:
		physical["notes"] += " K1 on the power driver board selects which branch of each shared L/R driver (1-8 / 25-32) is powered. sxx.muxSol = 10 makes PinMAME publish the R side at 25-32; Coil Auto pulses 10 before each of 25-32."
	if number == 11:
		physical["notes"] += " The relay on the power supply board switches the general illumination; the retained script turns its GI collection off while this output is on (SolGIUpdate)."
	if number == 16:
		physical["notes"] += " The Laserkick coil is the left-outlane kickback; the retained script fires its KickBack plunger (SolKickback)."
	if 17 <= number <= 22:
		printed = SPECIAL_PUBLIC_TO_PRINTED[number]
		device, transistor, control, control_pin, trigger, trigger_pin = SPECIAL_PRINTED[printed]
		physical["notes"] += (
			f" Pinned s11.c PIA comments identify handlers 0-5 as printed SP6, SP5, SP2, SP3, SP1, SP4; setSSSol applies the Data East permutation "
			f"{SPECIAL_DE_PERMUTATION}, so printed SP{printed} ({transistor}, control {control_pin}, trigger {trigger_pin}) publishes at {number}."
		)
		if printed != 6:
			physical["part_number"] = "23-800"
			physical["quantity"] = 1
			physical["notes"] += (
				f" The trigger wire closes from switch {SPECIAL_SWITCHES[printed]}, so the coil fires from that switch through the CPU's special-solenoid circuit. "
				"INITGAMES11 leaves sxx.ssSw empty, so PinMAME does not model the switch-driven firing and does not publish this address in play or in "
				"Coil Auto; the address mapping is derived from wiring and source, not observed. The retained script binds no callback here and fires "
				"the bumper or slingshot from the table's own physics."
			)
			status = "candidate"
		else:
			physical["notes"] += (
				" The manual prints SP6 NOT USED with no coil, so no physical load is fitted. Pinned PinMAME never drove it in the retained runs, "
				"but it can still publish this PIA-controlled public state; address availability therefore stays unknown until traced."
			)
		source_refs = [MANUAL_SOURCE, CORE_SOURCE]
	if number in (31, 32):
		physical["notes"] += (
			" No load is fitted: the schematic prints no R branch on this driver. Coil Auto pulses it after K1 and prints NONE, but PinMAME "
			f"publishes this address from the same {DRIVER_ROWS[number][1]} state bit as the fitted L{number - 24:02d} flasher whenever K1 is "
			"energized, so public-address availability stays unknown until traced."
		)
	if number == 24:
		physical["notes"] += " Pinned System 11 exposes this public address but nothing drives it on this machine."
	if 33 <= number <= 44:
		physical["notes"] += " Pinned System 11 exposes this public address but this Data East driver does not populate it."
		source_refs = [CORE_SOURCE]
	if 45 <= number <= 48:
		physical["notes"] += (
			" Synthetic PinMAME lower-flipper power/hold state; there is no separate physical driver at this public address."
			f" core_updateSw sets it while the switched-solenoid enable is on and the {'right' if number in (45, 46) else 'left'} cabinet button bit of PinMAME's flipper column is set: public {82 if number in (45, 46) else 84}, the same bit it copies into matrix switch {16 if number in (45, 46) else 15}."
			" Each physical flipper is one dual-winding 22-900 coil on the solid-state flipper board."
		)
		source_refs = [CORE_SOURCE, MANUAL_SOURCE, SCRIPT_SOURCE]
	if number == 49:
		physical["notes"] += " System 11 simulation-only shooter address; the physical machine uses a manual plunger."
		source_refs = [CORE_SOURCE]
	if number == 50:
		physical["notes"] += " Reserved public address with no meaningful machine state."
		source_refs = [CORE_SOURCE]
	if number == 24:
		source_refs = [CORE_SOURCE]
	if not (unused or unknown) and "quantity" not in physical and number not in {10, 11, 45, 46, 47, 48}:
		physical["quantity"] = 1
	result: dict[str, object] = {
		"id": device_id, "label": label, "kind": kind, "binding": {"group": "pinmame.output.solenoid", "device": number},
		"aliases": aliases("pinmame.solenoid", number, manual_number), "availability": "unknown" if unknown else ("unused" if unused else "used"),
		"physical": physical, "provenance": provenance(status, *source_refs),
	}
	if number in DRIVER_ROWS:
		result["wiring"] = {"board": "CPU Board / PPB", "driver_transistor": DRIVER_ROWS[number][1], "drive_wire": DRIVER_ROWS[number][2]}
	elif 17 <= number <= 22:
		printed = SPECIAL_PUBLIC_TO_PRINTED[number]
		result["wiring"] = {"board": "CPU Board", "driver_transistor": SPECIAL_PRINTED[printed][1]}
		if SPECIAL_PRINTED[printed][2]:
			result["wiring"]["drive_wire"] = SPECIAL_PRINTED[printed][2]
	if unused or unknown:
		result["spatial"] = not_applicable("virtual", "validated", *source_refs)
	elif number in RAW_FLASH_POINTS:
		result["spatial"] = located(device_id, [(x, y) for _, x, y in RAW_FLASH_POINTS[number]], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 10:
		result["spatial"] = not_applicable("internal_nonvisual", "validated", CORE_SOURCE, MANUAL_SOURCE)
	elif number == 11:
		physical["notes"] += f" The {len(RAW_GI_POINTS)} GI-collection lights placed here are visual consumers, not a survey of the physical G.I. sockets."
		result["spatial"] = located(device_id, [(x, y) for _, x, y in RAW_GI_POINTS], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE)
	elif number in COIL_EFFECT_POINTS:
		result["spatial"] = located(device_id, [COIL_EFFECT_POINTS[number][1]], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number in (45, 46, 47, 48):
		result["spatial"] = not_applicable("virtual", "validated", CORE_SOURCE)
	return result


def displays() -> list[dict[str, object]]:
	labels = ["Player 1/2 alphanumeric row", "Player 3/4 alphanumeric row"]
	return [{
		"id": f"display.segment-{index}", "label": label, "kind": "segment", "controller_index": index, "segment_start": 20 * index, "width": 16,
		"spatial": not_applicable("cabinet_or_service", "validated", CORE_SOURCE, MANUAL_SOURCE), "provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
	} for index, label in enumerate(labels)]


def mechanisms() -> list[dict[str, object]]:
	m, s, r = MANUAL_SOURCE, SCRIPT_SOURCE, RUNTIME_SOURCE
	return [
		{"id": "mechanism.outhole", "label": "Outhole kicker", "kind": "kicker", "actuators": ["coil.driver-25"], "sensors": ["switch.matrix-10"], "behavior": "A drained ball rests on the outhole switch 10; output 25 (R01) kicks it into the trough. The manual lists Outhole Kicker Assy. 500-5082-00 and a 23-840 coil; the ROM's Coil Auto names 25 OUTHOLE.", "assembly_part_number": "500-5082-00", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.ball-trough", "label": "Three-ball trough and eject", "kind": "other", "actuators": ["coil.driver-26"], "sensors": ["switch.matrix-11", "switch.matrix-12", "switch.matrix-13"], "behavior": "Three balls rest on Trough #1-#3. Output 26 (R02, 23-840, which the ROM's Coil Auto names SHOOTER LANE) ejects one into the shooter lane, where switch 14 sees it before the manual plunger launches it. The retained script's cvpmBallStack orders the switches 13, 12, 11 from the eject end; the manual does not draw their order.", "assembly_part_number": "500-5012-00", "positions": [{"id": "trough.position-1", "label": "Eject position", "sensors": ["switch.matrix-13"]}, {"id": "trough.position-2", "label": "Middle position", "sensors": ["switch.matrix-12"]}, {"id": "trough.position-3", "label": "Rear position", "sensors": ["switch.matrix-11"]}], "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.left-eject", "label": "Upper-left eject saucer", "kind": "kicker", "actuators": ["coil.driver-27"], "sensors": ["switch.matrix-28"], "behavior": "A saucer at the upper left holds the ball on switch 28; output 27 (R03, 27-1300) kicks it out. One of three Playfield Eject Assy. 500-5051-02.", "assembly_part_number": "500-5051-02", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.top-eject", "label": "Top eject saucer", "kind": "kicker", "actuators": ["coil.driver-28"], "sensors": ["switch.matrix-29"], "behavior": "A saucer at the top center holds the ball on switch 29; output 28 (R04, 27-1300, Ball Guide Eject) kicks it out.", "assembly_part_number": "500-5051-02", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.right-eject", "label": "Right eject saucer (Scanner)", "kind": "kicker", "actuators": ["coil.driver-29"], "sensors": ["switch.matrix-30"], "behavior": "A saucer at the top right holds the ball on switch 30; output 29 (R05, 27-1300) kicks it out past the Right Eject Ball Guide. The rules award the Scanner value and a ROBOCOP letter per shot (lamps 17-18 and 25-29).", "assembly_part_number": "500-5051-02", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.vertical-up-kicker", "label": "Vertical Up Kicker", "kind": "kicker", "actuators": ["coil.driver-30"], "sensors": ["switch.matrix-45"], "behavior": "A ball entering the left kicker hole rests on switch 45; output 30 (R06, 23-800) kicks it vertically onto the VUK Left Flip. Feed Ramp (535-5355-00), which returns it to the left flipper.", "assembly_part_number": "500-5067-00", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.laser-kick", "label": "Left-outlane Laser Kick", "kind": "kicker", "actuators": ["coil.driver-16"], "sensors": ["switch.matrix-17"], "behavior": "A kickback at the foot of the left outlane. Switch 17 reports the ball in the lane; when lit (lamp 20 Relite Laser Kick, lamp 45 Laser Kick Outlane) the ROM fires output 16 (23-800 through Q5 TIP36C) to return the ball to play.", "assembly_part_number": "500-5080-00", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.left-flipper", "label": "Lower-left flipper", "kind": "other", "actuators": ["coil.driver-47", "coil.driver-48"], "sensors": ["switch.matrix-15"], "behavior": "One 22-900 dual-winding coil on the solid-state flipper board moves the left flipper. FLIP1516 makes core_updateSw copy the left cabinet button, public 84, into switch 15 and fabricate 47/48.", "assembly_part_number": "500-5177-02", "provenance": provenance("validated", m, CORE_SOURCE, r)},
		{"id": "mechanism.right-flipper", "label": "Lower-right flipper", "kind": "other", "actuators": ["coil.driver-45", "coil.driver-46"], "sensors": ["switch.matrix-16"], "behavior": "One 22-900 dual-winding coil on the solid-state flipper board moves the right flipper. FLIP1516 makes core_updateSw copy the right cabinet button, public 82, into switch 16 and fabricate 45/46.", "assembly_part_number": "500-5177-01", "provenance": provenance("validated", m, CORE_SOURCE, r)},
		{"id": "mechanism.left-slingshot", "label": "Left slingshot", "kind": "other", "actuators": ["coil.driver-18"], "sensors": ["switch.matrix-21"], "behavior": "Trigger and point switches at 21 close the SP3 trigger wire, firing the left slingshot coil through the CPU's special-solenoid circuit. Pinned PinMAME publishes SP3 at 18 but never drives it for this driver.", "assembly_part_number": "500-5077-00", "provenance": provenance("candidate", m, CORE_SOURCE, s)},
		{"id": "mechanism.right-slingshot", "label": "Right slingshot", "kind": "other", "actuators": ["coil.driver-21"], "sensors": ["switch.matrix-22"], "behavior": "Trigger and point switches at 22 close the SP5 trigger wire, firing the right slingshot coil. Pinned PinMAME publishes SP5 at 21 but never drives it for this driver.", "assembly_part_number": "500-5077-00", "provenance": provenance("candidate", m, CORE_SOURCE, s)},
		{"id": "mechanism.left-turbo-bumper", "label": "Left turbo bumper", "kind": "other", "actuators": ["coil.driver-19"], "sensors": ["switch.matrix-46"], "behavior": "Switch 46 closes the SP4 trigger wire, firing the left turbo bumper coil. PinMAME publishes SP4 at 19 but never drives it for this driver.", "assembly_part_number": "500-5034-10", "provenance": provenance("candidate", m, CORE_SOURCE, s)},
		{"id": "mechanism.center-turbo-bumper", "label": "Center turbo bumper", "kind": "other", "actuators": ["coil.driver-22"], "sensors": ["switch.matrix-47"], "behavior": "Switch 47 closes the SP2 trigger wire, firing the center turbo bumper coil. PinMAME publishes SP2 at 22 but never drives it for this driver.", "assembly_part_number": "500-5034-10", "provenance": provenance("candidate", m, CORE_SOURCE, s)},
		{"id": "mechanism.right-turbo-bumper", "label": "Right turbo bumper", "kind": "other", "actuators": ["coil.driver-17"], "sensors": ["switch.matrix-48"], "behavior": "Switch 48 closes the SP1 trigger wire, firing the right turbo bumper coil. PinMAME publishes SP1 at 17 but never drives it for this driver.", "assembly_part_number": "500-5034-10", "provenance": provenance("candidate", m, CORE_SOURCE, s)},
		{"id": "mechanism.green-standups", "label": "Left four-bank green standup targets", "kind": "other", "actuators": [], "sensors": ["switch.matrix-33", "switch.matrix-34", "switch.matrix-35", "switch.matrix-36"], "behavior": "Four fixed standup targets, Green Target 1 (left) to 4 (right), each with its own switch and lamp (4 down to 1). The parts list prints 4 Bank S.U. Tgt. Assy. 515-5211-14; there is no reset coil.", "assembly_part_number": "515-5211-14", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.yellow-standups", "label": "Center three-bank yellow standup targets", "kind": "other", "actuators": [], "sensors": ["switch.matrix-41", "switch.matrix-42", "switch.matrix-43"], "behavior": "Three fixed standup targets, Yellow Target 1 (left) to 3 (right), each with a switch and lamp 9-11. The parts list prints 3 Bank S.U. Tgt. Assy 500-5103-16; there is no reset coil.", "assembly_part_number": "500-5103-16", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.ten-point-switches", "label": "Two 10-point standup switches", "kind": "other", "actuators": [], "sensors": ["switch.matrix-37", "switch.matrix-38"], "behavior": "Two fixed 10 Point S.U. Switches (500-5069-00), top and bottom. The retained table has no object for either, so their positions are not established.", "assembly_part_number": "500-5069-00", "provenance": provenance("validated", m, r)},
		{"id": "mechanism.trap-ball", "label": "Right trap ball", "kind": "other", "actuators": [], "sensors": ["switch.matrix-23"], "behavior": "The manual records the trap ball only through switch 23 Right Trap Ball (500-5035-02) and lamps 19 Trap Ball Top and 22 Red Trap Ball; its parts list prints no assembly for it. The retained table builds it as a captive ball (CapBall1) in the right lane below a target that reports switch 23, matching the drawn positions of lamps 22 (low) and 19 (top). The physical construction is not documented by a retained source.", "provenance": provenance("candidate", m, s, TABLE_SOURCE)},
		{"id": "mechanism.manual-shooter", "label": "Manual plunger and shooter lane", "kind": "other", "actuators": [], "sensors": ["switch.matrix-14"], "behavior": "The player launches the ball with the ball-shooter assembly (500-5019-04); switch 14 reports a ball in the shooter lane. The ROM's 100K top lane award is for a plunge through a flashing ball guide.", "provenance": provenance("validated", m, r, s)},
		{"id": "mechanism.fixed-routes", "label": "Lanes, ramps and spinner", "kind": "other", "actuators": [], "sensors": ["switch.matrix-18", "switch.matrix-19", "switch.matrix-20", "switch.matrix-25", "switch.matrix-26", "switch.matrix-27", "switch.matrix-31", "switch.matrix-32", "switch.matrix-44"], "behavior": "Passive paths: the left and right return lanes, the right outlane, the 2-0-9 top lanes, the Left Catch Ramp and Right Ramp with a ramp switch each (Ramp Sw. Act. Wire 535-5361-00), and the spinning target 515-5236-00 whose Spin. Sw. Actuator Wire (535-5319-00) works switch 44. No motor, diverter or magnet is fitted.", "provenance": provenance("validated", m, r, s)},
	]


def build_runtime_evidence_text() -> str:
	return (ROOT / RUNTIME_EVIDENCE_PATH).read_text(encoding="utf-8")


def sources() -> list[dict[str, object]]:
	excerpt_meta = [{
		"id": "excerpt.robocop." + path.stem, "path": path.as_posix(), "sha256": sha256_text(content), "method": "manual", "reviewed": True,
		"locator": EXCERPT_LOCATORS[path.name], "transcribed_by": "curator, read from Poppler renders; the PDF text layer located pages and gave a second reading",
	} for path, content in EXCERPTS.items() if path.name in EXCERPT_LOCATORS]
	vpm_path = EXCERPT_DIR / "vpm-script-library-flippers.md"
	return [
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "license": "BSD-3-Clause", "locator": "src/wpc/driver.c lines 482-484 list robo_a29, robo_a30 and robo_a34; src/wpc/degames.c line 279 CORE_GAMEDEF(robo,a34,...) is the root and lines 287 and 295 CORE_CLONEDEF robo_a29 and robo_a30 of it."},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "license": "BSD-3-Clause", "locator": "src/wpc/degames.c lines 77-80 define INITGAMES11 as {gen, disptype, {flippers,0,0,0,sb,db,gs1}, NULL, {{0}}, {10}}, so line 271 INITGAMES11(robo, GEN_DE, de_dispAlpha3, FLIP1516, SNDBRD_DE1S, S11_LOWALPHA, 0) sets hw.display = S11_LOWALPHA, leaves wpc.invSw zero and sxx.ssSw empty, and sets sxx.muxSol = 10; lines 88 and 102-104 define FLIP1516 = FLIP_SWNO(15,16) and two 16-character alphanumeric rows; robo_a29, robo_a30 and robo_a34 share that block and its sound ROMs (lines 272-295). src/wpc/s11.c lines 537-539 apply the Data East special-solenoid permutation {3,4,5,1,0,2}, lines 579 and 618-623 bind PIA handlers 0-5 to setSSSol, and the PIA board comments name those handlers SP6, SP5, SP2, SP3, SP1 and SP4; src/wpc/core.c core_updateSw (lines 1808-1843) copies the cabinet flipper-button bits 82/84 into the FLIP_SWNO switches and fabricates 45-48."},
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://www.ipdb.org/files/1976/Data_East_1989_Robocop_English_Manual.pdf", "sha256": MANUAL_SHA256, "acquired_at": "2026-10-30T13:55:46Z", "locator": f"IPDB machine 1976 (Robocop, Data East, 1989); retained at external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb/{MANUAL_FILENAME}. 54 pages; 64,987,666 bytes; scanned with a noisy OCR text layer. Pages 24-29 (printed 20-25) carry the switch matrix, switch part list, lamp matrix, lamp list and location drawing, special-solenoid and flipper tables, coil location drawing with its backbox inset, coil part chart and coil schematic; page 31 (printed 27) the playfield top parts list. Every mapping cell was read from Poppler renders.", "license": "NOASSERTION", "attribution": "Data East Pinball; scan hosted by the Internet Pinball Database", "original_filename": MANUAL_FILENAME, "rights": "NOASSERTION", "excerpts": excerpt_meta},
		{"id": TABLE_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/data-east/robocop-1989/{TABLE_FILENAME}", "sha256": TABLE_SHA256, "revision": "drakkon mod 1.2", "known_working": True, "source_id": "retained-robocop-drakkon-mod-1.2", "original_filename": TABLE_FILENAME, "license": "Community table; redistribution terms not supplied", "attribution": "Credited RoboCop table contributors (drakkon mod 1.2)", "locator": "vpxtool git:v0.33.3; 1555 files under gameitems/; exact asserted bounds (0,0)-(952,2256)"},
		{"id": SCRIPT_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/data-east/robocop-1989/vpxtool-extract/script.vbs", "sha256": SCRIPT_SHA256, "revision": "script from retained drakkon mod 1.2", "license": "Community script; redistribution terms not supplied", "attribution": "Credited table-script contributors", "locator": "Line 102 LoadVPM \"01560000\", \"DE.VBS\", 3.46; line 106 cGameName = robo_a34; lines 166-189 the trough, three saucers and VUK ball stacks; lines 317-337 SolCallback 1-16 and 25-30; lines 645-680 bumper handlers (Bumper3 pulses 46); lines 691-800 lane, ramp, spinner and target handlers; Set Lights binds 1-55 and 57-64 with 44 to L24a and 52-55 to Light44/46/48/50."},
		{"id": EXTRACTION_SOURCE, "kind": "vpx_table", "uri": MANIFEST_PATH.as_posix(), "sha256": MANIFEST_CONTENT_SHA256, "revision": "vpxtool git:v0.33.3", "locator": f"2064 files; 94583062 bytes; algorithm: {MANIFEST_ALGORITHM}; canonical manifest SHA-256 {MANIFEST_SHA256}; 1555 files under gameitems/"},
		{"id": RENDER_SOURCE, "kind": "human_review", "uri": f"external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb/{MANUAL_FILENAME}", "locator": "54-page contact sheet; PDF pages 24-29 rendered at 300 dpi and the coil schematic and location pages at 600 dpi, page 31 at 200 dpi, with Poppler pdftoppm 23.05.0 on 2026-10-30. Rendered cells governed every mapping."},
		{
			"id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI, "original_filename": "de.vbs", "sha256": VPM_DE_SHA256,
			"acquired_at": "2026-09-25T23:32:01Z",
			"locator": f"The VPinMAME script library the retained table loads at runtime (script.vbs line 102 LoadVPM \"01560000\", \"DE.VBS\", 3.46; DE.VBS executes core.vbs), retained from the contributor's working installation together with core.vbs (SHA-256 {VPM_CORE_SHA256}). DE.VBS defines swLRFlip = 82 and swLLFlip = 84 and sets them from the flipper keys in vpmKeyDown/vpmKeyUp, and names the staged upper flipper keys swURFlip/swULFlip at 86 and 88.",
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [{"id": "excerpt.robocop.vpm-script-library-flippers", "locator": "de.vbs lines 33-36, 62-73 and 94-105; script.vbs lines 102, 135, 259-261, 286, 290-293 and 309", "path": vpm_path.as_posix(), "sha256": sha256_text(EXCERPTS[vpm_path]), "method": "manual", "transcribed_by": "curator, read from the library and script files", "reviewed": True}],
		},
		{"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": RUNTIME_EVIDENCE_PATH.as_posix(), "revision": PINMAME_REVISION, "sha256": sha256_text(build_runtime_evidence_text()), "locator": "Two successful isolated LibPinMAME runs, robo_a34 and robo_a30, of tools/harness-scenarios/data-east/robo-a34-service-walk.json walk the ROM's Switch Test (host closes every matrix address and holds both flipper keys), Lamp Test (Start steps lamps 1-64) and Coil Auto (one full cycle 1-16 then 10 before each of 25-32). The compact evidence keeps, per address, the Player 1/2 name frame and the Player 3/4 wire-code or bank-code frame; both ROMs print identical names. Built by tools/build_robocop_runtime_evidence.py from the external runs.", "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external."},
	]


def build_machine() -> dict[str, object]:
	inputs = diagnostic_inputs() + [switch_input(number) for number in range(1, 65)] + flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP1516 = FLIP_SWNO(15,16)",
		core_refs=(CORE_SOURCE,), button_refs=(SCRIPT_SOURCE, VPM_DE_LIBRARY_SOURCE, RUNTIME_SOURCE),
		button_notes={
			side: (
				f"The retained known-working script drives it: table1_KeyDown/table1_KeyUp (script lines 259-309) hand the {side} "
				f"flipper key to DE.VBS vpmKeyDown/vpmKeyUp, which set Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} (excerpt vpm-script-library-flippers). In the retained robo_a34 and robo_a30 "
				f"Switch Test the held {side} flipper key makes the ROM print {'LEFT' if side == 'left' else 'RIGHT'} FLIPPER at switch "
				f"{15 if side == 'left' else 16}. The physical counterpart is the {side} cabinet flipper button (180-5048-01)."
			)
			for side in ("left", "right")
		},
		unused_notes=vpm_staged_flipper_notes(library="DE.VBS"),
		unused_note_refs=(VPM_DE_LIBRARY_SOURCE,),
	)
	outputs = [solenoid_output(number) for number in range(1, 51)] + [lamp_output(number) for number in range(1, 65)]
	drivers = [
		{"id": "robo_a34", "description": "Robocop (3.4)", "year": "1989", "manufacturer": "Data East", "flags": 0, "physical_compatibility": "identical", "variant_notes": "The root driver. The retained table and the primary service walk run it."},
		{"id": "robo_a30", "clone_of": "robo_a34", "description": "Robocop (3.0)", "year": "1989", "manufacturer": "Data East", "flags": 0, "physical_compatibility": "identical", "variant_notes": "Earlier CPU ROM revision on the same INITGAMES11 hardware block and sound ROMs. Its Switch Test, Lamp Test and Coil Auto print the same names in the same order as robo_a34 in the retained runs."},
		{"id": "robo_a29", "clone_of": "robo_a34", "description": "Robocop (2.9)", "year": "1989", "manufacturer": "Data East", "flags": 0, "physical_compatibility": "identical", "variant_notes": "Earliest CPU ROM revision on the same INITGAMES11 hardware block and sound ROMs. The authorized ROM library does not hold it, so it was not run; nothing in pinned source distinguishes its hardware."},
	]
	return {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Robocop", "manufacturer": "Data East", "year": 1989, "kind": "physical_pinball", "ipdb_id": 1976, "opdb_id": "Grlxe-MJ916", "playfield": {"width": RIGHT, "height": BOTTOM, "units": "vpx", "provenance": provenance("validated", TABLE_SOURCE)}},
		"coverage": {"status": "partial", "missing": ["output_semantics", "mechanism_behavior", "polarity", "spatial_placement"], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "candidate", "variant_coverage": "validated", "recreation_knowledge": "candidate", "spatial_placement": "candidate"}},
		"controller": {"platform": "pinmame.dataeast", "hardware_generation": "0x1000", "inversion_applied_by_emulator": True},
		"drivers": drivers,
		"inputs": inputs, "outputs": outputs, "displays": displays(), "mechanisms": mechanisms(),
		"relationships": [{"id": f"relationship.lr-relay-{number}", "kind": "relay_gated", "source": "coil.driver-10", "destination": f"coil.driver-{number}", "provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE)} for number in range(25, 31)] + flipper_column_relationships(
			flip_swno=FLIP_SWNO, matrix_ids={15: "switch.matrix-15", 16: "switch.matrix-16"}, refs=(CORE_SOURCE,),
		),
		"sources": sources(), "knowledge": {"path": KNOWLEDGE_PATH.as_posix(), "status": "partial"}, "conflicts": [],
	}


def build_spatial(machine: dict[str, object]) -> dict[str, object]:
	resolved = []
	for device in machine["inputs"] + machine["outputs"] + machine["displays"]:
		spatial = device.get("spatial")
		if isinstance(spatial, dict) and spatial.get("status") != "not_applicable":
			resolved.append({"id": device["id"], "status": spatial["status"], "placements": len(spatial["placements"])})
	placed_lamps = [f"lamp.matrix-{number}" for number in range(1, 65) if number not in BACK_PANEL_LAMPS | {56}]
	unplaced = [f"switch.matrix-{number}" for number in (11, 12, 13, 37, 38)] + [f"lamp.matrix-{number}" for number in sorted(BACK_PANEL_LAMPS)]
	return {
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
		"coordinate_system": {"space": "playfield", "x": "0 left, 1 right", "y": "0 rear/backglass, 1 front/apron", "normalization": "x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top)", "raw_bounds": {"left": 0.0, "top": 0.0, "right": RIGHT, "bottom": BOTTOM}},
		"evidence": {"manual_sha256": MANUAL_SHA256, "table_sha256": TABLE_SHA256, "script_sha256": SCRIPT_SHA256, "extraction_manifest_algorithm": MANIFEST_ALGORITHM, "extraction_manifest_sha256": MANIFEST_SHA256},
		"method": [
			"Asserted both exact gamedata.json bounds (0,0)-(952,2256) before normalization; no other machine's geometry is reused.",
			"Read every switch, lamp and coil table cell from rendered manual pages; the noisy PDF text layer only located pages.",
			"Took sensor placements from the script-bound objects (triggers, targets, saucers, bumpers, spinner, slingshot walls) and lamp and flash placements from the objects the script binds to each address.",
			"Compared the coil location drawing's callouts with the table's flash objects: every flash output's callout falls in the same playfield region as its bound objects, and every R-side kicker callout at its saucer or kicker.",
			"Used the coil location page's backbox inset and the lamp location drawing's back-panel row for physical-plane classification only; neither drawing has a registered frame.",
		],
		"excluded_helpers": {
			"back-panel-lamps": "L41-L43 and Flashers F41-F43 sit in the apron area of the table, but the manual draws lamps 41-43 on the back panel at the rear of the playfield; the apron objects are presentation proxies and give those lamps no coordinate.",
			"gi-lamp-overlap": "Light44, Light46, Light48 and Light50 belong to the GI collection and are also bound to lamps 52-55; they are placed only as lamps.",
			"gi-and-flash-proxies": "The GI collection and the grouped F* flash lights are visual effects, not surveys of physical bulb sockets.",
			"synthetic-flipper-states": "Public outputs 45-48 are PinMAME-generated winding states of the two physical flippers and carry no placement.",
		},
		"projection_classes": [
			{"class": "script-bound-light-candidate", "devices": placed_lamps, "status": "candidate", "reason": "The script's Set Lights binding proves which object consumes each address; light centers are not socket surveys."},
			{"class": "mechanical-effect-object", "devices": [f"coil.driver-{number}" for number in sorted(COIL_EFFECT_POINTS)], "status": "candidate", "reason": "Kicker, saucer, bumper and slingshot objects give the effect location, not the under-playfield coil center."},
		],
		"resolved": sorted(resolved, key=lambda row: row["id"]),
		"unresolved": [
			{"dimension": "unplaced_devices", "devices": unplaced, "reason": "The table models the trough as a ball stack with no geometry and has no object for the two 10-point switches; the manual draws back-panel lamps 41-43 above the playfield outline without a registered frame, and the table's apron objects for them are proxies."},
			{"dimension": "flasher_socket_binding", "devices": [f"coil.driver-{number}" for number in FLASH_OUTPUTS], "reason": "The manual fixes each flash output's backbox/playfield bulb split and its playfield region, but not its socket centers."},
		],
		"blockers": [
			{"dimension": "output_semantics", "devices": [f"coil.driver-{number}" for number in (17, 18, 19, 20, 21, 22, 31, 32)], "reason": "The special-solenoid addresses are derived from the manual's SP wiring and pinned s11.c, but PinMAME never publishes them for this driver (sxx.ssSw is empty), so no runtime evidence confirms the mapping; unfitted SP6 (20) and mux branches R07/R08 (31, 32) can still carry public state nothing explains.", "would_resolve": "Static analysis of the ROM's PIA special-line writes, or a gameplay trace of 20, 31 and 32 alongside the bumper and slingshot switches."},
			{"dimension": "mechanism_behavior", "devices": ["mechanism.trap-ball", "mechanism.left-slingshot", "mechanism.right-slingshot", "mechanism.left-turbo-bumper", "mechanism.center-turbo-bumper", "mechanism.right-turbo-bumper"], "reason": "The trap-ball construction is documented only by a switch and two lamp names, and the switch-to-coil firing of the slingshots and turbo bumpers is wiring-derived and runtime-unobservable.", "would_resolve": "A photograph of an original playfield's right trap-ball lane, and the special-solenoid evidence above."},
			{"dimension": "polarity", "devices": ["switch.diagnostic-6"], "reason": "The Green Forward/Reverse service button toggles the ROM's direction on each press, but no retained source settles its contact construction or the level PinMAME publishes for it.", "would_resolve": "A coin-door wiring page or a harness trace of the published -6 level across a direction change."},
			{"dimension": "spatial_placement", "devices": placed_lamps + [f"coil.driver-{number}" for number in FLASH_OUTPUTS] + ["coil.driver-11", "switch.matrix-48"] + unplaced, "reason": "Lamp, flash, GI and coil coordinates are retained-table candidates; three trough switches, both 10-point switches and the three back-panel lamps have no placement.", "would_resolve": "A drawing callout check against a registered playfield drawing or photograph, and positions for the trough and 10-point switches."},
		],
		"conflicts": [],
		"promotion_decision": "Keep partial. Every public address is named and wired from the manual and confirmed by the ROM's own tests on two revisions, but the special-solenoid mapping is unobservable, the trap-ball construction is undocumented, one service-button polarity is open, and placements are candidates.",
	}


def spatial_markdown(report: dict[str, object]) -> str:
	rows = [
		"# RoboCop spatial-resolution report", "",
		"Exact retained-table bounds: `left=0`, `top=0`, `right=952`, `bottom=2256`.", "",
		"## Extraction identity", "",
		f"- Manifest algorithm: {report['evidence']['extraction_manifest_algorithm']}",
		f"- Manifest SHA-256: `{report['evidence']['extraction_manifest_sha256']}`", "",
		"## Promotion decision", "", report["promotion_decision"], "", "## Blockers", "",
	]
	for blocker in report["blockers"]:
		rows.extend([f"### {blocker['dimension']}", "", blocker["reason"], "", f"Would resolve: {blocker['would_resolve']}", "", "Devices: " + ", ".join(f"`{device}`" for device in blocker["devices"]), ""])
	rows.extend(["## Unresolved", ""] + [f"- `{item['dimension']}`: {item['reason']}" for item in report["unresolved"]] + [""])
	rows.extend(["## Resolver controls", ""] + [f"- {method}" for method in report["method"]] + ["", "## Excluded helpers", ""] + [f"- `{key}`: {value}" for key, value in report["excluded_helpers"].items()] + [""])
	return "\n".join(rows)


def knowledge_markdown(machine: dict[str, object]) -> str:
	missing = ", ".join(f"`{value}`" for value in machine["coverage"]["missing"])
	return f"""# Data East RoboCop (1989)

Machine definition: `{MACHINE_PATH.as_posix()}`

## Identity and drivers

Pinned PinMAME publishes three drivers for the one physical machine: root `robo_a34` (3.4) and clones `robo_a30` (3.0) and `robo_a29` (2.9). All three share one `INITGAMES11` block and the same sound ROMs, so they run identical hardware. The ROM library holds `robo_a34` and `robo_a30`; both were walked through the ROM's own service tests and print the same names in the same order. `robo_a29` is not held and was not run.

`INITGAMES11(robo, GEN_DE, de_dispAlpha3, FLIP1516, SNDBRD_DE1S, S11_LOWALPHA, 0)` sets generation `GEN_DE` (`0x1000`), two 16-character alphanumeric rows, `hw.flippers = FLIP1516`, `hw.display = S11_LOWALPHA`, no `gameSpecific1` flags (so no `S11_MUXDELAY`), an empty special-solenoid switch table and `sxx.muxSol = 10`.

## Controller contract

- Inputs: service buttons -7 (Black, Step) and -6 (Green, Forward/Reverse), jumper W7 at DIP 0, matrix 1-64 and PinMAME's flipper column 81-88.
- Outputs: lamps 1-64 and public solenoids 1-50.
- Solenoid 10 is the A/B relay K1. The eight L/R pairs share a driver: L01-L08 publish at 1-8 and R01-R08 at 25-32. Only R01-R06 carry coils. 31 and 32 have no branch, but PinMAME publishes them from the same driver bits as the fitted L07 and L08 flashers whenever K1 is energized, so their availability stays `unknown`.
- Solenoid 11 is the G.I. relay; 23 is Game On; 24 and 33-44 are unused; 45-48 are synthetic flipper winding states; 49 is a simulation shooter; 50 is reserved.
- Public 17-22 are the six switch-triggered special solenoids. Pinned `s11.c` permutes the PIA handlers so printed SP1 Right Turbo Bumper lands at 17, SP3 Left Slingshot at 18, SP4 Left Turbo Bumper at 19, unfitted SP6 at 20 (availability `unknown`, since it is PIA state PinMAME could still publish), SP5 Right Slingshot at 21 and SP2 Center Turbo Bumper at 22. `sxx.ssSw` is empty, so PinMAME never publishes these addresses for this driver: a recreation fires the bumpers and slingshots from its own switch events.

Every matrix switch rests open. The ROM's Active Switch test reads NONE with all public switches at 0 and names each switch as it closes, so `normally_closed` is false throughout.

FLIP1516 makes `core_updateSw` copy the cabinet buttons into 15 and 16 on every update: left button 84 into 15, right button 82 into 16, fabricating 47/48 and 45/46 from them. **A recreation drives 82/84, never 15/16.** The ROM's Switch Test names the held left flipper key LEFT FLIPPER at 15 and the right RIGHT FLIPPER at 16. The manual prints the flippers' Instant Info and EOS contacts there; PinMAME models no EOS on this platform, so the label follows what a consumer receives.

## Names

The manual's matrix, its part list, the ROM's own tests and the coil schematic name a few devices differently. Each set denotes one device, so none is a conflict:

- Switch 17: matrix and ROM Laser Kick, part list Left Outlane — the left-outlane rollover in front of the kickback.
- Switch 28 / coil 27: matrix Left Eject, ROM MID EJECT, schematic Middle Eject — the upper-left saucer (location drawing R03).
- Switch 29 / coil 28: matrix Center Eject, list and ROM Top Eject, schematic Ball Guide Eject — the top saucer (R04).
- Coil 26: schematic Trough, ROM SHOOTER LANE — the trough eject into the shooter lane.

## Wiring

The ROM's Switch Test and Lamp Test print each address's wire code on the Player 3/4 row. Every code matches the manual's matrix headers: switches return 91-98 and drive 51, 52, 53, 54, 50, 56, 57, 58 by column; lamps return 21, 20, 23-28 and drive 41, 42, 43, 40, 45-48. Coil Auto prints each driver's bank code, L01-L08, 09-16 and R01-R08.

## Flash lamps

The coil location page has a separate `Backbox Flash lamps` inset of nineteen bulbs. Together with the schematic's bulb counts, it gives each flash output's split: 1 has 3 backbox + 1 playfield, 3 has 2 + 1, 4, 5 and 6 have 1 + 1 each, 7 has 3 + 1, 9, 12 and 13 have 2 + 2 each, 14 and 15 have 1 + 3 each, and 2 and 8 are one playfield bulb each. Every output's total matches its schematic row. The playfield callouts agree with the table's flash objects: the L01-L06 ladder up the right center, 09 and 12 in the center, 13 lower right, 14/15 alternating up the right ramp, L07 at the left and L08 at the top left.

The coil part chart lists six 23-800 coils while the schematic draws seven (Vertical Up Kicker, Laser Kick and SP1-SP5). Both readings are kept in the excerpt.

## Lamps

Lamps 41-43 (Back Panel Red, Yellow, Green) are on the back panel at the rear of the playfield. The retained table draws them on the apron; those are presentation proxies, and no source registers the lamps' positions on the panel, so they have no placement yet. The manual's drawing does not show lamps 44, 63 or 64. The parts list's `Red Mini Lamp - ED 209 (2)` fits 63 and 64, ED 209 Left and Right, but that pairing is inferred from the names. Lamp 56 is unused.

## Retained-table defects

These are bugs in the retained table, not facts about the machine:

- Its right turbo bumper (Bumper3) pulses switch 46 instead of 48, so the table never closes 48.
- It has no object for the two 10-point switches 37 and 38.
- Its key handlers write switch 15 from the right flipper key and 16 from the left. PinMAME overwrites both every update, so the writes have no effect; the real flipper input goes through DE.VBS to 82/84.
- It adds Light44, Light46, Light48 and Light50, the objects for lamps 52-55, to its GI collection.

## Mechanisms

- A three-ball trough (500-5012-00) is fed by the outhole kicker (25) and ejects into the shooter lane (26).
- Three Playfield Eject saucers sit at the upper left (switch 28, coil 27), top (29 / 28) and top right (30 / 29). The right one is the Scanner shot.
- The Vertical Up Kicker (45 / 30) lifts the ball onto a feed ramp to the left flipper.
- The Laser Kick (17 / 16) is a left-outlane kickback.
- Three turbo bumpers and two slingshots fire from the special-solenoid circuit.
- There are fixed standups: a green four-bank (33-36), a yellow three-bank (41-43) and two 10-point switches (37, 38).
- The right trap ball (23) is documented only by its switch and two lamp names. The table builds it as a captive ball below a target, but its physical construction is unconfirmed.
- The remaining features are passive: the 2-0-9 top lanes, the Left Catch Ramp and Right Ramp, a spinning target (44) and the return lanes and outlanes. The playfield has no drop targets, diverters, magnets or motors.

## Coverage

Status stays `partial`; `coverage.missing` is [{missing}].

- `output_semantics`: special solenoids 17-22 are wiring-derived and never published, so nothing at runtime confirms them; unfitted 20, 31 and 32 may still carry public state nothing explains.
- `mechanism_behavior`: no retained source documents the trap ball's construction, and the special-solenoid firing is unobservable.
- `polarity`: the Green Forward/Reverse button's contact construction and published level are not settled.
- `spatial_placement`: every placement is a retained-table candidate. The trough switches, the 10-point switches and back-panel lamps 41-43 have none.

## Recreation boundary

Consume PinMAME's decoded outputs, with K1 already applied to 25-30. Drive the flipper buttons at 82/84. Fire the turbo bumpers and slingshots from switch events, because PinMAME will not publish 17-22. Put lamps 41-43 on the back panel at the rear of the playfield, and split each flash output's bulbs between the backbox and the playfield as listed above.
"""


def json_text(value: object) -> str:
	return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def desired_files() -> dict[Path, str]:
	machine = build_machine()
	spatial = build_spatial(machine)
	return {
		MACHINE_PATH: json_text(machine), SEED_PATH: json_text(machine), SPATIAL_JSON_PATH: json_text(spatial),
		SPATIAL_MD_PATH: spatial_markdown(spatial), KNOWLEDGE_PATH: knowledge_markdown(machine), **EXCERPTS,
	}


def compare_lf(path: Path, expected: str) -> bool:
	return path.is_file() and path.read_text(encoding="utf-8").replace("\r\n", "\n") == expected.replace("\r\n", "\n")


def generate() -> None:
	if (ROOT / AUTHOR_READY_PATH).exists():
		raise RuntimeError(f"refusing to overwrite partial artifacts while {AUTHOR_READY_PATH.as_posix()} exists")
	if not (ROOT / RUNTIME_EVIDENCE_PATH).is_file():
		raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH.as_posix()} is missing; build it with tools/build_robocop_runtime_evidence.py")
	if sha256_file(ROOT / MANIFEST_PATH) != MANIFEST_CONTENT_SHA256:
		raise RuntimeError(f"{MANIFEST_PATH.as_posix()} does not match its pinned digest")
	for relative, content in desired_files().items():
		write_text(ROOT / relative, content.replace("\r\n", "\n"))
	rebuild_catalog(ROOT)
	write_coverage_report(ROOT)


def check() -> None:
	drift = [relative.as_posix() for relative, content in desired_files().items() if not compare_lf(ROOT / relative, content)]
	if not (ROOT / MANIFEST_PATH).is_file() or sha256_file(ROOT / MANIFEST_PATH) != MANIFEST_CONTENT_SHA256:
		drift.append(MANIFEST_PATH.as_posix())
	if (ROOT / AUTHOR_READY_PATH).exists():
		drift.append(AUTHOR_READY_PATH.as_posix())
	catalog = load_json(ROOT / "catalog/pinmame.json")
	machine_rows = [row for row in catalog["machines"] if row["id"] == MACHINE_ID]
	if len(machine_rows) != 1 or machine_rows[0].get("definition") != MACHINE_PATH.as_posix() or machine_rows[0].get("definition_sha256") != content_sha256(build_machine()):
		drift.append("catalog/pinmame.json")
	drivers = {row["id"]: row for row in catalog["drivers"]}
	for driver in ("robo_a34", "robo_a30", "robo_a29"):
		if drivers.get(driver, {}).get("machine_id") != MACHINE_ID or drivers.get(driver, {}).get("definition") != MACHINE_PATH.as_posix():
			drift.append("catalog/pinmame.json")
	coverage = build_coverage_report(ROOT)
	queue = build_curation_queue(ROOT)
	generated = {
		Path("reports/coverage.json"): json_text(coverage), Path("reports/coverage.md"): render_coverage_markdown(coverage),
		Path("reports/curation-queue.json"): json_text(queue), Path("reports/curation-queue.md"): render_curation_queue_markdown(queue),
	}
	drift.extend(relative.as_posix() for relative, content in generated.items() if not compare_lf(ROOT / relative, content))
	if drift:
		raise SystemExit("drift: " + ", ".join(sorted(set(drift))))


def main() -> int:
	parser = argparse.ArgumentParser(description="Generate the reviewed Data East RoboCop physical-machine record")
	parser.add_argument("--check", action="store_true", help="refuse generated-artifact drift; CRLF and LF compare equally")
	args = parser.parse_args()
	if args.check:
		check()
	else:
		generate()
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
