# South Park — Cabinet / Coin Door Wiring Diagram

Read from `Sega_1999_South_Park_Manual_English.pdf`, PDF page 52 (left half), printed Section 5 page 88, "Cabinet /
Coin Door Wiring Diagram", from a 220 dpi render of the scan.

Matrix switches through the COIN DOOR CONNECTOR (every switch drawn as a normally open contact):

| Switch as printed | Return | Return wire | Drive | Drive wire |
| --- | --- | --- | --- | --- |
| PLUMB BOB TILT | SW RETURN 8, CPU BD CN7 pin 1 | WHT-GRY | SW DRIVE 7, CPU BD CN5 pin 8 | GRN-VIO |
| START BUTTON | SW RETURN 6, CN7 pin 3 | WHT-BLU | SW DRIVE 7 | GRN-VIO |
| Slam Tilt | SW RETURN 7, CN7 pin 2 | WHT-VIO | SW DRIVE 7 ("from CN5-P8 (Sw. Drive 7)") | GRN-VIO |
| 5th Coin Slot Future Use | SW RETURN 7 | WHT-VIO | SW DRIVE 1 ("from CN5-P1 (Sw. Drive 1)") | GRN-BRN |
| Left Coin Slot | SW RETURN 6 | WHT-BLU | SW DRIVE 1 | GRN-BRN |
| U.S. Bill Acceptor Center Coin Slot | SW RETURN 5, CN7 pin 5 | WHT-GRN | SW DRIVE 1 | GRN-BRN |
| Right Coin Slot | SW RETURN 4, CN7 pin 6 | WHT-YEL | SW DRIVE 1 | GRN-BRN |
| 6th Coin Slot Future Use | SW RETURN 3, CN7 pin 7 | WHT-ORG | SW DRIVE 1 | GRN-BRN |
| 4th Coin Slot European Use | SW RETURN 2, CN7 pin 8 | WHT-RED | SW DRIVE 1 | GRN-BRN |

Dedicated and service inputs:

- Memory Protect Switch: CPU BD CN6 pin 12, BLK-RED, to BLK (ground, CPU BD CN7 pin 10).
- PORTALS™ SERVICE BUTTONS: CN6 pin 10 GRY-BLK "BEGIN TEST / ENTER: BLACK BUTTON"; pin 9 GRY-VIO "SERVICE CREDITS / RT.:
  GREEN BUTTON"; pin 8 GRY-BLU "VOLUME / LEFT: RED BUTTON".
- CN6 pin 7 GRY-GRN runs to the coin door connector with no switch drawn.
- DEDICATED SWITCHES: RIGHT FLIPPER BUTTON on CN6 pin 4 GRY-ORG and LEFT FLIPPER BUTTON on pin 2 GRY-BRN, both to BLK.

Outputs and lamps:

- G.I. LAMPS on COIN DOOR: two bulbs on YEL-WHT and YEL, fed from I/O DRVR BD J15 pins 3 and 8 (WHT-GRN, GRN), "G.I. 6.3V AC".
- TO COIN METER: "J16-7 +5VDC I/O DRVR BD 22 RED" to pin 1, "J7-10 Q24 I/O DRVR BD 78 VIO-GRY" to pin 2, pin 3 N/C.
- The page draws no Start-button lamp.

Boxes on the page:

- "EXTRA CABINET BUTTONS (SAV-A-BALL)", "✻✻✻ UK ONLY ✻✻✻": LEFT SAV-A-BALL and RIGHT SAV-A-BALL, each N.O., share
  GRN-BRN from CPU/SND CN5 pin 1; the left returns on WHT-BRN, printed beside CPU/SND CN7 pin "1", the right on WHT-GRY,
  printed beside pin "9". The Switch Matrix Grid (DR. 4) puts WHT-BRN on CN7-P9 and WHT-GRY on CN7-P1, so the two pin
  numbers in this box are crossed against the grid; the wire colours agree with it.
- "COIL POWER INTERLOCK SWITCH": two normally open sections, one in the 20v DC coil supply (I/O DRVR BD J17 pin 7,
  RED-WHT and WHT-RED 16 VAC) and one in the 50v DC coil supply (J11 pin 3, BLK-YEL 48 VAC).
- "FOR USA 2 SLOT COIN DOOR ONLY": 115v AC to the $ bill validator, SW DRV 1 GRN-BRN and SW RET 5 WHT-GRN through a
  112-5001-00 1N4001 diode.
- "FOR USE ONLY IN SENTINEL COIN DOOR", "MONO SPEAKERS X3" and "PRINTER INTERFACE OPTIONAL" boxes carry no playfield
  devices.
