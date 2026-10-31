# Williams The Flintstones (1994) — Flipper circuits

Source: Williams *The Flintstones* Operations Manual 16-50029-101 (July 1994), IPDB machine 888 file
`Williams_1994_The_Flintstones_English_Manual.pdf`. Read from the native 300 dpi renders; each section
names its page. Text is transcribed as printed; `[?]` marks a reading the scan leaves uncertain.

## FLIPPER CIRCUITS, PDF page 125 (printed page 3-11)

Williams Electronics Games, Operations Manual 16-50029-101 (July 1994), "The Flintstones", PDF page 125, printed page 3-11. Title: "FLIPPER CIRCUITS". The page is one wiring diagram around the vertical block labelled `FLIPTRONIC II BOARD`, with the `CPU BOARD` (connector J202) and the `POWER DRIVER BOARD` (connectors J114, J105, J116) below it and the `FLIPPER OPTO BOARDS` at the right. There is no table; the diagram is transcribed per connector, then per flipper.

### Connector J907 (top of the Fliptronic II board)

Four pins, printed left to right in one box: `4 8 1 6`. Each pin has a +50VDC wire leaving the board and running to one flipper coil (traced from the diagram):

| J907 pin | Wire label as printed | Goes to (traced) |
| --- | --- | --- |
| 4 | Red-Blue +50VDC | Lower Left Flipper Coil |
| 8 | Red-Gray +50VDC | Upper Left Flipper Coil |
| 1 | Red-Green +50VDC | Lower Right Flipper Coil |
| 6 | Red-Violet +50VDC | Upper Right Flipper Coil |

### Connector J906: "End-of-Stroke Switches"

Heading printed: `End-of-Stroke Switches`. J906 pins top to bottom: 5, 3, 4, 1, 6.

| J906 pin | Wire colour | Label | Switch |
| --- | --- | --- | --- |
| 5 | Black-Gray | U. Left Flipper | F7 |
| 3 | Black-Blue | L. Left Flipper | F3 |
| 4 | Black-Violet | U. Right Flipper | F5 |
| 1 | Black-Green | L. Right Flipper | F1 |
| 6 | Orange | Ground | (ground symbol at pin 6) |

F7, F3, F5 and F1 are each drawn as a switch symbol with a common return line; that common line runs off to the right edge of the group (not labelled further).

### Connector J902: coil drive wires (Fliptronic II board)

J902 pins top to bottom: 6, 4, 13, 11, 3, 1, 9, 7. Each pair is a Power and a Hold wire, with a transistor designator printed at the right end:

| J902 pin | Wire colour | Function | Transistor | Flipper coil it reaches |
| --- | --- | --- | --- | --- |
| 6 | Yellow-Violet | Power | Q2 | Upper Right Flipper Coil |
| 4 | Orange-Violet | Hold | Q7 | Upper Right Flipper Coil |
| 13 | Yellow-Green | Power | Q4 | Lower Right Flipper Coil |
| 11 | Orange-Green | Hold | Q11 | Lower Right Flipper Coil |
| 3 | Yellow-Gray | Power | Q1 | Upper Left Flipper Coil |
| 1 | Orange-Gray | Hold | Q5 | Upper Left Flipper Coil |
| 9 | Yellow-Blue | Power | Q3 | Lower Left Flipper Coil |
| 7 | Orange-Blue | Hold | Q9 | Lower Left Flipper Coil |

Four coil boxes printed (each a stepped box on the right): `Upper Right Flipper Coil`, `Lower Right Flipper Coil`, `Upper Left Flipper Coil`, `Lower Left Flipper Coil`. No coil part numbers are printed on this page.

### Connector J905: flipper cabinet buttons to "FLIPPER OPTO BOARDS"

J905 pins top to bottom: 5, 2, 3, 1, 6. The wires run to the box labelled `FLIPPER OPTO BOARDS` (right side).

