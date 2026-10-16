# Corvette (Bally, 1994) - Motor boards: slave board, motor driver master board, dual H-drive controller, engine hall adjustment (PDF pages 137-141, plus amendment 16-9890 pages a-08, a-09, a-11, a-12)

Transcribed from the Corvette service manual scan (rendered at 300 dpi as `m-NNN.png`, NNN = PDF page) and from Amendment 16-9890 (rendered as `a-NN.png`). Each heading below is one page and carries its printed title, assembly number and printed folio. Read from the rendered page, not from the OCR text.

| Source page | Printed folio | Printed title | Content transcribed |
| --- | --- | --- | --- |
| m-137 | 3-23 | Slave Board A-18533 | whole page (pin lists, board drawing, block diagram, engine bottom view labels) |
| m-138 | 3-24 | Slave Board Schematic A-18533 | whole page (schematic labels) |
| m-139 | 3-25 | Motor Driver Master Board A-18532 | whole page (pin list, board drawing, schematic) |
| m-140 | 3-26 | Dual H-Drive Motor Controller P.C.B. Assembly A-19159 | whole page (pin lists, board drawing, wiring diagram) |
| m-141 | 3-27 | Dual H-Drive Motor Controller Schematic A-19159 | whole page (schematic labels) |
| a-08 | 8 (amendment page number) | Section 2 Corrections/Changes: Page 2-14, A-19625 / A-19243 | the A-19625 entry and its parts list |
| a-09 | (see its section) | Motor Driver Slave Board Schematic A-19625 | whole page |
| a-11 | (see its section) | Engine block changes; A-19711 Hall Adjustment Assembly | engine item changes and the A-19711 parts list |
| a-12 | (see its section) | Hall Offset Adjust P.C.B. schematic A-19706 | whole page |

Conventions: spelling, capitalization, hyphenation and punctuation are as printed. A line of printed text is given in a code span. Drawing labels are listed in the order printed. Wire routing that I followed by eye rather than read as a printed word is marked `(traced)`. `[?]` marks an unreadable character; see the final section.

## m-137 - printed title `Slave Board` `A-18533`, folio `3-23`

Board drawing (top): outline with connectors `J1` (four positions, `4` at the top and `1` at the bottom, key mark at position 3), `J2` (six positions, `6` at the top and `1` at the bottom, key mark at position 2), `J3` (a long rectangular socket, pin `1` at the top), `J5` (nine positions, `1` at the top and `9` at the bottom, key mark at position 6), `J4` (five positions, `1` at the top and `5` at the bottom, key mark at position 4).

