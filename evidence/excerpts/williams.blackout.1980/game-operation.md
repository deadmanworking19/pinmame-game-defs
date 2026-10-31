# Williams Blackout (game 495) - Board requirements, game operation and power turn-on

Sources:

- Instruction Booklet 16P-495-103 (`Williams_1980_Blackout_Operators_Handbook.pdf`), PDF pages 1-2 / printed 1-2: Special Considerations When Replacing Circuit Boards and Game Operation, transcribed in full except the speech phrase list, which is summarized at the end.
- Instruction Manual and Drawing Set (`Williams_1980_Blackout_Manual_with_paginated_schematics.pdf`), PDF page 2 / printed 2-3 Foreword, and PDF page 4 / printed 6, Power Turn-On, Electrical Adjustments and Special Maintenance Information.

## Booklet, printed page 1

Cover: `16P-495-103`, `Game No. 495`, `April, 1980`, INSTRUCTION BOOKLET.

This booklet provides game operation, bookkeeping, game adjustment, and diagnostic procedures for BLACKOUT. For installation and special maintenance information refer to the blue-covered game manual. For detailed information refer to Williams Solid State Flipper Maintenance Manual.

SPECIAL CONSIDERATIONS WHEN REPLACING CIRCUIT BOARDS

CPU Board

1. For memory protection feature, revision level 6 CPU Boards (batteries located on lower right corner of board) must be used. Revision level 4 CPU Boards equipped with IC14 and IC26 sockets may be used but the memory protection feature is lost.
2. Must be equipped with green-labeled BLACKOUT PROMs or game ROM and green-labeled flipper ROMs.
3. When Game ROM is used, jumper J3 must be connected and J4 removed.

Sound Board

1. Model D 8224 with jumper J1 removed required for speech.
2. Must be jumpered for white-labeled sound ROM operation and be equipped with Sound ROM 2. (Jumpers W2, W5, W7, W9, W10, and W15 connected; W3, W4, W6, W8, W11, W12, and W13 removed)

Power Supply Board

1. Fuse F4 (10A SB) for flipper solenoids must be installed.

Optional Speech Module

1. Requires 5T4951 (IC7), 5T4952 (IC5), and 5T4953 (IC6) speech ROMs.

GAME OPERATION

*Indicates adjustable features

Game Over Mode - Turn game ON; player scores show zero, high score to date* alternates with player 1 score, player 1 up lamp flashes, game over lamp lights, all playfield lamps except for credit lamp cycle in attract mode.

Credit Posting - Insert coin; knocker sounds, number of credits displayed. If maximum credits* exceeded by coin or high score to date*, credits are posted correctly, coin lockout de-energized until remaining credits are below maximum. No credits may be won and coins are rejected while lockout is energized.

Game Start - Push credit button; start-up tune played, ball served, credit display reduced by one, player 1 up lamp flashes until first scoring switch is made, ball in play shows 1. Pushing credit button before ball 2 displayed allows additional players.*

LANE CHANGE is a trademark of Williams Electronics, Inc.

