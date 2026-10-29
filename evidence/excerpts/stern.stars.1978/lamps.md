# Stars lamp-driver extraction

Source: *Stern 1978 Stars Manual*, native-rendered PDF pages 35–36, schematic **B-431-S-103**. Page 35 supplies decoder-output-to-resistor wiring; page 36 supplies SCR-to-connector wiring, printed labels, and wire codes. Connector names below use the requested A5 prefix.

**Public** is derived, not printed in the schematic: `16 × (U − 1) + selector + 1`, following PinMAME `by35_lampStrobe`. Selector 15 is excluded. `[blank]` means no label or wire code is printed at that connector entry; it does not establish that a physical load is unused. Multiple entries in one cell are separate connector branches from the same SCR.

| Decoder selector | Public, derived | Resistor | SCR | Connector pin → literal printed label → wire |
|---|---:|---|---|---|
| U1:0 | 1 | R14 | Q14 | A5J1-18 → SPECIAL WITH YELLOW STAR → BRN-B |
| U1:1 | 2 | R12 | Q12 | A5J1-19 → SPECIAL WITH WHITE STAR → GREY-G |
| U1:2 | 3 | R13 | Q13 | A5J1-17 → 1K BONUS → PUR |
| U1:3 | 4 | R8 | Q8 | A5J1-23 → 5K BONUS → BLU-W |
| U1:4 | 5 | R9 | Q9 | A5J1-14 → 9K BONUS → R-B |
| U1:5 | 6 | R10 | Q10 | A5J1-15 → STAR-YELLOW → -R- |
| U1:6 | 7 | R11 | Q11 | A5J1-16 → STAR-AMBER → O-B |
| U1:7 | 8 | R4 | Q4 | A5J1-28 → 2 ADVANE BONUS → BLU-Y |
| U1:8 | 9 | R1 | Q1 | A5J1-24 → [blank] → [blank] |
| U1:9 | 10 | R2 | Q2 | A5J1-25 → DOUBLE BONUS FEATURE → BRN-O |
| U1:10 | 11 | R3 | Q3 | A5J1-26 → SAME PLAYER SHOOTS AGAIN → G-W<br>A5J2-21 → [blank] → [blank] |
| U1:11 | 12 | R7 | Q7 | A5J1-27 → 400 #1 SPINNER → BRN-BLU<br>A5J2-13 → [blank] → [blank] |
| U1:12 | 13 | R16 | Q16 | A5J2-22 → BALL IN PLAY → BRN-BLU |
| U1:13 | 14 | R5 | Q5 | A5J2-16 → PLAYER #1 → Y-G |
| U1:14 | 15 | R6 | Q6 | A5J2-14 → PLAYER UP 1 → W-Y |
| U2:0 | 17 | R29 | Q29 | A5J1-1 → SPECIAL WITH PURPLE STAR → BLU-R |
| U2:1 | 18 | R27 | Q27 | A5J1-9 → [blank] → [blank] |
| U2:2 | 19 | R28 | Q28 | A5J1-8 → 2K BONUS → G-B |
| U2:3 | 20 | R35 | Q35 | A5J1-3 → 6K BONUS → R-G |
| U2:4 | 21 | R34 | Q34 | A5J1-2 → 10K BONUS → GREY-O |
| U2:5 | 22 | R22 | Q22 | A5J1-10 → SPECIAL WITH GREEN STAR → G-R |
| U2:6 | 23 | R26 | Q26 | A5J1-7 → [blank] → [blank] |
| U2:7 | 24 | R25 | Q25 | A5J1-6 → LEFT & RIGHT OUT LANE → B-Y |
| U2:8 | 25 | R24 | Q24 | A5J1-5 → LEFT & RIGHT RETURN LANE → BLU-O |
| U2:9 | 26 | R17 | Q17 | A5J1-11 → TRIPLE BONUS FEATURE → B-O |
| U2:10 | 27 | R23 | Q23 | A5J1-4 → [blank] → [blank]<br>A5J2-8 → MATCH → GREY-Y |
| U2:11 | 28 | R21 | Q21 | A5J1-12 → 400 #2 SPINNER → G-Y<br>A5J2-12 → [blank] → [blank] |
| U2:12 | 29 | R15 | Q15 | A5J2-23 → HIGHEST SCORE → GREY-O |
| U2:13 | 30 | R18 | Q18 | A5J2-20 → PLAYER #2 → Y-W |
| U2:14 | 31 | R19 | Q19 | A5J2-15 → PLAYER UP 2 → Y-BLU |
| U3:0 | 33 | R36 | Q36 | A5J3-26 → SPECIAL WITH AMBER STAR → -B- |
| U3:1 | 34 | R38 | Q38 | A5J3-25 → [blank] → [blank] |
| U3:2 | 35 | R44 | Q44 | A5J3-19 → 3K BONUS → Y-G |
| U3:3 | 36 | R49 | Q49 | A5J3-17 → 7K BONUS → Y-W |
| U3:4 | 37 | R48 | Q48 | A5J3-16 → [blank] → [blank] |
| U3:5 | 38 | R37 | Q37 | A5J3-23 → STAR-PURPLE → O-R |
| U3:6 | 39 | R32 | Q32 | A5J3-27 → [blank] → [blank] |
| U3:7 | 40 | R20 | Q20 | A5J1-13 → [blank] → [blank] |
| U3:8 | 41 | R42 | Q42 | A5J3-21 → [blank] → [blank] |
| U3:9 | 42 | R41 | Q41 | A5J3-20 → WOW FEATURE → PUR-B |
| U3:10 | 43 | R40 | Q40 | A5J3-22 → 7000 RIGHT → PUR-Y<br>A5J2-9 → [blank] → [blank] |
| U3:11 | 44 | R39 | Q39 | A5J3-24 → DOUBLE BONUS → R-Y<br>A5J2-4 → [blank] → [blank] |
| U3:12 | 45 | R33 | Q33 | A5J2-11 → GAME OVER → GREY-W |
| U3:13 | 46 | R30 | Q30 | A5J2-6 → PLAYER #3 → B-W |
| U3:14 | 47 | R31 | Q31 | A5J2-2 → PLAYER UP 3 → BLU |
| U4:0 | 49 | R57 | Q57 | A5J3-1 → STAR-GREEN → B-W |
| U4:1 | 50 | R50 | Q50 | A5J3-12 → [blank] → [blank] |
| U4:2 | 51 | R51 | Q51 | A5J3-15 → 4K BONUS → GREY-Y |
| U4:3 | 52 | R54 | Q54 | A5J3-11 → 8K BONUS → W-GREY |
| U4:4 | 53 | R55 | Q55 | A5J3-9 → [blank] → [blank] |
| U4:5 | 54 | R60 | Q60 | A5J3-3 → STAR-WHITE → BRN-R |
| U4:6 | 55 | R59 | Q59 | A5J3-4 → [blank] → [blank] |
| U4:7 | 56 | R58 | Q58 | A5J3-2 → [blank] → [blank] |
| U4:8 | 57 | R56 | Q56 | A5J3-10 → [blank] → [blank] |
| U4:9 | 58 | R46 | Q46 | A5J3-18 → SPECIAL FEATURE → R-BLU |
| U4:10 | 59 | R52 | Q52 | A5J3-13 → 7000 LEFT → Y-B<br>A5J2-5 → [blank] → [blank] |
| U4:11 | 60 | R53 | Q53 | A5J3-14 → TRIPLE BONUS → PUR-W<br>A5J2-3 → [blank] → [blank] |
| U4:12 | 61 | R47 | Q47 | A5J2-10 → TILT → GREY-B |
| U4:13 | 62 | R43 | Q43 | A5J2-7 → PLAYER #4 → GREY-R |
| U4:14 | 63 | R45 | Q45 | A5J2-1 → PLAYER UP 4 → BRN |