Pin lists, two columns:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Red +20VDC to A-19158` |
| J1-2 | `J1-2 Yellow to A-19158` |
| J1-3 | `J1-3 Key` |
| J1-4 | `J1-4 Black ground to A-19158` |
| J2 | `J2 Not Used` |
| J3 | `J3 Ribbon Cable from Master Driver A-18532 J3` |
| J4-1 | `J4-1 Red-White +20VDC from J107-6` |
| J4-2 | `J4-2 Red-White loop from J4-1` |
| J4-3 | `J4-3 Black loop from J4-5` |
| J4-4 | `J4-4 Key` |
| J4-5 | `J4-5 Black ground from J116-3` |
| J5-1 | `J5-1 Red to engine coil (see below)` |
| J5-2 | `J5-2 Yellow to engine coil (see below)` |
| J5-3 | `J5-3 Orange to engine coil (see below)` |
| J5-4 | `J5-4 Brown to engine coil (see below)` |
| J5-5 | `J5-5 Violet-Yellow to engine coil (see below)` |
| J5-6 | `J5-6 Key` |
| J5-7 | `J5-7 Violet-Orange to engine coil (see below)` |
| J5-8 | `J5-8 Violet-Red to engine coil (see below)` |
| J5-9 | `J5-9 Violet-Brown to engine coil (see below)` |

Block diagram (bottom). Boxes and labels: `CPU BOARD` with connectors `J204` and `J211`; `MOTOR DRIVER MASTER P.C.B.` `A-18532` with connectors `J1`, `J2` (pins drawn `3 4 ... 1`) and `J3`; `LINEAR HALL EFFECT SENSOR` `A-19158` with three wires; `SLAVE BOARD` `A-18533` with connectors `J1`, `J3`, `J4`, `J5`; `POWER DRIVER BOARD` with connectors `J113`, `J116` (pins `4` `3`) and `J107` (pin `6`).

- `Ribbon Cable` from `J204` (CPU board) to `J1` (master board).
- `Ribbon Cable` from master `J3` to slave `J3`.
- `J211` (CPU board) drawn as five parallel lines to `J113` on the Power Driver Board.
- Master board `J2`: wires printed along their length, `Gray` `+5VDC` (from `J116` pin 4 to `J2` pin 3), `Black` `Ground` (from `J116` pin 3 to `J2` pin 4), `Red-White` `+20VDC` (from `J107` pin 6 to `J2` pin 1) (traced). The `Black` ground and `Red-White` `+20VDC` lines also continue to slave `J4` (traced): slave `J4` pins drawn `5 3 2 1`, with `5` and `3` strapped together and `2` and `1` strapped together.
- Hall sensor wires to slave `J1`: `Black` (pin 4), `Yellow` (pin 2), `Red` (pin 1).
- Slave `J5`, pins drawn top to bottom `3 7 4 9 1 8 2 5`, wires printed beside them: `Orange` (3), `Violet-Orange` (7), `Brown` (4), `Violet-Brown` (9), `Red` (1), `Violet-Red` (8), `Yellow` (2), `Violet-Yellow` (5), going to the engine connector.
- Engine bottom view, caption `Engine (Bottom View)`, wire labels at the engine, in the order printed (top to bottom): `VIOLET/YELLOW`, `YELLOW`, `VIOLET/RED`, `RED`, `ORANGE`, `VIOLET/ORANGE`, `BROWN`, `VIOLET/BROWN`. The drawing shows four coils (two upper, two lower) each with two leads, joined to one multi-pin connector.

Folio: `3-23`.

## m-138 - printed title `Slave Board Schematic` `A-18533`, folio `3-24`

One schematic, drawn in normal page orientation with small text, connectors `J2` and `J5`, `J4` along the top, `J3` and `J1` at the lower left and right. It was read after rotating tiles of the page. Connectors, each with the bracketed heading printed beside it:

| Connector | Printed heading | Pin legend as printed |
| --- | --- | --- |
| `J2` | `(LED OUTPUTS)` | 1 `+12V`; 2 `KEY`; 3 `LEDA1`; 4 `LEDA2`; 5 `LEDB1`; 6 `LEDB2` |
| `J5` | `(SOLENOID DRIVE OUTPUTS)` | 1 `SOLB1`; 2 `SOLB2`; 3 `SOLA1`; 4 `SOLA2`; 5 `20V`; 6 `KEY`; 7 `20V`; 8 `20V`; 9 `20V` |
| `J4` | `(SOLENOID POWER SUPPLY INPUT)` | 1 `20V`; 2 `20V`; 3 `PWR_GND`; 4 `KEY`; 5 `PWR_GND` |
| `J3` | `(FROM MASTER BOARD J3)` | 26-pin dual row, left column `1 3 5 7 9 11 13 15 17 19 21 23 25`, right column `2 4 6 8 10 12 14 16 18 20 22 24 26` (see below) |
| `J1` | `(HALL EFFECT SENSE INPUT)` | 1 `+5V`; 2 `SENSE`; 3 `KEY`; 4 `GND` |

(`J2` pin 2, `J5` pin 6 and `J4` pin 4 `KEY` are drawn with no connection. A `+12V` supply flag is attached to `J2` pin 1.)

`J3` connections as drawn:

| J3 pin | Printed label / connection |
| --- | --- |
| 1, 3, 5, 7, 9, 11, 13, 15, 17, 25 | strapped together to a ground symbol |
| 2, 4, 6, 8, 10, 12, 14, 16 | the eight data lines `D0` to `D7`, printed collectively with a slash mark and the legend `D0-D7` (each `D` overlined), to the `AD7524` data pins |
| 18 | `DRV_DISABLE_B` (traced) |
| 20 | `DRV_DISABLE_A` (traced) |
| 22 | `LEDA1` (traced) |
| 23 | `LEDA2` (traced) |
| 21 | `LEDB1` (traced) |
| 19 | `LEDB2` (traced) |
| 24, 26 | to the `+12V` supply (junction dot) |

Solenoid (engine coil) drive section (values as printed, roles traced):

| Part | Printed value | Role (traced) |
| --- | --- | --- |
| `Q3` | `TIP102` | drives `SOLB1` (`J5-1`) |
| `Q5` | `TIP102` | drives `SOLB2` (`J5-2`) |
| `Q4` | `TIP102` | drives `SOLA1` (`J5-3`) |
| `Q6` | `TIP102` | drives `SOLA2` (`J5-4`) |
| `D2`, `D4`, `D3`, `D5` | `1N4004` | one on each of `Q3`, `Q5`, `Q4`, `Q6` to the `20V` rail |
| `R39`, `R41`, `R40`, `R42` | `0.5  5W` | emitter resistor of `Q3`, `Q5`, `Q4`, `Q6` respectively |
| `R32`, `R33`, `R34`, `R35` | `220` | base resistor of `Q3`, `Q5`, `Q4`, `Q6` |
| `C16`, `C15`, `C13`, `C14` | `.33` | base-to-ground capacitor of `Q3`, `Q5`, `Q4`, `Q6` |

- The base resistors of `Q3` and `Q5` are joined to a line labelled (printed vertically, one letter per line) `DRIVE B`; those of `Q4` and `Q6` to a line labelled `DRIVE A`.
- `DRIVE B` is fed through `R30` `220` from the output (pin `14`) of `U1D` (`LM324`, `+` pin 12, `-` pin 13, supply pin 4); `R26` `100K` runs from `U1D` output back to its `+` input node. `DRIVE A` is fed through `R44` `220` from the output (pin `14`) of `U3D` (`LM324`, `+` pin 12, `-` pin 13); `R38` `100K` from its output back to its `+` input node.
- `R27` `10K` joins the `U1C` output (pin 8) to the `U1D` `-` input node; `R28` `10K` runs from the `U1C` output downward; `R43` `10K` from the `U3D` `-` input node; `R29` `10K` between two nodes next to `U3A`.
- `J5` pins 5, 7, 8, 9 and `J4` pins 1 and 2 tie to the `20V` rail (the line carrying the diode cathode side); `J4` pins 3 and 5 `PWR_GND` to the emitter-resistor ground line.

Control and bias section (labels as printed):

- `DRV_DISABLE_B` through `R36` `1K` to the base of `Q1` `2N3904`; `DRV_DISABLE_A` through `R37` `1K` to the base of `Q2` `2N3904`; both emitters to ground; collectors go up toward the drive lines (not fully followed). `R18` `10K` and `R19` `10K` pull the two disable lines up to `+12V`.
- `U2` `AD7524` (DAC), legend as printed on the symbol: left side `14` `VDD`, `13` `WR`, `12` `CS`, `11` `D0`, `10` `D1`, `9` `D2`, `8` `D3`, `7` `D4`, `6` `D5`, `5` `D6`, `4` `D7`; right side `1` `OUT1`, `2` `OUT2`, `15` `VREF`, `16` `VERFB` (as printed), `3` `GND`. `VDD` to `+12V`; `OUT1` to `+5V`; `OUT2` and `GND` to ground; `WR` and `CS` tied to ground (junction dot at `CS`); data pins each tied through `R10` to `R17` (printed as the group `R10-R17` `10K X 8`) to `+12V`. `VREF` goes through `R9` `10K` `1%` to a node with `R8` `20K` `1%` (to `+5V`) and `R7` `20K` `1%` (to ground), and on to the `+` input (pin 5) of `U1B`.
- `U1B` `LM324` (`+` pin 5, `-` pin 6, output pin 7, supply pin 4): `R4` `10K` `1%` and `C3` `0.47` `5%` at its `-` side; `R24` `12.1K` `1%` from its output; `R3` `10K` `1%` from the `-` node down.
- `V/2 REF`: `R5` `10K` `1%` (from `+5V`) and `R6` `10K` `1%` (to ground) divider with `C1` `10` (`+` marked) to ground.
- `U1C` `LM324` (output pin 8, `+` pin 10, `-` pin 9): `C4` `0.1, 5%` and `R25` `10K` `1%` in its feedback.
- `U1A` `LM324` (`+` pin 3, `-` pin 2, output pin 1, supply pin 4) with `R2` `160K` and `R1` `10K` at its `-` input; `U3A` `LM324` (`+` pin 3, `-` pin 2, output pin 1) with `R29` `10K`.
- `BIAS` net: `R31` `620` `1%` from `+5V`, zener `D1` `1N5225B` `3.0V` `500mW` to ground, `C12` `10` (`+` marked) to ground.
- `J1`: `+5V` to its supply flag, `SENSE` (pin 2) to a long line running to the comparator input area, `GND`.

Supply and indicator section: `U1` box, pin `4` to `+5V` and pin `11` to ground, `C2` `.1`; `U2` box, pins `1` and `14` to `+5V` and `+12V` respectively, pin `3` to ground, `C5` `.1` and `C6` `.1`; `U3` box, pin `4` to `+5V` and pin `11` to ground, `C11` `.1`. Regulator `U4` `7805` (pin `1` from `+12V`, pin `2` ground, pin `3` out to `+5V`) with `C7` `100` (`+` marked) and `C8` `.33` on its input and `C10` `100` (`+` marked) and `C9` `.33` on its output. `LED1` with `R45` `270` from `+5V` to ground. LED outputs: `R20` `820`, `R21` `820`, `R22` `820`, `R23` `820`, one in each of the four lines `LEDA1`, `LEDA2`, `LEDB1`, `LEDB2` between `J3` and `J2`.

Folio: `3-24`.

## m-139 - printed title `Motor Driver Master Board` `A-18532`, folio `3-25`

Board drawing (top): outline with connector `J2` (five positions, `1` at the left and `5` at the right, key mark at position 2), connector `J1` (long socket at the left edge, `1` at the top), connector `J3` (long socket at the right edge, `1` at the bottom).

Pin list (printed as plain lines, in this order):

| Pin | Printed text |
| --- | --- |
| J1 | `J1 Ribbon Cable from J204` |
| J2-1 | `J2-1 Red-White +20VDC from 107-6` |
| J2-2 | `J2-2 Key` |
| J2-3 | `J2-3 Gray +5VDC from J116-4` |
| J2-4 | `J2-4 Black ground from J116-3` |
| J2-5 | `J2-5 Not Used` |
| J3 | `J3 Ribbon Cable to Slave Board A-18533 J3` |

(`107-6` in `J2-1` is printed without the leading `J`.)

Schematic (caption `Schematic`, below it). `J1` is headed `(FROM j204 OF WPC CPU)` (printed with a lowercase `j`). It is a 26-pin dual-row connector, left column `26 24 22 ... 4 2`, right column `25 23 21 ... 3 1`:

| J1 pin | Printed label / connection |
| --- | --- |
| 25 | `D0` |
| 23 | `D1` |
| 21 | `D2` |
| 19 | `D3` |
| 17 | `D4` |
| 15 | `D5` |
| 13 | `D6` |
| 11 | `D7` |
| 9 | `BLANK` |
| 7 | stub, no label, no connection |
| 5 | line with no label, goes to the `CLK` input (pin 11) of `U1` (traced) |
| 3 | `DIS2` |
| 1 | stub, no label, no connection |
| 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4 | strapped together to a ground symbol |
| 2 | stub, no label, no connection |

Parts and connections as printed (those marked `(traced)` followed by eye):

- Data lines `D0` to `D7` run from `J1` to `U1` `74LS374` pins `3 4 7 8 13 14 17 18` (`D0` to `D7`). `D0`, `D1`, `D2` also branch (junction dots) down to `U2` inputs `D1` (pin 4), `D2` (pin 5), `D3` (pin 12) respectively (traced).
- `U1` `74LS374`: outputs `Q0` to `Q7` on pins `2 5 6 9 12 15 16 19`; `OC` (pin 1, inversion bubble) to ground; `CLK` (pin 11) from `J1` pin 5. Supply: pin `20` to `+5V`, pin `10` to ground, `C6` `.1`.
- Series resistors `R15` `R14` `R13` `R12` `R11` `R10` `R9` `R8` (no values printed) from `U1` `Q0` to `Q7` to `U3` inputs `A1` to `A8` (pins `1` to `8`).
- `U3` `ULN2803`: `G` (pin 9) to ground; outputs `Y1` to `Y8` on pins `18 17 16 15 14 13 12 11`, each drawn with an inversion bubble; `CLAMP` (pin 10) to `+12V`; supply bypass `C8` `.1` with pin `10` to `+12V` and pin `9` to ground. `Y1` to `Y8` go straight across to `J3` pins `2 4 6 8 10 12 14 16`; a dashed slash with the legend `D0-D7` (each `D` overlined) marks them.
- `U2` `74LS374` (only part of it drawn): `D1` (pin 4), `D2` (pin 5), `D3` (pin 12) from the data lines as above; `D4` (pin 13) to ground; `CLK` (pin 9) from `J1` pin 3 `DIS2` (traced); `CLR` (pin 1, inversion bubble) to the node that joins `U4` `Y7` and `R17` (traced). Outputs: `Q1` (pin 2), `Q1` overlined (pin 3, stub), `Q2` (pin 7), `Q2` overlined (pin 6, stub), `Q3` (pin 10), `Q3` overlined (pin 11, stub), `Q4` (pin 15, stub), `Q4` overlined (pin 14, stub). Supply: pin `16` to `+5V`, pin `8` to ground, `C5` `.1`.
- `U2` `Q1` goes to `R6` `1K` and `R5` `1K` (both fed from the same node) to `U4` `A1` and `A2`; `Q2` goes to `R4` `1K` and `R3` `1K` to `U4` `A3` and `A4`; `Q3` goes to `R2` `1K` and `R1` `1K` to `U4` `A5` and `A6`. `J1` pin 9 `BLANK` goes through `R16` `1K` to `U4` `A7`, and also through `R7` `330` to ground (traced). `A8` and `G` of `U4` go to ground.
- `U4` `ULN2803`: outputs `Y1` to `Y8` on pins `18 17 16 15 14 13 12 11`, each with an inversion bubble; `CLAMP` (pin 10) to `+12V`; supply `+12V` on pin `10`, ground pin `9`, `C7` `.1`. `Y7` (pin 12) goes to a node that joins `R17` `10K` to `+5V` and the `CLR` pin of `U2`; `Y8` (pin 11) is a stub, no connection.
- `U4` outputs go to `J3` (traced; the outermost loop is printed last): `Y1` `DISABLE B` (to `J3` pin 18), `Y2` `DISABLE A` (pin 20), `Y3` `LEDA1` (pin 22), `Y4` `LEDA2` (pin 23), `Y5` `LEDB1` (pin 21), `Y6` `LEDB2` (pin 19).
- Supply flags: `+5V` (four), `+12V` (three), ground symbols.

`J3` is headed `(TO SLAVE BOARD J3)`, 26-pin dual row, drawn with the even pins `2 4 6 ... 26` in the left column and the odd pins `1 3 5 ... 25` in the right column:

| J3 pin | Printed label / connection (traced) |
| --- | --- |
| 2, 4, 6, 8, 10, 12, 14, 16 | `U3` `Y1` to `Y8`, legend `D0-D7` (each `D` overlined) |
| 18 | `DISABLE B` |
| 20 | `DISABLE A` |
| 22 | `LEDA1` |
| 23 | `LEDA2` |
| 21 | `LEDB1` |
| 19 | `LEDB2` |
| 24, 26 | to a `+12V` supply flag (a junction dot joins them) |
| 1, 3, 5, 7, 9, 11, 13, 15, 17, 25 | strapped together to ground |

Folio: `3-25`.

## m-140 - printed title `Dual H-Drive Motor Controller P.C.B. Assembly` `A-19159`, folio `3-26`

Board drawing (top, dotted outline): connector `J1` (eleven positions, `11` at the top and `1` at the bottom, key mark at position 9), connector `J2` (four positions, `1` at the top and `4` at the bottom, key mark at position 3), connector `J3` (four positions, `1` at the top and `4` at the bottom, key mark at position 2).

Pin lists, two columns:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Not Used` |
| J1-2 | `J1-2 Black-Orange from J126-3` |
| J1-3 | `J1-3 Not Used` |
| J1-4 | `J1-4 Black-Red from J126-2` |
| J1-5 | `J1-5 Not Used` |
| J1-6 | `J1-6 Black-Brown from J126-1` |
| J1-7 | `J1-7 Not Used` |
| J1-8 | `J1-8 Black-Brown loop from J1-6` |
| J1-9 | `J1-9 Key` |
| J1-10 | `J1-10 Black ground from J116-3` |
| J1-11 | `J1-11 Red-White +20VDC from J107-6` |
| J2-1 | `J2-1 Red-White +20VDC to Sol 18` |
| J2-2 | `J2-2 Not Used` |
| J2-3 | `J2-3 Key` |
| J2-4 | `J2-4 Black ground to Sol 18` |
| J3-1 | `J3-1 Red-White +20VDC to Sol 19` |
| J3-2 | `J3-2 Key` |
| J3-3 | `J3-3 Not Used` |
| J3-4 | `J3-4 Black ground to Sol 19` |

