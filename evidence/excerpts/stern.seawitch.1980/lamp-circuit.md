# Seawitch LDA-100 circuit

Schematics PDF p9,12B-432-S-123 sheet1of3. Drawing crop is separate from the transcribed load table. Read visually against the retained tiled scan. U1-U4 are MC14514B. S0-S14 below are normalized into numerical order: U3/U4 print S12-S14 ABOVE S0. Every output line and labelled connector branch is retained. R and Q numbers agree on every drawn line. Public values are derived from pinned by35_lampStrobe, not printed.

| Decoder | Output | Resistor | SCR | Derived public |
| --- | ---: | --- | --- | ---: |
| U1 | S0 | R14 | Q14 | 1 |
| U1 | S1 | R12 | Q12 | 2 |
| U1 | S2 | R13 | Q13 | 3 |
| U1 | S3 | R8 | Q8 | 4 |
| U1 | S4 | R9 | Q9 | 5 |
| U1 | S5 | R10 | Q10 | 6 |
| U1 | S6 | R11 | Q11 | 7 |
| U1 | S7 | R4 | Q4 | 8 |
| U1 | S8 | R1 | Q1 | 9 |
| U1 | S9 | R2 | Q2 | 10 |
| U1 | S10 | R3 | Q3 | 11 |
| U1 | S11 | R7 | Q7 | 12 |
| U1 | S12 | R16 | Q16 | 13 |
| U1 | S13 | R5 | Q5 | 14 |
| U1 | S14 | R6 | Q6 | 15 |
| U2 | S0 | R29 | Q29 | 17 |
| U2 | S1 | R27 | Q27 | 18 |
| U2 | S2 | R28 | Q28 | 19 |
| U2 | S3 | R35 | Q35 | 20 |
| U2 | S4 | R34 | Q34 | 21 |
| U2 | S5 | R22 | Q22 | 22 |
| U2 | S6 | R26 | Q26 | 23 |
| U2 | S7 | R25 | Q25 | 24 |
| U2 | S8 | R24 | Q24 | 25 |
| U2 | S9 | R17 | Q17 | 26 |
| U2 | S10 | R23 | Q23 | 27 |
| U2 | S11 | R21 | Q21 | 28 |
| U2 | S12 | R15 | Q15 | 29 |
| U2 | S13 | R18 | Q18 | 30 |
| U2 | S14 | R19 | Q19 | 31 |
| U3 | S0 | R36 | Q36 | 33 |
| U3 | S1 | R38 | Q38 | 34 |
| U3 | S2 | R44 | Q44 | 35 |
| U3 | S3 | R49 | Q49 | 36 |
| U3 | S4 | R48 | Q48 | 37 |
| U3 | S5 | R37 | Q37 | 38 |
| U3 | S6 | R32 | Q32 | 39 |
| U3 | S7 | R20 | Q20 | 40 |
| U3 | S8 | R42 | Q42 | 41 |
| U3 | S9 | R41 | Q41 | 42 |
| U3 | S10 | R40 | Q40 | 43 |
| U3 | S11 | R39 | Q39 | 44 |
| U3 | S12 | R33 | Q33 | 45 |
| U3 | S13 | R30 | Q30 | 46 |
| U3 | S14 | R31 | Q31 | 47 |
| U4 | S0 | R57 | Q57 | 49 |
| U4 | S1 | R50 | Q50 | 50 |
| U4 | S2 | R51 | Q51 | 51 |
| U4 | S3 | R54 | Q54 | 52 |
| U4 | S4 | R55 | Q55 | 53 |
| U4 | S5 | R60 | Q60 | 54 |
| U4 | S6 | R59 | Q59 | 55 |
| U4 | S7 | R58 | Q58 | 56 |
| U4 | S8 | R56 | Q56 | 57 |
| U4 | S9 | R46 | Q46 | 58 |
| U4 | S10 | R52 | Q52 | 59 |
| U4 | S11 | R53 | Q53 | 60 |
| U4 | S12 | R47 | Q47 | 61 |
| U4 | S13 | R43 | Q43 | 62 |
| U4 | S14 | R45 | Q45 | 63 |

| Jack | Pin | SCR |
| --- | ---: | --- |
| J1 | 18 | Q14 |
| J1 | 19 | Q12 |
| J1 | 17 | Q13 |
| J1 | 23 | Q8 |
| J1 | 14 | Q9 |
| J1 | 15 | Q10 |
| J1 | 16 | Q11 |
| J1 | 28 | Q4 |
| J1 | 24 | Q1 |
| J1 | 25 | Q2 |
| J1 | 26 | Q3 |
| J1 | 27 | Q7 |
| J1 | 1 | Q29 |
| J1 | 9 | Q27 |
| J1 | 8 | Q28 |
| J1 | 3 | Q35 |
| J1 | 2 | Q34 |
| J1 | 10 | Q22 |
| J1 | 7 | Q26 |
| J1 | 6 | Q25 |
| J1 | 5 | Q24 |
| J1 | 11 | Q17 |
| J1 | 13 | Q20 |
| J1 | 4 | Q23 |
| J1 | 12 | Q21 |
| J2 | 21 | Q3 |
| J2 | 13 | Q7 |
| J2 | 22 | Q16 |
| J2 | 16 | Q5 |
| J2 | 14 | Q6 |
| J2 | 8 | Q23 |
| J2 | 12 | Q21 |
| J2 | 23 | Q15 |
| J2 | 20 | Q18 |
| J2 | 15 | Q19 |
| J2 | 11 | Q33 |
| J2 | 6 | Q30 |
| J2 | 2 | Q31 |
| J2 | 9 | Q40 |
| J2 | 4 | Q39 |
| J2 | 5 | Q52 |
| J2 | 10 | Q47 |
| J2 | 7 | Q43 |
| J2 | 1 | Q45 |
| J2 | 3 | Q53 |
| J3 | 26 | Q36 |
| J3 | 25 | Q38 |
| J3 | 19 | Q44 |
| J3 | 17 | Q49 |
| J3 | 16 | Q48 |
| J3 | 23 | Q37 |
| J3 | 27 | Q32 |
| J3 | 21 | Q42 |
| J3 | 20 | Q41 |
| J3 | 22 | Q40 |
| J3 | 24 | Q39 |
| J3 | 1 | Q57 |
| J3 | 12 | Q50 |
| J3 | 15 | Q51 |
| J3 | 11 | Q54 |
| J3 | 9 | Q55 |
| J3 | 3 | Q60 |
| J3 | 4 | Q59 |
| J3 | 2 | Q58 |
| J3 | 10 | Q56 |
| J3 | 18 | Q46 |
| J3 | 13 | Q52 |
| J3 | 14 | Q53 |

J1-5/Q24 and J1-4/Q23 are read by following their nets through the heavy lettering. J2-3 is the Q53 net shared with J3-14: follow the continuous line from U4 S11/R53 rather than reading the degraded final glyph as Q58. U2 S7/S8 reach R25/Q25 and R24/Q24; U3/U4 S9 reach Q41/Q46. Connector branches do not establish extra bulb quantities. The chart names no load for Q15,Q42,Q51,Q56. Omission does not prove non-fitment.
