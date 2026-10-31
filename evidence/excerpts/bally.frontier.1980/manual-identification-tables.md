# Frontier - solenoid identification table and switch assembly self-test display numbers

Transcribed from `Bally_1980_Frontier_Manual.pdf`, PDF page 21 (printed page 17), read from the native 300 dpi render of the scan (the PDF has no text layer). The page is headed "GAME #1217 FRONTIER (FIGURE V)". Each table is printed in two columns, left column first; they are reproduced here as one list each. Spelling, capitalisation and quotation marks are the page's own. A row the page prints with a number and no description is kept with an explicitly empty cell. The page prints no connector, wire, transistor or part columns.

## SOLENOID IDENTIFICATION TABLE

| Self Test # | SOLENOID IDENTIFICATION |
| --- | --- |
| 01 | OUTHOLE |
| 02 | KNOCKER |
| 03 | 3 DROP TARGET RESET |
| 04 | SAUCER |
| 05 | DROP TARGET RESET (INLINE) |
| 06 | LEFT THUMPER BUMPER |
| 07 | RIGHT THUMPER BUMPER |
| 08 | BOTTOM THUMPER BUMPER |
| 09 | LEFT SLINGSHOT |
| 10 | RIGHT SLINGSHOT |
| 11 | GATE |
| 12 | COIN LOCKOUT DOOR |
| 13 | KI RELAY (FLIPPER ENABLE) |

The page prints "KI" for the K1 relay.

## SWITCH ASSEMBLY SELF-TEST DISPLAY NUMBERS

| Switch Self Test # | DESCRIPTION |
| --- | --- |
| 01 | 30 POINT REBOUND (4) |
| 02 | RIGHT OUT |
| 03 | RIGHT FLIPPER FEED |
| 04 | LEFT FLIPPER FEED |
| 05 | LEFT OUT |
| 06 | CREDIT BUTTON |
| 07 | TILT (3) |
| 08 | OUTHOLE |
| 09 | COIN III (RIGHT) |
| 10 | COIN I (LEFT) |
| 11 | COIN II (MIDDLE) |
| 12 | SAUCER |
| 13 | "A" ROLLOVER |
| 14 | "B" ROLLOVER |
| 15 | "C" ROLLOVER |
| 16 | SLAM (2) |
| 17 | (blank) |
| 18 | (blank) |
| 19 | (blank) |
| 20 | (blank) |
| 21 | 3RD INLINE DROP TARGET |
| 22 | 2ND INLINE DROP TARGET |
| 23 | 1ST INLINE DROP TARGET |
| 24 | GRIZZLY TARGET |
| 25 | SAUCER ROLLOVER BUTTON |
| 26 | (blank) |
| 27 | SPINNER |
| 28 | (blank) |
| 29 | LEFT TARGET |
| 30 | CENTER TARGET |
| 31 | RIGHT TARGET |
| 32 | (blank) |
| 33 | BOTTOM SIDE D.T. |
| 34 | MIDDLE SIDE D.T. |
| 35 | TOP SIDE DROP TARGET |
| 36 | RIGHT SLINGSHOT |
| 37 | LEFT SLINGSHOT |
| 38 | BOTTOM THUMPER BUMPER |
| 39 | RIGHT THUMPER BUMPER |
| 40 | LEFT THUMPER BUMPER |

Below the switch table the page prints: "NOTE: SLINGSHOT & THUMPER BUMPER COILS WILL BE ENERGIZED WHEN SWITCH IS MADE."

The switch numbers are the switch test's display numbers; the ROM's own switch test shows the same number when the public PinMAME switch of that number closes, for all forty. The solenoid numbers are the order of the ROM's cycling solenoid test, not public addresses: the retained solenoid test pairs them with public outputs 7, 6, 9, 10, 8, 11, 12, 13, 14, 15, 17, 18 and 19.
