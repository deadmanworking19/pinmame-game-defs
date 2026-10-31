# Elvis (Stern) — Cabinet / Coin Door Wiring Diagram

Read from `Elvis_Manual.pdf`, PDF page 125, printed `Section 5, Chapter 3, Page 108` ("Cabinet Wiring"), from a 200 dpi
render checked against the page's text layer. Only the parts that bear on switch, lamp and output identity are
transcribed; the speaker, printer, Sentinel and electronic-coin-mech blocks are summarised at the end.

## Cabinet matrix switches (CPU/SND BD. CN7 returns, CN5 drives)

| Switch label as printed | Return (CN7 pin, wire) | Drive (CN5 pin, wire) | Contact as printed |
| --- | --- | --- | --- |
| PLUMB BOB TILT SW. 56 | SW RETURN 8, pin 1, WHT-GRY | SW DRIVE 7, pin 8, GRN-VIO | N.O. |
| TOURNIE BUTTON SW. 55 | SW RETURN 7, pin 2, WHT-VIO | SW DRIVE 7, pin 8, GRN-VIO | N.O. |
| START BUTTON SW. 54 | SW RETURN 6, pin 3, WHT-BLU | SW DRIVE 7, pin 8, GRN-VIO | N.O. |

## Coin door switches (through the COIN DOOR CONNECTOR)

All share the drive "from CN5-P1 (Sw. Drive 1) GRN-BRN". The page prints "All Above Switches Normally Open (N.O.)".

| Return (CN7 pin, wire) | Coin door connector pin | Label as printed |
| --- | --- | --- |
| SW RETURN 7, pin 2, WHT-VIO | 2 | 5th Coin Slot Future Use |
| SW RETURN 6, pin 3, WHT-BLU | 3 | Left Coin Slot |
| SW RETURN 5, pin 5, WHT-GRN | 5 | U.S. Bill Acceptor Center Coin Slot |
| SW RETURN 4, pin 6, WHT-YEL | 6 | Right Coin Slot |
| SW RETURN 3, pin 7, WHT-ORG | 7 | 6th Coin Slot Future Use |
| SW RETURN 2, pin 8, WHT-RED | 8 | 4th Coin Slot European Use |

## Dedicated switches and memory protect (CPU/SND BD. CN6)

| CN6 pin, wire | Label as printed | Contact as printed |
| --- | --- | --- |
| 12, BLK-RED | Memory Protect Switch (closes to the BLK ground from CN7 pin 10) | N.O. |
| 10, GRY-BLK | D.S. 8 BEGIN TEST / ENTER: BLACK BUTTON (PORTALS™ SERVICE BUTTONS) | N.O. (printed once below D.S. 6) |
| 9, GRY-VIO | D.S. 7 SERVICE CREDITS / RT.: GREEN BUTTON | |
| 8, GRY-BLU | D.S. 6 VOLUME / LEFT: RED BUTTON | |
| 7, GRY-GRN | D.S. 5 UPPER RIGHT FLIPPER BUTTON | N.O. (printed once below D.S. 1) |
| 4, GRY-ORG | D.S. 3 RIGHT FLIPPER BUTTON | |
| 2, GRY-BRN | D.S. 1 LEFT FLIPPER BUTTON | |

The three flipper buttons are drawn as "DEDICATED SWITCHES" sharing one `BLK` ground.

## Outputs and lamps

- "TO COIN METER": "J16-7 +5V DC I/O DRVR BD" `22 RED` to pin 1; "J7-10 Q24 I/O DRVR BD" `78 VIO-GRY` to pin 2; pin 3
  `N/C`.
- "START / TOURNIE BUTTON LAMPS": "Lamp 80 Start" and "Lamp 79 Tournie", each with a diode, fed by `RED` from "J12 I/O
  PWR DRVR BD." pin 11, returning on `YEL-VIO` (J13 pin 3) and `YEL-GRY` (J13 pin 1).
- "G.I. LAMPS on COIN DOOR": two bulbs fed from "G.I. 5.7V AC" J15 pin 3 `WHT-GRN` and pin 8 `GRN` through the coin door
  connector as `YEL-WHT` and `YEL`.

## Coil power interlock switch

"COIL POWER INTERLOCK SWITCH": two N.O. contacts ganged by a dashed line. "20v DC COILS": "Normally Open - 1 RED-WHT 16V
AC" (I/O PWR DRVR BD. J17 pin 7) and "Common - 1 WHT-RED 16V AC" (TRANSFORMER (XFRMR)). "50v DC COILS": "Normally Open
- 2 BLK-YEL 48V AC" (I/O PWR DRVR BD. J11 pin 3) and "Common - 2 BLK-YEL 48V AC" (TRANSFORMER (XFRMR)).

## UK-only buttons

Boxed text, verbatim: "UK ONLY: 2 Extra Cabinet Buttons for the Post Save™ Feature are used. The Left Button operates
the Left Outlane Ball Deflector. The Right Button operates the Right Outlane Ball Deflector. Both buttons pushed together
operate the Center Up/Down Post. Both buttons are located under the Flipper Buttons."

The "UK ONLY" drawing: "LEFT BUTTON" N.O. on `WHT-BRN` (CN7 pin 9) and "RIGHT BUTTON" N.O. on `WHT-GRY` (CN7 pin 1),
both driven by `GRN-BRN` (CN5 pin 1).

## Other blocks (summarised)

"MONO SPEAKERS X3" (backbox left and right, cabinet bottom, on CPU/SND BD. CN4); "FOR THE PRINTER SUB-ASSEMBLY" and
"PRINTER INTERFACE OPTIONAL" (cable 036-5408-00, RS-232 board 520-5069-00); "FOR USE ONLY IN SENTINEL COIN DOOR"
(Sentinel Interface Board 520-5037-01); "Electronic Coin Mech. Interface Board, 520-5193-00"; "AMP CONNECTOR TO $ BILL
ACCEPTOR (DBA)" and "FOR USA 2 SLOT COIN DOOR ONLY" (115V AC line voltage, 1N4001 diode SPI part 112-5001-00).
