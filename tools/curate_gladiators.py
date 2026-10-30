"""Curate the physical Gottlieb Gladiators (1993) machine definition.

The builder is side-effect free and deterministic: every reviewed label is a literal here, so regeneration reproduces
the canonical definition, its pinned seed and the spatial report byte for byte without reading the external evidence
roots. ``--check`` refuses drift, and ``--regenerate`` is the only path that writes them.

Gladiators is a Gottlieb System 3 DMD machine (``GEN_GTS3``, ``mGTS3DMDS``) with one driver, ``gladiatr``, declared as
``INITGAME2(gladiatr, DMD, FLIP8283, 4, SNDBRD_GTS3, 4)``: the cabinet port flagged ``0x8000`` (coins, Start, Tournament
and Front Door on public 0-6), cabinet-wired flippers copied into matrix switches 82 and 83 from PinMAME's flipper column
(public 143 and 141), and ``hw.lampCol = 4``, so no auxiliary driver board and no lamps 120-127. No service manual is
retained: IPDB lists its charts without hosting them. The ROM's own service tests name every switch, lamp and solenoid,
and a harness run of each pairs the name with the public address it drives or reads
(``evidence/runtime/gts3/gladiators-gladiatr-service-tests.json``). Playfield positions come from the retained VR edit
of Kiwi's VPX v1.1.1 table, whose embedded script binds every controller address exactly as the pinned v1.1.1 script
does; with one table and no factory drawing they stay ``observed``. The object coordinates are literals here, and
``verify_retained_table`` re-derives each one from the retained extraction and OBJ export.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "gottlieb.gladiators.1993"
PARTIAL_PATH = ROOT / "machines/partial/gottlieb/gladiators-1993.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/gottlieb/gladiators-1993.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/gottlieb/gladiators-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/gottlieb/gladiators-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/gottlieb/gladiators-1993.md"
KNOWLEDGE_PATH = "knowledge/gottlieb/gladiators-1993.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/gts3/gladiators-gladiatr-service-tests.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-gts3"
IDENTITY_SOURCE = "identity.gottlieb.gladiators.1993"
RUNTIME_SOURCE = "runtime.gladiators.gladiatr-service-tests"
SCRIPT_SOURCE = "vpx-script.gladiators-kiwi-1-1-1"
OLDER_SCRIPT_SOURCE = "vpx-script.gladiators-kiwi-1-0-1"
VPM_LIBRARY_SOURCE = "vpm-script-library.gts3-vbs"
VPM_LIBRARY_URI = "external:pinmame-review-artifacts/vpm-script-libs/gts3.vbs"
VPM_GTS3_SHA256 = "66c329fa86e97d2f10a8036a9a6527be6a67ce59bb3591962aa1c8a9da101314"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"

STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
TABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
IPDB_PAGE_SHA256 = "1cc4a4c44942e0ecf9f253047398abe9d5f63ef5f2e11becc9db8ffbf813d4ce"
# The pinned Git blob (LF); the local checkout materializes it with CRLF as 5f6892ee...
SCRIPT_SHA256 = "25060187b97e5a57499429689be0c247003d26342bed632961d0cd9ba02cfe69"
SCRIPT_CHECKOUT_SHA256 = "5f6892eee612ded70df23c88d51813145572495395e807c000851d132f128853"
OLDER_SCRIPT_SHA256 = "13b45d7e9a4ead26633cb0dd6ed1adf2e25fdcb0785360b3bcdddc7db5ba45e7"

# The retained table: MaX's 2024 VR edit of Kiwi's VPX v1.1.1, under the working root's vpx-sources.
VPX_TABLE_SOURCE = "vpx-table.gladiators-kiwi-1-1-1-vr"
VPX_EXTRACTION_SOURCE = "vpx-extraction.gladiators-kiwi-1-1-1-vr"
VPX_OBJ_SOURCE = "vpx-obj-export.gladiators-kiwi-1-1-1-vr"
VPX_DIRECTORY = Path("gottlieb/gladiators-1993/kiwi-v1.1.1-vr")
TABLE_FILENAME = "Gladiators (Premier 1993) v1.1.1 VR.vpx"
TABLE_RELATIVE_PATH = VPX_DIRECTORY / "source" / TABLE_FILENAME
TABLE_SHA256 = "b2925083424e053ebf9149657301b4358ef5448008ba41f3fd7e747c1d126ef9"
TABLE_BYTES = 108167168
# The embedded script as vpxtool extracts it (CRLF, 51,298 bytes).
EMBEDDED_SCRIPT_SHA256 = "0c8c67f2e39b62597bc4b067fd9b1fb092a402deba8e673067b877d718f2380f"
EXTRACTION_RELATIVE_PATH = VPX_DIRECTORY / "extracted-vpxtool"
EXTRACTION_MANIFEST_RELATIVE_PATH = VPX_DIRECTORY / "extracted-vpxtool.manifest.json"
EXTRACTION_FILE_COUNT = 2052
EXTRACTION_TOTAL_BYTES = 203551065
# SHA-256 of the canonical manifest bytes, so a changed extraction with a refreshed manifest is refused.
EXTRACTION_MANIFEST_SHA256 = "9433e0a06daafaa1170dc81cecfc2f9c0c6342e27eb6091d49351c279e3d2f05"
OBJ_RELATIVE_PATH = VPX_DIRECTORY / "export-obj-vpu" / "Gladiators (Premier 1993) v1.1.1 VR.obj"
OBJ_SHA256 = "33f6ef95d046df9dc83942642396e6a136aa345757a16d27f0bb4dbd4b37e1c2"
VPXTOOL_VERSION = "vpxtool git:v0.33.3"

PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

# (left, right) in the driver's own FLIP_SWNO macro order (FLIP8283).
FLIP_SWNO = (82, 83)

DRIVER_IDS = ("gladiatr",)
DRIVER_COMPATIBILITY = {
	"gladiatr": (
		"identical",
		"The only Gladiators driver (gprom.bin with dsprom.bin), declared INITGAME2(gladiatr, DMD, FLIP8283, 4, SNDBRD_GTS3, 4) "
		"in pinned src/wpc/gts3games.c lines 505-516 and catalogued with CORE_GAMEDEFNV(gladiatr, \"Gladiators\", 1993, "
		"\"Gottlieb\", mGTS3DMDS, 0); its power-up screen reads GLADIATORS / (Install 4 Balls) / Game #737, ID #000000 / GPROM "
		"CHECKSUM-FC59, and model 737 is IPDB's model number for the machine. Every runtime probe here ran on it, and the "
		"known-working script loads it (cGameName = \"gladiatr\").",
	),
}

# --- Switches. Public addresses are Gottlieb's own decimal numbers (gts3_sw2m): tens digit strobe, units digit return.
# ROM_SWITCH_NAMES is the name the Switch Matrix Test (self-test 5) displays while the host holds the address at 1.
ROM_SWITCH_NAMES = {
	0: "COIN CHUTE #1 -LEFT", 1: "COIN CHUTE #2 -RIGHT", 2: "COIN CHUTE #3 -CENTER", 3: "COIN CHUTE #4",
	5: "TOURNAMENT", 6: "FRONT DOOR (SERVICE)", 10: "TOP LEFT POP BUMPER", 11: "TOP RIGHT POP BUMPER",
	12: "BOTTOM POP BUMPER", 13: "LEFT KICKING TARGET", 14: "RIGHT KICKING TARGET", 15: "DROP TARGET #1", 20: "SPINNER",
	21: "TOP HOLE", 22: "CENTER UPKICKER", 23: "OUTHOLE", 24: "SHOOTER LANE ROLLOVER", 25: "DROP TARGET #2",
	30: "RAMP MOTOR", 31: "LEFT HOLE", 32: "RIGHT UPKICKER", 33: "TROUGH", 35: "DROP TARGET #3",
	80: "L HORSESHOE (OPTO)", 81: "R HORSESHOE (OPTO)", 82: "L FLIPPER (SENSOR BD)", 83: "R FLIPPER (SENSOR BD)",
	90: "LEFT RAMP #1 (OPTO)", 91: "LEFT RAMP #2 (OPTO)", 92: "L OUTSIDE ROLLOVER", 93: "R OUTSIDE ROLLOVER",
	94: "TOP STAR R.O.", 95: "LEFT SPOT TARGET #2", 100: "SHOOTER LANE (OPTO)", 101: "RIGHT RAMP (OPTO)",
	102: "LEFT RETURN R.O.", 103: "RIGHT RETURN R.O.", 104: "LEFT SPOT TARGET #1",
}
MATRIX_ADDRESSES = tuple(column * 10 + row for column in range(12) for row in range(8))
UNUSED_SWITCHES = frozenset(address for address in MATRIX_ADDRESSES if address not in ROM_SWITCH_NAMES and address != 4)
SWITCH_LABELS = {
	0: "Coin Chute #1 (Left)", 1: "Coin Chute #2 (Right)", 2: "Coin Chute #3 (Center)", 3: "Coin Chute #4",
	4: "Credit Button (Start)", 5: "Tournament Button", 6: "Front Door (Service)",
	10: "Top Left Pop Bumper", 11: "Top Right Pop Bumper", 12: "Bottom Pop Bumper", 13: "Left Kicking Target",
	14: "Right Kicking Target", 15: "Drop Target #1",
	20: "Spinner", 21: "Top Hole", 22: "Center Upkicker", 23: "Outhole", 24: "Shooter Lane Rollover", 25: "Drop Target #2",
	30: "Ramp Motor (Catapult Home)", 31: "Left Hole", 32: "Right Upkicker", 33: "Trough", 35: "Drop Target #3",
	80: "Left Horseshoe Opto", 81: "Right Horseshoe Opto", 82: "Left Flipper (Matrix Copy)", 83: "Right Flipper (Matrix Copy)",
	90: "Left Ramp #1 Opto", 91: "Left Ramp #2 Opto", 92: "Left Outside Rollover", 93: "Right Outside Rollover",
	94: "Top Star Rollover", 95: "Left Spot Target #2",
	100: "Shooter Lane Opto", 101: "Right Ramp Opto", 102: "Left Return Rollover", 103: "Right Return Rollover",
	104: "Left Spot Target #1",
}
OPTO_SWITCHES = frozenset({80, 81, 90, 91, 100, 101})
CABINET_SWITCH_ROLES = {
	0: "cabinet.coin", 1: "cabinet.coin", 2: "cabinet.coin", 3: "cabinet.coin", 4: "cabinet.start", 5: "cabinet.service",
	6: "cabinet.coin-door", 82: "cabinet.flipper", 83: "cabinet.flipper",
}
CABINET_SWITCH_TYPES = {4: "button", 5: "button"}
# What the ROM did with the address at 1 outside the Switch Matrix Test.
ROM_RUNTIME = {
	0: "the Front Door Test counted a coin on chute 1 for each pulse at 1 (run front-door), and two pulses gave one credit in attract mode (runs gameplay, tournament-door)",
	1: "the Front Door Test counted a coin on chute 2 for the pulse at 1 (run front-door)",
	2: "the Front Door Test counted a coin on chute 3 for the pulse at 1 (run front-door)",
	3: "the Front Door Test counted a coin on chute 4 for the pulse at 1 (run front-door)",
	4: "with one credit a pulse at 1 started a game: the display read BALL 1 and the ROM pulsed the plunger gate (13) (runs gameplay, tournament-door, mechanism-sensors)",
	10: "of three 100 ms pulses at 1 during a game, the third made the ROM fire 1, TOP LEFT POP BUMPER (run gameplay)",
	11: "each of three 100 ms pulses at 1 during a game made the ROM fire 2, TOP RIGHT POP BUMPER (run gameplay)",
	12: "of three 100 ms pulses at 1 during a game, the third made the ROM fire 3, BOTTOM POP BUMPER (run gameplay)",
	13: "of three 100 ms pulses at 1 during a game, the second made the ROM fire 4, L KICKING TARGET (run gameplay)",
	21: "held at 1 for 1.5 s during a game, the ROM fired 7, TOP HOLE, twice (run gameplay)",
	22: "held at 1 for 1.5 s during a game, the ROM fired 11, CENTER UPKICKER, twice (run gameplay)",
	23: "when it rose to 1 during a game the ROM reset the 3-bank (10), energized the ramp motor relay (23) and the ball release (28), then fired 29, OUTHOLE, and energized the game-over relay (32) (run gameplay)",
	31: "held at 1 for 1.5 s during a game, the ROM fired 6, LEFT HOLE, twice (run gameplay)",
	32: "held at 1 for 1.5 s during a game, the ROM fired 12, RIGHT UPKICKER, twice (run gameplay)",
	82: "with the left flipper button (143), which core_updateSw copies into it, at 1, the menu stepped to the next item (run nvram-init)",
	83: "with the right flipper button (141), which core_updateSw copies into it, at 1, the menu selected SELF-TEST and each test stepped to its next item (runs lamp-matrix, solenoids, switch-matrix, front-door)",
}
# The known-working script's writer for each playfield switch.
SCRIPT_WRITERS = {
	10: "Bumper1_Hit pulses it (line 621)", 11: "Bumper2_Hit pulses it (line 622)", 12: "Bumper3_Hit pulses it (line 623)",
	13: "LeftSlingshot_Slingshot pulses it (line 584)", 14: "RightSlingshot_Slingshot pulses it (line 602)",
	15: "the dtBank drop target object writes it, 1 while the target is down (line 310)",
	25: "the dtBank drop target object writes it, 1 while the target is down (line 310)",
	35: "the dtBank drop target object writes it, 1 while the target is down (line 310)",
	20: "sw20_Spin pulses it on each spinner turn (line 626)",
	21: "the bsTP saucer holds it at 1 while a ball sits in Kicker sw21 (line 272)",
	22: "the bsCP saucer holds it at 1 while a ball sits in Kicker sw22 (line 292)",
	23: "bsTrough.InitSw names it the stack's entry switch, 1 while a drained ball waits in the outhole (line 262)",
	24: "sw24_Hit writes 1 and sw24_UnHit 0 (lines 639-640)",
	30: "the mRMotor mechanism holds it at 1 at step 0, its home position (.AddSw 30, 0, 0, line 322)",
	31: "the bsLP saucer holds it at 1 while a ball sits in Kicker sw31 (line 282)",
	32: "the bsRP saucer holds it at 1 while a ball sits in Kicker sw32 (line 300)",
	33: "bsTrough.InitSw names it the stack's first position, 1 while the trough holds a ball (line 262)",
	80: "sw80_Hit writes 1 and sw80_UnHit 0 (lines 641-642)", 81: "sw81_Hit writes 1 and sw81_UnHit 0 (lines 643-644)",
	90: "Gate90_Hit pulses it (line 659); the trigger handlers that would hold it are commented out (lines 660-661)",
	91: "sw91_Hit writes 1 and sw91_UnHit 0 (lines 662-663)", 92: "sw92_Hit writes 1 and sw92_UnHit 0 (lines 649-650)",
	93: "sw93_Hit writes 1 and sw93_UnHit 0 (lines 653-654)", 94: "sw94_Hit writes 1 and sw94_UnHit 0 (lines 645-646)",
	95: "sw95_Hit pulses it (line 684)", 100: "sw100_Hit writes 1 and sw100_UnHit 0 (lines 647-648)",
	101: "sw101_Hit writes 1 and sw101_UnHit 0 (lines 664-665)", 102: "sw102_Hit writes 1 and sw102_UnHit 0 (lines 651-652)",
	103: "sw103_Hit writes 1 and sw103_UnHit 0 (lines 655-656)", 104: "sw104_Hit pulses it (line 685)",
}

# --- Solenoids. ROM_COIL_NAMES[public] is the Relay & Solenoid Test's name for driver (public - 1).
ROM_COIL_NAMES = {
	1: "TOP LEFT POP BUMPER", 2: "TOP RIGHT POP BUMPER", 3: "BOTTOM POP BUMPER", 4: "L KICKING TARGET",
	5: "R KICKING TARGET", 6: "LEFT HOLE", 7: "TOP HOLE", 8: "VOLCANO & MOON 67", 9: "CATAPULT & BALL 67",
	10: "3 BANK RESET", 11: "CENTER UPKICKER", 12: "RIGHT UPKICKER", 13: "PLUNGER GATE", 14: "SPOT TARGET 67",
	15: "MOTOR RAMP DOME 67", 16: "RIGHT RAMP DOME 67", 17: "R UPKICKER DOME 67", 18: "SPINNER 67",
	19: "LIGHTSTRIP 67 #1", 20: "LIGHTSTRIP 67 #2", 21: "LIGHTSTRIP 67 #3", 22: "L & R DRAGON 67",
	23: "RAMP MOTOR RELAY (B)", 24: "SHIELD & C DRAGON 67", 25: "SHAKER MOTOR", 26: "LIGHTBOX RELAY (A)",
	27: "TICKET/COIN METER", 28: "BALL RELEASE", 29: "OUTHOLE", 30: "KNOCKER", 31: "TILT RELAY (T)",
	32: "GAME OVER RELAY (Q)",
}
SOLENOID_LABELS = {
	1: "Top Left Pop Bumper", 2: "Top Right Pop Bumper", 3: "Bottom Pop Bumper", 4: "Left Kicking Target Coil",
	5: "Right Kicking Target Coil", 6: "Left Hole Kicker", 7: "Top Hole Kicker", 8: "Volcano & Moon Flasher",
	9: "Catapult & Ball Flasher", 10: "3-Bank Drop Target Reset", 11: "Center Upkicker Coil", 12: "Right Upkicker Coil",
	13: "Plunger Gate", 14: "Spot Target Flasher", 15: "Motor Ramp Dome Flasher", 16: "Right Ramp Dome Flasher",
	17: "Right Upkicker Dome Flasher", 18: "Spinner Flasher", 19: "Lightstrip Flasher #1", 20: "Lightstrip Flasher #2",
	21: "Lightstrip Flasher #3", 22: "Left & Right Dragon Flasher", 23: "Ramp Motor Relay (B)",
	24: "Shield & Center Dragon Flasher", 25: "Shaker Motor", 26: "Lightbox Relay (A)", 27: "Ticket/Coin Meter",
	28: "Ball Release", 29: "Outhole Kicker", 30: "Knocker", 31: "Tilt Relay (T)", 32: "Game Over Relay (Q)",
}
FLASHER_SOLENOIDS = frozenset({8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24})
SOLENOID_KIND = {23: "relay", 25: "motor", 26: "relay", 31: "relay", 32: "relay"}
# Flashers the known-working script draws in its backbox section (lines 1143-1159, at backbox height Fpy, line 374).
SCRIPT_BACKBOX_FLASHERS = {8: 188, 9: 189, 22: 182, 24: 184}
SOLENOID_CALLBACKS = {
	6: "SolBallReleaseLP (line 706), which kicks the ball out of the bsLP saucer at Kicker sw31 and swings its eject arm (lines 772-776)",
	7: "SolBallReleaseTP (line 707), which kicks the ball out of the bsTP saucer at Kicker sw21",
	10: "dtcbank (line 710), which raises the dtBank drop targets 15, 25 and 35 (lines 757-759)",
	11: "SolBallReleaseCP (line 711), which lifts the ball out of the bsCP vertical upkicker at Kicker sw22",
	12: "SolBallReleaseRP (line 712), which kicks the ball out of the bsRP saucer at Kicker sw32",
	13: "PlungerGate (line 713), which drops the post Perno while the output is on and raises it again from a timer after it turns off (lines 740-750)",
	25: "MShaker (line 725), a sound only (lines 825-826)",
	26: "GIBackBox (line 726), which turns the backbox G.I. (its lamp 156) off while the relay is on (lines 846-849)",
	28: "bsTroughSolOut (line 727), which kicks the lead ball out of the four-ball bsTrough stack at BallRelease",
	29: "bsTrough.SolIn (line 728), which moves a drained ball from the outhole into the stack",
	30: "KnockerSound (line 729), a sound only",
	31: "GIRelay (line 730), which turns the playfield G.I. (its lamps 150 and 151) off while the relay is on (lines 839-844)",
	32: "SolRun (line 731), which passes the state to vpmNudge.SolGameOn (lines 852-853)",
}
SOLENOID_RUNTIME = {
	1: "fired on the third of three pulses of its switch 10 during a game (run gameplay)",
	2: "fired on each of three pulses of its switch 11 during a game (run gameplay)",
	3: "fired on the third of three pulses of its switch 12 during a game (run gameplay)",
	4: "fired on the second of three pulses of its switch 13 during a game (run gameplay)",
	6: "fired twice while switch 31 was held at 1 for 1.5 s, and in each ball search (runs gameplay, mechanism-sensors)",
	7: "fired twice while switch 21 was held at 1 for 1.5 s, and in each ball search (runs gameplay, mechanism-sensors)",
	10: (
		"fired at power-up in every run that booted to attract mode and again when the ROM served a ball after the drain; "
		"holding 15, 25 and 35 at 1 together for six seconds during the first ball drew no reset (run gameplay)"
	),
	11: "fired twice while switch 22 was held at 1 for 1.5 s, and in each ball search (runs gameplay, mechanism-sensors)",
	12: "fired twice while switch 32 was held at 1 for 1.5 s, and in each ball search (runs gameplay, mechanism-sensors)",
	13: "was pulsed at Start and again in each ball search (runs gameplay, mechanism-sensors, tournament-door)",
	17: "flashed five times after the drain, as the next ball was served (run gameplay)",
	23: (
		"was energized by the ROM's ball search, about 15 s after the plunge in run mechanism-sensors, and stayed on to "
		"the end of that run while the host closed, opened and closed switch 30; in run gameplay it stayed on for about 22.4 s "
		"(35.1-57.5 s) and the ROM energized it again when the ball drained"
	),
	28: "was energized about 1.7 s after the outhole switch 23 rose during a game and held for about 0.7 s (run gameplay)",
	29: "fired about 2.9 s after the outhole switch 23 rose during a game, after 28 and once the scenario had opened 23 again (run gameplay)",
	32: (
		"rose after the drain in the scripted game; from Start to the drain it stayed off and the flipper presses raised "
		"nothing, so the run does not show what energizes it during a played first ball (run gameplay)"
	),
}
GAMEPLAY_GAPS = {
	5: (
		"Three 100 ms pulses of its switch (14) during the gameplay run published nothing here. PinMAME smooths System 3 "
		"solenoids over four frames (GTS3_SOLSMOOTH), which can swallow a short coil pulse, so that is a possible "
		"explanation, not a proven one. The Relay & Solenoid Test fired it."
	),
}
CABINET_SOLENOIDS = {25: "cabinet", 26: "backbox", 27: "cabinet", 30: "cabinet", 32: "cabinet"}

# --- Lamps. ROM_LAMP_NAMES is the Lamp Matrix Test's name for each LAMP:nn (A0-B7 = 100-117) it blinked.
ROM_LAMP_NAMES = {
	0: "\"SHOOT AGAIN\"", 1: "CREDIT BUTTON", 2: "L CARDHOLDER \"W\"", 3: "L CARDHOLDER \"E\"", 4: "L CARDHOLDER \"A\"",
	5: "L CARDHOLDER \"P\"", 6: "L CARDHOLDER \"O\"", 7: "L CARDHOLDER \"N\"", 10: "TOP HOLE \"LOCK\"",
	11: "TOP HOLE \"?\"", 12: "R CARDHOLDER \"D\"", 13: "R CARDHOLDER \"O\"", 14: "R CARDHOLDER \"U\"",
	15: "R CARDHOLDER \"B\"", 16: "R CARDHOLDER \"L\"", 17: "R CARDHOLDER \"E\"", 20: "SPOT TARGET \"1\"",
	21: "SPOT TARGET \"2\"", 22: "\"LIGHT MULTIBALL\"", 23: "LEFT BLUE #1", 24: "LEFT BLUE #2", 25: "LEFT BLUE #3",
	26: "LEFT BLUE #4", 27: "LEFT BLUE #5", 30: "\"BEGIN ROUND\"", 31: "\"ADV. MULTIPLIER\"", 32: "\"SPELL WEAPON\"",
	33: "RIGHT YELLOW #1", 34: "RIGHT YELLOW #2", 35: "RIGHT YELLOW #3", 36: "RIGHT YELLOW #4", 37: "RIGHT YELLOW #5",
	40: "L TAR. \"ADV. YELLOW\"", 41: "L HOLE \"SPELL DOUBLE\"", 42: "L HOLE \"ATTACK!\"",
	43: "L HOLE \"CATAPULT 50M\"", 44: "L RAMP \"HOLD\"", 45: "L RAMP \"ATTACK!\"", 46: "L RAMP \"COMBO\"",
	47: "L RAMP \"M\"", 50: "\"EVERYTHING DOUBLED\"", 51: "R RAMP \"SPECIAL\"", 52: "R RAMP \"COMBO\"",
	53: "R RAMP \"T\"", 54: "SPINNER \"!\"", 55: "SPINNER \"ACU-SPIN\"", 56: "SPINNER \"COMBO\"", 57: "SPINNER \"I\"",
	60: "L OUTSIDE ROLLOVER", 61: "L RETURN ROLLOVER", 62: "R LOOP \"SPELL WEAPON\"", 63: "R LOOP \"COMBO\"",
	64: "R LOOP \"L", 65: "L LOOP \"SPELL WEAPON\"", 66: "L LOOP \"COMBO\"", 67: "L LOOP \"U\"",
	70: "\"THIS ROUND 2X\"", 71: "\"THIS ROUND 3X\"", 72: "\"RAIN OF TERROR\"", 73: "\"CATAPULT\"",
	74: "\"FIRE & ICE\"", 75: "\"CATACLYSM\"", 76: "\"BLADE FIGHT\"", 77: "CALM BEFORE THE STORM",
	81: "3 BANK \"ADV. BLUE\"", 82: "3 BANK \"5M\"", 83: "3 BANK \"ADV. YELLOW\"", 84: "R BILLBOARD \"500K\"",
	85: "R BILLBOARD \"1M\"", 86: "R BILLBOARD \"2M\"", 87: "R BILLBOARD \"BALL\"", 91: "C UPKICKER \"ABYSS\"",
	92: "C UPKICKER \"E.B.\"", 93: "C UPKICKER \"WEAPON\"", 94: "L BILLBOARD \"500K\"", 95: "L BILLBOARD \"1M\"",
	96: "L BILLBOARD \"2M\"", 97: "L BILLBOARD \"EXTRA\"", 100: "R TARGET \"ADV. BLUE\"", 101: "R RETURN ROLLOVER",
	102: "R OUTSIDE ROLLOVER", 103: "R UPKICKER \"LIGHT 2X\"", 104: "R UPKICKER \"LIGHT 3X\"",
	105: "R UPKICKER \"TIMED\"", 106: "R UPKICKER \"MULTIBALL\"", 107: "R UPKICK BEGIN PYRAMID", 112: "LIGHTBOX #1",
	113: "LIGHTBOX #2", 114: "LIGHTBOX #3", 115: "LIGHTBOX #4", 116: "LIGHTBOX #5", 117: "LIGHTBOX #6",
}
LAMP_ADDRESSES = MATRIX_ADDRESSES
LIGHTBOX_LAMPS = frozenset({112, 113, 114, 115, 116, 117})
# Lamps PinMAME's gladiatr block types as strobed LEDs (gts3.c lines 712-714): the WEAPON and DOUBLE cardholders and the
# left billboard.
LED_LAMPS = {
	**{address: "'WEAPON' LEDs" for address in range(2, 8)},
	**{address: "'DOUBLE' LEDs" for address in range(12, 18)},
	**{address: "Left Billboard LEDs" for address in range(94, 98)},
}
# Lamp numbers the known-working script's UpdateLamps binds (lines 941-1029 l<n>, 1031-1048 f84-f87/f94-f97, 1145-1150 l112-l117).
SCRIPT_LAMPS = frozenset(address for address in ROM_LAMP_NAMES if address != 1)
# The billboard lamps the script's UpdateLamps drives with Flashm (lines 1033-1047); 91-93 use NFadeL (lines 1019-1021).
SCRIPT_FLASH_LAMPS = frozenset((84, 85, 86, 87, 94, 95, 96, 97))
WORD_EXPANSIONS = {"L": "Left", "R": "Right", "C": "Center", "TAR.": "Target", "UPKICK": "Upkicker", "R.O.": "Rollover"}

# --- Placements. Retained-table objects as (item type, x, y) in VPX units: a Wall's drag-point mean, a HitTarget's or
# Primitive's stored position, otherwise the stored centre. verify_retained_table re-derives every value.
TABLE_POINTS: dict[str, tuple[str, float, float]] = {
	"Bumper1": ("Bumper", 504.0, 256.25), "Bumper2": ("Bumper", 716.75, 192.0), "Bumper3": ("Bumper", 677.75, 406.75),
	"LeftSlingshot": ("Wall", 233.8338625, 1553.35235), "RightSlingshot": ("Wall", 631.618045, 1553.35235),
	"sw15": ("HitTarget", 462.32104, 971.5609), "sw25": ("HitTarget", 520.5886, 988.3476), "sw35": ("HitTarget", 577.74634, 1004.4406),
	"sw20": ("Spinner", 758.118, 824.6247),
	"sw21": ("Kicker", 534.0, 134.0), "sw22": ("Kicker", 635.125, 914.5), "sw31": ("Kicker", 321.65, 658.0),
	"sw32": ("Kicker", 747.0, 1166.4), "Drain": ("Kicker", 454.0, 2031.0), "BallRelease": ("Kicker", 819.0, 1833.0),
	"sw24": ("Trigger", 896.0, 1865.0), "sw80": ("Trigger", 115.0, 266.0), "sw81": ("Trigger", 370.0, 204.0),
	"Gate90": ("Gate", 89.0, 132.0), "sw91": ("Trigger", 252.875, 166.0), "sw92": ("Trigger", 52.992188, 1522.8281),
	"sw93": ("Trigger", 811.6172, 1520.9688), "sw94": ("Trigger", 573.375, 482.25), "sw95": ("HitTarget", 87.86694, 1101.6996),
	"sw100": ("Trigger", 859.0, 168.0), "sw101": ("Trigger", 520.5, 296.0), "sw102": ("Trigger", 123.25, 1555.5),
	"sw103": ("Trigger", 742.0, 1555.5), "sw104": ("HitTarget", 60.95288, 1126.2096),
	"Perno": ("Wall", 252.875, 187.796876875),
	"fl14": ("Light", 43.69995, 1067.5), "fl15": ("Light", 125.5, 590.5), "fl16": ("Light", 727.5, 654.7281),
	"fl17": ("Light", 805.0, 1065.5), "l197": ("Light", 813.0, 932.0),
	"l0": ("Light", 565.25, 1637.6719),
	"l2": ("Light", 78.5, 1886.0), "l3": ("Light", 108.75, 1886.0), "l4": ("Light", 139.0, 1886.0),
	"l5": ("Light", 169.25, 1886.0), "l6": ("Light", 199.5, 1886.0), "l7": ("Light", 229.75, 1886.0),
	"l10": ("Light", 824.16797, 670.0996), "l11": ("Light", 852.75586, 599.21094),
	"l12": ("Light", 514.0, 1943.75), "l13": ("Light", 556.5, 1919.5), "l14": ("Light", 598.75, 1895.5),
	"l15": ("Light", 640.5, 1872.0), "l16": ("Light", 683.0, 1847.75), "l17": ("Light", 724.25, 1824.0),
	"l20": ("Light", 175.01367, 1330.875), "l21": ("Light", 148.16895, 1269.748), "l22": ("Light", 115.62988, 1196.5352),
	"l23": ("Light", 399.30078, 1609.7988), "l24": ("Light", 399.5332, 1560.793), "l25": ("Light", 399.30078, 1511.2695),
	"l26": ("Light", 399.5332, 1461.7285), "l27": ("Light", 399.30078, 1412.7051),
	"l30": ("Light", 896.6836, 1403.8555), "l31": ("Light", 896.4512, 1310.8867), "l32": ("Light", 896.6836, 1217.4531),
	"l33": ("Light", 464.3789, 1609.7988), "l34": ("Light", 464.61133, 1560.793), "l35": ("Light", 464.3789, 1511.2695),
	"l36": ("Light", 464.61133, 1461.7285), "l37": ("Light", 464.61133, 1412.4727),
	"l40": ("Light", 234.7461, 1487.2949), "l41": ("Light", 321.09082, 897.87305), "l42": ("Light", 321.67188, 830.2383),
	"l43": ("Light", 321.67188, 751.9121), "l44": ("Light", 251.48047, 1284.623), "l45": ("Light", 231.72461, 1226.0527),
	"l46": ("Light", 209.2959, 1155.3965), "l47": ("Light", 182.56738, 1079.627),
	"l50": ("Light", 299.82422, 1637.207), "l51": ("Light", 430.56152, 655.9219), "l52": ("Light", 495.63965, 631.05273),
	"l53": ("Light", 569.08496, 602.9297), "l54": ("Light", 609.17773, 1232.793), "l55": ("Light", 629.63086, 1173.7578),
	"l56": ("Light", 653.4541, 1103.1016), "l57": ("Light", 679.834, 1026.8672),
	"l60": ("Light", 51.83008, 1422.6816), "l61": ("Light", 140.15039, 1487.7598), "l62": ("Light", 391.74707, 496.7129),
	"l63": ("Light", 391.9795, 429.31055), "l64": ("Light", 392.2119, 349.82227), "l65": ("Light", 186.05371, 473.70312),
	"l66": ("Light", 162.34668, 408.625), "l67": ("Light", 133.75879, 332.39062),
	"l70": ("Light", 292.38672, 1055.9199), "l71": ("Light", 351.6543, 1055.9199), "l72": ("Light", 336.40625, 1331.3398),
	"l73": ("Light", 431.4668, 1331.3398), "l74": ("Light", 526.0625, 1331.3398), "l75": ("Light", 384.05273, 1279.5098),
	"l76": ("Light", 478.88086, 1279.7422), "l77": ("Light", 431.23438, 1226.75),
	"l81": ("Light", 417.94885, 1122.0284), "l82": ("Light", 476.4181, 1139.1476), "l83": ("Light", 532.5166, 1156.0042),
	"l91": ("Light", 430.91016, 813.0117), "l92": ("Light", 414.64062, 850.1992), "l93": ("Light", 436.7207, 885.2949),
	"l100": ("Light", 630.56055, 1487.5273), "l101": ("Light", 724.9238, 1487.7598), "l102": ("Light", 813.24414, 1422.6816),
	"l103": ("Light", 628.9336, 1392.4668), "l104": ("Light", 688.2012, 1421.2871), "l105": ("Light", 658.6836, 1333.8965),
	"l106": ("Light", 718.416, 1362.7168), "l107": ("Light", 720.5078, 1283.4609),
	"Bulb1": ("Light", 153.0, 1685.0), "Bulb2": ("Light", 691.0, 1697.0), "Bulb3": ("Light", 209.5, 1594.5),
	"Bulb4": ("Light", 657.0, 1594.5), "Bulb5": ("Light", 49.5, 1224.5), "Bulb6": ("Light", 74.0, 1057.0),
	"Bulb7": ("Light", 762.0, 1002.0), "Bulb8": ("Light", 535.75, 943.75), "Bulb9": ("Light", 823.0, 815.0),
	"Bulb10": ("Light", 669.0, 818.0), "Bulb11": ("Light", 158.5, 639.0), "Bulb12": ("Light", 757.0, 622.0),
	"Bulb13": ("Light", 625.25, 506.5), "Bulb14": ("Light", 815.0, 445.0), "Bulb15": ("Light", 89.5, 390.5),
	"Bulb16": ("Light", 768.0, 312.0), "Bulb17": ("Light", 263.0, 451.0), "Bulb18": ("Light", 288.0, 394.0),
	"Bulb19": ("Light", 297.0, 295.0),
}
# Primitives whose stored position is not the part's centre: the world bounding-box centre of each in the retained
# `export obj --units vpu` (OBJ x and y are playfield x and y), rounded to six decimals.
MESH_POINTS: dict[str, tuple[float, float]] = {
	"LeftKicking": (236.502745, 1551.78445), "RightKicking": (628.99727, 1551.78445), "RMotor": (258.08785, 457.26481),
	"LEDR84": (698.51999, 105.6652), "LEDR85": (752.10285, 153.430315), "LEDR86": (805.84445, 200.832395),
	"LEDR87": (868.33945, 256.60192), "LEDR94": (56.838067, 802.661195), "LEDR95": (88.09173, 781.16167),
	"LEDR96": (125.2763, 754.97985), "LEDR97": (156.061805, 733.32457),
}
# The object the embedded script binds to each playfield switch.
SWITCH_OBJECTS = {
	10: "Bumper1", 11: "Bumper2", 12: "Bumper3", 13: "LeftSlingshot", 14: "RightSlingshot", 15: "sw15", 20: "sw20",
	21: "sw21", 22: "sw22", 23: "Drain", 24: "sw24", 25: "sw25", 31: "sw31", 32: "sw32", 35: "sw35", 80: "sw80",
	81: "sw81", 90: "Gate90", 91: "sw91", 92: "sw92", 93: "sw93", 94: "sw94", 95: "sw95", 100: "sw100", 101: "sw101",
	102: "sw102", 103: "sw103", 104: "sw104",
}
SWITCH_PROJECTIONS = {
	30: ("RMotor", (
		"Projected onto the catapult ramp (Primitive RMotor, world mesh centre), the moving rail the script turns about its "
		"top end and whose home step writes this switch (.AddSw 30, 0, 0); the sensor has no object of its own."
	)),
	33: ("BallRelease", (
		"Projected onto the ball release (Kicker BallRelease), the trough exit the script's four-ball stack kicks from; the "
		"script keeps the trough as a virtual stack and has no object for this switch."
	)),
}
SOLENOID_OBJECTS = {
	1: "Bumper1", 2: "Bumper2", 3: "Bumper3", 4: "LeftKicking", 5: "RightKicking", 6: "sw31", 7: "sw21", 10: "sw25",
	11: "sw22", 12: "sw32", 13: "Perno", 14: "fl14", 15: "fl15", 16: "fl16", 17: "fl17", 18: "l197", 23: "RMotor",
	28: "BallRelease", 29: "Drain",
}
SOLENOID_PROJECTED = {
	4: "the left kicking target it drives (the script's KickingT primitive, which it swings on the target's hit); the coil has no object of its own",
	5: "the right kicking target it drives (the script's KickingT primitive, which it swings on the target's hit); the coil has no object of its own",
	6: "the left hole the script ejects from; the coil has no object of its own",
	7: "the top hole the script ejects from; the coil has no object of its own",
	10: "the bank's middle drop target; the reset coil sits below the bank and has no object of its own",
	11: "the center upkicker the script lifts the ball from; the coil has no object of its own",
	12: "the right upkicker the script ejects from; the coil has no object of its own",
	23: "the catapult ramp its motor turns; the relay and motor have no object of their own",
	28: "the trough exit the script releases balls from; the coil has no object of its own",
	29: "the outhole kicker the script receives drained balls on; the coil has no object of its own",
}
# Flashers placed on the Light under a modelled dome, or a bulb light, rather than on a Flasher sprite.
FLASHER_LIGHTS = {
	14: "Light fl14 under the Flasher24B14 dome", 15: "Light fl15 under the Flasher24B15 dome",
	16: "Light fl16 under the Flasher24B16 dome", 17: "Light fl17 under the Flasher24B17 dome",
	18: "Light l197, a bulb light beside the spinner (the script drives it as its lamp 198)",
}
# Playfield lamps placed on a bulb primitive instead of their Light: the billboard LEDs on the two raised signs.
LAMP_MESH_OBJECTS = {address: f"LEDR{address}" for address in (84, 85, 86, 87, 94, 95, 96, 97)}
# Playfield G.I.: the bulb lights the script drives as its lamp 150, which GIRelay switches with relay 31.
GI_BULBS = tuple(f"Bulb{index}" for index in range(1, 20))


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _uri_path(path: Path) -> str:
	return path.as_posix().replace(" ", "%20").replace("(", "%28").replace(")", "%29")


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Gladiators retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)}
			for path in paths
		],
	}


def _table_object_point(extraction_root: Path, kind: str, name: str) -> tuple[float, float]:
	path = extraction_root / "gameitems" / f"{kind}.{name}.json"
	if not path.is_file():
		raise RuntimeError(f"Gladiators retained table has no {kind} {name}: {path}")
	item = load_json(path)[kind]
	if kind == "Wall":
		points = item["drag_points"]
		return (sum(point["x"] for point in points) / len(points), sum(point["y"] for point in points) / len(points))
	if kind in ("Primitive", "HitTarget"):
		return (item["position"]["x"], item["position"]["y"])
	return (item["center"]["x"], item["center"]["y"])


def _obj_mesh_centres(obj_path: Path, names: set[str]) -> dict[str, tuple[float, float]]:
	bounds: dict[str, list[float]] = {}
	current = None
	with obj_path.open("r", encoding="utf-8", errors="replace") as stream:
		for line in stream:
			if line.startswith(("o ", "g ")):
				current = line[2:].strip() if line[2:].strip() in names else None
			elif current and line.startswith("v "):
				x, y = map(float, line.split()[1:3])
				box = bounds.setdefault(current, [x, x, y, y])
				box[:] = [min(box[0], x), max(box[1], x), min(box[2], y), max(box[3], y)]
	return {name: (round((box[0] + box[1]) / 2, 6), round((box[2] + box[3]) / 2, 6)) for name, box in bounds.items()}


def verify_retained_table(source_root: Path) -> None:
	"""Re-derive every placement literal from the retained table; raise on any difference."""
	table = source_root / TABLE_RELATIVE_PATH
	if not table.is_file() or table.stat().st_size != TABLE_BYTES or _file_sha256(table) != TABLE_SHA256:
		raise RuntimeError(f"Gladiators retained table is missing or not the pinned one: {table}")
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file() or _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Gladiators retained extraction manifest is missing or not the pinned one: {manifest_path}")
	extraction = source_root / EXTRACTION_RELATIVE_PATH
	manifest = load_json(manifest_path)
	if canonical_bytes(manifest) != canonical_bytes(build_extraction_manifest(extraction)):
		raise RuntimeError("Gladiators retained extraction does not match its manifest")
	if len(manifest["files"]) != EXTRACTION_FILE_COUNT or sum(item["size"] for item in manifest["files"]) != EXTRACTION_TOTAL_BYTES:
		raise RuntimeError("Gladiators retained extraction file count or byte total is not the pinned one")
	if _file_sha256(extraction / "script.vbs") != EMBEDDED_SCRIPT_SHA256:
		raise RuntimeError("Gladiators retained table's embedded script is not the pinned one")
	for name, (kind, x, y) in TABLE_POINTS.items():
		if _table_object_point(extraction, kind, name) != (x, y):
			raise RuntimeError(f"Gladiators table point {name} does not match the retained {kind}")
	obj = source_root / OBJ_RELATIVE_PATH
	if not obj.is_file() or _file_sha256(obj) != OBJ_SHA256:
		raise RuntimeError(f"Gladiators retained OBJ export is missing or not the pinned one: {obj}")
	if _obj_mesh_centres(obj, set(MESH_POINTS)) != MESH_POINTS:
		raise RuntimeError("Gladiators mesh points do not match the retained OBJ export")


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def shown(address: int) -> str:
	"""How the service tests print an address: 00-97, then A0-A7 and B0-B7 for 100-117."""
	return f"{address:02d}" if address < 100 else ("A" if address < 110 else "B") + str(address % 10)


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


TABLE_REFS = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, SCRIPT_SOURCE)


def norm(x: float, y: float) -> tuple[float, float]:
	"""Normalize a retained-table coordinate (VPX units) into the canonical playfield space."""
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


def object_point(name: str) -> tuple[float, float]:
	if name in MESH_POINTS:
		return MESH_POINTS[name]
	_, x, y = TABLE_POINTS[name]
	return (x, y)


def object_label(name: str) -> str:
	return f"Primitive {name} (world mesh centre)" if name in MESH_POINTS else f"{TABLE_POINTS[name][0]} {name}"


def object_refs(*names: str) -> tuple[str, ...]:
	return TABLE_REFS + ((VPX_OBJ_SOURCE,) if any(name in MESH_POINTS for name in names) else ())


def located(identifier: str, role: str, names: list[str]) -> dict[str, Any]:
	placements = []
	for index, name in enumerate(names, start=1):
		x, y = norm(*object_point(name))
		placements.append({
			"id": f"{identifier}.{role}" + (f".{index}" if len(names) > 1 else ""), "role": role, "space": "playfield",
			"x": x, "y": y, "provenance": provenance(*object_refs(name), status="observed"),
		})
	return {"status": "observed", "placements": placements}


def _excerpt(identifier: str, locator: str, filename: str, method: str, transcribed_by: str, reviewed: bool = True) -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	return {
		"id": identifier, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path),
		"method": method, "transcribed_by": transcribed_by, "reviewed": reviewed,
	}


def source_records() -> list[dict[str, Any]]:
	script_path = "Gladiators%20%28Premier%201993%29%20v1.1.1/Gladiators%20%28Premier%201993%29%20v1.1.1.vbs"
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned PinmameGetGames catalog record for gladiatr, a root driver with no clones",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/gts3games.c lines 9 (DMD = GTS3_dispDMD), 18 (FLIP8283 = FLIP_SWNO(82,83)), 21 (GTS3_dispDMD, one "
				"32x128 CORE_DMD), 56-61 (INITGAME2: core_tGameData {GEN_GTS3, disptype, {flippers, 4, lamps, 0, sb, 0}} and "
				"GTS32_INPUT_PORTS_START) and 505-516 (the Gladiators #737 block: INITGAME2(gladiatr, DMD, FLIP8283, 4, "
				"SNDBRD_GTS3, 4), its ROM set and CORE_GAMEDEFNV(gladiatr) on mGTS3DMDS); src/wpc/gts3.h line 55 "
				"GTS32_COMPORTS (coins 0-3, Start 4, Tournament 5 and Front Door 6 toggles, flag 0x8000), lines 101 "
				"(GTS3_SOLSMOOTH 4) and 108-111 (GTS3_SWDIAG -8, GTS3_SWTILT -7, GTS3_SWSLAM -6, GTS3_SWPRIN -5); "
				"src/wpc/gts3.c xvia_0_a_r (the matrix returns read as ~core_getSwCol), dmd_u4_pb_r (test and tilt, not "
				"inverted), xvia_0_b_w (twelve-column lamp and switch strobe), line 467 (GTS3_interface_update calls "
				"core_updateSw with solenoid 32 as the flipper enable), lines 493-500 (gts3_sw2m/gts3_m2sw), lines 665-672 "
				"(gts3dmd_init: nGI = 0, nLamps = 64 + lampCol * 8, outputs 26/31/32 typed as the A and T relays and Q game-on) "
				"and 708-715 (the gladiatr block: outputs 8-9, 14-22 and 24 typed as #89 'Playfield & Backbox flashers', "
				"lamps 2-7 'WEAPON' LEDs, 12-17 'DOUBLE' LEDs and 94-97 'Left Billboard LEDs'); src/wpc/core.c core_updateSw "
				"(flipSwCol 15 for GEN_GTS3, the FLIP_SWNO copy and synthetic 45-48) and core_getAllSol; src/wpc/gen.h "
				"GEN_GTS3 0x0020000000000"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/gts3.json", "revision": "repository",
			"locator": "Gottlieb System 3 decimal switch and lamp numbering, cabinet test inputs -8 to -5, the cabinet port on 0-6, the 140-147 flipper column, solenoids 1-32 and synthetic 45-48, and the auxiliary-board lamps 120-127",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=1011",
			"revision": "live page 2026-10-30", "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-30T12:00:00Z",
			"locator": (
				"IPDB machine 1011 'Gladiators' (Premier Technology, trade name Gottlieb, November 1993, model 737, Gottlieb "
				"System 3, 1,995 units), opened in a browser that cleared the site's Cloudflare check and saved as rendered "
				"(retained as manuals/by-machine/gottlieb.gladiators.1993/ipdb/ipdb-1011-page-rendered.html). It lists the "
				"instruction manual pages and the coil, fuse and switch charts as 'Availability limited by copyright' without a "
				"link. The title, manufacturer, model number 737 (which the ROM's power-up screen prints as Game #737) and the "
				"System 3 MPU match the machine being curated."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [
				_excerpt("excerpt.gladiators.ipdb-page", "IPDB machine 1011 page, saved 2026-10-30", "ipdb-page.md", "manual", "curator, read from the retained HTML"),
			],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(RUNTIME_EVIDENCE_PATH),
			"locator": (
				"Pinned LibPinMAME runs of gladiatr, each from a new state directory holding only the factory-settings NVRAM: "
				"the Lamp Matrix, Relay & Solenoid and Switch Matrix self-tests, each step paired with the public address it "
				"drove or the host held and with the text the DMD showed, read glyph by glyph by tools/gts3_dmd_text.py, plus "
				"the Front Door Test, a tournament and coin-door probe, one scripted game and a mechanism-sensor run. Raw "
				"runs, DMD frames, NVRAM and the manifest are retained outside the repository."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes, NVRAM and DMD frames remain external",
		},
		{
			"id": SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{STANDALONE_REVISION}/{script_path}",
			"revision": STANDALONE_REVISION, "original_filename": "Gladiators (Premier 1993) v1.1.1.vbs", "sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Kiwi's Gladiators (Premier 1993) VPX v1.1.1 table script in the pinned known-working corpus. The recorded "
				f"SHA-256 is the 46,453-byte LF blob at the pinned revision; the local checkout materializes it with CRLF as "
				f"{SCRIPT_CHECKOUT_SHA256}. Runtime authority: cGameName = \"gladiatr\" (line 53), LoadVPM gts3.VBS (line 193), "
				"UseSolenoids = 2 (line 200), the trough, saucer, drop-bank and ramp-motor objects (lines 260-324), the key "
				"handlers (lines 470-524), the switch writers (lines 584-685), the solenoid callbacks (lines 706-871) and "
				"UpdateLamps (lines 940-1204). The retained VR edit of the table embeds the same script with only VR-room "
				"additions, so its bindings are these."
			),
			"license": "NOASSERTION", "attribution": "Kiwi; pinned copy in jsm174/vpx-standalone-scripts", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.gladiators.kiwi-script-bindings", "Gladiators (Premier 1993) v1.1.1.vbs lines 53-1204, controller bindings", "kiwi-script-bindings.md", "manual", "curator, read from the pinned script"),
			],
		},
		{
			"id": OLDER_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{TABLE_SCRIPTS_REVISION}/Gladiators%20%28Premier%201993%29%20v1.0.1.vbs",
			"revision": TABLE_SCRIPTS_REVISION, "original_filename": "Gladiators (Premier 1993) v1.0.1.vbs", "sha256": OLDER_SCRIPT_SHA256,
			"locator": (
				"Kiwi's earlier v1.0.1 script of the same table in the second pinned corpus. Same author and lineage as v1.1.1, "
				"so it corroborates and never independently confirms; it is cited only for that."
			),
			"license": "NOASSERTION", "attribution": "Kiwi; pinned copy in sverrewl/vpxtable_scripts", "rights": "NOASSERTION",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{_uri_path(TABLE_RELATIVE_PATH)}",
			"original_filename": TABLE_FILENAME, "sha256": TABLE_SHA256, "acquired_at": "2026-10-30T15:58:00Z",
			"locator": (
				f"Retained VR edit of Kiwi's Gladiators (Premier 1993) VPX v1.1.1 ({TABLE_BYTES:,} bytes; script header \"VR room "
				"added by MaX in 2024 with permission\"), copied on 2026-10-30 from the contributor's table collection, where "
				"the file is dated 2024-04-06. Its embedded script "
				f"(SHA-256 {EMBEDDED_SCRIPT_SHA256}) differs from the pinned v1.1.1 script only by the VR-room additions, so it "
				"binds every controller address to the same objects; line numbers differ. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952 and y/2162. Geometry authority for script-bound table objects."
			),
			"license": "NOASSERTION", "attribution": "Kiwi; VR room by MaX", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt(
					"excerpt.gladiators.vpx-table-objects", "gameitems/*.json and the OBJ export, placed objects and their bindings",
					"vpx-table-objects.md", "mixed", "curator, generated from the retained extraction and checked against an overlay on the playfield image",
				),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{_uri_path(EXTRACTION_MANIFEST_RELATIVE_PATH)}",
			"sha256": EXTRACTION_MANIFEST_SHA256, "acquired_at": "2026-10-30T16:02:52Z",
			"locator": (
				f"Retained {VPXTOOL_VERSION} extraction of the VR table, {EXTRACTION_FILE_COUNT} files and "
				f"{EXTRACTION_TOTAL_BYTES:,} bytes, with a full sorted path/size/SHA-256 manifest whose own SHA-256 is this "
				f"record's sha256. Bounds are {TABLE_BOUNDS}. A Wall is placed at the mean of its drag points, a HitTarget or "
				"Primitive at its stored position, every other object at its stored centre."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_OBJ_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{_uri_path(OBJ_RELATIVE_PATH)}",
			"sha256": OBJ_SHA256, "acquired_at": "2026-10-30T16:04:35Z",
			"locator": (
				f"{VPXTOOL_VERSION} `export obj --units vpu` of the VR table, the world-space mesh of every object (OBJ x is "
				"playfield x, OBJ y is playfield y). Used only for primitives whose stored position is not the part's centre: "
				"the kicking targets LeftKicking and RightKicking, the catapult ramp RMotor (its stored position is the pivot at "
				"the ramp's top end) and the billboard LED bulbs LEDR84-87 and LEDR94-97, each placed at its world bounding-box "
				"centre. Control: the same export's apron LED bulb LEDR2 centres at (78.50004, 1886.0), within 0.0001 units of "
				"its stored position (78.5, 1886.0), which is also Light l2's centre."
			),
			"license": "NOASSERTION", "attribution": "vpxtool export of the retained table",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "gts3.vbs", "sha256": VPM_GTS3_SHA256,
			"locator": (
				"The VPinMAME script library the known-working script loads (LoadVPM \"01560000\", \"gts3.VBS\", 3.26), retained "
				f"with core.vbs (SHA-256 {VPM_CORE_SHA256}). GTS3.VBS defines swLRFlip = 141, swLLFlip = 143, swTilt = -7 and "
				"GameOnSolenoid = 32 and writes the flipper addresses from the flipper keys in vpmKeyDown/vpmKeyUp; core.vbs "
				"defines sLRFlipper = 46 and sLLFlipper = 48 and the vpmNudge TiltSwitch pulse."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.gladiators.vpm-script-library", "gts3.vbs lines 21-123 and core.vbs lines 1120-2865", "vpm-script-library.md", "manual", "curator, read from the library files"),
			],
		},
	]


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
		"aliases": [{"namespace": "pinmame.switch" if group == "pinmame.input.switch" else ("pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.coil"), "value": str(address)}],
	}
	device.update(extra)
	return device


READ_PATH_NOTE = (
	" Gladiators' game data sets no inverted-switch mask and gts3.c's xvia_0_a_r hands the CPU the complement of the "
	"matrix column, so public 1 is the closed contact the CPU sees, and the Switch Matrix Test reads ALL SWITCHES OPEN "
	"with every address at 0: the matrix contact rests open and closes when the device is actuated."
)
MATRIX_TEST_NOTE = (
	" In the Switch Matrix Test, holding public {address} at 1 alone displayed SWITCH:{shown} and the ROM's name "
	"\"{name}\" (run switch-matrix)."
)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	cabinet = {
		-8: ("Test (Diagnostic) Button", "service.test", "button", (
			"GTS3_SWDIAG on the cabinet port (internal column 0), read through dmd_u4_pb_r on VIA U4 PB3 without inversion. "
			"Every retained self-test run enters and steps the tests with it: two presses at 1 bring up TEST MODE and the "
			"menu, and each further press steps to the next self-test (runs lamp-matrix, solenoids, switch-matrix, front-door)."
		), (RUNTIME_SOURCE,)),
		-7: ("Tilt", "cabinet.tilt", "tilt", (
			"GTS3_SWTILT on the cabinet port, read through dmd_u4_pb_r on VIA U4 PB4 without inversion. Held at 1 inside the "
			"Switch Matrix Test it replaced the test screen with TILT (run switch-matrix), so the ROM reads it active at 1. "
			"GTS3.VBS names it swTilt = -7. The known-working script sets vpmNudge.TiltSwitch = 151 (line 255), which is not "
			"this address or any address System 3 publishes, so its nudge tilt pulses nothing the ROM reads: a defect in that "
			"table."
		), (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE, SCRIPT_SOURCE)),
		-6: ("Slam Tilt", "cabinet.slam-tilt", "tilt", (
			"GTS3_SWSLAM on the cabinet port, read through VIA U4 CA1 on the DMD generation. A pulse at 1 inside the Front "
			"Door Test reset the game to attract mode (GAME OVER, run front-door), so the ROM reads it active at 1. GTS3.VBS "
			"names it swSlamTilt = -6."
		), (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE)),
	}
	for address, (label, role, switch_type, notes, refs) in cabinet.items():
		items.append(_device(
			f"switch.cabinet-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used", core + refs,
			roles=[role], normally_closed=False,
			physical={"location": "coin door and cabinet", "switch_type": switch_type, "notes": notes},
			spatial=not_applicable("cabinet_or_service", *core),
		))
	items.append(_device(
		"switch.cabinet-5", "Communications Adapter Present", "virtual", "pinmame.input.switch", -5, "optional", core + (RUNTIME_SOURCE,),
		physical={
			"location": "CPU board auxiliary connector (optional communications adapter)",
			"notes": (
				"GTS3_SWPRIN, which PinMAME reads back into the printer status that aux1_r returns for the optional "
				"communications adapter (printer) on the CPU board's auxiliary connector: at 1 the status reads ready, at 0 "
				"not connected. It is not a matrix switch, and held at 1 inside the Switch Matrix Test it put no SWITCH line of "
				"its own on the display (run switch-matrix). A recreation without the adapter leaves it at 0."
			),
		},
		spatial=not_applicable("virtual", *core),
	))
	for address in MATRIX_ADDRESSES:
		identifier = f"switch.matrix-{address}"
		column, row = divmod(address, 10)
		if address in UNUSED_SWITCHES:
			items.append(_device(
				identifier, f"Not Used (Matrix Position {address})", "switch", "pinmame.input.switch", address, "unused",
				core + (RUNTIME_SOURCE,),
				physical={"notes": (
					f"Strobe {column}, return {row}." + MATRIX_TEST_NOTE.format(address=address, shown=shown(address), name="(NOT USED)")
					+ " The ROM scans the position and calls it unused; the known-working script never writes it."
				)},
				spatial=not_applicable("unused", CORE_SOURCE, RUNTIME_SOURCE),
			))
			continue
		label = SWITCH_LABELS[address]
		notes = f"Strobe {column}, return {row}."
		if address in ROM_SWITCH_NAMES:
			if address in FLIP_SWNO:
				notes += (
					f" In the Switch Matrix Test, holding the flipper button {143 if address == 82 else 141} at 1 displayed "
					f"SWITCH:{address} and the ROM's name \"{ROM_SWITCH_NAMES[address]}\" (run switch-matrix)."
				)
			else:
				notes += MATRIX_TEST_NOTE.format(address=address, shown=shown(address), name=ROM_SWITCH_NAMES[address])
		refs: tuple[str, ...] = core + (RUNTIME_SOURCE,)
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {}
		if address in ROM_RUNTIME:
			notes += f" In play, {ROM_RUNTIME[address]}."
		if address in SCRIPT_WRITERS:
			notes += f" The known-working script treats it as actuated at 1: {SCRIPT_WRITERS[address]}."
			refs += (SCRIPT_SOURCE,)
		notes += READ_PATH_NOTE
		if address in OPTO_SWITCHES:
			physical["switch_type"] = "opto"
			notes += " The ROM's own name marks it as an opto; the matrix contact rests open by the read-path rule above, whatever the beam does."
		if address in CABINET_SWITCH_TYPES:
			physical["switch_type"] = CABINET_SWITCH_TYPES[address]
		if address == 4:
			notes += (
				" The Switch Matrix Test was not asked about it: Start is one of the self-tests' own controls. Lamp 1 is the "
				"button's lamp, which the Lamp Matrix Test names CREDIT BUTTON. GTS32_COMPORTS calls it START1, and GTS3.VBS "
				"writes it from the start key (swStartButtonX = 4)."
			)
			refs += (VPM_LIBRARY_SOURCE,)
		if address == 5:
			notes += (
				" A service button inside the coin door. Closed at 1 in attract mode it changed nothing on the display, and a "
				"game started with it held at 1 began as an ordinary game (run tournament-door), so these runs do not show what "
				"the ROM's tournament mode needs. The known-working script never writes it."
			)
		if address == 6:
			notes += (
				" The ROM names it the front door (service) switch. The game took coins with it at either level "
				"(run tournament-door held it at 1 while coining and opened it before Start; run gameplay left it at 0), and no retained source shows "
				"which door position closes the contact. The known-working script never writes it."
			)
		if address in (0, 1, 2, 3):
			notes += (
				f" The Front Door Test counts it as coin chute {address + 1}. GTS3.VBS names it swCoin{address + 1} = {address:02d}, "
				"and GTS32_COMPORTS rewrites it from a coin key only with PinMAME keyboard handling on."
			)
			refs += (VPM_LIBRARY_SOURCE,)
		if address in FLIP_SWNO:
			button = 143 if address == 82 else 141
			notes += (
				f" The driver declares FLIP_SWNO(82,83) with no FLIP_SOL, so core_updateSw copies the {'left' if address == 82 else 'right'} "
				f"flipper button from PinMAME's flipper column (public {button}) into this switch on every update; it cannot be "
				f"driven directly, because a host write here is overwritten on the next update. Drive {button}. The ROM's name "
				"says the switch comes from the flipper sensor board. The known-working script also writes "
				f"{address} from the flipper key before calling vpmKeyDown/vpmKeyUp, which writes {button} (lines "
				f"{471 if address == 82 else 472} and {498 if address == 82 else 499}): a defect with no effect, since the copy "
				"overwrites it. Its BumpersDisable turns the pop bumpers' hit events off while it reads both 82 and 83 at 1 "
				"(lines 515-524), a table behaviour, not the machine's."
			)
			refs += (SCRIPT_SOURCE, VPM_LIBRARY_SOURCE)
		if address in (13, 14):
			notes += (
				" The ROM calls it a kicking target and fires its own coil from it; the known-working script models it as the "
				f"{'left' if address == 13 else 'right'} slingshot. The retained table draws a kicking target there, Primitive "
				f"{'LeftKicking' if address == 13 else 'RightKicking'} (mesh KickingT), which the script swings when the slingshot "
				"wall is hit, so the part is a kicking target in the slingshot position; no manual confirms it."
			)
		if address in (21, 22, 31, 32):
			notes += f" The ROM's coil {dict(((21, 7), (22, 11), (31, 6), (32, 12)))[address]} kicks the ball out (run gameplay, above)."
		if address == 23:
			notes += " The machine holds four balls (the power-up screen reads Install 4 Balls; the script's bsTrough holds four, line 266)."
		if address == 30:
			notes += (
				" It senses the catapult ramp's home position: the script's ramp mechanism, driven by RAMP MOTOR RELAY (B) (23), "
				"closes it at its start step. In the retained runs the ROM did not release 23 when the host changed 30, and "
				"held at 1 in attract mode it drew no response, so the runs do not show how the ROM uses it."
			)
		if address in SWITCH_OBJECTS:
			name = SWITCH_OBJECTS[address]
			notes += f" Placed at the retained table's {object_label(name)}, which the script binds to this address."
			extra["spatial"] = located(identifier, "sensor", [name])
			refs += tuple(ref for ref in object_refs(name) if ref not in refs)
		elif address in SWITCH_PROJECTIONS:
			name, reason = SWITCH_PROJECTIONS[address]
			notes += f" {reason}"
			extra["spatial"] = located(identifier, "sensor", [name])
			refs += tuple(ref for ref in object_refs(name) if ref not in refs)
		physical["notes"] = notes
		if address in CABINET_SWITCH_ROLES:
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			physical["location"] = "coin door and cabinet" if address in (0, 1, 2, 3, 4, 5, 6) else "matrix copy of the cabinet flipper button"
			extra["spatial"] = not_applicable("cabinet_or_service", *core)
		extra["normally_closed"] = False
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", refs, physical=physical, **extra))
	items += flipper_column_inputs()
	return items


FLIPPER_COLUMN = (
	(140, "CORE_SWLRFLIPEOSBIT", 0x01, "Lower Right", "right", "eos"),
	(141, "CORE_SWLRFLIPBUTBIT", 0x02, "Lower Right", "right", "button"),
	(142, "CORE_SWLLFLIPEOSBIT", 0x04, "Lower Left", "left", "eos"),
	(143, "CORE_SWLLFLIPBUTBIT", 0x08, "Lower Left", "left", "button"),
	(144, "CORE_SWURFLIPEOSBIT", 0x10, "Upper Right", "right", "eos"),
	(145, "CORE_SWURFLIPBUTBIT", 0x20, "Upper Right", "right", "button"),
	(146, "CORE_SWULFLIPEOSBIT", 0x40, "Upper Left", "left", "eos"),
	(147, "CORE_SWULFLIPBUTBIT", 0x80, "Upper Left", "left", "button"),
)


def flipper_column_inputs() -> list[dict[str, Any]]:
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	matrix = {"left": FLIP_SWNO[0], "right": FLIP_SWNO[1]}
	items: list[dict[str, Any]] = []
	for address, constant, bit, position, side, kind in FLIPPER_COLUMN:
		base = (
			f"PinMAME flipper switch column (internal column 15, which core_updateSw uses for GEN_GTS3), bit {constant} = "
			f"0x{bit:02X}, published at {address} through gts3_m2sw(15, row) = 140 + row."
		)
		if address in (141, 143):
			notes = (
				f"{base} This is the {side} cabinet flipper button as the ROM receives it. The driver declares FLIP_SWNO(82,83) "
				"with no FLIP_SOL, so with keyboard handling off (the LibPinMAME default) core_updateSw reads this bit as the host "
				f"wrote it, copies it into matrix switch {matrix[side]} on every update and fabricates the synthetic "
				f"{'45/46' if side == 'right' else '47/48'} flipper outputs from it while the game-over relay (32) is energized. "
				f"Drive this address, not {matrix[side]}. In the self-tests it is the menu's "
				f"{'select' if side == 'right' else 'step'} control (TEST MODE screen: L FLIPPER TO STEP, R FLIPPER TO SELECT); "
				+ ("every retained self-test run pressed it there, and each press in the Relay & Solenoid Test, which energizes "
				"32, raised 45 and 46 (run solenoids)" if side == "right" else "the nvram-init run pressed it there to reach GAME "
				"ADJUSTMENTS, and no retained run pressed it while 32 was on, so 47 and 48 were never observed")
				+ f". GTS3.VBS names it swL{'R' if side == 'right' else 'L'}Flip = {address} and writes it from the flipper key in "
				"vpmKeyDown/vpmKeyUp, which the known-working script calls. The machine's buttons are two-stage (IPDB: a light "
				"press works the lower flipper, a heavy press the lower and upper), but the ROM reads one switch per side, so "
				"this address is the button's first stage."
			)
			items.append({
				"id": f"switch.flipper-column-{address}",
				"label": f"{position} Flipper Button (PinMAME Flipper Column)",
				"kind": "switch",
				"binding": {"group": "pinmame.input.switch", "device": address},
				"availability": "used",
				"provenance": provenance(*core, RUNTIME_SOURCE, VPM_LIBRARY_SOURCE, IDENTITY_SOURCE),
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"roles": [f"flipper.lower.{side}.button"],
				"normally_closed": False,
				"physical": {"location": "cabinet flipper button", "switch_type": "button", "notes": notes},
				"spatial": not_applicable("cabinet_or_service", *core),
			})
			continue
		if kind == "eos":
			reason = (
				"locals.flipMask carries this end-of-stroke bit only when hw.flippers sets FLIP_EOS, and FLIP_SWNO(82,83) does "
				"not, so core_updateSw neither synthesizes it nor copies it anywhere: PinMAME models no end-of-stroke switch on "
				"this machine."
			)
		else:
			reason = (
				"core_updateSw copies only the two lower button bits into the matrix and the synthetic outputs; this upper-button "
				"bit would join locals.flipMask only if hw.flippers set the matching upper FLIP_SW bit, which FLIP_SWNO(82,83) "
				"does not. The upper flippers' heavy-press stage (IPDB) never reaches the CPU."
			)
		reason += (
			" A host write survives in the column, but the ROM cannot read it there: xvia_0_a_r reads the matrix only through "
			"core_getSwCol with the twelve-bit lamp/switch strobe, which reaches internal columns 1-12."
		)
		items.append({
			"id": f"switch.flipper-column-{address}",
			"label": f"Unused Flipper Column {position} {'End-of-Stroke' if kind == 'eos' else 'Button'} ({address})",
			"kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": address},
			"availability": "unused",
			"provenance": provenance(*core, *((IDENTITY_SOURCE,) if kind == "button" else ())),
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"physical": {"location": "internal public address space", "switch_type": "other", "notes": f"{base} {reason}"},
			"spatial": not_applicable("unused", *core),
		})
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	for address in range(1, 33):
		driver = address - 1
		name = ROM_COIL_NAMES[address]
		notes = (
			f"The Relay & Solenoid Test names driver {driver} \"{name}\", and the credit button fired public {address} there "
			"(run solenoids; the displayed driver number is the public address minus one)."
		)
		refs = core + (RUNTIME_SOURCE,)
		if address in SOLENOID_RUNTIME:
			notes += f" In play it {SOLENOID_RUNTIME[address]}."
		if address in GAMEPLAY_GAPS:
			notes += " " + GAMEPLAY_GAPS[address]
		if address in SOLENOID_CALLBACKS:
			notes += f" The known-working script binds SolCallback({address}) to {SOLENOID_CALLBACKS[address]}."
			refs += (SCRIPT_SOURCE,)
		if address in (1, 2, 3, 4, 5):
			notes += (
				" The CPU fires it from its switch: the ROM, not a separate special-solenoid circuit, closes the loop, so a "
				"consumer only drives the switch. The known-working script assigns no callback to it and kicks the ball with "
				"the table's own bumper and slingshot physics (lines 584-623)."
			)
			refs += (SCRIPT_SOURCE,)
		if address in FLASHER_SOLENOIDS:
			notes += (
				" The ROM's name ends in 67, the #67 flasher bulb; PinMAME's gladiatr block (gts3.c lines 708-715) models it as a "
				"#89 bulb among its 'Playfield & Backbox flashers'."
			)
			if address in SCRIPT_BACKBOX_FLASHERS:
				notes += (
					f" The known-working script drives its lamp {SCRIPT_BACKBOX_FLASHERS[address]} from it (SolCallback line "
					f"{706 + address - 6 if address < 23 else 724}) and draws that lamp in its backbox section, at backbox height "
					"(lines 374-390 and 1143-1159), as the backglass art the name describes; no manual confirms the location, so "
					"the output is not placed."
				)
			else:
				notes += (
					f" The known-working script drives its flasher lamp {194 + address - 14 if 14 <= address <= 19 else 190 + address - 20} "
					"from it and draws it with the playfield flashers (lines 714-721 and 1121-1141)."
				)
			refs += (SCRIPT_SOURCE,)
		if address == 13:
			notes += (
				" The ROM pulsed it at Start and fired no ball release (28) until after the drain (run gameplay). The host "
				"supplied the shooter-lane switches itself, so the run does not show where the first ball of a game waits."
			)
		if address == 23:
			notes += (
				" The relay switches the motor of the catapult, the moving rail ramp (IPDB). The known-working script's mRMotor "
				"mechanism runs while it is on (vpmMechOneSol + vpmMechReverse, 136 steps) and reports the ramp's home at switch "
				"30 (lines 313-324); SolCallback(23) is commented out (line 723)."
			)
			refs += (SCRIPT_SOURCE, IDENTITY_SOURCE)
		if address == 25:
			notes += " IPDB lists a shaker motor among the machine's features; it sits in the cabinet."
			refs += (IDENTITY_SOURCE,)
		if address == 26:
			notes += " PinMAME's System 3 init types it as the 'A' relay: lightbox insert (backbox) illumination."
		if address == 27:
			notes += (
				" An optional cabinet accessory output: the known-working script assigns no callback to it and no gameplay run "
				"published it."
			)
			refs += (SCRIPT_SOURCE,)
		if address == 31:
			notes += (
				" PinMAME's System 3 init types it as the 'T' relay, general illumination. The ROM calls it the tilt relay: it "
				"switches the playfield G.I. off when energized, which the known-working script reproduces. The placements are "
				f"the {len(GI_BULBS)} bulb lights Bulb1-Bulb{len(GI_BULBS)} of the retained table, which the script's GIRelay "
				"switches with this relay; without a manual no G.I. bulb count or layout is known, and a table's grouping is not "
				"the machine's wiring, so they stay observed without a quantity."
			)
			refs += (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		if address == 32:
			notes += (
				" PinMAME's System 3 init types it as the 'Q' relay, game on, and passes its state to core_updateSw as the "
				"flipper enable: the synthetic flipper outputs 45-48 follow the buttons only while it is on. The Relay & "
				"Solenoid Test energizes it while the test runs (runs solenoids, switch-matrix, front-door). GTS3.VBS names it "
				"GameOnSolenoid = 32."
			)
			refs += (VPM_LIBRARY_SOURCE,)
		kind = "flasher" if address in FLASHER_SOLENOIDS else SOLENOID_KIND.get(address, "coil")
		availability = "optional" if address == 27 else "used"
		identifier = f"device.{slug(SOLENOID_LABELS[address])}"
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {}
		if address in CABINET_SOLENOIDS:
			physical["location"] = CABINET_SOLENOIDS[address]
			extra["spatial"] = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
		elif address in SOLENOID_OBJECTS:
			obj = SOLENOID_OBJECTS[address]
			if address in FLASHER_LIGHTS:
				notes += f" Placed at the retained table's {FLASHER_LIGHTS[address]}."
			elif address in SOLENOID_PROJECTED:
				notes += f" Projected onto {SOLENOID_PROJECTED[address]} ({object_label(obj)})."
			else:
				notes += f" Placed at the retained table's {object_label(obj)}."
			extra["spatial"] = located(identifier, "emitter" if kind == "flasher" else "effect", [obj])
			refs += tuple(ref for ref in object_refs(obj) if ref not in refs)
		elif address == 31:
			physical["location"] = "relay in the cabinet or backbox; the placements are the playfield G.I. it switches"
			extra["spatial"] = located(identifier, "emitter", list(GI_BULBS))
		elif address in (19, 20, 21):
			notes += (
				f" The retained table draws it only as the Flasher sprite f{address}, a render helper at the top edge of the "
				"playfield, and models no bulb light or socket for it, so the output is not placed."
			)
			refs += (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		physical["notes"] = notes
		items.append(_device(
			identifier, SOLENOID_LABELS[address], kind, "pinmame.output.solenoid", address,
			availability, refs, physical=physical, **extra,
		))
	synthetic = {
		45: ("Synthetic Lower Right Flipper Power", 141), 46: ("Synthetic Lower Right Flipper Hold", 141),
		47: ("Synthetic Lower Left Flipper Power", 143), 48: ("Synthetic Lower Left Flipper Hold", 143),
	}
	for address, (label, button) in synthetic.items():
		items.append(_device(
			f"device.{slug(label)}", label, "virtual", "pinmame.output.solenoid", address, "used", core + (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE),
			roles=["internal.synthetic-flipper"],
			physical={"notes": (
				f"PinMAME fabricates it from the flipper button at public {button} (core_updateSw, CORE_FIRSTLFLIPSOL = 45) while "
				"the game-over relay 32 is energized, and core_getAllSol publishes the power and hold outputs of a pair together. "
				f"Gladiators' flippers are cabinet-wired (FLIP_SWNO(82,83), no FLIP_SOL), so no CPU driver stands behind it. "
				+ (
					"Each press of 141 in the Relay & Solenoid Test, which energizes 32, raised the pair for the press (run "
					"solenoids); in the scripted game 32 stayed off until the drain and the presses raised nothing."
					if button == 141 else
					"No retained run pressed 143 while 32 was energized, so the pair was never observed; core_updateSw treats it "
					"exactly as it treats 45/46."
				)
				+ f" core.vbs names the hold output s{'LR' if button == 141 else 'LL'}Flipper = {46 if button == 141 else 48}, and the "
				"known-working script fires both its lower and upper flipper of that side from it (lines 870-886)."
			)},
			spatial=not_applicable("virtual", *core),
		))
	return items


def _lamp_label(address: int) -> str:
	name = ROM_LAMP_NAMES[address]
	prefix, quote, insert = name.partition("\"")
	insert = insert.rstrip("\"")
	words = [WORD_EXPANSIONS.get(word, word.capitalize() if not re.fullmatch(r"#?\d+[A-Z]*", word) else word) for word in prefix.split()]
	if not quote:
		return " ".join(words)
	text = " ".join(word.capitalize() if not re.fullmatch(r"\d+[MKX]?|E\.B\.|ACU-SPIN", word) else word for word in insert.split())
	return f"{' '.join(words)} \"{text}\"".strip() if words else text


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	for address in LAMP_ADDRESSES:
		column, row = divmod(address, 10)
		identifier = f"lamp.matrix-{address}"
		if address not in ROM_LAMP_NAMES:
			items.append(_device(
				identifier, f"Not Used (Lamp {address})", "lamp", "pinmame.output.lamp", address, "unused", core + (RUNTIME_SOURCE, SCRIPT_SOURCE),
				physical={"notes": (
					f"Strobe {column}, row {row}. The Lamp Matrix Test steps through LAMP:{shown(address)} and names it (NOT USED); "
					"the known-working script binds no lamp to it."
				)},
				spatial=not_applicable("unused", CORE_SOURCE, RUNTIME_SOURCE),
			))
			continue
		name = ROM_LAMP_NAMES[address]
		notes = (
			f"Strobe {column}, row {row}. In the Lamp Matrix Test LAMP:{shown(address)} blinks this public address while the "
			f"display names it {name} (run lamp-matrix); a quoted name is the insert's printed text."
		)
		if address == 64:
			notes += " The ROM prints this name without its closing quote."
		refs = core + (RUNTIME_SOURCE,)
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {}
		if address in LED_LAMPS:
			notes += (
				f" PinMAME's gladiatr block types it as a strobed LED among its {LED_LAMPS[address]} (CORE_MODOUT_LED_STROBE_1_10MS, "
				"gts3.c lines 712-714); the known-working script lights an LED object LEDR"
				f"{address} beside its lamp."
			)
		if address == 1:
			notes += " The lamp in the cabinet's credit (Start) button; the known-working script binds no object to it."
			physical["location"] = "cabinet"
			extra["spatial"] = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
		elif address in LIGHTBOX_LAMPS:
			notes += (
				f" One of six lightbox lamps behind the backglass. The known-working script flashes its object l{address} in "
				"its backbox section (lines 1145-1150), at backbox height (lines 374-381)."
			)
			physical["location"] = "backbox"
			extra["spatial"] = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
			refs += (SCRIPT_SOURCE,)
		else:
			binding = f"f{address}" if address in SCRIPT_FLASH_LAMPS else f"l{address}"
			notes += f" The known-working script's UpdateLamps binds its object {binding} to it."
			if address in SCRIPT_FLASH_LAMPS:
				notes += " The script draws the billboard lamps as flasher objects (Flashm, lines 1033-1047)."
			obj = LAMP_MESH_OBJECTS.get(address, f"l{address}")
			if address in LAMP_MESH_OBJECTS:
				notes += (
					f" Placed at the retained table's {object_label(obj)}, the LED bulb on the raised billboard the script "
					f"also flashes from this lamp (FlashDL); the f{address} flasher sprite is a render helper."
				)
			elif address in LED_LAMPS:
				notes += (
					f" Placed at the retained table's Light l{address}, which sits on LEDR{address} in the apron card holder."
				)
			else:
				notes += f" Placed at the retained table's Light l{address}."
			extra["spatial"] = located(identifier, "emitter", [obj])
			refs += (SCRIPT_SOURCE,) + tuple(ref for ref in object_refs(obj) if ref != SCRIPT_SOURCE)
		physical["notes"] = notes
		items.append(_device(identifier, _lamp_label(address), "lamp", "pinmame.output.lamp", address, "used", refs, physical=physical, **extra))
	return items


def displays() -> list[dict[str, Any]]:
	return [{
		"id": "display.dmd", "label": "128x32 dot-matrix display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32,
		"physical_location": "cabinet_or_service",
		"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE),
		"provenance": provenance(CORE_SOURCE, RUNTIME_SOURCE),
	}]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
			"provenance": provenance(*refs),
		}

	def coil(address: int) -> str:
		return f"device.{slug(SOLENOID_LABELS[address])}"

	def switch(address: int) -> str:
		return f"switch.matrix-{address}"

	m = (RUNTIME_SOURCE, SCRIPT_SOURCE, CORE_SOURCE)
	return [
		mechanism(
			"mechanism.trough", "Outhole, trough, ball release, shooter lane and plunger gate", "kicker",
			[coil(29), coil(28), coil(13)], [switch(23), switch(33), switch(24), switch(100)],
			"The machine holds four balls (the power-up screen reads Install 4 Balls). A drained ball lands on the OUTHOLE "
			"switch (23); the OUTHOLE coil (29) kicks it into the trough, whose TROUGH switch (33) reports a ball, and the BALL "
			"RELEASE coil (28) feeds the lead ball into the shooter lane, where the SHOOTER LANE ROLLOVER (24) sees it waiting "
			"at the plunger; the SHOOTER LANE (OPTO) (100) sits at the top of the lane, where the retained table puts its "
			"trigger sw100, so it sees the ball after the plunge. The PLUNGER GATE (13) is a post the known-working script "
			"drops while the output is on (lines 740-750). In the scripted game the ROM pulsed 13 at Start and served nothing "
			"from the trough, so the run does not show how the first ball reaches the shooter lane; when 23 rose it reset the 3-bank (10), energized 28 "
			"for about 0.7 s, fired 29 and energized the game-over relay (32) (run gameplay). The script models the trough as "
			"one four-ball stack with entry switch 23 and position switch 33 (lines 260-266).",
			*m,
		),
		mechanism(
			"mechanism.catapult", "Catapult moving rail ramp", "motorized", [coil(23)], [switch(30)],
			"The catapult is a moving rail ramp that must be shot with skill and timing to drop the ball into the Catapult "
			"Hole for 50,000,000 points (IPDB); the lamp matrix carries a CATAPULT 50M insert at the left hole (43) and a "
			"CATAPULT mode insert (73), and the Relay & Solenoid Test names a CATAPULT & BALL flasher (9). RAMP MOTOR RELAY "
			"(B) (23) switches the ramp's motor and RAMP MOTOR (30) senses its home. The known-working script runs the ramp as "
			"a one-solenoid reversing mechanism of 136 steps while 23 is on, with 30 closed at step 0 (lines 313-324), and "
			"swaps which ramp section is collidable as it moves (lines 531-540). The ROM energized 23 in its ball search and "
			"at the drain; opening and closing 30 did not make it release 23 (runs gameplay, mechanism-sensors), so the runs "
			"do not show the ROM's own stop condition.",
			*m, IDENTITY_SOURCE,
		),
		mechanism(
			"mechanism.holes-and-upkickers", "Top hole, left hole, center and right upkickers", "kicker",
			[coil(7), coil(6), coil(11), coil(12)], [switch(21), switch(31), switch(22), switch(32)],
			"Four ball holds: the TOP HOLE (switch 21, coil 7), the LEFT HOLE (switch 31, coil 6), the CENTER UPKICKER (switch "
			"22, coil 11), which the script models as a vertical upkicker, and the RIGHT UPKICKER (switch 32, coil 12). Each "
			"switch held at 1 for 1.5 s during a game made the ROM fire its coil twice, and the ROM's ball search fires all "
			"four with the plunger gate (13) and the ramp motor relay (23) (runs gameplay, mechanism-sensors). The script "
			"models each as a saucer that holds its switch at 1 while the ball sits in it (lines 269-300).",
			*m,
		),
		mechanism(
			"mechanism.3-bank", "3-bank drop targets", "drop_target_bank", [coil(10)], [switch(15), switch(25), switch(35)],
			"Three drop targets, DROP TARGET #1-#3 (15, 25, 35), reset together by 3 BANK RESET (10). The ROM fired the reset "
			"at power-up and when it served a ball after the drain; holding all three down for six seconds during the "
			"first ball drew no reset (run gameplay), so the run does not show when the ROM resets a completed bank in play. "
			"The script's dtBank writes the switches and raises the bank on 10 (lines 307-310 and 757-759).",
			*m,
		),
		mechanism(
			"mechanism.cpu-fired-coils", "Pop bumpers and kicking targets", "other",
			[coil(1), coil(2), coil(3), coil(4), coil(5)], [switch(10), switch(11), switch(12), switch(13), switch(14)],
			"Three pop bumpers (switches 10, 11 and 12, coils 1, 2 and 3) and two kicking targets (switches 13 and 14, coils 4 "
			"and 5), which the known-working script models as the two slingshots. System 3 has no special-solenoid circuit: "
			"the CPU reads each switch and fires its coil (pulses of 10, 11, 12 and 13 during a game fired 1, 2, 3 and 4; 5 "
			"was not observed, which PinMAME's four-frame solenoid smoothing could explain), so a consumer drives only the "
			"switch. The script assigns no callbacks to these coils and kicks with its own physics.",
			*m,
		),
		mechanism(
			"mechanism.flippers", "Four flippers on two two-stage buttons, cabinet-wired", "other", [coil(32)],
			[switch(82), switch(83)],
			"Four flippers (IPDB): a light press on a flipper button works only the lower flipper of that side, a heavy press "
			"the lower and the upper. The cabinet buttons fire them through the flipper circuit while the GAME OVER RELAY (Q, "
			"32) is energized, so no CPU driver appears for them in the solenoid test; PinMAME fabricates 45-48 from the "
			"buttons at 141 and 143 while 32 is on. The ROM reads one switch per side, matrix switches 82 and 83 (named for "
			"the flipper sensor board), which core_updateSw copies from 143 and 141; neither the ROM nor PinMAME sees the heavy "
			"stage. The known-working script fires the upper flipper of each side together with the lower one (lines "
			"870-886), so it does not model the two stages.",
			*m, VPM_LIBRARY_SOURCE, IDENTITY_SOURCE,
		),
		mechanism(
			"mechanism.relays-and-cabinet", "Relays, shaker, knocker and coin meter", "other",
			[coil(26), coil(31), coil(25), coil(30), coil(27)], [],
			"The LIGHTBOX RELAY (A, 26) switches the backbox lightbox illumination and the TILT RELAY (T, 31) the playfield "
			"G.I., which goes out while it is energized (PinMAME's System 3 init types them as the A and T relays; the script "
			"turns its backbox and playfield G.I. off while each is on). The SHAKER MOTOR (25) shakes the cabinet (IPDB lists "
			"it), the KNOCKER (30) is in the cabinet, and TICKET/COIN METER (27) drives an optional ticket dispenser or coin "
			"meter.",
			*m, IDENTITY_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": f"relationship.flipper-column-{button}-to-matrix-{target}", "kind": "direct",
			"source": f"switch.flipper-column-{button}", "destination": f"switch.matrix-{target}",
			"provenance": provenance(CORE_SOURCE, RUNTIME_SOURCE),
		}
		for button, target in ((141, FLIP_SWNO[1]), (143, FLIP_SWNO[0]))
	]


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


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Gladiators", "manufacturer": "Gottlieb", "year": 1993, "kind": "physical_pinball",
			"model_number": "737", "ipdb_id": 1011, "opdb_id": "G4P9q-MLnOY",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE, status="observed")},
		},
		"coverage": {
			"status": STATUS,
			"missing": COVERAGE_MISSING,
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
				"physical_wiring": "unknown", "mechanisms": "observed", "variant_coverage": "validated",
				"recreation_knowledge": "validated", "display_inventory": "validated", "spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.gts3", "hardware_generation": "0x20000000000", "inversion_applied_by_emulator": True},
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
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Gladiators device identifiers are not unique: {duplicates}")
	labels = [device["label"] for device in definition["outputs"] if device["binding"]["group"] == "pinmame.output.lamp"]
	repeated = sorted({label for label in labels if labels.count(label) > 1 and not label.startswith("Not Used")})
	if repeated:
		raise RuntimeError(f"Gladiators lamp labels are not unique: {repeated}")
	return definition


SPATIAL_BLOCKERS = [
	"No factory drawing is retained: IPDB lists the instruction manual pages and the coil, fuse and switch charts without "
	"hosting them, and no other attributable copy was found, so no placement can be checked against the machine's own "
	"switch, lamp or coil location drawings.",
	"Only one table is retained, the VR edit of Kiwi's VPX v1.1.1, and the pinned v1.0.1 script is the same author's "
	"earlier release of it, so no independently built geometry can confirm a placement. Every placement comes from that "
	"table and stays observed.",
	"Solenoid 31 (Tilt Relay, playfield G.I.): the 19 placements are the bulb lights the table's GIRelay switches; a "
	"table's grouping is not the machine's wiring and the bulb count is unknown, so they stay observed without a quantity.",
	"Solenoids 8, 9, 22 and 24 are drawn in the script's backbox and solenoids 19-21 only as flasher sprites, so none of "
	"the seven is placed or classified; the lamps 112-117 are lightbox lamps by the ROM's own names.",
	"Ramp motor switch 30 and trough switch 33 have no table object of their own and are projected onto the catapult ramp "
	"and the ball release.",
]


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs, located_outputs, omitted_inputs, omitted_outputs = [], [], [], []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	statuses: dict[str, int] = {}
	placement_count = 0
	for collection, located_list, omitted in (("inputs", located_inputs, omitted_inputs), ("outputs", located_outputs, omitted_outputs)):
		for device in definition[collection]:
			binding: Any = device["binding"]["device"] if collection == "inputs" else {"group": device["binding"]["group"], "address": device["binding"]["device"]}
			spatial = device.get("spatial")
			if spatial is None:
				omitted.append(binding)
			elif spatial["status"] == "not_applicable":
				(na_inputs if collection == "inputs" else na_outputs).setdefault(spatial["reason"], []).append(binding)
			else:
				located_list.append(binding)
				for item in spatial["placements"]:
					placement_count += 1
					statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1

	def output_key(item: dict[str, Any]) -> tuple[str, int]:
		return (item["group"], item["address"])

	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "observed",
		"blockers": SPATIAL_BLOCKERS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "source_ref": VPX_EXTRACTION_SOURCE},
		"source_hashes": {"embedded_script_sha256": EMBEDDED_SCRIPT_SHA256, "table_sha256": TABLE_SHA256, "obj_export_sha256": OBJ_SHA256},
		"placement_count": placement_count,
		"placement_status_counts": dict(sorted(statuses.items())),
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=output_key),
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(values, key=output_key) for reason, values in sorted(na_outputs.items())},
		"omitted_inputs": sorted(omitted_inputs),
		"omitted_outputs": sorted(omitted_outputs, key=output_key),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, (_, reason) in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto {reason}."} for address, reason in sorted(SOLENOID_PROJECTED.items())]
		),
		"excluded_object_classes": [
			"Bulb<n>a Light doubles of the G.I. bulbs, and Bulb8T15, Bulb8T25 and Bulb8T35 beside the drop targets: Bulb1-Bulb19, the members with a bulb mesh, are the placements",
			"giB1-giB3 and LR1-LR3 Light objects, which model no bulb",
			"Flasher sprites: fgit, the f<n> lamp and flasher overlays, and f19-f21; a sprite is a render helper, not a socket",
			"The l197a companion light the script fades with l197, and the LEDR primitives of the apron LEDs, which sit at their l<n> lights",
			"VR room, cabinet and backbox objects",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Gladiators (Gottlieb, 1993) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at `machines/partial/gottlieb/gladiators-1993.json`; "
		f"its spatial dimension stays open because of the {len(report['blockers'])} spatial blockers below.",
		"",
		f"The geometry source is the retained `{TABLE_FILENAME}`, a VR edit of Kiwi's VPX v1.1.1, SHA-256 `{TABLE_SHA256}`. "
		f"Its embedded script (SHA-256 `{EMBEDDED_SCRIPT_SHA256}`) binds every controller address exactly as the pinned "
		f"known-working v1.1.1 script does. Bounds are `{TABLE_BOUNDS}`; every coordinate is x/952 and y/2162, rounded to at "
		"most six places. `evidence/excerpts/gottlieb.gladiators.1993/vpx-table-objects.md` lists each placed object, its "
		"coordinate and the script lines that bind it, and the curator's `verify_retained_table` re-derives every coordinate "
		"from the retained extraction and OBJ export.",
		"",
		"## Evidence decisions",
		"",
		"- A placement is the table object the script binds to the address: a trigger, target, spinner, gate, kicker, bumper "
		"or slingshot wall for a switch, the `l<n>` light `UpdateLamps` fades for each lamp, the light under each flasher "
		"dome, the object a coil moves or kicks from, and each G.I. bulb light `GIRelay` switches.",
		"- Primitives whose stored position is not the part's centre (the kicking targets, the catapult ramp and the billboard "
		"LED bulbs) are placed at the centre of their world-space mesh from `vpxtool export obj --units vpu`.",
		"- Sensors and coils with no table object of their own are documented projections onto their own mechanism's object.",
		"- Backbox and cabinet devices take controlled `not_applicable` records: the six lightbox lamps, the credit-button "
		"lamp, the lightbox and game-over relays, the shaker motor, the knocker, the coin meter, the cabinet and "
		"flipper-button switches, the test inputs and the DMD.",
		"- No placement is validated: no factory drawing is retained to check it, and only one table is.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		short = "Switch" if entry["group"] == "pinmame.input.switch" else "Solenoid"
		lines.append(f"- {short} {entry['address']}: {entry['reason']}")
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
	lines += ["", "## Excluded table objects", ""] + [f"- {entry}" for entry in report["excluded_object_classes"]]
	lines += ["", "## Blockers", ""] + [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated with a semantic disposition taken from the ROM's own service tests, the "
		"mechanisms are covered, and polarity is settled for every switch by the read path, the ROM's Switch Matrix Test and "
		"the known-working script. Promotion to `author_ready` is refused because every playfield placement rests on one "
		"community table's geometry with nothing independent to check it, so `coverage.missing` is "
		"`[\"spatial_placement\"]`. The instruction manual's switch, lamp and coil location drawings, or a second table built "
		"independently from the machine, would close the gap.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		if STATUS != "author_ready":
			raise RuntimeError(f"refusing to replace the author-ready Gladiators definition with a {STATUS} one: {stale}")
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
		raise RuntimeError(f"Gladiators is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	definition = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Gladiators definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Gladiators seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Gladiators spatial report drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Gladiators spatial review drifted from its deterministic curator: {markdown_path}")
	print("Gladiators definition, seed, and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed and the spatial report")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
