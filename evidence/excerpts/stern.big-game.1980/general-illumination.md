Source: `Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf` (IPDB machine 249), PDF page 6, drawing `12B-168-6A`, title block `TRANSFORMER SCHEMATIC FOR GENERAL USE` (dated 8-24-79), and PDF page 7, drawing `12B-STD-110-2`, `WIRING DIAGRAM FOR SOLID STATE`. Both are shared drawings, not drawn for this game. Stored sideways; read rotated a quarter turn clockwise at native resolution and at half of it.

Transformer schematic, the `TA-100 P.C. BOARD` connector lists, verbatim (pin, wire colour, label):

| Connector | Pin | Wire | Label |
| --- | ---: | --- | --- |
| J2 (CABINET) | 6 | -Y- | A.C. POWER |
| J2 (CABINET) | 7 | -W- | A.C. RETURN |
| J2 (CABINET) | 2 | -G- | COIN LOCK-OUT & KNOCKER BUS |
| J2 (CABINET) | 1 | Y-B | GEN. ILL. BUS |
| J2 (CABINET) | 5 | G-R | GEN. ILL. RETURN |
| J2 (CABINET) | 10 | -G- | A.C. POWER GRD. |
| J2 (CABINET) | 8 | | KEY |
| J1 (PLAYFIELD) | 8 | -W- | GEN. ILL. BUS |
| J1 (PLAYFIELD) | 6 | BLU-W | SOLENOID BUS |
| J1 (PLAYFIELD) | 4 | | KEY |
| J1 (PLAYFIELD) | 7 | -BLU- | FEATURE LAMP BUS |
| J1 (PLAYFIELD) | 1 | -R- | |
| J1 (PLAYFIELD) | 3 | | FEATURE LAMP BUS |
| J3 (BACK-BOX) | 9 | -Y- | FLIPPER ENABLE RE. BUS |
| J3 (BACK-BOX) | 12 | GREY | ZERO CROSSING INPUT |
| J3 (BACK-BOX) | 10 | -O- | GEN. ILL. BUS |
| J3 (BACK-BOX) | 11 | -R- | GEN. ILL. BUS |
| J3 (BACK-BOX) | 6 | -BLU- | FEATURE LAMP BUS |
| J3 (BACK-BOX) | 8 | -O- | 11.9 V.D.C. BUS |
| J3 (BACK-BOX) | 5 | GREY | TO REG. 185VDC INPUT |
| J3 (BACK-BOX) | 1 | -G- | GEN. ILL. RETURN |
| J3 (BACK-BOX) | 2 | -W- | GEN. ILL. RETURN |
| J3 (BACK-BOX) | 3, 4 | R-B, W-R | LDA BOARD RETURN |

The general-illumination buses come from the `7.3 VAC` winding through the board with no switching element drawn. The wiring diagram's A1 insert box draws two general-illumination lamp symbols in the backbox at `5.9 VAC`, one `TO A2J3-11` and `TO A2J3-2`, the other `TO A2J3-10` and to a return printed `A3J3-1` (the A2 list has `GEN. ILL. RET. BACK BOX` on both J3 pins 1 and 2), each labelled `GEN ILL LAMPS`; its A2 transformer list prints J1 pin 1 `GEN. ILL. RET PLAYFIELD`, pin 5 and pin 8 `GEN. ILL. BUSS`, J2 pin 1 `GEN. ILL. BUSS` and pin 5 `GEN ILL. RET.`.

This game's own playfield wiring diagram (PDF page 9) draws `A2J1-8 (W)` `6 VAC` to a lamp `GEN. ILLUM` returning on `A2J1-1 (R)`, and its cabinet sheet (PDF page 8) draws `A2J2-1 (Y-B)` to `FRONT DOOR LITES` returning on `A2J2-5 (G-R)`. None of these sheets draws a relay in a general-illumination circuit.
