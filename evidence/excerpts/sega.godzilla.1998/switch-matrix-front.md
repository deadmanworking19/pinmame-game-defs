# Switch matrix and dedicated switches, front reference

Source: Sega Godzilla manual, PDF page 6, printed `DR. 4`; SHA-256
`fc71e6584b2a8ad715100f94b5d4d690b0cd3864cd9abd6746c2441ad4d6c1c5`.
Method: Windows.Media.Ocr for navigation, then manual transcription from the
native-resolution render by `tools/render_excerpt_image.py` (150 dpi, embedded
1280-pixel scan). Transcribed by: curator. Review: candidate; the small location
sub-labels still need a second visual read.
Question marks below are transcription uncertainty, not printed punctuation.
Numbers are the printed cell numbers, not an independent public-address proof.

## Matrix drive and return headers

| Column | Driver | Wire | Connector |
|---|---|---|---|
| 1 | Q1 | GRN-BRN | CN5-P1 |
| 2 | Q2 | GRN-RED | CN5-P3 |
| 3 | Q3 | GRN-ORG | CN5-P4 |
| 4 | Q4 | GRN-YEL | CN5-P5 |
| 5 | NOT USED (merged header) | — | — |
| 6 | Q6 | GRN-BLU | CN5-P7 |
| 7 | Q7 | GRN-VIO | CN5-P8 |
| 8 | Q8 | GRN-GRY | CN5-P9 |

| Row | Input | Wire | Connector |
|---|---|---|---|
| 1 | U400 | WHT-BRN | CN7-P9 |
| 2 | U400 | WHT-RED | CN7-P8 |
| 3 | U400 | WHT-ORG | CN7-P7 |
| 4 | U400 | WHT-YEL | CN7-P6 |
| 5 | U401 | WHT-GRN | CN7-P5 |
| 6 | U401 | WHT-BLU | CN7-P3 |
| 7 | U401 | WHT-VIO | CN7-P2 |
| 8 | U401 | WHT-GRY | CN7-P1 |

## Matrix cells

The scan shades the NOT USED cells and the UK-only cells. Column 5 prints one
merged NOT USED header, rather than separate driver, wire or connector cells.
Legible small captions include `on Coin Door` for the coin slots (2–7),
`Cabinet Front` for launch 53 and start 54, and `Inside Cabinet` for plumb
bob tilt 56. The remaining small location captions are not yet fully
transcribed; this excerpt remains a candidate.

| Row | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 LEFT SAV-A-BALL (UK ONLY) | 9 NOT USED | 17 LEFT 4-BANK BOTTOM | 25 NOT USED | 33 NOT USED | 41 LT CAPTIVE BALL BOT | 49 LEFT TURBO BUMPER | 57 LEFT OUTLANE |
| 2 | 2 4TH COIN SLOT | 10 NOT USED | 18 LEFT 4-BANK #2 | 26 GODZILLA RAMP (LT) | 34 NOT USED | 42 LT CAPTIVE BALL TOP | 50 RIGHT TURBO BUMPER | 58 LEFT RETURN LANE |
| 3 | 3 6TH COIN SLOT | 11 4-BALL TROUGH #1 (LEFT) | 19 LEFT 4-BANK #3 | 27 NOT USED | 35 NOT USED | 43 RT CAPTIVE BALL BOT | 51 BOTTOM TURBO BUMPER | 59 LEFT SLINGSHOT |
| 4 | 4 RIGHT COIN SLOT | 12 4-BALL TROUGH #2 | 20 LEFT 4-BANK TOP | 28 ORBIT RAMP (RT) | 36 NOT USED | 44 RT CAPTIVE BALL TOP | 52 NOT USED | 60 RIGHT OUTLANE |
| 5 | 5 CENTER COIN SLOT / DBA | 13 4-BALL TROUGH #3 | 21 RIGHT 4-BANK BOTTOM | 29 (T)AXI S-U | 37 NOT USED | 45 INNER LEFT ORBIT | 53 LAUNCH BUTTON | 61 RIGHT RETURN LANE |
| 6 | 6 LEFT COIN SLOT | 14 4-BALL TROUGH VUK OPTO | 22 RIGHT 4-BANK #2 | 30 T(A)XI S-U | 38 NOT USED | 46 SPINNER | 54 START BUTTON | 62 RIGHT SLINGSHOT |
| 7 | 7 5TH COIN SLOT | 15 4-BALL STACKING OPTO | 23 RIGHT 4-BANK #3 | 31 TA(X)I S-U | 39 NOT USED | 47 LEFT ORBIT | 55 SLAM TILT | 63 NOT USED |
| 8 | 8 RIGHT SAV-A-BALL (UK ONLY) | 16 SHOOTER LANE | 24 RIGHT 4-BANK TOP | 32 TAX(I) S-U | 40 NOT USED | 48 RIGHT ORBIT | 56 PLUMB BOB TILT | 64 NOT USED |

## Dedicated switches

The ground header prints `Ground`, `BLK`, `CN6-P1,-P11`. The input header
prints `U206`. The fifth row is shaded `NOT USED` in both cells; it does not
print a wire or connector.

| Input | Wire | Connector | Printed description | Printed identifier |
|---|---|---|---|---|
| 1 U206 | GRY-BRN | CN6-P2 | #1 LEFT FLIPPER BUTTON | DS-1 |
| 2 U206 | GRY-RED | CN6-P3 | #2 LEFT FLIPPER E.O.S (End-of-Stroke) | DS-2 |
| 3 U206 | GRY-ORG | CN6-P4 | #3 RIGHT FLIPPER BUTTON | DS-3 |
| 4 U206 | GRY-YEL | CN6-P6 | #4 RIGHT FLIPPER E.O.S. (End-of-Stroke) | DS-4 |
| NOT USED (merged input header) | — | — | NOT USED | DS-5 |
| 6 U206 | GRY-BLU | CN6-P8 | #6 VOLUME (RED BUTTON) (In Test: LEFT) | DS-6 |
| 7 U206 | GRY-VIO | CN6-P9 | #7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT) | DS-7 |
| 8 U206 | GRY-BLK | CN6-P10 | #8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER) | DS-8 |
