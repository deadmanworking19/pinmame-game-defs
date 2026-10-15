# Seawitch complete option assignments and setting tables

Source: manual PDF pages 11-15. Complete printed option regions, visually checked. Grouped/merged assignment cells are represented once with their printed range; settings tables retain printed column order. Dotted leaders and wrapping are normalized. Page 11 assignment prints Coin Chute No.1 for S9-12; the chute table on page 12 confirms that the first physical chute uses those bits, while S1-4 belong to chute 2.

| SWITCH | SEAWITCH SWITCH ASSIGNMENT |
| --- | --- |
| 32,31 | Special Award [one grouped cell] |
| 30 | Maximum Added Extra Balls |
| 29 | Minimum Added Extra Balls |
| 28,27,26,25 | Coin Chute No. 3 [one grouped cell] |
| 24,23 | Extra Ball Alternation [one grouped cell] |
| 22 | Special Replay Limit |
| 21 | Match Feature |
| 20 | Credit Display |
| 19,18 | Max Credits [one grouped cell] |
| 17 | Special Alternation |
| 16,15 | High Game To Date Feature [one grouped cell] |
| 14 | Background Sound |
| 13 | Not Used |
| 12 thru 9 | Coin Chute No. 1 [one grouped cell] |
| 8 | Special on (6X,7X or 7X) |
| 7 | Ball Per Game (3 or 5) |
| 6 | High Score Feature |
| 5 | Not Used |
| 4 thru 1 | Coin Chute No. 2 [one grouped cell] |

## Credits/coin, page 12

Bit column order is 28,27,26,25 for chute3 (RED-WHITE), 4,3,2,1 for chute2 (BRN-WHITE), and 12,11,10,9 for chute1 (BLU). The same printed settings apply to all three; this is one shared table, not three independently printed copies.

| Four switches, printed order | CREDITS | COINS | SEQUENCE OF CREDITS PER COIN 1,2,3,4 |
| --- | ---: | ---: | --- |
| OFF OFF OFF OFF | 1 | 1 [merged cell] | [blank] |
| OFF OFF OFF ON | 2 | 1 [merged cell repeated] | [blank] |
| OFF OFF ON OFF | 3 | 1 [merged cell repeated] | [blank] |
| OFF OFF ON ON | 4 | 1 [merged cell repeated] | [blank] |
| OFF ON OFF OFF | 5 | 1 [merged cell repeated] | [blank] |
| OFF ON OFF ON | 6 | 1 [merged cell repeated] | [blank] |
| OFF ON ON OFF | 7 | 1 [merged cell repeated] | [blank] |
| OFF ON ON ON | 8 | 1 [merged cell repeated] | [blank] |
| ON OFF OFF OFF | 14 | 1 [merged cell repeated] | [blank] |
| ON OFF OFF ON | 1 | 2 | 0,1,[blank],[blank] |
| ON OFF ON OFF | 3 | 2 | 1,2,[blank],[blank] |
| ON OFF ON ON | 5 | 2 | 0,5,[blank],[blank] |
| ON ON OFF OFF | 7 | 2 | 0,7,[blank],[blank] |
| ON ON OFF ON | 3 | 4 | 0,1,0,2 |
| ON ON ON OFF | 5 | 4 | 1,1,1,2 |
| ON ON ON ON | 7 | 4 | 1,2,1,3 |

Printed notes: same multiple-coin pricing combines coins from identically adjusted chutes; credit sequence resets on credit-button press or when points are scored.

## Game setting tables, pages 13-15

| Feature | Printed switch order | Setting | Result |
| --- | --- | --- | --- |
| HIGH SCORE FEATURE | 6 | OFF | Extra Ball (Works with #29 and #30) |
| HIGH SCORE FEATURE | 6 | ON | Replay |
| BALL PER GAME | 7 | OFF | 3 |
| BALL PER GAME | 7 | ON | 5 |
| SPECIAL on, BONUS RESET | 8 | OFF | SPECIAL on 7X; BONUS resets to 3X at 7X |
| SPECIAL on, BONUS RESET | 8 | ON | SPECIAL on 6X or 7X; BONUS resets to 3X at 6X or 7X |
| BACKGROUND SOUND | 14 | OFF | OFF |
| BACKGROUND SOUND | 14 | ON | ON |
| HIGH GAME TO DATE FEATURE | 16,15 | OFF OFF | Novelty |
| HIGH GAME TO DATE FEATURE | 16,15 | OFF ON | 1 Free Game |
| HIGH GAME TO DATE FEATURE | 16,15 | ON OFF | 2 Free Games |
| HIGH GAME TO DATE FEATURE | 16,15 | ON ON | 3 Free Games |
| ALTERNATING SPECIAL LITE | 17 | ON | RUN-WAY SPECIAL lite always on |
| ALTERNATING SPECIAL LITE | 17 | OFF | Alternating RUN-WAY SPECIAL lite |
| MAXIMUM CREDITS | 19,18 | OFF OFF | 10 |
| MAXIMUM CREDITS | 19,18 | OFF ON | 15 |
| MAXIMUM CREDITS | 19,18 | ON OFF | 25 |
| MAXIMUM CREDITS | 19,18 | ON ON | 40 |
| CREDIT DISPLAY | 20 | ON | YES |
| CREDIT DISPLAY | 20 | OFF | NO |
| MATCH FEATURE | 21 | ON | ON |
| MATCH FEATURE | 21 | OFF | OFF |
| NO. OF SPECIALS | 22 | OFF | 1 Per Ball |
| NO. OF SPECIALS | 22 | ON | 1 Per Game |
| PLAYFIELD EXTRA BALL | 23,24 | OFF OFF | Completely off |
| PLAYFIELD EXTRA BALL | 23,24 | ON OFF | Left on,both off,right on,both off,repeat |
| PLAYFIELD EXTRA BALL | 23,24 | OFF ON | Alternate |
| PLAYFIELD EXTRA BALL | 23,24 | ON ON | Both on,both off |
| MINIMUM ADDED EXTRA BALLS | 29 | OFF | Only 1 stored in memory |
| MINIMUM ADDED EXTRA BALLS | 29 | ON | Works with Switch 30 |
| EXTRA BALL (WITH MEMORY), S6 OFF and S29 ON | 30 | OFF | 3 maximum |
| EXTRA BALL (WITH MEMORY), S6 OFF and S29 ON | 30 | ON | 5 maximum |
| SPECIAL AWARD | 31,32 | OFF OFF | No Award |
| SPECIAL AWARD | 31,32 | OFF ON | Extra Ball |
| SPECIAL AWARD | 31,32 | ON OFF | 100,000 Points |
| SPECIAL AWARD | 31,32 | ON ON | Replay |

Page 11: the thirty-two physical option switches are in four sixteen-lead packages S1-8,S9-16,S17-24,S25-32 in the backbox MPU; ON is marked. S33 is a separate pushbutton. These settings are operator options, not fixed default rules.
