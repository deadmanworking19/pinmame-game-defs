# Williams Barracora (game 510) - Game operation and power turn-on

Sources:

- `Williams_1981_Barracora_Operators_Handbook.pdf` (instruction booklet 16P-510-103), PDF pages 1-2 = printed pages `1` and `2`: `SPECIAL CONSIDERATIONS WHEN REPLACING CIRCUIT BOARDS` and `Game Operation`.
- `Williams_1981_Barracora_Instruction_and_Drawing_Set_paginated_schematics_cover_page_missing.pdf`, PDF page 3, `Power Turn-On and Game Setup` (first half of the page).

Method: native page images read visually and transcribed in full for the sections named. Italics and trademark marks are dropped; asterisks are as printed. Paragraph breaks are as printed.

## Booklet page 1: SPECIAL CONSIDERATIONS WHEN REPLACING CIRCUIT BOARDS

**CPU Board**

1. Revision level 7 CPU Boards (batteries located on lower left corner at board) of later boards must be used.
2. Must be equipped with blue-labeled Flipper ROMs and blue-labeled Game ROMs.
3. Jumpers W3, W10, W11, W14, W17, W19, W20, and W22 must be connected. Jumpers W4, W9, W12, W15, W16, W18, W21, and W23 must be removed. With the exception of W25, (Factory Setting Jumper) all other jumpers are not changed.

**Driver Board** Must be equipped with zero-ohm resistors or wire jumpers (W9-W16) in place of switch matrix drive series resistors R204-R211.

**Sound Board** Must be jumpered for ROM operation and be equipped with Sound ROM 4. (Jumpers W3, W5, W7, W9, W10, W12, and W15 connected; W2, W4, W6, W8, W11, and W13 removed).

**Power Supply Board**

1. Model D 8345 board required (equipped with relay).
2. Fuse F4 (10A SB) for flipper solenoids must be installed.

**Display Boards** Model C 8363 Master Display and 7-digit Slave Displays required.

## Booklet pages 1-2: Game Operation

*Indicates adjustable features.

**Game Over Mode** - Turn game ON; player 1 score shows 00; all player scores alternate the high score to date. Game Over lamp lights. All playfield lamps cycle in attract mode.

**Credit Posting** - Insert coins; sound produced, number of credits displayed. If maximum credits* exceeded by coin or high score to date, credits posted correctly and coin lockout de-energizes until remaining credits are below maximum. No credits may be won and coins are rejected while the coin lockout is de-energized.

**Game Start** - Three balls must be resting on ball ramp or ball shooter switches (maximum of one ball in ball shooter trough) before game will start. Push credit button, startup tune played, ball served, credit display reduced by 1, player 1 score flashes 00 until first scoring switch is made, ball in play display shows 1. Pushing credit button before ball 2 allows additional players.

Multi-Ball and Lane Change are trademarks of Williams Electronics, Inc.

**Bonus Advance** - One advance for top lane rollovers, flipper return lane rollovers, and outlane rollovers. Making B-A-RR and A-C-O-R-A drop targets in sequence spots lamps in the BARRACORA lane. Making the lane rollover awards one advance for each lit letter. With bonus at maximum (29,000), 1,000 points is scored in lieu of each bonus advance. Completing the B-A-RR or A-C-O-R-A drop target bank advances the Bonus Multiplier from 2X through 5X. Completing both drop target banks advances Super Bonus Multiplier from 2X through 5X. When the bonus is collected it is equal to the Super Bonus Multiplier times the Bonus Multiplier times the accrued Bonus (up to 25 times the accrued Bonus).

