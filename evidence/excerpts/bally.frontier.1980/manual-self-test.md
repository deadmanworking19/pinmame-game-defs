# Frontier - self-test procedure and the bookkeeping press count

Transcribed from `Bally_1980_Frontier_Manual.pdf`, PDF pages 6, 17 and 18 (printed pages 3, 13 and 14), read from the native 300 dpi renders of the scan with Windows OCR as a first pass, checked against the rendered pages. Quoted text is the page's own.

## PDF page 17 (printed 13), VIII. ROUTINE MAINTENANCE ON LOCATION - Game Self-Diagnostic Tests

> MPU Module Self-Test: At power on, the LED on the MPU module flashes once. (Flicker-Flash). After a pause. it flashes six more times and goes out. A power-up tune is played to announce game readiness This indicates proper MPU operating condition and successful completion of the power-up test.
>
> 1. Pressing the Self-Test button inside the door initiates the Self-Test routine. See Figures III and IV All switched lamps flash off and on continuously.
> 2. Pressing the Self-Test button again causes each digit on each display to cycle from 0 thru 9, and repeat continuously.
> 3. Pressing the Self-Test button again causes each solenoid to be energized, one at a time, in a continuous sequence. Hold both flipper buttons 'in' during this test. The number appearing on the Player Score displays is the same as the number assigned to the solenoid, The sound of a solenoid pulling-in as a number appears indicates proper operation. The absence of sound is improper If sound is absent, see Page 17 for help in Solenoid identification.
> 4. Pressing Self-Test button again causes the sound module to play the "Game Over" tune repeatedly.
> 5. Pressing the Self-Test button again causes the MPU to search each switch assembly for stuck contacts. If any are found, the number of the first set encountered is flashed on the Player Score displays. The number remains until the fault is cleared. See Page 17 for help in Stuck Switch identification. Other numbers may follow if more stuck contacts are present. If there are no stuck switches, the Match/Ball in Play display flashes '0'.
> 6. Pressing the Self-Test button 20 more times causes the MPU to step thru the threshold and bookkeeping functions described previously and finally to repeat the power-up test. For more rapid exit to power-up, turn the game off, then on. The game is now ready to play.
>
> After successful completion of the Self Diagnostic Test procedure, set the game up for play. Exercise each rollover, thumper-bumper, slingshot, etc., by hand until each switch assembly on the playfield has been checked for proper operation. If actuating a switch assembly results in intermittent or no response, clean contacts by gently closing them on a clean business card or piece of paper and wiping until they wipe clean. Regap, if necessary, to 1/16". Do not burnish or file Gold Plated Switch Contacts.

## PDF page 18 (printed 14), FIGURE IV flow chart, the steps that name a test

> ALL FEATURE LAMPS LIGHT, FLASH ON AND OFF?
> ALL DISPLAYS COUNT 0000000 to 9999999
> ALL SOLENOIDS * PULL-IN* IN SEQUENCE?
> SOUND MODULE PLAYS "GAME OVER" TUNE
> ALL SWITCHES* OPEN?
> PRESS SELF-TEST BUTTON 20X OR TURN POWER OFF AND THEN ON.
> *SOLENOID AND STUCK-SWITCH NUMBER IS FLASHED ON PLAYER SCORE DISPLAYS AS AN AID IN TROUBLESHOOTING
> FLIPPER BUTTONS IN DURING TEST

The display test's "0000000 to 9999999" is seven digits.

## PDF page 6 (printed 3), III. BOOKKEEPING FUNCTIONS - how the entries are reached

> The game displays the first bookkeeping entry if the Self-Test button (See Fig. III) on the inside of the front door is pressed ten times. Alternately push and release the Self-Test button at one second intervals. The number 05 appears in the 'Match/Ball in Play' window. Current credits appear on the player score displays. Each additional press of the button causes the next entry to be displayed.
>
> After the data in each bookkeeping register is recorded, it can be set to zero simply by pressing switch button S33, located on A4, the MPU module in the back box (See Fig. III), or by pressing the Coin Chute #3 switch.

## What the retained ROM did

In the retained harness runs (pinned LibPinMAME, empty NVRAM, first press 30 s after power-on), three presses reached the cycling solenoid test, a fourth press ended it (moving to the manual's sound test) and a fifth started the stuck-switch test, which flashed 0 on the Match/Ball in Play display with every switch open.
