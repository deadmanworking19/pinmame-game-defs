# Williams Blackout (game 495) - Insert board wiring

Source: Instruction Manual and Drawing Set, PDF page 23 / printed 28, Insert Board Wiring Diagram (`INSERT BOARD WIRING`).

Connector 9J1, every pin as printed:

| 9J1 pin | Label |
|---|---|
| 1 | 6.3 VAC |
| 2 | 6.3 VAC |
| 3 | N.C. |
| 4 | 6.3 VAC |
| 5 | 6.3 VAC |
| 6 | LAMP COLUMN 7 |
| 7 | LAMP COLUMN 8 |
| 8 | LAMP ROW 1 |
| 9 | LAMP ROW 2 |
| 10 | LAMP ROW 3 |
| 11 | LAMP ROW 4 |
| 12 | LAMP ROW 5 |
| 13 | LAMP ROW 6 |
| 14 | LAMP ROW 7 |
| 15 | LAMP ROW 8 |

Lamps, each through its own series diode to its row; the column is the vertical bus the lamp's line joins:

| Row | Insert | Column | Bulbs drawn |
|---|---|---|---|
| 1 | "PLAYER 1 UP" | 8 | 1 |
| 2 | "1 CAN PLAY" | 7 | 1 |
| 2 | "PLAYER 2 UP" | 8 | 1 |
| 3 | "2 CAN PLAY" | 7 | 1 |
| 3 | "PLAYER 3 UP" | 8 | 1 |
| 4 | "3 CAN PLAY" | 7 | 1 |
| 4 | "PLAYER 4 UP" | 8 | 1 |
| 5 | "4 CAN PLAY" | 7 | 1 |
| 5 | "TILT" | 8 | 1 |
| 6 | "MATCH" | 7 | 1 |
| 6 | "GAME OVER" | 8 | 2, in parallel |
| 7 | "BALL IN PLAY" | 7 | 1 |
| 7 | "SAME PLAYER SHOOTS" | 8 | 2, in parallel |
| 8 | "HIGH SCORE" | 8 | 2, in parallel |

Column 7 rows 1 and 8 are not drawn on this board (they are playfield lamps 49 and 56 on the playfield lamp sheet).

General illumination: pins 1 and 4 (6.3 VAC) and pins 2 and 5 (6.3 VAC) feed a parallel string drawn with three bulbs and two dashed bulbs; no count is printed.
