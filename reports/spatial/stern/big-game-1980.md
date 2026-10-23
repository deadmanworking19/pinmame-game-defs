# Big Game (Stern, 1980) spatial review

Status: incomplete. Every lamp placement is `observed` and general illumination has none, so the machine record stays `partial` at `machines/partial/stern/big-game-1980.json`.

The geometry source is the retained `Big Game (Stern 1980) - redbone(MOD) v1.2.0.vpx` at SHA-256 `6d37ab3ac46fdc116c3324c46bffae19ce784fc4bbece209b13f31840f823bfe`; its embedded script (SHA-256 `61b2cf1d0cd6e6e09e7582a1ab5f8c3c092d54da113a74c436de552646d93e85`) binds the same lamps, switches and coils as the pinned known-working 1.5.1 script. Exact playfield bounds are left 0, top 0, right 1093, bottom 2115, and every canonical coordinate is x/1093 and y/2115 rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, in normalized VPX/player view.

## Evidence decisions

- The script's bindings choose each switch's and coil's object. Lamps are placed on the light at the insert their printed row names; where no row names an insert, on the light the script binds.
- Four lamps are bound differently by the table than by this game's Lamp Driver Schematic. The ROM sides with the sheet wherever it can tell: the left spinner and the right roll-over buttons scored their lit values while the sheet's lamps (37 and 5) were on and the table's (6 and 34) were off. The placements follow the sheet and the defects are stated on the devices:
  - lamp 5: The second placement is the `100 / 2.000 WHEN LIT` insert beside the right roll-over buttons (table light l64), which the row's `R. 1,000 WHEN LIT` names. The retained script binds that light to lamp 34 (the reserve bonus) instead, a defect of the table: in the retained gameplay run the right roll-over buttons scored their lit 2,000 while card Z (this lamp) was on and lamp 34 was off.
  - lamp 6: Placed on the `5.000 WHEN LIT` insert above the middle top lane (table light l72), which the row `TOP R.O.W. "I" 5,000` names. The retained script does not drive that light from lamp 6; it lights it itself whenever lamps 10, 26 and 42 (B, I, G) are all on, the condition under which the ROM turns lamp 6 on, and it binds lamp 6 to the two spinner inserts instead (lights l6 and l48), a defect of the table.
  - lamp 30: Placed on the `100 OR 1000 WHEN LIT` insert beside the right spinning target (table light l6), which the row `RIGHT SPIN. TARG. 1,000` names; the retained script binds that light to lamp 6. The script binds lamp 30 to l30, a glow under the top-left roll-over button (not a bulb light), which is not placed; no printed row names a lamp at that button.
  - lamp 37: The second placement is the `200 OR 2000 WHEN LIT` insert beside the left spinning target (table light l48), which the row `"X" & LEFT SPIN. TARG.` names. The retained script binds that light to lamp 6, a defect of the table: in the retained gameplay run the left spinner scored its lit 2,000 while card X (this lamp) was on and lamp 6 was off.

## Explicit projections

- pinmame.input.switch 12: Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position.
- pinmame.input.switch 13: Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position.
- pinmame.input.switch 33: Placed on the table's Drain kicker, its ball-collection proxy below the apron; the out-hole switch itself is not modelled. The shooter-lane BallRelease kicker is the virtual serve destination and is not used.
- pinmame.input.switch 37: One placement per contact, each at the mean of the drag points of the rubber wall the script pulses (sw37 left of the top lanes, sw37a right of them).
- pinmame.output.solenoid 4: Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 5: Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 7: Projected onto the top-left bank it resets: the mean of the table's own three target objects. The reset coil sits under the bank and has no object.
- pinmame.output.solenoid 8: Projected onto the top-right bank it resets: the mean of the table's own three target objects.
- pinmame.output.solenoid 9: Projected onto the lower-right bank it resets: the mean of the table's own three target objects.
- pinmame.output.solenoid 11: Placed on the table's Drain kicker, the ball-collection proxy where the ball enters the out-hole; the out-hole coil is not modelled.
- physical.input.direct 1: Placed on the left flipper pivots (lower, upper): each end-of-stroke contact is mounted on its flipper assembly.
- physical.input.direct 2: Placed on the right flipper pivots (lower, upper): each end-of-stroke contact is mounted on its flipper assembly.
- pinmame.output.solenoid 46: Placed on the two right flipper pivots, both moved by this one callback.
- pinmame.output.solenoid 48: Placed on the two left flipper pivots, both moved by this one callback.

