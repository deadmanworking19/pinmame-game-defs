# Corvette (Bally, 1994) - Section 3 Boards: opto, flipper, trough and track boards (PDF pages 125-136, plus amendment 16-9890 pages a-07 and a-08)

Transcribed from the Corvette service manual scan (rendered at 300 dpi as `m-NNN.png`, NNN = PDF page) and from Amendment 16-9890 (rendered as `a-NN.png`). Each heading below is one PDF page and carries its printed title, assembly number and printed folio (read at the page bottom). Read from the rendered page, not from the OCR text.

| Source page | Printed folio | Printed title | Content transcribed |
| --- | --- | --- | --- |
| m-125 | 3-11 | LED P.C.B. Assembly (transmitter) A-16908; Photo Transistor P.C.B. Assembly (receiver) A-16909 | whole page (drawing labels) |
| m-126 | 3-12 | Flipper Opto P.C.B. Assembly A-17316 | whole page (pin lists, board drawing, schematic) |
| m-127 | 3-13 | Flipper Circuit Diagram | whole page (drawing labels and note) |
| m-128 | 3-14 | Flipper Coil Circuits; Flipper End-of-Stroke Switches | whole page (drawing labels and text) |
| m-129 | 3-15 | Flipper Cabinet Switch Circuit Diagram; Flipper Cabinet Switches | whole page (drawing labels and text) |
| m-130 | 3-16 | TROUGH 7 IRED PCB ASSEMBLY A-18617 | whole page (pin list, drawing labels) |
| m-131 | 3-17 | TROUGH 7 IR TSTR PCB ASSEMBLY A-18618 | whole page (pin list, drawing labels) |
| m-132 | 3-18 | Opto SW10 P.C.B. A-18159 | whole page (pin lists, board drawing) |
| m-133 | 3-19 | Opto SW10 schematic | whole page (drawing labels) |
| m-134 | 3-20 | Opto Track Limit P.C.B. A-18821 | whole page (pin list, drawing labels) |
| m-135 | 3-21 | Opto Track Encoder P.C.B. A-18822 | whole page (pin list, drawing labels) |
| a-07 | (no folio read, see its section) | CHANGE to Opto Track Encoder P.C.B. A-18822: Page 3-21 | whole page |
| m-136 | 3-22 | Engine Full-Stroke Opto P.C.B. A-18951 | whole page (pin list, drawing labels) |
| a-08 | (see its section) | Section 2 corrections, A-19606 Track Limit P.C.B. parts lines | the A-19606 lines only |

Conventions: spelling, capitalization, hyphenation and punctuation are as printed (including printed slips such as `Fliptronic Ii`). A line of printed text is given in a code span. Drawing labels are listed in the order printed. Wire routing that I followed by eye rather than read as a printed word is marked `(traced)`. `[?]` marks an unreadable character; see the final section.

## m-125 - printed titles `LED P.C.B. Assembly (transmitter)` `A-16908` and `Photo Transistor P.C.B. Assembly (receiver)` `A-16909`, folio `3-11`

Two stacked drawings, each with an assembly view, a side view and three small views (solder side, schematic, component side). No connector pin list is printed on this page.

Transmitter A-16908 (top drawing):

- Wire colour labels: `Green` (above the board, at the mounting hole), `Gray` (left wire), `Black` (right wire), `WHT` (above the side view).
- Board terminal labels: `A` (left terminal), `K` (right terminal), `SOLDER`.
- Small views: `solder side` shows terminals `A` `K`; `schematic` shows an LED symbol with `A` `K`; `component side` shows `K` `A` (mirror order).

Receiver A-16909 (bottom drawing):

- Wire colour labels: `Blue` (above the board), `White` (left wire), `Green` (right wire), `BLK` (above the side view).
- Board terminal labels: `C`, `E`, `SOLDER`.
- Small views: `solder side` shows `C` `E`; `schematic` shows a phototransistor symbol with `C` `E`; `component side` shows `E` `C` (mirror order).

Folio: `3-11`.

## m-126 - printed title `Flipper Opto P.C.B. Assembly` `A-17316`, folio `3-12`

Board drawing (rotated, J1 pin 1 at the top): `OPTO 1`, `OPTO 2`, `R1`, `R2`, connector `J1` with pins `1` to `7` and the legend beside the pins, top to bottom: `SW1`, `SW2`, `GND`, `GND`, `KEY`, `+12VDC`, `+12VDC`. The drawing also shows a slot/edge connector at the lower left with three vertical lines and a small `O` mounting-hole mark beside each opto.

Schematic (J1 pins listed top to bottom as drawn): `J1` `7` `+12VDC`; `6` `+12VDC`; `5` `KEY`; `1` `SW1`; `2` `SW2`; `3` `GND`; `4` `GND`. Components: `R1` `470Ω`, `R2` `470Ω`, `OPTO1`, `OPTO2` (each an LED facing a phototransistor). Both resistors run from the `+12VDC` rail to the LED anodes; the phototransistor collector of `OPTO1` goes to `SW1` (pin 1) and of `OPTO2` to `SW2` (pin 2); emitters and LED cathodes go to `GND` (traced).

Pin lists, two columns, headings underlined as printed:

