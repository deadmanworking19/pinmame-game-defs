# Star Gazer — solenoid driver sheet, flipper, relay and continuous drivers

Transcribed from `Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf`, PDF page 3, "SOLENOID DRIVER/VOLTAGE REGULATOR SCHEMATIC FOR STAR GAZER", the block in its lower left, read from the rendered page and checked against a native-resolution crop. The same sheet's momentary output connectors are transcribed in their own excerpt. Printed device types in this block: `SE9302` for the four drivers `Q15`, `Q17`, `Q18` and `Q19`, the note `*SE9302 Substitute X44E198`, and `CR20 IN4004` across the relay coil.

| drawn item | connector pin | printed label / wire |
| --- | --- | --- |
| To Left Flipper Coil | J1 pin 8 | [G] |
| To Right Flipper Coil | J1 pin 9 | [O] |
| left flipper switch contacts (drawn pins 4 and 6) | J2 pin 2 | To LEFT [BLU] FLIPPER BUTTON |
| right flipper switch contacts (drawn pins 3 and 5) | J2 pin 1 | To RIGHT [R] FLIPPER BUTTON |
| FLIPPER ENABLE RELAY (coil, with a CR20 IN4004 across it, supply 43 VDC) | J3 pin 5 | To A2J3-8 [Y-W] |
| driver `Q15` (SE9302) | the relay coil above | |
| driver `Q17` (SE9302) | J5 pin 7, drawn as a box with no label | |
| driver `Q18` (SE9302) | J2 pin 15 | BALL KICKER (R-W) |
| driver `Q19` (SE9302) | J2 pin 8 | COIN LOCK-OUT [Y-W] |
| J5 pin 3 | | N/U |
| J3 pin 4 | | N/U |
| J3 pin 24 | | [W-O], marked `+43 V SOLENOID GND` |
| J3 pin 23 | | [R-Y] |

The four continuous drivers are fed from J4 lines `PB6` (pin 8, `FLIPPER DISABLE`, [BLU-W]), `PB4` (pin 11, [Y-W]), `PB7` (pin 10, [Y-R]) and `PB5` (pin 9, [BLU-O]).

The sheet labels the `Q18` load `BALL KICKER`; the manual's solenoid page prints position 18 as `OPEN` and its parts list has no ball-kicker coil, so the label is kept here as printed and the disagreement is stated on the device.
