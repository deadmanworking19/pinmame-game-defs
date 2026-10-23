Source: `Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf` (IPDB machine 249), PDF page 8, drawing `12B-432-S-121`, title block `CABINET AND FRONT DOOR WIRING` `FOR STANDARD` (dated 10-16-79). The drawing is stored sideways; it was read rotated a quarter turn clockwise at native resolution.

Service buttons at the top left, verbatim: `A4J3-5 (-W-)` to the `S33 MEMORY CLEAR` pushbutton; `A4J3-1 (R)` to the `TEST SWITCH` pushbutton; both buttons return on `A3J2-7 (Y-R)`.

The cabinet matrix repeats the five strobes `STO A` to `ST4 E` and eight returns `I0` to `I7`. The cabinet sheet labels only these cells; the others are drawn as unlabelled contacts, some with a series diode and some without, and are the playfield sheet's switches:

| Return | Wire, as printed | Labelled cell (ST0 column) |
| --- | --- | --- |
| I0 | A4J3-9 (R-W) | CHUTE |
| I1 | A4J3-10 (BRN-W) | CHUTE |
| I2 | A4J3-11 (BLU) | CHUTE |
| I5 | A4J3-14 (BLU-W) | CREDIT |
| I6 | A4J3-15 (BLU-O) | TILT, with a second contact drawn in parallel and a capacitor across the pair |
| I7 | A4J3-16 (Y) | SLAM |

ST0 is fed on `A4J3-2 (R-Y)`; ST1 on `A4J3-3 (R-G)`; the other strobe wires are drawn without a printed pin. In the ST0 column the CHUTE contacts on I0 and the CREDIT, TILT and SLAM contacts are drawn with a series diode; the I1 and I2 CHUTE contacts are drawn without one.

Flipper buttons, verbatim: `A3J2-2 (BLU)` to `LEFT FLIPPER`, `A3J2-1 (R)` to `RIGHT FLIPPER`, both returning on `A2J2-9 (O)`. Front door lights: `A2J2-1 (Y-B)` to a lamp labelled `FRONT DOOR LITES`, returning on `A2J2-5 (G-R)`. Coin lockout: `A2J2-2 (G)` and `A3J2-8 (Y-W)` to the `COIN LOCKOUT` coil. Knocker: `A3J2-5 (B-Y)` to the `KNOCKER` coil. Notes, verbatim: `N/U = NOT USED`, `ALL DIODES ARE IN-4004`.