`Left Side Flipper Cabinet Opto Switch Board`

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Black-Blue from Fliptronic II Board J905-2` |
| J1-2 | `J1-2 Blue-Gray from Fliptronic II Board J905-2` |
| J1-3 | `J1-3 Not Used` |
| J1-4 | `J1-4 Orange from Fliptronic II Board J905-6` |
| J1-5 | `J1-5 Not Used` |
| J1-6 | `J1-6 Gray-Yellow to Right Flipper Opto Board J1-6` |
| J1-7 | `J1-7 Gray Yellow from Fliptronic Ii Board J118-2` |

`Right Side Flipper Cabinet Opto Switch Board`

| Pin | Printed text |
| --- | --- |
| J2-1 | `J2-1 Black-Yellow from Fliptronic II Board J905-3` |
| J2-2 | `J2-2 Blue-Violet from Fliptronic II Board J905-1` |
| J2-3 | `J2-3 Orange from Fliptronic II Board J905-6` |
| J2-4 | `J2-4 Orange from Left Flipper Opto Board J1-4` |
| J2-5 | `J2-5 Not Used` |
| J2-6 | `J2-6 Gray-Yellow to Left Flipper Opto Board J1-6` |
| J2-7 | `J2-7 Not Used` |

Printed slips kept literally: both left J1-1 and J1-2 are printed `from Fliptronic II Board J905-2`; the right list is headed `J2-n` although the right board's connector is `J1` on the drawing; J1-7 is printed `Gray Yellow` (no hyphen) `Fliptronic Ii Board J118-2`. Folio: `3-12`.

## m-127 - printed title `Flipper Circuit Diagram`, folio `3-13`

Whole page is one block diagram: Fliptronic II Board (large box, label `FLIPTRONIC II BOARD`), `CPU BOARD` (small box lower left), `POWER DRIVER BOARD` (box lower right), the four flipper coils and `CABINET OPTO SWITCHES`.

Top, 50 VDC feeds, printed above the diagram, left to right, with connector `J907` (box printed `4 8 1 6`, label `J907` below):

| J907 pin (printed order) | Printed wire | Printed voltage | Goes to (traced) |
| --- | --- | --- | --- |
| 4 | `Red-Blue` | `+50VDC` | LOWER LEFT FLIPPER COIL (outermost line) |
| 8 | `Red-Gray` | `+50VDC` | UPPER LEFT FLIPPER COIL |
| 1 | `Red-Green` | `+50VDC` | LOWER RIGHT FLIPPER COIL |
| 6 | `Red-Violet` | `+50VDC` | UPPER RIGHT FLIPPER COIL (innermost line) |

End-of-stroke switches, heading `END-OF-STROKE SWITCHES`, connector `J906` (pin, wire, location, switch):

| J906 pin | Printed wire | Printed location | Switch |
| --- | --- | --- | --- |
| 5 | `Black-Gray` | `U. Left Flipper` | `F7*` |
| 3 | `Black-Blue` | `L. Left Flipper` | `F3` |
| 4 | `Black-Violet` | `U. Right Flipper` | `F5*` |
| 1 | `Black-Green` | `L. Right Flipper` | `F1` |
| 6 | `Orange` | `Ground` | (common, to ground symbol) |

Coil drive lines, connector `J902` (pin, wire, role, transistor, coil box):

| J902 pin | Printed wire | Role | Transistor | Coil box |
| --- | --- | --- | --- | --- |
| 6 | `Yellow-Violet` | `Power` | `Q2` | `UPPER* RIGHT FLIPPER COIL` |
| 4 | `Orange-Violet` | `Holding` | `Q7` | `UPPER* RIGHT FLIPPER COIL` |
| 13 | `Yellow-Green` | `Power` | `Q4` | `LOWER RIGHT FLIPPER COIL` |
| 11 | `Orange-Green` | `Holding` | `Q11` | `LOWER RIGHT FLIPPER COIL` |
| 3 | `Yellow-Gray` | `Power` | `Q1` | `UPPER* LEFT FLIPPER COIL` |
| 1 | `Orange-Gray` | `Holding` | `Q5` | `UPPER* LEFT FLIPPER COIL` |
| 9 | `Yellow-Blue` | `Power` | `Q3` | `LOWER LEFT FLIPPER COIL` |
| 7 | `Orange-Blue` | `Holding` | `Q9` | `LOWER LEFT FLIPPER COIL` |

Cabinet opto switches, connector `J905` (pin, wire, location, switch), going to the box `CABINET OPTO SWITCHES`:

| J905 pin | Printed wire | Printed location | Switch |
| --- | --- | --- | --- |
| 5 | `Black-Blue` | `U. Left Flipper` | `F8` |
| 2 | `Blue-Gray` | `L. Left Flipper` | `F4` |
| 3 | `Blue-Violet` | `U. Right Flipper` | `F6` |
| 1 | `Black-Yellow` | `L. Right Flipper` | `F2` |
| 6 | `Orange` | `Ground` | (to ground symbol) |

A further wire into the `CABINET OPTO SWITCHES` box is printed `Gray-Yellow` `+12V`; it runs down to Power Driver Board connector `J116` pin `2` (traced).

AC and low-voltage feeds from the Power Driver Board:

| Fliptronic pin | Printed wire | Printed function | Power Driver Board pin (traced) |
| --- | --- | --- | --- |
| `J901` 1 | `White-Blue` | `50VAC` | `J105` 1 |
| `J901` 5 | `White-Blue` | `50VAC` | `J105` 2 |
| `J904` 4 | `Black` | `Ground` | `J114` 7 |
| `J904` 5 | `Black` | `Ground` | `J114` 5 |
| `J904` 1 | `Gray` | `+5V` | `J114` 3 (also tied to `J114` 4) |
| `J904` 2 | `Gray-Green` | `+12V` | `J114` 1 (also tied to `J114` 2) |

Other labels: `J903` (on the Fliptronic II Board, five heavy parallel lines) connecting to `J202` on the `CPU BOARD`; Power Driver Board connectors drawn `J114` (pins `1 2 3 4 5 7`, pin 7 to ground symbol), `J105` (pins `2 1`), `J116` (pin `2`).

Footnote, bottom: `*NOTE: Used as circuits other than flipper circuits in this game.` Folio: `3-13`.

## m-128 - printed title `Flipper Coil Circuits` and `Flipper End-of-Stroke Switches`, folio `3-14`

Upper half, two circuits side by side, headings `Left Flipper Circuit` and `Right Flipper Circuit`, each in a dashed box `FLIPTRONIC II BOARD`.

Left Flipper Circuit labels: connector `J901` pins `1` `2` `3` `5` (1 tied to 2, 3 tied to 5), bridge `BR1`, capacitor `C2`, fuses `F904` and `F902`, connector `J907` pins `4` `5` `7` `8`, caption `Playfield`, wires `Red-Blue` (from J907 pin 5, after F904) to `Lower Left Flipper` coil and `Red-Gray` (from J907 pin 7, after F902) to `Upper Left Flipper` coil; pins 4 and 8 are strapped to 5 and 7 respectively (traced). Connector `J902`: pin `9` `Yellow-Blue` `Power`, pin `7` `Orange-Blue` `Holding` (these two to the Lower Left coil); pin `3` `Yellow-Gray` `Power`, pin `1` `Orange-Gray` `Holding` (to the Upper Left coil). Each coil is drawn with a power winding and a holding winding and a diode across each. Connector `J906`: pin `3` `Black-Blue` to `Lower Left End-of-Stroke Switch`; pin `6` ground symbol, `Orange` common to both switches; pin `5` `Black-Gray` to `Upper Left End-of-Stroke Switch`.

Right Flipper Circuit labels: `J901` pins `1` `2` `3` `5`, `BR1`, `C2`, fuses `F903` and `F901`, `J907` pins `1` `2` `6` `7`, `Playfield`, wires `Red--Green` (printed with a doubled dash; J907 pin 2, after F903) to `Lower Right Flipper` and `Red-Violet` (J907 pin 6, after F901) to `Upper Right Flipper`. `J902`: pin `13` `Yellow-Green` `Power`, pin `11` `Orange-Green` `Holding` (Lower Right coil); pin `6` `Yellow-Violet` `Power`, pin `4` `Orange-Violet` `Holding` (Upper Right coil). `J906`: pin `1` `Black-Green` to `Lower Right End-of-Stroke Switch`; pin `6` ground, `Orange`; pin `4` `Black-Violet` to `Upper Right End-of-Stroke Switch`.

Lower half, heading `Flipper End-of-Stroke Switches`. Legend, top to bottom: `F1 Lower Right Flipper`, `F5 Upper Right Flipper`, `F3 Lower Left Flipper`, `F7 Upper Left Flipper`. Box `FLIPTRONIC II BOARD`, connector `J906`:

| J906 pin | Printed wire (printed IC pin) | Switch |
| --- | --- | --- |
| 1 | `Black-Green` `(U4A-5)` | `F1` |
| 4 | `Black-Violet` `(U6A-5)` | `F5` |
| 3 | `Black-Blue` `(U4C-9)` | `F3` |
| 5 | `Black-Gray` `(U6C-9)` | `F7` |
| 6 | `Orange` | common (ground symbol) |

Generic circuit drawing (dashed box `FLIPTRONIC II BOARD`): `74HCT244` (box), `10K` pull-up to `+5V`, comparator `LM339` with input node `B` and output node `A`, `1K` to `+12v`, diode `1N4004`, connector `J906` pin `X` and pin `6`, wire `Black-xxx` to `End-of-Stroke Switch`, `Orange` to ground, caption `Dedicated Input`. Truth table as printed:

| Switch | A | B | (unlabelled column) |
| --- | --- | --- | --- |
| Open | H | H | Off |
| Closed | L | L | On |

Printed text, bottom, two paragraphs:

`The flipper switch circuits operate similar to the dedicated switch circuit. The circuits are active low and tied to ground through the switch.`

`When a switch closes the row side (dedicated input) of the circuit activates. The "+" input to the LM339 drops below +5V therefore its output is low. Since the row (dedicated input) circuit is tied directly to ground through the switch, the switch is considered closed by the microprocessor. When the switch opens, the "+" input to the LM339 is about +5V, its output is high and the row (dedicated input) is inactive.`

Folio: `3-14`.

## m-129 - printed title `Flipper Cabinet Switch Circuit Diagram` and `Flipper Cabinet Switches`, folio `3-15`

Upper diagram: `LEFT FLIPPER OPTO SWITCH BOARD` and `RIGHT FLIPPER OPTO SWITCH BOARD`, each with board connector `J1` (pins `6 7`, `3 4`, `1 2`, drawn with small jumper loops between 6-7 and 3-4, the 3-4 loop dashed), and a second column of cable-side pins `6 7 3 4 1 2` (left) and `6 7 3 4 1 2` (right). Other boxes: `POWER DRIVER BOARD` with connector `J116` pin `2`; `FLIPTRONIC II BOARD` with connector `J905` pins `6`, `2`, `5` (left group) and `1`, `3` (right group).

| Printed wire | Printed function | Ends (traced) |
| --- | --- | --- |
| `Gray-Yellow` `+12V` | | `J116` pin 2 to left cable pin 6 |
| `Orange` `Ground` (dashed line) | | left cable pin 3 to `J905` pin 6 |
| `Blue-Gray` `L. Left Flipper F4` | | left cable pin 1 to `J905` pin 2 |
| `Black-Blue` `U. Left Flipper F8` | | left cable pin 2 to `J905` pin 5 |
| `Black-Yellow` `L. Right Flipper F2` | | right cable pin 1 to `J905` pin 1 |
| `Blue-Violet` `U. Right Flipper F6` | | right cable pin 2 to `J905` pin 3 |

Daisy-chain lines between the two boards (traced): left cable pin 7 to right cable pin 6; left cable pin 4 to right cable pin 3 (dashed vertical).

Lower diagram, heading `Flipper Cabinet Switches`: legend top to bottom `F2 Lower Right Flipper`, `F6 Upper Right Flipper`, `F4 Lower Left Flipper`, `F8 Upper Left Flipper`. Box `FLIPTRONIC II BOARD`, connector `J905`; box `FLIPPER OPTO SWITCH BOARDS` containing four opto symbols each with a resistor to a `+12V` rail:

| J905 pin | Printed IC pin | Printed wire | Switch |
| --- | --- | --- | --- |
| 1 | `(U4B-7)` | `Black-Yellow` | `F2` |
| 3 | `(U6B-7)` | `Blue-Violet` | `F6` |
| 2 | `(U4D-11)` | `Blue-Gray` | `F4` |
| 5 | `(U6D-11)` | `Black-Blue` | `F8` |
| 6 | | `Orange` | ground symbol |

Single-circuit drawing: `FLIPTRONIC II BOARD` dashed box with `74HCT244`, `10K` to `+5V`, `LM339` (nodes `A` output, `B` input), `1K` to `+12V`, `1N4004`, caption `Dedicated Input`; connector `J905` pins `X` and `6`; wires `Blue-xxx` and `Black-xxx` (to `J1` pin `X`) and `Orange` (to `J1` pin `3`); dashed box `FLIPPER OPTO SWITCH BOARD` with `J1` pins `X`, `3`, `6`, caption `Cabinet Switch`, opto symbol, `470Ω` resistor; dashed box `POWER DRIVER BOARD` with `+12V`, connector `J116` pin `2`, wire `Gray-Yellow` to `J1` pin `6`. Table as on m-128:

| Switch | A | B | (unlabelled column) |
| --- | --- | --- | --- |
| Open | H | H | Off |
| Closed | L | L | On |

The same two-paragraph text as on m-128 is printed at the bottom (see m-128). Folio: `3-15`.

## m-130 - printed title `TROUGH 7 IRED PCB ASSEMBLY` `A-18617`, folio `3-16`

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Not Used` |
| J1-2 | `J1-2 Not Used` |
| J1-3 | `J1-3 Gray-Black, from Opto SW10 Board J1-4` |
| J1-4 | `J1-4 Gray-Orange, from Opto SW10 Board J1-5` |
| J1-5 | `J1-5 Gray-Red, from Opto SW10 Board J1-6` |
| J1-6 | `J1-6 Gray-Brown, from Opto SW10 Board J1-7` |
| J1-7 | `J1-7 Gray-Violet, from Opto SW10 Board J1-1` |
| J1-8 | `J1-8 Key` |
| J1-9 | `J1-9 Black, from Opto SW10 Board J1-9` |

