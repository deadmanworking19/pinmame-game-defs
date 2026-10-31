# Williams Blackout (game 495) - Bookkeeping, adjustments and diagnostics

Source: Instruction Booklet 16P-495-103 (`Williams_1980_Blackout_Operators_Handbook.pdf`), PDF page 3 / printed 3 (Bookkeeping and Evaluation Totals, Game Adjustment Procedure, Diagnostic Procedures), PDF page 4 / printed 4 (Table 1 Game Adjustments) and PDF page 7 / printed 7 (Resetting Audit Totals and Adjustments; Initiating Auto-Cycle Mode; Figures 1 and 2). Pages 3 and 7 are transcribed in full; the step numbers of page 3 were not legible on the scan and are given in order.

## Bookkeeping and Evaluation Totals (Functions 01-12)

1. In game over mode, set toggle switch to AUTO-UP and depress ADVANCE pushbutton. Test 04 is indicated in number of credits display, Function 00 in ball in play display, and game identification in Player 1 display.
2. Operate the ADVANCE pushbutton to display each function on the ball in play display (see Table 1) and record each total from Player 1 display. (To review a total that has been advanced past, set toggle switch to MANUAL-DOWN and operate the ADVANCE pushbutton.)
3. Calculate the following if desired: % Paid Credits = Function 04 ÷ Function 08.
4. Turn the game OFF and back ON to return to game over mode.
5. To change current High Score to Date to value of Function 13, momentarily depress HIGH SCORE RESET pushbutton.
6. To zero Functions 01-11, see page 7.

## Game Adjustment Procedure (Functions 13-35)

1. Coin door must be open to change settings. In game over mode, set toggle switch to AUTO-UP and depress ADVANCE pushbutton. Test 04 is indicated in number of credits display, Function 00 in ball in play display, and game identification in Player 1 display.
2. To raise Function number in ball in play display, operate ADVANCE pushbutton with switch set to AUTO-UP. To lower Function number operate ADVANCE with it set to MANUAL-DOWN.
3. With desired Function indicated in ball in play display, raise value in player 1 display by operating credit button with switch set to AUTO-UP; lower value by operating credit button with it set to MANUAL-DOWN. Value left of Player 1 display is new setting. For values see Table 1 and (for pricing) Table 2.
4. Repeat steps 2 and 3 until all required adjustments have been made.
5. Turn game OFF and back ON to return to game over mode.
6. To restore factory settings and zero audit totals, see page 7.

## Diagnostic Procedures (Display Digits, Lamp, Solenoid, and Switch Tests)

1. In game over mode, set toggle switch to MANUAL-DOWN and depress ADVANCE. All displays should go blank.
2. Momentarily depress ADVANCE and set toggle switch to AUTO-UP. Display Digits test is performed.
3. Momentarily depress ADVANCE. Test 01 is indicated on number of credits display and Lamp Test is performed.
4. Set toggle switch to MANUAL-DOWN and momentarily depress ADVANCE. Test 02 is indicated on number of credits display and solenoid 01 on the ball in play display; solenoid 01 is pulsed by driver board.
5. Operate ADVANCE to pulse each solenoid (see Figure 3).
6. Set toggle switch to AUTO-UP and momentarily depress ADVANCE. Test 03 is indicated on number of credits display and stuck switches on ball in play display.
7. See Figure 4. Operate switches; switch number is indicated on ball in play display.
8. Turn game OFF and back ON to return to game over mode.
9. To set up Auto-Cycle Mode (Display Digits, Lamp, and Solenoid Tests) see page 7.

## Table 1. Game Adjustments (printed page 4)

Columns FUNCTION, DESCRIPTION, NOTES, FACTORY SETTING as printed; `-` is a printed dash. The scanned copy carries handwritten operator values beside several rows (for example 650,000, 440,000, 590,000 and 10, and digits in the left margin); they are not part of the table and are not transcribed.

