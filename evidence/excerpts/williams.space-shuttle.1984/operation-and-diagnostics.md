# Literal transcription — corrections, ROM summary, game play, adjustments and test procedures

`reviewed: true`; transcribed by the curator from the scan's text layer (pdftotext 23.05.0 -layout) and corrected
against 300 dpi renders on 2026-10-30
`source: Instruction Manual PDF pages 3, 7, 8, 10, 11 and 13`

Retained renders: `external:pinmame-manuals/by-machine/williams.space-shuttle.1984/rendered-300/p-03.png`,
`p-07.png`, `p-08.png`, `p-10.png`, `p-11.png`, `p-13.png` (pdftoppm 23.05.0 -r 300 -gray).

Only the paragraphs this definition relies on are transcribed, each in full. OCR errors in the text layer
(`IPII` for `1P11`, `1.120` for `U20`, `boll` for `ball`) are corrected to the rendered page; `[…]` marks an
omitted paragraph.

## PDF 3 — CORRECTIONS (typed insert)

> Page 1 — 1. CIRCUIT BOARDS. CPU BOARD. Your level-9, CPU BOARD must be equipped with the ROMS specified in the
> ROM summary. Only jumpers W2, W5 through W7, W9, and W12 should be connected. Substitute W1 for W2 when a 6802
> microprocessor is used instead of a 6808 microprocessor.
>
> Page 13 — Switch Test: Paragraph 1. 1J9 (Rows) should be 1J10 (Rows). Paragraph 4. Change 1P9 to 1P10 and 1J9
> to 1J10.
>
> Page 15 — Under SYSTEM-9 MEMORY CHIP TEST: 1. No indication, U20 Game ROM 1 faulty. Solenoid Diagrams are
> reversed.
>
> Page 17 — Flash Lamp Connections: 1. Change 2.2, 1W to 5, 10W. 2. Change 330, 1W to 330, 2W.

## PDF 7 — ROM Summary

| IC | DESCRIPTION | TYPE | NUMBER | BOARD | PART NO. |
| --- | --- | --- | --- | --- | --- |
| Game-ROM 1 | 16Kx8 ROM | 27128 | U20 | CPU | A-5343-10767 |
| Sound ROM | 16Kx8 ROM | 27128 | U49 | CPU | A-5343-10768 |
| Speech ROM | 4Kx8 ROM | 2532 | U4 | Speech | A-5343-10785 |
| Speech ROM | 4Kx8 ROM | 2532 | U5 | Speech | A-5343-10786 |
| Speech ROM | 4Kx8 ROM | 2532 | U6 | Speech | A-5343-10787 |

## PDF 8 — Game Play and Game Operation

> S-H-U-T-T-L-E SPELLOUT: S-H-U-T-T-L-E value is selected randomly at the start of each ball. Hitting right-ramp
> target re-selects value. Hitting "T" drop target last awards 100,000 bonus.
>
> STOP & SCORE: Center-ramp shot freezes rolling numbers in score displays and awards frozen value.
>
> HEAT SHIELD: Center-ramp shot raises heat shield between flippers.
>
> SPINNER: Drop-target three-bank increases spinner value.
>
> EXTRA BALL: Right ramp scores extra ball after multiplier reaches 7X or spinner reaches 7,000.
>
> […]
>
> CREDIT POSTING. Insert coins. A sound is produced and the number of credits is displayed. If maximum credits*
> are exceeded by coin or high score, credits are posted correctly. But the coin-lockout coil de-energizes until
> the remaining credits are below the maximum. No credits may be won (and coins are rejected) while the
> coin-lockout coil is de-energized.
>
> GAME START. Push the CREDIT button. A start-up tune is played, a ball is served, and the CREDIT display is
> reduced by one. PLAYER 1 UP flashes until the first scoring-switch is made, and the BALL-IN-PLAY display shows
> 1. […]
>
> TILT. With the first closure of the ball-roll or playfield tilts, or the third* closure of the plumb-bob tilt,
> the player loses the rest of his turn. The slam tilt on the coin door returns the game to the Game-Over Mode.

`*` indicates adjustable feature (printed footnote).

## PDF 10-11 — Game-Adjustment Tables (functions used here)

> 29 Maximum Plumb-Bob Tilts (including warnings)
>
> 34 Game-Adjustment #4 - Gate Setting. 00: At beginning of each turn, gate is closed. 1: At beginning of each
> turn, gate is open. 2: At beginning of game, gate is open. (Gate position is stored in memory from ball to
> ball.)
>
> 37 Game-Adjustment #7 - New Or Old-Gate Setting. Note: The old gate energizes to let the ball drain. The new
> gate energizes to return the ball to the flipper. 00: For games with old gate. 01: For games with new gate.

The factory-setting column of these rows is not legible in the scan; the runtime evidence ran with the factory
settings the ROM writes into an empty CMOS.

## PDF 13 — Lamp, Solenoid and Switch tests

> LAMP TEST 2. (From Sound Test) Use AUTO-UP and press ADVANCE. Test 01 should be indicated in the CREDITS
> display and all feature-lamps should flash.
>
> SOLENOID TEST 1. Refer to your Solenoid Table for solenoid numbers and wiring. CPU-Board connections at plugs
> 1P11 and 1P12 are also shown there. 2. (From Lamp Test) Use AUTO-UP and press ADVANCE. Test 02 should be
> indicated in the CREDITS display. The MATCH display sequences from 01 through 25. Corresponding solenoids are
> pulsed. The flipper relay is de-energized with subtest 25. 3. Special solenoids (jet bumpers, kickers, etc.)
> aren't pulsed during the Solenoid Test. Instead, you must check these solenoids manually: Press on their
> trigger switches or pull their switch-trigger lines low. 4. To continuously pulse a single solenoid use
> MANUAL-DOWN. Press ADVANCE to sequence through controlled solenoids one at a time. Use AUTO-UP to resume
> sequencing.
>
> SWITCH TEST 1. Refer to the Switch-Matrix Table for switch numbers and wiring. CPU-Board connections at jacks
> 1J8 (columns) and 1J9 (rows) are also shown there. 2. (From Solenoid Test) Use AUTO-UP and press ADVANCE. Test
> 03 should be indicated in the CREDITS display with the switch numbers sequencing in the BALL-IN-PLAY display.
> As a switch number is displayed a sound is produced. As a switch is opened, its number is removed from the
> sequence. When all switches are open, the BALL-IN-PLAY display is blank and the sounds stop.

Read against the runtime evidence: this ROM's solenoid test steps 01-16 and wraps (the generic System 9 text's
01-25 and sub-test 25 do not apply), and its switch test names 1-49 and nothing above 49. The gameplay run
needed three playfield-tilt (49) closures to tilt, not the one the TILT paragraph describes.
