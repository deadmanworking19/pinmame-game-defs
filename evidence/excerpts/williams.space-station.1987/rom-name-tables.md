# Space Station — ROM lamp, switch and coil name tables

Decoded by `tools/space_station_rom_name_tables.py` from the user-authorized local ROM archive; no ROM bytes are
reproduced. Each table is a run of fixed 14-byte entries in the 32 KiB **U27** program ROM: seven characters for the
player 1 display followed by seven for the player 2 display, which is how the Single Lamps, Switch Levels and Coil
tests print them. A byte with bit 7 set is the character in its low seven bits followed by the display's period
segment. Entries are shown with the two halves joined by one space and padding trimmed. The lamp table ends where
the switch table begins; the coil table starts at its own anchor further on, after a block of non-text bytes.

| Driver | ROM archive SHA-256 | ROM member | Member SHA-256 | Lamp table | Switch table | Coil table |
| --- | --- | --- | --- | --- | --- | --- |
| spstn_l5 | `8c5cdaf5a8e6a4b112873f17c6a66ca34de6ac15eb830474965cdfa035434f7c` | sstn_u27.l5 | `9b6b108a53e1149d6fd3ff6abe308bc3e7f3ffceee204a44caf3dbe2dfa53bf5` | 0x1299 | 0x1619 | 0x19f2 |

## Lamp table (public lamp address = entry number)

| Lamp | ROM text |
| --- | --- |
| 1 | BON BAL PLYR 1 |
| 2 | BON BAL PLYR 2 |
| 3 | BON BAL PLYR 3 |
| 4 | BON BAL PLYR 4 |
| 5 | EXTRA BALL |
| 6 | RIGHT RELEASE |
| 7 | LEFT RELEASE |
| 8 | DOCKING WL LEFT |
| 9 | CHANGE SHUTTLE |
| 10 | CHANGE STATION |
| 11 | 1X BONUS |
| 12 | 2X BONUS |
| 13 | 4X BONUS |
| 14 | UPPER LAMP 1 |
| 15 | UPPER LAMP 2 |
| 16 | UPPER LAMP 3 |
| 17 | LEFT DRAIN |
| 18 | SHUTTLE S |
| 19 | SHUTTLE H |
| 20 | SHUTTLE U |
| 21 | SHUTTLE 1ST T |
| 22 | SHUTTLE 2ND T |
| 23 | SHUTTLE L |
| 24 | SHUTTLE E |
| 25 | STATION S |
| 26 | STATION 1ST T |
| 27 | STATION A |
| 28 | STATION 2ND T |
| 29 | STATION I |
| 30 | STATION O |
| 31 | STATION N |
| 32 | RIGHT DRAIN |
| 33 | STOP  N SCORE |
| 34 | DOCKING WL RGHT |
| 35 | SPECIAL |
| 36 | 100 K WHEN LT |
| 37 | STATION WHEEL 4 |
| 38 | USA U |
| 39 | USA S |
| 40 | USA A |
| 41 | STATION WHEEL 6 |
| 42 | RELAUN W LIT |
| 43 | DOCKED LEFT |
| 44 | HOLD BONUS |
| 45 | DOCKED RIGHT |
| 46 | STATION WHEEL 3 |
| 47 | STATION WHEEL 2 |
| 48 | STATION WHEEL 1 |
| 49 | FLAME 1 |
| 50 | SH SCOR SPECIAL |
| 51 | SH SCOR EX BALL |
| 52 | SH SCOR 50K REN |
| 53 | SH SCOR 50K BON |
| 54 | SH SCOR 150 K |
| 55 | SH SCOR 75 K |
| 56 | SH SCOR 25 K |
| 57 | STATION WHEEL 5 |
| 58 | ST SCOR SPECIAL |
| 59 | ST SCOR EX BALL |
| 60 | ST SCOR 50K REN |
| 61 | ST SCOR 50K BON |
| 62 | ST SCOR 150 K |
| 63 | ST SCOR 75 K |
| 64 | ST SCOR 25 K |

## Switch table (public switch address = entry number)

