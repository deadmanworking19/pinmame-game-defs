# Star Gazer — MPU option-switch assignment

Transcribed from `Stern_1980_Star_Gazer_Manual.pdf`, PDF page 11 (printed page 10), the "STAR GAZER SWITCH ASSIGNMENT" chart (drawing number `12C-266-11`), read from the rendered scan. The page text above the chart says the thirty-two switches sit on the MPU module in the back box, in four sixteen-lead packages numbered S1-8, S9-16, S17-24 and S25-32, and that the "On" position is marked on the assembly.

The chart lists each switch number beside its function, with two printed columns, ON and OFF, on the right. A row whose ON and OFF cells hold arrows is decoded by the small table drawn beside it. Rows are listed here from the top of the printed chart (switch 32) to the bottom (switch 1).

| switch | printed function | ON | OFF |
| ---: | --- | --- | --- |
| 32 | Special Award | decoded by table | decoded by table |
| 31 | Special Award | decoded by table | decoded by table |
| 30 | Extra Ball Award | On | Off |
| 29 | Bottom Banks Spot Next Zodiac | Lib. | Cons. |
| 28 | Coin Chute #3 | See Catalog | |
| 27 | Coin Chute #3 | See Catalog | |
| 26 | Coin Chute #3 | See Catalog | |
| 25 | Coin Chute #3 | See Catalog | |
| 24 | Special on Complete Zodiac | decoded by table | decoded by table |
| 23 | Special—Alternation | Lib. | Cons. |
| 22 | Special on Complete Zodiac | decoded by table | decoded by table |
| 21 | Match Feature | Yes | No |
| 20 | Credit Display | Yes | No |
| 19 | Maximum Credits | decoded by table | decoded by table |
| 18 | Maximum Credits | decoded by table | decoded by table |
| 17 | Extra Ball Lite Control | Lib. | Cons. |
| 16 | High Game To Date Features | decoded by table | decoded by table |
| 15 | High Game To Date Features | decoded by table | decoded by table |
| 14 | Maximum Add-A-Balls | 6 | 3 |
| 13 | Add-A-Ball (Memory) | On | Off |
| 12 | Coin Chute #2 | See Catalog | |
| 11 | Coin Chute #2 | See Catalog | |
| 10 | Coin Chute #2 | See Catalog | |
| 9 | Coin Chute #2 | See Catalog | |
| 8 | Background Sound | Off | On |
| 7 | Ball Per Game | 5 | 3 |
| 6 | High Score Feature | Replay | X Ball |
| 5 | Flashing Value Lite Speed | Slow | Fast |
| 4 | Coin Chute #1 | See Catalog | |
| 3 | Coin Chute #1 | See Catalog | |
| 2 | Coin Chute #1 | See Catalog | |
| 1 | Coin Chute #1 | See Catalog | |

The row "Ball Per Game" is drawn with a dotted leader across both columns, and its ON and OFF cells hold `5` and `3`.

## Decoding tables printed beside the rows

Special Award (switches 32 over 31):

| | NONE | X BALL | 100K | REPLAY |
| --- | --- | --- | --- | --- |
| 32 | OFF | ON | OFF | ON |
| 31 | OFF | OFF | ON | ON |

Special on Complete Zodiac (switches 24 over 22). The printed header cells read `DIP`, `4th`, `3rd`, `2nd`, `2nd`:

| DIP | 4th | 3rd | 2nd | 2nd |
| --- | --- | --- | --- | --- |
| 24 | OFF | OFF | ON | ON |
| 22 | OFF | ON | OFF | ON |

Maximum Credits (switches 19 over 18):

| | 10 | 15 | 25 | 40 |
| --- | --- | --- | --- | --- |
| 19 | OFF | OFF | ON | ON |
| 18 | OFF | ON | OFF | ON |

High Game To Date Features (switches 16 over 15):

| | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| 16 | OFF | OFF | ON | ON |
| 15 | OFF | ON | OFF | ON |

## Where the printed text and this chart disagree

The same manual's explanatory pages (PDF pages 9 and 12 to 15) describe several of these switches in prose and tables of their own. Three of those descriptions do not agree with the chart above:

- Special on Complete Zodiac: the prose tables print the 22/24 combinations in the order `2nd` (22 OFF, 24 OFF), `2nd` (22 ON, 24 OFF), `3rd` (22 OFF, 24 ON), `4th` (22 ON, 24 ON), which does not match the chart's `4th`, `3rd`, `2nd`, `2nd` columns.
- Special alternation (switch 23): the prose says ON makes all three special positions alternate (the conservative setting) and OFF leaves the target-bank position lit while the outlanes alternate (the liberal setting), the opposite of the chart's `Lib.` and `Cons.` cells.
- Add-A-Ball: the prose says switches 13 and 14 select how many add-a-balls the memory stores (1 only, 3, or 5), where the chart calls switch 14 "Maximum Add-A-Balls" with 6 or 3.

These are option-menu semantics of a coin-operated game and do not change any device address; the chart is transcribed as printed and the prose is not relied on for anything here.
