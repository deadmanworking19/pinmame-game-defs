# Literal transcription - CYCLONE Switch-Matrix Table

`reviewed: true`; transcribed by the curator from a 300 dpi render and visually checked against it on 2026-10-31
`source: Manual & Schematics PDF page 34 (printed page CYCLONE 30), Test/Diagnostic Procedures, Switch Tests`

Retained render: `external:pinmame-manuals/by-machine/williams.cyclone.1988/rendered-native/manual/p-34.png` (300 dpi).

Literal heading: `CYCLONE Switch-Matrix Table`. Each column header prints the column number, its driver transistor,
its wire colour and its CPU connector pin; each row header prints the row number, its wire colour and its CPU
connector pin. Each cell is `printed name - printed number`; line breaks inside a cell are joined with a space.
Cells 14, 15 and 16 print a large numeral above the word `Lane`. No cell is shaded or marked as an opto, and no
cell is blank: every unused position prints `Not Used`.

| row / wire / connector | 1 Q45 GRN-BRN 1J8-1 | 2 Q49 GRN-RED 1J8-2 | 3 Q44 GRN-ORN 1J8-3 | 4 Q48 GRN-YEL 1J8-4 | 5 Q43 GRN-BLK 1J8-5 | 6 Q47 GRN-BLU 1J8-7 | 7 Q42 GRN-VIO 1J8-8 | 8 Q46 GRN-GRY 1J8-9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 WHT-BRN 1J10-9 | Plumb Bob Tilt - 1 | Playfield Tilt - 9 | Ferris Wheel Entrance - 17 | Ball Shooter Lane - 25 | Not Used - 33 | Mystery Wheel Opto "Home" (Insert bd) - 41 | Not Used - 49 | Left Flipper Lane Change - 57 |
| 2 WHT-RED 1J10-8 | Not Used - 2 | Outhole - 10 | Drop Target (center) - 18 | Shuttle 10K (kickbig) - 26 | Score CYCLONE - 34 | Not Used - 42 | Not Used - 50 | Right Flipper Lane Change - 58 |
| 3 WHT-ORN 1J10-7 | Credit Button - 3 | Score Spook House - 11 | Ducks (top) - 19 | Shuttle 25K (bottom) - 27 | 10 pt (R. Bottom) - 35 | Not Used - 43 | Not Used - 51 | Spot Ball Toss - 59 |
| 4 WHT-YEL 1J10-6 | Right Coin Chute - 4 | Not Used - 12 | Ducks (middle) - 20 | Shuttle 100K - 28 | 10 pt (R. Middle) - 36 | Not Used - 44 | Not Used - 52 | Left Jet Bumper - 60 |
| 5 WHT-GRN 1J10-5 | Center Coin Chute - 5 | Boomerang Kickbig - 13 | Ducks (bottom) - 21 | Shuttle 25K - 29 | 10 pt (R. Top) - 37 | Not Used - 45 | Left Outlane Ex. Ball - 53 | Right Jet Bumper - 61 |
| 6 WHT-BLU 1J10-3 | Left Coin Chute - 6 | 1 Lane - 14 | Ball Toss (top) - 22 | Shuttle 5K (top) - 30 | Not Used - 38 | Not Used - 46 | Right Outlane Ex. Ball - 54 | Bottom Jet Bumper - 62 |
| 7 WHT-VIO 1J10-2 | Slam Tilt - 7 | 2 Lane - 15 | Ball Toss (middle) - 23 | Enter COMET Ramp - 31 | Not Used - 39 | Not Used - 47 | Left Return Lane - 55 | Left Kicker - 63 |
| 8 WHT-GRY 1J10-1 | High-Score Reset - 8 | 3 Lane - 16 | Ball Toss (bottom) - 24 | Score COMET Ramp - 32 | Not Used - 40 | Not Used - 48 | Right Return Lane - 56 | Right Kicker - 64 |

Text printed below the table on the same page (verbatim): `Row Problems. If a display of two (or more) switch
numbers of a row occurs, although only one switch is closed, check for a short circuit between the column wires.`
`Multiple Switch Number Indications. Check the associated column wire for a short circuit to ground.` `Column
Problems. If display of two (or more) switch numbers in a column occurs (while only one switch is actuated), check
for a short circuit between the row wires.` `Use AUTO-UP to proceed to the next test.`

The text above the table on the same page (Switch Levels): `For CYCLONE, switch numbers can range from 01 through
64. Refer to the Switch-Matrix Table for switch numbers and wiring information. CPU Board connections at jacks 1J8
(columns) and 1J10 (rows) are also listed in the table.`

Uncertainty: the matrix is a wiring and name table. It does not print contact construction, polarity or location;
`Drop Target (center)` is an opto (switch-location list, excerpt `location-parts-lists`), and `Mystery Wheel Opto
"Home"` is on the backbox insert board.
