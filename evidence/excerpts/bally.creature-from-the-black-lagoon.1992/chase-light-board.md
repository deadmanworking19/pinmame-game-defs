# Creature from the Black Lagoon — Chase Light II board

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 118, printed page 3-14, "Chase Light II P.C.
Board Assembly A-15541", and PDF page 119, printed page 3-15, "Chase Light II Schematic". Read from the pages'
native 200 dpi scans. Printed wording is kept; only line breaks were normalized.

## Connector list (3-14)

| Pin | Printed text |
| --- | --- |
| J1-1 | Green from J120-5 |
| J1-2 | Brown from J120-1 |
| J1-3 | Black, Ground from J118-3 |
| J1-4 | Gray-Yellow, +12VDC from J118-2 |
| J1-5 | Key |
| J1-6 | White-Green from J120-10 |
| J1-7 | White-Brown from J120-7 |
| J2-1 | Black-Yellow from J126-8 |
| J2-2 | Blue-Gray from J126-8 |
| J2-3 | Key |
| J3-1 | White-Green to chase lights |
| J3-2 | Orange-Green to chase lights |
| J3-3 | Key |
| J3-4 | Orange-Blue to chase lights |
| J3-5 | Orange-Violet to chase lights |
| J3-6 | Orange-Gray to chase lights |
| J4-1 | White-Brown to chase lights |
| J4-2 | Key |
| J4-3 | Orange-Brown to chase lights |
| J4-4 | Orange-Red to chase lights |
| J4-5 | Orange-Black to chase lights |
| J4-6 | Orange-Yellow to chase lights |

## Block diagram (3-14, lower half)

`POWER DRIVER BOARD` J118-2 GRY-YEL and J118-3 BLK to the board's J1-4 and J1-3; J120-7 WHT-BRN to J1-7, J120-10
WHT-GRN to J1-6, J120-1 BRN to J1-2, J120-5 GRN to J1-1; J126-8 BLU-GRY to J2-2 and J126-4 BLK-YEL to J2-1.
`CHASE LIGHT II P.C.B.` J4 (pins 1, 3, 4, 5, 6: WHT-BRN, ORG-BRN, ORG-RED, ORG-BLK, ORG-YEL) to a box `A-16087
FLEXIBLE LAMP BOARD`; J3 (pins 1, 2, 4, 5, 6: WHT-GRN, ORG-GRN, ORG-BLU, ORG-VIO, ORG-GRY) to a box `A-16088
FLEXIBLE LAMP BOARD`, which is drawn connected on to a third box `A-16089 FLEXIBLE LAMP BOARD`.

The block diagram draws J126-4 on J2-1 where the connector list prints "J126-8" for both J2 pins.

## Schematic (3-15)

J1: pin 7 `G. I. (1)`, pin 6 `G. I. (2)`, pin 2 `G. I. RT1`, pin 1 `G. I. RT2`, pin 5 `KEY`, pin 4 `+12VDC`, pin 3
`GND`. J2: pin 1 `DRIV. 1`, pin 2 `DRIVE. 2`, pin 3 `KEY`. Each drive line passes a 2N4403 (Q18 for DRIV. 1, Q17 for
DRIVE. 2) to the A and B inputs of both halves of a 74LS139 (U1A, U1B; C inputs tied low). U1A outputs Y0-Y3 and U1B
outputs Y0-Y3 drive, through a ULN2803 (U2) and 2N4403 stages, eight BT138E triacs: Q4, Q3, Q8, Q7 (referred to RT1)
to J4 `LAMP 1A`-`LAMP 4A` (J4 pins 3-6, with `G. I. (1)` on J4-1), and Q12, Q11, Q16, Q15 (referred to RT2) to J3
`LAMP 1B`-`LAMP 4B` (J3 pins 2, 4, 5, 6, with `G. I. (2)` on J3-1). An LM7805 regulator and LED 1 sit on the +12VDC
input.

## Reading notes

- G.I. string 1 (brown, J120-1/J120-7) feeds the A half and G.I. string 4 (green, J120-5/J120-10) the B half. On
  this power driver board those are public G.I. 0 and 3 (`solenoid-flasher-wiring.md`, printed strings 01 and 04,
  "Sequential G.I. #1" and "#2").
- The two drive lines are solenoid outputs 20 (J126-4, Black-Yellow) and 24 (J126-8, Blue-Gray), printed
  "Sequential G.I. #1/#2" in the solenoid tables. Both 74LS139 halves see the same two select bits, so the A and B
  strings with the same number step together.
- Each drive line's 2N4403 conducts while its solenoid driver pulls the line low and then drives its select input
  high (Q18 for DRIV. 1 on the A inputs, Q17 for DRIVE. 2 on the B inputs), so the selected output is the solenoid-20
  bit plus twice the solenoid-24 bit, as pinned PinMAME computes it, when solenoid 20 is on J2-1. The Power Driver
  Board connector list instead sends solenoid 20 to J2-2 and solenoid 24 to J2-1 (`power-driver-board-connectors.md`).
- The 74LS139 outputs are active low (drawn with bubbles). The selected output goes low, its ULN2803 channel stops
  sinking, its 2N4403 turns off and its triac gets no gate current, while the three unselected outputs stay high, sink
  through the ULN2803 and turn their 2N4403s and triacs on. Each group therefore lights three strings and darkens the
  selected one: the chase is a moving dark string.
- The boards the diagram names are flexible 8-lamp boards: the parts list (`parts-list.md`) puts A-16087, A-16088
  and A-16089 on the A-15621-1 swirl ramp and an A-15672 8-lamp board in the A-15993 bowl. The diagram's chaining
  disagrees with the parts list, which puts the strip socket A-16088 plugs into on A-16087 and gives A-16089 its own
  cable header; the diagram does not draw the bowl board at all.
