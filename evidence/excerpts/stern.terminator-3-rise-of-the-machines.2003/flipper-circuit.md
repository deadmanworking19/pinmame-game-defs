# Terminator 3 — 2-Flipper Circuit Wiring Diagram

Read from `Stern_2003_Terminator_3_Rise_of_the_Machines_Pinball_Game_Service_Manual.pdf`, PDF page 124, printed
`Section 5, Chapter 2, Page 106` ("2-Flipper Circuit Wiring Diagram"), from a 150 dpi render.

## Drawing

- `CPU-SOUND BOARD (PARTIAL VIEW)`, `CN6`, "DEDICATED SWITCH INPUTS (SWITCH TO GROUND)", pins numbered `1 2 3 4 6 12`.
  Wires to CN6, left to right: `GRY-YEL`, `GRY-ORG`, `GRY-RED`, `GRY-BRN`.
- `RIGHT FLIPPER IN CABINET DEDICATED SWITCH DS-3`, marked `N.O.`, on `GRY-ORG`.
- `LEFT FLIPPER IN CABINET DEDICATED SWITCH DS-1`, marked `N.O.`, on `GRY-BRN`.
- `RIGHT E.O.S. ON ASSY. DEDICATED SWITCH DS-4`, marked `N.C.`, on `GRY-YEL`.
- `LEFT E.O.S. ON ASSY. DEDICATED SWITCH DS-2`, marked `N.C.`, on `GRY-RED`.
- The other side of all four switches joins on `BLK (GROUND)` to `J16` pin 11 ("POWER OUT J16", pins `1 11 15`).
- "NOTE: N.C. = Normally Closed N.O. = Normally Open".
- `I/O POWER DRIVER BOARD (PARTIAL VIEW)`: `MOS FET STP20N10L` transistors `Q13`, `Q14`, `Q15`, `Q16`; `J9 HIGH CURRENT
  SOLENOIDS` pins `9 8 … 1`; `J10 VOLTAGE OUTPUTS` pins `10 … 2 1`, with `↕ RED-YEL 50V DC ↕` from J10 pins 1 and 2.
- `LOWER RIGHT FLIPPER COIL`, `22-1080`, "Coil Wrap: YEL-GRN", drive wire `ORG-VIO` to J9; power through a `3A
  SLO-BLO (Located under Playfield)` fuse, `RED-YEL 50V DC` to `BLU-YEL`.
- `LOWER LEFT FLIPPER COIL`, `22-1080`, "Coil Wrap: YEL-GRN", drive wire `ORG-GRY` to J9; power through a `3A SLO-BLO
  (Located under Playfield)` fuse, `RED-YEL 50V DC` to `GRY-YEL`.
- Each coil is drawn as a single winding with one diode across it.
- Note beside the fuses: "The 3A 250v Slo-Blo Fuses are located under the playfield NEAR the Flipper Assembly, see previous
  page for locations."

## Text

"The Outside LEFT FLIPPER BUTTON located on the Cabinet operates the Left Flipper. The Outside RIGHT FLIPPER BUTTON located
on the Cabinet operates the Right Flipper."

"Technical Overview — Our Flipper System uses one supply voltage (50v DC) for both kick & hold. Once the Game CPU detects a
Flipper Cabinet Switch closure (during game play) it applies a 40msec pulse to the gate of the Flipper Drive Transistor
(STP-20N10L). If it continues to detect a Flipper Cabinet Switch closure (the player holding the button in) it will
continue to pulse the flipper drive transistor 1msec every 12msecs for the duration of the hold cycle.

The E.O.S. (End-Of-Stroke) Switch serves the same function as before as it prevents foldback when the player has the
flipper energized to capture balls. The E.O.S. Switch is a normally closed switch which opens approximately 1/16" when the
flipper is energized. The Game CPU will detect a switch closure if the flipper bat is forced back by a high velocity shot
or rebound on the playfield and will apply another 40msec pulse of 50v DC to the coil."
