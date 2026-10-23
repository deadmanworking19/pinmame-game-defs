Source: `Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf` (IPDB machine 249), PDF page 2, drawing `12B-432-S-121`, `LAMP DRIVER SCHEMATIC FOR BIG GAME` (stored sideways; read rotated a quarter turn clockwise). The four decoder chips `U1`-`U4`, each printed `MC14514B`, on the left of the circuit, with the resistor labels on their output lines. Each output line carries a resistor labelled `R<n>` and `2KΩ`; the resistor's label is printed directly above its zig-zag, and the labels alternate between a position near the chip and one further right. The S-index is the output number printed beside the chip; the outer number is the chip pin. For `U3` and `U4` the outputs S12, S13 and S14 (pins 14, 13 and 16) are drawn above S0 rather than below S11. The SCR column to the right labels each line's SCR `Q<n>` with the same number as its resistor. Every label was read at 1.8 times the native resolution.

### U1 (MC14514B)

| Output | Chip pin | Resistor | SCR |
| ---: | ---: | --- | --- |
| S0 | 11 | R14 | Q14 |
| S1 | 9 | R12 | Q12 |
| S2 | 10 | R13 | Q13 |
| S3 | 8 | R8 | Q8 |
| S4 | 7 | R9 | Q9 |
| S5 | 6 | R10 | Q10 |
| S6 | 5 | R11 | Q11 |
| S7 | 4 | R4 | Q4 |
| S8 | 18 | R1 | Q1 |
| S9 | 17 | R2 | Q2 |
| S10 | 20 | R3 | Q3 |
| S11 | 19 | R7 | Q7 |
| S12 | 14 | R16 | Q16 |
| S13 | 13 | R5 | Q5 |
| S14 | 16 | R6 | Q6 |

### U2 (MC14514B)

| Output | Chip pin | Resistor | SCR |
| ---: | ---: | --- | --- |
| S0 | 11 | R29 | Q29 |
| S1 | 9 | R27 | Q27 |
| S2 | 10 | R28 | Q28 |
| S3 | 8 | R35 | Q35 |
| S4 | 7 | R34 | Q34 |
| S5 | 6 | R22 | Q22 |
| S6 | 5 | R26 | Q26 |
| S7 | 4 | R25 | Q25 |
| S8 | 18 | R24 | Q24 |
| S9 | 17 | R17 | Q17 |
| S10 | 20 | R23 | Q23 |
| S11 | 19 | R21 | Q21 |
| S12 | 14 | R15 | Q15 |
| S13 | 13 | R18 | Q18 |
| S14 | 16 | R19 | Q19 |

### U3 (MC14514B)

| Output | Chip pin | Resistor | SCR |
| ---: | ---: | --- | --- |
| S0 | 11 | R36 | Q36 |
| S1 | 9 | R38 | Q38 |
| S2 | 10 | R44 | Q44 |
| S3 | 8 | R49 | Q49 |
| S4 | 7 | R48 | Q48 |
| S5 | 6 | R37 | Q37 |
| S6 | 5 | R32 | Q32 |
| S7 | 4 | R20 | Q20 |
| S8 | 18 | R42 | Q42 |
| S9 | 17 | R41 | Q41 |
| S10 | 20 | R40 | Q40 |
| S11 | 19 | R39 | Q39 |
| S12 | 14 | R33 | Q33 |
| S13 | 13 | R30 | Q30 |
| S14 | 16 | R31 | Q31 |

### U4 (MC14514B)

| Output | Chip pin | Resistor | SCR |
| ---: | ---: | --- | --- |
| S0 | 11 | R57 | Q57 |
| S1 | 9 | R50 | Q50 |
| S2 | 10 | R51 | Q51 |
| S3 | 8 | R54 | Q54 |
| S4 | 7 | R55 | Q55 |
| S5 | 6 | R60 | Q60 |
| S6 | 5 | R59 | Q59 |
| S7 | 4 | R58 | Q58 |
| S8 | 18 | R56 | Q56 |
| S9 | 17 | R46 | Q46 |
| S10 | 20 | R52 | Q52 |
| S11 | 19 | R53 | Q53 |
| S12 | 14 | R47 | Q47 |
| S13 | 13 | R43 | Q43 |
| S14 | 16 | R45 | Q45 |

The `R18` label of U2 S13 is written over another digit and reads `R18`; the SCR column prints `Q18` on that line. U2 S7/S8 read R25 and R24, and U3/U4 S9 read R41 and R46: these are the two pairs most easily transposed. The sixteenth output (S15) of each chip is not drawn.