| J905 pin | Wire colour | Label | Switch |
| --- | --- | --- | --- |
| 5 | Black-Blue | U. Left Flipper | F8 |
| 2 | Blue-Gray | L. Left Flipper | F4 |
| 3 | Blue-Violet | U. Right Flipper | F6 |
| 1 | Black-Yellow | L. Right Flipper | F2 |
| 6 | Orange | Ground | (ground symbol at pin 6) |

Also to the `FLIPPER OPTO BOARDS` box: `Gray-Yellow +12VDC`, running down the right side of the page to `J116` pin 2 on the Power Driver Board.

### Per flipper (grouped; all from the tables above)

- Lower Left flipper: +50VDC Red-Blue (J907-4); coil drive Power Yellow-Blue J902-9 Q3, Hold Orange-Blue J902-7 Q9; end-of-stroke switch F3 Black-Blue (J906-3); cabinet button (opto) F4 Blue-Gray (J905-2).
- Lower Right flipper: +50VDC Red-Green (J907-1); coil drive Power Yellow-Green J902-13 Q4, Hold Orange-Green J902-11 Q11; end-of-stroke switch F1 Black-Green (J906-1); cabinet button (opto) F2 Black-Yellow (J905-1).
- Upper Right flipper: +50VDC Red-Violet (J907-6); coil drive Power Yellow-Violet J902-6 Q2, Hold Orange-Violet J902-4 Q7; end-of-stroke switch F5 Black-Violet (J906-4); cabinet button (opto) F6 Blue-Violet (J905-3).
- Upper Left flipper: +50VDC Red-Gray (J907-8); coil drive Power Yellow-Gray J902-3 Q1, Hold Orange-Gray J902-1 Q5; end-of-stroke switch F7 Black-Gray (J906-5); cabinet button (opto) F8 Black-Blue (J905-5).

### Connector J901 (Fliptronic II board) to Power Driver Board J105

| J901 pin | Wire | Goes to |
| --- | --- | --- |
| 1 | White-Blue 50VAC | J105 pin 1 (traced) |
| 5 | White-Blue 50VAC | J105 pin 2 (traced) |

### Connector J904 (Fliptronic II board) to Power Driver Board J114

J904 pins top to bottom: 4, 5, 1, 2. A ground symbol (with a junction dot) is drawn to the left of pins 4 and 5.

| J904 pin | Wire | Goes to (traced) |
| --- | --- | --- |
| 4 | Black Ground | J114 pin 7 |
| 5 | Black Ground | J114 pin 5 |
| 1 | Gray +5V | J114 pins 3 and 4 (the two pins are tied together in the drawing) |
| 2 | Gray-Green +12VDC | J114 pins 1 and 2 (the two pins are tied together in the drawing) |

J114 is drawn with pins `1 2 3 4 5 7` (no pin 6 drawn); a ground symbol is attached at pin 7.

### Other connectors named

- `J903` on the Fliptronic II board is drawn as a ribbon cable to `J202` on the `CPU BOARD`.
- Power Driver Board connectors drawn: `J114` (pins 1 2 3 4 5 7), `J105` (pins 2 1), `J116` (pin 2).

Printed page number at the bottom: `3-11`

### Notes on apparent misprints

- Black-Blue appears as the wire colour of both the L. Left Flipper end-of-stroke switch F3 (J906 pin 3) and the U. Left Flipper cabinet button F8 (J905 pin 5), as printed.
- The `Fliptronic II` label spelling is printed as `FLIPTRONIC II BOARD` (rotated text).

### Uncertain readings

- The tracing of which +50VDC wire reaches which coil box (J907 table, last column) and of J904/J901 wires to J114/J105 pins is by following the drawn lines, not by printed text; the lines are clear but long [?].

## FLIPPER COIL CIRCUIT, PDF page 126 (printed page 3-12)

Williams Electronics Games, Operations Manual 16-50029-101 (July 1994), "The Flintstones", PDF page 126, printed page 3-12. Title: "FLIPPER COIL CIRCUIT" (the page also carries the sub-diagram "FLIPPER END-OF-STROKE SWITCH CIRCUIT" and two paragraphs of text). This page is schematics only; no tables and no coil part numbers are printed.

