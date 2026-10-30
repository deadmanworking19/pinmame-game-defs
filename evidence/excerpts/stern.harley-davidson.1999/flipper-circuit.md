# Harley-Davidson (Stern) — 2-Flipper Circuit Wiring Diagram

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`, PDF page 104, printed `Section 5, Chapter
2, Page 88` ("Playfield Wiring"). The crop `flipper-circuit.webp` renders the whole page. Read from a 200 dpi render and
checked against the page's decoded text layer.

## Dedicated switches (CN6, "DEDICATED SWITCH INPUTS (SWITCH TO GROUND)", CPU-SOUND BOARD)

| Drawn switch | Wire | CN6 pin | Contact as drawn |
| --- | --- | --- | --- |
| LEFT FLIPPER IN CABINET DEDICATED SWITCH DS-1 | GRY-BRN | 2 | N.O. |
| LEFT E.O.S. ON ASSY. DEDICATED SWITCH DS-2 | GRY-RED | 3 | N.C. |
| RIGHT FLIPPER IN CABINET DEDICATED SWITCH DS-3 | GRY-ORG | 4 | N.O. |
| RIGHT E.O.S. ON ASSY. DEDICATED SWITCH DS-4 | GRY-YEL | 6 | N.C. |
| UPPER LT or RT FLIPPER IN CABINET DEDICATED SWITCH DS-5 | GRY-GRN | 7 | N.O.; drawn in green with a "NOT USED" tag |

The CN6 header prints pins 1 2 3 4 6 7 ... 12. All switch commons join "BLK (GROUND)" to J16 ("POWER OUT", pins 1, 11,
15) on the I/O POWER DRIVER BOARD. "NOTE: N.C. = Normally Closed N.O. = Normally Open".

## Coils (I/O POWER DRIVER BOARD, "MOS FET STP20N10L" Q13-Q16)

| Coil | Drive wire (J9) | Power wire | Fuse | Coil |
| --- | --- | --- | --- | --- |
| LOWER RIGHT FLIPPER COIL | ORG-VIO | RED-YEL 50V DC through the fuse to BLU-YEL | 3A SLO-BLO (Located under Playfield) | 23-1100, "Coil Wrap: ORANGE" |
| LOWER LEFT FLIPPER COIL | ORG-GRY | RED-YEL 50V DC through the fuse to GRY-YEL | 3A SLO-BLO (Located under Playfield) | 22-1080, "Coil Wrap: YEL-GRN" |

"↕ RED-YEL 50V DC ↕" leaves J10 ("VOLTAGE OUTPUTS", pins 2 and 1). J9 is "HIGH CURRENT SOLENOIDS", the drive lines on its
pins 9 and 8. Each coil carries a diode across it. "The 3A 250v Slo-Blo Fuses are located under the playfield NEAR the
Flipper Assembly, see previous page for locations."

## Technical Overview, verbatim

"Our Flipper System uses one supply voltage (50v DC) for both kick & hold. Once the Game CPU detects a Flipper Cabinet
Switch closure (during game play) it applies a 40msec pulse to the gate of the Flipper Drive Transistor (STP-20N10L). If
it continues to detect a Flipper Cabinet Switch closure (the player holding the button in) it will continue to pulse the
flipper drive transistor 1msec every 12msecs for the duration of the hold cycle."

"The E.O.S. (End-Of-Stroke) Switch serves the same function as before as it prevents foldback when the player has the
flipper energized to capture balls. The E.O.S. Switch is a normally closed switch which opens approximately 1/16" when
the flipper is energized. The Game CPU will detect a switch closure if the flipper bat is forced back by a high velocity
shot or rebound on the playfield and will apply another 40msec pulse of 50v DC to the coil."