## Factory drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it.

- Stern_1980_Big_Game_Manual.pdf PDF 19: switch location drawing (BIG GAME / SWITCHES), the whole page rendered at 216 dpi, three times the 72 dpi scan: 7 controls (leave-one-out max 0.0153), 35 callout pairs, callout fit on 34 (leave-one-out max 0.0583)
- Stern_1980_Big_Game_Manual.pdf PDF 21: solenoid location drawing (BIG GAME / SOLENOIDS), the whole page rendered at 216 dpi, three times the 72 dpi scan: 7 controls (leave-one-out max 0.0167), 14 callout pairs, callout fit on 11 (leave-one-out max 0.058)
- Validated 44 of 49 checked placements; not validated: device.lower-left-thumper-bumper.effect, device.saucer-eject.effect, device.top-left-bank-reset.effect, switch.right-spinner.sensor, switch.saucer.sensor

## Counts

- Placements: 115 (71 observed, 44 validated) on 100 records
- Records with a controlled `cabinet_or_service` record: 24
- Records with a controlled `dip_switch` record: 32
- Records with a controlled `internal_nonvisual` record: 2
- Records with a controlled `unused` record: 11
- Records with a controlled `virtual` record: 2
- Records with no spatial key: 1 (gi.general-illumination)

## Excluded table objects

- gi*, Light001-Light007 and accent* lights: render and general-illumination helpers; Big Game's general illumination has no controller address and no bulb inventory in any retained source
- l13, l29, l45, l61, l63: backglass text boxes of the backbox lamps (a controlled cabinet_or_service record each)
- l14, l15, l16, l30, l31: glows under the five star roll-over buttons (not bulb lights); the script binds them to lamp numbers 14, 15, 16, 30 and 31 and keeps them lit, and no printed row names a lamp under a button
- BallRelease: the shooter-lane kicker the script serves the ball from, a virtual destination rather than the out-hole kicker
- Gate2: a hidden gate in the shooter lane; Gate1 and Gate3 are the two passive gates of the mechanism record and carry no controller binding

## Blockers

- Public 20 (continuous driver Q18) is driven by the ROM in attract mode with no documented load, so its availability stays unknown and output semantics stays missing; see the knowledge note.
- Every lamp placement is `observed`: the manual prints no lamp-location drawing, and there is one retained factory-layout table, so nothing independent can check the lamp positions; the IPDB photographs confirm order and side by eye only.
- General illumination has no placement: no retained source gives its bulb quantity or positions, and the table's GI light collection is render membership, not a socket count.
- Switch and coil placements the factory drawings do not confirm under the callout check stay `observed`; they are listed under `callout_check.not_validated`.

## Promotion decision

Promotion to `author_ready` is refused: public 20's output is unexplained, every lamp placement rests on one table with no lamp-location drawing to check it, and general illumination has no placement. The record stays `partial` with `coverage.missing = ["output_semantics", "spatial_placement"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/big-game-1980/redbone-1.2.0/Big Game (Stern 1980) - redbone(MOD) v1.2.0/manifest.json`, SHA-256 `ca8c7886640ec273ad41afd4884d5abee5be71a65ca0b2805c0526800808a691`, 689 files, 22106949 bytes.
- Object-centre dump of every extracted game item at `external:pinmame-review-artifacts/big-game-1980/redbone-1.2.0-geometry.tsv`.
- Callout reads, tiles and overlays under `external:pinmame-review-artifacts/big-game-1980/callout-check`.
