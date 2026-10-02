Source: `Stern_1980_Quicksilver_Manual.pdf` (IPDB machine 1895, "English Manual [Stern Electronics]", 35 pages, a 300 dpi bilevel scan with no text layer), PDF page 22, the left part of the cabinet and door wiring schematic (drawing number `12B-432-S-121`, printed at lower left).
Hand-drawn schematic. The right part of the same sheet is on PDF page 23 (see the front-door jack excerpt).

Test and memory-clear controls at the top of the sheet:

| Printed label | Connection |
| --- | --- |
| `S33 MEMORY CLEAR` pushbutton | `A4J3-5 (-W-)` |
| `TEST SWITCH` | `A4J3-1 (R)`, common with `A3J2-7 (Y-R)` |

Matrix as drawn on this sheet: the same five strobe columns `ST0 A` to `ST4 E` and eight returns `I0` to `I7`, with the
returns leaving on the MPU connector `A4J3` here (the playfield sheet used `A4J2`):

| Return | Connection |
| --- | --- |
| I0 | A4J3-9 (BLU) |
| I1 | A4J3-10 (BRN-W) |
| I2 | A4J3-11 (R-W) |
| I3 | (no wire printed) |
| I4 | (no wire printed) |
| I5 | A4J3-14 (BLU-W) |
| I6 | A4J3-15 (BLU-O) |
| I7 | A4J3-16 (Y) |

Strobe lines run off the bottom of the grid: `A4J3-2 (R-Y)` for ST0 and `A4J3-3 (R-G)` for ST1; the lines for ST2-ST4 are
drawn but carry no label on this page.

Labelled cells in the ST0 column: `CHUTE #1` at I0, `CHUTE #2` at I1, `CHUTE #3` at I2, `CREDIT` at I5, `TILT` at I6 and `SLAM`
at I7. The TILT cell is drawn with an additional contact path below it, a second set of contacts with a small
pendulum-like symbol, so the tilt position carries more than one contact. The two cells at I3/ST4 and I4/ST4 are drawn as pairs of contacts feeding one diode; the other unlabeled
cells of the grid carry a switch symbol and a diode but no text.

Below the grid, three hard-wired flipper-button runs and the door lights:

| Printed label | Connection |
| --- | --- |
| `LEFT FLIPPER` contact | `A3J2-2 (BLU)` |
| `RIGHT FLIPPER` contact | `A3J2-1 (R)` |
| common return of both flipper contacts | `A2J2-9 (O)` |
| `FRONT DOOR LITES` | supply `A2J1-1 (Y-B)`, return `A2J2-5 (G-R)` |

At upper right: the `COIN LOCKOUT` coil with a diode, supply `A2J2-2 (G)` and return `A3J2-8 (Y-W)`; a further wire
`A3J2-5 (B-Y)` leaves toward the knocker on the next page.

Notes, verbatim: `N/U = NOT USED`; `ALL DIODES ARE 1N-4004`.