### LEFT FLIPPER CIRCUIT (box label `FLIPTRONIC II BOARD`, right part labelled `PLAYFIELD`)

- Connector `J901`: pins `1`, `2`, `3`, `5` feed a bridge rectifier `BR1`; ground symbol at the bridge's "-" side; capacitor `C2` on the bridge's "+" side.
- From the bridge "+" rail, two fuses: `F904` and `F902`.
- Connector label printed as `J90` (the last character is not visible; see uncertain readings), pins `4`, `5`, `8`, `9`:
  - `F904` feeds pins 4 and 5 (tied together); wire `Red-Blue` leaves to the playfield, to the coil labelled `Lower Left Flipper`.
  - `F902` feeds pin 8; pin 9 is tied to pin 8; wire `Red-Gray` leaves to the playfield, to the coil labelled `Upper Left Flipper`.
- Connector `J902` (left side), pins and wires as printed:

| J902 pin | Wire | Function printed |
| --- | --- | --- |
| 9 | Yellow-Blue | Power |
| 7 | Orange-Blue | Holding |
| 3 | Yellow-Gray | Power |
| 1 | Orange-Gray | Holding |

- Coil `Lower Left Flipper`: a two-winding coil symbol with a diode on each winding; the Red-Blue wire joins the coil's top, the Yellow-Blue (Power) wire reaches the first winding and the Orange-Blue (Holding) wire the second.
- Coil `Upper Left Flipper`: same arrangement; Red-Gray at the top, Yellow-Gray (Power) and Orange-Gray (Holding).
- Connector `J906` (bottom of the left circuit), pins `3`, `6`, `5`:
  - pin 3: `Black-Blue` to `Lower Left E.O.S. Switch` (printed "Lower Loft E.O.S. Switch", see misprints)
  - pin 6: `Orange` (ground symbol at pin 6), returned to both switches
  - pin 5: `Black-Gray` to `Upper Left E.O.S. Switch` (printed "Upper Loft E.O.S. Switch")
  - second `Orange` wire label beside each switch (the common return).

### RIGHT FLIPPER CIRCUIT (box label `FLIPTRONIC II BOARD`, right part labelled `PLAYFIELD`)

- Connector `J901`: pins `1`, `2` (tied together), `3`, `5` (tied together), feeding bridge `BR1` with capacitor `C2`; ground symbol at the bridge's "-" side.
- Fuses `F903` and `F901`.
- Connector `J907`, pins `1`, `2`, `6`, `7`:
  - `F903` feeds pins 1 and 2 (tied together); wire `Red-Green` leaves to the playfield, to the upper of the two coil symbols (this coil has no text label on the page).
  - `F901` feeds pin 6; pin 7 is tied to pin 6; wire `Red-Violet` leaves to the playfield, to the coil labelled `Upper Right Flipper`.
- Connector `J902` (left side), pins and wires as printed:

| J902 pin (as printed) | Wire | Function printed |
| --- | --- | --- |
| 9 | Yellow-Green | Power |
| 7 | Orange-Green | Holding |
| 3 | Yellow-Violet | Power |
| 1 | Orange-Violet | Holding |

- Coil symbols: the upper coil (fed by Red-Green; Yellow-Green Power and Orange-Green Holding) carries no label; the lower coil (fed by Red-Violet; Yellow-Violet Power and Orange-Violet Holding) is labelled `Upper Right Flipper`. Each coil is drawn with two windings and a diode on each.
- Connector `J906` (bottom of the right circuit), pins `1`, `6`, `4`:
  - pin 1: `Black-Green` to `Lower Right E.O.S. Switch`
  - pin 6: `Orange` (ground symbol at pin 6), common return
  - pin 4: `Black-Violet` to `Upper Right E.O.S. Switch`

### FLIPPER END-OF-STROKE SWITCH CIRCUIT (first sub-diagram)

Legend printed at the left:
- `F1  Lower Right Flipper`
- `F5  Upper Right Flipper`
- `F3  Lower Left Flipper`
- `F7  Upper Right Flipper`

Box `FLIPTRONIC II BOARD`, connector `J906`:

