# Centaur — AS-2518-43 Auxiliary Lamp Driver A9, connector J2

Transcribed from `Bally_1981_Centaur_Installation_and_General_Game_Operation_Instructions_with_schematics_OCR_searchable.pdf`,
PDF page 51, drawing **W-1207-11**. The accompanying crop is the same region.

The board is generic Bally hardware, so its internal wiring is the same on every machine that
carries one; only the functions printed against the J2 pins are game-specific.

## Structure

Each lamp data line enables one MC14555B decoder half, and the two latched address bits select one
of its outputs:

| data line | decoder half |
| --- | --- |
| PD0 | U2A |
| PD1 | U2B |
| PD2 | U3A |
| PD3 | U3B |

**`Q3` is marked `N/U` on all four halves.** That is why latched address 3 reaches no bulb, and why
public lamps 68, 84, 100 and 116 are bare matrix positions rather than unused lamps.

## Decoder output to SCR to connector pin, with printed function

| half | output | resistor | SCR | J2 pin | printed function |
| --- | --- | --- | --- | --- | --- |
| U2A | Q0 | R14 | Q6 | 7 | TOP LEFT LANE |
| U2A | Q1 | R13 | Q5 | 6 | RIGHT SLINGSHOT |
| U2A | Q2 | R12 | Q4 | 5 | #1 CHAMBER (2) (FROM BOTTOM) |
| U2A | Q3 | — | — | — | N/U |
| U2B | Q0 | R9 | Q1 | 1 | TOP MIDDLE LANE |
| U2B | Q1 | R10 | Q2 | 2 | LEFT SLINGSHOT |
| U2B | Q2 | R11 | Q3 | 3 | #2 CHAMBER (2) |
| U2B | Q3 | — | — | — | N/U |
| U3A | Q0 | R20 | Q12 | 18 | TOP RIGHT LANE |
| U3A | Q1 | R19 | Q11 | 19 | RIGHT THUMPER BUMPER |
| U3A | Q2 | R18 | Q10 | 20 | #3 CHAMBER (2) |
| U3A | Q3 | — | — | — | N/U |
| U3B | Q0 | R15 | Q7 | 11 | *(blank on the sheet)* |
| U3B | Q1 | R16 | Q8 | 12 | LEFT THUMPER BUMPER |
| U3B | Q2 | R17 | Q9 | 17 | #4 CHAMBER (2) (TOP) |
| U3B | Q3 | — | — | — | N/U |

Other J2 pins: `4 KEY`, `8 GND`, `9 GND`, and `10`, `13`, `14`, `15`, `16` marked `N/U`.

## What this side of the sheet does and does not settle

**The decoder-to-pin chain.** With `public = 64 + 16k + address + 1`, the chain above puts public
65 on `J2-7`, 81 on `J2-1`, 97 on `J2-18` and 113 on `J2-11`, and likewise for the Q1 and Q2 rows.
The ROM confirms the data-line half of it in play: a struck right slingshot (switch 37) flicks 66,
the left slingshot (38) flicks 82, the right thumper bumper (39) flicks 98 and the left (40) flicks
114, each the lamp this sheet prints on that row.

**The outer top-lane labels do not survive the ROM.** The sheet prints TOP LEFT LANE against `J2-7`
(public 65) and TOP RIGHT LANE against `J2-18` (public 97). The ROM lights 97 when the top left lane
rollover (switch 5, at the left lane in the switch table and in Figure V) closes, and 65 for the top
right lane (switch 3). A lit top lane is a made lane, so the lamp that lights for the left rollover
is the left lane's lamp: the two outer labels are transposed on this sheet, and on the harness
drawing W-1255-2 that copies them. The retained tables bind 97 to the left insert and 65 to the
right; an earlier pass of this record called that a table mistake, which the ROM shows it is not.

**Pin 11 is blank because nothing is plugged onto it.** It carries a real SCR and series resistor
exactly like its eleven siblings, but no function is printed against it, while the pins this sheet
calls unused (`10`, `13`, `14`, `15`, `16`) are marked `N/U`. The harness side of the same sheet,
transcribed in `a9-harness-j2-list.md`, draws a cable branch on exactly the eleven pins that print a
function and none on pin 11, and a photograph of a Centaur's own A9 board shows no wire in that
position. Public 113 is a built but unwired circuit.