| Function | Description | Notes | Factory setting |
|---|---|---|---|
| 00 | Game Identification | 1 | 1495 1 |
| 01 | Coins, Left Chute (Closest to coin door hinge) | 1 | - |
| 02 | Coins, Center Chute | 1 | - |
| 03 | Coins, Right Chute | 1 | - |
| 04 | Total Paid Credits | 1 | - |
| 05 | Total Specials | 1 | - |
| 06 | Total Replay (Extra Ball) Scores | 1 | - |
| 07 | Match and High Score to Date Credits | 1 | - |
| 08 | Total Credits | 1,2 | - |
| 09 | Total Extra Balls | 1,3 | - |
| 10 | Total Ball Time in Minutes | 1 | - |
| 11 | Total Number of Balls Played | 1 | - |
| 12 | Current High Score to Date | 4 | 600,000 |
| 13 | Backup High Score to Date | 5 | 500,000 |
| 14 | Replay 1 Score | 6 | 600,000 |
| 15 | Replay 2 Score | 6 | 440,000 |
| 16 | Replay 3 Score | 6 | 590,000 |
| 17 | Replay 4 Score | 6 | 0 |
| 18 | Maximum Credits | 7 | 20 |
| 19 | Standard and Custom Pricing Control (00-07) | 8 | 02 |
| 20 | Left Coin Slot Multiplier | 8 | 01 |
| 21 | Center Coin Slot Multiplier | 8 | 04 |
| 22 | Right Coin Slot Multiplier | 8 | 01 |
| 23 | Coin Units Required for Credit | 8 | 01 |
| 24 | Coin Units Bonus Point | 8 | 00 |
| 25 | High Score Credits | 5 | 03 |
| 26 | Match (00=ON, 01=OFF) | - | 00 |
| 27 | Special: 00 = Awards Credit; 01 = Awards Extra Ball; 02 = Awards Points | - | 00 |
| 28 | Scoring Awards: 00 = Credits at Replay Score; 01 = Extra Ball at Replay Score | - | 00 |
| 29 | Maximum Plumb Bob Tilts (1-9) | - | 03 |
| 30 | Number of Balls (03 or 05) | - | 03 |
| 31 | Extra Ball Difficulty: 00 = Conservative, Left Spinner 5,000 Not Lit Initially; 01 = Moderate, Left Spinner 5,000 Lit Initially | - | 01 |
| 32 | Outlane Special Difficulty: 00 = Conservative, Left and Right Inside Rollovers Lit Separately; 01 = Moderate, Left and Right Inside Rollovers Lit Together | - | 01 |
| 33 | Right Spinners: 00 = Conservative, Spinners Lit Separately; 01 = Moderate, Spinners Lit Together | - | 01 |
| 34 | Extra Ball Control: 00 = Extra Ball Allowed; 01 = No Extra Ball | - | 00 |
| 35 | Background Sound/Bonus Multiplier Memory/Attract Mode Sound. 1st Setting = With attract mode sounds. 2nd Setting = Without attract mode sounds. 00/10 = No Background Sound, No Bonus Multiplier Memory; 01/11 = Background Sound On, No Bonus Multiplier Memory; 02/12 = No Background Sound, Bonus Multiplier on Memory; 03/13 = Background Sound On, Bonus Multiplier on Memory | 9 | 03 |

## Resetting Audit Totals and Adjustments; Initiating Auto-Cycle Mode (printed page 7)

1. In game over mode, set the AUTO-UP/MANUAL-DOWN switch to MANUAL-DOWN and momentarily depress the ADVANCE pushbutton. All displays should go blank.
2. Remove the backglass and unlatch and open the insert door.
3. Set all switches on the MASTER COMMAND slide switch to OFF (move to the right).
4. Set switch on MASTER COMMAND switch to ON (move to left):
   a. To zero audit totals (Functions 01-11) set switch 8 to ON.
   b. To restore factory settings and zero audit totals, set switch 7 to ON. Coin Door must remain open to restore factory settings.
   c. For Auto-Cycle Mode set switch 6 to ON.
5. Momentarily depress MASTER COMMAND ENTER pushbutton. The LEDs should blink once.
6. a. After zeroing audit totals turn game OFF and ON to return to game over mode.
   b. After restoring factory settings, turn game OFF and on twice to return to game over mode.
   c. To initiate Auto-Cycle Mode, set toggle switch to AUTO-UP and momentarily depress the ADVANCE pushbutton. Each cycle of this mode sequences through display digits test, flashes all multiplexed lamps 64 times and pulses each solenoid. To terminate the Auto-Cycle mode and go to game over, turn the game OFF and ON.

Figure 1. Coin Door Diagnostic Switches: a photograph of the coin door with leaders to HIGH SCORE RESET, ADVANCE and AUTO-UP / MANUAL-DOWN.

Figure 2. Master Command Settings Switch: an eight-position slide-switch bank labelled MASTER COMMAND, with positions 8, 7 and 6 labelled ZERO AUDIT TOTALS, RESTORE FACTORY SETTINGS and AUTO-CYCLE MODE; a second eight-position bank labelled NOT USED; an LED beside each bank; and two pushbuttons labelled MASTER COMMAND ENTER and DIAGNOSTIC.
