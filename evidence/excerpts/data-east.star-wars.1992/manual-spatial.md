# Star Wars factory spatial evidence

Manually transcribed and visually checked by the integration curator on 2026-10-22.
Operator's manual: `Star_Wars_DE_OPS.pdf`, SHA-256
`dda489f3270e465dc285102a1d311d7538f58de9772542c78ba0fedc3c546ab0`,
downloaded from https://www.bmigaming.com/Games/Manuals/pinball-machines/Star_Wars_DE_OPS.pdf.
Schematics: `starwars_schematics.pdf`, SHA-256
`e2a5dedc7e9529a449151f8b9a7ec8d94eda3054dc1022d1e987e1124f9714d1`,
downloaded from https://www.maypin.eu/pinsdata/starwars_schematics.pdf.
Copyright Data East Pinball, Inc., 1992; local research copies, NOASSERTION.

## Lamp Locations: complete list

Operator's manual printed p.27 / PDF 29. Two printed columns are flattened in
address order; spacing and leading zeros are normalized. The drawing crop beside
this excerpt retains the location symbols. It is a physical layout drawing, not
the electrical matrix. Positions measured on it remain observed; the affine
control readings and coordinates are in `tools/star_wars_manual_geometry.json`.

| Number | Description |
| --- | --- |
| 01 | STAR WARS |
| 02 | STAR WARS |
| 03 | STAR WARS |
| 04 | STAR WARS |
| 05 | STAR WARS |
| 06 | STAR WARS |
| 07 | STAR WARS |
| 08 | STAR WARS |
| 09 | D.S. Moon 1 Left |
| 10 | D.S. Moon 2 |
| 11 | D.S. Moon 3 |
| 12 | D.S. Moon 4 |
| 13 | D.S. Moon 5 |
| 14 | D.S. Moon 6 |
| 15 | D.S. Moon 7 |
| 16 | D.S. Moon 8 Right |
| 17 | Not Used |
| 18 | Extra Ball |
| 19 | Lite C3PO Eyes |
| 20 | Lite the Force |
| 21 | Yoda |
| 22 | D.S. X Wing Mult. |
| 23 | D.S. Tie Fighter |
| 24 | Death Star Insert |
| 25 | Credit Button |
| 26 | C3PO Left Eye |
| 27 | C3PO Mouth |
| 28 | C3PO Right Eye |
| 29 | Death Star Sphere 1 |
| 30 | Death Star Sphere 2 |
| 31 | Launch (Shooter Lane) |
| 32 | Upper Left Outlane |
| 33 | X-Wing Target 1 Left |
| 34 | X-Wing Target 2 |
| 35 | X-Wing Target 3 |
| 36 | X-Wing Target 4 |
| 37 | X-Wing Target 5 (Right) |
| 38 | Drop Target Top |
| 39 | Drop Target Center |
| 40 | Drop Target Bottom |
| 41 | 10 Million Left |
| 42 | 10 Million Center |
| 43 | Large Tie Fighter |
| 44 | 10 Million Right |
| 45 | R2D2 When Lit |
| 46 | Lite Laser Kick |
| 47 | Power Scoop Left |
| 48 | Power Scoop Right |
| 49 | Ramp Hyper Space |
| 50 | Ramp Jackpot |
| 51 | Ramp Empire |
| 52 | Light Saber Arc |
| 53 | Right Outlane |
| 54 | Right Return Lane |
| 55 | Left Return Lane |
| 56 | Laser Kick |
| 57 | R2D2 Dome Left |
| 58 | R2D2 Dome Right |
| 59 | Victory |
| 60 | Special |
| 61 | Top Turbo Bumper |
| 62 | Left Turbo Bumper |
| 63 | Right Turbo Bumper |
| 64 | Bottom Turbo Bumper |

## Flash locations and limits

Operator's manual printed p.28 / PDF 30 contains separate playfield and insert-panel
diagrams. The committed crop is only the playfield diagram. It locates the 6R
pair beside the drop-target bank, the 3R pair at the central round insert, and the
4R lamps along the right edge. The paired 5R and 7R symbols on the toys provide
coarse cross-checks only; they are too far outside the controls for coordinates.
The 6R pair is measured on the drawing. Other published banks use selected VPW
Lights consistent with the drawing, without treating the drawing as validation.
Three 2R back-panel symbols
are excluded from the playfield positions. The 8R drawing shows four playfield
symbols: one at the rear left and three in the bumper area. This disagrees with
the schematic's three-playfield annotation. Neither these
readings nor the table establish precise hidden socket centres.

