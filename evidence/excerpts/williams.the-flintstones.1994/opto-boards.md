# Williams The Flintstones (1994) — Outhole trough and drop-target opto boards

Source: Williams *The Flintstones* Operations Manual 16-50029-101 (July 1994), IPDB machine 888 file
`Williams_1994_The_Flintstones_English_Manual.pdf`, PDF pages 134-136, printed pages 3-20 to 3-22.
Read from the native 300 dpi renders. Labels are transcribed as printed.

## Outhole Trough Circuit, PDF page 134 (printed page 3-20)

### Block Diagram

Boxes: `Trough 7 IR LED Board (green board)` connector `J1`; `Trough 7 IR Photo Transistor Board (blue
board)` connector `J1`; `Power Driver Board` connectors `J118` and `J113`; `CPU Board` connectors `J211`,
`J209` and `J207` (a ribbon cable joins `J113` and `J211`); and on the right `7-Opto Switch Board` with
connectors `J1`, `J2` and `J3`.

| From | Pin | Wire | Label | 7-Opto Switch Board pin |
| --- | --- | --- | --- | --- |
| Trough 7 IR LED Board J1 | 1 | GRY-VIO | LED7 | J1-1 |
| Trough 7 IR LED Board J1 | 2 | GRY-GRN | LED5 | J1-3 |
| Trough 7 IR LED Board J1 | 3 | GRY-BLK | LED4 | J1-5 |
| Trough 7 IR LED Board J1 | 4 | GRY-ORG | LED3 | J1-6 |
| Trough 7 IR LED Board J1 | 5 | GRY-RED | LED2 | J1-7 |
| Trough 7 IR LED Board J1 | 6 | GRY-BRN | LED1 | J1-8 |
| Trough 7 IR LED Board J1 | 7 | BLK | GND | J1-10 |
| Trough 7 IR Photo Transistor Board J1 | 1 | GRY-YEL | +12V | J2-10 |
| Trough 7 IR Photo Transistor Board J1 | 2 | ORG-BRN | PHOTO TRANSISTOR 1 | J2-7 |
| Trough 7 IR Photo Transistor Board J1 | 3 | ORG-RED | PHOTO TRANSISTOR 2 | J2-6 |
| Trough 7 IR Photo Transistor Board J1 | 4 | ORG-BLK | PHOTO TRANSISTOR 3 | J2-5 |
| Trough 7 IR Photo Transistor Board J1 | 5 | ORG-YEL | PHOTO TRANSISTOR 4 | J2-4 |
| Trough 7 IR Photo Transistor Board J1 | 6 | ORG-GRN | PHOTO TRANSISTOR 5 | J2-3 |
| Trough 7 IR Photo Transistor Board J1 | 7 | ORG-VIO | PHOTO TRANSISTOR 7 | J2-1 |
| Power Driver Board J118 | 2 | GRY-YEL | +12V | J3-1 |
| Power Driver Board J118 | 3 | BLK | GND | J3-3 |
| CPU Board J209 | 1 | WHT-BRN | SW. ROW 1 | J3-5 |
| CPU Board J209 | 2 | WHT-RED | SW. ROW 2 | J3-6 |
| CPU Board J209 | 3 | WHT-ORG | SW. ROW 3 | J3-7 |
| CPU Board J209 | 4 | WHT-YEL | SW. ROW 4 | J3-8 |
| CPU Board J209 | 5 | WHT-GRN | SW. ROW 5 | J3-9 |
| CPU Board J209 | 7 | WHT-BLU | SW. ROW 6 | J3-10 |
| CPU Board J207 | 3 | GRN-ORG | SW. COL. 3 | J3-12 |

No LED 6 or photo transistor 6 line is drawn. The page prints which board pin carries which LED or photo
transistor, but not which switch number each opto pair reports.

Printed note under the block diagram, in bold italic capitals:

> NOTE: GRAY-BLUE AND ORANGE-BLUE WIRES FROM THE 7-OPTO SWITCH BOARD GO TO THE BALL POPPER AND ARE NOT
> PART OF THE OUTHOLE TROUGH CIRCUIT.

### Outhole Trough Circuit Detail

One LED and one photo transistor are drawn, between the `7 IR LED BOARD` and the `7 IR PHOTO TRANS.
BOARD`, with a dashed outline round each and arrows from the LED to the photo transistor. Bracketed
labels: `REPEATED FOR ALL SIX LEDS` beside `GRY-VIO LED7`, `GRY-GRN LED5`, `GRY-BLK LED4`, `GRY-ORG LED3`,
`GRY-RED LED2`, `GRY-BRN LED1`; and `REPEATED FOR ALL SIX PHOTO TRANSISTORS` beside `ORG-BRN PHOTO
TRANSISTOR 1`, `ORG-RED PHOTO TRANSISTOR 2`, `ORG-BLK PHOTO TRANSISTOR 3`, `ORG-YEL PHOTO TRANSISTOR 4`,
`ORG-GRN PHOTO TRANSISTOR 5`, `ORG-VIO PHOTO TRANSISTOR 7`. Further wires: `BLK, GND` and `GRY-YEL, +12V`
to the `7-Opto Switch Board`. Printed text at the right, in capitals:

