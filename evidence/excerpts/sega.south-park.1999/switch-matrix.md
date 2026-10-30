# South Park — Switch Matrix Grid and dedicated switches

Read from `Sega_1999_South_Park_Manual_English.pdf` (IPDB 4444, 72 scanned spreads with two printed pages each). The
Switch Matrix Grid is the front-matter drawing printed `DR. 4` on PDF page 4 (left half); its part-number and mounting
details repeat in the printed page-15 switch table on PDF page 15 (right half). Both are scans with no text layer;
every cell was read from a 220 dpi render and checked against a Windows OCR pass.

## Matrix drives and returns

| Column | Drive transistor | Drive wire | Connector |
| --- | --- | --- | --- |
| 1 | Q1 | GRN-BRN | CN5-P1 |
| 2 | Q2 | GRN-RED | CN5-P3 |
| 3 | Q3 | GRN-ORG | CN5-P4 |
| 4 | Q4 | GRN-YEL | CN5-P5 |
| 5 | Q5 | GRN-BLK | CN5-P6 |
| 6 | Q6 | GRN-BLU | CN5-P7 |
| 7 | Q7 | GRN-VIO | CN5-P8 |
| 8 | Q8 | GRN-GRY | CN5-P9 |

| Row | Receiver | Return wire | Connector |
| --- | --- | --- | --- |
| 1 | U400 | WHT-BRN | CN7-P9 |
| 2 | U400 | WHT-RED | CN7-P8 |
| 3 | U400 | WHT-ORG | CN7-P7 |
| 4 | U400 | WHT-YEL | CN7-P6 |
| 5 | U401 | WHT-GRN | CN7-P5 |
| 6 | U401 | WHT-BLU | CN7-P3 |
| 7 | U401 | WHT-VIO | CN7-P2 |
| 8 | U401 | WHT-GRY | CN7-P1 |

## Matrix switches

Switch number = (column − 1) × 8 + row. "Grid" is the cell text on DR. 4; "Part" and "Notes" come from the
printed page-15 table, which spells some names differently (both spellings are kept). A part cell the table prints
once beside several rows is marked "(shared cell)".

