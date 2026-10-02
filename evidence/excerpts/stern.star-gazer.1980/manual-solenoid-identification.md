# Star Gazer — solenoid identification, self-test display numbers

Transcribed from `Stern_1980_Star_Gazer_Manual.pdf`, PDF page 20 (printed page 19), read from the rendered scan. The page is titled "STAR GAZER / SOLENOID IDENTIFICATION / SELF TEST DISPLAY NUMBERS". The left column is the number the ROM's solenoid self test shows on the player score display as it energises each driver; the schematic's own note says that number "is Drive Transistor (Q) Position on SDU". It is a test order and a driver position, never a PinMAME public address.

| SOLENOID NO. | SOLENOID LOCATION |
| ---: | --- |
| 1 | LEFT SLING-SHOT |
| 2 | RIGHT SLING-SHOT |
| 3 | KNOCKER |
| 4 | LEFT DROP TARGET |
| 5 | TOP DROP BANK |
| 6 | RIGHT DROP BANK |
| 7 | LEFT THUMPER |
| 8 | MIDDLE THUMPER |
| 9 | RIGHT THUMPER |
| 10 | OUT-HOLE |
| 11 | OPEN |
| 12 | OPEN |
| 13 | OPEN |
| 14 | OPEN |
| 15 | ENABLE REPLAY |
| 16 | OPEN |
| 17 | OPEN |
| 18 | OPEN |
| 19 | COIN LOCKOUT |
| 20 THRU 29 | SOUND |

"OPEN" is the page's own word for a driver position with nothing connected. Number 15 is printed "ENABLE REPLAY"; the schematic names the load wired at that position the flipper enable relay, so the printed words are kept here literally and the disagreement is stated on the device.

The page after this table is a playfield drawing numbering each solenoid at its position; it is transcribed in the solenoid-locations excerpt.

## PDF page 16 (printed page 15): parts list, assembly coils

The same manual's parts list ("STAR GAZER #127") prints these coil assemblies and modules, copied here with their printed spelling:

| item | part number |
| --- | --- |
| Coin Lockout | C-36-5300 |
| Flipper (L & R) | J-25-475/34-4500 |
| Knocker | N-26-1200 |
| Outhole Kicker (1) | JX-26-1200 |
| Thumper Bumper (3) | J-26-1200 |
| Slingshot (2) | J-26-1200 |
| Drop Target Reset (3) | B-27-2300 |
| Lamp Driver | B-431 |
| Display Driver (5 Used) | C-645 |
| Solenoid Driver/Voltage Regulator | B-432 |
| MPU | C-602 |
| Power Supply p.c. assembly | A-430 |
| Sound Module | C-605 |

The list has no ball-kicker coil and no replay-enable coil: no coil assembly exists for the positions the page calls OPEN, nor for a replay enable.
