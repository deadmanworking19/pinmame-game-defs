# FunHouse — November 1990 operator handbook switch and G.I. evidence

Source: `Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf`, PDF pages 5 and 9-10, visually checked against 250 dpi full-page renders.

## General illumination

The handbook's Solenoid Table on PDF page 5 prints the following complete G.I. block:

| No. | Function | Wire | Connector | Transistor | Bulb |
| --- | --- | --- | --- | --- | --- |
| 01 | Upper Backglass | White-Brown | J120-7 | Q18 | #555 |
| 02 | Front Playfield | White-Violet | J119-1 | Q10 | #555 |
| 03 | Rear Playfield | White-Yellow | J121-9 | Q14 | #555 |
| 04 | Center Backglass / Right Rear Playfield | White-Orange | J120-8 | Q16 | #555 |
| 05 | Top Playfield | White-Green | J120-10 | Q12 | #555 |

PinMAME exposes the five circuits as zero-based public addresses 0-4 in printed order, and the transistor column follows that order: Q18, Q10, Q14, Q16 and Q12 are the triacs of WPC G.I. strings 1-5. The names and wires of rows 02, 04 and 05 do not. On the power driver board each triac is fixed to its pins and wires (Q10 drives orange on J120-2/J120-8, Q16 green on J120-5/J120-10, Q12 violet on J120-6/J120-11 and the J119 cabinet branch), and the L-9 ROM's T.6 G.I. test prints, for each public string, its name, wires, playfield and backbox pins, fuse and driver (`evidence/runtime/wpc-alpha/funhouse-fh_l9-gi-test.json`):

| Public | ROM name | Wires | P.F. pins | B.B. pins | Fuse | Driver |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | BACKGLASS UPPER | WHT-BRN BRN | J120-7 120-1 | J121-7 121-1 | F110 | Q18 |
| 1 | RUDY / BACKGLASS | WHT-ORN ORN | J120-8 120-2 | J121-8 121-2 | F109 | Q10 |
| 2 | REAR PLAYFIELD | WHT-YEL YEL | J120-9 120-3 | J121-9 121-3 | F108 | Q14 |
| 3 | BACKGLASS CENTER | WHT-GRN GRN | J120-10 120-5 | J121-10 121-5 | F107 | Q16 |
| 4 | FRONT PLAYFIELD | WHT-VIO VIO | J120-11 120-6 | J121-11 121-6 | F106 | Q12 |

So rows 02, 04 and 05 carry their names, wires and pins one string out of place, as Terminator 2's handbook does: "Front Playfield" with White-Violet J119-1 is public 4, "Center Backglass / Right Rear Playfield" with White-Orange J120-8 is public 1, and "Top Playfield" with White-Green J120-10 stands for public 3, which the ROM names BACKGLASS CENTER. An owner's repair confirms the orange string's loads: with fuse F109 failed, the spotlight that shines on Rudy and the lower third of the backbox G.I. were dark, and the orange and white-orange wires enter at J120 (`pinside-gi-orange-string.md`). The retained script drives Rudy's spotlight from public 1, the rear playfield from 2 and the front playfield from 4, and nothing on the playfield from 0 or 3. Public 3 is therefore a backbox string. The printed "Top Playfield" name is a misprint, not a playfield branch.

## Flipper inventory

The same PDF page prints the complete fitted flipper inventory:

| Function | Wire | Connector | Part |
| --- | --- | --- | --- |
| Lower Right | Blue-Yellow | J109-7 | FL-11630 |
| Lower Left | Gray-Yellow | J109-5 | FL-11630 |
| Upper Left | Gray-Yellow | J109-5 | FL-11753 |

There is no fitted upper-right flipper. This inventory resolves the generic four-position connector table in the operations manual: three positions are populated, and the upper-left row is real FunHouse hardware.

## Right trough switch 63

The Switch Matrix on PDF page 9 names address `63` `Right Trough`, and the Switch Locations drawing on PDF page 10 places callout 63 at the rightmost trough position. The retained script independently binds `Controller.Switch(63)` to the `ballrelease` kicker: `ballrelease_hit` asserts it, and `KickBallToLane` kicks the ball and clears it. The kicker center is therefore the validated spatial location for switch 63.
