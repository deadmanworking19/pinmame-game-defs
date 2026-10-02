# Star Gazer — LDA lamp chart ("LDA LIGHT LOCATION")

Transcribed from `Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf`, PDF page 2 (the playfield sheet, right-hand table) and compared row by row with the second copy printed on PDF page 4 (the lamp-driver schematic, captioned "LDA LIGHT LOCATION"). The two copies print the same values in every row and column except one cell: the pin of the `R. OUT L` row, which the page 2 copy prints as `6` and the page 4 copy prints as a bold glyph that reads `5`. Because they are two copies of one table they count as one source. The table has five printed columns, `DESCRIPTION`, `WIRE COLOR`, `JACK LDA`, `PIN NO.` and `TRANSISTOR`, and the foot note `NOTE: * INDICATES MCR106-1 TRANSISTOR  ALL OTHER TRANSISTORS 2N5060`.

Normalisation disclosed: the typewriter-style `Q` in the transistor column often looks like a `0` in the scan (`060`, `016`, `09`); it is read as `Q` throughout because every value is a Q number from 1 to 60. The sheet prints no lamp locations, bulb counts or coordinates; the table lists one row per lamp circuit. The description `SHOOT AGAIN` appears twice with the same transistor `Q3` and different jack pins, as printed. Sixty rows are printed; fifty-eight distinct transistor numbers appear, because `Q3` is printed on both `SHOOT AGAIN` rows and `Q27` on two different rows, and `Q6` and `Q24` do not appear.

| DESCRIPTION | WIRE COLOR | JACK LDA | PIN NO. | TRANSISTOR |
| --- | --- | --- | ---: | --- |
| AQUARIUS | PUR | J1 | 17 | Q13 |
| ARIES | B-R | J3 | 19 | Q44 |
| BONUS 1K | BLU-W | J1 | 23 | Q8 * |
| BONUS 2K | R-G | J1 | 3 | Q35 * |
| BONUS 3K | Y-BLU | J3 | 17 | Q49 * |
| BONUS 4K | W-BLU | J3 | 11 | Q54 * |
| BONUS 5K | GREY-O | J1 | 14 | Q9 * |
| BONUS 6K | PUR-W | J1 | 2 | Q34 * |
| BONUS 7K | R-B | J3 | 16 | Q48 * |
| BONUS 8K | O | J3 | 9 | Q55 * |
| BONUS 9K | GREY-Y | J1 | 15 | Q10 * |
| BONUS 10K | GREY-BLU | J1 | 10 | Q22 * |
| BONUS 11K | W | J3 | 23 | Q37 * |
| BONUS 12K | G | J3 | 3 | Q60 * |
| BONUS 12,000 | PUR | J2 | 8 | Q23 * |
| BONUS 24,000 | GREY | J2 | 9 | Q40 * |
| CANCER | BLU-R | J1 | 1 | Q29 |
| CAPRICORN | G-R | J3 | 12 | Q50 |
| GAME OVER | O-G | J2 | 11 | Q33 * |
| GEMINI | BRN-B | J1 | 18 | Q14 * |
| HIGH SCORE TO DATE | GREY-O | J2 | 22 | Q16 * |
| L. BANK | G | J2 | 16 | Q5 * |
| L. B 1 | BLU | J2 | 15 | Q19 |
| L. B 3 STAR ROLL | B | J2 | 2 | Q31 |
| L. B 3 STAR ROLL-OVER | B-G | J3 | 21 | Q42 * |
| L OUT L | BLU-W | J2 | 7 | Q43 |
| L. R B 4 STAR ROLL-OVER | GREY-B | J3 | 10 | Q56 * |
| L. SPINNER LITE | B-Y | J2 | 5 | Q52 |
| L. 3 FROM TOP STAR ROLL-OVER | BLU-O | J1 | 5 | Q27 |
| LEO | B | J3 | 26 | Q36 |
| LIBRA | GREY-G | J1 | 19 | Q12 |
| MATCH | GREY-Y | J2 | 1 | Q45 |
| PISCES | G-B | J1 | 8 | Q28 |
| R. BANK L | G-O | J2 | 20 | Q18 |
| R. OUT L | Y | J2 | 6 | Q30 |
| R. SPINNER | W | J2 | 23 | Q15 * |
| SAGITTARIUS | R-Y | J3 | 25 | Q38 |
| SCORPIO | GREY | J1 | 9 | Q27 |
| SHOOT AGAIN | GREY-R | J1 | 26 | Q3 * |
| SHOOT AGAIN | GREY-R | J2 | 21 | Q3 * |
| SPINNER & BANK 500 | B | J1 | 16 | Q11 |
| SPINNER & BANK 1000 | Y-G | J1 | 7 | Q26 |
| SPINNER & BANK 1500 | O-W | J3 | 27 | Q32 |
| SPINNER & BANK 2000 | R-W | J3 | 4 | Q59 |
| SPINNER & BANK 2500 | B-W | J1 | 28 | Q4 |
| SPINNER & BANK 3000 | BRN-R | J1 | 6 | Q25 |
| SPINNER & BANK 3500 | W-BLU | J1 | 13 | Q20 |
| SPINNER & BANK 4000 | Y-BLU | J3 | 2 | Q58 |
| STAR ROLL-OVER BOTTOM | BRN-BLU | J1 | 24 | Q1 * |
| TAURUS | W-B | J3 | 15 | Q51 |
| TILT | GREY-B | J2 | 10 | Q47 * |
| VIRGO | R-G | J3 | 1 | Q57 |
| ZODIAC TARGET 1000 | PUR-B | J1 | 25 | Q2 * |
| ZODIAC TARGET 2000 | B-O | J1 | 11 | Q17 * |
| ZODIAC TARGET 3000 | G-B | J3 | 20 | Q41 * |
| ZODIAC TARGET 4000 | R-BLU | J3 | 18 | Q46 |
| 1 X | GREY-G | J2 | 13 | Q7 |
| 2 X | W-Y | J2 | 12 | Q21 |
| 3 X | PUR-B | J2 | 4 | Q39 |
| 4 X | B-W | J2 | 3 | Q53 |

## Rows that need a note

- `L. 3 FROM TOP STAR ROLL-OVER` (`BLU-O`, `J1` pin 5) prints `Q27`, the same transistor the `SCORPIO` row (`GREY`, `J1` pin 9) prints. The lamp-driver schematic on PDF page 4 draws `J1` pin 5 at transistor `Q24`, and the same board's pin 6 at `Q25`; the chart's `Q27` on the `L. 3 FROM TOP` row is therefore a misprint of `Q24` (a wiring-detail disagreement about a transistor designator, not about the lamp or its connector pin).
- `R. OUT L` (`Y`, `J2`, `Q30`): the page 2 copy prints pin `6`; the page 4 copy prints a bold glyph that reads `5`. The lamp-driver schematic on page 4 draws `J2` pin 6 at `Q30` (and pin 5 at `Q52`, the `L. SPINNER LITE` row), so `6` is the structured reading and the page 4 glyph is read as a misprint of it; both readings are kept here (a wiring-detail disagreement between two copies of one table).
- `SHOOT AGAIN` is listed twice, `J1` pin 26 and `J2` pin 21, both on `Q3` (marked `*`); one transistor drives both connector pins.
