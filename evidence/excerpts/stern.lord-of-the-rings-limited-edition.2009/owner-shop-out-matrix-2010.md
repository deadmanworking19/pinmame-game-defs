# An LE owner's shop-out matrix (2010)

Two retained documents from one owner, Richard Harvey ("firepower"), who kept the LOTR Pinball blog about their own Limited Edition. Neither is a factory document: the chart is Stern's 2003 cabinet chart as the owner corrected it against their LE. Both are recorded as an owner's first-hand report.

## The blog post

`Shop-out Matrix for LOTR LE Cabinet and documentation`, posted 29 Oct 2010, https://lotrpinball.blogspot.com/2010/10/shopout-pages-for-lotr-le.html (retained HTML SHA-256 `ab7dc2457789de5f70aa83d240f9d5e748e5a20ad6fcbf7d9c961551959904c8`). The passages about the hardware, as printed:

> Recently discovered that the 17" x 11" Page stapled in to the cabinet had mistakes,  as it was the one used on the  original LOTR.

> This is what a pinball tech or you might refer to when fault finding.  On my LE at least, wire colors and 2 solenoids positions were changed.  The updated LE matrix I did shows a different Solenoid table and correct wiring colours for the Lamp Matrix.

> LE Examples: I have shown coil #12 as the opt. shaker motor, #14 is unused on the LE, #28 is the Helms Deep Right flasher.

> The main board that changed in the LE compared to the original 2003/2005 LOTR was the I/O Power Driver Board which is a Stern 520-5249-00 (Sam).  I also don't like using a "Z" connector used between the playfield and the I/O Driver board to convert J10 to the new positions.  Why not just make the harness terminate correctly in the first place?

> The CPU Sound II Board is a Stern 520-5300-00 Rev A (Whitestar).

The post links an LE manual and a `LOTR LE I/O Driver Board Schematic` (`Sam 520-5249-00 in 17" x 11" format`) on blackknightpinball.com; those links timed out and nothing from them is retained.

## The chart

`Stern_Lord_of_the_Rings_LE_Tech_Chart.pdf`, mirrored at https://www.pinballrebel.com/pinball/cards/Tech_Charts/Stern_Lord_of_the_Rings_LE_Tech_Chart.pdf (SHA-256 `a7eeefd8f739d48cea1c80ef18c48d42a08d5e9c2438ed7d2b2c6cbfe9e94d02`), `COILS DETAILED CHART TABLE`. Columns: number and function, Drive Transistor, Driver Ouput Board (sic), Power Line Color, Power Line Connection, Power Voltage, Drive Transistor Control Line Color, D.T. Control Line Connect. Rows 11-14 and 27-29 as printed; the driver-board cell is one merged `I/O Power Driver` cell per group, repeated here. Rows 12 and 14 are shaded grey, and their three power-line cells are blank.

| # | Function | Drive Transistor | Driver Ouput Board (sic) | Power Line Color | Power Line Connection | Power Voltage | D.T. Control Line Color | D.T. Control Line Connect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #11 | BOTTOM BUMPER | Q11 | I/O Power Driver | BRN-BLU | J10-P4/5 | 50v DC | BLU-ORG | J9-P4 |
| #12 | OPTIONAL SHAKER MOTOR | Q12 | I/O Power Driver | (blank) | (blank) | (blank) | BLU-YEL | J9-P5 |
| #13 | ORBIT PIN | Q13 | I/O Power Driver | YEL-BLU | J7-P1 | 20v DC | BLU-GRN | J9-P6 |
| #14 | NOT USED  NC J9-P7 | Q14 | I/O Power Driver | (blank) | (blank) | (blank) | BLU-BLK | J9-P7 |
| #27 | FLASH:  BACK PANEL | Q27 | I/O Power Driver | YEL-ORG | J6-P10 | 20v DC | BLK-ORG | J6-P3 |
| #28 | FLASH: HELMS DEEP RT | Q28 | I/O Power Driver | YEL-ORG | J6-P10 | 20v DC | BLU-BLK | J6-P4 |
| #29 | FLASH:  RINGWRAITH | Q29 | I/O Power Driver | YEL-ORG | J6-P10 | 20v DC | BLK-GRN | J6-P5 |

The note under the flasher rows still reads, its last parenthesis in red: `Note:  In Test Flash Lamps Menu ("Flash" Icon), Flashers tested are all Flash Lamps located between Q1-Q32 (This Game: Q14, Q23 & Q25-Q27, Q29-Q32)`. It lists Q14 and omits Q28, which is the 2003 machine's flasher set: the note was not updated with the rows above it.