| # | Col | Row | Grid | Page-15 name | Part | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | LEFT BUTTON (UK ONLY) | LEFT BUTTON (UK ONLY) | 180-5160-00 | on cabinet side |
| 2 | 1 | 2 | 4TH COIN SLOT | 4TH COIN SLOT | 180-5024-00 | coin door |
| 3 | 1 | 3 | 6TH COIN SLOT | 6TH COIN SLOT | Future Use | |
| 4 | 1 | 4 | RIGHT COIN SLOT | RIGHT COIN SLOT | 180-5024-00 (shared cell) | |
| 5 | 1 | 5 | CENTER COIN SLOT / DBA | CENTER COIN SLOT / DBA | 180-5024-00 (shared cell) | |
| 6 | 1 | 6 | LEFT COIN SLOT | LEFT COIN SLOT | 180-5024-00 (shared cell) | |
| 7 | 1 | 7 | 5TH COIN SLOT | 5TH COIN SLOT | Future Use | |
| 8 | 1 | 8 | RIGHT BUTTON (UK ONLY) | RIGHT BUTTON (UK ONLY) | 180-5160-00 | |
| 9 | 2 | 1 | NOT USED | NOT USED | | |
| 10 | 2 | 2 | 5-BALL TROUGH #1 (LEFT) | 5-BALL TROUGH #1 (LEFT) | 180-5119-02 | under P/F |
| 11 | 2 | 3 | 5-BALL TROUGH #2 | 5-BALL TROUGH #2 | 180-5119-02 | under P/F |
| 12 | 2 | 4 | 5-BALL TROUGH #3 | 5-BALL TROUGH #3 | 180-5119-02 | under P/F |
| 13 | 2 | 5 | 5-BALL TROUGH #4 | 5-BALL TROUGH #4 | 180-5119-02 | under P/F |
| 14 | 2 | 6 | 5-BALL TROUGH VUK OPTO | 5-BALL TROUGH VUK OPTO | BOT TRANS 520-5173-00 / BOT REC 520-5174-00 | ‡ |
| 15 | 2 | 7 | 5-BALL STACKING OPTO | 5-BALL STACKING OPTO | TOP TRANS 520-5173-00 / TOP REC 520-5174-00 | ‡ |
| 16 | 2 | 8 | SHOOTER LANE | SHOOTER LANE | 180-5157-00 | DOTS |
| 17 | 3 | 1 | LEFT 5-BANK BOTTOM | LEFT 5-BANK BOT. (Prp. Sq. Rear Mnt.) | 500-6139-09R | R |
| 18 | 3 | 2 | LEFT 5-BANK #2 | LEFT 5-BANK #2 | 500-6139-09R | R |
| 19 | 3 | 3 | LEFT 5-BANK #3 | LEFT 5-BANK #3 | 500-6139-09R | R |
| 20 | 3 | 4 | LEFT 5-BANK #4 | LEFT 5-BANK #4 | 500-6139-09R | R |
| 21 | 3 | 5 | LEFT 5-BANK TOP | LEFT 5-BANK TOP (Purp. Sq. Rear Mnt.) | 500-6139-09R | R |
| 22 | 3 | 6 | CENTER 3-BANK LEFT | CENTER 3-BANK LT. (Grn. Nar. Rear Mnt.) | 500-6138-04R | R |
| 23 | 3 | 7 | CENTER 3-BANK MIDDLE | CENTER 3-BANK MID. (Red Rect. Fwd.) | 500-6228-02 | |
| 24 | 3 | 8 | CENTER 3-BANK RIGHT | CENTER 3-BANK RT. (Grn. Narrow Fwd.) | 500-6138-04 | |
| 25 | 4 | 1 | RIGHT RAMP ENTER | RIGHT RAMP ENTER | 180-5087-00 | above P/F |
| 26 | 4 | 2 | RIGHT RAMP EXIT | RIGHT RAMP EXIT | 180-5087-00 | above P/F |
| 27 | 4 | 3 | NOT USED | NOT USED | | |
| 28 | 4 | 4 | NOT USED | NOT USED | | |
| 29 | 4 | 5 | NOT USED | NOT USED | | |
| 30 | 4 | 6 | NOT USED | NOT USED | | |
| 31 | 4 | 7 | NOT USED | NOT USED | | |
| 32 | 4 | 8 | NOT USED | NOT USED | | |
| 33 | 5 | 1 | NOT USED | NOT USED | | |
| 34 | 5 | 2 | RIGHT 3-BANK BOTTOM | RT 3-BANK BOT. (Flo.Grn. Rnd. Rear Mnt.) | 500-6075-11R | R |
| 35 | 5 | 3 | RIGHT 3-BANK MIDDLE | RT 3-BANK MID. | 500-6075-11R | R |
| 36 | 5 | 4 | RIGHT 3-BANK TOP | RT 3-BANK TOP | 500-6075-11R | R |
| 37 | 5 | 5 | POP BUMPER TARGET LT | POP BUMPER TARGT LT (Flo. Grn. Sq.) | 500-6139-11 | |
| 38 | 5 | 6 | POP BUMPER TARGET RT | POP BUMPER TARGT RT | 500-6139-11 | |
| 39 | 5 | 7 | NOT USED | NOT USED | | |
| 40 | 5 | 8 | NOT USED | NOT USED | | |
| 41 | 6 | 1 | NOT USED | NOT USED | | |
| 42 | 6 | 2 | KENNY OPTO | KENNY (OPTO) | TRANS 520-5082-00 / REC 520-5083-01 | under P/F; OPTO & Bracket (Long) Assembly 500-6242-02-71 |
| 43 | 6 | 3 | UNDERTROUGH (TOILET) | UNDERTROUGH (TOILET) | 180-5057-00 | |
| 44 | 6 | 4 | UNDERTROUGH (KENNY) | UNDERTROUGH (KENNY) | 180-5057-00 | |
| 45 | 6 | 5 | SVUK | SVUK (Super Vertical Up-Kicker Switch) | 180-5052-00 | DOTS |
| 46 | 6 | 6 | VUK | VUK (Vertical Up-Kicker Switch) | 180-5116-01 | DOTS |
| 47 | 6 | 7 | LEFT ORBIT (TO VUK) | LEFT ORBIT (TO VUK) | 500-6227-02 | |
| 48 | 6 | 8 | UNDERTROUGH SVUK | UNDERTROUGH SVUK | 180-5057-00 | |
| 49 | 7 | 1 | LEFT TURBO BUMPER | LEFT TURBO BUMPER | 180-5015-03 | page 15 prints its column/row as "7 4" |
| 50 | 7 | 2 | RIGHT TURBO BUMPER | RIGHT TURBO BUMPER | 180-5015-03 | |
| 51 | 7 | 3 | BOTTOM TURBO BUMPER | BOTTOM TURBO BUMPER | 180-5015-03 | |
| 52 | 7 | 4 | NOT USED | NOT USED | | |
| 53 | 7 | 5 | NOT USED | NOT USED | | |
| 54 | 7 | 6 | START BUTTON | START BUTTON (Red) | 500-6090-02 | grid: Cabinet Front |
| 55 | 7 | 7 | SLAM TILT | SLAM TILT (On Coin Door) | 180-5022-00 | |
| 56 | 7 | 8 | PLUMB BOB TILT | PLUMB BOB TILT | HANGER 535-5319-00, CONTACT 535-7563-01 | Inside Cabinet |
| 57 | 8 | 1 | LEFT OUTLANE | LEFT OUTLANE (Rt. Mount R/O) | 500-6227-02 | |
| 58 | 8 | 2 | LEFT RETURN LANE | LEFT RETURN LANE | 500-6227-02 | |
| 59 | 8 | 3 | LEFT SLINGSHOT | LEFT SLINGSHOT (Double-Switch) | 180-5054-00 | |
| 60 | 8 | 4 | RIGHT OUTLANE | RIGHT OUTLANE | 500-6227-02 | |
| 61 | 8 | 5 | RIGHT RETURN LANE | RIGHT RETURN LANE | 500-6227-02 | |
| 62 | 8 | 6 | RIGHT SLINGSHOT | RIGHT SLINGSHOT (Double-Switch) | 180-5054-00 | |
| 63 | 8 | 7 | NOT USED | NOT USED | | |
| 64 | 8 | 8 | NOT USED | NOT USED | | |

