"""Curate the physical Williams Space Station (1987) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and table
coordinate is a literal here, so regeneration reproduces the canonical definition, its pinned seed and
the spatial report byte for byte without reading the external evidence roots. ``--check`` refuses
drift, and ``--regenerate`` is the only path that writes them.

Space Station is a System 11B machine (``GEN_S11B``) declared with ``INITGAMEFULL(spstn, GEN_S11B,
s11_dispS11b1, 12, FLIP_SWNO(55,56), 0,0,0,0, 0,63,61,64,60,62)``: ``sxx.muxSol = 12``, so pinned PinMAME
publishes the eight switched "A" loads at 1-8 while the A/C relay is released and their "C" partners at
25-32 while it is energized; ``gameSpecific1`` is 0, so switch 2 is an ordinary (unfitted) matrix
position rather than a relay copy; the cabinet flippers are copied into the two lane-change switches
(``FLIP_SWNO(55,56)``); and ``sxx.ssSw`` maps special solenoids 18-22 to their own playfield switches
(63, 61, 64, 60, 62) while special 17, the right dock kicker, has no switch and is driven by the ROM.
The Space Station toy is a 24 VAC motor switched by a relay on controlled solenoid 16, whose position
cam is read by two optos at switches 52 and 53.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_flipper_column import (
	VPM_CORE_SHA256,
	VPM_LIBRARY_SOURCE,
	VPM_LIBRARY_URI,
	VPM_S11_SHA256,
	flipper_column_inputs,
	flipper_column_relationships,
	vpm_staged_flipper_notes,
)


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.space-station.1987"
PARTIAL_PATH = ROOT / "machines/partial/williams/space-station-1987.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/space-station-1987.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/williams/space-station-1987.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools/seeds/williams/space-station-1987-legacy-aliases.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/space-station-1987.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/space-station-1987.md"
KNOWLEDGE_PATH = "knowledge/williams/space-station-1987.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/space-station-l5-service-and-mechanisms.json"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.williams.space-station.1987"
AMENDMENT_SOURCE = "service-bulletin.williams.space-station.1987.amendments"
ROM_TABLE_SOURCE = "rom-static.space-station.spstn-l5-name-tables"
RUNTIME_SOURCE = "runtime.space-station.l5-service-and-mechanisms"
VARIANT_SOURCE = "human-review.space-station.production-variants"
VPX_SCRIPT_SOURCE = "vpx-script.space-station-vpw-1-0-1"

# (left, right) in the driver's own FLIP_SWNO macro order.
FLIP_SWNO = (55, 56)
AC_RELAY = 12
# INITGAMEFULL ss17..ss22: the playfield switch PinMAME reads for each special solenoid (0 = none).
SPECIAL_SWITCHES = {17: 0, 18: 63, 19: 61, 20: 64, 21: 60, 22: 62}

MANUAL_SHA256 = "71e3212599e733ed432cdc533190ead6a925ff7a5d62862d7c09897566aaddbc"
AMENDMENT_SHA256 = "ae36309aeaed2ab6e2d5e71872658e688d1fcac95477fe040b96f4e6b8da994c"
ROM_ARCHIVE_SHA256 = "8c5cdaf5a8e6a4b112873f17c6a66ca34de6ac15eb830474965cdfa035434f7c"
ROM_U27_SHA256 = "9b6b108a53e1149d6fd3ff6abe308bc3e7f3ffceee204a44caf3dbe2dfa53bf5"
SCRIPT_SHA256 = "0d47d55e2f5cbf6208ace2b01a1beaf30ff0e6e94d51c6712adc17eb282ae9e9"
SCRIPT_NAME = "Space Station (Williams 1987) VPW v1.0.1.vbs"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

DRIVER_IDS = ("spstn_l5",)
DRIVER_COMPATIBILITY = {
	"spstn_l5": (
		"identical",
		"Williams LA-5 production game ROMs (sstn_u26.l5, sstn_u27.l5) with the L-1 sound ROMs, the only Space Station driver "
		"in the pinned catalog (src/wpc/s11games.c lines 486-498; catalogued 1988, the year the manual was printed, while IPDB "
		"dates the first units December 7, 1987). The local archive's members match the driver's SHA-1s, and the retained "
		"known-working table binds it (cGameName = \"spstn_l5\"). Its lamp test is written for the \"Wheel Version\" backbox "
		"insert (see lamps 37, 41, 46-49 and 57); the same ROM runs both production insert boards.",
	),
}

# --- Switch matrix (public address = (column-1)*8+row; System 11 sequential column-major).
# Labels of record follow the Switch-Matrix Table (printed page 51) with detail from the Switches parts list
# (printed page 50); the ROM's own Switch Levels names are kept per address.
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 3: "Credit Button", 4: "Right Coin Chute", 5: "Center Coin Chute", 6: "Left Coin Chute",
	7: "Slam Tilt", 8: "High Score Reset", 9: "Playfield Tilt", 10: "Outhole", 11: "Ball Trough #1 (Right)",
	12: "Ball Trough #2 (Middle)", 13: "Ball Trough #3 (Left)", 14: "1 (Mini-Playfield Lane)", 15: "2 (Mini-Playfield Lane)",
	16: "3 (Mini-Playfield Lane)", 17: "Left Drain Lane", 18: "S (SHUTTLE Standup)", 19: "H (SHUTTLE Standup)",
	20: "U (SHUTTLE Standup)", 21: "First T (SHUTTLE Standup)", 22: "Second T (SHUTTLE Standup)", 23: "L (SHUTTLE Standup)",
	24: "E (SHUTTLE Standup)", 25: "S (STATION Standup)", 26: "First T (STATION Standup)", 27: "A (STATION Standup)",
	28: "Second T (STATION Standup)", 29: "I (STATION Standup)", 30: "O (STATION Standup)", 31: "N (STATION Standup)",
	32: "Right Drain Lane", 33: "Right Single Drop Target (Ramp)", 34: "West German Scoreboard Switch", 35: "Change Shuttle/Station Score Target",
	37: "Top Left Roll-Under", 38: "U (U-S-A Lane)", 39: "S (U-S-A Lane)", 40: "A (U-S-A Lane)", 41: "Left Ball Popper",
	42: "Right Ball Popper", 43: "Ball Shooter Lane", 45: "Right Lock", 46: "Right Lock Entry (Station Exit Ramp)",
	47: "Left Lock", 48: "Left Lock Entry (Wire Ramp)", 50: "10 Point (Top Right)", 52: "Space Station Position #1",
	53: "Space Station Position #2", 54: "10 Point (Lower Right)", 55: "Left Lane Change (Left Flipper)",
	56: "Right Lane Change (Right Flipper)", 57: "3-Bank Drop Target (Upper)", 58: "3-Bank Drop Target (Center)",
	59: "3-Bank Drop Target (Lower)", 60: "Left Jet Bumper", 61: "Right Jet Bumper", 62: "Lower Jet Bumper",
	63: "Left Slingshot", 64: "Right Slingshot",
}
UNUSED_SWITCHES = frozenset({2, 36, 44, 49, 51})
# Fitted only on some machines: the West German version's scoreboard switch.
OPTIONAL_SWITCHES = frozenset({34})
# Switch-Matrix Table cell wording (printed page 51), every cell.
MATRIX_WORDING = {
	1: "Plumb Bob Tilt", 2: "Not Used", 3: "Credit Button", 4: "Right Coin Chute", 5: "Center Coin Chute", 6: "Left Coin Chute",
	7: "Slam Tilt", 8: "High-Score Reset", 9: "Playfield Tilt", 10: "Outhole", 11: "Ball Trough #1 (right)",
	12: "Ball Trough #2 (mid)", 13: "Ball Trough #3 (left)", 14: "1", 15: "2", 16: "3", 17: "Drain Lane (left)", 18: "S",
	19: "H", 20: "U", 21: "T", 22: "T", 23: "L", 24: "E", 25: "S", 26: "T", 27: "A", 28: "T", 29: "I", 30: "O", 31: "N",
	32: "Drain Lane (right)", 33: "Single Drop Target (right ramp)", 34: "(German Score Board Sw)",
	35: "Change Shuttle/Station Score", 36: "Not Used", 37: "Top left Roll-under", 38: "U", 39: "S", 40: "A",
	41: "Left Ball Popper", 42: "Right Ball Popper", 43: "Ball Shooter", 44: "Not Used", 45: "Right Lock", 46: "Right Lock Entry",
	47: "Left Lock", 48: "Left Lock Entry", 49: "Not Used", 50: "10-Point (top right)", 51: "Not Used", 52: "Space Station #1",
	53: "Space Station #2", 54: "10-Point (lwr right)", 55: "LANE CHANGE (left flipper)", 56: "LANE CHANGE (right flipper)",
	57: "3-bank Dr Tgt (upr)", 58: "3-bank Dr Tgt (cntr)", 59: "3-bank Dr Tgt (lwr)", 60: "Jet Bumper (left)",
	61: "Jet Bumper (right)", 62: "Jet Bumper (lower)", 63: "Left Kicker (\"sling\")", 64: "Right Kicker (\"sling\")",
}
# Switches parts list (printed page 50): (part number, description); None = printed blank.
SWITCH_PARTS = {
	1: ("A-8476", "Plumb Bob Tilt"), 2: (None, "Not Used"), 3: ("SW-1A-126", "Credit Button"),
	4: ("904845*", "Right Coin Chute"), 5: ("904845*", "Center Coin Chute"), 6: ("904845*", "Left Coin Chute"),
	7: ("904704*", "Slam Tilt"), 8: ("5641-09369-00", "High Score Reset"), 9: ("SW-1A-117", "Playfield Tilt"),
	10: ("17-1067", "Outhole"), 11: ("5647-09938-00", "Ball Trough #1 (right)"), 12: ("5647-09957-00", "Ball Trough #2 (mid)"),
	13: ("5647-09957-00", "Ball Trough #3 (left)"), 14: ("5647-12073-01", "1 (lane rollover)"),
	15: ("5647-12073-01", "2 (lane rollover)"), 16: ("5647-12073-01", "3 (lane rollover)"),
	17: ("5647-12073-10", "Left Drain Lane"), 18: ("B-11696-5", "S (Standup Target)"), 19: ("B-11696-5", "H (Standup Target)"),
	20: ("B-11696-5", "U (Standup Target)"), 21: ("B-11696-5", "T (Standup Target)"), 22: ("B-11696-5", "T (Standup Target)"),
	23: ("B-11696-5", "L (Standup Target)"), 24: ("B-11696-5", "E (Standup Target)"), 25: ("B-11696-5", "S (Standup Target)"),
	26: ("B-11696-5", "T (Standup Target)"), 27: ("B-11696-5", "A (Standup Target)"), 28: ("B-11696-5", "T (Standup Target)"),
	29: ("B-11696-5", "I (Standup Target)"), 30: ("B-11696-5", "O (Standup Target)"), 31: ("B-11696-5", "N (Standup Target)"),
	32: ("5647-12073-10", "Right Drain Lane"), 33: ("C-11903-R", "Right1-bank Dr Tgt Opto"), 34: (None, "(German Scoreboard)"),
	35: ("B-11696-8", "Change Sh/St Score"), 36: ("Not Used", None), 37: ("SW-1A-168", "Top left Roll-under"),
	38: ("5647-12073-10", "U (lane rollover)"), 39: ("5647-12073-10", "S (lane rollover)"),
	40: ("5647-12073-10", "A (lane rollover)"), 41: ("SW-1A-167", "Left Ball Popper"), 42: ("SW-1A-167", "Right Ball Popper"),
	43: ("5647-12073-04", "Ball Shooter Lane"), 44: (None, "Not Used"), 45: ("5647-12073-10", "Right Lock"),
	46: ("SW-1A-164", "R Lock Entry (St. exit ramp)"), 47: ("5647-12133-01", "Left Lock"),
	48: ("5647-12073-01", "L Lock Entry (on wire ramp)"), 49: ("Not Used", None), 50: ("B-4834-K-1", "10 point (top right)"),
	51: (None, "Not Used"), 52: ("C-11872", "Space Station #1"), 53: ("C-11872", "Space Station #2"),
	54: ("B-4834-K-1", "10 point (lwr right)"), 55: ("SW-1A-150-1", "Lane Change (L Flipper)"),
	56: ("SW-1A-150", "Lane Change (R Flipper)"), 57: ("C-11318", "3-bank Dr Tgt (upper)"), 58: ("C-11318", "3-bank Dr Tgt (center)"),
	59: ("C-11318", "3-bank Dr Tgt (lower)"), 60: ("SW-11A-35", "Jet Bumper (left)"), 61: ("SW-11A-35", "Jet Bumper (right)"),
	62: ("SW-11A-35", "Jet Bumper (lower)"), 63: ("SW-1A-122", "Left Sling (scoring)**"), 64: ("SW-1A-122", "RightSling (scoring)**"),
}
# Switch table text in the U27 program ROM, as the Switch Levels test prints it (excerpt rom-name-tables).
ROM_SWITCH_NAMES = {
	1: "PLUMB TILT", 2: "BALL TILT", 3: "CREDIT BUTTON", 4: "COIN SLOT 1", 5: "COIN SLOT 2", 6: "COIN SLOT 3", 7: "SLAM TILT",
	8: "HISCORE RESET", 9: "PLAYFLD TILT", 10: "OUTHOLE", 11: "TROUGH BALL 1", 12: "TROUGH BALL 2", 13: "TROUGH BALL 3",
	14: "ROLOVER 1", 15: "ROLOVER 2", 16: "ROLOVER 3", 17: "LEFT DRAIN", 18: "SHUTTLE S", 19: "SHUTTLE H", 20: "SHUTTLE U",
	21: "SHUTTLE 1ST T", 22: "SHUTTLE 2ND T", 23: "SHUTTLE L", 24: "SHUTTLE E", 25: "STATION S", 26: "STATION 1ST T",
	27: "STATION A", 28: "STATION 2ND T", 29: "STATION I", 30: "STATION O", 31: "STATION N", 32: "RIGHT DRAIN",
	33: "R SNGLE DROP TG", 34: "NOT USED", 35: "SHT CHG BOTTOM", 36: "NOT USED", 37: "ROL UND TOP L", 38: "USA U", 39: "USA S",
	40: "USA A", 41: "L BALL POPPER", 42: "R BALL POPPER", 43: "PLUNGER", 44: "", 45: "RIGHT LOCK UP", 46: "R LOCK ENTRY",
	47: "LEFT LOCK UP", 48: "L LOCK ENTRY", 49: "NOT USED", 50: "TOP RGT 10 PTS", 51: "LEFT 10 PTS", 52: "SPC STA SWTCH 1",
	53: "SPC STA SWTCH 2", 54: "LOW RGT 10 PTS", 55: "LEFT FLIPPER", 56: "RIGHT FLIPPER", 57: "3 BANK BOTTOM", 58: "3 BANK CENTER",
	59: "3 BANK TOP", 60: "LEFT BUMPER", 61: "RIGHT BUMPER", 62: "BOTTOM BUMPER", 63: "LEFT KICKER", 64: "RIGHT KICKER",
}
# Construction is asserted only where a part number, footnote or assembly page identifies it.
SWITCH_TYPES = {1: "tilt", 3: "button", 4: "other", 5: "other", 6: "other", 7: "tilt", 8: "button", 9: "tilt", 33: "opto", 52: "opto", 53: "opto", 57: "opto", 58: "opto", 59: "opto"}
MICROSWITCH_PREFIXES = ("5647-12073-", "5647-09957-", "5647-09938-")
SWITCH_COLUMN_WIRING = {
	1: ("GRN-BRN", "1J8-1", "Q45"), 2: ("GRN-RED", "1J8-2", "Q49"), 3: ("GRN-ORN", "1J8-3", "Q44"),
	4: ("GRN-YEL", "1J8-4", "Q48"), 5: ("GRN-BLK", "1J8-5", "Q43"), 6: ("GRN-BLU", "1J8-7", "Q47"),
	7: ("GRN-VIO", "1J8-8", "Q42"), 8: ("GRN-GRY", "1J8-9", "Q46"),
}
SWITCH_ROW_WIRING = {
	1: ("WHT-BRN", "1J10-9"), 2: ("WHT-RED", "1J10-8"), 3: ("WHT-ORN", "1J10-7"), 4: ("WHT-YEL", "1J10-6"),
	5: ("WHT-GRN", "1J10-5"), 6: ("WHT-BLU", "1J10-3"), 7: ("WHT-VIO", "1J10-2"), 8: ("WHT-GRY", "1J10-1"),
}
DEDICATED_LABELS = {
	-7: ("Advance (Diagnostic)", "service.advance"), -6: ("Auto-Up/Manual-Down (Diagnostic)", "service.updown"),
	-5: ("CPU Diagnostic (SW 2)", "service.cpu-diag"), -4: ("Sound Diagnostic (SW 1)", "service.sound-diag"),
}
CABINET_SWITCH_ROLES = {
	1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin", 7: "cabinet.slam-tilt",
	8: "cabinet.service", 9: "cabinet.tilt", 55: "cabinet.flipper", 56: "cabinet.flipper",
}
# What the retained known-working script does with each switch.
SWITCH_SCRIPT = {
	9: "vpmNudge.TiltSwitch = 9 (script line 383), so the table's nudge tilt closes the playfield tilt",
	10: "sw10_Hit/UnHit (lines 1189-1190), the drain kicker the script's trough starts from",
	11: "sw11_Hit/UnHit (lines 1187-1188); held closed at start (line 397)",
	12: "sw12_Hit/UnHit (lines 1185-1186); held closed at start (line 398)",
	13: "sw13_Hit/UnHit (lines 1183-1184); held closed at start (line 399)",
	14: "sw14_Hit/UnHit (lines 1665-1666), commented \"Upper Playfield\"",
	15: "sw15_Hit/UnHit (lines 1667-1668), commented \"Upper Playfield\"",
	16: "sw16_Hit/UnHit (lines 1669-1670), commented \"Upper Playfield\"",
	17: "sw17_Hit/UnHit (lines 1672-1673); its comment \"Left Inlane\" is wrong, the machine has no inlanes",
	32: "sw32_Hit/UnHit (lines 1674-1675); its comment \"Right Inlane\" is wrong, the machine has no inlanes",
	33: "sw33_Hit -> DTHit 33 (line 1728), a drop target the DT33 entry of DTArray models",
	35: "sw35_hit -> STHit 35 (line 1725), commented \"Change\"",
	37: "sw37_Hit/UnHit (lines 1690-1691), commented \"Left Orbit\"",
	38: "sw38_Hit/UnHit (lines 1677-1678), commented \"USA Rollover\"",
	39: "sw39_Hit/UnHit (lines 1679-1680), commented \"USA Rollover\"",
	40: "sw40_Hit/UnHit (lines 1681-1682), commented \"USA Rollover\"",
	41: "sw41_Hit/unhit (lines 1770-1780), the kicker KickerUpperLeft (solenoid 3) lifts",
	42: "sw42_Hit/unhit (lines 1794-1804), the kicker KickerUpperRight (solenoid 4) lifts",
	43: "sw43_Hit/UnHit (lines 1684-1685), commented \"Shooter Lane\"",
	45: "sw45_Hit/unhit (lines 1818-1826), the right dock RightDockKick (solenoid 17) kicks",
	46: "sw46_Hit/UnHit (lines 1686-1687), commented \"Right Lock Ramp Entry\"",
	47: "sw47_Hit/unhit (lines 1848-1857), the left dock LeftDockKick (solenoid 32) kicks",
	48: "sw48_Hit/UnHit (lines 1693-1694), commented \"Left Lock Entry\"",
	50: "sw50_rubber_Hit -> vpmTimer.PulseSw(50) (line 1697), commented \"Lower Right Rubber Switch\"",
	52: "MotorUpdate (lines 1238-1249) writes it from its modelled station angle: 1 between 180 and 360 degrees",
	53: "MotorUpdate (lines 1238-1249) writes it from its modelled station angle: 1 between 90 and 270 degrees",
	54: "sw54_rubber_Hit -> vpmTimer.PulseSw(54) (line 1698), commented \"Uppper Right Rubber Switch\"",
	57: "sw57_Hit -> DTHit 57 (line 1737), DT57 of DTArray",
	58: "sw58_Hit -> DTHit 58 (line 1738), DT58 of DTArray",
	59: "sw59_Hit -> DTHit 59 (line 1739), DT59 of DTArray",
	60: "Bumper1_Hit -> vpmTimer.PulseSw 60 (line 1702)",
	61: "Bumper2_Hit -> vpmTimer.PulseSw 61 (line 1703)",
	62: "Bumper3_Hit -> vpmTimer.PulseSw 62 (line 1704)",
	63: "LeftSlingShot_Slingshot -> vpmTimer.PulseSw(63) (line 1507)",
	64: "RightSlingShot_Slingshot -> vpmTimer.PulseSw(64) (line 1482)",
}
for _address in range(18, 32):
	SWITCH_SCRIPT[_address] = f"sw{_address}_hit -> STHit {_address} (lines 1708-1723)"
# The script's comments for 50 and 54 are crossed against the manual: the manual and the ROM put 50 at the top
# right and 54 at the lower right; the comments say the opposite. The binding object decides placement.

# --- Solenoid Table (PDF 2, reprinted on printed page 28) and Solenoids/Flashers list (printed page 54).
# Switched A/C pairs: (A-side public, C-side public, CPU connection, playfield/cabinet connection, driver, C-side CPU wire).
AC_PAIRS = {
	1: (1, 25, "1P11-1", "8P3-1 (to J1-9 on Aux Pwr Drvr Bd)", "Q33", "Gry-Brn"),
	2: (2, 26, "1P11-3", "8P3-2 (to J1-7 on Aux Pwr Drvr Bd)", "Q25", "Gry-Red"),
	3: (3, 27, "1P11-4", "8P3-3 (to J1-6 on Aux Pwr Drvr Bd)", "Q32", "Gry-Orn"),
	4: (4, 28, "1P11-5", "8P3-4 (to J1-5 on Aux Pwr Drvr Bd)", "Q24", "Gry-Yel"),
	5: (5, 29, "1P11-6", "8P3-5 (to J1-4 on Aux Pwr Drvr Bd)", "Q31", "Gry-Grn"),
	6: (6, 30, "1P11-7", "8P3-6 (to J1-3 on Aux Pwr Drvr Bd)", "Q23", "Gry-Blu"),
	7: (7, 31, "1P11-8", "8P3-7 (to J1-2 on Aux Pwr Drvr Bd)", "Q30", "Gry-Vio"),
	8: (8, 32, "1P11-9", "8P3-8 (to J1-1 on Aux Pwr Drvr Bd)", "Q22", "Gry-Blk"),
}
SOLENOID_LABELS = {
	1: "Outhole Kicker", 2: "Ball Shooter Lane Feeder", 3: "Left Ball Popper", 4: "Right Ball Popper",
	6: "3-Bank Drop Target Reset", 7: "Knocker", 8: "Right Single Drop Target Reset",
	9: "Playfield G.I. Relay", 10: "Green G.I. Relay", 11: "Insert Board G.I. Relay", 12: "A/C Select Relay",
	13: "Left Re-Entry Kickback", 15: "Playfield Top Panel Flashers", 16: "Space Station Motor Relay",
	17: "Right Dock Kickback", 18: "Left Slingshot", 19: "Right Jet Bumper", 20: "Right Slingshot", 21: "Left Jet Bumper",
	22: "Lower Jet Bumper",
	25: "Relaunch + \"ON\" Flashers", 26: "Left Side + \"SP\" Flashers", 27: "Right Side + \"AC\" Flashers",
	28: "Top (Upper Playfield) + \"ES\" Flashers", 29: "Playfield Top Panel + \"TA\" Flashers", 30: "Flame + \"TI\" Flashers",
	31: "Station Flashers", 32: "Left Dock Kickbig",
}
UNUSED_SOLENOIDS = {5: "Unused Switched Drive 05A", 14: "Unused Controlled Drive 14"}
SOLENOID_MANUAL_NUMBER = {address: f"{address:02d}A" for address in range(1, 9)}
SOLENOID_MANUAL_NUMBER.update({address: f"{address - 24:02d}C" for address in range(25, 33)})
SOLENOID_MANUAL_NUMBER.update({address: f"{address:02d}" for address in range(9, 23)})
SOLENOID_TABLE_WORDING = {
	1: "Outhole Kicker", 2: "Ball Shooter Lane Feeder", 3: "Left Ball Popper", 4: "Right Ball Popper", 5: "Not Used",
	6: "3-bank Drop Target", 7: "Knocker (or Ticket Dispenser)", 8: "R Sngl Drop Target - Raise",
	9: "General Illum Relay (Playfield)", 10: "General Illum Relay (Green)", 11: "General Illum Relay (Insert Bd)",
	12: "A/C Select Relay", 13: "Left Re-Entry Kickback (drain)", 14: "Not Used", 15: "P'fld Top Panel Flashers (3)",
	16: "Space Station Motor/Relay", 17: "Right Dock Kickback", 18: "Lower Left Kicker (\"sling\")", 19: "Rt Jet Bumper",
	20: "Lower Right Kicker (\"sling\")", 21: "Left Jet Bumper", 22: "Lower Jet Bumper",
	25: "Relaunch + \"ON\" Flashers", 26: "Left Side + \"SP\" Flashers", 27: "Right Side + \"AC\" Flashers",
	28: "Top (upr p/f) + \"ES\" Flashers", 29: "P'fld Top Panel + \"TA\" Flashers", 30: "Flame + \"TI\" Flashers",
	31: "Station Flasher", 32: "Left Dock Kickbig",
}
LIST_WORDING = {
	1: "Outhole Kicker", 2: "Ball Shooter Lane Feeder", 3: "Left Ball Popper", 4: "Right Ball Popper", 5: "Not Used",
	6: "3-bank Drop Tgt-Raise", 7: "Knocker (or Ticket Dispenser)", 8: "Right 1-bank Drop Tgt-Raise",
	9: "Gen. Illumin. Relay, P'field*", 10: "Gen. Illumin. Relay, Green*", 11: "Gen. Illumin. Relay, B'box*",
	12: "A/C Select Relay**", 13: "Left Re-Entry Kickback", 14: "Not Used", 15: "P/f Top Panel Flashers",
	16: "S. Station Motor Relay***", 17: "Right Dock Kickback", 18: "Lower Left Kicker (\"sling\")", 19: "Right Jet Bumper",
	20: "Lower Right Kicker (\"sling\")", 21: "Left Jet Bumper", 22: "Lower Jet Bumper",
	25: "Relaunch + \"ON\" Flashers", 26: "Left Side + \"SP\" Flashers", 27: "Right Side + \"AC\" Flashers",
	28: "Top (upr p/f) + \"ES\" Flashers", 29: "P/f Top Panel + \"TA\" Flashers", 30: "Flame + \"TI\" Flashers",
	31: "Station Flashers", 32: "Left Dock Kickbig",
}
ROM_COIL_NAMES = {
	1: "OUTHOLE", 25: "RELNCH FLASHER", 2: "BALL RELEASE", 26: "LEFT FLASHER", 3: "LF BALL POPPER", 27: "RIGHT FLASHER",
	4: "RT BALL POPPER", 28: "TOP FLASHER", 29: "PANEL FLASHER", 6: "3 BANK", 30: "FLAME FLASHER", 7: "INSERT KNOCKER",
	31: "STATION FLASHER", 8: "RIGHT DROP TG", 32: "LEFT DOCK", 9: "PLAYFLD GEN ILU", 10: "PLAYFLD GRN GI", 11: "INSERT GI",
	12: "AC SELECT", 13: "LEFT REENTRY", 15: "PANEL LIGHTS", 16: "SPACE STATION", 17: "RIGHT DOCK", 18: "LEFT SLING",
	19: "RIGHT JET", 20: "RIGHT SLING", 21: "LEFT JET", 22: "BOTTOM JET",
}
COIL_TEST_ORDER = (1, 25, 2, 26, 3, 27, 4, 28, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22)
SOLENOID_WIRE = {
	1: "Vio-Brn", 25: "Blk-Brn", 2: "Vio-Red", 26: "Blk-Red", 3: "Vio-Orn", 27: "Blk-Orn", 4: "Vio- Yel", 28: "Blk-Yel",
	5: "Vio-Grn", 29: "Blk-Grn", 6: "Vio-Blu", 30: "Blk-Blu", 7: "Vio-Blk", 31: "Blk-Vio", 8: "Vio-Gry", 32: "Blk-Gry",
	9: "Brn-Blk", 10: "Brn-Red", 11: "Brn-Orn", 12: "Brn-Yel", 13: "Brn-Grn", 14: "Brn-Blu", 15: "Brn-Vio", 16: "Brn-Gry",
	17: "Blu-Brn", 18: "Blu-Red", 19: "Blu-Orn", 20: "Blu-Yel", 21: "Blu-Grn", 22: "Blu-Blk",
}
CONTROLLED = {
	9: ("1P12-1", "8P3-9", "Q17"), 10: ("1P12-2", "8P3-10", "Q9"), 11: ("1P12-4", "6P3-5", "Q16"), 12: ("1P12-5", "8P3-12", "Q8"),
	13: ("1P12-6", "8P3-13", "Q15"), 14: ("1P12-7", "8P3-14", "Q7"), 15: ("1P12-8", "8P3-15", "Q14"), 16: ("1P12-9", "8P3-16", "Q6"),
	17: ("1P19-7", "8P3-17", "Q75"), 18: ("1P19-4", "8P3-18", "Q71"), 19: ("1P19-3", "8P3-19", "Q73"), 20: ("1P19-6", "8P3-20", "Q69"),
	21: ("1P19-8", "8P3-21", "Q77"), 22: ("1P19-9", "8P3-22", "Q79"),
}
# Supply voltage of each load's frame on the Controlled, Special, and Switched Solenoids fold-out (printed page 69).
NOMINAL_VOLTAGE = {1: 25, 2: 25, 8: 25, 3: 50, 4: 50, 6: 50, 7: 50, 9: 25, 10: 25, 11: 25, 12: 25, 15: 25, 16: 25, 13: 50, 17: 50, 18: 50, 20: 50, 19: 25, 21: 25, 22: 25}
NOMINAL_VOLTAGE.update({address: 25 for address in range(25, 33)})
SOLENOID_PART = {
	1: "AE-23-800", 25: "#89 flashlamps", 2: "AE-23-800", 26: "#89 flashlamps", 3: "AE-24-900", 27: "#89 flashlamps",
	4: "AE-23-800", 28: "#89 flashlamps", 29: "#89 flashlamps", 6: "AE-26-1200", 30: "#89 flashlamps", 7: "AE-26-1200",
	31: "#89 flashlamps", 8: "AE-23-800", 32: "AE-23-800", 9: "5580-09555-01", 10: "5580-09555-01", 11: "5580-09555-01",
	12: "5580-09555-01", 13: "AE-24-900", 15: "#1251 flashlamps", 16: "14-7941-2/5580-12145-01", 17: "AE-23-800",
	18: "AE-26-1200", 19: "AE-23-800", 20: "AE-26-1200", 21: "AE-23-800", 22: "AE-23-800",
}
# The Solenoid Table's quantity suffix (b = backbox, p = playfield) per flasher circuit.
FLASHLAMP_QUANTITY = {25: (2, 2), 26: (2, 2), 27: (2, 2), 28: (2, 2), 29: (2, 2), 30: (4, 0), 31: (2, 0), 15: (3, 0)}
SOLENOID_KIND = {
	1: "coil", 2: "coil", 3: "coil", 4: "coil", 6: "coil", 7: "coil", 8: "coil", 9: "gi", 10: "gi", 11: "gi", 12: "relay",
	13: "coil", 15: "flasher", 16: "motor", 17: "coil", 18: "coil", 19: "coil", 20: "coil", 21: "coil", 22: "coil",
	25: "flasher", 26: "flasher", 27: "flasher", 28: "flasher", 29: "flasher", 30: "flasher", 31: "flasher", 32: "coil",
}
# What the retained known-working script does with each address.
SOLENOID_CALLBACKS = {
	1: "SolTrough (line 1094), which kicks a drained ball from the drain kicker sw10 into the trough",
	2: "SolRelease (line 1095), which kicks the lead trough ball from sw11 into the shooter lane",
	3: "KickerUpperLeft (line 1096), which lifts the ball out of kicker sw41 (KickBall angle 0, vertical speed 30)",
	4: "KickerUpperRight (line 1097), which lifts the ball out of kicker sw42 (KickBall angle 270, vertical speed 60)",
	6: "ResetDrops3 (line 1099), raising the three drop targets 57-59",
	7: "SolKnocker (line 1100), the knocker sound at the table's KnockerPosition",
	8: "ResetDrops1 (line 1101), raising drop target 33",
	9: "SolModCallback GIUpdates (line 1103), which sets every playfield G.I. light (collections GI and gi_green) to the modulated level",
	10: "GiSelect (line 1104), which shows the white G.I. light maps while it reads on and the green ones while it reads off",
	11: "GiBackbox (line 1105), which switches the backglass G.I. light GI_BG",
	12: "SolACSelectRelay (line 1107), a relay sound only",
	13: "SolKickBack (line 1108), firing the VPX Kickback object at the left outlane",
	15: "SolModCallback SolMod15 (line 1116), commented \"P/f Top Panel Flashers (x3 pf - 28v Lamps)\", driving flashers f15, f15b and f15c",
	16: "StationMotor (line 1110), which runs MotorUpdate's modelled station rotation while it is on",
	17: "RightDockKick (line 1111), which kicks the ball out of sw45",
	23: "none directly; s11.vbs's flipper handling enables the flippers while it is on",
	25: "SolMod25 (line 1117), commented \"Relaunch (x2 pf) + \\\"ON\\\" Flashers (x2 Backbox)\", driving f25 and f25b",
	26: "SolMod26 (line 1118), commented \"Left Side (x2 pf) + \\\"SP\\\" Flashers (x2 Backbox)\", driving f26 and f26b",
	27: "SolMod27 (line 1119), commented \"Right Side (x2 pf) + \\\"AC\\\" Flashers (x2 Backbox)\", driving f27 and f27b",
	28: "SolMod28 (line 1120), commented \"Top Upper Playfield (x2 pf) + \\\"ES\\\" Flashers (x2 Backbox)\", driving f28 and f28b",
	29: "SolMod29 (line 1121), commented \"Playfield Top Panel (x2pf) + \\\"TA\\\" Flashers (x2 Backbox)\", driving f29 and f29b",
	30: "SolMod30 (line 1122), commented \"Flame + \\\"TI\\\" Flashers (x4 Backbox)\", driving f30",
	31: "SolMod31 (line 1123), commented \"Station Flashers (x2 Backbox)\", driving f31",
	32: "LeftDockKick (line 1113), which kicks the ball out of sw47; its comment says \"Right Dock Kickback\" but the code works sw47",
}
# Behaviour each output showed in the runs, appended to its note.
SOLENOID_RUNTIME = {
	1: "With the outhole switch (10) held from power-up the ROM fired it every 2.2 s; in the gameplay run it fired 0.6 s after the drained ball closed 10.",
	2: "In the gameplay run the ROM fired it at Start and again 2.1 s later until the host emptied a trough switch, and again for each ball served while a ball was docked.",
	3: "At power-up the ROM pulses it once in its ball search (power-up probes); with 41 and 42 held from power-up it fired every 2.2 s alongside 4.",
	4: "At power-up the ROM pulses it once in its ball search; in the gameplay run it fired 0.45 s after the right popper switch (42) closed.",
	6: "In the gameplay run the ROM fired it once all three 3-bank targets (57-59) were held down, and once more 1.3 s later.",
	8: "In the gameplay run the ROM fired it about 24 s after the single drop target (33) went down, at the end of the Stop 'N' Score timer, and retried every 1.4 s while 33 stayed down.",
	9: "In the gameplay run the ROM energized it, with 11, from the third plumb-bob tilt until the next ball started, and flickered it for display effects.",
	10: "In the gameplay run the ROM energized it 4.5 s after the left popper started multiball with both locks full and released it 8 s later, as the locked balls left.",
	11: "In the gameplay run the ROM energized it, with 9, from the third plumb-bob tilt until the next ball started, and flickered it for display effects.",
	12: "The ROM energizes it ahead of the C-side steps of the Coil Test and releases it for every A-side step.",
	13: "In the gameplay run the ROM fired it within one poll of the left drain lane switch (17) closing with the kickback lit.",
	16: "At power-up the ROM energizes it until the position switches change into (52 open, 53 closed), or for about 5.3 s when they never change (power-up probes); in the gameplay run, with 52 and 53 left open, it held it on from Start for 90 s.",
	17: "At power-up the ROM pulses it once in its ball search; with 45 held from power-up it fired once more and then stopped.",
	18: "In the Switch Levels and gameplay runs it rose with switch 63, through PinMAME's switch-driven special solenoid path.",
	19: "In the Switch Levels and gameplay runs it rose with switch 61, through PinMAME's switch-driven special solenoid path.",
	20: "In the Switch Levels and gameplay runs it rose with switch 64, through PinMAME's switch-driven special solenoid path.",
	21: "In the Switch Levels and gameplay runs it rose with switch 60, through PinMAME's switch-driven special solenoid path.",
	22: "In the Switch Levels and gameplay runs it rose with switch 62, through PinMAME's switch-driven special solenoid path.",
	32: "At power-up the ROM pulses it once in its ball search; with 47 held from power-up it fired every 2.1 s.",
}

VIRTUAL_SOLENOIDS = {
	23: ("Game-On / Special-Solenoid Enable", "used", "internal.game-on-enable", (
		"PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL (pinned src/wpc/s11.h S11_GAMEONSOL 23), set from PIA0 CB2 in "
		"pia0cb2_w and used to gate the switch-driven special solenoids and the synthetic flipper outputs 45-48. It has no "
		"driver transistor and no Sol. No. of its own. In the gameplay run it rises at Start, falls at the third plumb-bob "
		"tilt and rises again for the next ball; the ROM also holds it while its diagnostic tests run."
	)),
	24: ("Unassigned Solenoid Slot 24", "unused", "internal.unused-platform-slot", (
		"Unassigned platform gap between the special-solenoid enable (23) and the A/C-relay C-side bank (25-32); no System "
		"11 driver populates it and no Space Station run published it."
	)),
	45: ("Synthetic Lower Right Flipper Power", "used", "internal.synthetic-flipper", (
		"PinMAME's synthetic lower-right flipper power output (CORE_FIRSTLFLIPSOL = 45). spstnGameData declares "
		"FLIP_SWNO(55,56) with no FLIP_SOL, so core_updateSw fabricates 45/46 from the right button bit at public 82 and "
		"47/48 from the left bit at public 84 while the enable (23) is on; in the Switch Levels run holding 82 raised 45 and "
		"46 and holding 84 raised 47 and 48. The manual confirms there is no driver behind them: the two flipper rows of the "
		"Solenoid Table carry no Sol. No. and no transistor, and note 1 says the CPU-board wire runs to the flipper switch. "
		"The retained script binds SolCallback(sLRFlipper) and SolCallback(sLLFlipper) to its flipper subs (lines "
		"1125-1126)."
	)),
	46: ("Synthetic Lower Right Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-right flipper hold output; see address 45."),
	47: ("Synthetic Lower Left Flipper Power", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper power output; see address 45."),
	48: ("Synthetic Lower Left Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper hold output; see address 47."),
	49: ("PinMAME Simulator Ball-Shooter Channel", "unused", "internal.unused-platform-slot", (
		"Platform-wide simulator-only output (CORE_FIRSTSIMSOL = 49); spstnGameData declares no simulator."
	)),
	50: ("Unassigned Solenoid Slot 50", "unused", "internal.unused-platform-slot", (
		"Unassigned gap below the custom-solenoid base (51). spstnGameData declares no custSol, so MACHINE_INIT(s11) sizes "
		"coreGlobals.nSolenoids as CORE_FIRSTCUSTSOL-1+0 = 50 and nothing above 50 is modelled."
	)),
}
UPPER_FLIPPER_NOTE = (
	"Platform generic upper-flipper address (CORE_FIRSTUFLIPSOL = 33). spstnGameData's FLIP_SWNO(55,56) sets no upper "
	"FLIP_SW or FLIP_SOL bit and core_getSol serves 33-36 only for WPC and SAM generations, so it reads as always zero. "
	"Space Station has two flippers only: the Solenoid Table and the Solenoids/Flashers list name a right and a left "
	"flipper and nothing else."
)
OVERLAY_NOTE = (
	"Platform sound-overlay range (37-44). spstnGameData's hw.gameSpecific1 is 0, so S11_SNDOVERLAY is unset and "
	"pia5cb2_w never diverts the sound byte to a solenoid pattern. Unpopulated on this machine."
)

# --- Lamp matrix (public address = (column-1)*8+row). Labels from the Lamps list (printed page 53) and the
# Lamp-Matrix Table (printed page 52); the insert-board lamps are labelled for both production insert boards.
LAMP_LABELS = {
	1: "Bonus Ball Player 1", 2: "Bonus Ball Player 2", 3: "Bonus Ball Player 3", 4: "Bonus Ball Player 4",
	5: "Extra Ball (3-Bank Drop Targets)", 6: "Release (Right)", 7: "Release (Left)", 8: "Dock When Lit (Left)",
	9: "Change Shuttle", 10: "Change Station", 11: "1X", 12: "2X", 13: "4X", 14: "1 (Mini-Playfield Lane)",
	15: "2 (Mini-Playfield Lane)", 16: "3 (Mini-Playfield Lane)", 17: "Re-Entry When Lit (Left Drain)",
	18: "S (in SHUTTLE)", 19: "H (in SHUTTLE)", 20: "U (in SHUTTLE)", 21: "First T (in SHUTTLE)", 22: "Second T (in SHUTTLE)",
	23: "L (in SHUTTLE)", 24: "E (in SHUTTLE)", 25: "S (in STATION)", 26: "First T (in STATION)", 27: "A (in STATION)",
	28: "Second T (in STATION)", 29: "I (in STATION)", 30: "O (in STATION)", 31: "N (in STATION)",
	32: "Re-Entry When Lit (Right Drain)", 33: "Stop 'N' Score", 34: "Dock When Lit (Right)", 35: "Special",
	36: "100,000 When Lit", 37: "Station Wheel 4 / Little Shuttle (Backbox Insert)", 38: "U (U-S-A Lane)",
	39: "S (U-S-A Lane)", 40: "A (U-S-A Lane)", 41: "Station Wheel 6 (Backbox Insert, Wheel Version)",
	42: "Relaunch When Lit", 43: "Docked Port Side", 44: "Hold Bonus", 45: "Docked Starboard Side",
	46: "Station Wheel 3 / Williams Left (Backbox Insert)", 47: "Station Wheel 2 / Williams Middle (Backbox Insert)",
	48: "Station Wheel 1 / Williams Right (Backbox Insert)", 49: "Big Flame #1 (Backbox Insert)",
	50: "Shuttle Score Special", 51: "Shuttle Score Extra Ball", 52: "Shuttle Score 50,000 + Re-Entry",
	53: "Shuttle Score 50,000 + Bonus Ball", 54: "Shuttle Score 150,000 + Hold Bonus", 55: "Shuttle Score 75,000",
	56: "Shuttle Score 25,000", 57: "Station Wheel 5 / Big Flame #2 (Backbox Insert)", 58: "Station Score Special",
	59: "Station Score Extra Ball", 60: "Station Score 50,000 + Re-Entry", 61: "Station Score 50,000 + Bonus Ball",
	62: "Station Score 150,000 + Hold Bonus", 63: "Station Score 75,000", 64: "Station Score 25,000",
}
LAMP_MATRIX_WORDING = {
	1: "Bonus Ball Player #1", 2: "Bonus Ball Player #2", 3: "Bonus Ball Player #3", 4: "Bonus Ball Player #4",
	5: "Extra Ball (3-bnk D T)", 6: "RELEASE (right)", 7: "RELEASE (left)", 8: "DOCK W/L (left)", 9: "Change Shuttle",
	10: "Change Station", 11: "1X", 12: "2X", 13: "4X", 14: "1", 15: "2", 16: "3", 17: "RE-ENTRY (Left W/LIT Drain)",
	18: "S", 19: "H", 20: "U", 21: "T", 22: "T", 23: "L", 24: "E", 25: "S", 26: "T", 27: "A", 28: "T", 29: "I", 30: "O",
	31: "N", 32: "RE-ENTRY (Right W/LIT Drain)", 33: "Stop & Score", 34: "DOCK W/L (right)", 35: "SPECIAL",
	36: "100,000 When Lit", 37: "Little Shuttle (insert bd)", 38: "U", 39: "S", 40: "A", 41: "Not Used",
	42: "RELAUNCH WHEN LIT", 43: "DOCKED Port Side", 44: "Hold Bonus", 45: "DOCKED Starboard Side",
	46: "Williams (insert bd, left)", 47: "Williams (insert bd, middle)", 48: "Williams (insert bd, right)",
	49: "Big Flame (insert bd)", 50: "Shuttle Score SPECIAL", 51: "Extra Ball", 52: "50,000 + Re-Entry", 53: "50,000 + Bonus Ball",
	54: "150,000 + Hold Bonus", 55: "75,000", 56: "25,000", 57: "Big Flame (insert bd)", 58: "Station Score SPECIAL",
	59: "Extra Ball", 60: "50,000 + Re-Entry", 61: "50,000 + Bonus Ball", 62: "150,000 + Hold Bonus", 63: "75,000", 64: "25,000",
}
LAMP_LIST_WORDING = {
	1: "Bonus Ball Player #1", 2: "Bonus Ball Player #2", 3: "Bonus Ball Player #3", 4: "Bonus Ball Player #4",
	5: "EXTRA BALL (3-bk Dr Tgt)", 6: "RELEASE (right)", 7: "RELEASE (left)", 8: "DOCK W/L (left)", 9: "CHANGE Shuttle",
	10: "CHANGE Station", 11: "1X", 12: "2X", 13: "4X", 14: "1 (lane)", 15: "2 (lane)", 16: "3 (lane)",
	17: "RE-ENTRY W/LIT (L Drain)", 18: "S (in Shuttle)", 19: "H (in Shuttle)", 20: "U (in Shuttle)", 21: "T (in Shuttle)",
	22: "T (in Shuttle)", 23: "L (in Shuttle)", 24: "E (in Shuttle)", 25: "S (in Station)", 26: "T (in Station)",
	27: "A (in Station)", 28: "T (in Station)", 29: "I (in Station)", 30: "O (In Station)", 31: "N (in Station)",
	32: "RE-ENTRY W/LIT (R Drain)", 33: "STOP & SCORE", 34: "DOCK W/L (right)", 35: "SPECIAL",
	36: "100,000 When Lit (near \"A\" lane)", 37: "Little Shuttle (insert bd)", 38: "U (lane)", 39: "S (lane)", 40: "A (lane)",
	41: "Dome (insert bd)", 42: "RELAUNCH WHEN LIT", 43: "DOCKED PORT SIDE", 44: "HOLD BONUS", 45: "DOCKED STARBOARD SIDE",
	46: "WILLIAMS (insert bd, left)", 47: "WILLIAMS (insert bd, mid)", 48: "WILLIAMS (insert bd, right)",
	49: "Big Flame #1 (insert bd)", 50: "SPECIAL (Shuttle Scores)", 51: "EXTRA BALL (Shuttle Scores)",
	52: "50,000+Re-entry (Sh. Scores)", 53: "50,000+Bon.Ball (Sh. Scores)", 54: "150,000+Hold Bon (Sh. Scores)",
	55: "75,000 (Sh. Scores)", 56: "25,000 (Sh. Scores)", 57: "Big Flame #2 (insert bd)", 58: "SPECIAL (Station Scores)",
	59: "EXTRA BALL (Station Scores)", 60: "50,000+Re-entry (St. Scores)", 61: "50,000+Bon.Ball (St. Scores)",
	62: "150,000+Hold Bon (St. Scores)", 63: "75,000 (St. Scores)", 64: "25,000 (St. Scores)",
}
ROM_LAMP_NAMES = {
	1: "BON BAL PLYR 1", 2: "BON BAL PLYR 2", 3: "BON BAL PLYR 3", 4: "BON BAL PLYR 4", 5: "EXTRA BALL", 6: "RIGHT RELEASE",
	7: "LEFT RELEASE", 8: "DOCKING WL LEFT", 9: "CHANGE SHUTTLE", 10: "CHANGE STATION", 11: "1X BONUS", 12: "2X BONUS",
	13: "4X BONUS", 14: "UPPER LAMP 1", 15: "UPPER LAMP 2", 16: "UPPER LAMP 3", 17: "LEFT DRAIN", 18: "SHUTTLE S",
	19: "SHUTTLE H", 20: "SHUTTLE U", 21: "SHUTTLE 1ST T", 22: "SHUTTLE 2ND T", 23: "SHUTTLE L", 24: "SHUTTLE E",
	25: "STATION S", 26: "STATION 1ST T", 27: "STATION A", 28: "STATION 2ND T", 29: "STATION I", 30: "STATION O",
	31: "STATION N", 32: "RIGHT DRAIN", 33: "STOP  N SCORE", 34: "DOCKING WL RGHT", 35: "SPECIAL", 36: "100 K WHEN LT",
	37: "STATION WHEEL 4", 38: "USA U", 39: "USA S", 40: "USA A", 41: "STATION WHEEL 6", 42: "RELAUN W LIT",
	43: "DOCKED LEFT", 44: "HOLD BONUS", 45: "DOCKED RIGHT", 46: "STATION WHEEL 3", 47: "STATION WHEEL 2",
	48: "STATION WHEEL 1", 49: "FLAME 1", 50: "SH SCOR SPECIAL", 51: "SH SCOR EX BALL", 52: "SH SCOR 50K REN",
	53: "SH SCOR 50K BON", 54: "SH SCOR 150 K", 55: "SH SCOR 75 K", 56: "SH SCOR 25 K", 57: "STATION WHEEL 5",
	58: "ST SCOR SPECIAL", 59: "ST SCOR EX BALL", 60: "ST SCOR 50K REN", 61: "ST SCOR 50K BON", 62: "ST SCOR 150 K",
	63: "ST SCOR 75 K", 64: "ST SCOR 25 K",
}
INSERT_BOARD_LAMPS = frozenset({37, 41, 46, 47, 48, 49, 57})
LAMP_COLUMN_WIRING = {
	1: ("YEL-BRN", "1J7-1", "Q66"), 2: ("YEL-RED", "1J7-2", "Q64"), 3: ("YEL-ORN", "1J7-3", "Q62"),
	4: ("YEL-BLK", "1J7-4", "Q60"), 5: ("YEL-GRN", "1J7-6", "Q58"), 6: ("YEL-BLU", "1J7-7", "Q56"),
	7: ("YEL-VIO", "1J7-8", "Q54"), 8: ("YEL-GRY", "1J7-9", "Q52"),
}
LAMP_ROW_WIRING = {
	1: ("RED-BRN", "1J6-1", "Q80"), 2: ("RED-BLK", "1J6-2", "Q81"), 3: ("RED-ORN", "1J6-3", "Q82"),
	4: ("RED-YEL", "1J6-5", "Q83"), 5: ("RED-GRN", "1J6-6", "Q84"), 6: ("RED-BLU", "1J6-7", "Q85"),
	7: ("RED-VIO", "1J6-8", "Q86"), 8: ("RED-GRY", "1J6-9", "Q87"),
}
INSERT_BOARD_NOTES = {
	37: "On the \"Williams Version\" insert, which the manual documents, this is the controlled lamp behind the little shuttle flame (Lamps list \"Little Shuttle (insert bd)\"); on the \"Wheel Version\", which the ROM's lamp test is written for, it is the fourth of the six station-wheel lamps (\"STATION WHEEL 4\") and the flame lamp is G.I.",
	41: "Both copies of the Lamp-Matrix Table also print \"Not Used\"; the owner's comparison resolves the two pages as the two production insert boards: on the \"Williams Version\" this address is unused, and on the \"Wheel Version\" it is the sixth station-wheel lamp (\"STATION WHEEL 6\"). It is therefore optional: fitted on one production insert board and not the other.",
	46: "On the \"Williams Version\" insert this is the left of three controlled lamps behind the Williams logo; on the \"Wheel Version\" it is the third station-wheel lamp (\"STATION WHEEL 3\") and the logo lamps are G.I.",
	47: "On the \"Williams Version\" insert this is the middle of three controlled lamps behind the Williams logo; on the \"Wheel Version\" it is the second station-wheel lamp (\"STATION WHEEL 2\").",
	48: "On the \"Williams Version\" insert this is the right of three controlled lamps behind the Williams logo; on the \"Wheel Version\" it is the first station-wheel lamp (\"STATION WHEEL 1\").",
	49: "A controlled lamp behind the big shuttle flame on both production insert boards (Lamps list \"Big Flame #1 (insert bd)\", ROM \"FLAME 1\"); the owner reports that it drives the flame's parallel lamp pair on the \"Wheel Version\" and the single lamp near the shuttle engines on the \"Williams Version\".",
	57: "On the \"Williams Version\" insert this is the big shuttle flame's parallel lamp pair (Lamps list \"Big Flame #2 (insert bd)\"); on the \"Wheel Version\" it is the fifth station-wheel lamp (\"STATION WHEEL 5\").",
}

# --- Placements: retained known-working table object centres in VPX units, each the object the script binds to the
# address (literals read once from the retained extraction; the curator never reads the external roots).
VPX_TABLE_SOURCE = "vpx-table.space-station-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.space-station-vpw-1-0"
TABLE_SHA256 = "3d595e21bc52cf39ba2741902526a0bcbce45de101490d24e3127dcefa4d1d25"
EMBEDDED_SCRIPT_SHA256 = "075c55dd8ef256266c58cf6033433f84cef231823704af8136b9414d593cb6ff"
EXTRACTION_RELATIVE_PATH = Path("williams/space-station-1987/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/space-station-1987/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 3313
# SHA-256 of the canonical manifest bytes, so a changed extraction with a refreshed manifest is refused.
EXTRACTION_MANIFEST_SHA256 = "92c42c90f658579a8a731c90a7c05194a4a8c8a78847570a47d6fb76a4baf8ff"
TABLE_BOUNDS = "left=0 top=0 right=952.941 bottom=1976.471"
PLAYFIELD_WIDTH = 952.941
PLAYFIELD_HEIGHT = 1976.471
SPATIAL_SOURCES: tuple[str, ...] = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)

STATION_PIVOT = (742.0278, 222.0325)
SWITCH_OBJECTS = {
	10: ("Kicker sw10", (453.276, 1910.7352)),
	11: ("Kicker sw11", (827.6841, 1691.7074)),
	12: ("Kicker sw12", (713.5172, 1757.248)),
	13: ("Kicker sw13", (595.9039, 1825.585)),
	14: ("Trigger Sw14", (226.0477, 202.9206)),
	15: ("Trigger Sw15", (314.8322, 201.5722)),
	16: ("Trigger Sw16", (402.8745, 201.4872)),
	17: ("Trigger Sw17", (50.9854, 1555.7914)),
	18: ("HitTarget sw18", (98.8882, 1213.3374)),
	19: ("HitTarget sw19", (107.5892, 1162.2026)),
	20: ("HitTarget sw20", (117.0892, 1110.7852)),
	21: ("HitTarget sw21", (125.0479, 1059.5607)),
	22: ("HitTarget sw22", (134.4295, 1006.2736)),
	23: ("HitTarget sw23", (144.0066, 955.4251)),
	24: ("HitTarget sw24", (153.4038, 902.3925)),
	25: ("HitTarget sw25", (344.819, 673.7525)),
	26: ("HitTarget sw26", (382.5602, 707.8217)),
	27: ("HitTarget sw27", (421.7652, 743.039)),
	28: ("HitTarget sw28", (742.9262, 541.4868)),
	29: ("HitTarget sw29", (746.0096, 602.9869)),
	30: ("HitTarget sw30", (748.844, 659.376)),
	31: ("HitTarget sw31", (752.0381, 718.0148)),
	32: ("Trigger Sw32", (820.081, 1527.6824)),
	33: ("Wall sw33 (drag-point mean, the drop target's primary wall)", (761.6714, 984.9103)),
	35: ("HitTarget sw35", (896.8765, 945.517)),
	37: ("Trigger sw37", (99.3809, 243.0763)),
	38: ("Trigger Sw38", (228.3132, 239.5909)),
	39: ("Trigger Sw39", (314.536, 236.3336)),
	40: ("Trigger Sw40", (399.7384, 236.5748)),
	41: ("Trigger sw41", (560.8845, 66.9213)),
	42: ("Trigger sw42", (870.9604, 66.9213)),
	43: ("Trigger Sw43", (895.9338, 1736.843)),
	45: ("Trigger sw45", (899.7704, 383.3958)),
	46: ("Trigger Sw46", (898.5764, 240.2071)),
	47: ("Trigger sw47", (48.1358, 979.5949)),
	48: ("Trigger Sw48", (296.8715, 575.7327)),
	50: ("Wall sw54_rubber (drag-point mean, the upper right 10-point rubber)", (785.4123, 438.7628)),
	54: ("Wall sw50_rubber (drag-point mean, the lower right 10-point rubber)", (747.76, 818.4537)),
	57: ("Wall sw57 (drag-point mean, the drop target's primary wall)", (575.4794, 337.4376)),
	58: ("Wall sw58 (drag-point mean, the drop target's primary wall)", (558.9121, 392.6882)),
	59: ("Wall sw59 (drag-point mean, the drop target's primary wall)", (541.9115, 447.6623)),
	60: ("Bumper Bumper1", (257.1557, 481.8517)),
	61: ("Bumper Bumper2", (440.7689, 402.3231)),
	62: ("Bumper Bumper3", (415.6144, 602.2856)),
	63: ("Wall LeftSlingShot (drag-point mean)", (159.2312, 1476.3517)),
	64: ("Wall RightSlingShot (drag-point mean)", (701.0981, 1477.6619)),
}
SWITCH_PLACEMENT_NOTES = {
	11: "The table models each trough position with its own kicker (sw11-sw13); 11 is nearest the shooter lane.",
	50: (
		"Placed at the upper right 10-point rubber, Wall sw54_rubber, not at the table's sw50_rubber: the table binds 50 to "
		"its lower right rubber (sw50_rubber_Hit, commented \"Lower Right Rubber Switch\") and 54 to its upper right one, "
		"crossed against the manual's Switch-Matrix Table and Switches list (50 \"top right\", 54 \"lwr right\"), its switch "
		"drawing (callout 50 above 54 on the right) and the ROM's names (TOP RGT and LOW RGT 10 PTS). Both score alike, so the "
		"table's crossed binding is a defect with no effect on play; the placement follows the machine."
	),
	54: "Placed at the lower right 10-point rubber, Wall sw50_rubber; see switch 50 for the table's crossed binding.",
	57: "The table puts DT57 at the upper (rearmost) target of the bank and DT59 at the lower, as the manual does.",
	60: "The script pulses 60 from Bumper1, the left bumper.",
	61: "The script pulses 61 from Bumper2, the right (upper) bumper.",
	62: "The script pulses 62 from Bumper3, the lower bumper.",
}
# Sensors with no table object of their own, placed on their own mechanism's object.
SWITCH_PROJECTIONS = {
	52: (STATION_PIVOT, "Projected onto the Space Station's rotation centre (the pivot of Primitive BM_SS_01, which the script turns about its own position): the C-11872 opto board sits on the station's shaft under the playfield, and the script writes 52 from its modelled angle rather than from an object."),
	53: (STATION_PIVOT, "Projected onto the Space Station's rotation centre; see switch 52."),
}
LAMP_LIGHTS = {
	1: (187.9146, 1284.1743), 2: (226.9244, 1328.7628), 3: (266.0331, 1373.3042), 4: (304.3979, 1418.0668),
	5: (592.2615, 460.2586), 6: (632.8182, 334.5731), 7: (101.7205, 517.3269), 8: (144.6908, 638.2637),
	9: (835.2123, 1029.8969), 10: (865.6056, 1056.2751), 11: (560.2708, 1412.8196), 12: (606.6329, 1359.0679),
	13: (653.4142, 1305.5297), 14: (227.3478, 42.6578), 15: (314.968, 31.7441), 16: (405.3603, 31.4734),
	17: (51.1269, 1425.303), 18: (148.9519, 1224.686), 19: (157.6703, 1172.7616), 20: (166.5241, 1120.2839),
	21: (175.5406, 1066.7583), 22: (184.8244, 1013.9649), 23: (194.8401, 961.6246), 24: (203.845, 911.2826),
	25: (308.9261, 707.2208), 26: (349.8463, 742.6595), 27: (388.2111, 779.2701), 28: (691.1523, 544.1229),
	29: (694.8141, 603.1881), 30: (697.7098, 662.3707), 31: (701.6571, 719.5812), 32: (812.5557, 1427.1964),
	33: (736.4441, 1032.436), 34: (688.341, 1128.3094), 35: (801.7134, 1103.8317), 36: (396.1114, 66.5095),
	38: (229.5109, 138.6592), 39: (314.4796, 139.1901), 40: (399.3991, 139.3027), 42: (430.7462, 1579.0793),
	43: (324.8798, 1502.8739), 44: (430.4577, 1467.5283), 45: (536.1508, 1504.0221), 50: (364.7081, 959.775),
	51: (364.8258, 1018.6924), 52: (364.8337, 1077.5151), 53: (365.0844, 1136.3224), 54: (363.9558, 1196.1329),
	55: (364.8334, 1254.5637), 56: (364.3322, 1314.3751), 58: (495.0043, 959.1835), 59: (495.7551, 1017.7432),
	60: (495.7629, 1076.5659), 61: (496.0137, 1135.3732), 62: (494.8851, 1195.1837), 63: (495.7627, 1253.6145),
	64: (495.2614, 1313.4259),
}
# The insert-board lamps' lights sit in a row above the playfield (y = -213.3422), the table's backglass helpers.
PARKED_LAMP_Y = -213.3422
FLASHER_LIGHTS = {
	15: [("f15", (595.7675, -12.5083)), ("f15b", (747.8923, -12.8071)), ("f15c", (898.911, -12.8071))],
	25: [("f25", (393.9281, 1579.4426)), ("f25b", (465.0604, 1579.4426))],
	26: [("f26", (63.9974, 1158.1141)), ("f26b", (94.4718, 989.0109))],
	27: [("f27", (837.2954, 1311.6038)), ("f27b", (787.9332, 618.697))],
	28: [("f28", (64.2009, 38.1716)), ("f28b", (511.4006, 270.283))],
	29: [("f29", (671.0504, -12.7503)), ("f29b", (822.6813, -12.1875))],
}
# The playfield G.I. bulb lights of the script's two collections: GI (white) and gi_green.
GI_LIGHTS = (
	("GI01", (139.4809, 1551.0597)), ("GI02", (94.7743, 1470.9839)), ("GI24", (853.7897, 1274.926)),
	("GI25", (760.0696, 1483.8059)), ("GI26", (694.6755, 1563.8873)), ("GI_003", (49.2693, 1250.4598)),
	("GI_004", (49.6583, 1109.6672)), ("GI_005", (104.4976, 942.4268)), ("GI_006", (45.7689, 763.1296)),
	("GI_007", (47.7136, 681.8429)), ("GI_008", (128.6113, 317.0244)), ("GI_009", (50.4514, 132.2514)),
	("GI_010", (114.9987, 49.4396)), ("GI_011", (185.7842, 238.0712)), ("GI_012", (270.5713, 237.2931)),
	("GI_013", (356.5253, 237.2933)), ("GI_014", (511.0608, 308.2087)), ("GI_015", (561.9097, 186.958)),
	("GI_016", (423.6609, 702.8983)), ("GI_017", (686.6329, 63.7787)), ("GI_018", (442.4166, 238.0613)),
	("GI_019", (917.0471, 228.3535)), ("GI_020", (782.2741, 595.9677)), ("GI_021", (791.2366, 736.7536)),
	("GI_022", (913.5396, 894.3161)), ("GI_023", (913.9822, 1067.8135)),
)
GI_GREEN_LIGHTS = (
	("GI_G_001", (118.3533, 1521.2039)), ("GI_G_002", (100.8201, 1438.2588)), ("GI_G_003", (48.2206, 1211.6766)),
	("GI_G_004", (83.287, 1078.1558)), ("GI_G_005", (127.1199, 866.4078)), ("GI_G_006", (56.9872, 716.0269)),
	("GI_G_007", (34.0592, 645.8937)), ("GI_G_008", (122.3994, 359.6861)), ("GI_G_009", (142.1138, 287.7549)),
	("GI_G_010", (43.009, 219.0209)), ("GI_G_011", (173.0175, 47.4525)), ("GI_G_012", (384.7846, 669.1962)),
	("GI_G_013", (504.9783, 339.794)), ("GI_G_014", (493.1905, 229.0724)), ("GI_G_015", (540.7628, 208.0227)),
	("GI_G_016", (656.9581, 67.6911)), ("GI_G_017", (781.7377, 559.5594)), ("GI_G_018", (790.6085, 703.2589)),
	("GI_G_019", (913.9062, 860.7081)), ("GI_G_020", (912.1318, 1098.4327)), ("GI_G_021", (879.7546, 1227.4961)),
	("GI_G_022", (853.587, 1408.451)), ("GI_G_023", (759.5608, 1453.6897)), ("GI_G_024", (721.4191, 1546.8278)),
	("GI_G_025", (902.269, 194.2174)),
)
KICKBACK = (50.9062, 1640.6409)
# Coils with no table object of their own: (anchor, the part the projection lands on).
SOLENOID_PROJECTIONS = {
	1: (SWITCH_OBJECTS[10][1], "the drain kicker sw10 the script kicks from; the outhole kicker coil has no object of its own"),
	2: (SWITCH_OBJECTS[11][1], "the trough kicker sw11 the script releases from; the C-9638-3 feeder has no object of its own"),
	3: (SWITCH_OBJECTS[41][1], "the left popper's switch trigger sw41, whose ball the script lifts; the D-11335-1 popper coil has no object of its own"),
	4: (SWITCH_OBJECTS[42][1], "the right popper's switch trigger sw42, whose ball the script lifts; the popper coil has no object of its own"),
	6: (SWITCH_OBJECTS[58][1], "the bank's middle drop target sw58; the reset coil sits below the bank and has no object of its own"),
	8: (SWITCH_OBJECTS[33][1], "the single drop target sw33; its reset coil sits below it and has no object of its own"),
	16: (STATION_PIVOT, "the Space Station's rotation centre (the pivot of Primitive BM_SS_01); the motor sits below the station on its shaft"),
	17: (SWITCH_OBJECTS[45][1], "the right lock's switch trigger sw45, whose ball the script kicks; the dock kicker has no object of its own"),
	32: (SWITCH_OBJECTS[47][1], "the left lock's switch trigger sw47, whose ball the script kicks; the kickbig has no object of its own"),
}
SOLENOID_OBJECTS = {
	13: [("Plunger Kickback", KICKBACK)],
	18: [("Wall LeftSlingShot (drag-point mean)", SWITCH_OBJECTS[63][1])],
	19: [("Bumper Bumper2", SWITCH_OBJECTS[61][1])],
	20: [("Wall RightSlingShot (drag-point mean)", SWITCH_OBJECTS[64][1])],
	21: [("Bumper Bumper1", SWITCH_OBJECTS[60][1])],
	22: [("Bumper Bumper3", SWITCH_OBJECTS[62][1])],
}
FLASHER_PLACEMENT_NOTES = {
	15: (
		"Placed at the table's three flasher lights f15, f15b and f15c, which SolMod15 drives: domes on the top panel at the "
		"rear edge of the playfield, interleaved with 29's two (an IPDB upper-playfield photograph shows the five orange domes "
		"in a row behind the Space Station). The lights sit 12.5-12.8 units behind the rear edge (y = -12.51 to -12.81), so "
		"their y is clamped to the edge, where the manual's \"P'fld Top Panel\" puts them."
	),
	25: "Placed at the table's flasher lights f25 and f25b, which SolMod25 drives, either side of the RELAUNCH insert at the bottom centre.",
	26: "Placed at the table's flasher lights f26 and f26b, which SolMod26 drives, on the left side.",
	27: "Placed at the table's flasher lights f27 and f27b, which SolMod27 drives, on the right side.",
	28: "Placed at the table's flasher lights f28 (top left corner) and f28b (upper centre), which SolMod28 drives.",
	29: (
		"Placed at the table's flasher lights f29 and f29b, which SolMod29 drives: two domes on the top panel between 15's "
		"three. The lights sit 12.2-12.8 units behind the rear edge, so their y is clamped to the edge."
	),
}


def _clamped(xy: tuple[float, float]) -> tuple[float, float]:
	return (xy[0], max(0.0, xy[1]))


SWITCH_PLACEMENTS: dict[int, list[tuple[str, tuple[float, float], str]]] = {
	address: [(obj, xy, "observed")] for address, (obj, xy) in SWITCH_OBJECTS.items()
}
SWITCH_PLACEMENTS.update({address: [("projection", xy, "validated")] for address, (xy, _reason) in SWITCH_PROJECTIONS.items()})
SOLENOID_PLACEMENTS: dict[int, list[tuple[str, tuple[float, float], str]]] = {
	address: [("projection", xy, "validated")] for address, (xy, _reason) in SOLENOID_PROJECTIONS.items()
}
SOLENOID_PLACEMENTS.update({address: [(obj, xy, "observed") for obj, xy in objects] for address, objects in SOLENOID_OBJECTS.items()})
SOLENOID_PLACEMENTS.update({address: [(name, _clamped(xy), "observed") for name, xy in lights] for address, lights in FLASHER_LIGHTS.items()})
SOLENOID_PLACEMENTS[9] = [(name, xy, "observed") for name, xy in GI_LIGHTS + GI_GREEN_LIGHTS]
SOLENOID_PLACEMENTS[10] = [(name, xy, "observed") for name, xy in GI_GREEN_LIGHTS]
LAMP_PLACEMENTS: dict[int, list[tuple[str, tuple[float, float], str]]] = {
	address: [(f"Light l{address}", xy, "observed")] for address, xy in LAMP_LIGHTS.items()
}
PLACEMENT_NOTES: dict[tuple[str, int], str] = {}
for _address, (_obj, _xy) in SWITCH_OBJECTS.items():
	PLACEMENT_NOTES[("switch", _address)] = SWITCH_PLACEMENT_NOTES.get(_address, f"Placed at the retained table's {_obj}, which the script binds to this address.")
	if _address in SWITCH_PLACEMENT_NOTES and _address not in (50, 54):
		PLACEMENT_NOTES[("switch", _address)] = f"Placed at the retained table's {_obj}, which the script binds to this address. " + SWITCH_PLACEMENT_NOTES[_address]
for _address, (_xy, _reason) in SWITCH_PROJECTIONS.items():
	PLACEMENT_NOTES[("switch", _address)] = _reason
for _address, (_xy, _reason) in SOLENOID_PROJECTIONS.items():
	PLACEMENT_NOTES[("solenoid", _address)] = f"Placed at a documented projection onto {_reason}."
for _address, _objects in SOLENOID_OBJECTS.items():
	PLACEMENT_NOTES[("solenoid", _address)] = f"Placed at the retained table's {_objects[0][0]}."
PLACEMENT_NOTES.update({("solenoid", address): note for address, note in FLASHER_PLACEMENT_NOTES.items()})
PLACEMENT_NOTES[("solenoid", 9)] = (
	"The placements are the 51 playfield G.I. bulb lights of the retained table's two collections, the 26 white ones (GI) "
	"and the 25 green ones (gi_green), which GIUpdates sets together from this output; a table's G.I. grouping is not the "
	"machine's wiring, so they stay observed and no quantity is asserted."
)
PLACEMENT_NOTES[("solenoid", 10)] = (
	"The placements are the 25 green G.I. bulb lights of the retained table's gi_green collection, the string this relay "
	"selects when energized; they stay observed and no quantity is asserted."
)
for _address in LAMP_LIGHTS:
	PLACEMENT_NOTES[("lamp", _address)] = f"Placed at the retained table's Light l{_address}, which vpmMapLights binds to this lamp through its timer interval {_address}."


def norm(x: float, y: float) -> tuple[float, float]:
	"""Normalize a retained-table coordinate (VPX units) into the canonical playfield space."""
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def placement(identifier: str, role: str, xy: tuple[float, float], status: str, *refs: str) -> dict[str, Any]:
	x, y = norm(*xy)
	return {"id": identifier, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs, status=status)}


def located(identifier: str, role: str, entries: list[tuple[str, tuple[float, float], str]], *refs: str) -> dict[str, Any]:
	placements = [
		placement(f"{identifier}.{role}" + (f".{index}" if len(entries) > 1 else ""), role, xy, status, *refs)
		for index, (_, xy, status) in enumerate(entries, start=1)
	]
	order = {"candidate": 0, "observed": 1, "validated": 2}
	return {"status": min((p["provenance"]["status"] for p in placements), key=order.__getitem__), "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def solenoid_platform_label(address: int) -> str:
	if 33 <= address <= 36:
		return f"Unused Upper Flipper Slot {address}"
	if 37 <= address <= 44:
		return f"Unused Sound Overlay Slot {address}"
	raise KeyError(address)


def output_id(address: int) -> str:
	if address in SOLENOID_LABELS:
		return f"device.{slug(SOLENOID_LABELS[address])}"
	if address in UNUSED_SOLENOIDS:
		return f"device.{slug(UNUSED_SOLENOIDS[address])}"
	if address in VIRTUAL_SOLENOIDS:
		return f"device.{slug(VIRTUAL_SOLENOIDS[address][0])}"
	return f"device.{slug(solenoid_platform_label(address))}"


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def _excerpt(identifier: str, locator: str, filename: str, method: str = "manual", transcribed_by: str = "curator, read from the rendered pages") -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	return {
		"id": identifier, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path),
		"method": method, "transcribed_by": transcribed_by, "reviewed": True,
	}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned PinmameGetGames catalog record for spstn_l5, the only Space Station driver",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c lines 38-41 INITGAMEFULL macro and lines 486-498 INITGAMEFULL(spstn, GEN_S11B, s11_dispS11b1, 12, "
				"FLIP_SWNO(55,56), 0,0,0,0, 0,63,61,64,60,62): sxx.muxSol = 12, hw.display 0, gameSpecific1 0, sxx.ssSw = "
				"{0,63,61,64,60,62}, the spstn_l5 ROM set and CORE_GAMEDEF(spstn,l5); src/wpc/s11.h s11_dispS11b1 = s11_dispS11a, "
				"S11_GAMEONSOL 23 and the diagnostic switch numbers; src/wpc/s11.c s11_dispS11a (two DISP_SEG_7 rows of 16-segment "
				"and two of 7-segment digits), the switch-driven special-solenoid loop (core_getSw(sxx.ssSw[ii]) published at "
				"CORE_FIRSTSSSOL+ii while the enable is on), setSSSol and its WMS ssSolNo table, updsol (the muxSol copy of the low "
				"solenoid byte to 25-32 while 12 is pulsed), pia0cb2_w (S11_GAMEONSOL), pia4a_r returning core_getSwCol without "
				"inversion, SWITCH_UPDATE(s11) and MACHINE_INIT(s11) output sizing with the spstn_ output-type block (9, 10 and 11 as "
				"reverse #44 \"GI output\", 15 and 25-31 as #89 bulbs, commented \"7 muxed flasher outputs (Mux relay is solenoid "
				"#12)\"); src/wpc/core.h CORE_FIRSTSSSOL 17, CORE_SSFLIPENSOL 23, CORE_FIRSTLFLIPSOL 45, CORE_FIRSTSIMSOL 49, "
				"CORE_FIRSTCUSTSOL 51, CORE_FLIPPERSWCOL 11; src/wpc/core.c core_updateSw's FLIP_SWNO copy and synthetic 45-48; "
				"src/wpc/gen.h GEN_S11B (0x100)"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
			"locator": "System 11 sequential switch/lamp matrices, dedicated diagnostic inputs, the Country jumper, the A/C mux alias bank, special solenoids, the sound-overlay range, synthetic flipper outputs and the 81-88 flipper column",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "https://web.archive.org/web/20250119091340id_/https://www.ipdb.org/files/2261/Williams_1987_Space_Station_Operations_Manual_and_Test_Procedures.pdf",
			"original_filename": "Williams_1987_Space_Station_Operations_Manual_and_Test_Procedures.pdf",
			"sha256": MANUAL_SHA256, "acquired_at": "2026-10-23T18:45:00Z", "source_id": "ipdb.2261",
			"locator": (
				"IPDB machine 2261 (Williams Space Station, model 552, manufactured December 7, 1987; machine page "
				"https://www.ipdb.org/machine.cgi?id=2261, read through https://web.archive.org/web/20240420050407id_/https://www.ipdb.org/machine.cgi?id=2261, "
				"resource https://www.ipdb.org/files/2261/Williams_1987_Space_Station_Operations_Manual_and_Test_Procedures.pdf) "
				"downloaded through the Wayback Machine (the capture's SHA-1 matches the CDX digest): the 86-page Williams SPACE "
				"STATION Operations Manual 16-552-101 (January 1988) with Section 3 schematics, 150 dpi image-only scans with no text "
				"layer; a Windows OCR pass was used only to find pages. For Sections 1 and 2 the printed folio \"SPACE STATION n\" is "
				"PDF page n + 4. PDF 2 ROM and Jumper Table and Solenoid Table (reprinted on PDF 32); PDF 6-9 circuit boards, game "
				"controls and operation; PDF 30-36 Test/Diagnostic Procedures (Lamp-Matrix Table reprinted on PDF 31, Switch-Matrix "
				"Table on PDF 34); PDF 40 display board; PDF 47-53 opto positioner, backbox, mechanism and Space Station assemblies; "
				"PDF 54-58 the Switches, Switch-Matrix, Lamp-Matrix, Lamps and Solenoids/Flashers pages with their numbered location "
				"drawings; PDF 60 underside boards; PDF 81-82 the Controlled, Special, and Switched Solenoids fold-out (printed 69); "
				"PDF 85 third copies of both matrix tables."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.space-station.switch-matrix", "PDF page 55 (printed 51), with the copies on PDF 34 and 85, SPACE STATION Switch-Matrix Table and wiring drawing", "switch-matrix.md"),
				_excerpt("excerpt.space-station.lamp-matrix", "PDF page 56 (printed 52), with the copies on PDF 31 and 85, SPACE STATION Lamp-Matrix Table and wiring drawing", "lamp-matrix.md"),
				_excerpt("excerpt.space-station.solenoid-table", "PDF page 2 (no folio), with the copy on PDF 32 (printed 28), SPACE STATION ROM and Jumper Table and Solenoid Table", "solenoid-table.md"),
				_excerpt("excerpt.space-station.switch-locations", "PDF page 54 (printed 50), Switches parts list and drawing callouts", "switch-locations.md"),
				_excerpt("excerpt.space-station.lamp-locations", "PDF page 57 (printed 53), Lamps list and drawing callouts", "lamp-locations.md"),
				_excerpt("excerpt.space-station.solenoid-flasher-locations", "PDF pages 58, 60 and 81-82 (printed 54, 56 and 69), Solenoids/Flashers list, underside boards and the solenoid wiring fold-out", "solenoid-flasher-locations.md"),
				_excerpt("excerpt.space-station.mechanism-assemblies", "PDF pages 38, 47 and 49-53 (printed 34, 43 and 45-49), opto positioner, backbox, mechanism and Space Station assemblies", "mechanism-assemblies.md"),
				_excerpt("excerpt.space-station.diagnostics-and-operation", "PDF pages 1, 3, 6-7, 9, 30-35 and 40 (printed 2-3, 5, 26-31 and 36), boards, game controls, operation, Test/Diagnostic Procedures and the display board", "diagnostics-and-operation.md"),
			],
		},
		{
			"id": AMENDMENT_SOURCE, "kind": "service_bulletin",
			"uri": "https://web.archive.org/web/20250119091314id_/https://www.ipdb.org/files/2261/Williams_1987_Space_Station_Operations_Manual_Amendments_and_Additions.pdf",
			"original_filename": "Williams_1987_Space_Station_Operations_Manual_Amendments_and_Additions.pdf",
			"sha256": AMENDMENT_SHA256, "acquired_at": "2026-10-23T18:46:00Z", "source_id": "ipdb.2261",
			"locator": (
				"IPDB machine 2261 resource https://www.ipdb.org/files/2261/Williams_1987_Space_Station_Operations_Manual_Amendments_and_Additions.pdf "
				"through the Wayback Machine: the two-page Amendments and Additions sheet (date code 011888). Page 1: pen-and-ink "
				"corrections (fuse values, the Special Solenoids (25V) supply wire RED-WHT on printed page 69) and a revised Game "
				"Adjustment Setting Comparison Table; page 2: schematics of the Space Station Opto Positioner board C-11872 and the "
				"3-bank (C-11318-1) and 1-bank (C-11903-L/-R) drop-target opto boards."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": [_excerpt("excerpt.space-station.amendments", "Amendments and Additions, pages 1-2", "amendments.md")],
		},
		{
			"id": ROM_TABLE_SOURCE, "kind": "rom_static_analysis", "uri": "internal:tools/space_station_rom_name_tables.py",
			"sha256": ROM_U27_SHA256,
			"locator": (
				f"The lamp, switch and coil name tables of the spstn_l5 U27 program ROM (sstn_u27.l5, SHA-256 {ROM_U27_SHA256}; "
				f"archive SHA-256 {ROM_ARCHIVE_SHA256}) decoded by tools/space_station_rom_name_tables.py: 14-byte entries, lamp "
				"table at 0x1299, switch table at 0x1619, coil table at 0x19f2. No ROM bytes are reproduced."
			),
			"license": "NOASSERTION", "attribution": "Decoded locally from the user-authorized ROM corpus; ROM bytes remain external",
			"excerpts": [_excerpt(
				"excerpt.space-station.rom-name-tables", "U27 lamp, switch and coil name tables", "rom-name-tables.md", method="mixed",
				transcribed_by="tools/space_station_rom_name_tables.py, checked against the Switch Levels, Single Lamps and Coil Test displays",
			)],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(RUNTIME_EVIDENCE_PATH),
			"locator": (
				"Pinned LibPinMAME runs of spstn_l5, each from a new state directory inheriting only the retained initialization "
				"run's NVRAM: the Coil Test paired step by step with the name the ROM displays, the Single Lamps test stepped through "
				"designators 01-64 with the Credit button, the Switch Levels test over public 1-64 and 81-88, thirteen power-up "
				"probes with switches held from start, two reactive Space Station probes that answer the motor relay with modelled "
				"position patterns, and a gameplay run. Raw runs, manifest and hashes are retained outside the repository."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external",
		},
		{
			"id": VARIANT_SOURCE, "kind": "human_review", "uri": "external:pinmame-review-artifacts/williams.space-station.1987/sources",
			"locator": (
				"Retained captures quoted in excerpt production-variants: the IPDB machine page "
				"(https://web.archive.org/web/20240420050407id_/https://www.ipdb.org/machine.cgi?id=2261, SHA-256 "
				"b506da25c6859d452324fa2594de386543e720e4e4bf2efb91e81216705c57ee), an owner's comparison of the two production "
				"backbox insert boards (https://web.archive.org/web/20260316215711id_/https://jeff-z.com/pinball/spacestation/pics/pics.html, "
				"SHA-256 8aab18f31f8ea422f0eea0bfe2769bd080626b70a2a5ba6b97b5047365cb72df, with four insert-board photographs) and "
				"Steve Loft's 1993 rulesheet (SHA-256 c62036f5007e668f43186b4ae56a76b5419ad43b730ac08872f46d8486597612)."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Machine Database; Jeff-Z.com; Steve Loft", "rights": "NOASSERTION",
			"excerpts": [_excerpt(
				"excerpt.space-station.production-variants", "IPDB notes, the owner's Insert Board Variations section and the rulesheet",
				"production-variants.md", transcribed_by="curator, read from the retained captures",
			)],
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/{quote(SCRIPT_NAME, safe='/')}",
			"revision": VPXTABLE_SCRIPTS_REVISION, "original_filename": SCRIPT_NAME, "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Pinned script-corpus copy of VPW's Space Station table script (5,232 lines; its header credits nFozzy with the "
				"Space Station toy code and iaakki with side-by-side testing against a real machine). Runtime authority: cGameName = "
				"\"spstn_l5\" (line 280), LoadVPM \"03060000\", \"s11.vbs\" (line 320), HandleMechanics = 0 (line 372), "
				"vpmNudge.TiltSwitch = 9 (line 383), the solenoid callbacks (lines 1094-1126), the trough (lines 1178-1219), the "
				"Space Station motor model writing switches 52 and 53 (lines 1222-1330), the switch subs (lines 1665-1739), the "
				"VUK and dock kickers (lines 1752-1880) and the G.I. subs (lines 4616-4697)."
			),
			"license": "NOASSERTION", "attribution": "VPW (Virtual Pinball Workshop) and the contributors credited in the script", "rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads (LoadVPM \"03060000\", \"s11.vbs\", 3.36), retained with "
				f"core.vbs (SHA-256 {VPM_CORE_SHA256}). S11.VBS defines swLRFlip = 82 and swLLFlip = 84 and sets them from the "
				"flipper keys in vpmKeyDown/vpmKeyUp, which the table's key handlers call."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
		},
	] + list(SPATIAL_SOURCE_RECORDS)


SPATIAL_SOURCE_RECORDS: tuple[dict[str, Any], ...] = (
	{
		"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
		"uri": "external:pinmame-vpx-sources/williams/space-station-1987/source/Space%20Station%20(Williams%201987)%20VPW%20v1.0.vpx",
		"original_filename": "Space Station (Williams 1987) VPW v1.0.vpx", "sha256": TABLE_SHA256,
		"locator": (
			"Retained copy of VPW's known-working Space Station recreation, version 1.0, from the contributor's table collection "
			f"(downloaded from VPUniverse). Its embedded script (SHA-256 {EMBEDDED_SCRIPT_SHA256}) is the pinned v1.0.1 script "
			"apart from whitespace and one trailing changelog comment, so its line numbers are the same. Exact playfield bounds "
			f"are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT}. Geometry authority for "
			"script-bound table objects."
		),
		"license": "NOASSERTION", "attribution": "VPW (Virtual Pinball Workshop) and the contributors credited in the script", "rights": "NOASSERTION",
	},
	{
		"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
		"uri": "external:pinmame-vpx-sources/williams/space-station-1987/extracted-vpxtool.manifest.json",
		"sha256": EXTRACTION_MANIFEST_SHA256,
		"locator": (
			f"Retained vpxtool git:v0.33.3 extraction of the retained table, {EXTRACTION_FILE_COUNT} files, with a full sorted "
			f"path/size/SHA-256 manifest whose own SHA-256 is this record's sha256. Bounds are {TABLE_BOUNDS}."
		),
		"license": "NOASSERTION", "attribution": "vpxtool extraction",
	},
)


def _switch_wiring(column: int, row: int) -> dict[str, Any]:
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "System 11B CPU board (D-11883-552)", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "driver_transistor": f"column {drive_component}",
	}


RUNTIME_SWITCH_NOTE = (
	" In the ROM's Switch Levels test (run switch-levels) holding public {address} at 1 makes the player 1 and 2 displays "
	"show the ROM's name for it and the player 3 display its number, so the ROM reads it active at 1. spstnGameData has no "
	"inverted-switch mask and pia4a_r returns core_getSwCol raw, so the contact the matrix sees is open at rest and closed "
	"when actuated."
)
OPTO_NOTE = (
	" The manual identifies it as an optotransistor ({where}): each opto interrupter switches a 2N3906 PNP transistor onto "
	"the matrix row and column, per the amendment sheet's schematic. The matrix sees that transistor, which by the read-path "
	"rule stated below rests open, whatever the beam does."
)
MICROSWITCH_NOTE = (
	" Its 5647-series part is a microswitch: the Ball Trough Switches page labels the 5647-09632-00 and 5647-12073-08 parts "
	"\"MICROSWITCH\" and calls 5647-12073-08 a \"Submin. Switch\"."
)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role) in DEDICATED_LABELS.items():
		items.append(_device(
			f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}], roles=[role], normally_closed=False,
			physical={
				"location": "coin door and CPU board diagnostic switches", "switch_type": "button",
				"notes": (
					"System 11 diagnostic input on the S11_COMINPORT keyboard port. The manual's Game Control Locations and "
					"Test/Diagnostic Procedures drive every test from the coin-door ADVANCE button and AUTO-UP/MANUAL-DOWN "
					"switch, and name the CPU board's SW 2 the CPU Diagnostic switch and its SW 1 the Sound Diagnostic switch. "
					"The retained runs enter and step the tests with -6 and -7."
				),
			},
			spatial=not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		))
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"switch.matrix-{address}"
		unused = address in UNUSED_SWITCHES
		label = f"Not Used (Matrix Position {address})" if unused else SWITCH_LABELS[address]
		physical: dict[str, Any] = {}
		notes = f"Printed switch-matrix column {column} ({SWITCH_COLUMN_WIRING[column][0]}), row {row} ({SWITCH_ROW_WIRING[row][0]})."
		rom_name = ROM_SWITCH_NAMES[address]
		notes += f" The ROM's Switch Levels test names it \"{rom_name}\"." if rom_name else " The ROM's Switch Levels test shows a blank name for it."
		if MATRIX_WORDING[address] != label and address not in UNUSED_SWITCHES:
			notes += f" The Switch-Matrix Table prints \"{MATRIX_WORDING[address]}\"."
		part, description = SWITCH_PARTS[address]
		if description and description != label and description != MATRIX_WORDING[address]:
			notes += f" The Switches parts list prints \"{description}\"."
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_TABLE_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": _switch_wiring(column, row),
		}
		if address in OPTIONAL_SWITCHES:
			notes += (
				" The Switch-Matrix Table prints \"(German Score Board Sw)\" and the Switches parts list \"(German Scoreboard)\" "
				"with no part number: a switch of the scoreboard the West German version carries (the manual cuts jumper W7 for "
				"West German games). The L-5 ROM, the only pinned driver, names the "
				"address \"NOT USED\", so on this firmware nothing reads it; the West German machines' own game ROM is not in "
				"the pinned catalog. No source describes the switch's construction, polarity or location, so it is optional, "
				"without a normally-closed assertion or a placement."
			)
			availability = "optional"
		elif unused:
			if address == 2:
				notes += (
					" The Switch-Matrix Table and the Switches parts list both print \"Not Used\" (no part number). spstnGameData's "
					"gameSpecific1 is 0, so S11_MUXSW2 is unset and PinMAME does not copy the A/C relay into this address; the ROM "
					"still scans it under the platform name \"BALL TILT\", but no switch is fitted."
				)
			elif address == 51:
				notes += (
					" The Switch-Matrix Table and the Switches parts list print \"Not Used\" with no part number, and the manual's "
					"switch drawing has no callout 51. The ROM nevertheless keeps a name for it, \"LEFT 10 PTS\", beside the fitted "
					"\"TOP RGT 10 PTS\" (50) and \"LOW RGT 10 PTS\" (54); a ROM name is not fitment, and the retained script binds "
					"nothing to it."
				)
			else:
				notes += " The Switch-Matrix Table and the Switches parts list print \"Not Used\" and the ROM names it accordingly; no switch is fitted."
			notes += " The Switch Levels test still reports a closure here, so the ROM scans the position."
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE)
			availability = "unused"
		else:
			availability = "used"
			extra["normally_closed"] = False
			if part:
				physical["part_number"] = part.rstrip("*")
				if part.endswith("*"):
					notes += " The parts list marks the part number as a Coinco part number."
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			elif part and part.startswith(MICROSWITCH_PREFIXES):
				physical["switch_type"] = "microswitch"
				notes += MICROSWITCH_NOTE
			if address == 11:
				notes += (
					" The Ball Trough Switches page lists the right trough switch as A-11660 \"Ball Trough Switch, Right\" with a "
					"5647-12073-08 sub-miniature switch, where the Switches list prints 5647-09938-00; both are microswitches."
				)
			if address in (11, 12, 13):
				notes += " The ROM calls 11-13 TROUGH BALL 1-3; 11 sits under the shooter-lane end of the trough, where the feeder (2) kicks."
			if address == 33:
				notes += OPTO_NOTE.format(where="C-11903-R 1-Bank Drop Target Opto Switch Assembly")
				notes += (
					" In the gameplay run the ROM fired the single drop-target reset (8) about 24 s after this address went to 1, at "
					"the end of the Stop 'N' Score timer the target starts, and retried every 1.4 s while it stayed at 1, so public 1 "
					"is the dropped target."
				)
			if address in (57, 58, 59):
				notes += OPTO_NOTE.format(where="C-11318 3-Bank Drop Target Opto Switch Assembly, one opto per target")
				notes += (
					" In the gameplay run the ROM fired the 3-bank reset (6) once all three addresses were held at 1, so public 1 "
					"is a dropped target. The manual's matrix and parts list put 57 at the upper target and 59 at the lower, while "
					"the ROM's names run the other way (\"3 BANK BOTTOM\" at 57, \"3 BANK TOP\" at 59); the ROM scores the three "
					"alike and resets them together, so the order changes no recreation and the labels follow the manual."
				)
			if address in (52, 53):
				notes += OPTO_NOTE.format(where="C-11872 Space Station Opto Positioner board, OPTO 1 and OPTO 2, read through the 03-8106 Wheel Positioner Cam under the playfield")
				notes += (
					" With both position switches open at power-up the ROM energizes the motor relay (16) until (52, 53) changes "
					"into (0, 1), from either modelled direction of rotation (runs station-reactive-ccw and station-reactive-cw), and "
					"gives up after about 5.3 s when nothing changes (runs boot-station-*); see the Space Station mechanism. The "
					"retained script writes it from a modelled station angle rather than from a physical object."
				)
			if address in (60, 61, 62, 63, 64):
				coil = {60: 21, 61: 19, 62: 22, 63: 18, 64: 20}[address]
				notes += (
					f" spstnGameData maps this switch to special solenoid {coil} (sxx.ssSw), so PinMAME raises {coil} while it is "
					"closed and the switched-solenoid enable (23) is on; the Switch Levels and gameplay runs show it."
				)
			if address in (55, 56):
				side = "left" if address == 55 else "right"
				button = 84 if address == 55 else 82
				notes += (
					f" The Lane Change switch (SW-1A-150{'-1' if address == 55 else ''}) is fitted to the {side} cabinet flipper "
					"button and tells the CPU the button is pressed; the button's own SW-10A-48 switch fires the flipper coil "
					"directly. spstnGameData's FLIP_SWNO(55,56) without FLIP_SOL makes core_updateSw rewrite this address from "
					f"PinMAME's flipper column, public {button}, on every update, so a consumer cannot drive it directly: it drives "
					f"{button}, and the Switch Levels test shows \"{rom_name}\" while {button} is held."
				)
			if address == 9:
				notes += (
					" The manual's Game Operation says actuating \"the playfield tilt switch\" loses the ball in play like the third "
					"plumb-bob closure. It is a tilt contact (SW-1A-117), not a ball sensor, so it takes no playfield placement."
				)
			if address in SWITCH_SCRIPT:
				notes += f" Retained script: {SWITCH_SCRIPT[address]}."
				refs = (MANUAL_SOURCE, ROM_TABLE_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			notes += RUNTIME_SWITCH_NOTE.format(address=address)
			if address in CABINET_SWITCH_ROLES:
				extra["roles"] = [CABINET_SWITCH_ROLES[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				if address in (55, 56):
					refs = (MANUAL_SOURCE, ROM_TABLE_SOURCE, RUNTIME_SOURCE, CORE_SOURCE, VPM_LIBRARY_SOURCE)
			elif address in SWITCH_PLACEMENTS:
				entries = SWITCH_PLACEMENTS[address]
				extra["spatial"] = located(identifier, "sensor", entries, *SPATIAL_SOURCES)
				if ("switch", address) in PLACEMENT_NOTES:
					notes += " " + PLACEMENT_NOTES[("switch", address)]
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	column = flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP_SWNO(55,56)",
		core_refs=(CORE_SOURCE, CONTROLLER_SOURCE), button_refs=(VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE),
		button_notes={
			side: (
				f"The retained known-working script drives it: Table1_KeyDown and Table1_KeyUp pass the {side} flipper key to "
				"S11.VBS vpmKeyDown/vpmKeyUp (script lines 1063 and 1086), which set "
				f"Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'}. In the Switch Levels run holding this address showed "
				f"\"{'LEFT FLIPPER' if side == 'left' else 'RIGHT FLIPPER'}\" with the number {55 if side == 'left' else 56} and "
				f"raised the synthetic outputs {'47 and 48' if side == 'left' else '45 and 46'}. The physical counterpart is the "
				f"{side} cabinet flipper button (SW-10A-48), which fires the flipper coil through the flipper circuit and carries "
				f"the Lane Change switch {55 if side == 'left' else 56}."
			)
			for side in ("left", "right")
		},
		unused_notes=vpm_staged_flipper_notes(), unused_note_refs=(VPM_LIBRARY_SOURCE,),
	)
	for item in column:
		if item["availability"] == "used":
			item["normally_closed"] = False
	items.extend(column)
	items.append(_device(
		"switch.dip-0", "Country Jumper (USA/Germany)", "dip_switch", "pinmame.input.dip", 0, "used",
		(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
		aliases=[{"namespace": "pinmame.dip", "value": "0"}],
		physical={
			"location": "System 11B CPU board (D-11883-552)", "switch_type": "dip",
			"notes": (
				"System 11's single Country jumper, read via core_getDip(0)<<7 on PIA2 PA7 (pinned s11.c labels it \"Jumper W7\"). "
				"The manual's ROM and Jumper Table lists the CPU board's installed jumpers (W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and "
				"19), and its Circuit Boards text says \"(Jumper W7 is cut/removed for West German games.)\""
			),
		},
		spatial=not_applicable("dip_switch", MANUAL_SOURCE),
	))
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	pair_of = {a: pair for pair, (a, c, *_rest) in AC_PAIRS.items() for a in (a, c)}
	for address in list(range(1, 23)) + list(range(25, 33)):
		number = SOLENOID_MANUAL_NUMBER[address]
		unused = address in UNUSED_SOLENOIDS
		identifier = output_id(address)
		label = UNUSED_SOLENOIDS[address] if unused else SOLENOID_LABELS[address]
		kind = "coil" if unused else SOLENOID_KIND[address]
		notes = f"Solenoid Table entry {number} (\"{SOLENOID_TABLE_WORDING[address]}\")"
		if LIST_WORDING[address] != SOLENOID_TABLE_WORDING[address]:
			notes += f"; the Solenoids/Flashers list prints \"{LIST_WORDING[address]}\""
		notes += "."
		if address in pair_of:
			pair = pair_of[address]
			a_side, c_side, cpu, playfield, driver, cpu_wire = AC_PAIRS[pair]
			notes += (
				f" Switched pair {pair:02d}A/{pair:02d}C on driver {driver}: the \"A\" load is pulsed with the A/C Select Relay "
				f"(12) de-energized and the \"C\" load with it energized (the table's note 3). Pinned updsol publishes the A load "
				f"at {a_side} and the C load at {c_side}."
			)
			wiring: dict[str, Any] = {
				"board": "System 11B CPU board (D-11883-552) through the D-11813 Aux Power Driver Board", "driver_transistor": driver,
				"drive_wire": SOLENOID_WIRE[address], "control_connection": cpu if address == a_side else f"{cpu} (C side, through the A/C Select Relay)",
				"drive_connection": playfield,
			}
			if address == c_side:
				wiring["control_wire"] = cpu_wire
		else:
			cpu, playfield, driver = CONTROLLED[address]
			kind_word = "Controlled" if address <= 16 else f"Special #{address - 16}"
			notes += f" Solenoid Type \"{kind_word}\"."
			wiring = {
				"board": "System 11B CPU board (D-11883-552)", "driver_transistor": driver, "drive_wire": SOLENOID_WIRE[address],
				"control_connection": cpu, "drive_connection": playfield,
			}
		if address in NOMINAL_VOLTAGE:
			wiring["nominal_voltage_v"] = NOMINAL_VOLTAGE[address]
			wiring["voltage_type"] = "dc"
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_TABLE_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if unused:
			notes += (
				" The Solenoid Table and the Solenoids/Flashers list print \"Not Used\" with no part number, and the wiring "
				+ ("fold-out draws the drive with a \"Not Used\" box." if address == 5 else "fold-out draws no load for it.")
				+ " The driver transistor is still fitted, as on every System 11B board, but no load is connected. The ROM's Coil "
				"Test skips this address (its coil table has no entry for it)"
				+ (
					", and no power-up, service or gameplay run published it."
					if address == 5 else
					". The only state any run published here is the 50-60 ms pulse that every controlled output (9-16) shows "
					"together about 0.27 s after power-up, before the ROM's initialization settles PIA0 port B; it is a property "
					"of the port, not a drive of this address."
				)
			)
			physical: dict[str, Any] = {"notes": notes}
			items.append(_device(
				identifier, label, kind, "pinmame.output.solenoid", address, "unused", refs,
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": number}],
				physical=physical, wiring=wiring, spatial=not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE),
			))
			continue
		step = COIL_TEST_ORDER.index(address) + 1
		notes += (
			f" The ROM's Coil Test (run coil-test) pulses this address at step {step} of {len(COIL_TEST_ORDER)} while the player 1 "
			f"and 2 displays show \"{ROM_COIL_NAMES[address]}\"."
		)
		if address in NOMINAL_VOLTAGE:
			notes += f" The wiring fold-out (printed page 69) draws it in a {NOMINAL_VOLTAGE[address]} V frame."
		if 17 <= address <= 22:
			switch = SPECIAL_SWITCHES[address]
			if switch:
				notes += (
					f" Special #{address - 16}: spstnGameData maps switch {switch} to it (sxx.ssSw), so PinMAME publishes it while "
					f"switch {switch} is closed and the switched-solenoid enable (23) is on, as the physical special-solenoid "
					"circuit fires the coil from its own switch."
				)
			else:
				notes += (
					" Special #1 has no switch in spstnGameData (sxx.ssSw entry 0), so PinMAME publishes it only when the ROM drives "
					"its PIA line itself (setSSSol, WMS ssSolNo order), which the Coil Test and the power-up ball search show."
				)
		if address in SOLENOID_RUNTIME:
			notes += " " + SOLENOID_RUNTIME[address]
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
			refs = (MANUAL_SOURCE, ROM_TABLE_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		else:
			notes += " The retained script has no callback for this address."
		physical = {"part_number": SOLENOID_PART[address]}
		if address in FLASHLAMP_QUANTITY:
			backbox, playfield_count = FLASHLAMP_QUANTITY[address]
			physical["quantity"] = backbox + playfield_count
		extra_roles: list[str] = []
		spatial: dict[str, Any] | None = None
		if address == 7:
			notes += (
				" The knocker is in the backbox: the Backbox Parts Listing (printed page 43) has item 2 \"B-10686-2 Knocker "
				"Assembly\", and the ROM names the step \"INSERT KNOCKER\"."
			)
			extra_roles = ["cabinet.knocker"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 12:
			notes += (
				" The A/C select relay (5580-09555-01, the table's note 5: \"mounted on Aux Power Driver Bd, D-11813 in the "
				"backbox\"). Pinned PinMAME publishes its own state here and, while it is pulsed, moves the low solenoid byte to "
				"25-32. spstnGameData does not set S11_MUXSW2, so no switch mirrors it."
			)
			extra_roles = ["internal.ac-select-relay"]
			spatial = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 9:
			notes += (
				" The relay (5580-09555-01 on a C-11998-1 relay board under the playfield, the table's note 4) switches the "
				"playfield's white general illumination. Energized means G.I. off: the ROM holds it through a tilt, and pinned "
				"PinMAME types it as a reverse-acting #44 \"GI output\", so its modulated state is the brightness of the string the "
				"released relay feeds. The manual prints no G.I. bulb count or layout."
			)
			extra_roles = ["gi.playfield"]
		elif address == 10:
			notes += (
				" The relay (5580-09555-01 on a second C-11998-1 relay board under the playfield) switches the playfield G.I. "
				"between its white bulbs and a second string of green bulbs: IPDB's \"Double GI - General Lighting changes from "
				"white to green during multiball\" and an owner's \"secondary GI circuit of green bulbs that comes on during "
				"multiball\". The ROM energized it at multiball (see the gameplay run above), so energized is green. Pinned PinMAME "
				"types it as a reverse-acting #44 \"GI output\", and the retained script sets UseVPMModSol = 2 (line 313), so its "
				"GiSelect receives the modelled brightness of the string the released relay feeds: it reads on, and shows the "
				"white light maps, while the relay is released."
			)
			extra_roles = ["gi.playfield"]
		elif address == 11:
			notes += (
				" The relay (5580-09555-01 on a C-11998-1 relay board, the table's note 4; the wiring fold-out labels it \"RELAY "
				"BOARD: INSERT BD, GEN'L ILLUM\" and its drive 6P3-5 is a backbox connector) switches the backbox insert board's "
				"general illumination, which lights the translite. Energized means G.I. off, as for 9."
			)
			extra_roles = ["gi.backbox"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 16:
			notes += (
				" The output energizes a relay (5580-12145-01 on the C-11902-1 relay board under the playfield, note 6) that "
				"switches the 14-7941-2 Space Station motor (24 VAC, 11 rpm), which turns the Rotating Ball Guide; the motor runs "
				"in one direction only and the ROM reads the station's position from the opto positioner (52, 53). See the Space "
				"Station mechanism."
			)
		elif address == 30:
			notes += (
				" The Solenoid Table prints 4b: all four #89 bulbs are in the backbox, behind the translite's shuttle flame and the "
				"\"TI\" of SPACE STATION. The retained script lights a backbox flasher (f30)."
			)
			extra_roles = ["cabinet.backbox-flasher"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 31:
			notes += (
				" The Solenoid Table prints 2b: both #89 bulbs are in the backbox, behind the translite's space station. The "
				"retained script lights a backbox flasher (f31)."
			)
			extra_roles = ["cabinet.backbox-flasher"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif 25 <= address <= 29:
			letters = {25: "ON", 26: "SP", 27: "AC", 28: "ES", 29: "TA"}[address]
			notes += (
				f" The Solenoid Table prints 2b,2p: two #89 bulbs in the backbox behind the \"{letters}\" of the translite's SPACE "
				"STATION and two on the playfield. Only the playfield pair takes placements."
			)
		elif address == 15:
			notes += (
				" The Solenoid Table prints \"#1251 flashlamps 3b\" with note 6: three #1251 lamps switched through a relay on the "
				"C-11902-1 relay board, the retained script's \"x3 pf - 28v Lamps\". PinMAME types the output as a #89 bulb."
			)
		if address in SOLENOID_PLACEMENTS and spatial is None:
			role = "emitter" if kind in ("flasher", "gi", "lamp") else "effect"
			spatial = located(identifier, role, SOLENOID_PLACEMENTS[address], *SPATIAL_SOURCES)
			if ("solenoid", address) in PLACEMENT_NOTES:
				notes += " " + PLACEMENT_NOTES[("solenoid", address)]
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": number}]
		if 17 <= address <= 22:
			aliases.append({"namespace": "manual.special-solenoid", "value": f"Special #{address - 16}"})
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		if extra_roles:
			extra["roles"] = extra_roles
		if spatial is not None:
			extra["spatial"] = spatial
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
	for address in (23, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
		if address in VIRTUAL_SOLENOIDS:
			label, availability, role, notes = VIRTUAL_SOLENOIDS[address]
		elif address <= 36:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", UPPER_FLIPPER_NOTE
		else:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", OVERLAY_NOTE
		refs = (CONTROLLER_SOURCE, CORE_SOURCE)
		if availability == "used":
			refs = (CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE) if address == 23 else (CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE)
		items.append(_device(
			output_id(address), label, "virtual", "pinmame.output.solenoid", address, availability, refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}], roles=[role], physical={"notes": notes},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"lamp.matrix-{address}"
		wiring = {
			"board": "System 11B CPU board (D-11883-552)",
			"drive_wire": LAMP_COLUMN_WIRING[column][0], "drive_connection": LAMP_COLUMN_WIRING[column][1],
			"return_wire": LAMP_ROW_WIRING[row][0], "return_connection": LAMP_ROW_WIRING[row][1],
			"driver_transistor": f"column {LAMP_COLUMN_WIRING[column][2]}, row {LAMP_ROW_WIRING[row][2]}",
		}
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		label = LAMP_LABELS[address]
		notes = (
			f"Printed lamp-matrix column {column}, row {row}. In the Single Lamps test (run single-lamps) designator {address:02d} "
			f"blinks this address while the player 1 and 2 displays show \"{ROM_LAMP_NAMES[address]}\"."
		)
		if LAMP_LIST_WORDING[address] != label:
			notes += f" The Lamps list prints \"{LAMP_LIST_WORDING[address]}\""
			notes += f" and the Lamp-Matrix Table \"{LAMP_MATRIX_WORDING[address]}\"." if LAMP_MATRIX_WORDING[address] != LAMP_LIST_WORDING[address] else "."
		physical: dict[str, Any] = {}
		refs = (MANUAL_SOURCE, ROM_TABLE_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		availability = "used"
		extra: dict[str, Any] = {}
		if address in INSERT_BOARD_LAMPS:
			notes += (
				" A lamp on the backbox insert board, behind the translite; the lamp drawing has no callout for it. " + INSERT_BOARD_NOTES[address]
				+ " Both production insert boards run the same L-5 ROM (excerpt production-variants)."
			)
			refs = (MANUAL_SOURCE, ROM_TABLE_SOURCE, RUNTIME_SOURCE, VARIANT_SOURCE, CORE_SOURCE)
			extra["roles"] = ["cabinet.backglass-indicator"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VARIANT_SOURCE)
			if address == 41:
				availability = "optional"
		else:
			if address in (14, 15, 16):
				notes += " A lamp of the 1-2-3 mini-playfield (R-11780); the ROM calls 14-16 UPPER LAMP 1-3."
			if address in (50, 51, 52, 53, 54, 55, 56):
				notes += " One of the seven Shuttle Score award inserts, drawn together under the lamp drawing's \"50-56\" callout."
			if address in (58, 59, 60, 61, 62, 63, 64):
				notes += " One of the seven Station Score award inserts, drawn together under the lamp drawing's \"58 64\" callout."
			if address in LAMP_PLACEMENTS:
				extra["spatial"] = located(identifier, "emitter", LAMP_PLACEMENTS[address], *SPATIAL_SOURCES)
				if ("lamp", address) in PLACEMENT_NOTES:
					notes += " " + PLACEMENT_NOTES[("lamp", address)]
		physical["notes"] = notes
		items.append(_device(
			identifier, label, "lamp", "pinmame.output.lamp", address, availability, refs,
			aliases=aliases, wiring=wiring, physical=physical, **extra,
		))
	return items


def displays() -> list[dict[str, Any]]:
	def display(identifier: str, label: str, index: int, start: int) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": "segment", "controller_index": index, "segment_start": start,
			"width": 7, "height": 1, "physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		}

	return [
		display("display.player-1", "Player 1 score, seven 16-segment alphanumeric characters (DSPY1, 5670-10873-00, on the D-11609 display board)", 0, 1),
		display("display.player-2", "Player 2 score, seven 16-segment alphanumeric characters (DSPY2, 5670-10873-00, on the D-11609 display board)", 1, 9),
		display("display.player-3", "Player 3 score, seven 7-segment digits (DSPY3, 5670-09439-00, on the D-11609 display board)", 2, 21),
		display("display.player-4", "Player 4 score, seven 7-segment digits (DSPY4, 5670-09439-00, on the D-11609 display board)", 3, 29),
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly:
			record["assembly_part_number"] = assembly
		return record

	m = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	v = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, VARIANT_SOURCE, CORE_SOURCE)
	return [
		mechanism(
			"mechanism.trough", "Outhole, three-ball trough and shooter-lane feeder", "kicker", [output_id(1), output_id(2)],
			["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13", "switch.matrix-43"],
			"A drained ball rolls onto the outhole switch (10, 17-1067) and the Outhole Kicker (1, AE-23-800) kicks it into the "
			"trough, where up to three balls queue on Ball Trough #3 (13, left), #2 (12) and #1 (11, right; the ROM's TROUGH BALL "
			"1-3). The Ball Shooter Lane Feeder (2, C-9638-3 with an AE-23-800 coil) kicks the lead ball into the shooter lane, "
			"whose switch (43, the ROM's PLUNGER) the ball rests on until plunged; a wire habitrail carries the plunged ball to the "
			"1-2-3 mini-playfield. With 10 held from power-up the ROM fired the outhole kicker every 2.2 s; in the gameplay run it "
			"fed the first ball at Start and repeated the feed 2.1 s later until a trough switch opened, served a new ball for "
			"each ball docked in a lock, and kicked the outhole 0.6 s after the drain. With no ball in the trough at power-up the "
			"ROM runs a ball search through 17, 32, 4 and 3; in play it searches through 3, 4, 13, 1, 8, 2 and the docks. The "
			"retained script models the trough with kickers sw10-sw13 and a cascade timer.",
			*m, assembly="C-9638-3",
		),
		mechanism(
			"mechanism.mini-playfield", "1-2-3 mini-playfield and U-S-A lanes", "other", [],
			["switch.matrix-14", "switch.matrix-15", "switch.matrix-16", "switch.matrix-38", "switch.matrix-39", "switch.matrix-40", "switch.matrix-37"],
			"A raised translucent-blue mini-playfield (R-11780, 03-8109) at the top left takes the plunged ball and the ball the "
			"right popper lifts. Its three lanes 1 (14), 2 (15) and 3 (16) (5647-12073-01 switches on the A-11991 Switch & Diode "
			"Assy, lamps 14-16, the ROM's ROLOVER and UPPER LAMP 1-3) feed past two ball gates (B-11861, B-11788) onto the main "
			"playfield. Three lanes U (38), S (39) and A (40) run underneath it, reached by the shot round the left and back of the "
			"playfield past the Top Left Roll-Under (37); completing U-S-A advances the Stop 'N' Score multiplier and 1-2-3 the jet "
			"bumper value (rulesheet). IPDB pictures an opaque black prototype mini-playfield with leaf switches.",
			*v, assembly="R-11780",
		),
		mechanism(
			"mechanism.space-station", "Space Station rotating ball guide", "motorized", [output_id(16)], ["switch.matrix-52", "switch.matrix-53"],
			"The Space Station Wheel (03-8123) and the Rotating Ball Guide (03-8107) sit above the playfield at the top right on a "
			"shaft turned by the 14-7941-2 motor (24 VAC, 11 rpm) below it. Controlled solenoid 16 energizes the relay on the "
			"C-11902-1 relay board that runs the motor, in one direction only; the Wheel Positioner Cam (03-8106) on the shaft "
			"interrupts the two optos of the C-11872 Opto Positioner Board (OPTO 1 and OPTO 2), read as Space Station #1 (52) and "
			"#2 (53). The guide sends a ball arriving from the right ramp (through 46 on the station exit ramp) or lifted by the "
			"left popper (41, solenoid 3) to the right lock (45) or, over the wire ramp past 48, to the left lock (47). Per the "
			"rulesheet the ROM turns the station so that a ramp shot goes to an empty lock, and holds a ball in the left popper "
			"while it turns the station when one ball is already locked. At power-up the ROM energizes 16 and stops it on the "
			"edge into (52 open, 53 closed), whether the modelled cam reached it through (1,0) and (1,1) or straight from (0,0), "
			"and gives up after about 5.3 s when the switches never change; in the gameplay run, with both switches held open, it "
			"kept the motor running from Start until both locks emptied 90 s later. The physical cam profile is not printed. The "
			"retained known-working script, tested side by side with a real machine, models one revolution as two half-turn "
			"opto bits in quadrature (52 closed from 180 to 360 degrees, 53 closed from 90 to 270, starting at 90) with the guide "
			"sending balls left at 0 and 180 degrees and right at 90 and 270; a recreation that answers the ROM with that pattern "
			"satisfies the power-up homing seen here.",
			MANUAL_SOURCE, AMENDMENT_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, VARIANT_SOURCE, CORE_SOURCE,
			assembly="C-11872 with 14-7941-2 and C-11902-1",
		),
		mechanism(
			"mechanism.ball-poppers", "Left (centre) and right ball poppers", "kicker", [output_id(3), output_id(4)],
			["switch.matrix-41", "switch.matrix-42"],
			"Two D-11335-1 Ball Popper Assemblies (vertical up-kickers) under the top of the playfield. The left popper (41, "
			"SW-1A-167, kicked by 3 with an AE-24-900 coil), which the rulesheet calls the centre popper, takes the shot round the "
			"left and back past the U-S-A lanes and lifts the ball to the Space Station, which guides it to a lock; it awards "
			"100,000 when lit (lamp 36) and starts multiball with two balls locked. The right popper (42, kicked by 4, AE-23-800), "
			"reached past the drop targets, lifts the ball to the mini-playfield. In the gameplay run the ROM fired 4 0.45 s after "
			"42 closed, and with 41 held while both locks were full it started multiball (\"PILOT ONE ... LAUNCH PROBES\") before "
			"lifting the ball. With both popper switches held from power-up it fired each every 2.2 s. An owner reports an "
			"artwork hole in front of a popper for a prototype drop target, which IPDB pictures.",
			*v, assembly="D-11335-1",
		),
		mechanism(
			"mechanism.docks", "Left and right locks (docks)", "kicker", [output_id(17), output_id(32)],
			["switch.matrix-45", "switch.matrix-46", "switch.matrix-47", "switch.matrix-48"],
			"Two ball locks the game calls docks. The right lock (45, the ROM's RIGHT LOCK UP) is kicked out by the Right Dock "
			"Kickback (17, Special #1, AE-23-800), which the Maintenance Information describes as the Right Eject Hole device using "
			"the shooter-lane feeder's mechanism; its entry switch (46, SW-1A-164) sits on the station exit ramp. The left lock "
			"(47, the ROM's LEFT LOCK UP) is kicked out by the Left Dock Kickbig (32, switched 08C, the B-11051-R Kickbig Arm "
			"Assembly with an AE-23-800 coil), and its entry switch (48) sits on the wire ramp. Docking W/L lamps 8 (left) and 34 "
			"(right) show which dock holds a ball; Docked Port Side (43) and Docked Starboard Side (45) light for a docked ball. In "
			"the gameplay run docking the right lock showed DOCKED RIGHT and the left DOCKED LEFT, each served a new ball, and the "
			"multiball release kicked the docks. At power-up the ROM kicks each once in its ball search; with 47 held it kept "
			"kicking 32 every 2.1 s, while with 45 held it kicked 17 only once more.",
			*m, assembly="B-11051-R",
		),
		mechanism(
			"mechanism.ramp-and-single-drop", "Right ramp and its single drop target (Stop 'N' Score)", "drop_target_bank", [output_id(8)],
			["switch.matrix-33", "switch.matrix-46"],
			"A ramp on the right of the playfield carries the ball up to the Space Station; a single drop target (C-11212-2 "
			"Single-Bank Drop Target Assembly, C-11903-R opto board, switch 33) stands in front of its entrance and is raised by "
			"the Right Single Drop Target Reset (8, AE-23-800). Knocking it down starts Stop 'N' Score; a ramp shot before the "
			"timer runs out scores the counting value (lamp 33 STOP 'N' SCORE). In the gameplay run the ROM raised the target "
			"about 24 s after it went down and retried every 1.4 s while it stayed down. Owners report clear and black ramps; the "
			"production ramp is black.",
			*v, assembly="C-11212-2 with C-11903-R",
		),
		mechanism(
			"mechanism.three-bank", "3-bank drop targets", "drop_target_bank", [output_id(6)],
			["switch.matrix-57", "switch.matrix-58", "switch.matrix-59"],
			"Three drop targets (C-11223-1, 03-8036 blades) sensed by the optos of a C-11318 opto switch assembly and reset together "
			"by the AE-26-1200 coil (6). Completing the bank advances the end-of-ball bonus multiplier (lamps 11-13 1X/2X/4X; the "
			"gameplay run showed 2X BONUS) and, at the adjusted multiplier, lights Extra Ball (lamp 5). In the gameplay run the "
			"ROM fired the reset once all three were held down and once more 1.3 s later.",
			*m, assembly="C-11223-1 with C-11318",
		),
		mechanism(
			"mechanism.kickback", "Left re-entry kickback", "kicker", [output_id(13)], ["switch.matrix-17"],
			"A bell-armature kicker (B-11873-1, AE-24-900 coil, solenoid 13) at the left drain lane (17), the left outlane of a "
			"machine with no inlanes, returns a draining ball to play while lamp 17 RE-ENTRY W/LIT is lit (lit at the start of a "
			"ball at the factory setting). In the gameplay run the ROM fired it within one poll of 17 closing. Lamp 32 RE-ENTRY "
			"W/LIT marks the right drain lane (32), which has no kicker. The retained script fires a VPX Kickback object.",
			*m, assembly="B-11873-1",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other", [output_id(21), output_id(19), output_id(22)],
			["switch.matrix-60", "switch.matrix-61", "switch.matrix-62"],
			"Three jet bumpers (B-9414 above, B-9415-1 coil assemblies below, SW-11A-35 skirt switches): Left (21, switch 60), "
			"Right (19, switch 61) and Lower (22, switch 62). They are special solenoids whose circuits fire the coil from the "
			"bumper's own switch; spstnGameData mirrors that in PinMAME through sxx.ssSw, so each coil address rises with its "
			"switch while 23 is on. The wiring fold-out calls 21 the CENTER JET BUMPER.",
			*m, assembly="B-9414 with B-9415-1",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other", [output_id(18), output_id(20)], ["switch.matrix-63", "switch.matrix-64"],
			"Two kicker arm assemblies (B-9463, AE-26-1200 coils) above the flippers: Left (18, scoring switch 63) and Right (20, "
			"scoring switch 64). The Switches list footnote gives each a separate Kicker Actuating Switch (A-4834-H; B-8734 w/RC) "
			"with no matrix address. As special solenoids, each rises with its scoring switch through sxx.ssSw.",
			*m, assembly="B-9463",
		),
		mechanism(
			"mechanism.flippers", "Two flippers, cabinet-wired", "other", [], ["switch.matrix-55", "switch.matrix-56"],
			"Two lower flippers (C-11626-R-4 and -L-4, FL-11630-50VDC coils). The cabinet buttons (SW-10A-48) fire the coils "
			"through the flipper circuit, so no Sol. No. or driver is printed for them and PinMAME fabricates 45-48 from the "
			"buttons at public 82 and 84. Each button also closes a Lane Change switch (55 left, 56 right) for the CPU, which "
			"core_updateSw copies from 84 and 82; the end-of-stroke switches in the coil circuit have no matrix address.",
			*m, assembly="C-11626-R-4 with C-11626-L-4",
		),
		mechanism(
			"mechanism.targets-and-lanes", "SHUTTLE and STATION standups, Change target and 10-point switches", "other", [],
			[f"switch.matrix-{address}" for address in range(18, 32)] + ["switch.matrix-35", "switch.matrix-50", "switch.matrix-54"],
			"Seven B-11696-5 standups on the left spell SHUTTLE (18-24, lamps 18-24), three in the centre and four on the right spell "
			"STATION (25-31, lamps 25-31), and the B-11696-8 CHANGE bullseye target (35) changes the randomised SHUTTLE or STATION "
			"award shown on the two ladders of seven inserts in the middle of the playfield (lamps 50-56 and 58-64, with Change "
			"Shuttle 9 and Change Station 10). Two B-4834-K-1 10-point rubber switches sit at the top right (50) and lower right "
			"(54).",
			*m,
		),
		mechanism(
			"mechanism.general-illumination", "White, green and insert-board G.I. relays", "other", [output_id(9), output_id(10), output_id(11)], [],
			"Three relays (5580-09555-01 on C-11998-1 relay boards) switch the general illumination: 9 the playfield's white G.I., "
			"10 between the white string and a second string of green bulbs, and 11 the backbox insert board's G.I. Energizing 9 "
			"or 11 turns its G.I. off (the ROM holds both through a tilt) and energizing 10 selects green, which the ROM does "
			"during multiball. PinMAME types all three as reverse-acting AC G.I. outputs.",
			MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, VARIANT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.ac-select", "A/C solenoid select relay", "other", [output_id(12)], [],
			"The A/C Select Relay (12) on the D-11813 Aux Power Driver Board switches each of the eight switched drivers "
			"(Q22-Q25, Q30-Q33) between its \"A\" load, while it is released, and its \"C\" load, while it is energized. Pinned "
			"PinMAME publishes the C loads separately at 25-32.",
			MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other", [output_id(7)], [],
			"The A-side load of pair 07 (7, AE-26-1200) raps the B-10686-2 Knocker Assembly in the backbox; the table allows a "
			"ticket dispenser in its place.",
			MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	items = []
	for coil, switch in sorted(SPECIAL_SWITCHES.items()):
		if not switch:
			continue
		items.append({
			"id": f"relationship.switch-{switch}-fires-special-{coil}", "kind": "direct",
			"source": f"switch.matrix-{switch}", "destination": output_id(coil),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		})
	return items + flipper_column_relationships(flip_swno=FLIP_SWNO, matrix_ids={55: "switch.matrix-55", 56: "switch.matrix-56"}, refs=(CORE_SOURCE, RUNTIME_SOURCE))


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items = []
	for driver_id in DRIVER_IDS:
		record = by_id[driver_id]
		item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		items.append(item)
	return items


COVERAGE_MISSING = ["spatial_placement"]


def build_base() -> dict[str, Any]:
	machine: dict[str, Any] = {
		"id": MACHINE_ID, "name": "Space Station", "manufacturer": "Williams", "year": 1987, "kind": "physical_pinball",
		"model_number": "552", "ipdb_id": 2261, "opdb_id": "G5QXO-MQowd",
	}
	machine.update(PLAYFIELD_RECORD)
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": machine,
		"coverage": {
			"status": STATUS,
			"missing": COVERAGE_MISSING,
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
				"physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated",
				"recreation_knowledge": "validated", "display_inventory": "validated", "spatial_placement": SPATIAL_DIMENSION,
			},
		},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": [],
	}
	apply_legacy_aliases(definition)
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Space Station device identifiers are not unique: {duplicates}")
	return definition


PLAYFIELD_RECORD: dict[str, Any] = {"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE)}}
SPATIAL_DIMENSION = "observed"


def apply_legacy_aliases(definition: dict[str, Any]) -> None:
	"""Carry the legacy import's numeric, zero-padded and named aliases by binding, while compatibility needs them."""
	legacy = load_json(LEGACY_ALIAS_SEED_PATH)["aliases"]
	devices = {(device["binding"]["group"], str(device["binding"]["device"])): device for device in definition["inputs"] + definition["outputs"]}
	for group, addresses in legacy.items():
		for address, aliases in addresses.items():
			device = devices.get((group, address))
			if device is None:
				raise RuntimeError(f"legacy alias target {group} {address} is not in the Space Station definition")
			device["aliases"] = list(device.get("aliases", [])) + [{"namespace": namespace, "value": value} for namespace, value in aliases]


