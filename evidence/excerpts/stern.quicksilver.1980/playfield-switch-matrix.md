Source: `Stern_1980_Quicksilver_Manual.pdf` (IPDB machine 1895, "English Manual [Stern Electronics]", 35 pages, a 300 dpi bilevel scan with no text layer), PDF page 20, the left part of the playfield wiring diagram (the title block is on PDF page 21: `STERN ELECTRONICS INC.`,
`WIRING DIAGRAM`, `FOR QUICK SILVER`, `SHEET #2 OF 3`, drawing number `12B-432-S-117`). Hand-drawn schematic. Transcribed by
hand from the 300 dpi render and checked cell by cell.

Every switch is drawn as a normally open contact in series with a diode; the notes say `ALL DIODES ARE 1N - 4004`.
Standup targets, roll-over buttons and the lone standup are additionally drawn with a small target-actuator symbol
under the contact; drop-target, roll-over wire form, kick-out and lane cells are not.

Strobe columns (headed `ST0 A`, `ST1 B`, `ST2 C`, `ST3 D`, `ST4 E`) and the MPU wire each strobe line leaves on:

| Strobe | Connection |
| --- | --- |
| ST0 | A4J2-1 (W-R) |
| ST1 | A4J2-2 (BRN-W) |
| ST2 | A4J2-3 (W-BLU) |
| ST3 | A4J2-4 (W-Y) |
| ST4 | A4J2-5 (Y-R) |

Return rows `I0` to `I7` (the first row's label is printed `Ic`) and the MPU wire each return leaves on:

| Return | Connection |
| --- | --- |
| I0 | A4J2-8 (BRN) |
| I1 | A4J2-9 (GREY) |
| I2 | A4J2-10 (W-O) |
| I3 | A4J2-11 (W-B) |
| I4 | A4J2-12 (W-G) |
| I5 | A4J2-13 (W-BRN) |
| I6 | A4J2-14 (BRN-Y) |
| I7 | A4J2-15 (O) |

Cell labels, verbatim, by return row and strobe column. A cell with no label is drawn with a switch symbol and a
diode but no text; it is blank on this sheet, not unused (`N/U` is the printed word for unused and appears nowhere in
the grid).

| Return | ST0 | ST1 | ST2 | ST3 | ST4 |
| --- | --- | --- | --- | --- | --- |
| I0 | (blank) | RIGHT THUMP. | TOP L. R.O.W. | TOP RIGHT S.U. | OUT-HOLE |
| I1 | (blank) | LEFT THUMP. | TOP R.O.W. | R. S.U. | LEFT OUT-LANE |
| I2 | (blank) | LOWER THUMP. | TOP R.O.W | RIGHT S.U. BOTTOM | RIGHT OUT-LANE |
| I3 | RIGHT S.T. | LEFT SL. SHOT | TOP R. R.O.W. | RIGHT R.O.B. | L. RETURN LANE |
| I4 | LEFT S.T. | RIGHT SL. SHOT | CENTER HIGHEST D.T. | KICKOUT HOLE | R. RETURN LANE |
| I5 | (blank) | L. LOWER S.U. | CENTER D.T. | RIGHT D.T. TOP | (4) 10-PT. SWITCHES |
| I6 | (blank) | L. MID. S.U. | CENTER D.T. | RIGHT D.T. MIDDLE | TOP R.O.B. |
| I7 | (blank) | L. TOP S.U. | CENTER D.T. LOWEST | RIGHT D.T. LOWER | LONE S.U. |

The ST0 cells at I0, I1, I2, I5, I6 and I7 are the cabinet switches drawn in full on the cabinet sheet (PDF page 22):
chutes 1-3, credit, tilt and slam. A small marginal mark `A +1` (probably `A ±1`) beside the I0 wire label is
illegible and is not interpreted.

Below the grid, at lower centre: `A2J1-8 (W)` `6 VAC` feeding a lamp labelled `GEN. ILLUM`, returning on `A2J1-1 (R)`
labelled `RETURN`. The general illumination is a plain 6 VAC lamp string with no driver-board connection.

Notes, verbatim: `N/U = NOT USED`; `ALL DIODES ARE IN - 4004`; `D.T. = DROP TARGET`; `S.U. = STAND-UP TARGET`;
`R.O.B. = ROLL-OVER BUTTON`; `SP.T. = SPINNING TARGET`; `R.O.W. = ROLL-OVER WIRE FORM`. Drawing number box at lower
left: `12B-432-S-117`.