> IN THE OUTHOLE TROUGH CIRCUIT, THE BALL ROLLS BETWEEN THE TWO BOARDS AND BREAKS THE BEAM, CAUSING THE
> SWITCH TO READ AS MADE.

## A-13609 3-Bank Drop Target Board Assembly, PDF page 135 (printed page 3-21)

Board layout: `OPTO 1`, `OPTO 2`, `OPTO 3` left to right, `D1`, `LED1`, `R1`, `R2`, `R3`, `R4` and
connector `J1`.

Schematic: three optos drawn right to left as `Opto 1`, `Opto 2`, `Opto 3`, each an LED with a series
resistor (`R1 330Ω`, `R3 330Ω`, `R4 330Ω`) and a photo transistor. The photo transistor collectors go to
`J1` pins as follows: `Opto 1` to pin 3 (`Row`), `Opto 2` to pin 2 (`Row`), `Opto 3` to pin 1 (`Row`). The
emitters join and run through `D1 1N4004` to pin 4 (`Col.`). `R2 1.2KΩ` and `LED1` hang from the `+12V`
line (pin 7). Pin 5 is `Key`; pin 6 is `Gnd`.

Printed connector list:

| Pin | Printed text |
| --- | --- |
| J1-1 | White-Violet, Switch Row 7, from CPU Board J209-8 |
| J1-2 | White-Blue, Switch Row 6, from CPU Board J209-7 |
| J1-3 | White-Green, Switch Row 5, from CPU Board J209-5 |
| J1-4 | Green-Yellow, Switch Column 4, from CPU Board J207-4 |
| J1-5 | Key |
| J1-6 | Black, Ground, from Power Driver Board J118-3 |
| J1-7 | Gray-Yellow, +12V, from Power Driver Board J118-2 |

So `Opto 1` reports on row 5 (switch 45), `Opto 2` on row 6 (switch 46) and `Opto 3` on row 7 (switch
47).

## A-19103 4-Bank Drop Target Board Assembly, PDF page 136 (printed page 3-22)

Board layout: `OPTO 1`, `OPTO 2`, `OPTO 3`, `OPTO 4` left to right (pins marked `A`, `E`, `K`, `C`),
diodes `D1`-`D4`, resistors `R1`-`R5`, `LED1`, and a 9-pin connector `J1` (pin 9 at the left, pin 1 at the
right).

Schematic: four optos drawn right to left as `OPTO 1`, `OPTO 2`, `OPTO 3`, `OPTO 4`, each LED with a
series resistor (`R1 470Ω`, `R3 470Ω`, `R4 470Ω`, `R5 470Ω`) and each photo transistor's emitter through
its own diode (`D1`-`D4`, each `1N4004`) to `COL. 4`. The photo transistor collectors go to `J1` as
follows: `OPTO 1` to pin 4 (`ROW 4`), `OPTO 2` to pin 3 (`ROW 3`), `OPTO 3` to pin 2 (`ROW 2`), `OPTO 4`
to pin 1 (`ROW 1`). `R2 820Ω` feeds `LED 1`.

Printed connector list:

| Pin | Printed text |
| --- | --- |
| J1-1 | White-Brown, Switch Row 1, from CPU Board J209-1 |
| J1-2 | White-Red, Switch Row 2, from CPU Board J209-2 |
| J1-3 | White-Orange, Switch Row 3, from CPU Board J209-3 |
| J1-4 | White-Yellow, Switch Row 4, from CPU Board J209-4 |
| J1-5 | Green-Yellow, Switch Column 4, from CPU Board J207-4 |
| J1-6 | Key |
| J1-7 | Black, ground, from Power Driver Board J118-3 |
| J1-8 | Gray-Yellow, +12V, from Power Driver Board J118-2 |
| J1-9 | N/C |

So `OPTO 1` reports on row 4 (switch 44), `OPTO 2` on row 3 (43), `OPTO 3` on row 2 (42) and `OPTO 4` on
row 1 (41). Neither board page says which physical target faces which opto.

## Switch-row connector pins

PDF pages 134 and 135 both print switch row 5 as `WHT-GRN` / `White-Green` on CPU board `J209-5`, and
row 6 on `J209-7`. The switch matrix on PDF page 107 prints row 5's connector as `J209-4` (see the switch
matrix excerpt).
