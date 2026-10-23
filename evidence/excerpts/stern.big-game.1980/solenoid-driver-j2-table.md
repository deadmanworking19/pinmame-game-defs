Source: `Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf` (IPDB machine 249), PDF page 5, drawing `12B-432-S-121`, title block `SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC FOR BIG GAME` (dated 11-15-79). The drawing is stored sideways; it was read rotated a quarter turn clockwise at native resolution.

The boxed `J2` table at the lower left of the sheet, verbatim:

| J2 pin | Label |
| ---: | --- |
| 9 | LEFT THUMPER(W-O) |
| 4 | TOP THUMPER (G-R) |
| 10 | RIGHT THUMPER(Y-BLU) |
| 11 | L. SLING-SHOT(B-BLU) |
| 5 | KNOCKER (B-Y) |
| 12 | R. SLING-SHOT(O-W) |

Note at the centre of the sheet, verbatim: `U1, U2 & U3 = CA3081`, `*SE9302 Substitute X44E198`, `Solenoid Test Display No. is Drive Transistor (Q) Position on SDU`. The driver chain is a `74154` decoder `U2` (inputs from J4 pins 3, 4, 5 and 6, `MOMENTARY SOLENOID DATA`, and pin 7 `SOLENOID BANK SELECT LOW WHEN SELECTED`) driving sixteen pre-driver/driver pairs.

The playfield wiring diagram (PDF page 9) calls the J2 pin-9 and pin-10 coils `LOWER L. THUMPER` and `LOWER R. THUMPER` and the Solenoid Identification table calls them `LOWER LEFT THUMPER` and `LOWER RIGHT THUMPER`; all three name the same two bumpers below the top thumper.
