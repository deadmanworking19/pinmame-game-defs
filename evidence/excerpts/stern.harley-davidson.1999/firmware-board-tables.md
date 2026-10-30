# Harley-Davidson (Stern) — firmware, production and board-type appendices

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`: PDF page 142 ("APPENDIX A, Pinball Game
Firmware (White Star Board System Only*) Table"), PDF page 143 (the same appendix's footnotes), PDF page 145 ("APPENDIX C,
Production Start Date, Manual Part Nº, ROM Size, Positions and Jumper W6 Installed Note‡ (White Star Board System
Only*)") and PDF page 146 ("APPENDIX D, Board Type (White Star Board System Only*) Table"). Read from 130-400 dpi renders
and checked against the pages' decoded text layer. Only the Harley-Davidson rows and the footnotes they cite are
transcribed.

## Appendix A: firmware rows

Columns: ROM, Chip Size, Program Part Nº, USA Ver. & Check Sum, Bd. Loc., Raw Part Nº.

**Harley-Davidson® (Notes 4, 5, 6) Original (1999-2001)**

| ROM | Chip Size | Program Part Nº | USA Ver. & Check Sum | Bd. Loc. | Raw Part Nº |
| --- | --- | --- | --- | --- | --- |
| Game ROM | (1M) | 965-0319-67 | A1.03 \| $3EFF | U210 | 960-5009-00 |
| Sound | (512K) | 965-0320-67 | 1.00 \| $F4FF | U7 | 960-7001-02 |
| Display | (4M) | 965-0321-67 | A1.04 \| $FC7C | ROM 0 | 960-5015-01 |
| Voice 1 | (8M) | 965-0322-67 | 1.00 \| $CD26 | U17 | 960-5016-00 |
| Voice 2 | (8M) | 965-0323-67 | 1.00 \| $9396 | U21 | 960-5016-00 |
| Voice 3 | (8M) | 965-0324-67 | 1.00 \| $FB72 | U36 | 960-5016-00 |
| Voice 4 | (4M) | 965-0325-67 | 1.00 \| $6100 | U37 | 960-5015-01 |

**▶ Harley-Davidson® (Notes 4, 5, 6, 8) 2nd Edition (2002-2003)**

| ROM | Chip Size | Program Part Nº | USA Ver. & Check Sum | Bd. Loc. | Raw Part Nº |
| --- | --- | --- | --- | --- | --- |
| Game ROM | (1M) | 965-0319-67A (A in red) | A1.08 \| $23FF | U210 | 960-5009-00 |
| Display | (4M) | 965-0321-67A (A in red) | A1.05 \| $B594 | ROM 0 | 960-5015-01 |

**▶ Harley-Davidson® (Notes 4, 5, 6, 8) 3rd Edition (2004)**

| ROM | Chip Size | Program Part Nº | USA Ver. & Check Sum | Bd. Loc. | Raw Part Nº |
| --- | --- | --- | --- | --- | --- |
| Game ROM | (1M) | 965-0319-87 | A3.00 \| $22FF | U210 | 960-5009-00 |
| Display | (4M) | 965-0321-87 | A3.00 \| $B596 | U5 | 960-5015-01 |

A vertical tab beside the two edition blocks reads "Sound & Voice 1-4 identical to above H-D® Original."

Footnotes (page 143), verbatim for the numbers the rows cite:

- "4 ROMs on CPU/Sound Bd.: 520-5136-16† (Mono) (†FCC 02-98) & Display Controller Board: 520-5055-03‡ (‡FCC 02-98)"
- "5 This game uses 8MB VOICE ROMS at U17, U21, U36 & U37 (if 3 ROMs use U37 will be unused) requiring a Jumper at Loc.
  W6. Refer to CPU/Snd. Bd. Schematic (2 of 3)."
- "6 Harley-Davidson® 2nd Edition: For Game ROM, Sound & Display info (version, check sums, part numbers) call Tech
  Support or check our website (see back cover) for current versions or other info. Raw Part numbers are identical to the
  H-D® original."
- "7 ToPS™ (Tournament Pinball System) READY!"
- "8 ROMs on CPU/Sound Board II (with ATMEL Processor): 520-5300-00 & Display Cont. Bd.: 520-5055-03‡ (‡FCC 02-98)"

## Appendix C: production rows

Columns: "Game\ Name White Star Board System™", "Production Start Date and Manual PNº", CPU/Sound Board Voice ROMs U17,
U21, U36, U37 (the heading also names "Sound U7 512K" and "Game U210 1MB"), "Jumper Installed (‡ see Note)".

| # | Game\ Name | Production Start Date and Manual PNº | U17 | U21 | U36 | U37 | Jumper |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 42 a | Harley-Davidson® | AUG 99, 780-5067-01 | 8MB | 8MB | 8MB | 8MB | W6 |
| 42 b | Harley-Davidson®2nd Ed. | SEP 02, 780-5067-10 | 8MB | 8MB | 8MB | 8MB | W6 |
| 42 c | Harley-Davidson® 3rd Ed. | OCT 04, 780-5087-00 | 8MB | 8MB | 8MB | 8MB | W6 |

Appendix C prints U37 as 8MB where Appendix A prints Voice 4 as a (4M) chip at U37.

## Appendix D: board types

Columns: Game Name, Flipper, I/O Power Driver, CPU/Sound Stereo, Disp. Power Supply, Dot Matrix Display, Display
Controller, OPTO Transmitter, OPTO Receiver, OPTO Application. The Harley-Davidson row's name cell reads
"Harley-Davidson® 1st-3rd* Editions"; its Flipper cell is empty (a line under the Golden Eye row reads "GAMES HEREON NO
LONGER REQUIRE THE FLIPPER BOARD WITH THE WHITE STAR BOARD SYSTEM™").

| Field | Cell |
| --- | --- |
| I/O Power Driver | 520-5137-01 |
| CPU/Sound | 520-5136-16 over *520-5300-00* |
| Disp. Power Supply | 520-5138-00 |
| Dot Matrix Display | 520-5052-00 128 X 32 |
| Display Controller | 520-5055-03 |
| OPTO (first row) | 515-0173-00 Dual OPTO / 515-0174-00 Dual OPTO / "4-Ball Trough over Up-Kicker" |
| Miscellaneous PC Boards | Relay Board 520-5010-00; Shaker Mtr. Bd. 520-5065-00; Diode Board 520-5146-00 |
| OPTO (second row) | 520-5082-00 Long Hop OPTO / 520-5083-01 Long Hop OPTO / "Motorcycle Enter" |

The asterisks on "3rd*" and "*520-5300-00*" have no key on the page; the table title's own asterisk ("White Star Board
System Only*") keys the black note band.