The native images were checked for the bends and junction dots. The table contains Q1–Q60 exactly once, all 60 legal derived addresses—1–15, 17–31, 33–47 and 49–63—and all 68 connector endpoints drawn for those SCRs, including eight split outputs. Pins absent from the drawing are not added.

**Transcription uncertainty:** A5J1-28 appears to read “2 ADVANE BONUS”; the apparent missing **C** is preserved rather than silently corrected. The schematic is split across the two rendered pages, so resistor-to-SCR continuity is read across the adjoining page edges. Primary curator checked the decoder order and connector branches against the native renders; the ROM independently confirms Tilt at public 61. Blank labels remain unresolved fitment, never presumed unused.

Printed SCR asterisks are recorded separately rather than appended to the
SCR identifiers in the normalized table: Q1, Q2, Q3, Q8, Q9, Q10, Q15,
Q16, Q17, Q22, Q23, Q24, Q33, Q34, Q35, Q40, Q41, Q42, Q47, Q48, Q49,
Q54, Q55, Q56. Page 35 notes: `* SCR'S MCR106 - 1 OTHERS 2N5060`;
`U5, U6, U7 & U8 PINS 1 CONNECTED TO +5 WHILE PINS 8 ARE GROUNDED`;
`U1, U2, U3 & U4 ARE MC14514 OR EQUIVALENT`;
`U5, U6, U7 & U8 ARE CD4050 OR EQUIVALENT`.
