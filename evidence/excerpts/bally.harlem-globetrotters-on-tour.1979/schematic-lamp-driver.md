# Harlem Globetrotters On Tour - A5 lamp driver schematic, connector function lists

Transcribed from `Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf`, PDF page 44, "A5 LAMP DRIVER SCHEMATIC, HARLEM GLOBE TROTTERS", part no. W-1182-18c (title block: game "#1161-E"), read from a 206 dpi render of the scan. The sheet draws the four MC14514CP decoders U1-U4 (E-620-37) driving the SCRs (Q1-Q60) and brings their outputs to connectors J1 and J3 ("TO PLAYFIELD") and J2 ("TO BACK BOX"). The three connector lists are transcribed whole, in the order the sheet prints them (top to bottom), with the pin number first; the circled numbers are printed as ① to ⑤. The sheet's SCR-to-pin wiring is a drawing and is not transcribed here.

## J1 (TO PLAYFIELD)

| pin | function |
| ---: | --- |
| 22 | N/U |
| 21 | N/U |
| 20 | KEY |
| 18 | 1K BONUS |
| 19 | 5K BONUS |
| 17 | 9K BONUS |
| 23 | SPINNERS ① BOTTOM |
| 14 | SPINNERS ⑤ TOP |
| 15 | LEFT SIDE SPINNER 100 |
| 16 | SAUCER "G" |
| 28 | SAUCER "E" |
| 24 | SIDE TARGET ⑤ TOP |
| 25 | SIDE TARGET ① BOTTOM |
| 26 | CENTER "E" |
| 27 | 2 X BONUS |
| 1 | 2 K BONUS |
| 9 | 6 K BONUS |
| 8 | DUNK SHOT 5K |
| 3 | SPINNERS ② |
| 2 | DUNK SHOT OPENS GATE |
| 10 | LEFT SIDE SPINNER 200 |
| 7 | SAUCER "L" |
| 6 | DUNK SHOT SPECIAL |
| 5 | SIDE TARGET ④ |
| 11 | BOTTOM THUMPER BUMPER |
| 13 | 25K LEFT OUTLANE |
| 4 | N/U |
| 12 | 3X BONUS |

## J2 (TO BACK BOX)

| pin | function |
| ---: | --- |
| 21 | N/U |
| 13 | N/U |
| 22 | BALL IN PLAY |
| 16 | 10K BONUS |
| 14 | CENTER "G" |
| 8 | MATCH |
| 12 | N/U |
| 23 | HIGH SCORE TO DATE |
| 20 | 20 K BONUS |
| 15 | CENTER "L" |
| 11 | GAME OVER |
| 6 | 30 K BONUS |
| 2 | CENTER "O" |
| 9 | SHOOT AGAIN |
| 4 | N/U |
| 5 | N/U |
| 3 | N/U |
| 10 | TILT |
| 7 | 40 K BONUS |
| 1 | CENTER "B" |
| 17 | N/U |
| 18 | KEY |
| 19 | N/U |

## J3 (TO PLAYFIELD)

| pin | function |
| ---: | --- |
| 26 | 3K BONUS |
| 25 | 7K BONUS |
| 19 | RIGHT SPIN. ADV. BONUS |
| 17 | SPINNERS ③ |
| 16 | GATE OPEN W/LIT |
| 23 | LEFT SIDE SPINNER 1K |
| 27 | SAUCER "O" |
| 21 | SIDE TARGET ③ |
| 20 | LEFT AND RIGHT THUMPER BUMPER |
| 22 | S.P.S.A. |
| 24 | 5 X BONUS |
| 1 | 4 K BONUS |
| 12 | 8 K BONUS |
| 15 | LEFT SPIN. ADV. BONUS |
| 11 | SPINNERS ④ |
| 9 | TARGET SAUCER 25K |
| 3 | LEFT SIDE SPINNER 2K |
| 4 | SAUCER "B" |
| 2 | SAUCER TARGET SPECIAL |
| 10 | SIDE TARGET ② |
| 18 | DUNK SHOT EXTRA BALL |
| 13 | CREDIT INDICATOR |
| 14 | G-L-O-B-E SPECIAL |
| 5 | N/U |
| 6 | N/U |
| 7 | N/U |
| 8 | KEY |
| 28 | N/U |

The last five J3 pin numbers are overprinted in the scan; they read 5, 6, 7, 8 and 28. Two wires of the lower J1 group are drawn joined by dots to J2 lines (the sheet ties some J1 and J2 pins to one SCR output); which SCR drives which pin is read from the drawing, not from these lists.

Sheet notes:

> 1. *SCRs ARE MCR-106-1 (E-585-29), ALL OTHERS ARE 2N5060 (E-585-14) OR EQUIVALENTS.
> 2. ALL RESISTORS ARE 1/4W, ± 5%.
> 3. PREFIX ALL REFERENCE DESIGNATIONS WITH "A5".
> 4. * INDICATES "AID" TEST POINT