(The scan's `lockout is energized` in the Credit Posting sentence is printed as shown; the same sentence says the lockout de-energizes to reject coins.)

## Booklet, printed page 2

Bonus Advance - 1, 2, and 3 Rollovers, top left target, green targets when flashing, top 3-bank drop targets; 3 advances for Special rollovers and, when lit, bottom inside rollovers. Bonus multiplier advanced by spotting "1-2-3". "1-2-3" lamps rotate by actuating right flipper (LANE CHANGE(TM) feature).

Green Targets - Making five green targets scores 10,000, lights eject hole green lamp, advances lighting of left spinner lamps, lights inside rollovers, and lights outlanes for Special.

Top 3-Bank - Making top 3-bank lights eject hole yellow lamp, advances lighting of top 3-bank target lamps, lights right spinners, and lights eject hole BLACKOUT lamp.

Center 3-Bank - Making center 3-Bank lights eject hole red lamp. Lighting of jet bumpers is controlled by center 3-bank and top left target. Center 3-bank target lamps rotate from spinners.

Spinner Loop - Making complete loop between left and top right spinners collects and advances left spinner lamp values. Advancing lamps past 20,000 lights eject hole for Extra Ball.

BLACKOUT - Lit when eject green, yellow, and red lamps lit. When lit, doubles eject hole value.

Extra Ball - Maximum of one Extra Ball per ball. Making spinner loop shot to collect 20,000 (or making 5 green targets when spinner loop 20,000 lit) lights eject hole for Extra Ball. Making eject hole when lit awards Extra Ball.

Tilts - Ball in play tilted on first closure of Playfield and Ball Roll tilts and third* closure of Plumb Bob. Slam Tilt returns game to game over.

Memory - Lit "1-3" rollovers, green target lamps, eject hole lamps until made for 30,000 and/or Extra Ball, and *bonus multipliers below 5x.

End of Game - Match Digits* appears in ball in play display, *credit awarded for match. Exceeding high score to date awards *three credits. Match, High Score to Date, and Game Over sounds made as appropriate.

With optional Speech Module, the following phrases are produced during game play: a two-column ACHIEVEMENT / PHRASE table (Game Start: Launch mission. Making 5-bank: Condition green. Making center 3-bank: Condition red. Making top 3-bank: Condition yellow. Making spinner loop shot: Orbit completed. Winning Extra Ball: Resume mission. Making Special: Mission completed. Making eject hole with BLACKOUT Lit: BLACKOUT), followed by a list of Game Over random phrases. The `Memory` and `Extra Ball` paragraphs carry ink blots over `rollovers`, `bonus` and `Extra`, read from context.

## Drawing set, printed pages 2-3 (Foreword)

The foreword repeats the booklet's board requirements with two differences: the sound board line reads `Model D 8224 required for speech.` (no jumper J1 clause), and the power supply line reads `Fuse F4 (10A SB) for flipper solenoids and magnet must be installed`. The CPU board line names `IC14 and IC16 sockets` where the booklet prints IC14 and IC26.

## Drawing set, printed page 6

Power Turn-On (numbered steps; the item numbers were not read reliably from the scan and are omitted):

- With the coin door closed, plug the game in and turn it ON. The game should come on in the game over mode as indicated by the player scores reading zero, player 1 up light flashing, game over lights lit, and the high score to date alternating with the player 1 score.
- If the game comes on in the diagnostic mode (number of credits display showing 04, ball in play display showing 00, and player 1 display showing game identification) turn the game OFF and ON again.
   a. If the game now comes on in the game over mode the bookkeeping and game evaluation totals have been reset to zero.
   b. If the game still comes on in the diagnostic mode, open the coin door and turn the game OFF and ON twice. This is an indication of the batteries being removed with the power OFF or coming loose during shipment. This has also resulted in features reverting to factory settings. Any changes from factory settings must be reentered using procedures provided in the instruction booklet.

Electrical Adjustments - Games with Speech Module:

1. Set miniature switch 2 to ON to enable speech; set it to OFF to inhibit speech.
2. Set switch 1 to OFF to select synthesized sounds, set it to ON to select musical notes.
3. Adjust balance control on Speech Module for relative volume of speech and sounds.
4. Adjust volume control in cabinet for desired volume.

Games without Speech Module: 1. Setting of miniature switch 2 does not matter. 2. Set switch 1 to OFF to select synthesized sounds; set it to ON to select musical notes. 3. Adjust volume control in cabinet for desired volume.

Special Maintenance Information: When the diagnostic pushbutton is depressed, eight electronic sounds are produced. Next, if the optional Speech Module is provided, the BLACKOUT vocabulary is produced. This sequence is continuously repeated until the game is turned OFF and back ON.

The VOCABULARY table lists BLACKOUT, LAUNCH, MISSION, CONDITION, GREEN, RED, YELLOW, RESUME, ORBIT and COMPLETED with the speech ROMs (5T 4951, 5T 4952, 5T 4953) that hold each word.
