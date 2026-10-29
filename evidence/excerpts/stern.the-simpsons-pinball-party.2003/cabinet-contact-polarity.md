# The Simpsons Pinball Party — physical contact construction

Source: Stern operations manual, SHA256 `412023c67f699d68c10c6a70120712d34d71417b7dd16f1662e252a66561c898`.
Method: mixed; complete relevant contact-diagram transcription and factual technical-overview paraphrase. Transcribed and visually reviewed by pinmame-game-defs curation against the factory pages on 2026-10-29. Contact construction is independent of the emulator's public state.

## PDF126 / printed108 — Cabinet/Coin Door Wiring Diagram

### Full upper cabinet/coin contact region

All entries below are explicitly N.O. or are covered by the exact coin-region note **“All Above Switches Normally Open (N.O.)”**. Matrix contacts join a scanned drive to a return. They are not literal ground closures.

| Physical contact | Rest state | CPU return wire/pin | Common drive wire/pin | Matrix address from own PDF30 table |
|---|---|---|---|---|
|PLUMB BOB TILT|N.O.|WHT-GRY/CN7-P1, SW RETURN8|GRN-VIO/CN5-P8, SW DRIVE7|56|
|START BUTTON|N.O.|WHT-BLU/CN7-P3, SW RETURN6|GRN-VIO/CN5-P8, SW DRIVE7|54|
|TOURNIE BUTTON|N.O.|WHT-GRN/CN7-P5, SW RETURN5|GRN-VIO/CN5-P8, SW DRIVE7|53|
|5th Coin Slot, Future Use|N.O., group note|WHT-VIO/CN7-P2, SW RETURN7|GRN-BRN/CN5-P1, SW DRIVE1|7|
|Left Coin Slot|N.O., group note|WHT-BLU/CN7-P3, SW RETURN6|GRN-BRN/CN5-P1, SW DRIVE1|6|
|U.S. Bill Acceptor / Center Coin Slot|N.O., group note|WHT-GRN/CN7-P5, SW RETURN5|GRN-BRN/CN5-P1, SW DRIVE1|5|
|Right Coin Slot|N.O., group note|WHT-YEL/CN7-P6, SW RETURN4|GRN-BRN/CN5-P1, SW DRIVE1|4|
|6th Coin Slot, Future Use|N.O., group note|WHT-ORG/CN7-P7, SW RETURN3|GRN-BRN/CN5-P1, SW DRIVE1|3|
|4th Coin Slot, European Use|N.O., group note|WHT-RED/CN7-P8, SW RETURN2|GRN-BRN/CN5-P1, SW DRIVE1|2|

The coin-door connector carries the same pin numbers2,3,5,6,7,8 for these six returns. Its pin1 carries GRN-BRN from CPU CN5-P1 (Sw. Drive1). A separate pin8 connection carries GRN-VIO from CPU CN5-P8 for start/tournament/tilt; these are distinct connector groups on the drawing and must not be collapsed merely because both bear pin8 labels.

### Full dedicated contact region, PDF126

The three cabinet flipper contacts and the three Portals service contacts are N.O. The common is BLK ground, shown connected to CPU CN7-P10 and to the coin-door/service ground wiring. The corresponding DS rows and CN6 pins are fully listed in the companion flipper-construction.md excerpt. The drawing calls the DS-5 contact **TOP RIGHT FLIPPER BUTTON**; PDF124 calls it UPPER RIGHT FLIPPER.

The **Memory Protect Switch** is also drawn and labelled N.O.; its input is BLK-RED on CPU CN6-P12 and its common is BLK ground. This is the contact state shown by the factory drawing. The canonical definition assigns switch.memory-protect public address -3 from se.h's SE_SWMEMORYPROTECT constant; se.c samples it directly with core_getSw to gate protected RAM writes. That controller number comes from the emulator source, not this factory drawing.

### Full UK contact region, PDF126

| UK-only physical contact | Rest state | CPU CN7 return | CPU CN5 common |
|---|---|---|---|
|LEFT BUTTON|N.O.|P9/WHT-BRN|P1/GRN-BRN|
|RIGHT BUTTON|N.O.|P1/WHT-GRY|P1/GRN-BRN|

The complete UK note says two extra cabinet buttons operate the Post Save feature. Left operates the Left Outlane Ball Deflector; right operates the Right Outlane Ball Deflector; both together operate the Center Up/Down Post. Both buttons are under the Flipper Buttons.

### Remaining physical switch contacts on PDF126

The two mechanically linked **COIL POWER INTERLOCK SWITCH** contacts are N.O. These are power contacts, not extra CPU switch inputs:

| Pole/application | Printed normally-open terminal | Printed common terminal | Board feed |
|---|---|---|---|
|Normally Open1 /20vDC coils|RED-WHT16VAC|WHT-RED16VAC|I/O driverJ17-P7|
|Normally Open2 /50vDC coils|BLK-YEL48VAC|BLK-YEL48VAC|I/O driverJ11-P3|

The lower Sentinel/C120 interface connector diagrams do not add physical contact rest states. In particular, **N.C. printed at a connector pin means an unused/not-connected pin in that connector context, not an EOS-style normally-closed switch symbol**. The coin-meter block uses N/C in the same connector sense. Do not turn those connector labels into invented NC contacts.


## Drawing crop

`cabinet-contact-polarity.webp`: The_Simpsons_Manual.pdf page 126, crop box 0.02,0.02,0.97,0.94, born-digital page rendered for legibility (smallest type in region 3.0pt, targeting 11px glyphs), rendered at 186 dpi, capped to 1500px wide, grayscale, 1501x1881 WebP quality 70.
