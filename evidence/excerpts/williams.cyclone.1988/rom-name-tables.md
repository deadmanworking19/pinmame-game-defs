# Cyclone - ROM lamp, switch and coil name tables

Decoded by `tools/cyclone_rom_name_tables.py` from the user-authorized local ROM archives; no ROM bytes are
reproduced. Every name is a fixed 14-byte record in the 32 KiB **U27** program ROM (mapped at 0x8000): seven
characters for the player 1 display followed by seven for the player 2 display, which is how the Single Lamps,
Switch Levels and Coil tests print them. A byte with bit 7 set is the character in its low seven bits followed by
the display's period segment (shown as `.`). The switch records are read in place; the coil and lamp names are
read through the ROM's own big-endian pointer tables, so a lamp that shares a switch's name points into the
switch table. Entries show the two halves joined by one space with padding trimmed. The three game ROMs decode
to identical text at identical offsets.

| Driver | ROM archive SHA-256 | ROM member | Member SHA-256 | Lamp pointers | Switch table | Coil pointers |
| --- | --- | --- | --- | --- | --- | --- |
| cycln_l5 | `8e1af710ea8e9c8b606c14221dfd418d5debd126c44a98d6f1c1aa2ab90516ff` | cycl_u27.l5 | `0e04287e7d874917dcdc622ebca3782d350317355d4f55494079ca314236b731` | 0x078a | 0x0ae2 | 0x0e62 |
| cycln_l4 | `2cc2625a8e5b44e46ab71a9848aa2679f842c2b42b91f9fb4fbab08baf9a41e3` | cycl_u27.l4 | `ed6852ebf5bf8525aae37c53a6b3206dab1ad52b771f56ec3c1e82cc5344d058` | 0x078a | 0x0ae2 | 0x0e62 |
| cycln_l1 | `e2d5a524287d35f26257ab33bfc033729036f2efb5652193b122f2e4a700beba` | cycl_u27.l1 | `bd14e2a2fc4c11732d8cef5029198ea373e19a1928e68819a68aed3dca90d1d8` | 0x078a | 0x0ae2 | 0x0e62 |

## Lamp names (public lamp address = pointer number)