Wiring diagram (bottom): box `POWER DRIVER BOARD` (label printed on four lines `POWER` `DRIVER` `BOARD`) with connectors `J107` (pin `6`), `J116` (pin `3`) and `J126` (pins `1` `2` `3`); box `DUAL H-DRIVE MOTOR CONTROLLER P.C.B.` `A-19159` with `J1` (pins drawn top to bottom `11` `10` `8` `6` `4` `2`), `J2` (pins `1` `4`) and `J3` (pins `1` `4`); two solenoid symbols `Sol. 18` and `Sol. 19`.

| From | Printed wire label | To |
| --- | --- | --- |
| `J107` pin 6 | `Red-White +20VDC` | `J1` pin 11 |
| `J116` pin 3 | `Black Ground` | `J1` pin 10 |
| `J126` pin 1 | `Black-Brown` | `J1` pin 6 (a dot at the junction joins it to `J1` pin 8) |
| `J126` pin 2 | `Black-Red` | `J1` pin 4 |
| `J126` pin 3 | `Black-Orange` | `J1` pin 2 |
| `J2` pin 1 | `Red-White +20VDC` | `Sol. 18` |
| `J2` pin 4 | `Black Ground` | `Sol. 18` |
| `J3` pin 1 | `Red-White +20VDC` | `Sol. 19` |
| `J3` pin 4 | `Black Ground` | `Sol. 19` |

