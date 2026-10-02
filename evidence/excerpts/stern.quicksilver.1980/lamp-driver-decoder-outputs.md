Source: `Stern_1980_Quicksilver_Lamp_Driver_Schematic.jpg` (IPDB machine 1895, "Lamp Driver Schematic", a 2330x1555 pixel grayscale JPEG scan, 300 dpi, drawing `12B-432-S-116`, `SHEET #1 OF 3`). Title block, verbatim: `STERN ELECTRONICS INC.`, `1725 DIVERSEY BLVD. CHICAGO 60614`, `LAMP DRIVER SCHEMATIC`, `FOR` with the word `CHEETAH` struck through by hand and `Quicksilver` written beside it. The sheet was drafted for a sister game and relabelled for this one by hand, so every cell below is read from the relabelled sheet, not carried from any other game. The four 4-to-16 decoder/latch chips `U1`-`U4` (printed `MC14514B`) on the left of the circuit. Each chip's four inputs are the lamp address lines `AD0`-`AD3` (pins 2, 3, 21, 22), its inhibit/data pin (pin 23) is one of the lamp data lines `PD0`-`PD3`, and its fifteen used outputs go through 2.2k resistors to the gates of the SCRs. Chip `U1` reads `PD0` and chip `U2` reads `PD1` as printed on the sheet; `U3` and `U4` take `PD2` and `PD3` in the same order. The sixteenth output (S15, pin 15) is not drawn.

Each output line carries a resistor labelled `R<n>` and ends at the gate of the SCR `Q<n>`; the resistor and SCR numbers match on every line that was read. The S-index is the printed output number beside the chip pin. For `U3` and `U4` the three last outputs (S12, S13, S14, pins 14, 13, 16) are drawn above S0 rather than below S11.

The sheet cell for a line is the one whose resistor label sits directly above that line's right-hand end. The S7/S8 outputs of `U2` read R25 and R24, and the S9 output of `U3` and `U4` read R41 and R46; these two pairs are the ones a reader is most likely to transpose.

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
