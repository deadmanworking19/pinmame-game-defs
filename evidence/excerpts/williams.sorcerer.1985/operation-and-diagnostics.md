# Literal transcription — ROM summary, control locations, game play and diagnostic procedures

`reviewed: true`; transcribed by the curator from 200-300 dpi renders and visually checked against them on 2026-10-16
`source: Instruction Manual PDF page 2 (printed 2), PDF page 6 (printed 6) and PDF page 11 (printed 11)`

Retained renders: `external:pinmame-manuals/by-machine/williams.sorcerer.1985/rendered-300/q-02.png`, `p-06.png`
and `q-11.png`. Paragraphs are quoted where this definition relies on them; elisions are marked `[...]`.

## PDF page 2 — System-9 ROM Summary

| IC | DESCRIPTION | TYPE | NUMBER | BOARD | PART NO. |
| --- | --- | --- | --- | --- | --- |
| Game-ROM 1 | ROM 8Kx8 | 2764 | U20 | CPU | A-5343-10764 |
| Game-ROM 2 | ROM 4Kx8 | 2732 | U19 | CPU | A-5343-10765 |
| Sound ROM | ROM 16Kx8 | 25128 | U49 | CPU | A-5343-10766 |
| Speech ROM | ROM 4Kx8 | 2532 | U6 | Speech | A-5343-10806 |
| Speech ROM | ROM 4Kx8 | 2532 | U7 | Speech | A-5343-10807 |
| Speech ROM | ROM 4Kx8 | 2532 | U8 | Speech | A-5343-10808 |
| Speech ROM | ROM 4Kx8 | 2532 | U9 | Speech | A-5343-10809 |

Below the table: `2732 ROMS may also be used for the speech ROMS.`

## PDF page 2 — System-9 Control Locations

> THE ON-OFF SWITCH is on the bottom of the cabinet near the right-front leg as you face the game.
>
> THE VOLUME CONTROL is accessible through the coin door on the left cabinet-wall.
>
> DIAGNOSTIC SWITCHES. ADVANCE, AUTO-UP/ MANUAL-DOWN, and HIGH-SCORE RESET switches are located on the back of
> the coin door. Refer to Game-Adjustment Procedure and Diagnostic Procedures for operation.
>
> THE MEMORY-PROTECT SWITCH must be open to clear bookkeeping totals and to make game adjustments. This switch is
> on the inside of the coin-door frame. It automatically opens when the coin door opens.
>
> ALL CIRCUITBOARDS are in the backbox.
>
> THE CPU DIAGNOSTIC-SWITCH operates the Memory-Chip Test explained in Diagnostic Procedures. This switch is on
> one edge of the CPU Board near a microprocessor (large, socketed) chip.
>
> THE SOUND DIAGNOSTIC-SWITCH is on the CPU Board near the batteries. This switch is used to initiate the Sound
> Section Test. Refer to Diagnostic Procedures.

## PDF page 6 — Replacing System-9 Circuitboards (display and power-supply paragraphs)

> DISPLAY BOARDS. Use the C-8363 Master Display Board with the C-8364 7-digit Slave Display. The C-8365 4-digit
> Slave Display is also used.
>
> POWER-SUPPLY BOARD. Use the D-8345 board (equipped with a relay).

## PDF page 6 — Game Play

> • SPOTTING A-B-C-D...advances bonus multiplier (2X, 4X, 6X, 8X), then scores 50,000.
> • SPOTTING S-O-R-C-E-R-E-R...lights DEMON at 3-bank, spinners, EXTRA BALL, and playfield SPECIAL.
> • COMPLETING 3-BANK DROP TARGET...lights one flipper return lane and awards flashing value, awards EXTRA BALL
>   (when lit), and spots BONUS HELD OVER (with DEMON lit).
> • MAKING THE RAMP SHOT...first time locks the ball: Second time: starts MULTI-BALL™ play: Each successive time
>   advances playfield multiplier.

`EXTRA BALL, and playfield SPECIAL` is printed in bold italics; `MULTI-BALL™` in bold italics.

## PDF page 11 — Lamp, Solenoid and Switch Test

> LAMP TEST [...] 2. (From Sound Test) Use AUTO-UP and press ADVANCE. Test 01 should be indicated in the
> CREDITS display and all feature-lamps should flash.
>
> SOLENOID TEST [...] 2. (From Lamp Test) Use AUTO-UP and press ADVANCE. Test 02 should be indicated in the
> CREDITS display. The MATCH display sequences from 01 through 25. Corresponding solenoids are pulsed. The flipper
> relay is de-energized with sub-test 25.
> 3. Special solenoids (jet bumpers, kickers, etc.) are not pulsed during the Solenoid Test. Instead, you must
> check these solenoids manually. Press on their trigger switches or pull their switch-trigger lines low.
> 4. To continuously pulse a single solenoid use MANUAL-DOWN. Press ADVANCE to step through controlled solenoids
> one at a time. Use AUTO-UP to resume sequencing.
>
> SWITCH TEST [...] 2. (From Solenoid Test) Use AUTO-UP and press ADVANCE. Test 03 should be indicated in the
> CREDITS display with the switch numbers sequencing in the BALL-IN-PLAY display. As a switch number is displayed
> a sound is produced. As a switch is opened, its number is removed from the sequence. When all switches are
> open, the BALL-IN-PLAY display is blank and the sounds stop.

The `01 through 25` and `sub-test 25` wording is the generic System 9 procedure; the retained L-1 and L-2
solenoid-test runs step 01-16 only (runtime evidence).
