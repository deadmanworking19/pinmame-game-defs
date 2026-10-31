# Terminator 3 — Cabinet / Coin Door Wiring Diagram

Read from `Stern_2003_Terminator_3_Rise_of_the_Machines_Pinball_Game_Service_Manual.pdf`, PDF page 126, printed
`Section 5, Chapter 3, Page 108` ("Cabinet / Coin Door Wiring Diagram"), from a 150 dpi render.

## Matrix switches in the cabinet and coin door

| CPU/SND BD. return | Wire | Switch as printed | Contact | Drive |
| --- | --- | --- | --- | --- |
| CN7 pin 1, SW RETURN 8 | WHT-GRY | PLUMB BOB TILT | N.O. | CN5 pin 8, SW DRIVE 7, GRN-VIO |
| CN7 pin 2, SW RETURN 7 | WHT-VIO | (none drawn on the cabinet side) | | |
| CN7 pin 3, SW RETURN 6 | WHT-BLU | START BUTTON | N.O. | SW DRIVE 7 |
| CN7 pin 5, SW RETURN 5 | WHT-GRN | TOURNIE BUTTON | N.O. | SW DRIVE 7 |
| CN7 pin 6, SW RETURN 4 | WHT-YEL | (none drawn on the cabinet side) | | |
| CN7 pin 7, SW RETURN 3 | WHT-ORG | (none drawn on the cabinet side) | | |
| CN7 pin 8, SW RETURN 2 | WHT-RED | (none drawn on the cabinet side) | | |

The COIN DOOR CONNECTOR block ("from CPU CN7 Pin:" and "from CPU CN5 Pin:") carries, on `SW DRIVE 1` (`from CN5-P1 (Sw.
Drive 1) GRN-BRN`):

| CN7 pin | Wire | Switch as printed |
| --- | --- | --- |
| 2 | WHT-VIO | 5th Coin Slot Future Use |
| 3 | WHT-BLU | Left Coin Slot |
| 5 | WHT-GRN | U.S. Bill Acceptor Center Coin Slot |
| 6 | WHT-YEL | Right Coin Slot |
| 7 | WHT-ORG | 6th Coin Slot Future Use |
| 8 | WHT-RED | 4th Coin Slot European Use |

"All Above Switches Normally Open (N.O.)"

## Dedicated switches (CPU/SND BD. CN6)

| CN6 pin | Wire | Switch as printed | Contact |
| --- | --- | --- | --- |
| 12 | BLK-RED | Memory Protect Switch | N.O. |
| 10 | GRY-BLK | BEGIN TEST / ENTER: BLACK BUTTON | N.O. |
| 9 | GRY-VIO | SERVICE CRED-ITS / RT.: GREEN BUTTON | N.O. |
| 8 | GRY-BLU | VOLUME / LEFT: RED BUTTON | N.O. |
| 7 | GRY-GRN | (no switch drawn) | |
| 4 | GRY-ORG | RIGHT FLIPPER BUTTON | (drawn open) |
| 2 | GRY-BRN | LEFT FLIPPER BUTTON | N.O. |

The three coin-door buttons are grouped as "PORTALS™ SERVICE BUTTONS"; CN6 pins 2 and 4 are labelled "DEDICATED
SWITCHES". Ground: CN7 pin 10 `BLK`.

## Other cabinet circuits

- "G.I. 5.7V AC" from `J15` pin 3 `WHT-GRN` and pin 8 `GRN`, through `YEL-WHT` and `YEL`, to two "G.I. LAMPS on COIN
  DOOR".
- "START / TOURNIE BUTTON LAMPS": `Lamp 53 Start` and `Lamp 54 Tournie`, each with a diode; `RED-VIO` to `J12` pin 7
  ("I/O PWR DRVR BD."), `YEL-BLU` to `J13` pin 6, `YEL-GRN` to `J13` pin 5.
- "TO COIN METER": `J16-7 +5V DC I/O DRVR BD 22 RED` to pin 1, `J7-10 Q24 I/O DRVR BD 78 VIO-GRY` to pin 2, pin 3 `N/C`.
- "COIL POWER INTERLOCK SWITCH": "20V DC COILS" through `J17` pin 7 (`Normally Open - 1 RED-WHT 16V AC`, `Common - 1 WHT-RED
  16V AC`) and "50V DC COILS" through `J11` pin 3 (`Normally Open - 2 BLK-YEL 48V AC`, `Common - 2 BLK-YEL 48V AC`), both
  `N.O.`, ganged by a dashed line.
- "MONO SPEAKERS X3": `BACKBOX LEFT SPEAKER (SP2)`, `BACKBOX RT. SPEAKER (SP2)`, `CABINET BOT. SPEAKER (SP3)` from CPU/SND
  BD. CN4.
- "UK ONLY: 2 Extra Cabinet Buttons for the Post Save™ Feature are used. The Left Button operates the Left Outlane Ball
  Deflector. The Right Button operates the Right Outlane Ball Deflector. Both buttons pushed together operate the Center
  Up/Down Post. Both buttons are located under the Flipper Buttons." The UK ONLY box draws `LEFT BUTTON` (`N.O.`,
  `WHT-BRN` to CN7 pin 9) and `RIGHT BUTTON` (`N.O.`, `WHT-GRY` to CN7 pin 1), both returning on `GRN-BRN` to CN5 pin 1.
- Also drawn: "FOR USA 2 SLOT COIN DOOR ONLY" (bill acceptor connector, 115V AC line voltage, 1N4001 diode SPI part No.
  112-5001-00, CN7 SW RET 5, CN5 SW DRV 1), "FOR USE ONLY IN SENTINEL COIN DOOR" (Sentinel Interface Board 520-5037-01),
  "FOR C120 INTERFACE BOARD", "FOR THE PRINTER SUB-ASSEMBLY" and "PRINTER INTERFACE OPTIONAL".
