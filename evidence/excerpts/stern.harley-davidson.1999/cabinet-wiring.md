# Harley-Davidson (Stern) — Cabinet / Coin Door Wiring Diagram

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`, PDF page 106, printed `Section 5, Chapter
3, Page 90` ("Cabinet Wiring"). Read from a 200 dpi render and checked against the page's decoded text layer. Only the
switch, lamp, coil-power and driver blocks are transcribed; the speaker, printer, Sentinel and C120 blocks are listed by
title only.

## Matrix switches in the cabinet (CPU/SND BD. CN7 returns, CN5 drives)

| Drawn switch | Return wire | CN7 pin, "SW RETURN" | Drive | Contact |
| --- | --- | --- | --- | --- |
| PLUMB BOB TILT | WHT-GRY | 1, SW RETURN 8 | GRN-VIO, CN5-8, SW DRIVE 7 | N.O. |
| START BUTTON (drawn in red) | WHT-BLU | 3, SW RETURN 6 | GRN-VIO, CN5-8, SW DRIVE 7 | N.O. |
| LAUNCH (FIRE) BUTTON (drawn in red) | WHT-GRN | 5, SW RETURN 5 | GRN-VIO, CN5-8, SW DRIVE 7 | N.O. |
| 5th Coin Slot Future Use | WHT-VIO | 2, SW RETURN 7 | GRN-BRN, "from CN5-P1 (Sw. Drive 1)" | "All Above Switches Normally Open (N.O.)" |
| Left Coin Slot | WHT-BLU | 3, SW RETURN 6 | GRN-BRN, CN5-1 | N.O. |
| U.S. Bill Acceptor Center Coin Slot | WHT-GRN | 5, SW RETURN 5 | GRN-BRN, CN5-1 | N.O. |
| Right Coin Slot | WHT-YEL | 6, SW RETURN 4 | GRN-BRN, CN5-1 | N.O. |
| 6th Coin Slot Future Use | WHT-ORG | 7, SW RETURN 3 | GRN-BRN, CN5-1 | N.O. |
| 4th Coin Slot European Use | WHT-RED | 8, SW RETURN 2 | GRN-BRN, CN5-1 | N.O. |

The coin switches pass through the "COIN DOOR CONNECTOR" (CN7 pins 2, 3, 5-8 and CN5 pins 8 and 1 carried through).

## Dedicated switches and coin-door buttons (CPU/SND BD. CN6)

| Drawn switch | Wire | CN6 pin |
| --- | --- | --- |
| Memory Protect Switch (N.O., to BLK ground via CN7-10) | BLK-RED | 12 |
| PORTALS SERVICE BUTTONS: BEGIN TEST / ENTER: BLACK BUTTON | GRY-BLK | 10 |
| SERVICE CREDITS / RT.: GREEN BUTTON | GRY-VIO | 9 |
| VOLUME / LEFT: RED BUTTON | GRY-BLU | 8 |
| UPPER RIGHT FLIPPER BUTTON (label and wire drawn in red) | GRY-GRN | 7 |
| RIGHT FLIPPER BUTTON | GRY-ORG | 4 |
| LEFT FLIPPER BUTTON (N.O.) | GRY-BRN | 2 |

All drawn N.O.; the flipper buttons and service buttons return to BLK ground. The block is labelled "DEDICATED
SWITCHES".

## Outputs

- "TO COIN METER": "J16-7 +5VDC I/O DRVR BD 22 RED" to pin 1; "J7-10 Q24 I/O DRVR BD 78 VIO-GRY" to pin 2; pin 3 N/C.
- "LAUNCH (FIRE) BUTTON LAMP": "Lamp 47 Launch" (drawn in red), RED-BLU to "J12 I/O PWR DRVR BD." pin 6 through a diode,
  YEL-VIO to "J13" pin 3.
- "G.I. LAMPS on COIN DOOR": YEL-WHT and YEL, from "G.I. 6.3V AC" WHT-GRN "J15" pin 3 and GRN pin 8 ("I/O PWR DRVR BD.").
- "COIL POWER INTERLOCK SWITCH": "20v DC COILS" through Normally Open - 1 / Common - 1 (RED-WHT 16 VAC, WHT-RED 16 VAC,
  "I/O PWR DRVR BD. J17" pin 7, from the TRANSFORMER (XFMR)); "50v DC COILS" through Normally Open - 2 / Common - 2
  (BLK-YEL 48 VAC, "J11" pin 3). The two contacts are drawn ganged by a dashed line.

## Post Save buttons

- Boxed note: "UK ONLY: 2 Extra Cabinet Buttons for the Post Save™ Feature are used. The Left Button operates the Left
  Outlane Ball Deflector. The Right Button operates the Right Outlane Ball Deflector. Both buttons pushed together operate
  the Center Up/Down Post. Both buttons are located under the Flipper Buttons."
- Box "LEFT UK ONLY": LEFT BUTTON (N.O.) on WHT-BRN to "CN7" pin 9; RIGHT BUTTON (N.O.) on WHT-GRY to "CN7" pin 1; both
  driven by GRN-BRN from "CN5" pin 1 ("CPU/SND BOARD").
- Vertical note beside it: "USA ONLY: The Extra Right Button is used to operate the Up/Down Center Post."

Other blocks on the page, by title: "MONO SPEAKERS X3" (CN4), "FOR THE PRINTER SUB-ASSEMBLY", "FOR USA 2 SLOT COIN DOOR
ONLY" (bill acceptor connector), "FOR USE ONLY IN SENTINEL COIN DOOR", "FOR C120 INTERFACE BOARD", "PRINTER INTERFACE
OPTIONAL".
