# Figure 3. Switch Matrix

Source: Firepower II Service Manual 16-521-101, July 1983, PDF page 18,
printed page 22; PDF SHA-256
`c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8`.
Method: manual transcription, visually checked against the retained native raster
by the curator. Line breaks are joined with spaces.
All 64 cells and all printed wiring headers follow. This region prints no
driver transistor identifiers or normally-closed marks.

| Column | Wire | Connection |
| --- | --- | --- |
| 1 | GRN-BRN | 2J2-9 |
| 2 | GRN-RED | 2J2-8 |
| 3 | GRN-ORN | 2J2-7 |
| 4 | GRN-YEL | 2J2-6 |
| 5 | GRN-BLK | 2J2-5 |
| 6 | GRN-BLU | 2J2-3 |
| 7 | GRN-VIO | 2J2-2 |
| 8 | GRN-GRY | 2J2-1 |

| Row | Wire | Connection | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | WHT-BRN | 2J3-9 | 1 Plumb Tilt | 9 Outhole | 17 Standup 100 | 25 "F" Target 1000 | 33 "R" Target 1000 | 41 Lower Left Jet Bumper 100/1000 | 49 Playfield Tilt | 57 Not Used |
| 2 | WHT-RED | 2J3-8 | 2 Ball Roll Tilt | 10 Right Ball Ramp | 18 Spinner 100/1000 | 26 "I" Target 1000 | 34 "A" Rollover 1000 | 42 Upper Right Jet Bumper 100/1000 | 50 Not Used | 58 Not Used |
| 3 | WHT-ORN | 2J3-7 | 3 Credit Button | 11 Left Ball Ramp | 19 Orbit in Roll Under | 27 "R" Target 1000 | 35 "B" Rollover 1000 | 43 Upper Left Jet Bumper 100/1000 | 51 Not Used | 59 Not Used |
| 4 | WHT-YEL | 2J3-6 | 4 Right Coin | 12 Ball Shooter Trough | 20 Upper Left Standup 50 | 28 "E" Target 1000 | 36 "C" Rollover 1000 | 44 Lower Right Jet Bumper 100/1000 | 52 Not Used | 60 Not Used |
| 5 | WHT-GRN | 2J3-5 | 5 Center Coin | 13 Lane Change | 21 Not Used | 29 "P" Target 1000 | 37 "D" Rollover 1000 | 45 Left Flipper Return Lane 1000 | 53 Not Used | 61 Not Used |
| 6 | WHT-BLU | 2J3-4 | 6 Left Coin | 14 Ramp in Roll Under | 22 Upper Right Standup 50 | 30 "O" Target 1000 | 38 Left Outlane 10,000 | 46 Right Flipper Return Lane 1000 | 54 Not Used | 62 Not Used |
| 7 | WHT-VIO | 2J3-3 | 7 Slam Tilt | 15 Ramp out Roll Under | 23 Eject Hole 5000/Lit Value | 31 "W" Target 1000 | 39 Right Outlane 10,000 | 47 Left Kicker 10 | 55 Not Used | 63 Not Used |
| 8 | WHT-GRY | 2J3-1 | 8 High Score Reset | 16 Center Left Standup 100 | 24 Release Target 1000 | 32 "E" Target 1000 | 40 Orbit Out Gate | 48 Right Kicker 10 | 56 Not Used | 64 Not Used |

Printed 57/58 are Not Used. The corpus scripts' direct writes to 57/58 do not
establish physical switches. The driver's FLIP_SWNO(0,13) copies the synthetic
right button 82 into matrix 13; a consumer drives 82 for lane change.
