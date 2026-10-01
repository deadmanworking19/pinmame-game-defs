# Wreck Ball Target Assembly (printed page 2-29)

Source: Williams Junk Yard (1996) Operations Manual, PDF page 105, printed page **2-29**.
Read from a native-resolution render (the page is a 200 dpi 1-bit scan, rendered at 200 dpi). The
drawing is a wiring and assembly drawing, so a rendered crop of it is retained beside this file
(`wreck-ball-target-assembly.webp`).

Title as printed: `A-21247` / `Wreck Ball Target Assembly`

## Parts table

Table header as printed: `Item` | `Part Number` | `Description`

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | A-21519 | Target Switch Assembly |
| 2 | H-21374.1 | Cable |
| 3 | 03-9255-3 | Spacer #8 x .541" Long |
| 4 | 31-2593 | Wreck Ball Target Cover |
| 5 | 4008-01113-14 | Mach. Screw, 8-32 x .875" |
| 6 | 4008-01113-04 | Mach. Screw, 8-32 x ¼" |

## Drawing

The left half of the drawing is a plan view of a semicircular bracket carrying target switches
around its inside, with callouts `1` (the arc), `4` (a cover at the upper end) and `9` (a cover at
the lower end). The parts table has no item 9; the callout is transcribed as printed. A circular
inset at the left shows a fastener stack with callouts `5`, `4 REF.`, `3` and `1 REF.`.

The right half is a side view of five target switches on a straight bracket, all wired into one
connector, callout `2` (the Cable). Each switch carries two labelled wires. Reading the switches
from top to bottom, the labels that lead to each one are:

| Switch (top to bottom) | Wire labels as printed |
| --- | --- |
| 1 | WHT-YEL, GRN-BLK |
| 2 | WHT-ORG, GRN-BLK |
| 3 | WHT-GRY, GRN-WHT |
| 4 | WHT-VIO, GRN-WHT |
| 5 | WHT-BLU, GRN-WHT |

Where two wires cross on their way to switches 1 and 2, the label positions make the WHT-YEL wire
end at switch 1 and the WHT-ORG wire at switch 2.

## Reading the wires against the switch matrix

The WPC-95 switch-matrix page of this manual (2-34) gives the return-row wires as row 3
White-Orange, row 4 White-Yellow, row 6 White-Blue, row 7 White-Violet and row 8 White-Gray, and
the column 5 drive wire as Green-Black. So switches 1 and 2 are column 5 rows 4 and 3, which the
Switch Locations page (2-35) names Car Target 5 (Right) and Car Target 4.

Switches 3 to 5 are rows 8, 7 and 6 on a drive wire printed GRN-WHT. The switch-matrix page prints
column 4 as Green-Yellow, so GRN-WHT is not that page's colour. Column 4 rows 6, 7 and 8 are Car
Target 1 (Left), Car Target 2 and Car Target 3, and these five addresses are exactly the five
switches the Switch Locations page footnotes `***ABOVE CRANE`. In the T.1 SWITCH EDGES test the
production `jy_11` and `jy_12` ROMs also print GRN-WHT as the column wire of column-4 switches,
while the `jy_03` prototype prints GRN-YEL.
