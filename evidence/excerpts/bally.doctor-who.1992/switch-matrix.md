# Doctor Who — Switch Matrix (wiring)

Transcribed from `Bally_1992_Doctor_Who_Manual.pdf`, PDF page 126, printed page `DOCTOR WHO 3-3`, the
`SWITCHES` matrix table with its dedicated and flipper grounded-switch blocks and its circuit drawing.
Read from the rendered page (300 dpi image-only scan), not from the OCR text. A foldout reprint of the
same table sits at PDF page 150 and is a copy of this page, not a second source.

**This page carries no shading and no opto legend.** Every one of the 64 matrix cells and every
dedicated and flipper cell is unshaded; the black-pixel fraction of each matrix cell was measured from
the 300 dpi render and the cells of the opto columns (3 and 7) are no different from the others beyond the
amount of text they hold. The Handy Technician's Chart, a different printing of the same data, does
shade cells as "OPTO, TYPICALLY CLOSED"; see `handy-technician-chart.md`.

## Matrix drive columns

| Column | Wire | Connector-pin | Drive IC |
| --- | --- | --- | --- |
| 1 | Green-Brown | J206-1 | U20-18 |
| 2 | Green-Red | J206-2 | U20-17 |
| 3 | Green-Orange | J206-3 | U20-16 |
| 4 | Green-Yellow | J206-4 | U20-15 |
| 5 | Green-Black | J206-5 | U20-14 |
| 6 | Green-Blue | J206-6 | U20-13 |
| 7 | Green-Violet | J206-7 | U20-12 |
| 8 | Green-Gray | J206-9 | U20-11 |

## Matrix return rows

| Row | Wire | Connector-pin | Return IC |
| --- | --- | --- | --- |
| 1 | White-Brown | J208-1 | U18-11 |
| 2 | White-Red | J208-2 | U18-9 |
| 3 | White-Orange | J208-3 | U18-5 |
| 4 | White-Yellow | J208-4 | U18-7 |
| 5 | White-Green | J208-5 | U19-11 |
| 6 | White-Blue | J208-7 | U19-9 |
| 7 | White-Violet | J208-8 | U19-5 |
| 8 | White-Gray | J208-9 | U19-7 |

## Dedicated grounded switches

| Switch | Wire and connector-pin | Printed label |
| --- | --- | --- |
| D1 | Orange-Brown J205-1 (1) | Left Coin Chute |
| D2 | Orange-Red J205-2 (2) | Center Coin Chute |
| D3 | Orange-Black J205-3 (3) | Right Coin Chute |
| D4 | Orange-Yellow J205-4 (4) | 4th Coin Chute |
| D5 | Orange-Green J205-6 (5) | Normal Function: Srv Credits; Test Function: Escape |
| D6 | Orange-Blue J205-7 (6) | Normal Function: Volume Dn; Test Function: Down |
| D7 | Orange-Violet J205-8 (7) | Normal Function: Volume Up; Test Function: Up |
| D8 | Orange-Gray J205-9 (8) | Normal Function: Begin Test; Test Function: Enter |

## Flipper grounded switches

| Switch | Wire and connector-pin | Printed label |
| --- | --- | --- |
| F1 | Black-Green J906-1 | Right Flipper End of Stroke |
| F2 | Blue-Violet J905-1 | Right Flipper Opto |
| F3 | Black-Blue J906-3 | Left Flipper End of Stroke |
| F4 | Blue-Gray J905-2 | Left Flipper Opto |
| F5 | Black-Violet J906-4 | Upper Right Flipper End of Stroke |
| F6 | Black-Yellow J905-3 | Upper Right Flipper Opto |
| F7 | Black-Gray J906-5 | Upper Left Flipper End of Stroke |
| F8 | Black-Blue J905-5 | Upper Left Flipper Opto |

## Matrix cells

Each cell prints the description with the two-digit address in its bottom-right corner (column digit
first, row digit second). Cell text as printed:

| Addr | Printed cell | Addr | Printed cell | Addr | Printed cell | Addr | Printed cell |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Not Used | 21 | Slam Tilt | 31 | Opto Popper | 41 | (E)-S-C-A-P-E |
| 12 | Not Used | 22 | Coin Door Closed | 32 | Mini-ply Home Opto | 42 | E-(S)-C-A-P-E |
| 13 | Start Button | 23 | Ticket Opto. | 33 | Enter Top Ramp Opto | 43 | E-S-(C)-A-P-E |
| 14 | Plumb Bob Tilt | 24 | Always Closed | 34 | Launch Ball | 44 | E-S-C-(A)-P-E |
| 15 | Left Sling | 25 | Trough 1 Ball | 35 | Score Top Ramp | 45 | E-S-C-A-(P)-E |
| 16 | Right Sling | 26 | Trough 2 Balls | 36 | Enter Bottom Ramp | 46 | E-S-C-A-P-(E) |
| 17 | Shooter Lane | 27 | Trough 3 Balls | 37 | Score Bottom Ramp | 47 | Hang On Score |
| 18 | Exit Jets | 28 | Outhole | 38 | Mini-ply Door, Middle | 48 | Select Doctor |

| Addr | Printed cell | Addr | Printed cell | Addr | Printed cell | Addr | Printed cell |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | (R)-E-P-A-I-R | 61 | Left Jet | 71 | Mini Opto 5 Bank Right 1 | 81 | Not Used |
| 52 | R-(E)-P-A-I-R | 62 | Right Jet | 72 | Mini Opto 5 Bank Right 2 | 82 | Playfield Glass |
| 53 | R-E-(P)-A-I-R | 63 | Bottom Jet | 73 | Mini Opto 5 Bank Middle | 83 | Not Used |
| 54 | R-E-P-(A)-I-R | 64 | Left Drain | 74 | Mini Opto 5 Bank Left 2 | 84 | Not Used |
| 55 | R-E-P-A-(I)-R | 65 | Left Return | 75 | Mini Opto 5 Bank Left 1 | 85 | Not Used |
| 56 | R-E-P-A-I-(R) | 66 | Right Return | 76 | Mini-ply Left Opto Eject | 86 | Not Used |
| 57 | Trap Door Down | 67 | Right Drain | 77 | Mini-ply Right Opto Eject | 87 | Not Used |
| 58 | Transmat Award | 68 | Mini-ply Door, Left | 78 | Mini-ply Lites Lock | 88 | Mini-ply Door, Right |

Address 78 prints `Mini-ply Lites Lock` here, and `Mini-ply Target` on the Switch Locations parts list
(`switch-locations.md`, item 78, assembly A-15903). The Handy Technician's Chart prints `MINI-PLY LITES LOCK`.
The page prints addresses 83-87 as Not Used cells and the Switch Locations list prints them as `83-87
Not Used`.

## Circuit drawing

The drawing shows a column circuit (ULN-2803 driver, +12V pull-up through 1K, J206 connector) feeding the
playfield switch, a series diode, and a row circuit (J209 connector, LM339 comparator, 74LS240). Column
A/B: inactive H L Off, active L H On. Row C/D/E: switch open H H L Off, switch closed L L H On. The text
beneath says that the microprocessor strobes each column, that a closing switch makes the row side
activate, and that both the row and column lines must be low for a switch to be considered closed.