Schematics printed p.48 / PDF 4 prints these complete branch annotations:

| Bank | Location annotation | Bulb annotation |
| --- | --- | --- |
| 1R | (3) PLFD (1) INSERT | (4) NO. 89 |
| 2R | (3) BACK PANEL (1) PLFD | (4) NO. 89 |
| 3R | (2) PLFD (2) INSERT | (4) NO. 89 |
| 4R | (4) PLFD | (3) NO. 89 |
| 5R | (2) DEATHSTAR (2) INSERT | (4) NO. 89 |
| 6R | (2) PLFD (2) INSERT | (3) NO. 89 |
| 7R | (2) R2D2 (2) INSERT | (4) NO. 89 |
| 8R | (3) PLFD (1) INSERT | (4) NO. 89 |

The discrepant printed totals for 4R and 6R are preserved. The 8R drawing/table
and schematic disagree on the playfield count. No complete bank quantity is
inferred from these inconsistent annotations or from VPX render-helper counts.
The same sheet identifies solenoid 11 as the G.I. GENERAL ILLUMINATION RELAY
on the POWER SUPPLY BOARD, rather than a playfield effect coil.

The same sheet's complete switched left-side coil branch labels are:

| Branch | Description | Coil |
| --- | --- | --- |
| 1L | Outhole | 23-840 |
| 2L | Trough Eject | 23-840 |
| 3L | Ball Launch | 23-800 |
| 4L | Left Power Scoop | 25-1240 |
| 5L | VUK | 23-800 |
| 6L | Drop Target | 23-800 |
| 7L | Right Power Scoop | 23-800 |
| 8L | Knocker | 23-800 |

The outhole and trough eject are physically separate. In VPW, the trough-entry
event and solenoid 1's drain effect use `Drain`; solenoid 2's release effect uses
`BallRelease`. The virtual trough's switch array includes switch 10, but the
factory switch chart identifies that contact as Outhole, not a fourth trough
contact. Stable legacy IDs are preserved while these two labels and anchors are
corrected.

## Cabinet and shifter identification

Operator's manual printed p.30 / PDF 32, complete Cabinet Parts Illustration list:

| Item | Description | Part No. |
| --- | --- | --- |
| 1 | Shifter Assembly | 500-5620-00 |
| 2 | Flipper Button | 500-5026-22 |
| 3 | Leg Bolt (Black) | 231-5000-01 |
| 4 | Cash Box Bottom | 545-5090-00 |
| 5 | On/Off Switch DP/ST | 180-5001-00 |
| 6 | Leg (Black) | 535-5020-30 |
| 7 | Lock Bracket-Cash Box | 535-5215-00 |
| 8 | Power Input Box Assy | 515-5360-00 |
| 9 | Transformer | 010-5003-00 |
| 10 | Speaker-Round (8 inch) | 031-5005-00 |
| 11 | Side Armor-Right | 535-5010-31 |
| 12 | Memory Protect Switch | 180-5000-00 |
| 13 | Memory Protect Switch Bracket | 535-6409-00 |
| 14 | Start Switch Assembly | 500-5407-02 |
| 15 | Flipper Leaf Switch | 180-5048-01 |
| 16 | Cash Box Top | 535-5013-03 |
| 17 | Plumb Bob Tilt Assembly | 500-5023-00 |
| 18 | Volume Control | 123-5000-00 |
| 19 | Playfield Glass (Tempered) * | 660-5001-00 |
| 20 | Side Armor-Left | 535-5010-32 |
| 21 | Recessed cup for line cord | 545-5122-00 |
| 22 | Service Switch (Not Shown) | 180-5012-00 |
| 23 | Front Molding Lockdown Assy. * | 500-5020-00 |
| 24 | Front Molding - Black * | 500-5021-10 |
| 25 | S.S.Flipper P.C.B. | 520-5033-02 |
| 26 | Roto Lock Bottom | 355-5006-01 |
| 27 | Rear Plastic Extrusion for Playfield Glass | 545-5038-00 |
| 28 | Mounting Foam for Extrusion | 626-5004-00 |
| 29 | Plastic Channel (Right & Left) | 545-5017-00 |
| 30 | Backbox Hinge Left * | 535-6172-00 |
| 31 | Backbox Hinge Right * | 535-6172-01 |
| 32 | Leg Leveler * | 500-5017-00 |
| 33 | Coin Door with Validator Blank * | 500-5018-17 |

