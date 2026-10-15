# Seawitch playfield matrix, coils, flippers and GI

Source: schematics PDF page 8. All five strobes and eight returns are retained below. [blank] means a genuinely unlabelled drawn contact, distinct from N/U. Cabinet contacts occupy the A-column blanks and are named on page 7. Leader dots/line wrapping are normalized.

| Return / MPU pin / wire | ST0 A | ST1 B | ST2 C | ST3 D | ST4 E |
| --- | --- | --- | --- | --- | --- |
| I0 / A4J2-8 / BRN | [blank] | TOP THUMPER | TOP R. S.U. | RIGHT R.O.B. | OUT-HOLE |
| I1 / A4J2-9 / GREY | [blank] | LEFT THUMPER | TOP L. S.U. | N/U | LEFT OUT-LANE |
| I2 / A4J2-10 / W-O | [blank] | N/U | TOP L. MID. S.U. | N/U | RIGHT OUT-LANE |
| I3 / A4J2-11 / W-B | TOP R.O.B. | LEFT SL.-SHOT | TOP L. LOW S.U. | N/U | LEFT RETURN LANE |
| I4 / A4J2-12 / W-G | RIGHT SPIN. TARG. | RIGHT SL.-SHOT | MID. D.T. #1 | TOP D.T. #1 | RIGHT RETURN LANE |
| I5 / A4J2-13 / W-BRN | [blank] | RIGHT THUMPER | MID. D.T. #2 | TOP D.T. #2 | L. D.T. #1 |
| I6 / A4J2-14 / BRN-Y | [blank] | N/U | MID. D.T. #3 | TOP D.T. #3 | L. D.T. #2 |
| I7 / A4J2-15 / O | [blank] | N/U | MID. D.T. #4 | TOP D.T. #4 | L. D.T. #3 |

| Strobe | MPU pin | Literal wire |
| --- | --- | --- |
| ST0 A | A4J2-1 | W-R |
| ST1 B | A4J2-2 | BRN-W |
| ST2 C | A4J2-3 | W-BLU |
| ST3 D | A4J2-4 | W-Y |
| ST4 E | A4J2-5 | Y-R |

Printed legend: n/u = not used; all diodes are 1n-4004; D.T. = drop target; S.U. = stand-up target; R.O.B. = roll-over button; SP.T. = spinning target; R.O.W. = roll-over wireform.

The four dual-winding flipper symbols each have a winding-bypass contact. The left pair shares A3J1-8 (G), the right pair A3J1-9 (O), supplied by A2J1-6 (BLU-W), with Y common and 1-AMP SLO-BLO fuse. Additional E.O.S.-labelled series marks appear in the second return branch of each pair. The marks are retained literally; they do not establish another public input or independent upper-flipper command. The parts list distinguishes lower and upper coil numbers.

Coil labels: top thumper A3J2-4 (G-BLU); left thumper A3J2-9 (G-O); right thumper A3J5-9 (R-BLU); left sling A3J2-11 (G-R); right sling A3J2-12 (R-Y); out-hole A3J5-11 (B-G); top D.T. A3J5-12 (B-Y); mid D.T. A3J1-5 (B-BLU); left D.T. A3J5-10 (B-O).

GEN. ILLUM is drawn from A2J1-8 (W), labelled 6 VAC, returning A2J1-1 (R). The feature-lamp bus is separately labelled A2J5-7 (BLUE). This game's cabinet drawing separately documents the front-door lighting. No populated backbox harness pin is inferred from the generic transformer drawing.
