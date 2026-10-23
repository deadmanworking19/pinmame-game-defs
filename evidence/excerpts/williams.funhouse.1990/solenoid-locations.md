# FunHouse — Solenoids and General Illumination (printed page 2-40)

Source: `Funhouse_OPS.pdf`, PDF page 101 (printed "2-40"), rendered at 300 dpi and read directly
from the image. Full "No. / Coil-Bulb / Description" table, both the Solenoids block and the
General Illumination block printed beneath it on the same page.

## Solenoids

| No. | Coil/Bulb | Description |
| --- | --- | --- |
| 01 | AE-26-1200 | Outhole |
| 02 | AE-26-1200 | Ramp Diverter |
| 03 | AE-26-1500 | Kickbig |
| 04 | AE-26-1200 | Tunnel Kickbig |
| 05 | AE-26-1500 | Trap Door Open |
| 06 | SM1-26-600 | Trap Door Closed |
| 07 | AE-23-800 | Knocker |
| 08 | A-14189 | Multi-ball Release |
| 09 | AE-26-1200 | Left Jet Bumper |
| 10 | AE-26-1200 | Right Jet Bumper |
| 11 | AE-26-1200 | Lower Jet Bumper |
| 12 | AE-26-1500 | Left Kicker |
| 13 | AE-26-1500 | Right Kicker |
| 14 | SZ-34-3500 | Steps Gate |
| 15 | AE-26-1200 | Trough |
| 16 | AE-26-1500 | Dummy Eject Hole |
| 17 | #906 | 3 Blue Flashers |
| 18 | #906 | Dummy Flashers |
| 19 | #906 | 2 Clock Flashers |
| 20 | #906 | 2 Superdog Flashers |
| 21 | A-13997 | Mouth Motor |
| 22 | C-13963 | Up/Down Driver |
| 23 | #906 | 3 Red Flashers |
| 24 | #906 | 3 Clear Flashers |
| 25 | SM-30-1100 | Eyes Right |
| 26 | SM-30-1100 | Eyelids Open |
| 27 | SM-30-1100 | Eyelids Close |
| 28 | SM-30-1100 | Eyes Left |

Every one of the 28 printed solenoid rows names a real coil or motor part number; no "Not Used"
row appears on this page (unlike the switch table, which lists several unused matrix positions).
"Kicker" (12/13) is this manual's term for the slingshot coils; the switch-locations page
(`switch-locations.md`) confirms the pairing directly with "Left (sling) Kicker" / "Right (sling)
Kicker" at addresses 41/53, and the switch-matrix page (`switch-matrix.md`) spells it out in full
as "Left Slingshot (Kicker)" / "Right Slingshot (Kicker)".

## General Illumination

| No. | Bulb | Description |
| --- | --- | --- |
| 01 | #555 | Upper Backglass G.I. |
| 02 | #555 | Front Playfield G.I. |
| 03 | #555 | Rear Playfield G.I. |
| 04 | #555 | Cntr Bckglss/Rt. Rr Plfld G.I. |
| 05 | #555 | Top Playfield G.I. |

Five printed G.I. circuits, numbered 01-05; PinMAME exposes them at zero-based public addresses 0-4. The names of 02, 04 and 05 do not belong to those strings. The L-9 ROM's T.6 G.I. test names the five public strings BACKGLASS UPPER, RUDY / BACKGLASS, REAR PLAYFIELD, BACKGLASS CENTER and FRONT PLAYFIELD (`evidence/runtime/wpc-alpha/funhouse-fh_l9-gi-test.json`), and the retained script drives Rudy from 1, the rear playfield from 2 and the front playfield from 4. "Front Playfield" is public 4's name, "Cntr Bckglss/Rt. Rr Plfld" (centre backglass plus Rudy's spotlight at the right rear) is public 1's, and "Top Playfield" stands where the ROM names public 3 BACKGLASS CENTER. The November 1990 handbook prints the same names beside the wires of those strings; `operator-handbook-switch-gi-evidence.md` gives the full reconciliation.

The accompanying playfield diagram (right half of the page) labels each solenoid's location by number. The November 1990 handbook prints the same drawing at 600 dpi; the definition's callout check reads that copy (`operator-handbook-solenoid-locations.md`). Circuits 17, 23, and 24 have one distinct retained emitter per printed bulb. Circuit 19's two Clock bulbs sit under the clock centre, where the drawing prints 19 once and the retained table models one fixture, so they share one placement. Circuit 20 instead has distinct `F20` and `F20a` Light objects, and the pinned community script assigns both to output 20, so its two Superdog bulbs retain separate measured placements.