The drawing places items 1 and 17 on/in the cabinet. Printed p.42 / PDF 44
identifies the Up-Down Shifter as 500-5620-00. Its complete parts list follows:

| Item | Description | Part No. |
| --- | --- | --- |
| 1 | Handle/Button/Harness | 515-5691-00 |
| 2 | Button & Harness | 515-5692-00 |
| 3 | Spring | 266-5031-01 |
| 4 | Screw 1/4-20 x 1/2 SCHS | 231-5024-00 |
| 5 | Micro Switch | 180-5111-00 |
| 6 | Screw 4-40 x 3/4 PHMS | 237-5887-00 |
| 7 | Screw 10-32 x 1 PHMS | 237-5888-00 |
| 8 | Screw 10-32 x 3/8 PHMS | 237-5889-00 |
| 9 | Decal | 820-6097-00 |
| 10 | Nylock Nut 1/4-20 | 240-5314-00 |
| 11 | Wrench (Shipped w/Game) * | 535-6410-01 |

The p.42 legend says '* Indicates Not Shown'. The switch chart identifies
50 as Shift Button and 51 as Shift Down. The retained VPW script supplies the
runtime binding, but its Magna-Save key mapping does not relocate this hardware
to a coin door.

## Complete switch parts chart

Schematics printed p.50 / PDF 6. Four printed columns flattened in address order.
An asterisk means "Indicates Cabinet Switches"; the original 52-through-64 row
is retained as a range. This chart establishes names, not runtime activity.

| Switch | Description | Part No. |
| --- | --- | --- |
| 01* | Plumb Tilt | See Cabinet |
| 02* | 4th Coin | - |
| 03* | Credit Button | 500-5097-02 |
| 04* | Right Coin | 180-5024-00 |
| 05* | Center Coin | 180-5024-00 |
| 06* | Left Coin | 180-5024-00 |
| 07* | Slam Tilt | 180-5022-00 |
| 08 | Not Used | - |
| 09 | Not Used | - |
| 10 | Outhole | 180-5011-00 |
| 11 | Left Trough | 180-5009-00 |
| 12 | Center Trough | 180-5009-00 |
| 13 | Right Trough | 180-5010-00 |
| 14 | Shooter Lane | 180-5100-01 |
| 15* | Left Flip. Cab. | 180-5048-01 |
| 16* | Right Flip. Cab. | 180-5048-01 |
| 17 | Right Loop | 500-5142-00 |
| 18 | Not Used | - |
| 19 | Left Loop | 180-5087-00 |
| 20 | Ramp Entrance | 180-5087-00 |
| 21 | Right Outlane | 515-5138-00 |
| 22 | Right Return | 515-5138-00 |
| 23 | Left Return | 500-5142-00 |
| 24 | Left Outlane | 500-5142-00 |
| 25 | X-Wing Target 1 (Left) | 180-5082-06 |
| 26 | X-Wing Target 2 | 180-5082-06 |
| 27 | X-Wing Target 3 | 180-5082-06 |
| 28 | X-Wing Target 4 | 180-5082-06 |
| 29 | X-Wing Target 5 (Right) | 180-5082-06 |
| 30 | Top Drop Target | 180-5092-00 |
| 31 | Mid.Drop Target | 180-5092-00 |
| 32 | Bot. Drop Target | 180-5092-00 |
| 33 | Right Scoop | 180-5057-00 |
| 34 | Death Star Trough | 180-5057-00 |
| 35 | Obi-Wan Trough | 180-5057-00 |
| 36 | Left Vertical Up Kicker | 180-6064-00 |
| 37 | Left Scoop | 180-5057-00 |
| 38 | R2D2 Entrance | 500-5142-00 |
| 39 | Ramp Exit | 180-5093-00 |
| 40 | Bar Target | 515-5630-00 |
| 41 | Bar Motor Up | 180-5052-00 |
| 42 | Bar Motor Down | 180-5052-00 |
| 43 | Left Slingshot | 180-5054-00 |
| 44 | Right Slingshot | 180-5054-00 |
| 45 | Top Turbo Bumper | 180-5015-00 |
| 46 | Left Turbo Bumper | 180-5015-00 |
| 47 | Right Turbo Bumper | 180-5015-00 |
| 48 | Bottom Turbo Bumper | 180-5015-00 |
| 49 | Not Used | - |
| 50 | Shift Button | 180-5110-00 |
| 51 | Shift Down | 180-5111-00 |
| 52 through 64 | Not Used | - |
