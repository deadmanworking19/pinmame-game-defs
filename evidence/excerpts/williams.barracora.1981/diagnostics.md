# Williams Barracora (game 510) - Diagnostic procedures

Source: `Williams_1981_Barracora_Operators_Handbook.pdf` (instruction booklet 16P-510-103):

- PDF page 7 = printed page `7`, `DIAGNOSTIC PROCEDURES`: `Display Digits Test` and `Sound Test`.
- PDF page 8 = printed page `8`, `Lamp Test` (top of the page; the rest of the page is Table 3, not transcribed here).
- PDF page 10 = printed page `10`, `Solenoid Test` (top of the page; the Figure 2 chart below it is in `solenoid-connections.md`).
- PDF page 11 = printed page `11`, `Switch Test` items 1-2 (bottom of the page, below Table 4).
- PDF page 12 = printed page `12`, `Switch Test` items 3-5 (top of the page, above Figure 3).
- PDF page 14 = printed page `14`, `INITIATING AUTO-CYCLE MODE`, `CPU BOARD SELF-TEST` and `SOUND BOARD SELF-TEST`.

Method: the pages' native images (1760 x 2663) were cropped and read visually; every section named above is transcribed in full. Numbering, capitalization and punctuation are as printed. Typographic quotes are rendered as plain quotes.

## Page 7

**DIAGNOSTIC PROCEDURES**

**Display Digits Test**

1. Set AUTO-UP/MANUAL-DOWN switch to MANUAL-DOWN and depress ADVANCE. Displays should indicate all 0's.
2. Set the switch to AUTO-UP. Displays should sequence from all 0's thru all 9's. Comma segments should come on when odd digits are displayed.
3. To stop cycling, set switch to MANUAL-DOWN. Operate ADVANCE pushbutton to step through the tests one number at a time. Set switch to AUTO-UP to resume cycling.

**Sound Test**

1. From Display Digits Test depress ADVANCE with the switch set to AUTO-UP. Test 00 should be indicated in the Credits display and the Match display should sequence from 00 thru 06. Different sounds should be produced for 00, 01, 02, 03, and 04.
2. To continuously pulse a single sound, set the toggle switch to MANUAL-DOWN. Operate ADVANCE pushbutton to sequence through sounds one at a time. Set toggle switch to AUTO-UP to resume sequencing.

## Page 8

**Lamp Test**

From Sound Test depress ADVANCE with the switch set to AUTO-UP. Test 01 should be indicated in the Credits display and all multiplexed lamps should flash.

## Page 10

**Solenoid Test**

1. From Lamp Test depress ADVANCE with the switch set to AUTO-UP. Test 02 should be indicated in the Credits display. The Match display sequences from 01 thru 25. Corresponding solenoids 01 thru 24 are pulsed. Flipper relay is de-energized with subtest 25.
2. To continuously pulse a single solenoid set switch to MANUAL-DOWN. Operate ADVANCE pushbutton sequence through the solenoids one at a time. Set switch to AUTO-UP to resume sequencing.

## Page 11

**Switch Test**

1. From Solenoid Test depress ADVANCE with the switch set to AUTO-UP. Test 03 should be indicated in the Credits display and any stuck switches in the Master display. As stuck switch(es) is displayed a sound is produced. The display continuously cycles through the stuck switches and as they are opened, the number is removed from the sequence. When all switches are open, the Match display is blank and the sounds stop.
2. If all switches in a row are displayed, first verify that all are open and then check for a short to ground on the row wire.

## Page 12

3. Operate switches; a sound is produced and switch number is momentarily indicated in the ball in play display. If two switches in a row are indicated with one switch closed, check for a short between the column wires; for multiple indication check column wire for short to ground. If two switches in a column are indicated with one switch closed, check for short between row wires.
4. If proper indications are obtained in Test 03 but matrix problem is suspected in game play, disconnect lamp connectors 2P5 and 2P7. Recheck in game play. Perform CPU Self-Test if problem remains. If problem is cleared, check for short between lamp matrix and jet bumper mounting brackets.
5. Shorted diodes can cause "rectangle" switch matrix problems as follows:
   The "B" target down (switch 41), the top "A" target down (switch 44), and with a ball hitting the upper right Bull's-Eye Target (switch 33), a shorted diode at switch 41 would cause switch 36 Playfield Tilt to be indicated. Note that the "rectangle" is always completed with an incorrect switch diagonally opposite from the switch with the shorted diode.

## Page 14

**INITIATING AUTO-CYCLE MODE**

1. Set AUTO-UP/MANUAL-DOWN switch to AUTO-UP and depress ADVANCE pushbutton. Test 04 is indicated in Credit display and Function 00 in Match Display.
2. Set switch to MANUAL-DOWN and depress ADVANCE to indicate Function 50 in the Match Display.
3. Set switch to AUTO-UP and operate Credit button to indicate 15 in Player 1 Display.
4. Depress ADVANCE pushbutton to start Auto-Cycle mode. Each cycle of this mode sequences thru the Display Digits Test, Sound Test (00), Lamp Test (01), and Solenoid test (02).
5. To terminate the test and return to game over, turn the game OFF and back ON.

**CPU BOARD SELF-TEST**

Depress the DIAGNOSTIC pushbutton on the left side of the CPU Board. The following indications are provided. With 0 indication the game returns to the game over mode.

| Indication | Meaning, as printed |
|---|---|
| 0 | Test Passed |
| 1 | IC13 RAM Faulty |
| 2 | IC16 RAM Faulty |
| 3 | IC17 ROM 2 Faulty |
| 4 | IC17 ROM 2 Faulty |
| 5 | IC20 ROM 1 Faulty |
| 6 | IC14 Game ROM 1 Faulty |
| 7 | IC26 Game ROM 0 Faulty |
| 8 | IC19 CMOS RAM or Memory Protect Circuit Faulty |
| 9 | Coin-door closed, Memory Protect Circuit Faulty, or IC19 CMOS RAM Faulty. |

Note that "0" remaining after power turn-on indicates CPU Board lockup.

**SOUND BOARD SELF-TEST**

Depress DIAGNOSTIC pushbutton on the top of the Sound Board. Several electronic sounds should be produced. This sequence of sounds is repeated until the game is turned OFF and back ON.

## Notes

- Indications 3 and 4 both read `IC17 ROM 2 Faulty` as printed; the duplicate is transcribed literally.
- The booklet's "Match display" and "ball in play display" are the same two-digit display; PinMAME publishes it as display indices 4 and 5. The "Credits display" is indices 6 and 7.
- PinMAME's `S7_COMPORTS` names the cabinet `Advance` (-7) and `Auto/Manual` (-6) switches, the CPU board's `CPU Diagnostic` (-5) pushbutton and the sound board's `Sound Diagnostic` (-4) pushbutton described above.
- The Solenoid Test text says solenoids 01 thru 24 are pulsed although Table 4 has no rows for 23 and 24 (`solenoid-connections.md`); the harness run in this record sees public 23 and 24 pulse in Test 02 with no load fitted to either.