| J906 pin | Wire | Chip pin | Switch |
| --- | --- | --- | --- |
| 1 | Black-Green | (U4A-5) | F1 |
| 4 | Black-Violet | (U6A-5) | F5 |
| 3 | Black-Blue | (U4C-9) | F3 |
| 5 | Black-Gray | (U6C-9) | F7 |
| 6 | Orange | (blank) | common return of the four switches (ground symbol at pin 6) |

The four switches F1, F5, F3, F7 are drawn as open contacts with their right-hand sides joined together to the Orange line.

### Dedicated-input circuit (second sub-diagram)

Box label `FLIPTRONIC II BOARD`, with `+5V` and `+12V` supply labels; label `Dedicated Input`.
Parts printed: `HCT244` (box), `10KΩ` (resistor to +5V), `LM339` comparator (points marked `A` and `B`), `1KΩ` (resistor to +12V), `1N4004` (diode), connector `J906` (pins `X` and `6`), `PLAYFIELD` switch on wire `Black-XXX`, return wire `Orange` to pin 6 (ground symbol).

Truth table printed at right:

| SWITCH | A | B | |
| --- | --- | --- | --- |
| OPEN | H | H | OFF |
| CLOSED | L | L | ON |

### Text at the bottom (as printed)

"The flipper E.O.S. circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground through the switch."

"When a switch closes, the row side, (dedicated input), of the circuit actives. The "+" input of the LM339 drops below +5V therefore its output is low. Since the row (dedicated input), circuit is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row (dedicated input) is inactive."

Printed page number at the bottom: `3-12`

### Notes on apparent misprints

- The legend lists `F7  Upper Right Flipper`, while the same diagram's F7 wire (`Black-Gray`) is the left upper flipper's switch in the left circuit on the same page and `U. Left Flipper F7` on the preceding page (3-11). Printed as is.
- The right flipper circuit repeats the J902 pin numbers `9, 7, 3, 1` of the left circuit, whereas page 3-11 lists J902 pins 13, 11, 6, 4 for the right-hand coils; printed as is.
- The right flipper circuit's J907 pins (1, 2, 6, 7) differ from the J907 pins listed on 3-11 (4, 8, 1, 6) for the left-hand wires (the left circuit here shows a `J90`[?] connector with pins 4, 5, 8, 9).
- `Lower Loft` / `Upper Loft` appear in the left circuit where "Left" is meant (scan reads "Loft"); transcribed as printed.

### Uncertain readings

- Connector label on the left circuit reads `J90` followed by nothing visible; likely cut off [?].
- Chip pin designators `(U6C-9)` for F7 and `(U6A-5)` for F5: the "6" and "C"/"A" are slightly blurred [?].
- `Orange-Blue` on J902 pin 7 of the left circuit is printed as `Orange-Bluc` in the scan; read as Orange-Blue.

## FLIPPER CABINET SWITCH CIRCUIT, PDF page 127 (printed page 3-13)

Williams Electronics Games, Operations Manual 16-50029-101 (July 1994), "The Flintstones", PDF page 127, printed page 3-13. Title: "FLIPPER CABINET SWITCH CIRCUIT". Three schematics and two paragraphs of text; no tables other than a small truth table.

### 1. Opto board harness (top diagram)

Boxes: `LEFT FLIPPER OPTO BOARD` (connector `J1`, pins printed top to bottom `6 7 3 4 1 2`, with a jumper loop joining 6-7 and another joining 3-4 on the board side), `RIGHT FLIPPER OPTO BOARD` (connector `J1`, pins `6 7 3 4 1 2`, same two jumper loops), `POWER DRIVER BOARD` (connector `J116`, pin `2`), `FLIPTRONIC II BOARD` (connector `J905`, pins `6`, `2`, `5`, `1`, `3`).

Each opto board's J1 mates with a harness connector with pins printed `6 7 3 4 1 2` (top to bottom).

Printed wire labels (between the left harness connector and the Fliptronic II / Power Driver boards):

