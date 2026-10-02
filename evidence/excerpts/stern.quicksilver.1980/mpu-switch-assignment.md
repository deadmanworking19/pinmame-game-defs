Source: `Stern_1980_Quicksilver_Manual.pdf` (IPDB machine 1895, "English Manual [Stern Electronics]", 35 pages, a 300 dpi bilevel scan with no text layer), PDF page 9 (printed 4), paragraph VII.B and the figure headed `QUICK SILVER SWITCH ASSIGNMENT` (figure number
`12C-266-10`). The paragraph says each game has thirty-two switches on the MPU module, supplied as four sixteen-lead
packages numbered S1-8, S9-16, S17-24 and S25-32, with the `On` position marked on the assembly. The figure is a two-column
list (left list of names, right list repeated with `ON` and `OFF` meanings), read from the 300 dpi render.

Column heads of the right list: `ON` (left arrow column) and `OFF`.

| Switch | Printed assignment | ON | OFF |
| ---: | --- | --- | --- |
| 1-4 | Coin Chute #1 | See Catalog | |
| 5 | Add-a-Ball (Memory) | 3 or 5 | 1 Only |
| 6 | High Score Feature | Replay | X Ball |
| 7 | Ball Per Game | 5 | 3 |
| 8 | Maximum Add-a-Balls | 5 | 3 |
| 9-12 | Coin Chute #2 | See Catalog | |
| 13 | 5 Ball - Extra Ball Flashing Lite | Start Over | Retain |
| 14 | Background Sound | ON | OFF |
| 15-16 | High Game To Date Features | 2-bit code 0/1/2/3 | |
| 17 | Quick Extra Ball Per Game | ONCE | OPEN END |
| 18-19 | Maximum Credits | 2-bit code 10/15/25/40 | |
| 20 | Credit Display | YES | NO |
| 21 | Match Feature | YES | NO |
| 22 | Quick Extra Ball | YES | NO |
| 23-24 | Special Lite Alternation | 2-bit code 0/3/2/1 | |
| 25-28 | Coin Chute #3 | See Catalog | |
| 29 | Quick Silver Special | Start Fresh | Carry Over |
| 30 | Special Replay Limit | 1/GAME | 1/BALL |
| 31-32 | Special Award | 2-bit code NONE/X BALL/100K/REPLAY | |

The three 2-bit boxes drawn beside the list, row 1 / row 2 giving the upper and lower switch states for each code:

| Code box | Upper-numbered switch | Lower-numbered switch |
| --- | --- | --- |
| High Game To Date: `0` `1` `2` `3` | S16: OFF OFF ON ON | S15: OFF ON OFF ON |
| Maximum Credits: `10` `15` `25` `40` | S19: OFF OFF ON ON | S18: OFF ON OFF ON |
| Special Lite Alternation: `0` `3` `2` `1` | S24: OFF OFF ON ON | S23: OFF ON OFF ON |
| Special Award: `NONE` `X BALL` `100K` `REPLAY` | S32: OFF ON OFF ON | S31: OFF OFF ON ON |

Hand-read note: the Special Award row pairs are transcribed from the render as S32 `OFF ON OFF ON` over S31 `OFF OFF ON ON`.
