Source: `Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf` (IPDB machine 249), PDF page 2, drawing `12B-432-S-121`, `LAMP DRIVER SCHEMATIC FOR BIG GAME` (stored sideways; read rotated a quarter turn clockwise). The three connector blocks `J1`, `J2` and `J3` between the SCR column and the lamp list. Each pin is drawn as an arrow with its pin number and the label of the SCR that drives it; a small triangle before a label marks an MCR106-1 part (note 1 of the sheet), the others are 2N5060. Some SCRs appear on more than one pin. Every row of every block is listed in printed order, read from the render at native resolution and at twice that size.

Two J1 rows print hand-written pin numbers that collide with other rows of the same block, so they are listed apart, below the J1 table: the row for `Q24` prints a flat-topped figure that reads as `3` or `5` (pin 3 is already `Q35`), and the row for `Q23` reads `14` (pin 14 is already `Q9`). J1 pins 4, 5, 20, 21 and 22 carry no other legible row.

### J1

| Pin | SCR label |
| ---: | --- |
| 18 | Q14 |
| 19 | Q12 |
| 17 | Q13 |
| 23 | Q8 |
| 14 | Q9 |
| 15 | Q10 |
| 16 | Q11 |
| 28 | Q4 |
| 24 | Q1 |
| 25 | Q2 |
| 26 | Q3 |
| 27 | Q7 |
| 1 | Q29 |
| 9 | Q27 |
| 8 | Q28 |
| 3 | Q35 |
| 2 | Q34 |
| 10 | Q22 |
| 7 | Q26 |
| 6 | Q25 |
| 11 | Q17 |
| 13 | Q20 |
| 12 | Q21 |

The two colliding rows, in printed order (`Q24` between `Q25` and `Q17`, `Q23` between `Q20` and `Q21`):

| SCR | Pin as printed | Reading |
| --- | --- | --- |
| Q24 | a flat-topped figure, `3` or `5` | 5 |
| Q23 | `14` | not settled |

The `Q24` row is read as pin 5 because the lamp list prints its one load, `"M"`, on J1 pin 5, and pin 3 belongs to `Q35`. No lamp-list row uses a J1 pin for `Q23`, whose load (`"Z-2"`) is on J2 pin 8, so its J1 pin is left unread.

### J2

| Pin | SCR label |
| ---: | --- |
| 21 | Q3 |
| 13 | Q7 |
| 22 | Q16 |
| 16 | Q5 |
| 14 | Q6 |
| 8 | Q23 |
| 12 | Q21 |
| 23 | Q15 |
| 20 | Q18 |
| 15 | Q19 |
| 11 | Q33 |
| 6 | Q30 |
| 2 | Q31 |
| 9 | Q40 |
| 4 | Q39 |
| 5 | Q52 |
| 10 | Q47 |
| 7 | Q43 |
| 1 | Q45 |
| 3 | Q53 |

### J3

| Pin | SCR label |
| ---: | --- |
| 26 | Q36 |
| 25 | Q38 |
| 19 | Q44 |
| 17 | Q49 |
| 16 | Q48 |
| 23 | Q37 |
| 27 | Q32 |
| 21 | Q42 |
| 20 | Q41 |
| 22 | Q40 |
| 24 | Q39 |
| 1 | Q57 |
| 12 | Q50 |
| 15 | Q51 |
| 11 | Q54 |
| 9 | Q55 |
| 3 | Q60 |
| 4 | Q59 |
| 2 | Q58 |
| 10 | Q56 |
| 18 | Q46 |
| 13 | Q52 |
| 14 | Q53 |

The lamp list's `"M"` row (J1 pin 5) is the only listed load that depends on either colliding row. The retained gameplay run places it independently: when the saucer collects the letters, public lamps 9, 10, 25, 26, 41, 42 and 57 flash together, the six others being the lamps of B, I, G, G, A and E, so public 25 (decoder U2 output S8, SCR Q24) is the seventh letter, M.
