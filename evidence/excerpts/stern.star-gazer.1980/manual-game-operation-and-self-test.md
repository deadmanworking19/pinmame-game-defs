# Star Gazer — general game operation and self test

Transcribed from `Stern_1980_Star_Gazer_Manual.pdf`, PDF pages 5 and 6 (printed pages 4 and 5), read from the rendered scans; the PDF has no text layer. Spelling and punctuation follow the pages, including the printed quotation marks and asterisks. Footnote marks `(*)` and `**` refer to the page's three foot notes, transcribed at the end of the first section.

## Printed page 4: "III. GENERAL GAME OPERATION"

**PLACE BALL INTO PLAYFIELD BY OUTHOLE:**

COIN GAME. Coin should be rejected. Plug in line cord. (For proper game operation grounding circuit must be used). Move power ON-OFF toggle switch at bottom right front corner of cabinet to "ON" position. Seven singular tones will be heard to indicate game-readiness. Feature lites will flash in a programmed attract mode, "HIGH SCORE" lite is lit, player displays flash high score to date, numbers 1 to 7 will display from right to left, all 7's will flash, "HIGH SCORE" lite goes off, previous played scores are flashed, "Coin lock-out coil" is energized and game is ready for play. Coin Game. The game should accept the coin and post credits for coins accepted (*). Pressing the credit button on the door will reset drop targets and cause the outhole kicker to move the ball to the shooter lane. The first player display will flash 00.

One player is registered each time the credit button is pressed (one to four can play). The credits are reduced by one each time the credit button is pressed until the credits are reduced to zero. (Credit button is in-operative after 4 players are registered). Shooting the ball initiates play.

When the ball enters the outhole, the bonus score is added to the player's score. The player-up and/or ball in play on the back box is advanced one position. The bonus score starts at ** points. The outhole kicker moves the ball to the shooter lane and play is resumed. This continues until each player has played the allowable number of balls per game (3 or 5). At this time the "Game Over" light becomes lit. A random "Match" number appears and the "Match" light becomes lit. If the match number is the same as the last two digits in the player's score a free game can be awarded (*).

Extra ball won during the course of the game is played immediately after the player's regular ball enters the outhole. The player-up and/or ball in play is not advanced for extra ball play. Bonus score is added to the player's score, the bonus is reset to ** and the bonus multiplier earned is restored (memory) or reset (*) before the game moves the extra ball for play.

At the end of the game, a "High Game" is flashed on all players scores. If the "High Game" is beat, this feature (*) can award up to 3 free games.

Tilting while playing the game results in loss of the ball in play. The flippers, thumper-bumper, etc., go "dead". Bonus score is not added. The purpose of the tilt penalty is to discourage the player from jostling the machine in an attempt to prolong play. Game action becomes normal after the outhole kicker moves the ball to the shooter lane.

Slamming the machine results in the loss of the game. All feature lights go out and the game becomes "dead" through a built-in time delay circuit. The purpose of the time delay circuit is to discourage abuse of the machine. After the delay, the "Game Over" light lites "Shoot Again" lite flashes and the game is ready for play. The time delay occurs anytime one of the slam switches is made to contact.

There is a slam switch on the front door, one on the tilt board. (Any number of slam switches could be installed by the operator, to meet his individual requirement). The switch should be adjusted to have approximately 1/16" gap between the contacts. The weighted blade should be adjusted to attain the desired sensitivity. Decreasing gap between contacts will make the switch more sensitive. Opening the gap will reduce sensitivity.

Foot notes: `*Some tunes and features can be disabled by operator if so desired.` `**Bonus starts at 0.` `***See back box adjustments.***`

## Printed page 5: "IV. SELF TEST AND BOOKKEEPING FUNCTIONS"

"The game is designed to help the operator perform certain diagnostic tests as well as accounting functions as follows:"

**IV. A. SELF TEST**

| TEST SWITCH PUSH NUMBER | BALL/MATCH DISPLAY | DESCRIPTION |
| --- | --- | --- |
| 1st | | Burn in test - all outputs tested |
| 2nd | | Lamp test - all feature lamps on and off |
| 3rd | | Display test - all digits display 000000 thru 999999 then an 8 shifts from left to right |
| 4th | | Solenoid test - continuous sequence of solenoids pulsed with solenoid driver transistor, "Q" number displayed |
| 5th | `lashing O if all switches open` (the first letter is cut off in the scan) | Switch test - switch I.D. No. displays if closed |

**IV. B. BOOKKEEPING FUNCTIONS**

| TEST SWITCH PUSH NUMBER | BALL/MATCH DISPLAY | DESCRIPTION | DISPLAYS |
| --- | --- | --- | --- |
| 6th | 01 | 1st Threshold (High Score) | |
| 7th | 02 | 2nd Threshold (High Score) | |
| 8th | 03 | 3rd Threshold (High Score) | |
| 9th | 04 | Current High Game Threshold | |
| 10th | 05 | Current Credits | 00 to 40 |
| 11th | 06 | Total Plays | 00 to 999999 |
| 12th | 07 | Total Replays | 00 to 999999 |
| 13th | 08 | Total times high score is passed | 00 to 999999 |
| 14th | 09 | Number of coins thru Chute No. 2 | 00 to 999999 |
| 15th | 10 | Number of coins thru Chute No. 1 | 00 to 999999 |
| 16th | 11 | Number of coins thru Chute No. 3 | 00 to 999999 |
| 17th | 12 | Total balls played | 00 to 999999 |
| 18th | 13 | Total Extra Balls Awarded | 00 to 999999 |
| 19th | 14 | Total Playfield Special Awards | 00 to 999999 |
| 20th | 15 | N/U | 00 |
| 21st | 16 | Total level 1 passed | 00 to 999999 |
| 22nd | 17 | Total level 2 passed | 00 to 999999 |
| 23rd | 18 | Total level 3 passed | 00 to 999999 |

The page says every test-display and bookkeeping count is six digits (`000000` to `999999`); the retained ROM's player displays have seven digit positions, and the manual's own high-score settings go up to `9,990,000`.