| Switch | ROM text |
| --- | --- |
| 1 | PLUMB TILT |
| 2 | BALL TILT |
| 3 | CREDIT BUTTON |
| 4 | COIN SLOT 1 |
| 5 | COIN SLOT 2 |
| 6 | COIN SLOT 3 |
| 7 | SLAM TILT |
| 8 | HISCORE RESET |
| 9 | PLAYFLD TILT |
| 10 | OUTHOLE |
| 11 | TROUGH BALL 1 |
| 12 | TROUGH BALL 2 |
| 13 | TROUGH BALL 3 |
| 14 | ROLOVER 1 |
| 15 | ROLOVER 2 |
| 16 | ROLOVER 3 |
| 17 | LEFT DRAIN |
| 18 | SHUTTLE S |
| 19 | SHUTTLE H |
| 20 | SHUTTLE U |
| 21 | SHUTTLE 1ST T |
| 22 | SHUTTLE 2ND T |
| 23 | SHUTTLE L |
| 24 | SHUTTLE E |
| 25 | STATION S |
| 26 | STATION 1ST T |
| 27 | STATION A |
| 28 | STATION 2ND T |
| 29 | STATION I |
| 30 | STATION O |
| 31 | STATION N |
| 32 | RIGHT DRAIN |
| 33 | R SNGLE DROP TG |
| 34 | NOT USED |
| 35 | SHT CHG BOTTOM |
| 36 | NOT USED |
| 37 | ROL UND TOP L |
| 38 | USA U |
| 39 | USA S |
| 40 | USA A |
| 41 | L BALL POPPER |
| 42 | R BALL POPPER |
| 43 | PLUNGER |
| 44 | (blank) |
| 45 | RIGHT LOCK UP |
| 46 | R LOCK ENTRY |
| 47 | LEFT LOCK UP |
| 48 | L LOCK ENTRY |
| 49 | NOT USED |
| 50 | TOP RGT 10 PTS |
| 51 | LEFT 10 PTS |
| 52 | SPC STA SWTCH 1 |
| 53 | SPC STA SWTCH 2 |
| 54 | LOW RGT 10 PTS |
| 55 | LEFT FLIPPER |
| 56 | RIGHT FLIPPER |
| 57 | 3 BANK BOTTOM |
| 58 | 3 BANK CENTER |
| 59 | 3 BANK TOP |
| 60 | LEFT BUMPER |
| 61 | RIGHT BUMPER |
| 62 | BOTTOM BUMPER |
| 63 | LEFT KICKER |
| 64 | RIGHT KICKER |

## Coil table (ROM coil-test order; entry numbers are table positions, not addresses)

The ROM's Coil Test pairs each displayed entry with the public solenoid it pulses; that pairing is in the
runtime evidence, not in this table. The audit-name table (`LEFT COINS`, ...) follows the blank entry.

| Entry | ROM text |
| --- | --- |
| 1 | OUTHOLE |
| 2 | RELNCH FLASHER |
| 3 | BALL RELEASE |
| 4 | LEFT FLASHER |
| 5 | LF BALL POPPER |
| 6 | RIGHT FLASHER |
| 7 | RT BALL POPPER |
| 8 | TOP FLASHER |
| 9 | PANEL FLASHER |
| 10 | 3 BANK |
| 11 | FLAME FLASHER |
| 12 | INSERT KNOCKER |
| 13 | STATION FLASHER |
| 14 | RIGHT DROP TG |
| 15 | LEFT DOCK |
| 16 | PLAYFLD GEN ILU |
| 17 | PLAYFLD GRN GI |
| 18 | INSERT GI |
| 19 | AC SELECT |
| 20 | LEFT REENTRY |
| 21 | PANEL LIGHTS |
| 22 | SPACE STATION |
| 23 | RIGHT DOCK |
| 24 | LEFT SLING |
| 25 | RIGHT JET |
| 26 | RIGHT SLING |
| 27 | LEFT JET |
| 28 | BOTTOM JET |
| 29 | NOT USED |
| 30 | (blank) |

Normalization: each seven-character half is trimmed and the halves are joined with one space; spaces inside a half are kept.