Board drawing labels: `LED1` to `LED7` (seven semicircular LED outlines), four unlabelled round holes, connector `J1` drawn with pin `9` at the left end and pin `1` at the right end (a star mark at pin 8).

Schematic labels (each LED drawn as a diode with arrows, anode side to a J1 pin, cathodes joined to `COMMON`): `LED 7` `(BALL 6)`, `LED 6` `(BALL 5)`, `LED 5` `(BALL 4)`, `LED 4` `(BALL 3)`, `LED 3` `(BALL 2)`, `LED 2` `(BALL 1)`, `LED 1` `(JAM BALL)`. Connector `J1` legend by pin:

| J1 pin | Printed legend | LED (traced) |
| --- | --- | --- |
| 1 | `BALL 6` | LED 7 |
| 2 | `BALL 5` | LED 6 |
| 3 | `BALL 4` | LED 5 |
| 4 | `BALL 3` | LED 4 |
| 5 | `BALL 2` | LED 3 |
| 6 | `BALL 1` | LED 2 |
| 7 | `JAM BALL` | LED 1 |
| 8 | `KEY` | |
| 9 | `COMMON` | all LED cathodes |

Folio: `3-16`.

## m-131 - printed title `TROUGH 7 IR TSTR PCB ASSEMBLY` `A-18618`, folio `3-17`

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Yellow, from Opto SW10 Board J2-9` |
| J1-2 | `J1-2 Key` |
| J1-3 | `J1-3 Orange-Violet, from Opto SW10 Board J2-1` |
| J1-4 | `J1-4 Orange-Brown, from Opto SW10 Board J2-8` |
| J1-5 | `J1-5 Orange-Red, from Opto SW10 Board J2-7` |
| J1-6 | `J1-6 Orange-Black, from Opto SW10 Board J2-5` |
| J1-7 | `J1-7 Orange-Yellow, from Opto SW10 Board J2-4` |
| J1-8 | `J1-8 Not Used` |
| J1-9 | `J1-9 Not Used` |

Board drawing labels: `Q1` to `Q7` (seven round transistor outlines), four unlabelled round holes, connector `J1` with pin `9` at the left and pin `1` at the right (star mark near pin 2).

Schematic labels (phototransistors, collectors joined together to `COL`): `Q1` `(JAM BALL)`, `Q2` `(BALL 1)`, `Q3` `(BALL 2)`, `Q4` `(BALL 3)`, `Q5` `(BALL 4)`, `Q6` `(BALL 5)`, `Q7` `(BALL 6)`. Connector `J1` legend by pin:

| J1 pin | Printed legend | Transistor (traced) |
| --- | --- | --- |
| 1 | `COL` | all collectors |
| 2 | `KEY` | |
| 3 | `JAM BALL` | Q1 emitter |
| 4 | `BALL 1` | Q2 |
| 5 | `BALL 2` | Q3 |
| 6 | `BALL 3` | Q4 |
| 7 | `BALL 4` | Q5 |
| 8 | `BALL 5` | Q6 |
| 9 | `BALL 6` | Q7 |

Note that the schematic legend names `J1-8` `BALL 5` and `J1-9` `BALL 6`, while the pin list on the same page prints `J1-8 Not Used` and `J1-9 Not Used`; both are printed. Folio: `3-17`.

## m-132 - printed title `Opto SW10 P.C.B.` `A-18159`, folio `3-18`

Page title is two lines, `Opto SW10 P.C.B.` and `A-18159`. Top left, pin lists (printed as plain lines, in this order); top right, the board drawing; bottom, a wiring diagram.

Pin lists:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Violet to A-18617 J1-7 Sw #37` |
| J1-2 | `J1-2 Gray-Blue to LED Sw #36` |
| J1-3 | `J1-3 Gray-Green to LED Sw #35` |
| J1-4 | `J1-4 Gray-Black to A-18617 J1-3 Sw #34` |
| J1-5 | `J1-5 Gray-Orange to A-18617 J1-4 Sw #33` |
| J1-6 | `J1-6 Gray-Red to A-18617 J1-5 Sw #32` |
| J1-7 | `J1-7 Gray-Brown to A-18617 J1-6 Sw #31` |
| J1-8 | `J1-8 Key` |
| J1-9 | `J1-9 Black Ground to A-18617 J1-9` |
| J2-1 | `J2-1 Orange-Violet to A-18618 J1-3 Sw #37` |
| J2-2 | `J2-2 Orange-Blue to Photo Transistor Sw #36` |
| J2-3 | `J2-3 Orange-Green to Photo Transistor Sw #35` |
| J2-4 | `J2-4 Orange-Yellow to A-18618 J1-7 Sw #34` |
| J2-5 | `J2-5 Orange-Black to A-18618 J1-6 Sw #33` |
| J2-6 | `J2-6 Key` |
| J2-7 | `J2-7 Orange-Red to A-18618 J1-5 Sw #32` |
| J2-8 | `J2-8 Orange-Brown to A-18618 J1-4 Sw #31` |
| J2-9 | `J2-9 Gray-Yellow +12VDC to A-18618 J1-1` |
| J3-1 | `J3-1 Black Ground from J116-3` |
| J3-2 | `J3-2 Gray-Yellow +12VDC from J116-2` |
| J3-3 | `J3-3 Green-Yellow from J207-4` |
| J3-4 | `J3-4 Green-Orange from J207-3` |
| J3-5 | `J3-5 Key` |
| J3-6 | `J3-6 White-Violet from J209-8` |
| J3-7 | `J3-7 White-Blue from J209-7` |
| J3-8 | `J3-8 White-Green from J209-5` |
| J3-9 | `J3-9 White-Yellow from J209-4` |
| J3-10 | `J3-10 White-Orange from J209-3` |
| J3-11 | `J3-11 White-Red from J209-2` |
| J3-12 | `J3-12 White-Brown from J209-1` |
| J4-1 | `J4-1 Gray-Orange to LED Sw #43` |
| J4-2 | `J4-2 Not Used` |
| J4-3 | `J4-3 Not Used` |
| J4-4 | `J4-4 Key` |
| J4-5 | `J4-5 Orange-Black to Photo Transistor Sw #43` |
| J5-1 | `J5-1 Gray-Red to LED Sw #42` |
| J5-2 | `J5-2 Not Used` |
| J5-3 | `J5-3 Key` |
| J5-4 | `J5-4 Not Used` |
| J5-5 | `J5-5 Orange-Red to Photo Transistor Sw #42` |
| J6-1 | `J6-1 Gray-Brown to LED Sw #41` |
| J6-2 | `J6-2 Key` |
| J6-3 | `J6-3 Black Ground` |
| J6-4 | `J6-4 Gray-Yellow +12VDC` |
| J6-5 | `J6-5 Orange-Brown to Photo Transistor Sw #41` |