Page notes, verbatim where legible:

- "‡ Sw.14/Sw.15 have both REC/TRANS on 1 board respectively"
- "Switches located in cabinet: 2,4,5,6,54,55,56"
- "Not used: 9, 27-33, 39-41, 52-53, 63-64"
- "UK only: 1+8"
- Japan ¥ coin switch: 180-5091-00.
- "R" = reverse (rear) mounted target and switch actuator. "DOTS" = Diode On Terminal Strip.

## Dedicated switches (U206 inputs; ground BLK, CN6-P1 and CN6-P11)

| Input | Wire | Connector | Function as printed | Location |
| --- | --- | --- | --- | --- |
| DS-1 | GRY-BRN | CN6-P2 | #1 Left Flipper Button | in cabinet side |
| DS-2 | GRY-RED | CN6-P3 | #2 Left Flipper E.O.S (End-of-Stroke) | |
| DS-3 | GRY-ORG | CN6-P4 | #3 Right Flipper Button | |
| DS-4 | GRY-YEL | CN6-P6 | #4 Right Flipper E.O.S. | |
| DS-5 | GRY-GRN | CN6-P7 | NOT USED | |
| DS-6 | GRY-BLU | CN6-P8 | #6 Volume (Red Button) (In Test: LEFT) | on coin door |
| DS-7 | GRY-VIO | CN6-P9 | #7 Serv. Cred. (Green Button) (In Test: RIGHT) | |
| DS-8 | GRY-BLK | CN6-P10 | #8 Begin Test (Black Button) (In Test: ENTER) | |
