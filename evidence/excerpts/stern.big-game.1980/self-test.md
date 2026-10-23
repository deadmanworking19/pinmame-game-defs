Source: `Stern_1980_Big_Game_Manual.pdf` (IPDB machine 249), PDF page 3 (`II. ROUTINE MAINTENANCE ON LOCATION`) and PDF page 6 (`IV. SELF TEST AND BOOKKEEPING FUNCTIONS`). Read from 144 dpi renders and transcribed by hand; every line was checked against them.

Page 3, `GAME SELF-DIAGNOSTIC TESTS`, verbatim:

"Pressing the Self-Test button inside the coin door activates the game into its self-diagnostic test.

1. BURN IN TEST - all outputs tested.
2. FEATURE LAMPS - All feature lamps will flash on and off continuously, determining any burnt lamps.
3. DISPLAYS - Each digit on all displays will cycle from 0 thru 9, then a number 8 will shift left to right. This test will recycle continuously.
4. SOLENOIDS - Each solenoid will be energized, one at a time, in a continuous sequence. (Holding both flipper buttons "in" during this test will cause the flipper coils to be energized). The number appearing on the Player Score displays is the same as the number assigned to the solenoid and also the same transistor number on the SDU board. The sound of a solenoid pulling-in as a number appears indicates proper operation providing transistor is being used, the absence of a solenoid sound shows a fault. If sound is absent, see Solenoid I.D. page in book for help in Solenoid Identification. *After the solenoids are tested, the game sounds are tested.
5. SWITCHES - The MPU will look at each switch assembly for stuck contacts. *(Flipper Button Switches are not included). If there are any stuck, the lowest number encountered is flashed on the Player Score displays. The number remains until the fault is corrected. See Switch I.D. page in book for help in switch identification. Other numbers may follow if more stuck contacts are present. If there are no stuck switches, the "Match/Ball in Play" display flashes '0'. DO NOT BURNISH OR FILE GOLD PLATED SWITCH CONTACTS.
6. GAME LEVELS AND BOOKKEEPING FUNCTIONS: - Pressing the Self-Test button eighteen more times causes the MPU to step thru the game levels and bookkeeping functions and finally to repeat the power-up test. To bypass these functions, turn the game off, then on. The game is now ready to play, after the MPU Self-Test."

Page 3, `MPU MODULE SELF-TEST`, verbatim: "During power-up, the MPU assembly tests itself, which can visibly be seen by the flashing of a LED on the board. When the game is turned on, the LED will flash, have a pause, flash again, a longer pause, then flash five more times and then will be dimly lit. Accompanying eah flash is one note (total of seven), this indicates proper MPU game operation conditions."

Page 6, `IV.A. SELF TEST`:

| Test switch push number | Ball/match display | Description |
| --- | --- | --- |
| 1st | | Burn in test - all outputs tested |
| 2nd | | Lamp test - all feature lamps on and off |
| 3rd | | Display test - all digits display 0000000 thru 9999999 then an 8 shifts from left to right |
| 4th | | Solenoid test - continuous sequence of solenoids pulsed with solenoid driver transistor, "Q" number displayed |
| 5th | Flashing O if all switches open | Switch test - switch I.D. No. displays if closed |

Page 6, `IV.B. BOOKKEEPING FUNCTIONS`: pushes 6th to 23rd show 01 to 18 on the Ball/Match display: 1st Threshold (High Score), 2nd Threshold (High Score), 3rd Threshold (High Score), Current High Game Threshold, Current Credits (00 to 40), Total Plays, Total Replays, Total times high score is passed, Number of coins thru Chute No. 2, Number of coins thru Chute No. 1, Number of coins thru Chute No. 3, Total balls played, Total Extra Balls Awarded, Total Playfield Special Awards, No. of Times Special (Sun Only) was Lit, Total level 1 passed, Total level 2 passed, Total level 3 passed. The March 1980 corrections sheet replaces pushes 20th to 24th (see `corrections.md`).
