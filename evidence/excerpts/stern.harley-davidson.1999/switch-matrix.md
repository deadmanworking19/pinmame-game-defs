# Harley-Davidson (Stern) — Switch Matrix Grid and dedicated switches

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf` (IPDB 5277 file, 160 pages). The Switch
Matrix Grid & Dedicated Switches is the front-matter drawing printed `DR. 4` on PDF page 6 (upper part); its part numbers
and mounting details repeat in the switch table printed `Section 3, Chapter 2, Page 15` on PDF page 33. The PDF carries a
text layer in a re-encoded font; every cell was read from a 200 dpi render and checked against that decoded text layer.

## Matrix drives and returns

Every column and row heading on DR. 4 also carries a small pale "NOT USED" line under its number; it is printed on all
sixteen headings and is kept here only as a literal observation.

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

Switch number = (column − 1) × 8 + row. "Grid" is the cell text on DR. 4 with its printed mounting line; "Page-15
description", "Part" and "Note" come from the page-15 table, which spells some names differently (both spellings are
kept). A part cell the table prints once beside several rows is marked "(shared cell)". The page-15 "See Note" column
prints `DODB` on 41-44 and `DOTS` on 45 and 46 and is blank on every other row; DR. 4 carries the same tags vertically
beside those cells. Cells 1 and 8 are shaded light grey on DR. 4; row 1 is shaded grey on page 15. NOT USED cells are
black on both pages.

| # | Col | Row | Grid | Page-15 description | Part | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | LEFT BUTTON (UK ONLY), on Cabinet side | LEFT BUTTON (UK ONLY) | 180-5160-00 | |
| 2 | 1 | 2 | 4TH COIN SLOT, On Coin Door | 4TH COIN SLOT | 180-5024-00 | number printed 2* |
| 3 | 1 | 3 | 6TH COIN SLOT, On Coin Door | 6TH COIN SLOT (italic) | (Future Use) | number printed 3* |
| 4 | 1 | 4 | RIGHT COIN SLOT, On Coin Door | RIGHT COIN SLOT | 180-5024-00 (shared cell) | number printed 4* |
| 5 | 1 | 5 | CENTER COIN SLOT / DBA, On Coin Door | CENTER COIN SLOT / DBA | 180-5024-00 (shared cell) | number printed 5* |
| 6 | 1 | 6 | LEFT COIN SLOT, On Coin Door | LEFT COIN SLOT | 180-5024-00 (shared cell) | number printed 6* |
| 7 | 1 | 7 | 5TH COIN SLOT, On Coin Door | 5TH COIN SLOT (italic) | (Future Use) | number printed 7* |
| 8 | 1 | 8 | RIGHT BUTTON (SKILL), on Cabinet side | RIGHT BUTTON (SKILL) | 180-5160-00 | |
| 9 | 2 | 1 | NOT USED | NOT USED | | |
| 10 | 2 | 2 | NOT USED | NOT USED | | |
| 11 | 2 | 3 | 4-BALL TROUGH #1 (LEFT), Under P/F | 4-BALL TROUGH #1 (LEFT) | 180-5119-00 | |
| 12 | 2 | 4 | 4-BALL TROUGH #2, Under P/F | 4-BALL TROUGH #2 | 180-5119-00 (shared cell) | |
| 13 | 2 | 5 | 4-BALL TROUGH #3, Under P/F | 4-BALL TROUGH #3 | 180-5119-00 (shared cell) | |
| 14 | 2 | 6 | 4-BALL TROUGH VUK OPTO, Under P/F | 4-BALL TROUGH VUK OPTO | BOT TRANS: 520-5173-00 / BOT REC: 520-5174-00 | number printed 14‡ |
| 15 | 2 | 7 | 4-BALL STACKING OPTO, Under P/F | 4-BALL STACKING OPTO | TOP TRANS: 520-5173-00 / TOP REC: 520-5174-00 | number printed 15‡ |
| 16 | 2 | 8 | SHOOTER LANE, Under P/F | SHOOTER LANE | 180-5100-01 | |
| 17 | 3 | 1 | LT 4-BANK D/T (L) IVE, Under P/F | LT 4-BANK D/T (L)IVE | 180-5104-00 | |
| 18 | 3 | 2 | LT 4-BANK D/T L (I) VE, Under P/F | LT 4-BANK D/T L(I)VE | 180-5104-00 (shared cell) | |
| 19 | 3 | 3 | LT 4-BANK D/T LI (V) E, Under P/F | LT 4-BANK D/T LI(V)E | 180-5104-00 (shared cell) | |
| 20 | 3 | 4 | LT 4-BANK D/T LIV (E), Under P/F | LT 4-BANK D/T LIV(E) | 180-5104-00 (shared cell) | |
| 21 | 3 | 5 | RT 4-BANK D/T (R) IDE, Under P/F | RT 4-BANK D/T (R)IDE | 180-5104-00 (shared cell) | |
| 22 | 3 | 6 | RT 4-BANK D/T R (I) DE, Under P/F | RT 4-BANK D/T R(I)DE | 180-5104-00 (shared cell) | |
| 23 | 3 | 7 | RT 4-BANK D/T RI (D) E, Under P/F | RT 4-BANK D/T RI(D)E | 180-5104-00 (shared cell) | |
| 24 | 3 | 8 | RT 4-BANK D/T RID (E), Under P/F | RT 4-BANK D/T RID(E) | 180-5104-00 (shared cell) | |
| 25 | 4 | 1 | RIGHT RAMP ENTER, Above P/F | RIGHT RAMP ENTER (Switch Gate) | 180-5087-00 | |
| 26 | 4 | 2 | RIGHT RAMP EXIT, Above P/F | RIGHT RAMP EXIT (Switch Gate) | 180-5087-00 (shared cell) | |
| 27 | 4 | 3 | RIGHT RAMP MID, Above P/F | RIGHT RAMP MID (Switch Gate) | 180-5087-00 (shared cell) | |
| 28 | 4 | 4 | SPINNER, Above P/F | SPINNER | 180-5010-04 | |
| 29 | 4 | 5 | S-U TRGT LT (M-CYCLE), Under P/F | S-U TRGT LT (M-CYLE) (Nar. Trgt. Red) | 500-6138-02 | |
| 30 | 4 | 6 | S-U TRGT RT (M-CYCLE), Under P/F | S-U TRGT RT (M-CYLE) (Nar. Trgt. Red) | 500-6138-02 (shared cell) | |
| 31 | 4 | 7 | S-U TRGT LT (RT RAMP), Under P/F | S-U TRGT LT (RT RAMP) (Nar. Trgt. Red) | 500-6138-02 (shared cell) | |
| 32 | 4 | 8 | S-U TRGT RT (RT RAMP), Under P/F | S-U TRGT RT (RT RAMP) (Nar. Trgt. Red) | 500-6138-02 (shared cell) | |
| 33 | 5 | 1 | LEFT ORBIT, Under P/F | LEFT ORBIT (Lt. Mount Roll-Over Lite Sw.) | 500-6227-03 | |
| 34 | 5 | 2 | RIGHT ORBIT, Under P/F | RIGHT ORBIT (Rt. Mount Roll-Over Lite Sw.) | 500-6227-04 | |
| 35 | 5 | 3 | MOTOR UP, Under P/F | MOTOR UP | 180-5052-00 | |
| 36 | 5 | 4 | MOTOR DOWN, Under P/F | MOTOR DOWN | 180-5052-00 (shared cell) | |
| 37 | 5 | 5 | OPTO, Under P/F | OPTO | TRANS 180-5082-00 / REC 180-5083-01 | number printed 37‡ |
| 38 | 5 | 6 | NOT USED | NOT USED | | |
| 39 | 5 | 7 | NOT USED | NOT USED | | |
| 40 | 5 | 8 | NOT USED | NOT USED | | |
| 41 | 6 | 1 | M-CYCLE TROUGH #4 (TOP), Under P/F | M-CYCLE TROUGH #4 (TOP) | (1) 4-Position Membrane Switch: 181-5001-00 | DODB |
| 42 | 6 | 2 | M-CYCLE TROUGH #3, Under P/F | M-CYCLE TROUGH #3 | (1) 4-Position Membrane Switch: 181-5001-00 (shared cell) | DODB |
| 43 | 6 | 3 | M-CYCLE TROUGH #2, Under P/F | M-CYCLE TROUGH #2 | (1) 4-Position Membrane Switch: 181-5001-00 (shared cell) | DODB |
| 44 | 6 | 4 | M-CYCLE TROUGH #1 (BOT), Under P/F | M-CYCLE TROUGH #1 (BOT) | (1) 4-Position Membrane Switch: 181-5001-00 (shared cell) | DODB |
| 45 | 6 | 5 | SUPER VUK, Under P/F | SUPER VUK | 180-5052-00 | DOTS |
| 46 | 6 | 6 | BALL EJECT (SCOOP), Under P/F | BALL EJECT (Power Scoop / Kick Big) | 180-5057-00 | DOTS |
| 47 | 6 | 7 | NOT USED | NOT USED | | |
| 48 | 6 | 8 | BEHIND TOP VUK, Under P/F | BEHIND TOP VUK (Metal Under-Trough) | 180-5057-00 | |
| 49 | 7 | 1 | LEFT TURBO BUMPER, Under P/F | LEFT TURBO BUMPER | 180-5015-03 | page 15 prints its column/row as "7 4" |
| 50 | 7 | 2 | RIGHT TURBO BUMPER, Under P/F | RIGHT TURBO BUMPER | 180-5015-03 (shared cell) | |
| 51 | 7 | 3 | BOTTOM TURBO BUMPER, Under P/F | BOTTOM TURBO BUMPER | 180-5015-03 (shared cell) | |
| 52 | 7 | 4 | TOP TURBO BUMPER, Under P/F | TOP TURBO BUMPER | 180-5015-03 (shared cell) | |
| 53 | 7 | 5 | LAUNCH BUTTON, Cabinet Front | LAUNCH BUTTON (Yel.) | 500-6121-06 | |
| 54 | 7 | 6 | START BUTTON, Cabinet Front | START BUTTON (Red) | 500-6090-02 | number printed 54* |
| 55 | 7 | 7 | SLAM TILT, On Coin Door | SLAM TILT (On Coin Door) | 180-5022-00 | number printed 55* |
| 56 | 7 | 8 | PLUMB BOB TILT, Inside Cabinet | PLUMB BOB TILT | HANGER 535-5319-00 / CONTACT 535-7563-01 | number printed 56* |
| 57 | 8 | 1 | LEFT OUTLANE, Under P/F | LEFT OUTLANE (Rt. Mount Roll-Over Sw.) | 500-6227-02 | |
| 58 | 8 | 2 | LEFT RETURN LANE, Under P/F | LEFT RETURN LANE (Rt. Mnt. R-O Sw.) | 500-6227-02 (shared cell) | |
| 59 | 8 | 3 | LEFT SLINGSHOT, Under P/F | LEFT SLINGSHOT (Double-Switch) | 180-5054-00 | |
| 60 | 8 | 4 | RIGHT OUTLANE, Under P/F | RIGHT OUTLANE (Rt. Mount R-O Sw.) | 500-6227-02 | |
| 61 | 8 | 5 | RIGHT RETURN LANE, Under P/F | RT RETURN LANE (Rt. Mount R-O Sw.) | 500-6227-02 (shared cell) | |
| 62 | 8 | 6 | RIGHT SLINGSHOT, Under P/F | RIGHT SLINGSHOT (Double-Switch) | 180-5054-00 | |
| 63 | 8 | 7 | NOT USED | NOT USED | | |
| 64 | 8 | 8 | NOT USED | NOT USED | | |

Page-15 notes, verbatim:

- Above the table: "Note: The ¥ Coin Switch (for Japan) is 180-5091-00"
- "‡ Sw. 14 / Sw. 15 have both REC/TRANS on 1 board respectively. Sw. 37 has both REC/TRANS on the same board."
- "DOTS: Diode On Terminal Strip, or DODB: Diode On Diode Board"
- "Legend Note: [white box] = Switches mounted above playfield. [black box] = Switches mounted below playfield."
- "* The following switches are located in the cabinet and are not noted in the diagram above: 2 4 5 6 54 55 56"
  (the page's own diagram nevertheless draws 54 and 56 as grey callouts).
- "The following switches are not used: 9 10 38 39 40 47 63 64"
- "Switches for Up/Down Post: ( 8 )"

DR. 4 prints the heading "Diode On Terminal Strip:" above the switch grid and "Diode On Diode Board:" below it.

## Dedicated switches (U206 inputs; ground BLK, CN6-P1, -P11)

| Input | Wire | Connector | Function as printed | Location as printed |
| --- | --- | --- | --- | --- |
| DS-1 | GRY-BRN | CN6-P2 | #1 LEFT FLIPPER BUTTON | in Cabinet side |
| DS-2 | GRY-RED | CN6-P3 | #2 LEFT FLIPPER E.O.S (End-of-Stroke) | in Cabinet side |
| DS-3 | GRY-ORG | CN6-P4 | #3 RIGHT FLIPPER BUTTON | in Cabinet side |
| DS-4 | GRY-YEL | CN6-P6 | #4 RIGHT FLIPPER E.O.S. (End-of-Stroke) | in Cabinet side |
| DS-5 | GRY-GRN | CN6-P7 | #5 NOT USED (input heading also prints NOT USED; cell black) | |
| DS-6 | GRY-BLU | CN6-P8 | #6 VOLUME (RED BUTTON) (In Test: LEFT) | on Coin Door |
| DS-7 | GRY-VIO | CN6-P9 | #7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT) | on Coin Door |
| DS-8 | GRY-BLK | CN6-P10 | #8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER) | on Coin Door |