Folio: `3-26`.

## m-141 - printed title `Dual H-Drive Motor Controller Schematic` `A-19159`, folio `3-27`

The schematic is drawn rotated 90 degrees on the page; it was read after rotating. No note text was found on the page for the `SEE NOTE 1` references.

Connector `J1` (legend printed beside the pins; pins `11` at the top and `1` at the bottom):

| J1 pin | Printed label |
| --- | --- |
| 11 | `+12 to +20 VDC` |
| 10 | `GND` |
| 9 | `KEY` (and `n.c.` printed at the pin) |
| 8 | `DIR_1` |
| 7 | `DIR_1` |
| 6 | `DIR_2` |
| 5 | `DIR_2` |
| 4 | `ENABLE_1` |
| 3 | `ENABLE_1` |
| 2 | `ENABLE_2` |
| 1 | `ENABLE_2` |

(Pins 8 and 7, 6 and 5, 4 and 3, 2 and 1 are drawn strapped together in pairs.)

Supply and indicator section: `+V` rail; `D1` `1N4004` to `VCC_1` with `C1` `100/35` (`+`) and `C2` `.01` to ground; `D2` `1N4004` to `VCC_2` with `C3` `100/35` (`+`) and `C4` `.01` to ground; `R1` `2K` and `LED1` from `+V` to ground.

Motor 1 half (printed `MOTOR 1` beside `J2`), as printed:

- Output connector `J2`: pin `1` `+`, pin `2` `n.c.`, pin `3` `KEY`, pin `4` `-` (pins 2 and 3 marked with an `x`).
- Output stage: `Q1` `TIP 102`, `Q2` `TIP 107`, `Q3` `TIP 102`, `Q4` `TIP 107`; diodes `D4` `1N4004` (Q1 emitter), `D5` `1N4004`, `D6` `1N4004`, `D7` `1N4004` (Q3 emitter), `D8` `1N4004`, `D9` `1N4004`; inductors `L1` `4.7uH`, `L2` `4.7uH`; capacitor `C7` `.01` across `J2`; jumper `JP1` with `R13` `5.6` `5W` in a dashed box labelled `BLOCK C` `SEE NOTE 1`.
- Drive: comparators `U1D` `LM339` (pin 13 out, 11 `+`, 10 `-`) and `U1C` `LM339` (pin 14 out, 9 `+`, 8 `-`); resistors `R5` `4.7K`, `R6` `10K`, `R7` `10K`, `R10` `4.7K`, `R11` `10K`, `R12` `10K`, `R8` `4.7K`, `R9` `10K`, `R2` `4.7K`, `R3` `4.7K`, `R4` `10K`; `C6` `.01` with `VCC_1`; `D3` `1N4004` and `D10` `1N4004`.
- Block A (dashed box labelled `BLOCK A` `SEE NOTE 1`): `Q5` `TIP 102` with `R14` `4.7K` and `R15` `4.7K` from `+V`.

Motor 2 half (printed `MOTOR 2` beside `J3`), as printed:

