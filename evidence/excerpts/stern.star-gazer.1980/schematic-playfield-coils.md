# Star Gazer — playfield sheet, coil circuits

Transcribed from `Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf`, PDF page 2 (the playfield sheet captioned "PLAYFIELD" and "STAR GAZER"), the coil block in the upper middle of the drawing, read from the rendered page and checked against a native-resolution crop. Each coil is drawn with its own suppression diode between a shared supply line, printed `(Y)`, and a driver return line labelled with a connector pin and a bracketed wire colour. The shared supply for the whole block runs through a fuse drawn on the right edge and labelled `1-AMP SLO-BLO`; the flipper supply is separately labelled `A2J1-6 (BLU-W)`.

| drawn coil | connector pin | wire |
| --- | --- | --- |
| LEFT FLIPPER (two windings, an end-of-stroke contact drawn between them) | A3J1-8 | (-G-) |
| RIGHT FLIPPER (two windings, an end-of-stroke contact drawn between them) | A3J1-9 | (-O-) |
| RIGHT SLING-SHOT | A3J2-4 | (G-BLU) |
| LEFT SLING-SHOT | A3J2-9 | (G-O) |
| OUT HOLE | A3J5-15 | (O-W) |
| RIGHT THUMPER | A3J5-9 | (R-BLU) |
| LEFT THUMPER | A3J2-12 | (R-Y) |
| CENTER THUMPER | A3J5-10 | (B-O) |
| LEFT DROP TARGET | A3J1-5 | (B-BLU) |
| TOP DROP TARGET | A3J2-10 | (G-Y) |
| RIGHT DROP TARGET | A3J2-11 | (G-R) |

The flipper circuits are drawn as hard-wired dual-winding assemblies: the supply feeds both windings of each flipper, and the contact drawn between the windings is the flipper's own end-of-stroke contact. No driver transistor is drawn between the supply and a flipper winding on this sheet; the solenoid-driver sheet draws the flipper-enable relay that gates the 43 V supply.

The sheet names the three drop-target coils `LEFT DROP TARGET`, `TOP DROP TARGET` and `RIGHT DROP TARGET`; the manual's solenoid page names them `LEFT DROP TARGET`, `TOP DROP BANK` and `RIGHT DROP BANK`. Neither document says which switch bank a coil resets; the definition takes that from the ROM.
