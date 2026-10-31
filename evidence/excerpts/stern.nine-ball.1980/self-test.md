Source: `Stern_1980_Nine_Ball_Manual.pdf` (IPDB machine 1678), PDF pages 3 and 6 (printed page 2 and the unnumbered page after printed page 5). Read from the retained 72 dpi page images, checked line by line against a three-times enlargement.

PDF page 3, `II. ROUTINE MAINTENANCE ON LOCATION`:

`MPU MODULE SELF-TEST:` "During power-up, the MPU assembly tests itself, which can visibly be seen by the flashing of a LED on the board. When the game is turned on, the LED will flash, have a pause, flash again, a longer pause, then flash five more times and then will be dimly lit. Accompanying each flash is one note (total of seven), this indicates proper MPU game operation conditions."

`GAME SELF-DIAGNOSTIC TESTS:` "Pressing the Self-Test button inside the coin door activates the game into its "Self-Diagnostic Test.""

1. "BURN IN TEST - All outputs tested."
2. "FEATURE LAMPS - All feature lamps will flash on and off continuously, determining any burnt lamps."
3. "DISPLAYS - Each digit on all displays will cycle from 0 thru 9, then a number 8 will shift left to right. This test will recycle continuously."
4. "SOLENOIDS - Each solenoid will be energized, one at a time; in a continuous sequence. (Holding both flipper buttons "in" during this test will cause the flipper coils to be energized). The number appearing on the "Player Score" display is the same as the number assigned to the solenoid and also the game transistor number on the SDU board. The sound of a solenoid pulling-in as a number appears indicates proper operation (providing transistor is being used), the absence of a solenoid sound shows a fault. If sound is absent, see Solenoid I.D. page in book for help in Solenoid Identification. (After the solenoids are tested, the game sounds are tested.)"
5. "SWITCHES - The MPU will look at each switch assembly for stuck contacts. (Flipper Button and flipper End of Stroke switches are not included). If there are any stuck, the lowest number encountered is flashed on the Player Score displays. The number remains until the fault is corrected. See Switch I.D. page in book for help in switch identification. Other numbers may follow if more stuck contacts are present. If there are no stuck switches, the "Match/Ball in Play" display flashes 0. DO NOT BURNISH OR FILE GOLD PLATED SWITCH CONTACTS."
6. "GAME LEVELS AND BOOKKEEPING FUNCTIONS: - Pressing the Self-Test button eighteen more times causes the MPU to step thru the game levels and bookkeeping functions and finally to repeat the power-up test. To bypass these functions, turn the game off, then on. The game is now ready to play, after the MPU Self-Test."

`CONTACT SWITCH ADJUSTMENTS` "All contact switches should be adjusted to have a gap 1/16" in the open position, and have .010" overtravel closed. All contact switches (except for flipper buttons & flipper end of stroke switches) are gold plated to resist corrosion and, SHOULD NOT BE FILED OR BURNISHED. ..." "FLIPPER BUTTON & FLIPPER SWITCHES ONLY. Tarnish or pitted contacts can be corrected with a contact file followed by a burnishing tool. Severely pitted contact must be replaced as an assembly."

PDF page 6, `IV. SELF TEST AND BOOKKEEPING FUNCTIONS`, `IV. A. SELF TEST`:

| TEST SWITCH PUSH NUMBER | BALL/MATCH DISPLAY | DESCRIPTION |
| --- | --- | --- |
| 1st | (blank) | Burn in test - all outputs tested |
| 2nd | (blank) | Lamp test - all feature lamps on and off |
| 3rd | (blank) | Display test - all digits display 000000 thru 999999 then an 8 shifts from left to right |
| 4th | (blank) | Solenoid test - continuous sequence of solenoids pulsed with solenoid driver transistor, "Q" number displayed |
| 5th | Flashing 0 if all switches open | Switch test - switch I.D. No. displays if closed |

`IV. B. BOOKKEEPING FUNCTIONS`:

| TEST SWITCH PUSH NUMBER | BALL/MATCH DISPLAY | DESCRIPTION | DISPLAYS |
| --- | --- | --- | --- |
| 6th | 01 | 1st Threshold (High Score) | (blank) |
| 7th | 02 | 2nd Threshold (High Score) | (blank) |
| 8th | 03 | 3rd Threshold (High Score) | (blank) |
| 9th | 04 | Current High Game Threshold | (blank) |
| 10th | 05 | Current Credits | 00 to 40 |
| 11th | 06 | Total Plays | 00 to 999999 |
| 12th | 07 | Total Replays | 00 to 999999 |
| 13th | 08 | Total times high score is passed | 00 to 999999 |
| 14th | 09 | Number of coins thru Chute No. 2 | 00 to 999999 |
| 15th | 10 | Number of coins thru Chute No. 1 | 00 to 999999 |
| 16th | 11 | Number of coins thru Chute No. 3 | 00 to 999999 |
| 17th | 12 | Total balls played | 00 to 999999 |
| 18th | 13 | No. of Top Bank wow | 00 to 999999 |
| 19th | 14 | No. of 8 Bank wow | 00 to 999999 |
| 20th | 15 | Total Playfield Special Awards | 00 |
| 21st | 16 | Total level 1 passed | 00 to 999999 |
| 22nd | 17 | Total level 2 passed | 00 to 999999 |
| 23rd | 18 | Total level 3 passed | 00 to 999999 |