- Output connector `J3`: pin `1` `+`, pin `2` `n.c.`, pin `3` `KEY`, pin `4` `-`.
- Output stage: `Q6` `TIP 102`, `Q7` `TIP 107`, `Q8` `TIP 102`, `Q9` `TIP 107`; diodes `D12`, `D13`, `D14`, `D15`, `D16`, `D17` (each `1N4004`); inductors `L3` `4.7uH`, `L4` `4.7uH`; capacitor `C9` `.01` across `J3`; jumper `JP2` with `R27` `5.6` `5W` in a dashed box labelled `BLOCK D` `SEE NOTE 1`.
- Drive: comparators `U1A` `LM339` (pin 1 out, 7 `+`, 6 `-`; pin 3 `VCC`, pin 2 ground, with `C5` `.01`) and `U1B` `LM339` (pin 2 out, 5 `+`, 4 `-`); resistors `R16` `4.7K`, `R17` `4.7K`, `R18` `10K`, `R19` `4.7K`, `R20` `10K`, `R21` `10K`, `R22` `4.7K`, `R23` `10K`, `R24` `4.7K`, `R25` `10K`, `R26` `10K`; `C8` `.01` with `VCC_2`; `D11` `1N4004`.
- Block B (dashed box labelled `BLOCK B` `SEE NOTE 1`): `Q10` `TIP 102` with `R28` `4.7K` and `R29` `4.7K` from `+V`; diode `D18` `1N4004`.

Net names printed: `VCC_1`, `VCC_2`, `+V`, `DIR_1`, `DIR_2`, `ENABLE_1`, `ENABLE_2`. Folio: `3-27`.

## a-08 (A-19625 Motor Driver Slave Board lines only) - amendment 16-9890 page headed `SECTION 2` `Corrections/Changes`, page number printed at the bottom `8`

Only the Page 2-14 entry is transcribed here (the A-19606 entry is in `section-3-boards.md`). The page is clipped at its right edge by the scan; clipped words are marked.

- `Page 2-14   Printed Circuit Boards` / `Item #1 changed to A-19625  Motor Driver Slave Board Assembly.`
- Heading line: `A-19243   Motor Driver Slave Board & Bracket Assembly`