The J4, J5 and J6 lists are printed in the right-hand column (J5 and J6) and the left-hand column (J4); J3 is the block directly under J2.

Board drawing (top right): connectors `J1` (nine positions, drawn `9` at the top and `1` at the bottom, key mark at position 8), `J2` (nine positions, `9` at the top and `1` at the bottom, key mark at position 6), `J3` (twelve positions, drawn `12` at the left and `1` at the right, key mark at position 5), `J4`, `J5`, `J6` (five positions each, `1` at the top and `5` at the bottom; key marks at positions 4, 3 and 2 respectively).

Wiring diagram (bottom):

- Left: box `CPU BOARD` with connector `J207` (pins `4`, `3`), connector `J209` (pins `8` `5` `4` `3` `2` `1` `7`, top to bottom) and `J211` (ribbon) down to `POWER DRIVER BOARD` connector `J113`; Power Driver Board connector `J116` (pins `3` `2`).
- Printed wire labels from the CPU board, with the connector pin they leave and the `J3` pin they reach (the `J3` end followed by eye, `(traced)`):

| CPU board pin | Printed wire label | J3 pin (traced) |
| --- | --- | --- |
| `J207` 4 | `Green-Yellow Sw. Col. 4` | 3 |
| `J207` 3 | `Green-Orange Sw. Col. 3` | 4 |
| `J209` 8 | `White-Violet Sw. Row 7` | 6 |
| `J209` 5 | `White-Green Sw. Row 5` | 8 |
| `J209` 4 | `White-Yellow Sw. Row 4` | 9 |
| `J209` 3 | `White-Orange Sw. Row 3` | 10 |
| `J209` 2 | `White-Red Sw. Row 2` | 11 |
| `J209` 1 | `White-Brown Sw. Row 1` | 12 |
| `J209` 7 | `White-Blue Sw. Row 6` | 7 |
| `J116` 3 | `Black Ground` | 1 |
| `J116` 2 | `Gray-Yellow +12V` | 2 |

