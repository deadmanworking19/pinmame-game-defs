Source: `Stern_1980_Nine_Ball_Schematic_Diagrams_paginated.pdf` (IPDB machine 1678), PDF page 3, `SOLENOID DRIVER/VOLTAGE REGULATOR SCHEMATIC FOR NINE BALL`, the `CONTINUOUS SOLENOIDS` section at the lower left. Reproduced in `solenoid-driver-continuous-section.webp`; read from enlargements of the page at its native resolution.

Inputs on connector `J4` `B`, verbatim: pin 8 `FLIPPER DISABLE` `PB6` `[BLU-W]`; pin 11 `PB4` `[Y-W]`; pin 10 `PB7` `[Y-R]`; pin 9 `PB5` `[BLU-O]`.

| Input | Stage parts as printed | Transistor | Output as drawn |
| --- | --- | --- | --- |
| J4-8 PB6 | R37 3.9K, R38 120 Ω, U4 pins 2/3, CR15 1N4004, C11 .002, R39 330 Ω | Q15 SE9302 * | `FLIPPER ENABLE RELAY` coil (pins 8 and 7, diode `CR20` `1N4004` across it) to `43 VDC`; `J3` `B` pin 5 `To A2J3-8 [Y-W]` |
| J4-11 PB4 | R40 3.9K, R41 120 Ω, U4 pin 10, CR17 1N4004, C12 .002, R42 330 Ω | Q17 SE9302 * | `LEFT DROP BANK RESET` `(O-R)` to `J5` pin 7 |
| J4-10 PB7 | R43 3.9K, R44 120 Ω, U4 pins 12/11, CR18 1N4004, C13 .002, R45 330 Ω | Q18 SE9302 * | `J5` pin 3 `LOOP D.T. (R-W)`; the same line continues to `J2` `C` pin 15 and `J3` pin 9 `N/U` |
| J4-9 PB5 | R46 3.9K, R47 3.9K, U4 pins 13/14, CR19 1N4004, C14 .002, R48 330 Ω | Q19 SE9302 * | `J2` pin 8 |

Flipper relay contacts, verbatim: `To LEFT FLIPPER COIL [G]` `J1` pin 8 through the `LEFT FLIPPER SW.` contact (terminals 4 and 6) to `J2` `C` pin 2 `To LEFT [BLU] FLIPPER BUTTON`; `To RIGHT FLIPPER COIL [O]` `J1` pin 9 through the `RIGHT FLIPPER SW.` contact (terminals 3 and 5) to `J2` pin 1 `To RIGHT [R] FLIPPER BUTTON`. A dashed line joins both contacts to the relay coil.

At the lower right, `+43V SOLENOID GND` to `J3` pins 24 `[W-O]` and 23 `[R-Y]`.

The `J2` pin 8 output of Q19 carries no label on this sheet; the manual's solenoid table names it `19 Q19 J2-8 Y-W COIN LOCK-OUT`.
