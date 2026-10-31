Source: `Stern_1980_Nine_Ball_Schematic_Diagrams_paginated.pdf` (IPDB machine 1678), PDF page 3, `SOLENOID DRIVER/VOLTAGE REGULATOR SCHEMATIC FOR NINE BALL` (the game name is lettered into the title block's blank), the `MOMENTARY SOLENOIDS` section at the right. Reproduced in `solenoid-driver-outputs.webp`; read from enlargements of the page at its native resolution.

Inputs, verbatim: `PINS 3, 4, 5 & 6 MOMENTARY SOLENOID DATA` and `PIN 7 SOLENOID BANK SELECT LOW WHEN SELECTED` on connector `J4` `B`: J4-6 `[BLU-Y]` to U2 pin 23, J4-5 `[BLU-R]` to 22, J4-4 `[O-B]` to 21, J4-3 `[R-W]` to 20, J4-7 `[BRN-R]` to 19, each with a 100K pull-up (R1-R4) to `+5`. The decoder is `U2` `74L154` (pin 24 supply, pin 12 ground).

Each decoder output runs through a resistor R57-R71 to a driver stage (an op-amp section of U1, U3 or U4, a diode CR, a capacitor C and a transistor Q). The first stage is annotated with the shared values `1.2K (x15)` (R57), `R5 120 Ω (x15)`, `1N4004 (x15)`, `.002 (x15)` (C1), `R6 330 Ω (x15)` and `SE9302 (x15)`. Decoder pin to output transistor, as drawn:

| U2 pin | Resistor | Transistor |
| ---: | --- | --- |
| 1 | R57 | Q2 |
| 2 | R58 | Q1 |
| 3 | R59 | Q5 |
| 4 | R60 | Q6 |
| 5 | R61 | Q7 |
| 6 | R62 | Q3 |
| 7 | R63 | Q4 |
| 8 | R64 | Q8 |
| 9 | R65 | Q13 |
| 10 | R66 | Q14 |
| 11 | R67 | Q9 |
| 13 | R68 | Q10 |
| 14 | R69 | Q12 |
| 15 | R70 | Q11 |
| 16 | R71 | Q16 |
| 17 | (no stage drawn) | |

Output connectors and their labels, verbatim:

| Connector pin | Label |
| --- | --- |
| J2-9 | LEFT SLINGSHOT (G-O) |
| J2-4 | RIGHT SLINGSHOT (G-Blu) |
| J2-10 | RIGHT DROP BANK (G-Y) |
| J2-11 | TOP DROP BANK (G-R) |
| J2-5 | KNOCKER (G-B) |
| J2-6 | (no label) |
| J2-12 | POP BUMPER (R-Y) |
| J3-7, J3-4 (`J3` `D`) | (no label) |
| J1-5 (`J1` `P`) | OUTHOLE (B-Blu) |
| J1-2, J1-3 | (no label) |
| J5-10 | LEFT LANE KICKOUT HOLE (B-O) |
| J5-12 | DROP TARGET #7 (B-Y) |
| J5-11 | DROP TARGET #6 (B-G) |
| J5-9 | DROP TARGET #5 (R-Blu) |
| J5-15 | DROP TARGET #4 (O-W) |
| J5-13 | DROP TARGET #3 (O-G) |
| J5-14 | DROP TARGET #2 (O-B) |
| J5-8 | DROP TARGET #1 (G-W) |

Notes printed below the section, verbatim: `U1, U2 & U3 = CA3081` / `*SE9302 Substitute X44E198` / `Solenoid Test Display No. is Drive Transistor (Q) Position on SDU`.

PinMAME publishes decoder output n (U2 pin 1-11 and 13-16 in order) as public solenoid n + 1, so this sheet's drawing gives public 1-15 to Q2, Q1, Q5, Q6, Q7, Q3, Q4, Q8, Q13, Q14, Q9, Q10, Q12, Q11 and Q16. The resistor and transistor labels are small at the scan's resolution; the ROM's own solenoid test (retained run `runtime.nine-ball.solenoid-test`) pairs the same numbers independently.