- Box `OPTO SW10 P.C.B.` `A-18159` with connectors `J3` (pins drawn top to bottom `3` `4` `6` `8` `9` `10` `11` `12` `7` `1` `2`; pin 5 not drawn), `J2` (pins drawn `1 2 3 4 5 7 8 9`; no pin 6 drawn), `J1` (pins drawn `1 2 3 4 5 6 7 9`; no pin 8 drawn), `J4` (pins `1` `5`), `J5` (pins `1` `5`), `J6` (pins `1` `3` `4` `5`).
- `J2` wires printed beside the pins (a `*` is printed above the brace that groups them, no footnote text for the `*` is printed on this page): pin 1 `Orange-Violet`, pin 2 `Orange-Blue`, pin 3 `Orange-Green`, pin 4 `Orange-Yellow`, pin 5 `Orange-Black`, pin 7 `Orange-Red`, pin 8 `Orange-Brown`, pin 9 `Gray-Yellow`. Pin 9 goes with the pin `E` side; all go up to the box `PLAYFIELD` > `Photo Transistor Board` (labels `C`, `E`; symbol of a phototransistor with the caption `Beam` and a dashed line to the LED).
- `J1` wires printed beside the pins (a `*` above the brace): pin 1 `Gray-Violet`, pin 2 `Gray-Blue`, pin 3 `Gray-Green`, pin 4 `Gray-Yellow`, pin 5 `Gray-Orange`, pin 6 `Gray-Red`, pin 7 `Gray-Brown`, pin 9 `Black`. They go up to box `PLAYFIELD` > `LED Board` (labels `K`, `A`). Note: the diagram prints `Gray-Yellow` at J1 pin 4 where the pin list prints `J1-4 Gray-Black`; both are printed.
- `J4`: two wires `Gray-Orange` and `Orange-Black`, labels beneath `(K)` `(C)`.
- `J5`: two wires `Gray-Red` and `Orange-Red`, labels beneath `(K)` `(C)`.
- `J6`: four wires, pin 1 `Gray-Brown`, pin 3 `Black`, pin 4 `Gray-Yellow`, pin 5 `Orange-Brown`, labels beneath `(K)` `(A)` `(E)` `(C)`.

Folio: `3-18`.

## m-133 - printed title `Opto SW10 P.C.B. Schematic`, folio `3-19`

The page title is `Opto SW10 P.C.B. Schematic` (no assembly number printed on this page). One schematic, connectors on the left (`J1`, `J2`, `J6`, `J5`, `J4`) and on the far right (`J3`).

`J1` (labelled `J1`, pins drawn `9` at the top to `1` at the bottom), each anode to `VCC` through a resistor printed `220 2W, 1/2W`:

| J1 pin | Printed label | Resistor |
| --- | --- | --- |
| 9 | `CATHODE` `GND` (to ground symbol) | |
| 8 | `KEY` | |
| 7 | `ANODE 1` | `R1` `220 2W, 1/2W` |
| 6 | `ANODE 2` | `R2` `220 2W, 1/2W` |
| 5 | `ANODE 3` | `R3` `220 2W, 1/2W` |
| 4 | `ANODE 4` | `R4` `220 2W, 1/2W` |
| 3 | `ANODE 5` | `R5` `220 2W, 1/2W` |
| 2 | `ANODE 6` | `R6` `220 2W, 1/2W` |
| 1 | `ANODE 7` | `R7` `220 2W, 1/2W` |

(R6 is printed `R6` on the anode-6 line on this drawing; a separate `R6` `2K` also appears on the OPTO 9 comparator input, see below. The two are printed as shown.)

`J2` (pins drawn top to bottom `9` `8` `7` `5` `4` `3` `2` `1` `6`; no pin 6 between 7 and 5):

| J2 pin | Printed label |
| --- | --- |
| 9 | `+12VDC` (to a `VCC` supply symbol) |
| 8 | `E1 OPTO 1` |
| 7 | `E2 OPTO 2` |
| 5 | `E3 OPTO 3` |
| 4 | `E4 OPTO 4` |
| 3 | `E5 OPTO 5` |
| 2 | `E6 OPTO 6` |
| 1 | `E7 OPTO 7` |
| 6 | `KEY` |

`J6` `OPTO 8`, `J5` `OPTO 9`, `J4` `OPTO 10` (heading printed beside each connector name):

| Connector | Pin | Printed label | Notes |
| --- | --- | --- | --- |
| `J6` `OPTO 8` | 1 | `A` | `R25` `220 2W, 1/2W` to `VCC` |
| | 2 | `NC` | |
| | 3 | `K` | to ground symbol |
| | 4 | `C` | to `VCC` |
| | 5 | `E8` | to the OPTO 8 comparator input |
| `J5` `OPTO 9` | 1 | `A` | `R28` `220 2W, 1/2W` to `VCC` |
| | 2 | `K` | to ground symbol |
| | 3 | `NC` | |
| | 4 | `C` | to `VCC` |
| | 5 | `E9` | to the OPTO 9 comparator input |
| `J4` `OPTO 10` | 1 | `A` | `R31` `220 2W, 1/2W` to `VCC` |
| | 2 | `K` | to ground symbol |
| | 3 | `C` | to `VCC` |
| | 4 | `NC` | |
| | 5 | `E10` | to the OPTO 10 comparator input |

Comparator stages (LM339 quad comparators `U1`, `U2`, `U3`; every input is a divider of two `2K` resistors, the series resistor from the `E` line and a shunt resistor to ground; the `+` inputs of all comparators are tied to one common bus). Followed by eye (`traced`):

