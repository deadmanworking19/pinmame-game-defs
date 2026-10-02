# Star Gazer — solenoid driver sheet, momentary output labels

Transcribed from `Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf`, PDF page 3, "SOLENOID DRIVER/VOLTAGE REGULATOR SCHEMATIC FOR STAR GAZER" with the heading "MOMENTARY SOLENOIDS", read from the rendered page and checked against a native-resolution crop of the output connectors on the right-hand side of the sheet. The sheet's lower-left flipper, relay and continuous-driver block is transcribed in its own excerpt. The sheet draws a 74L154 decoder (`U2`) whose outputs feed the momentary driver transistors, with four further drivers, `Q15`, `Q17`, `Q18` and `Q19`, drawn in a separate block and fed from PIA port-B lines. A printed note under the decoder reads: "Solenoid Test Display No. is Drive Transistor (Q) Position on SDU". Printed device types: `U1, U2 & U3 = CA3081`, `*SE9302 Substitute X44E198`.

## Momentary outputs, as labelled on the connectors

The drawing labels each decoder-driven output on the right-hand connectors. The transistor `Q` numbers are drawn beside the drivers but the output-to-transistor pairing is not legible for every row, so only the labels, pins and wire colours are transcribed.

| connector pin | printed label | printed wire |
| --- | --- | --- |
| J2 pin 9 | L. SLING-SHOT | (G-O) |
| J2 pin 4 | R. SLING-SHOT | (G-BLU) |
| J2 pin 10 | TOP DROP BANK | (G-Y) |
| J2 pin 11 | R. DROP BANK | (G-R) |
| J2 pin 5 | KNOCKER | (B-Y) |
| J2 pin 6 | OPEN | |
| J2 pin 12 | LEFT THUMPER | (R-Y) |
| J1 pins 5, 2, 3 | L. DROP BANK | (B-BLU) |
| J5 pin 10 | MID. THUMPER | (B-O) |
| J5 pin 12 | OPEN | |
| J5 pin 11 | OPEN | |
| J5 pin 9 | RIGHT THUMPER | (R-BLU) |
| J5 pin 15 | OUT-HOLE | (O-W) |
| J5 pin 13 | OPEN | |
| J5 pin 14 | OPEN | |
| J5 pin 8 | OPEN | |

Two further pins, labelled `7` and `4`, sit in a small separate block drawn under the J2 column and joined to the J2 pin 5 and pin 6 lines. The drawing gives that block no name.
