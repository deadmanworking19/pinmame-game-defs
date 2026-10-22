# Centaur — A9 playfield wiring diagram (W-1255-2)

Transcribed from `Bally_1981_Centaur_Installation_and_General_Game_Operation_Instructions_with_schematics_OCR_searchable.pdf`,
**PDF page 54**, the scanned drawing titled `WIRING DIAGRAM PLAYFIELD`, `CENTAUR`, `1239`, part
number `W-1255-2` sheet `b`. An arrow at the lower left reads `TO W-1207-11`, the A9 board sheet.
The accompanying crop is the same region of the native 590 dpi scan.

An earlier transcription of this drawing cited PDF page 46. That was wrong: the visible scan on page
46 is the `G I FLASHER (SCHEMATIC)` sheet `W-1253 b`, and the W-1255-2 text had been read from the
OCR text layer laid over that page, which belongs to page 54's drawing. Read the scan, not the
layer.

## The list, top to bottom

Each row is drawn as a wire leaving the harness trunk on the left, then a printed number, a
connector position, an optional function and, on the right, a lamp symbol tied to a common bus. The
bus ends at `A2J1-5`, labelled `5.4 VDC`. Every row carries a lamp symbol, `N/U` rows included. The
first column is the Bally wire-colour code: the same numbers sit against the same pins in the A9
sheet's own harness list (`a9-harness-j2-list.md`), and PinWiki's chart gives their colours (`54`
Wht-Grn, `25` Blu-Wht, `43` Grn-Yel).

| code | connector | printed function |
| --- | --- | --- |
| 72 | A9J3-18 | |
| N/U | A9J3-17 | |
| 56 | A9J3-16 | |
| 14 | A9J3-15 | |
| 27 | A9J2-12 | LEFT THUMPER BUMPER |
| 96 | A9J2-17 | #4 CHAMBER (2) (TOP) |
| 21 | A9J3-12 | |
| 70 | A9J3-11 | |
| 54 | A9J2-7 | TOP LEFT LANE |
| 53 | A9J3-9 | |
| 13 | A9J3-8 | |
| 82 | A9J2-19 | RIGHT THUMPER BUMPER |
| N/U | A9J3-6 | |
| N/U | A9J3-5 | |
| 95 | A9J2-20 | # 3 CHAMBER (2) |
| 20 | A9J3-3 | |
| 57 | A9J2 18 | *(printed without the dash)* |
| 43 | A9J2-1 | TOP MIDDLE LANE |
| N/U | A9J2-16 | |
| 52 | A9J2-15 | |
| 12 | A9J2-14 | |
| 40 | A9J2- 2 | LEFT SLING SHOT |
| 62 | A9J2-3 | #2 CHAMBER (2) |
| 18 | A9J2-11 | |
| 80 | A9J2-10 | |
| 25 | A9J2-18 | TOP RIGHT LANE |
| 51 | A9J2-8 | |
| 10 | A9J2-7 | |
| 45 | A9J2-6 | RIGHT SLING SHOT |
| 60 | A9J2-5 | #1 CHAMBER (2)(FROM BOTTOM) |
| 15 | A9J2-4 | |
| 20 | A2J1-5 | *(the bus, `5.4 VDC`)* |

Blank function cells are blank on the sheet.

## What the sheet can and cannot be used for

The eleven rows that print a function reproduce the A9 sheet's harness list exactly, code for code
and pin for pin. They are the eleven lamp circuits Centaur fits on the board.

The twenty rows without a function cannot be read as lamp circuits of the AS-2518-43 this machine
carries:

- eleven of them name an `A9J3` connector, and the AS-2518-43 has none: its parts list fits only a
  15-pin `J1` and two 10-pin wafers forming `J2`, and its schematic draws no `J3`;
- the rest name `J2` positions that W-1207-11 prints as `KEY` (4), `GND` (8), `N/U` (10, 14, 15,
  16) or the unwired pin 11, or repeat pins 7 and 18 under a second code.

A wire on the key position cannot exist. The sheet reads as a lamp-list template laid out for a
larger auxiliary board with a second output connector. The German manual's module list names the
28-output AS-2518-52 for A9 where the English parts list names the AS-2518-43, which fits that reading,
but that list also has other part-number errors (`german-manual-a9-and-solenoid-tables.md`). Its
unlabelled rows, including `18 — A9J2-11`, therefore establish no load on this machine; the A9
sheet's own harness list, which draws a wire only where a circuit is fitted, is the wiring record.