| Input line | Series / shunt resistors | Comparator (output pin) | Output diode | Row line it reaches (traced) |
| --- | --- | --- | --- | --- |
| `E1 OPTO 1` | `R9` `2K` / `R8` `2K` | `U1D` (pin 13; `+` pin 11, `-` pin 10) | `D1` `IN4004` | `ROW 1` |
| `E2 OPTO 2` | `R11` `2K` / `R10` `2K` | `U1C` (pin 14; `+` 9, `-` 8) | `D2` `IN4004` | `ROW 2` |
| `E3 OPTO 3` | `R13` `2K` / `R12` `2K` | `U1B` (pin 2; `+` 5, `-` 4) | `D3` `IN4004` | `ROW 3` |
| `E4 OPTO 4` | `R15` `2K` / `R14` `2K` | `U1A` (pin 1; `+` 7, `-` 6; `VCC` pin 3, ground pins 1/2 as drawn) | `D4` `IN4004` | `ROW 4` |
| `E5 OPTO 5` | `R17` `2K` / `R16` `2K` | `U2D` (pin 13; `+` 11, `-` 10) | `D5` `IN4004` | `ROW 5` |
| `E6 OPTO 6` | `R19` `2K` / `R18` `2K` | `U2C` (pin 14; `+` 9, `-` 8) | `D6` `IN4004` | `ROW 6` |
| `E7 OPTO 7` | `R21` `2K` / `R20` `2K` | `U2B` (pin 2; `+` 5, `-` 4) | `D7` `IN4004` | `ROW 7` |
| `E8` (J6) | `R24` `2K` / `R23` `2K` | `U3C` (pin 14; `+` 9, `-` 8) | `D10` `IN4004` | `ROW 1` (stub printed `ROW 1` beside the lower row lines) |
| `E9` (J5) | `R27` `2K` / `R6` `2K` | `U3B` (pin 2; `+` 5, `-` 4) | `D11` `IN4004` | `ROW 2` (stub printed `ROW 2`) |
| `E10` (J4) | `R30` `2K` / `R29` `2K` | `U3A` (pin 1; `+` 7, `-` 6) | `D12` `IN4004` | `ROW 3` (stub printed `ROW 3`) |

Each comparator carries `VCC` and ground symbols, and the printed device label `LM339` beside it.

Reference and column circuits, bottom: `R32` `100K` from `VCC` and `R39` `100K` from `VCC` each to a node feeding a resistor printed `R` `22K` (unnumbered, to `U2A` output pin 1) and `R36` `22K` (to `U3D` output pin 13); `U2A` `LM339` (`+` pin 7, `-` pin 6, `VCC` pin 3) with `R37` `10K`; `U3D` `LM339` (`+` pin 11, `-` pin 10) with `R38` `10K`; `R33` `22K` to ground and `R35` `100K` to `VCC`. Output nodes: `R40` `100K` to `VCC` and diode `D8` `IN4004` labelled `COL. 1`; `R41` `100K` to `VCC` and diode `D9` `IN4004` labelled `COL. 2`.

Supply section: `+12VDC` through diode `D13` `IN4004` to the `VCC` node; `R22` `1.2K` to `LED 1` (to ground); `C1` `100UF` to ground.

`J3` (right edge, pins drawn top to bottom `12` to `1`):

| J3 pin | Printed label |
| --- | --- |
| 12 | `ROW 1` |
| 11 | `ROW 2` |
| 10 | `ROW 3` |
| 9 | `ROW 4` |
| 8 | `ROW 5` |
| 7 | `ROW 6` |
| 6 | `ROW 7` |
| 5 | `KEY` |
| 4 | `COL 1` |
| 3 | `COL 2` |
| 2 | `+12VDC` |
| 1 | `GND` |

Cross-reference printed on the previous page (m-132, for the reader): its pin list prints `J3-4 Green-Orange from J207-3` and `J3-3 Green-Yellow from J207-4`, with the wiring diagram labels `Sw. Col. 3` and `Sw. Col. 4`, while this schematic names those same `J3` pins `COL 1` (pin 4) and `COL 2` (pin 3). Both are printed; the page 3-18 row wires `Sw. Row 1` to `Sw. Row 7` run to `J3` pins 12 to 7 and 6 (`Row 6` to J3-7, `Row 7` to J3-6) as the `ROW n` labels here. Folio: `3-19`.

## m-134 - printed title `Opto Track Limit P.C.B. Assembly` `A-18821`, folio `3-20`

Board drawing (top): a plain rectangular outline with one connector `J1` (six positions, `6` at the left and `1` at the right, key mark at position 5). No other labels are printed on the board drawing.

Pin list:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 White-Brown from J209-1` |
| J1-2 | `J1-2 Green-Black from J207-5` |
| J1-3 | `J1-3 Black from J116-3` |
| J1-4 | `J1-4 Gray-Yellow +12VDC from J116-2` |
| J1-5 | `J1-5 Key` |
| J1-6 | `J1-6 White-Red from J209-2` |

Schematic (caption `Schematic`): two opto couplers drawn as an LED and a phototransistor inside a dashed box, `OPTO 1` and `OPTO 2`; resistors `R1` and `R2` (no values printed) feeding the LEDs from the `+12V` line; diodes `D1` and `D2` (no type printed) from each phototransistor emitter to a common line that goes to `COL`; the two LED cathodes and phototransistor path join the `GND` line. Connector `J1` as drawn (top to bottom):

| J1 pin | Printed label |
| --- | --- |
| 6 | `R1` |
| 5 | `KEY` |
| 4 | `+12V` |
| 3 | `GND` |
| 2 | `COL` |
| 1 | `R2` |

(The schematic labels pin 6 `R1` and pin 1 `R2`; the pin list above and the wiring diagram below feed pin 1 from `J209-1` / `Row 1` and pin 6 from `J209-2` / `Row 2`. Both are printed as shown.)

Wiring diagram (bottom): `CPU BOARD` with connector `J207` (pin `5`), connector `J209` (pins `1`, `2`) and `J211`, ribbon to `POWER DRIVER BOARD` connector `J113`; Power Driver Board connector `J116` (pins `3` `2`); box `OPTO TRACK LIMIT P.C.B.` `A-18821` with connector `J1` (pins drawn top to bottom `2` `1` `6` `3` `4`).

| From | Printed wire label | To `J1` pin (traced) |
| --- | --- | --- |
| `J207` pin 5 | `Green-Black Sw. Col. 5` | 2 |
| `J209` pin 1 | `White-Brown Sw. Row 1` | 1 |
| `J209` pin 2 | `White-Red Sw. Row 2` | 6 |
| `J116` pin 3 | `Black Ground` | 3 |
| `J116` pin 2 | `Gray-Yellow +12V` | 4 |

Folio: `3-20`.

## m-135 - printed title `Opto Track Encoder P.C.B. Assembly` `A-18822`, folio `3-21`

Board drawing (top): a plain rectangular outline with connector `J1` (six positions, `1` at the left and `6` at the right, key mark at position 4, a ribbon of vertical lines above the connector). No other labels.

Pin list (original manual page):

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Yellow +12VDC from J116-2` |
| J1-2 | `J1-2 Black ground from J116-3` |
| J1-3 | `J1-3 Green-Black from J207-5` |
| J1-4 | `J1-4 Key` |
| J1-5 | `J1-5 White-Blue from J209-7` |
| J1-6 | `J1-6 White-Green from J209-5` |