Parts list, columns `Part Number`, `Designator`, `Description`, left half of the page; the first line is marked with a circled `1` at the left margin (item #1):

| Part Number | Designator | Description |
| --- | --- | --- |
| `A-19625` | (blank) | `Motor Driver Slave Board` |
| `5040-12808-00` | `C1, C12` | `Cap., 10µFd, 35v, Axial` |
| `5040-10974-00` | `C7, C10` | `Cap., 100µFd, 35v, Radial` |
| `5040-12751-00` | `C13-C16` | `Cap., 4.7µFd, 10v, Axial` |
| `5043-12807-00` | `C3` | `Cap., 1µFd, 50v, Axial` |
| `5043-09845-00` | `C4` | `Cap., 1KP, 50v, ±20% Axial` |
| `5043-08996-00` | `C2, C5, C6,C8,` (continued) `C9, C11, C17, C18, C22` | `Cap., 0.1µFd, 50v, ±20% Ax` (cut off by the column edge) |
| `5370-12960-00` | `U1, U3` | `IC LM324N OPAMP` |
| `5371-12727-00` | `U2` | `IC DAC AD7524` |
| `5250-09157-00` | `U4` | `Reg 7805 1.0A. 5V` |
| `5070-09054-00` | `D2 - D5` | `Diode, 1N4004 1.0A.` |
| `5160-10269-00` | `Q1, Q2` | `Trans 2N3904 NPN` |
| `5162-12635-00` | `Q3 - Q6` | `Trans TIP102` |
| `5013-14455-00` | `R48` | `Res., 1.62KW, 1/4w, 1%` |
| `5671-13732-00` | `LED1` | `Display LED Red` |
| `5013-14135-00` | `R3-R6, R9,` (continued) `R27-R29, R43` | `Res., 10KW, 1/4w, 1%` |
| `5010-09269-00` | `R24` | `Res., 12KW, 1/4w, 5%` |
| `5013-14136-00` | `R7, R8, R26,` (continued) `R38, R46, R47` | `Res., 20KW, 1/4w, 1%` |
| `5013-14456-00` | `R31` | `Res., 3.32KW, 1/4w, 1%` |
| `5010-12065-00` | `R2` | `Res., 120KW, 1/4w, 5%` |
| `5010-09534-00` | `JP1` | `Res., 0W` |
| `5010-08984-00` | `R36, R37, R49` | `Res., 1.0KW, 1/4w, 5%` |
| `5010-09034-00` | `R1, R10-R19,` (continued) `R52, R56` | `Res., 10KW, 1/4w, 5%` |
| `5010-09999-00` | `R45` | `Res., 2KW, 1/4w, 5%` |
| `5070-08919-00` | `D6, D7` | `Diode, 1N4148 1500MA` |
| `5010-09160-00` | `R32 - R35` | `Res., 220W, 1/4w, 5%` |
| `5012-14318-00` | `R39 - R42` | `Res., 0.51W, 5w, 5%` |
| `5791-10862-05` | `J4` | `Connector, 5-Pin Header` |
| `5791-10862-09` | `J5` | `Connector, 9-Pin Header` |
| `5791-10850-00` | `J3` | `Connector, 26-Pin Header` |
| `5791-13830-04` | `J1` | `Connector, 4-Pin Header` |

Right half of the page (same three columns):

| Part Number | Designator | Description |
| --- | --- | --- |
| `5010-09314-00` | `R53` | `Res., 1.2KW, 1/4w, 5%` |
| `5705-12454-00` | `Q3 - Q6` | `Heatsink, w/pins` |
| `4004-01005-06` | `Q3 - Q6` | `Mach. Screw, 4-40 x 3/8` (cut off after `3/`) |
| `4404-01119-00` | `Q3 - Q6` | `Nut, 4 x 40 SNUT` |
| `5010-09035-00` | `R25` | `Res., 47KW, 1/4w, 5%` |
| `5010-09036-00` | `R30, R44` | `Res., 100W, 5%, 1/4w` |
| `5010-08991-00` | `R50, R54` | `Res., 4.7KW, 1/4w, 5%` |
| `5010-09086-00` | `R51, R55` | `Res., 6.8KW, 1/4w, 5%` |
| `5043-08980-00` | `C19-C21, C23` | `Cap., 0.01M, 50v` (continued) `(+80,-20%)Axial` |

Below the right-half list, two further lines carry circled numbers at the left of the column (the circled digits are partly cut by the column edge and read as `2` and `3`):

| Circled item | Part Number | Designator | Description |
| --- | --- | --- | --- |
| 2 | `01-10756` | `-` | `Bracket` |
| 3 | `07-6688-18N` | `-` | `Rivet, 3/16 x 1/8"` |

Printed component-side placement drawing under the list (clipped at the right edge): connectors `J4` (five positions) and `J5` (nine positions) at the left edge, four heatsink/transistor blocks (two upper, two lower), capacitors, the resistor group at the right edge, `U3`, `U4`, `U1` ICs, and a circled `1` at lower right with a leader line. Silkscreen designators on the drawing are blurred; none was transcribed individually. Folio: page number `8`.

## a-09 - amendment 16-9890 page printed title `Motor Driver Slave Board Schematic` `A-19625`, page number printed at the bottom `9`

One schematic (small, low-contrast print, read after rotating tiles of the page). It replaces the A-18533 schematic (m-138) for the A-19625 board. Values here are printed in the amendment's style (`10.0K`, `20.0K`, `4.7/10`). Differences from m-138 are listed at the end.

Connectors, with headings as printed:

| Connector | Printed heading | Pin legend as printed |
| --- | --- | --- |
| `J5` | `(SOLENOID DRIVE OUTPUTS)` | 1 `SOL B1`; 2 `SOL B2`; 3 `SOL A1`; 4 `SOL A2`; 5 `20V`; 6 `KEY` (star-marked, no connection); 7 `20V`; 8 `20V`; 9 `20V` |
| `J4` | `(SOLENOID POWER SUPPLY INPUT)` | 1 `20V`; 2 `20V`; 3 `PWR GND`; 4 `KEY` (marked `x`); 5 `PWR GND` |
| `J1` | `(HALL EFFECT SENSE INPUT)` | 1 `+5V`; 2 `SENSE`; 3 `KEY` (marked `x`); 4 `GND` |
| `J3` | `(FROM MASTER BOARD J3)` | 26-pin dual row, left column `1 3 5 ... 25`, right column `2 4 6 ... 26` |

(`J5` pin labels are printed `SOL B1` `SOL B2` `SOL A1` `SOL A2` with a space; the title of the page is `Motor Driver Slave Board Schematic`.)

`J3` as drawn: odd pins `1 3 5 7 9 11 13 15 17` strapped to a ground symbol (pin `25` also to ground); even pins `2 4 6 8 10 12 14 16` carry `D0` to `D7` (each `D` overlined); pin `18` `DRV_DISABLE_B`; pin `20` `DRV_DISABLE_A`; pins `19`, `21`, `22`, `23` each marked with an `x` (no connection, no label); pins `24` and `26` strapped together and to the `+12V` supply line that feeds `U4` and the LED.

Solenoid drive section (values as printed, roles traced):

| Part | Printed value | Role |
| --- | --- | --- |
| `Q3` | `TIP102` | `SOL B1` (`J5-1`); `D2` `1N4004` to `+20V` |
| `Q5` | `TIP102` | `SOL B2` (`J5-2`); `D4` `1N4004` |
| `Q4` | `TIP102` | `SOL A1` (`J5-3`); `D3` `1N4004` |
| `Q6` | `TIP102` | `SOL A2` (`J5-4`); `D5` `1N4004` |
| `R32`, `R33`, `R34`, `R35` | `220` | base resistors of `Q3`, `Q5`, `Q4`, `Q6` |
| `C16`, `C15`, `C13`, `C14` | `4.7/10` | base-to-ground capacitors (`+` marked) |
| `R39`, `R41`, `R40`, `R42` | `.51` `5W` (`R39`, `R41`); `51` `5W` (`R40`, `R42`) as printed | emitter resistors of `Q3`, `Q5`, `Q4`, `Q6`, to a supply-return triangle symbol |
| `R46` | `20.0K` | from the `Q3` emitter node to the `BIAS`-side feedback line (left) |
| `R47` | `20.0K` | from the `Q4` emitter node to the feedback line |
| `JP1` | `(See Note 4)` | jumper (two small circles) between the `Q3` emitter-resistor return and a ground symbol |

(No page of the amendment in this range prints the text of `Note 4`. The `R39` value reads `.51 5W` and the `R40`, `R42` values read `51 5W` on the scan; both readings are as printed.)

- `DRIVE B` (printed `DRIVE B` beside `R51`): the op-amp is printed `U1B` `LM324` on the scan although its pins are `12` `13` `14` (a `U1D` position; see uncertain readings) (`+` pin 12 via `R51` `6.0K` from `BIAS`; `-` pin 13; output pin 14), output through `R30` `100` to the base resistors `R32` and `R33`; feedback from the output through `R26` `20.0K` and `C17` `.1` in series back to pin 13. `R27` `10.0K` joins the `U1C` output (pin 8) to its `-` input node (pin 13).
- `DRIVE A`: `U3D` `LM324` (`+` pin 12 via `R55` `6.0K` from `BIAS`; `-` pin 13; output pin 14), output through `R44` `100` to the base resistors `R34` and `R35`; feedback `R38` `20.0K` and `C18` `.1` in series. `R43` `10.0K` joins the `U3A` output to the `U3D` `-` input node.
- `Q1` `2N3904` with `R36` `1K` at its base from the `DRV_DISABLE_B` line, collector to the `DRIVE B` base line, emitter to ground; `Q2` `2N3904` with `R37` `1K` at its base from the `DRV_DISABLE_A` line, collector to the `DRIVE A` base line, emitter to ground (traced).
- `U1C` `LM324` (`-` pin 9, `+` pin 10 via `R52` `10K` from `V/2_REF`, output pin 8) with `R25` `47K` and `C4` `.001` in its feedback (printed `.001`, the exponent is blurred; see uncertain readings).
- `U1A` `LM324` (`+` pin 3 via `R56` `10K` from `V/2_REF`, `-` pin 2, output pin 1, `+5V` pin 4 with `C2` `.1`): `R1` `10K` at the `-` side, feedback `R2` `120K` in parallel with `C19` `.01`; input filter capacitors `C20` `.01`, `C21` `.01` and `C22` `.1` from the hall `SENSE` line (`J1` pin 2) side (traced).
- `U3A` `LM324` (`+` pin 3 via `R54` `4.7K` from `V/2_REF`, `-` pin 2, output pin 1, `+5V` pin 4 with `C11` `.1`): `R28` `10.0K` at the `-` input, feedback `R29` `10.0K` (as printed).
- `U1B` `LM324` near the DAC (pin 7 output, `+` pin 5 from the `VREF` node, `-` pin 6): `R4` `10.0K` from its output back to the `-` node, `R3` `10.0K` from the `-` node down; its output goes through `R24` `12K` to the `U1C` `-` input (pin 9) and through `R53` `1.2K` and `C3` `1/50` to the `U1C` feedback node (traced); `C23` `.01` from the `VREF` node to ground.

Reference and bias buffers (new on this board):

- `BIAS`: `+5V` through `R31` `3.32K` to the `+` input (pin 10) of `U3C` `LM324` (printed beside it `BIAS` output at pin 8); `R48` `1.6?K` (digit blurred) from that node to ground; `D6` `1N4148` from `+5V` across to the node; `C12` `10/35` (`+`) to ground; `R49` `1K` feedback from the output (pin 8) to the `-` input (pin 9).
- `V/2_REF`: `+5V` through `R5` `10.0K` to the `+` input (pin 5) of `U3B` `LM324` (output pin 7, printed `V/2_REF`); `R6` `10.0K` from that node to ground; `D7` `1N4148` across; `C1` `10/35` (`+`) to ground; `R50` `4.7K` feedback from the output (pin 7) to the `-` input (pin 6).

DAC section: `U2` `AD7524`, legend as printed on the symbol: `14` `VDD`, `13` `WR`, `12` `CS`, `11` `D0`, `10` `D1`, `9` `D2`, `8` `D3`, `7` `D4`, `6` `D5`, `5` `D6`, `4` `D7` on the left; `1` `OUT1`, `2` `OUT2`, `15` `VREF`, `16` `VREFB` (printed `VREF 9` with a stub `X`), `3` `GND` on the right; `VDD` to `+12V` with `C6` `.1`; `OUT1` to `+5V` (with `C5` `.1`); `OUT2` and `GND` to ground; `WR` and `CS` tied to ground (small circles on the pins); data lines `D0` to `D7` each pulled up through the resistor group `R10` to `R17` (each printed `10K`) to `+12V`; `R18` `10K` and `R19` `10K` pull the `DRV_DISABLE_B` and `DRV_DISABLE_A` lines up to `+12V`. `VREF` through `R9` `10.0K` to a node with `R8` `20.0K` (to `+5V`) and `R7` `20.0K` (to ground) and `C23` `.01`, then to the `U1B` `+` input (pin 5).

Supply and indicator: `U4` `LM7805` (pins printed `VI`, `GND`, `VO`) from `+12V` with `C7` `100/35` (`+`) and `C8` `.1` on the input and `C10` `100/35` (`+`) and `C9` `.1` on the output; `LED1` with `R45` `2K` from the `+12V` line to ground. Hall input: `J1` pin 1 `+5V` to its supply flag, pin 4 `GND`; capacitors `C22` `.1`, `C20` `.01`, `C21` `.01` as printed beside the connector.

Differences from m-138 (A-18533), as printed: `J3` pins 19, 21, 22 and 23 marked `x` (the four `LED` lines and their `820` resistors are not on this schematic); `J2` (LED outputs) does not appear; `J1` carries input capacitors `C20` `C21` `C22`; the `R1`/`R2` network is `10K` and `120K` with `C19` `.01`; each solenoid transistor has an extra `20.0K` resistor (`R46`, `R47`) and a `JP1` jumper (`See Note 4`); `BIAS` and `V/2_REF` are buffered by `U3C` and `U3B` with `1N4148` diodes `D6` and `D7`; the emitter resistors are `.51 5W` / `51 5W` instead of `0.5 5W`. Page number: `9`.

## a-11 - amendment 16-9890 page: drawing `A-19008  Engine Ramp Assembly`, text `Page 2-29  Engine Block`, assembly `A-19711  Hall Adjustment Assembly`, page number printed at the bottom `11`

Top drawing, heading `A-19008  Engine Ramp Assembly`: an exploded view of the engine ramp and engine block with circled item numbers (as printed, in no particular order): `1` `2` `3` `4` `5` `6` `7` `8` `9` `10` `11` `12` `13` `14` `15` `16` `17` `18` `19` `20` `21` `22` `23` `24` `25` `26` `27` `28` `29` `30` `31` `32` `33` `34` `35` `36` `37` `38` `39` (every number from `1` to `39` was seen at least once; they were not all read individually, see uncertain readings). Wire labels printed on the lower (engine block) view, on wire runs at the right, abbreviated and blurred: `BLK`, `GRY/BRN` (second word blurred, `[?]`), `GRY/YEL`, `ORG/BRN` (read, blurred `[?]`); each appears twice (an upper and a lower run). Cable plugs at the ends of cables carry leader numbers `20`, `23`, `25`, `18` and `22`.

Printed text under the drawing:

`Page 2-29   Engine Block`
`Items #7 and 14 were changed; item #15, 16, 17 and 18 were added.`

| Item | Part No. | Description |
| --- | --- | --- |
| `7.` | `4006-01003-06` | `MS #6-32 x 3/16"` |
| `14.` | `4006-09168-02` | `MS #6-32 x 1/8"` |
| `15.` | `H-19182` | `V8 Sw/Fl Cable` |
| `16.` | `23-6622` | `Double Sided Tape` |
| `17.` | `03-7655-4` | `Cable Clamp` |
| `18.` | `A-19711` | `Hall Adjustment Assembly (See assembly below)` |

Heading: `A-19711   Hall Adjustment Assembly`. Parts list, columns `Part No.`, `Designator`, `Description` (right side clipped by the scan):

| Part No. | Designator | Description |
| --- | --- | --- |
| `A-19706` | `-` | `Hall Offset Adjustmen` (cut off) |
| `5040-12808-00` | `C1` | `Cap., 10µFd, 35v Axia` (cut off) |
| `5043-08996-00` | `C2` | `Cap., 0.1M, 50v, ±20°` (cut off) |
| `5370-12960-00` | `U1` | `IC, LM324 N OPAM` (as printed) |
| `5791-13830-04` | `J1, J2` | `Connector, 4-pin` |
| `5014-10261-00` | `R7` | `Pot 10K, ¼w, ±20%` |
| `5010-08774-00` | `R3` | `Res., 22K, ¼w, 5%` |
| `5010-08991-00` | `R6` | `Res., 4.7K, ¼w, 5%` |
| `5010-10985-00` | `R1, R2` | `Res., 20K, ¼w, 5%` |
| `5013-14135-00` | `R4, R5,` (continued) `R8-R11` | `Res., 10K, ¼w, 5%` |
| `01-13609` | `-` | `Adjust Board Bracket` |
| `20-9811-1` | `-` | `Support Post` |
| `H-19707` | `-` | `Cable Assembly` |

Board drawing (left of the parts list): a rectangular board with four mounting holes, connector `J2` (four positions, left edge, with a vertical text strip beside it too blurred to read, `[?]`), connector `J1` (four positions, right edge, a similar strip, `[?]`), resistor blocks printed `R1` `R2` `R3` (upper left), `R4` `R5` `R6` (lower left), `R8` `R9` (upper right), `R10` `R11` (lower right), pot `R7` (round, top centre), `C1` (round, `+` marked), `U1` (IC), `C2`. Printed page number: `11`.

## a-12 - amendment 16-9890 page printed title `Hall Offset Asjust P.C.B. Schematic` `A-19706`, page number printed at the bottom `12`

(`Asjust` is printed so.) One schematic.

- Offset reference: `+5V` through `R1` `20K`, pot `R7` `10K` (wiper arrow), `R2` `20K` to ground; the wiper goes to a node with `C1` `10/35` (`+` marked) to ground and to the `+` input (pin `3`) of `U1A`.
- `U1A` `LM324`: `+` pin `3`, `-` pin `2`, output pin `1`, supply pin `4` (to `+5V`, with `C2` `.1` to ground), ground pin `11`; `R3` `22K` from the output back to pin 2. The output goes through `R6` `4.7K` (printed `4 7K`) to the line that rises to the `+` input (pin `5`) of `U1B`.
- Input connector `J2`, with the bracketed text `FROM HALL SENSOR` printed to its left and the pin legend printed to its right: pin `1` `5V` (to a `+5V` flag), pin `2` `SIGNAL`, pin `3` `n.c.` (marked with an `x`), pin `4` `GND` (to ground). `SIGNAL` goes through `R4` `10.0K` to the `-` input (pin `6`) of `U1B`.
- `U1B` `LM324`: `+` pin `5`, `-` pin `6`, output pin `7`; feedback `R5` `10.0K` from the output to pin 6. The output goes through `R10` `10.0K` to the line that runs down to the `-` input (pin `9`) of `U1C` (traced).
- Mid-scale divider: `+5V` through `R9` `10.0K` to a node, `R8` `10.0K` from the node to ground; the node goes to the `+` input (pin `10`) of `U1C`.
- `U1C` `LM324`: `+` pin `10`, `-` pin `9`, output pin `8`; feedback `R11` `10.0K` from the output to pin 9. The output goes to `J1` pin `3` (`SIGNAL`).
- Output connector `J1`, pin legend printed to its right: pin `1` `5V` (to a `+5V` flag), pin `2` `n.c.` (marked with an `x`), pin `3` `SIGNAL`, pin `4` `GND` (to ground). A bracket follows with text clipped by the page edge, printed `TC` / `SLA` / `PC` (clipped, `[?]`).
- `U1D` `LM324` (unused section): `+` pin `12` to ground, `-` pin `13` tied to output pin `14`.

Printed page number: `12`.

## Uncertain readings

Every connector pin-list line (m-137, m-139, m-140 and a-08 parts lines) was read at 2x or more on a crop and is believed exact. The following are less certain; the crop file names are in `review-artifacts/corvette-1994/scratch/mechboards/`.

- m-137, the pin-to-wire fan-out of slave `J5` and the pairing of wire colours to the four engine coils in the block diagram were traced, not printed (`m137-pl.png`, `m137-pr.png`, `m137-w1.png`, `m137-w2.png`). The engine bottom-view wire-colour label order was read at small size.
- m-137, the master `J2` supply wires drawn to slave `J4` (`Red-White` `+20VDC`, `Black`) and the strapping of slave `J4` pins `2`/`1` and `5`/`3` were read at small size (`m137-w1.png`).
- m-138, which `U1`/`U3` op-amp section is which in the control section, the exact collector connections of `Q1` and `Q2`, and which `D0`-`D7` data lines attach to which `AD7524` pin were followed only partly (`q138-*.png`, `n138-*.png`). The suffix of `R37`/`R38` labels in the control area, and the unit/value strings `0.1, 5%`, `0.47 5%`, `12.1K 1%` were read at 2x (`q138-700-720.png`, `q138-1400-720.png`).
- m-138, the `J3` pin-to-label assignment of `19`, `21`, `22`, `23` (`LEDB2`, `LEDB1`, `LEDA1`, `LEDA2`) is traced; the m-139 master board prints `Y3` `LEDA1` to pin 22, `Y4` `LEDA2` to 23, `Y5` `LEDB1` to 21, `Y6` `LEDB2` to 19 on the same traced basis (`t139-c.png`, `t139-e.png`, `q138-0-720.png`).
- m-139, `J1` pin `5` (the line to `U1` `CLK`) and pins `7`, `1`, `2` (stubs) are drawn without printed labels; `DIS2` on pin `3` is the only clock-side label printed. Crop `t139-a.png`.
- m-139, the connection of `U2` `CLK` (pin 9) to `J1` pin 3 `DIS2` and `U2` `CLR` to the `U4` `Y7` / `R17` node are traced (`t139-b.png`, `t139-d.png`, `t139-g.png`).
- m-140 and m-141 were read from rotated 1.5x to 2x crops (`r141-a.png` to `r141-h.png`, `m140-pl.png`, `m140-pr.png`, `m140-w1.png`, `m140-w2.png`). The m-141 resistor numbers and values (`R2` to `R29`) and which of `Q1` to `Q10` sits in which half are lower confidence than the pin lists; the `JP1`/`JP2` designators and `R13`/`R27` `5.6` `5W` values were read at the limit of legibility. The page's `SEE NOTE 1` blocks have no note text printed on the page.
- m-141, the pairing of `J1` pins `8`/`7`, `6`/`5`, `4`/`3`, `2`/`1` with `DIR_1`, `DIR_2`, `ENABLE_1`, `ENABLE_2` is as drawn; whether the two pins of each pair are strapped on the board or are two connector positions for one signal is not stated.
- a-08, the last line of the A-19625 parts list `Mach. Screw, 4-40 x 3/8` and the `Cap., 0.1µFd ... Ax` line are clipped by the page edge; the circled item numbers `2` and `3` beside `01-10756` and `07-6688-18N` are partly cut by the column edge (`a08-r2.png`, `a08-l1.png`). The placement drawing silkscreen is unreadable.
- a-09, this schematic is low-contrast print. Values read with some doubt: `R48` `1.6?K` (`1.62K` is the parts list value for `R48`), `R39` `.51`/`R40` `51` (parts list says `0.51W` for `R39` to `R42`), `C4` `.001` vs the parts list `1KP`, `C3` `1/50` vs `1µFd 50v`, `R53` `1.2K`, `R31` `3.32K`, `R49` `1K`, `R50` `4.7K`, `R51` and `R55` `6.0K` vs parts list `6.8KW` (`q09-1-0.png`, `q09-2-0.png`, `q09-2-1.png`). The op-amp labelled `U1B` next to `DRIVE B` has pins `12` `13` `14` (a `U1D` position) on the scan; both the printed label and the pin numbers are given in the transcription. The `x` marks on `J3` pins 19, 21, 22, 23 were read at 2x (`q09-0-0.png`).
- a-11, the exact wire labels on the engine block drawing (`GRY/BRN`, `ORG/BRN`) are blurred (`a11-top2.png`, `a11-lab2.png`); not every circled item number on the exploded view was read individually; the strip of text beside `J1` and `J2` on the A-19711 board drawing is unreadable (`a11-board.png`); the parts list is clipped at the right edge (`a11-parts.png`).
- a-12, the clipped bracket text beside `J1` (`TC` / `SLA` / `PC`) is cut by the page edge (`a12-c.png`); the route of the `U1B` output through `R10` to `U1C` pin 9 is traced (`a12-b.png`).
