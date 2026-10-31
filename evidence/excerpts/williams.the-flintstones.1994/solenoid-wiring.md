# Williams The Flintstones (1994) — Solenoid wiring

Source: Williams *The Flintstones* Operations Manual 16-50029-101 (July 1994), IPDB machine 888 file
`Williams_1994_The_Flintstones_English_Manual.pdf`. Read from the native 300 dpi renders; each section
names its page. Text is transcribed as printed; `[?]` marks a reading the scan leaves uncertain.

## SOLENOID WIRING, PDF page 120 (printed page 3-6)

Document: `Williams_1994_The_Flintstones_English_Manual.pdf` (Operations Manual 16-50029-101, July 1994), IPDB machine 888. PDF page 120, printed page number (folio) **3-6**, printed title "SOLENOID WIRING". A schematic-style drawing: board outlines (dashed) on the left, connector blocks with pin numbers, labelled wires running right to boxes that name each device and its solenoid number. Wire colour labels are printed above each wire. All labels below are as printed (upper case); no connection was added that is not drawn.

### Left-hand boards and connectors (top to bottom)

Dashed outline labelled `POWER DRIVER BOARD` contains connectors J107, J118, J126, J127 and J130. A second dashed outline labelled `FLIPTRONIC II BOARD` contains J907 and J902.

#### POWER DRIVER BOARD

**J107** (pins drawn: 2, 3)
- pin 2: `RED-BRN, +50V` -> a bus that runs right and then down to the lower group (the Sol. 1-8 horizontal bus; see below).
- pin 3: `RED-BLK, +50V` -> a bus that runs right and then down to the upper group (the Sol. 9-16 horizontal bus; see below).

**J118** (pin drawn: 2)
- pin 2: `GRY-YEL, +12V` -> `MOTOR EMI BOARD` connector `J1` pin `1`.

**J126** (pin drawn: 7)
- pin 7: `BLU-VIO` (dotted segment next to the pin) -> `MOTOR EMI BOARD` connector `J1` pin `3`.

**MOTOR EMI BOARD** box: connector `J1` (pins drawn: `1` at the top, `3` at the bottom), connector `J2` (pins drawn: `2` at the top, `1` at the bottom). Wires from J2: pin 2 `RED`, pin 1 `BLK`, both to the motor symbol labelled `BOULDER MACHINE MOTOR` / `SOL. 23`.

**J127** (pins drawn: 1, 3, 4, 5, 6, 7, 8, 9) -> upper group (Low Power: Sol. 9-16, fed from the J107 pin 3 +50V bus):

| J127 pin | Wire label | Device box | Sol. |
|---|---|---|---|
| 1 | BRN-BLK | RIGHT SLING | SOL. 9 |
| 3 | BRN-RED | LEFT SLING | SOL. 10 |
| 4 | BRN-ORG | LEFT JET BUMPER | SOL. 11 |
| 5 | BRN-YEL | MIDDLE JET BUMPER | SOL. 12 |
| 6 | BRN-GRN | RIGHT JET BUMPER | SOL. 13 |
| 7 | BRN-BLU | DICTABIRD (printed `DICTABIRO`, see Uncertain readings) | SOL. 14 |
| 8 | BRN-VIO | LOWER LEFT DIVERTER | SOL. 15 |
| 9 | BRN-GRY | LOWER RIGHT DIVERTER | SOL. 16 |

(pin 2 is not drawn on J127.) The eight device boxes sit in a row, left to right in the order above (Sol. 9 to Sol. 16); a horizontal bus with a dot above each box connects the top of all eight boxes to the +50V line, and each box's bottom connects down/left to its J127 wire.

**J130** (pins drawn: 1, 2, 4, 5, 6, 7, 8, 9) -> lower group (High Power: Sol. 1-8, fed from the J107 pin 2 +50V bus):

| J130 pin | Wire label | Device box | Sol. |
|---|---|---|---|
| 1 | VIO-BRN | BALL TROUGH | SOL. 1 |
| 2 | VIO-RED | BALL SHOOTER | SOL. 2 |
| 4 | VIO-ORG | TOP DIVERTER POST | SOL. 3 |
| 5 | VIO-YEL | TOP POPPER | SOL. 4 |
| 6 | VIO-GRN | 3-BANK D. TGT | SOL. 5 |
| 7 | VIO-BLU | 4-BANK D. TGT | SOL. 6 |
| 8 | VIO-BLK | KNOCKER | SOL. 7 |
| 9 | VIO-GRY | TOP DIVERTER (printed `TOP OIVERTER`, see Uncertain readings) | SOL. 8 |

(pin 3 is not drawn on J130.) Again eight boxes in a row (Sol. 1 to Sol. 8) with a dotted +50V bus above them.

How the two +50V lines reach the groups, as drawn: the `RED-BRN, +50V` line from J107 pin 2 runs right to the right edge, then down and left to the bus above the Sol. 1-8 row (lower row); the `RED-BLK, +50V` line from J107 pin 3 runs right, then down to a dot above the right end of the bus over the Sol. 9-16 row (upper row).

#### FLIPTRONIC II BOARD

**J907** (pin drawn: 8)
- pin 8: `RED-GRY, +50V` -> splits (dot) to the top of both gate boxes: `RIGHT UP/DN GATE` `SOL. 35` and `LEFT UP/DN GATE` `SOL. 36`.

**J902** (pins drawn: 3, 1)
- pin 3: `YEL-GRY` -> `RIGHT UP/DN GATE`, `SOL. 35`.
- pin 1: `ORG-GRY` -> `LEFT UP/DN GATE`, `SOL. 36`.

### Other labels on the page

Title `SOLENOID WIRING` at the top centre. Board labels `POWER DRIVER BOARD` and `FLIPTRONIC II BOARD`. Device box labels exactly as in the tables above, each ending with its `SOL. n`. Folio `3-6`. Nothing is drawn for Sols. 17-22, 24-28 (they are on the next page, "Flashlamp Wiring") or for the Fliptronic flipper coils (Sols. 29-34).

### Cross-reference to the tables (informational)

- The connector pins drawn here (J107-2/-3, J118-2, J126-7, J127-1,3,4,5,6,7,8,9, J130-1,2,4,5,6,7,8,9, J902-3, J902-1, J907-8) match the Voltage Connection / Drive Connection cells of the Solenoid/Flashlamp Circuit table for Sols. 1-16, 23, 35, 36. The Knocker (Sol. 7) is printed with its voltage and drive pins under the Backbox sub-column in the table; this drawing does not distinguish.
- Sol. 7 (KNOCKER) in this drawing hangs on the same J107-pin-2 +50V bus as Sols. 1-6, 8, matching the `J107-2` entry in the table.

### Uncertain readings

- The device name printed in the Sol. 14 box reads `DICTABIRO` and the Sol. 8 box reads `TOP OIVERTER`; the scan renders the letter D as O in this font. Taken as DICTABIRD and TOP DIVERTER [?].
- The J126 connector shows only pin `7` here; the pin number is read as 7 (consistent with `J126-7` / `Blu-Vio` in the table).
- Which of the two J107 lines ends at the upper versus the lower +50V bus was traced by following the lines at 0.4x and 0.78x enlargement; the line junction dots are visible but the long horizontal runs were not individually zoomed [?].
- The wire label of J127 pin 6 reads `BRN-GRN`; the middle letters of `GRN` are slightly broken in the scan.
