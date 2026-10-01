# Bally Midway Special Force (game no. 0E47) — Solenoid Identification Table and Switch Assembly Identification Table

Source: `Bally_1986_Special_Force_Manual.pdf` (Operating Manual, form no. 0E47-00300-0100), PDF page 17, printed
page 1-9. Transcribed by hand from a render of that page at its native 299 ppi. Both tables are transcribed in full,
in printed order, with the printed spelling and punctuation; the playfield drawing on the left half of the page is
not transcribed.

Page heading, verbatim: `SPECIAL FORCE` / `VII`.

## SOLENOID IDENTIFICATION TABLE

The column heading is `SELF TEST # SEQUENCE`, not a controller address: the driver board publishes fifteen momentary
and four continuous outputs, and several printed entries share one driver through the game's relay multiplexing.

| SELF TEST # SEQUENCE | SOLENOID IDENTIFICATION |
| --- | --- |
| 1 | LEFT BUMPER |
| 2 | RIGHT BUMPER |
| 3 | MIDDLE BUMPER |
| 4 | LEFT SLINGSHOT |
| 5 | RIGHT SLINGSHOT |
| 6 | BRIGHT LITES 1 |
| 7 | BRIGHT LITES 2 |
| 8 | BRIGHT LITES 3 |
| 9 | BRIGHT LITES 4 |
| 10 | BRIGHT LITES 5 |
| 11 | BRIGHT LITES 6 (NOT USED) |
| 12 | BRIGHT LITES 7 (NOT USED) |
| 13 | OUTHOLE |
| 14 | KNOCKER |
| 15 | IN-LINE DROP TARGETS UP |
| 16 | IN-LINE DROP TARGETS BOTTOM |
| 17 | IN-LINE DROP TARGETS MIDDLE |
| 18 | IN-LINE DROP TARGETS TOP |
| 19 | SAUCER |
| 20 | WEAPON DROP TARGET UP |
| 21 | WEAPON DROP TARGET DOWN |
| 22 | CAPTURE DROP TARGET |
| 23 | OUTHOLE EJECTOR |
| 24 | FLIPPER (BACKBOX) |

## SWITCH ASSEMBLY IDENTIFICATION TABLE

Column headings: `SWITCH SELF TEST # SEQUENCE` and `DESCRIPTION`. A parenthesized second line belongs to the row
above it and is joined here with a space.

| SWITCH SELF TEST # SEQUENCE | DESCRIPTION |
| --- | --- |
| 1 | COLLECT WEAPON |
| 2 | CHOPPER TOP |
| 3 | CHOPPER BOTTOM |
| 4 | REBOUND |
| 5 | LEFT LAUNCH (LT. ORANGE P.B.) |
| 6 | NEW GAME |
| 7 | RIGHT LAUNCH (RT. ORANGE P.B.) |
| 8 | OUTHOLE REGULAR |
| 9 | RIGHT COIN DOOR |
| 10 | LEFT COIN DOOR |
| 11 | MIDDLE COIN DOOR |
| 12 | LEFT OUTLANE |
| 13 | RIGHT OUTLANE |
| 14 | SLAM |
| 15 | TILT (CABINET) |
| 16 | RELEASE LEFT (BEHIND IN-LINE D.T.) |
| 17 | ROCKET 'R' |
| 18 | ROCKET 'O' |
| 19 | ROCKET 'C' |
| 20 | ROCKET 'K' |
| 21 | ROCKET 'E' |
| 22 | ROCKET 'T' |
| 23 | SAUCER CAPTURE 1 |
| 24 | SAUCER CAPTURE 2 |
| 25 | LEFT BUMPER |
| 26 | RIGHT BUMPER |
| 27 | MIDDLE BUMPER |
| 28 | LEFT SLINGSHOT |
| 29 | RIGHT SLINGSHOT |
| 30 | RIGHT OUTHOLE |
| 31 | MIDDLE OUTHOLE |
| 32 | LEFT OUTHOLE |
| 33 | BOMB 'B' |
| 34 | BOMB 'O' |
| 35 | BOMB 'M' |
| 36 | BOMB 'B' |
| 37 | NOT USED |
| 38 | COLLECT BONUS |
| 39 | NOT USED |
| 40 | WEAPON DROP TARGET |
| 41 | AUXILIARY CAPTIVE (NEAR SAUCER) |
| 42 | RETURN LANES |
| 43 | BONUS MULTIPLIER |
| 44 | LOAD BOMBS |
| 45 | IN-LINE DROP TARGET (BOTTOM) |
| 46 | IN-LINE DROP TARGET (MIDDLE) |
| 47 | IN-LINE DROP TARGET (TOP) |
| 48 | ROAD SWITCH |

Footnote, verbatim: `*NOTE: SEQUENCE NUMBERS SHOWN HERE ARE USED AS AN AID IN LOCATING FAULTY SOLENOID OR SWITCH
USING DRAWING SHOWN.` followed by `VECTOR SHOWING FOR EJECT SAUCER BALL SHOULD EXIT AS SHOWN.`

The switch sequence numbers are the public PinMAME switch numbers: the cabinet rows 6 (NEW GAME), 9-11 (coin doors),
14 (SLAM) and 15 (TILT (CABINET)) sit exactly where `by6803.c` `SWITCH_UPDATE(by6803)` writes Credit, the three coins,
Slam Tilt and Ball Tilt, and the ROM's own Switch Test names public 2, 5, 7, 14, 15 and 16 with these rows' words
(`evidence/runtime/by6803/special-force-specforc-switch-test.json`).