Schematic (caption `Schematic`): two opto couplers `OPTO 1` and `OPTO 2` (LED and phototransistor in a dashed box); resistors `R1` and `R2` (no values printed) from the `+12V` line to the LED anodes; diodes `D1` and `D2` (no type printed) from each phototransistor emitter to a common line that goes to `COL`; collectors go to `R2` (OPTO 2) and `R1` (OPTO 1) (traced). Connector `J1` as drawn:

| J1 pin | Printed label |
| --- | --- |
| 1 | `+12V` |
| 2 | `GND` |
| 3 | `COL` |
| 4 | `KEY` |
| 5 | `R2` |
| 6 | `R1` |

Wiring diagram (bottom): `CPU BOARD` with connector `J207` (pin `5`), connector `J209` (pins `5`, `7`) and `J211` with ribbon to `POWER DRIVER BOARD` connector `J113`; Power Driver Board connector `J116` (pins `3` `2`); box `OPTO TRACK ENCODER P.C.B.` `A-18822` with connector `J1` (pins drawn top to bottom `3` `6` `5` `2` `1`).

| From | Printed wire label | To `J1` pin (traced) |
| --- | --- | --- |
| `J207` pin 5 | `Green-Black Sw. Col. 5` | 3 |
| `J209` pin 5 | `White-Green Sw. Row 5` | 6 |
| `J209` pin 7 | `White-Blue Sw. Row 6` | 5 |
| `J116` pin 3 | `Black Ground` | 2 |
| `J116` pin 2 | `Gray-Yellow +12V` | 1 |

Folio: `3-21`.

## a-07 - amendment 16-9890 page printed `CHANGE to Opto Track Encoder P.C.B. A-18822: Page 3-21`, page number printed at the bottom `7`

Printed heading (underlined): `CHANGE to Opto Track Encoder P.C.B. A-18822:  Page 3-21`. The page replaces the drawings and pin list of m-135 above. The printed page number at the bottom of the amendment page is `7`.

Board drawing (top): rectangular outline with two boxes `OPTO 1` and `OPTO 2` and connector `J1` (six positions, `1` at the left, `6` at the right, key mark at position 3). (The original m-135 board drawing has no `OPTO 1` / `OPTO 2` boxes and its key mark is at position 4.)

Pin list (amendment):

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 White-Brown from J209-1` |
| J1-2 | `J1-2 White-Red from J209-2` |
| J1-3 | `J1-3 Key` |
| J1-4 | `J1-4 Green-Violet from J207-7` |
| J1-5 | `J1-5 Black ground from J116-3` |
| J1-6 | `J1-6 Gray-Yellow +12VDC from J116-2` |

Schematic (caption `Schematic`), labels as printed:

- Resistors `R2` `680 1/2W` and `R1` `680 1/2W` (LED supply, from the `+12V` line to the LEDs), capacitor `C1` `0.1u` (the unit character is blurred in the scan; `[?]` for the unit sign) from the `+12V` line to ground.
- Opto couplers `OPTO1` and `OPTO2`, each printed `SHARP` `GP1A52HR`, with package pins numbered `1` `2` `3` `4` `5` (`1` at the LED anode, `2` and `3` to ground, `4` the output, `5` to the supply line, traced). Each drawn as an LED, a photo-detector with Schmitt trigger symbol and an output transistor.
- Output resistors `R3` `2.2K` (from `OPTO1` pin 4) and `R4` `2.2K` (from `OPTO2` pin 4), each into the base of a transistor printed `Q1` `2N3904` and `Q2` `2N3904`.
- Diodes `D1`, `D2` (on `Q1`: `D1` from the collector to the `R1` line, `D2` from the emitter to the common node) and `D3`, `D4` (on `Q2`: `D3` from the collector to the `R2` line, `D4` from the emitter to the common node); no diode type is printed. The common node goes to `COL` (traced).
- Connector `J1`, pin legend as printed beside the pins: `1` `R1`; `2` `R2`; `3` `KEY`; `4` `COL`; `5` `GND`; `6` `+12V`. (A `J` designator above the connector is cut off at the page edge.)

Wiring diagram (bottom): `CPU BOARD` with connector `J207` (pin `7`), connector `J209` (pins `1`, `2`) and `J211` with ribbon to `POWER DRIVER BOARD` connector `J113`; Power Driver Board connector `J116` (pins `3` `2`); box `OPTO TRACK ENCODER P.C.B.` `A-18822` with connector `J1` (pins drawn top to bottom `4` `1` `2` `5` `6`).

| From | Printed wire label | To `J1` pin (traced) |
| --- | --- | --- |
| `J207` pin 7 | `Green-Violet Sw. Col. 7` | 4 |
| `J209` pin 1 | `White-Brown Sw. Row 1` | 1 |
| `J209` pin 2 | `White-Red Sw. Row 2` | 2 |
| `J116` pin 3 | `Black Ground` | 5 |
| `J116` pin 2 | `Gray-Yellow +12V` | 6 |

Differences from the original m-135 (3-21), all as printed:

| Item | Original m-135 (3-21) | Amendment a-07 |
| --- | --- | --- |
| J1-1 | `Gray-Yellow +12VDC from J116-2` | `White-Brown from J209-1` |
| J1-2 | `Black ground from J116-3` | `White-Red from J209-2` |
| J1-3 | `Green-Black from J207-5` | `Key` |
| J1-4 | `Key` | `Green-Violet from J207-7` |
| J1-5 | `White-Blue from J209-7` | `Black ground from J116-3` |
| J1-6 | `White-Green from J209-5` | `Gray-Yellow +12VDC from J116-2` |
| Switch matrix column wire | `Green-Black Sw. Col. 5` (`J207` pin 5) | `Green-Violet Sw. Col. 7` (`J207` pin 7) |
| Switch matrix row wires | `White-Green Sw. Row 5` (`J209` pin 5), `White-Blue Sw. Row 6` (`J209` pin 7) | `White-Brown Sw. Row 1` (`J209` pin 1), `White-Red Sw. Row 2` (`J209` pin 2) |
| Schematic pins | `1` `+12V`, `2` `GND`, `3` `COL`, `4` `KEY`, `5` `R2`, `6` `R1` | `1` `R1`, `2` `R2`, `3` `KEY`, `4` `COL`, `5` `GND`, `6` `+12V` |
| Schematic parts | `R1`, `R2`, `D1`, `D2`, two bare opto couplers (no values) | `R1` `R2` `680 1/2W`, `R3` `R4` `2.2K`, `C1` `0.1u`, `Q1` `Q2` `2N3904`, `D1` to `D4`, `SHARP GP1A52HR` opto ICs |
| Board drawing | no opto boxes, key mark at position 4 | `OPTO 1` / `OPTO 2` boxes, key mark at position 3 |

## m-136 - printed title `Engine Full-Stroke Opto P.C.B. Assembly` `A-18951`, folio `3-22`

Board drawing (top): rectangular outline with two vertical boxes labelled `OPTO1` (left) and `OPTO2` (right), and connector `J1` (six positions, `6` at the left and `1` at the right, key mark at position 3).

Pin list:

| Pin | Printed text |
| --- | --- |
| J1-1 | `J1-1 Gray-Yellow +12VDC from J116-2` |
| J1-2 | `J1-2 Black ground from J116-3` |
| J1-3 | `J1-3 Key` |
| J1-4 | `J1-4 Green-Violet from J207-7` |
| J1-5 | `J1-5 White-Red from J209-2` |
| J1-6 | `J1-6 White-Brown from J209-1` |

Schematic (caption `Schematic`): `OPTO 1` and `OPTO 2` (LED and phototransistor in a dashed box each), `R1` and `R2` (no values printed) from the `+12V` line to the LED anodes, diodes `D1` and `D2` (no type printed) from each phototransistor emitter to a common line to `COL`; the collectors go to `R2` (OPTO 1, pin 6) and `R1` (OPTO 2, pin 5) (traced). Connector `J1` as drawn:

| J1 pin | Printed label |
| --- | --- |
| 1 | `+12V` |
| 2 | `GND` |
| 3 | `KEY` |
| 4 | `COL` |
| 5 | `R1` |
| 6 | `R2` |

Wiring diagram (bottom): `CPU BOARD` with connector `J207` (pin `7`), connector `J209` (pins `2`, `1`) and `J211` with ribbon to `POWER DRIVER BOARD` connector `J113`; Power Driver Board connector `J116` (pins `3` `2`); box `ENGINE FULL-STROKE OPTO P.C.B.` `A-18951` with connector `J1` (pins drawn top to bottom `4` `5` `6` `2` `1`).

| From | Printed wire label | To `J1` pin (traced) |
| --- | --- | --- |
| `J207` pin 7 | `Green-Violet Sw. Col. 7` | 4 |
| `J209` pin 2 | `White-Red Sw. Row 2` | 5 |
| `J209` pin 1 | `White-Brown Sw. Row 1` | 6 |
| `J116` pin 3 | `Black Ground` | 2 |
| `J116` pin 2 | `Gray-Yellow +12V` | 1 |

Folio: `3-22`.

## a-08 (A-19606 Opto Track Limit PCB lines only) - amendment 16-9890 page headed `SECTION 2` `Corrections/Changes`, page number printed at the bottom `8`

Only the A-19606 entry of this page is transcribed here (the A-19625 entry is in `motor-boards.md`). The page is clipped at its right edge by the scan; a clipped word is marked.

Printed lines:

- `SECTION 2   Corrections/Changes`
- `Page 2-3   Cabinet Assembly` / `Item #5 changed to A-18531-1  4-Ball Cashbox Assembly.` (not a board; listed only because it sits between the headings)
- `Page 2-11   Printed Circuit Boards` / `Replace PCB A-18821 with A-19606 Opto Track Limit PCB Assembly.`