def build() -> dict[str, Any]:
	return build_base()


SPATIAL_BLOCKERS = [
	"Switch 34 (West German scoreboard switch): fitted only on West German machines, and no source gives its location, "
	"so it has no spatial key.",
	"No placement has been checked against the manual's numbered location drawings: every table object placement (switches, "
	"lamps, flashers, the slings, bumpers and kickback, and the G.I.) keeps the table's `observed` status. A callout check "
	"of the switch (printed page 50), lamp (53) and solenoid (54) drawings would validate the ones that land on their "
	"callouts.",
	"Solenoids 9 and 10 (playfield white and green G.I.): the placements are the bulb lights of the retained table's GI and "
	"gi_green collections. The manual prints no G.I. bulb count or layout and a table's grouping is not the machine's "
	"wiring, so they stay observed without a quantity.",
	"Solenoids 15 and 29 (top panel flashers): the five dome lights sit 12-13 units behind the rear edge and are clamped to "
	"it; the panel is upright, so the clamped point is the panel's foot, not the dome.",
	"Switches 50 and 54: the table binds them to the opposite rubbers from the manual and the ROM; the placements follow the "
	"machine, so they rest on the table's other object and stay observed.",
]


def _manifest_bytes(manifest: dict[str, Any]) -> bytes:
	return canonical_bytes(manifest)


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Space Station retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Space Station extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Space Station retained extraction manifest is missing: {manifest_path}")
	if _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Space Station retained extraction manifest is not the pinned one: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Space Station retained extraction manifest does not match the extracted files")
	if len(actual["files"]) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"Space Station retained extraction file count mismatch: {len(actual['files'])} != {EXTRACTION_FILE_COUNT}")
	return actual


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs, located_outputs, omitted_inputs, omitted_outputs = [], [], [], []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	statuses: dict[str, int] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device.get("spatial")
		if spatial is None:
			omitted_inputs.append(device["binding"]["device"])
		elif spatial["status"] == "not_applicable":
			na_inputs.setdefault(spatial["reason"], []).append(device["binding"]["device"])
		else:
			located_inputs.append(device["binding"]["device"])
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": device["binding"]["device"]}
		spatial = device.get("spatial")
		if spatial is None:
			omitted_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			na_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	unvalidated = sorted(
		item["id"] for collection in ("inputs", "outputs") for device in definition[collection]
		for item in (device.get("spatial") or {}).get("placements", []) if item["provenance"]["status"] != "validated"
	)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "observed",
		"blockers": SPATIAL_BLOCKERS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "source_ref": VPX_EXTRACTION_SOURCE},
		"source_hashes": {
			"embedded_script_sha256": EMBEDDED_SCRIPT_SHA256, "known_working_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256, "table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"placement_status_counts": dict(sorted(statuses.items())),
		"unvalidated_placements": unvalidated,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(values, key=lambda item: (item["group"], item["address"])) for reason, values in sorted(na_outputs.items())},
		"omitted_inputs": sorted(omitted_inputs),
		"omitted_outputs": sorted(omitted_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, (_, reason) in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto {reason}."} for address, (_, reason) in sorted(SOLENOID_PROJECTIONS.items())]
		),
		"clamped_placements": [
			{"group": "pinmame.output.solenoid", "address": address, "object": name, "raw_y": xy[1], "clamped_y": 0.0}
			for address in (15, 29) for name, xy in FLASHER_LIGHTS[address]
		],
		"excluded_object_classes": [
			"Light l37, l41, l46-l49 and l57: the insert-board lamps' backglass helpers, parked in a row at y = -213.3422 above the playfield; the lamps are backbox devices",
			"Light f30, f31 and GI_BG: backglass helpers of the backbox-only flashers 30 and 31 and the insert G.I. (11), at y = -198.3962",
			"Primitive and light-map objects (BM_*, LM_*, BP_*): baked render meshes; the Space Station's BM_SS_01 is used only for its pivot",
			"Trigger RampTrigger1-7, TriggerBallNearLF/RF and TriggerLF/RF: ramp-sound and flipper helpers with no switch binding",
			"Walls sw33a, sw57a, sw58a and sw59a: the drop targets' secondary walls; the primary walls are the placements",
			"Flasher objects: glow sprites, never placements",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Space Station (Williams, 1987) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at `machines/partial/williams/space-station-1987.json`; "
		f"its spatial dimension stays open because of the {len(report['blockers'])} spatial blockers below.",
		"",
		f"The geometry source is VPW's retained `Space Station (Williams 1987) VPW v1.0.vpx`, SHA-256 `{TABLE_SHA256}`, whose "
		f"embedded script (SHA-256 `{EMBEDDED_SCRIPT_SHA256}`) is the pinned known-working v1.0.1 script (SHA-256 "
		f"`{SCRIPT_SHA256}`) apart from whitespace and one trailing changelog comment, so every cited script line is the same in "
		f"both. Bounds are `{TABLE_BOUNDS}`; every coordinate is x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT}, rounded to at most "
		"six places.",
		"",
		"## Evidence decisions",
		"",
		"- A placement is the centre of the table object the script binds to the address: a trigger, kicker, hit target, bumper "
		"or drop-target wall for a switch, the `lN` light vpmMapLights binds for each lamp, the script-driven `fN` lights for "
		"each flasher, the bulb lights of the GI and gi_green collections for the playfield G.I., and the slingshot walls, "
		"bumpers and kickback for their coils.",
		"- Sensors and coils with no table object of their own (the Space Station optos and motor, the outhole, feeder, popper, "
		"drop-reset and dock coils) are documented projections onto their own mechanism's object.",
		"- Backbox and cabinet devices take controlled `not_applicable` records: the insert-board lamps 37, 41, 46-49 and 57, the "
		"backbox flashers 30 and 31, the insert G.I. (11), the knocker, the A/C relay, the cabinet, lane-change and diagnostic "
		"switches, the Country jumper and the four displays.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		short = "Switch" if entry["group"] == "pinmame.input.switch" else "Solenoid"
		lines.append(f"- {short} {entry['address']}: {entry['reason']}")
	lines += ["", "## Clamped placements", ""]
	for entry in report["clamped_placements"]:
		lines.append(f"- Solenoid {entry['address']}, {entry['object']}: raw y {entry['raw_y']} clamped to {entry['clamped_y']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({', '.join(f'{k} {v}' for k, v in report['placement_status_counts'].items())})",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Inputs with an omitted spatial key: {len(report['omitted_inputs'])}",
		f"- Outputs with an omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, values in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(values)}")
	for reason, values in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(values)}")
	lines += ["", "## Blockers", ""] + [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the "
		"mechanisms and both production insert boards are covered, polarity is settled by the ROM's Switch Levels test, and "
		"every playfield device has a placement. Promotion to `author_ready` is refused because the table placements are not "
		"checked against the factory drawings and the G.I. placements come only from the table's grouping, so "
		"`coverage.missing` is `[\"spatial_placement\"]`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		if STATUS != "author_ready":
			raise RuntimeError(f"refusing to replace the author-ready Space Station definition with a {STATUS} one: {stale}")
		stale.unlink()
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / STALE_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Space Station is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	definition = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Space Station definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Space Station seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Space Station spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Space Station spatial review drifted from its deterministic curator: {markdown_path}")
	print("Space Station definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed and the spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Space Station extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Space Station retained extraction matches its pinned manifest.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