| Lamp | Record | ROM text |
| --- | --- | --- |
| 1 | 0x080a | HOLD |
| 2 | 0x0811 | BONUS |
| 3 | 0x081f | DOUBLE |
| 4 | 0x0826 | SCORES |
| 5 | 0x0834 | CYCLONE 50K |
| 6 | 0x0842 | CYCLONE 100K |
| 7 | 0x0850 | CYCLONE GATEBON. |
| 8 | 0x085e | RIDE COMET |
| 9 | 0x086c | FERRIS WHEEL |
| 10 | 0x087a | ADVANCE X |
| 11 | 0x0888 | DUCKS 25K |
| 12 | 0x0896 | DUCKS 50K |
| 13 | 0x08a4 | DUCKS LIT EX.B. |
| 14 | 0x0b98 (switch 14's record) | TOP LANE 1 |
| 15 | 0x0ba6 (switch 15's record) | TOP LANE 2 |
| 16 | 0x0bb4 (switch 16's record) | TOP LANE 3 |
| 17 | 0x08b2 | RIDE AGAIN |
| 18 | 0x08c0 | SPINS M. WHEEL |
| 19 | 0x0bde (switch 19's record) | DUCKS TOP |
| 20 | 0x0bec (switch 20's record) | DUCKS MIDDLE |
| 21 | 0x0bfa (switch 21's record) | DUCKS BOTTOM |
| 22 | 0x0c08 (switch 22's record) | B. TOSS TOP |
| 23 | 0x0c16 (switch 23's record) | B. TOSS MIDDLE |
| 24 | 0x0c24 (switch 24's record) | B. TOSS BOTTOM |
| 25 | 0x0dba (switch 53's record) | LEFT OUTLANE |
| 26 | 0x0dc8 (switch 54's record) | RIGHT OUTLANE |
| 27 | 0x08ce | COMET 20K |
| 28 | 0x08dc | COMET 40K |
| 29 | 0x08ea | COMET 60K |
| 30 | 0x08f8 | COMET 80K |
| 31 | 0x0906 | COMET 100K |
| 32 | 0x0914 | COMET MILLION |
| 33 | 0x0922 | M. WHEEL TOP   1 |
| 34 | 0x0930 | M. WHEEL 2 |
| 35 | 0x093e | M. WHEEL 3 |
| 36 | 0x094c | M. WHEEL 4 |
| 37 | 0x095a | M. WHEEL RIGHT 5 |
| 38 | 0x0968 | M. WHEEL 6 |
| 39 | 0x0976 | M. WHEEL 7 |
| 40 | 0x0984 | M. WHEEL 8 |
| 41 | 0x0992 | M. WHEEL BOTTOM9 |
| 42 | 0x09a0 | M. WHEEL 10 |
| 43 | 0x09ae | M. WHEEL 11 |
| 44 | 0x09bc | M. WHEEL 12 |
| 45 | 0x09ca | M. WHEEL LEFT 13 |
| 46 | 0x09d8 | M. WHEEL 14 |
| 47 | 0x09e6 | M. WHEEL 15 |
| 48 | 0x09f4 | M. WHEEL 16 |
| 49 | 0x0a02 | 2 X |
| 50 | 0x0a48 | 7 X |
| 51 | 0x0a3a | 6 X |
| 52 | 0x0a2c | 5 X |
| 53 | 0x0a1e | 4 X |
| 54 | 0x0a10 | 3 X |
| 55 | 0x0a56 | BACKGLS. MYSTERY |
| 56 | 0x0a64 | BACKGLS. WHEEL |
| 57 | 0x0a72 | BACKGLS. 0.5 MIL. |
| 58 | 0x0a80 | BACKGLS. 1.0 MIL. |
| 59 | 0x0a8e | BACKGLS. 1.5 MIL. |
| 60 | 0x0a9c | BACKGLS. 2.0 MIL. |
| 61 | 0x0aaa | BACKGLS. 2.5 MIL. |
| 62 | 0x0ab8 | BACKGLS. 3.0 MIL. |
| 63 | 0x0ac6 | BACKGLS. 3.5 MIL. |
| 64 | 0x0ad4 | BACKGLS. 4.0 MIL. |

## Switch names (public switch address = record number)

| Switch | ROM text |
| --- | --- |
| 1 | PLUMB TILT |
| 2 | G. SCORE BOARD |
| 3 | CREDIT BUTTON |
| 4 | RIGHT COIN SW. |
| 5 | CENTER COIN SW. |
| 6 | LEFT COIN SW. |
| 7 | SLAM TILT |
| 8 | HI.SCORE RESET |
| 9 | PLAYFLD. TILT |
| 10 | OUTHOLE |
| 11 | SCORE SPOOK H. |
| 12 | NOT USED |
| 13 | BOMERNG. KICKER |
| 14 | TOP LANE 1 |
| 15 | TOP LANE 2 |
| 16 | TOP LANE 3 |
| 17 | FERRIS WHEEL |
| 18 | C. DROP TARGET |
| 19 | DUCKS TOP |
| 20 | DUCKS MIDDLE |
| 21 | DUCKS BOTTOM |
| 22 | B. TOSS TOP |
| 23 | B. TOSS MIDDLE |
| 24 | B. TOSS BOTTOM |
| 25 | SHOOTER LANE |
| 26 | SHUTTLE KICKER |
| 27 | SHUTTLE BOT 25K |
| 28 | SHUTTLE 100K |
| 29 | SHUTTLE 25K |
| 30 | SHUTTLE TOP  5K |
| 31 | ENTER COMET |
| 32 | SCORE COMET |
| 33 | NOT USED |
| 34 | SCORE CYCLONE |
| 35 | 10 PT. R. BOT. |
| 36 | 10 PT. R. MID. |
| 37 | 10 PT. R. TOP |
| 38 | NOT USED |
| 39 | NOT USED |
| 40 | NOT USED |
| 41 | M. WHEEL H. OPTO |
| 42 | NOT USED |
| 43 | NOT USED |
| 44 | NOT USED |
| 45 | NOT USED |
| 46 | NOT USED |
| 47 | NOT USED |
| 48 | NOT USED |
| 49 | NOT USED |
| 50 | NOT USED |
| 51 | NOT USED |
| 52 | NOT USED |
| 53 | LEFT OUTLANE |
| 54 | RIGHT OUTLANE |
| 55 | LEFT RETURN |
| 56 | RIGHT RETURN |
| 57 | LEFT FLIPPER |
| 58 | RIGHT FLIPPER |
| 59 | SPOT B. TOSS |
| 60 | LEFT JET |
| 61 | RIGHT JET |
| 62 | BOTTOM JET |
| 63 | LEFT KICKER |
| 64 | RIGHT KICKER |

## Coil-test names (two pointers per step)

Steps 01-08 name the A-side load first and the C-side load second; from step 09 the second pointer is the
blank record. The ROM's Coil Test pairs each displayed step with the public solenoid it pulses; that
pairing is in the runtime evidence, not in this table.

| Step | First name | Second name |
| --- | --- | --- |
| 01 | OUTHOLE | L.FERRIS JACKPOT |
| 02 | NOT USED | R.FERRIS C. TEETH |
| 03 | SHUTTLE KICKER | BCK. MID. L. EYE |
| 04 | BOMERNG. KICKER | CATS F.L. B. FIREW. |
| 05 | C. DROP TARGET | DUCK F.L. R. FIREW. |
| 06 | NOT USED | FERRIS FLASHER |
| 07 | KNOCKER | TOP RIT. R. EYE |
| 08 | NOT USED | SPOOK H. L. FIREW. |
| 09 | SPIN M.W. FLASHER | (blank) |
| 10 | PLAYFLD. G.I. | (blank) |
| 11 | BACKBOX G.I. | (blank) |
| 12 | ApC SELECT | (blank) |
| 13 | BOMERNG. 1251 | (blank) |
| 14 | BOMERNG. 1251 | (blank) |
| 15 | BOMERNG. 1251 | (blank) |
| 16 | FERRIS WHEEL | (blank) |
| 17 | LEFT JET | (blank) |
| 18 | LEFT KICKER | (blank) |
| 19 | RIGHT JET | (blank) |
| 20 | RIGHT KICKER | (blank) |
| 21 | BOTTOM JET | (blank) |
| 22 | NOT USED | (blank) |

Normalization: each seven-character half is trimmed and the halves are joined with one space; spaces inside a half are kept.