Board drawing printed under that entry (outline with a notch at the bottom holding connector `J1`): labels `D1`, `D2` (cylindrical diode outlines at the top, left and right), `OPTO1` (left box), `OPTO2` (right box, set higher), `R1` (below `OPTO1`), `R2` (below `OPTO2`), `J1` (six small circles in a notched edge at the bottom).

Parts list for A-19606, columns `Part No.`, `Designator`, `Description`:

| Part No. | Designator | Description |
| --- | --- | --- |
| `5791-13830-06` | `J1` | `Connector, 6-pin` |
| `5010-08930-00` | `R1, R2` | `Res., 470, 1/2w, 5%` |
| `5070-09054-00` | `D1, D2` | `Diode, 1N4004` |
| `5490-12451-00` | `OPTO1,` (continued on the next line) `OPTO2` | `Opto Integrated, 10m` (the line is cut off by the page edge after `10m`) |

No schematic, pin list or wire table is printed for A-19606 on this page. Folio: page number `8` (amendment page).

## Uncertain readings

Every pin-list line above was read at 2x to 3x on a crop and is believed exact. The following are less certain or are printed oddities worth a second look:

- m-133, the `R6` label on the OPTO 9 (`E9`, `J5`) comparator input divider (`2K` shunt resistor) was read as `R6`; the same page also prints `R6` on the `ANODE 6` line of `J1`. Crop: `m133-t14.png`, `m133-u4.png`, `m133-t11.png`. The unnumbered resistor printed only as `R` `22K` in front of `U2A` pin 1 is printed without a number. Crop: `m133-u5.png`.
- m-133, which row line each of `D1` to `D7` and `D10` to `D12` reaches was followed by eye through crossing lines (`m133-w1.png`, `m133-w2.png`, `m133-v1.png`, `m133-v3.png`); the stubs printed `ROW 1`, `ROW 2`, `ROW 3` beside `D10`, `D11`, `D12` support the last three.
- m-127, the destination of each `Red-` 50 VDC wire (which coil it feeds) and the `J901` to `J105` and `J904` to `J114` pin pairing were followed by eye (`m127-a.png` to `m127-d.png`); m-128 confirms the coil colours.
- m-129, the two cable-side interconnect lines between the left and right opto boards (left pin 7 to right pin 6, left pin 4 to right pin 3) and which left pin takes the `Gray-Yellow` `+12V` wire are traced and look inconsistent with the m-126 pin lists (`J1-6` vs `J1-7`). Crop: `m129-a.png`.
- m-132, the diagram prints `Gray-Yellow` at `J1` pin 4 where the pin list prints `Gray-Black`. Crops: `m132-j1wires.png`, `m132-j1.png`.
- m-126, the board-drawing slot connector at the lower left was not transcribed beyond its existence. Crop: `m126-board.png`.
- a-07, the unit sign after `0.1` on `C1` is blurred (read `0.1u`). Crop: `a07-sch.png`. The package pin roles of the `SHARP GP1A52HR` symbols are followed by eye.
- a-08, the last parts line is clipped by the page edge after `Opto Integrated, 10m`. Crop: `a08-limitr2.png`.