**Top Lanes** - Making a top rollover switch lights the 1, 2, or 3 lamp. If the respective 1, 2, or 3 lamp affected is already lit, the 4, 5, or 6 lamp directly underneath is lit. The right flipper Lane Change switch rotates the 1, 2, and 3 lamps from right to left and the left flipper Lane Change switch rotates the 4, 5, and 6 lamps from left to right. Lighting lamps 1, 2, and 3 advances the lower eject hole lamps (30,000, 60,000, & 90,000) and lighting lamps 4, 5, and 6 advances the upper right bull's-eye target values (20,000, 40,000, & Extra Ball). Completing lamps 1, 2, 3, 4, 5, and 6 lights the upper eject hole to collect the bonus. Note that if you collect the bonus from this eject hole the bonus collected will be the Super Bonus Multiplier times the Bonus Multiplier times the bonus, and only the bonus multipliers will not reset.

**Multi-Ball Play** - Completing the B-A-RR drop target bank lights the lower eject hole lock arrow and completing the A-C-O-R-A drop target bank lights the upper eject hole lock arrow. Making the lower eject hole when the lock arrow lamp is lit initiates 2-ball Multi-Ball play. With both eject hole lock arrows lit, the first ball must be locked in the upper eject hole and the next ball in the lower eject hole for 3-ball Multi-Ball play. If the first ball is locked in the lower eject hole, only 2-ball Multi-Ball play is achieved. If the ball in play drains while a ball is locked in the upper eject hole, the locked ball is released and played out.

**Target Bonus** - The left bull's-eye target advances the Target Bonus and the right bull's-eye target advances the Target Bonus multiplier value. Making the horseshoe shot scores the Target Bonus and resets the bonus lamps. If the lit bonus and multiplier lamps are lined up, they are not reset until collected twice.

**Bonus Ball** - A bonus ball will be awarded to the player with the highest score out of 2 or more players for 30* seconds of extra play.

**Memory** - Drop targets and all lamp features except regular bonus multipliers.

**Tilt** - Ball in play tilted on first closure of ball roll tilt and third* closure of plumb bob and playfield tilts. Slam tilt returns game to Game Over mode.

**End of Game** - Match Digits* appear in ball in play display, credit* awarded for match. Exceeding high score to date awards three* credits. Match, High Score to Date, and Game Over sounds made as appropriate. A new game cannot be started with more than one ball in the ball shooter trough; excess balls must be returned to playfield and drain to rest on ball ramp switches.

## Drawing set PDF page 3: Power Turn-On and Game Setup (first half)

(The page's first characters are lost at the left edge of the scan; they are restored in brackets.)

[T]his machine MUST BE PLUGGED INTO A PROPERLY GROUNDED OUTLET to PREVENT SHOCK HAZARD to ensure [P]ROPER GAME OPERATION. DO NOT use a "cheater" plug to defeat the ground pin on the line cord, and DO NOT cut off the ground pin. The line voltage MUST agree with that specified on the back of the cabinet or serious damage to the machine could occur. For low-line applications (105 or 210V ac), refer to the power wiring diagram.

1. With the coin door closed, plug the game in and turn it ON. The game should come on in the Game Over mode as indicated by the player 1 score reading zero, Game Over lights lit, and the high score to date alternating with the player scores.
2. If the game comes on in the Diagnostic Mode (number of credits display showing 04, ball in play display showing 00, and player 1 display showing game identification) turn the game OFF and ON again.

a. If the game now comes on in the Game Over mode the bookkeeping and game evaluation totals have been reset to zero.

b. If the game still comes on in the Diagnostic Mode, open the coin door and turn the game OFF, and ON twice. This is an indication of the batteries being removed with the power OFF or coming loose during shipment. This has also resulted in features reverting to factory settings. Any changes from factory settings must be reentered using procedures provided in the instruction booklet.

3. If the game still comes on in the Diagnostic Mode, refer to troubleshooting procedures in the maintenance manual.

(item marker lost at the left edge) Place three balls on playfield next to outhole.

## Notes

- The drawing set's own foreword gives F4 as `20A SB` "for flipper solenoids and magnets" (`cabinet-and-power.md`); this booklet page gives `10A SB`.
- The Top Lanes paragraph says the right flipper's Lane Change rotates lamps 1-3 and the left flipper's rotates lamps 4-6; which matrix number each flipper copies into is settled by the Test 03 run in the runtime evidence, not by this prose.
