# Gold — Solenoid/Flasher Table

Gold Operations Manual PDF page 122, printed 3-6. Complete table region visually checked against page-122.png. The separate G.I. block follows below; blanks are explicit `---`. Names, printed types (including motors printed as Flasher), supply connectors and transistor IDs are literal; separators normalized to `/` where two connectors share a row.

| Sol. | Function | Type | Wire | Connection | Driver | Part number |
| ---: | --- | --- | --- | --- | --- | --- |
| 01 | Chair Kickout | High Power | Vio-Brn | J130-1 | Q82 | AE-26-1200 |
| 02 | Thing Knocker | High Power | Vio-Red | J132-2 | Q80 | AE-23-800 |
| 03 | Ramp Diverter | High Power | Vio-Orn | J130-4 | Q78 | AE-26-1500 |
| 04 | Ball Release | High Power | Vio-Yel | J130-5 | Q76 | AE-26-1200 |
| 05 | Outhole | High Power | Vio-Grn | J130-6 | Q64 | AE-27-1200 |
| 06 | Thing Magnet | High Power | Vio-Blu | J130-7 | Q66 | A-12158-1 |
| 07 | Thing Kickout | High Power | Vio-Blk | J130-8 | Q68 | AE-23-800 |
| 08 | Lockup Kickout | High Power | Vio-Gry | J130-9 | Q70 | AE-26-1200 |
| 09 | Upper Left Jet | Low Power | Brn-Blk | J127-1 | Q58 | AE-26-1200 |
| 10 | Upper Right Jet | Low Power | Brn-Red | J127-3 | Q56 | AE-26-1200 |
| 11 | Center Left Jet | Low Power | Brn-Org | J127-4 | Q54 | AE-26-1200 |
| 12 | Center Right Jet | Low Power | Brn-Yel | J127-5 | Q52 | AE-26-1200 |
| 13 | Lower Jet | Low Power | Brn-Grn | J127-6 | Q50 | AE-26-1200 |
| 14 | Left Slingshot | Low Power | Brn-Blu | J127-7 | Q48 | AE-27-1200 |
| 15 | Right Slingshot | Low Power | Brn-Vio | J127-8 | Q46 | AE-27-1200 |
| 16 | Left Magnet | Low Power | Brn-Gry | J127-9 | Q44 | 20-9247 12V |
| 17 | Telephone/Upper Right Ramp | Flasher | Blk-Brn | J126-1 / J125-1 | Q42 | #906 |
| 18 | Train/Upper Left Ramp | Flasher | Blk-Red | J126-2 / J125-2 | Q40 | #906 |
| 19 | Lower Ramp/Jet Bumpers (2) | Flasher | Blk-Org | J126-3 / J125-3 | Q38 | #906 |
| 20 | Left Lightning Bolt/Mini Flipper | Flasher | Blk-Yel | J126-4 / J125-5 | Q36 | #906 |
| 21 | Right Lightning Bolt/Swamp | Flasher | Blu-Grn | J126-5 / J125-6 | Q28 | #906 |
| 22 | The Power/Backbox Cloud (3) | Flasher | Blu-Blk | J126-6 / J125-7 | Q30 | #906 |
| 23 | Upper Magnet | Low Power | Blu-Vio | J126-7 / J125-8 | Q34 | 20-9247 12V |
| 24 | Right Magnet | Low Power | Blu-Gry | J126-8 / J125-9 | Q32 | 20-9247 12V |
| 25 | Thing Motor | Flasher | Blu-Brn | J122-1 | Q26 | 14-7966 12V |
| 26 | Thing Eject Hole | Flasher | Blu-Red | J122-2 | Q24 | AE-27-1200 |
| 27 | Bookcase Motor | Flasher | Blu-Org | J122-3 | Q22 | 14-7969 12V |
| 28 | Swamp Release | Flasher | Blu-Yel | J122-4 | Q20 | AE-30-2000 |

## Flipper coils (same page)

Printed below the GI block without a solenoid number (public addresses per `wpc-fliptronic.json`,
not the printed circuit order):

| Printed label | Wire | Connection | Part number |
| --- | --- | --- | --- |
| Upper Left Flipper | Gry-Yel | J109-5 | FL-11753 |
| Upper Right Flipper | Blu-Yel | J109-7 | FL-11630 |
| Lower Left Flipper | Gry-Yel | J109-5 | FL-15411 |
| Lower Right Flipper | Blu-Yel | J109-7 | FL-15411 |


Gold page 2-43 independently lists 17 and 18 as two bulbs each; 19a has TWO jet-bumper bulbs and 19b has one lower-ramp bulb (circuit total THREE); 20a/20b and 21a/21b have two each; 22a has one playfield flasher and 22b has three atop-backbox bulbs (circuit total FOUR). The five main-playfield A-12336-1 socket assemblies in the Gold BOM reconcile two 19a + one 20a + one 21a + one 22a; the plastic-mounted dome sockets are separate subassemblies. Parenthetical quantities qualify the named subgroup, not necessarily the entire circuit. These are physical quantities, never counts of render objects. Magnet fuse footnote: 5 Amp S.B., underside of playfield.

## G.I. block (same table)

| No. | Function | Type | Wire | Connection | Triac | Bulb |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Left Playfield String | G.I. | Brown | J120-1 | Q18 | #44 |
| 02 | Insert House String | G.I. | Orange | J120-2 | Q10 | #555 |
| 03 | Insert People String | G.I. | Yellow | J120-3 | Q14 | #555 |
| 04 | Not Used | G.I. | Green | J121-5 | Q16 | --- |
| 05 | Right Playfield String | G.I. | Violet | J121-6 | Q12 | #44 |

The interboard table3-20 routes insert strings2/3 at J121-2/3 (returns J121-8/9), right playfield5 at J120-6 (return J120-11) with cabinet branch J119-3/1. Preserve the3-6 connector readings above; use3-20 for wiring. It changes no fitment/public binding. Public G.I. index = printed number minus1.
