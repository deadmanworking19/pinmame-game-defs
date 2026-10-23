Source: `Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf` (IPDB machine 249, "Schematics And Wiring Diagrams (Hi-resolution) [Stern Electronics, Inc]", nine 3328x5080 grayscale scans at about 300 dpi, no text layer), PDF page 9, drawing `12B-432-S-121`, title block `PLAYFIELD WIRING DIAGRAM BIG GAME` (Stern Electronics, 1725 Diversey Parkway). The drawing is stored sideways; it was read rotated a quarter turn clockwise at native resolution.

The switch matrix at the left of the sheet: five strobe columns and eight return rows. Every cell is a normally open contact with a series diode (note: `ALL DIODES ARE IN - 4004`). Column headings, verbatim: `STO A`, `STI B`, `ST2 C`, `ST3 D`, `ST4 E`. Strobe wires at the foot of the matrix: `A4J2-1 (W-R)` (ST0), `A4J2-2 (BRN-W)` (ST1), `A4J2-3 (W-BLU)` (ST2), `A4J2-4 (W-Y)` (ST3), `A4J2-5 (Y-R)` (ST4). Return wires at the left: `I0 A4J2-8 (BRN)`, `I1 A4J2-9 (GREY)`, `I2 A4J2-10 (W-O)`, `I3 A4J2-11 (W-B)`, `I4 A4J2-12 (W-G)`, `I5 A4J2-13 (W-BRN)`, `I6 A4J2-14 (BRN-Y)`, `I7 A4J2-15 (O)`.

Cell labels, verbatim; `(cap)` marks a cell that draws a capacitor across the contact; `(blank)` marks a contact drawn with no label (the cabinet positions, which this sheet does not wire):

| Return | ST0 A | ST1 B | ST2 C | ST3 D | ST4 E |
| --- | --- | --- | --- | --- | --- |
| I0 | (blank) | TOP THUMP. | TOP L. R.O.W. | CENTER R.O.B. (cap) | OUT- HOLE |
| I1 | (blank) | LOWER-L. THUMP. | TOP MID. R.O.W. | TOP LEFT ROB (cap) | SAUCER |
| I2 | (blank) | RIGHT THUMP. | TOP R. R.O.W. | CENTER LEFT R.O.W. | RIGHT OUTLANE |
| I3 | SP.T. (LEFT) | L. SLING SHOT | S.U."G" (cap) | R. RETURN LANE | LEFT OUTLANE |
| I4 | SP.T. (RIGHT) | R.SLING SHOT | S.U."A" (cap) | L. RETURN LANE | TOP(2) 10 PTS. |
| I5 | (blank) | LEFT D.T. #3 | TOP-R. D.T. #6 | LOW. R. D.T. #9 | TOP-R. R.O.B. (cap) |
| I6 | (blank) | LEFT D.T. #2 | TOP-R. D.T. #5 | LOW. R. D.T. #8 | R. MID. R.O.B. (cap) |
| I7 | (blank) | LEFT D.T. #1 | TOP-R. D.T. #4 | LOW. R. D.T. #7 | R. LOWER R.O.B. (cap) |

Public address = strobe x 8 + return + 1 (ST0 I0 = 1, ST4 I7 = 40); the five ST0 cells left blank here are 1-3 and 6-8, the cabinet switches on the cabinet sheet.

Below the matrix: `A2J1-8 (W)` labelled `6 VAC` feeding a lamp symbol `GEN. ILLUM`, returning on `A2J1-1 (R)` labelled `RETURN`. No switch, relay or driver transistor is drawn in that circuit.

Notes, verbatim: `N/U = NOT USED`, `ALL DIODES ARE IN - 4004`, `D.T. = DROP TARGET`, `S.U. = STAND-UP TARGET`, `R.O.B. = ROLL-OVER BUTTON`, `SP. T. = SPINNING TARGET`, `R.O.W. = ROLL-OVER WIRE FORM`.
