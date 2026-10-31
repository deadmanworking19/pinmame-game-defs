# Elvis (Stern) — Backbox I/O Power Driver Board Detailed Wiring Diagram

Read from `Elvis_Manual.pdf`, PDF page 118, printed `Section 5, Chapter 1, Page 101` ("Backbox Wiring"), from a 200 dpi
render checked against the page's text layer. The page draws the "Partial View I/O Power Driver Board 520-5137-01" with
its J6-J10 headers and every load. Transistor labels sit beside the header rows; the load column is transcribed here
row by row as drawn.

| Header pin | Wire | Load label as printed | Load drawn |
| --- | --- | --- | --- |
| J6-1 | RED | #25 Stepper (Motor) #1 | stepper motor winding |
| J6-2 | GREEN | #26 Stepper (Motor) #2 | stepper motor winding |
| J6-3 | BLACK | #27 Stepper (Motor) #3 | stepper motor winding |
| J6-4 | BLUE | #28 Stepper (Motor) #4 | stepper motor winding |
| J6-5 | BLK-GRN | #29 Elvis Legs | 29-1400 "ELVIS LEGS", RED-WHT both ends, "Diode in Conn." |
| J6-6 | BLK-BLU | #30 Elvis Arms | 29-1400 "ELVIS ARMS", RED-WHT both ends, "Diode in Conn." |
| J6-7 | BLK-VIO | #31 Flash: Elvis Spot Lights X2 | bulb glyph "#906 Clear Bulb X1" |
| J6-8 | BLK-GRY | #32 Flash: Slingshots X2 | bulb glyph "#906 Clear Bulb X2" |
| J6-10 | | ORG 20v DC LOW POWER ↘ | |
| J7-1 | | BRN 20v DC LOW POWER ↘ | feeds the legs and arms coils as `BROWN` |
| J7-2 | VIO-BRN | #17 Left Slingshot | 23-800 |
| J7-3 | VIO-RED | #18 Right Slingshot | 23-800 |
| J7-4 | VIO-ORG | #19 Hotel Door | 27-1500 |
| J7-6 | VIO-YEL | #20 Flash: Back Panel X2 | bulb glyph "#89 Clear Bulb X2" |
| J7-7 | VIO-GRN | #21 Flash: Back Panel TCB | bulb glyph "#89 Clear Bulb X1" |
| J7-8 | VIO-BLU | #22 Flash: Spinner | bulb glyph "#906 Clear Bulb X1" |
| J7-9 | VIO-BLK | #23 Flash:Upper Right Flipper X2 | bulb glyph "#906 Clear Bulb X2" |
| J7-10 | (VIO-GRY), printed grey under "Optional" | #24 Optional Coil (white on black) | a coil box printed "OPTIONAL", fed "FROM RED Power Out +5v DC J16-P8 I/O BD." |
| J8-1 | BRN-BLK | #1 Trough Up-Kicker | 26-1200 |
| J8-3 | BRN-RED | #2 Auto Launch | 23-800 |
| J8-4 | BRN-ORG | #3 Elvis 5-Bank (Drop Trgt.) Reset | 24-940 |
| J8-5 | BRN-YEL | #4 (OPT) Shaker Motor (Optional) (white on black) | runs to the Shaker Motor Board |
| J8-6 | BRN-GRN | #5 Magnet | 22-650 "MAGNET", BLACK both ends, "Diode in Conn.", fed "FROM VIO-YEL High Power 50v DC" J10-P3 |
| J8-7 | BRN-BLU | #6 Center Eject | 24-940 |
| J8-8 | BRN-VIO | #7 Hotel Lock Release | 23-800 |
| J8-9 | BRN-GRY | #8 Control Gate | 32-1800 |
| J9-1 | BLU-BRN | #9 Left Bumper | 26-1200 |
| J9-2 | BLU-RED | #10 Right Bumper | 26-1200 |
| J9-4 | BLU-ORG | #11 Bottom Bumper | 26-1200 |
| J9-5 | BLU-YEL | #12 Top Eject | 24-940 |
| J9-6 | BLU-GRN | #13 Upper Left Flipper | 23-900, 3A Slo-Blo, GRY-YEL |
| J9-7 | BLU-BLK | #14 Upper Right Flipper | 23-900, 3A Slo-Blo, BLU-YEL |
| J9-8 | ORG-GRY | #15 (Lower) Left Flipper | 22-900, 3A Slo-Blo, GRY-YEL |
| J9-9 | ORG-VIO | #16 (Lower) Right Flipper | 22-900, 3A Slo-Blo, BLU-YEL |

The four flipper fuses are fed "FROM RED-YEL High Power 50v DC" (J10-P1/2) and captioned "These Coil Fuses are located
under playfield NEAR assembly, see Sec. 5, Chp. 2, Playfield Wiring." The other 50v coils return to "FROM YEL-VIO High
Power 50v DC" (J10-P4/5).

Stepper motor block: "STEPPER MOTOR 041-5069-00 Haydon Nº 46868-12-002", drawn as two centre-tapped windings ("Shaft
Side" and "Rear"); RED, GRN, BLK and BLU leads to the four phase wires, both centre taps (WHT) to a "Lug Under
Playfield" fed "FROM GRY-RED Power Out +12v DC J16-P3 I/O BD.".

Shaker block: "order Shaker Motor Kit 502-5027-00-84", "OPTIONAL +12V DC SHAKER MOTOR 041-5029-01 Located in Cabinet",
driven through a "SHAKER MOTOR BOARD 520-5065-00, Located in Cabinet OPTIONAL" fed "FROM RED-WHT Transformer +16v AC
+12v DC" (J17-P7).

Board notes: "Q25-Q32 TIP122 110-0067-00", "Q17-Q24 TIP122 110-0067-00", "Q1-Q8 STP20N10L 110-0106-00", "Q9-Q16
STP20N10L 110-0106-00"; "Note: All Coils require diodes. Some diodes may be located on Terminal Strips & not on the coil
itself."

## Curator's observations (not printed)

- Flasher #31's name says two spot lights and its bulb glyph says one; the coil chart (PDF 8) prints the bulb type only.
  Both readings are kept.
- The #24 coin-meter output is drawn on +5v DC here and on the coil chart; the pink-page cabinet parts list offers the
  optional meter as "+12v DC". Both call the output optional.