| Wire colour | Label | Left-opto harness pin | Goes to |
| --- | --- | --- | --- |
| Gray-Yellow | +12V | 6 | Power Driver Board J116 pin 2 |
| Orange | Ground | 3 | Fliptronic II J905 pin 6 |
| Blue-Gray | L. Left Flipper F4 | 1 | Fliptronic II J905 pin 2 |
| Black-Blue | U. Left Flipper F8 | 2 | Fliptronic II J905 pin 5 |
| Black-Yellow | L. Right Flipper F2 | right-opto harness pin 1 | Fliptronic II J905 pin 1 |
| Blue-Violet | U. Right Flipper F6 | right-opto harness pin 2 | Fliptronic II J905 pin 3 |

The right opto board's harness is linked to the left opto board's harness by two unlabelled wires drawn from the left harness pins 7 and 4 to the right harness pins 6 and 3 respectively (traced from the drawing; these carry the +12V and ground to the right board).

### 2. Fliptronic II J905 to FLIPPER OPTO BOARDS (middle diagram)

Box `FLIPTRONIC II BOARD`, connector `J905` pins top to bottom: 1, 3, 2, 5, 6. Chip pin references printed at the left of each pin:

| J905 pin | Chip pin | Wire | Switch |
| --- | --- | --- | --- |
| 1 | (U4B-7) | Black-Yellow | F2 |
| 3 | (U6B-7) | Blue-Violet | F6 |
| 2 | U4D-11) | Blue-Gray | F4 |
| 5 | (U6D-11) | Black-Blue | F8 |
| 6 | (blank) | Orange (ground symbol at pin 6) | common return |

Legend printed at the left:
- `F2  Lower Right Flipper`
- `F6  Upper Right Flipper`
- `F4  Lower Left Flipper`
- `F8  Upper Left Flipper`

Box `FLIPPER OPTO BOARDS` shows four opto-coupler symbols (phototransistor plus LED), each with a series resistor to a `+12V` line (labelled at the right).

### 3. Dedicated-input circuit with one opto board (bottom diagram)

Box `FLIPTRONIC II BOARD`: `HCT244`, `10KΩ` to `+5V`, `LM339` comparator (points `A` and `B`), `1KΩ` to `+12V`, `1N4004` diode, label `Dedicated Input`, connector `J905` (pins `X` and `6`; ground symbol at pin 6). Wires `Blue-XXX` and `Black-XXX` (both printed, stacked) on pin X, `Orange` on pin 6.
Box `FLIPPER OPTO BOARD`: connector pins `X`, `3`, `6`; opto-coupler; resistor `470Ω` on the +12V side. Pin 3 connects to the Orange line, pin 6 to `Gray-Yellow` from `POWER DRIVER BOARD` connector `J116` pin `2` (`+12V`).

Truth table printed at the top right:

| SWITCH | A | B | |
| --- | --- | --- | --- |
| OPEN | H | H | OFF |
| CLOSED | L | L | ON |

### Text at the bottom (as printed)

"The flipper switch circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground through the switch circuit."

"When a switch closes, the row side, (dedicated input), of the circuit actives. The "+" input to the LM339 drops below +5V, therefore, its output is low. Since the row , (dedicated input), circuit is tied directly to ground through the switch, the switch is consisered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is high and the row, (dedicated input), is inactive."

Printed page number at the bottom: `3-13`

### Notes on apparent misprints

- `consisered` appears for "considered" in the closing paragraph; transcribed as printed.
- The chip pin for J905 pin 2 is printed `U4D-11)` without its opening parenthesis.
- The wire pairs of this page match page 3-11 (Black-Blue F8, Blue-Gray F4, Blue-Violet F6, Black-Yellow F2, Orange ground, Gray-Yellow +12VDC).

### Uncertain readings

- The two inter-board wires between the left and right opto harnesses (left pins 7 and 4 to right pins 6 and 3) are traced from the drawing, not labelled [?].
- Pin numbers of the harness connectors (6 7 3 4 1 2) are read from small print; the assignment of Gray-Yellow to pin 6 and Orange to pin 3 on the left harness is traced [?].
