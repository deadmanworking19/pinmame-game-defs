# Williams The Flintstones (1994) — Flashlamp wiring

Source: Williams *The Flintstones* Operations Manual 16-50029-101 (July 1994), IPDB machine 888 file
`Williams_1994_The_Flintstones_English_Manual.pdf`. Read from the native 300 dpi renders; each section
names its page. Text is transcribed as printed; `[?]` marks a reading the scan leaves uncertain.

## FLASHLAMP WIRING, PDF page 121 (printed page 3-7)

Document: `Williams_1994_The_Flintstones_English_Manual.pdf` (Operations Manual 16-50029-101, July 1994), IPDB machine 888. PDF page 121, printed page number (folio) **3-7**, printed title "FLASHLAMP WIRING". A schematic-style drawing in two halves separated by a long dashed line: the upper half headed `PLAYFIELD FLASHLAMPS` (italic), the lower half headed `BACKBOX FLASHLAMPS` (italic). Each half has a dashed board outline labelled `POWER DRIVER BOARD` (printed `POWER ORIVER BOARD` in the lower half; see Uncertain readings) on the left with connectors, wires labelled with colour codes, and boxes for the devices.

### PLAYFIELD FLASHLAMPS (upper half)

Board: `POWER DRIVER BOARD`.

**J107** (pin drawn: 6)
- pin 6: `RED-WHT, +20V` -> a horizontal bus running right across the top; dots drop from it to the top of each of the flashlamp boxes listed below (Sols. 17, 18, 19, 20, 21, 22, 24 along the upper row, and via a right-hand return down to a bus over Sols. 25 and 28 in the lower row).

**J126** (pins drawn: 1, 2, 3, 4, 5, 6, 8):

| J126 pin | Wire label | Device box (as printed) | Sol. |
|---|---|---|---|
| 1 | BLK-BRN | UNDER LEFT RAMP FLS. | SOL. 17 |
| 2 | BLK-RED | UNDER RIGHT RAMP FLS. | SOL. 18 |
| 3 | BLK-ORG | FLINT-STONES FLS. | SOL. 19 |
| 4 | BLK-YEL | POPPER RAMP FLS. | SOL. 20 |
| 5 | BLU-GRN | DINO SLIDE FLS. | SOL. 21 |
| 6 | BLU-BLK | BOWL-O-RAMA FLS. | SOL. 22 |
| 8 | BLU-GRY | BOULDER MACHINE FLS. | SOL. 24 |

(pin 7 is not drawn on J126 in this drawing; J126 pin 7 `BLU-VIO` is the Boulder Machine motor wire on the Solenoid Wiring page.) The upper row of boxes runs left to right in the order above (Sol. 17, 18, 19, 20, 21, 22, 24).

**J122** (pins drawn: 1, 2) -> lower row of the playfield half, two boxes with the +20V bus above them:

| J122 pin | Wire label | Device box | Sol. |
|---|---|---|---|
| 1 | BLU-BRN | DIG MILLIONS FLS. | SOL. 25 |
| 2 | BLU-YEL | FRED'S CHOICE FLS. | SOL. 28 |

Note: the Solenoid/Flashlamp Circuit table (PDF 109 / 119) lists Sol. 28 on `J122-4`; this drawing shows the `BLU-YEL` wire for Sol. 28 on J122 pin `2` (verified at 3.5x enlargement; J122 shows only two pins, 1 and 2). The wire colour matches the table (`Blu-Yel`).

### BACKBOX FLASHLAMPS (lower half)

Board: `POWER DRIVER BOARD` (printed `POWER ORIVER BOARD`).

**J106** (pin drawn: 5)
- pin 5: `RED-WHT, +20V` -> a horizontal bus running right; dots drop from it to the tops of the boxes Sols. 17, 18, 19, 20, 21 (upper row), and a right-hand return runs down to a bus with a dot over the Sol. 26 / Sol. 27 boxes (lower row).

**J125** (pins drawn: 1, 2, 3, 5, 6):

| J125 pin | Wire label | Device box (as printed) | Sol. |
|---|---|---|---|
| 1 | BLK-BRN | UNDER LEFT RAMP FLS. | SOL. 17 |
| 2 | BLK-RED | UNDER RIGHT RAMP FLS. | SOL. 18 |
| 3 | BLK-ORG | FLINT-STONES FLS. | SOL. 19 |
| 5 | BLK-YEL | POPPER RAMP FLS | SOL. 20 |
| 6 | BLU-GRN | DINO SLIDE FLS. | SOL. 21 |

(pin 4 is not drawn on J125.)

**J124** (pins drawn: 2, 3) -> lower row of the backbox half:

| J124 pin | Wire label | Device box | Sol. |
|---|---|---|---|
| 2 | BLU-RED | FLINT FLS. | SOL. 26 |
| 3 | BLU-ORG | STONES FLS. | SOL. 27 |

Counts: playfield half has 9 device boxes (Sols. 17, 18, 19, 20, 21, 22, 24, 25, 28); backbox half has 7 boxes (Sols. 17, 18, 19, 20, 21, 26, 27). Connectors drawn: J107, J126, J122 (playfield half); J106, J125, J124 (backbox half). Sols. 17-21 therefore appear in both halves, as a playfield flashlamp (via J126) and as a backbox flashlamp (via J125), each with its own box. Sol. 22, 24, 25, 28 appear only in the playfield half; Sol. 26 and 27 only in the backbox half. Folio `3-7`.

### Cross-reference to the tables (informational)

- J126 pins 1-6 and 8, J125 pins 1, 2, 3, 5, 6, J124 pins 2 and 3, J122 pin 1, J107 pin 6 and J106 pin 5 agree with the Solenoid/Flashlamp Circuit table cells for the same Sol. numbers, except J122 pin 2 here versus `J122-4` in the table for Sol. 28.
- The device names on this drawing are the same as the table's Function cells; `UNDER LEFT RAMP FLS.`, `POPPER RAMP FLS.` and `BOULDER MACHINE FLS.` are spelled out where the table abbreviates (`Rmp`).

### Uncertain readings

- `POWER ORIVER BOARD` in the lower half: the scan renders D as O; taken as DRIVER [?]. The upper half reads `POWER DRIVER BOARD` clearly.
- The left edge of the `UNDER LEFT RAMP FLS.` box is clipped by its neighbour so the text reads `LEFT RAMP` with the leading `UNDER` / `L` partly overprinted in both halves; read as `UNDER LEFT RAMP FLS.` [?].
- The horizontal wire runs between the board and the boxes are long; the box each wire ends at was determined by following the vertical drop into the box at the stated x position, not by reading a label at the box end.
