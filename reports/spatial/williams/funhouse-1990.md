# FunHouse (Williams, 1990) spatial review

Status: partial. The physical machine record lives at `machines/partial/williams/funhouse-1990.json`.

The matching source is the retained known-working `Funhouse (Williams 1990)_1.3.vpx` at SHA-256 `69c37fa9a84e669a2934d6da0e5ee0277c4a0ef01e71eaa19e7271ba3396873e`. Its embedded script at SHA-256 `322fba2dec939b50e0730da8caca177545aa8f8bc055ba136360ae55deb4e863` is the runtime and causality authority. Exact playfield bounds are `left=0 top=0 right=964 bottom=2162`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.

## Evidence decisions

- The embedded script is the runtime address and causality authority; the Williams manuals are the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry, checked against the factory location drawings.
- Each placement is the table object the script binds for the device: the trigger, target, kicker, bumper or slingshot wall for a switch, the object a solenoid callback moves, and for a lamp or flasher the Light the script fades, or the bulb the table models where the script flashes only a glow sprite (lamps 57 and 58 on their overhead BulbFil filaments). A primitive is placed at the centre of its world-space mesh bounds, never at its stored position: the Magic Mirror lamp glasses L71 and L74-L78 and the back-panel flasher domes.
- Drawing check: A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. Pages: hb-5 (Solenoid Locations drawing; 8 controls, control leave-one-out at most 0.0483, 17 callout pairs), hb-7 (Lamp Locations drawing; 8 controls, control leave-one-out at most 0.047, 60 callout pairs), hb-9 (Switch Locations drawing; 8 controls, control leave-one-out at most 0.0451, 23 callout pairs). 100 of 102 checked placements agree; the others are second bulbs under an insert the drawing marks once.
- The November 1990 handbook prints the factory drawings at 600 dpi; they are the same artwork as the operations manual's 2-36, 2-38 and 2-40 drawings. Each page is fitted on its three jet-bumper caps, its three flipper pivots and its outer frame's top corners, which match the table bounds.
- A number the drawing prints with no leader in open space or along an edge marks no part, so it checks nothing; the placements whose only read is such a number are listed as excluded checks. The flashers 17, 23 and 24 each have a back-panel dome, which the drawing labels only in a leader-less row along the top rail.
- The three Steps switches (15, 26, 36) and the three Steps lamps (54, 55, 56) are drawing measurements: the drawing puts the switches on three wire slots across the Steps track and the lamps on small sockets on its left rail, while the table's invisible star triggers lie 0.06-0.07 from the slots, outside the drawn track and twice as far apart, and its raised `_finger_1` sign hotspots 0.05-0.08 from the sockets.
- Solenoid 8 (Multi-ball Release) is the lock-release gate primitive the script's MBRelease swings, where the drawing prints 8; the coils of Rudy's eyes and eyelids (25-28) project onto the eyelid assembly inside his head.
- Lamp 12 is `Gangway 100,000`: two Williams lamp-matrix pages and the physical playfield photograph agree, resolving the older lamp-location page's isolated `10,000` as a typo.
- Switch 63 is placed on the retained `ballrelease` kicker because the handbook locates it at the right trough and the script asserts and clears that exact switch as the kicker receives and releases the ball.
- FunHouse is pre-Fliptronics WPC-Alpha hardware. It has lower-right, lower-left, and upper-left direct-wired physical flippers. PinMAME publishes two button-driven synthetic sides at 45-48 for digital animation; the left callback drives both fitted left bats, and those virtual states have no playfield coordinates of their own.

## General illumination

Public G.I. names, wires, pins, fuses and triacs come from the L-9 ROM's T.6 test. Public 1's socket is the spotlight, the RudyShade Light under the table's lamp-shade primitives (Case 1). For public 2 and 4 the retained 1.3 table draws a bulb at only some of the Lights its script drives (Case 2 GI_Upper, Case 4 GI_Lower), so the bulbs come from version 2.0c of the same table, which models a bulb (pBulb glass, pFiliment filament, pFBase base) under each Light its script assigns to the same public string (GI_UpperBulbs, GI_LowerBulbs). A socket is a 2.0c bulb with a driven 1.3 Light within 0.01 normalized; of the co-located 1.3 render doubles the placement is the one that shows its own bulb mesh, else the one on a BulbFil filament primitive, else the one with the smallest falloff radius. A 1.3 Light under no 2.0c bulb makes no socket. Both tables split the strings as the ROM's names do (Rudy's spotlight, rear playfield, front playfield) and as the owners traced the orange and violet strings, no retained table contradicts the split, and public 0 and 3 light only the backbox (docs/SPATIAL.md, G.I. string membership). The manuals draw no G.I. socket and give no per-string bulb count, so no quantity is asserted.

- Public 1: 1 socket.
- Public 2: 14 sockets: Light18 (pBulb21), Light24 (pBulb23), Light17 (pBulb22), Light25 (pBulb24), Light20 (pBulb20), Light19 (pBulb19), Light23 (pBulb18), Light21 (pBulb17), Light39 (pBulb16), Light12 (pBulb14), Light8 (pBulb15), Light26 (pBulb25), Light13 (pBulb13), Light14 (pBulb12).
- Public 4: 11 sockets: LowerGI_B19 (pBulb8), Light38 (pBulb11), Light34 (pBulb9), Light35 (pBulb10), Light37 (pBulb7), Light33 (pBulb1), Light30 (pBulb6), Light29 (pBulb5), Light31 (pBulb2), Light27 (pBulb4), Light32 (pBulb3).
- Public 0 and 3: backbox only, controlled `cabinet_or_service` records.
- Not placed, RudySign1, RudySign2: f_refl glow sprites Case 1 drives on Rudy's face; the spotlight that lights them is RudyShade.
- Not placed, Light22: public 2 render light 0.026 normalized from the Light23 socket; neither table models a bulb under it.
- Not placed, Bottom_GI_32, Bottom_GI_39: public 4 render lights under the apron instruction cards; neither table models a bulb there, and the apron G.I. bulbs a parts supplier names are the record's blocker.
- Not placed, LowerGI_B14: halo partner of LowerGI_B4 at Light33's socket, 0.014 normalized from it and on no bulb.
- Not placed, public 1 backbox branch, public 4 coin-door lamps: cabinet parts of playfield strings, not placed.

## Drawing measurements

- `lamp.matrix-54.emitter.hb-7-socket` on hb-7 at pixel [439.5, 1492.0]: (0.188, 0.326). Steps Lights Frenzy lamp: centre of the small round socket printed just right of the number 54, the lowest of the three.
- `lamp.matrix-55.emitter.hb-7-socket` on hb-7 at pixel [398.0, 1381.0]: (0.167, 0.296). Steps Lights Ex. Ball lamp: centre of the small round socket printed just right of the number 55 below 56.
- `lamp.matrix-56.emitter.hb-7-socket` on hb-7 at pixel [375.0, 1221.5]: (0.157, 0.254). Steps 500,000 lamp: centre of the small round socket printed just right of the number 56 on the Steps track's left rail.
- `switch.matrix-15.sensor.hb-9-slot` on hb-9 at pixel [457.0, 1224.0]: (0.096, 0.27). Bottom step switch (Steps Lights Frenzy): centre of the lowest wire slot across the Steps track, where leader 15 ends on the slot's left end.
- `switch.matrix-26.sensor.hb-9-slot` on hb-9 at pixel [439.0, 1144.0]: (0.087, 0.249). Middle step switch (Steps Lights Ex. Ball): centre of the middle wire slot across the Steps track, where leader 26 ends on the slot's left end.
- `switch.matrix-36.sensor.hb-9-slot` on hb-9 at pixel [421.0, 1062.0]: (0.078, 0.227). Top step switch (Steps 500,000): centre of the uppermost of the three wire slots across the Steps track, midway between its rounded ends, where leader 36 ends on the slot's left end.

## Excluded checks

- `device.3-blue-flashers.emitter.1`: the drawing prints 17 only in the row of leader-less back-panel labels along the top rail, which does not draw the part, so it checks nothing; the placement is the table's Flupper dome primitive on the back panel.
- `device.3-clear-flashers.emitter.1`: the drawing prints 24 only in the row of leader-less back-panel labels along the top rail, which does not draw the part, so it checks nothing; the placement is the table's Flupper dome primitive on the back panel.
- `device.3-red-flashers.emitter.1`: the drawing prints 23 only in the row of leader-less back-panel labels along the top rail, which does not draw the part, so it checks nothing; the placement is the table's Flupper dome primitive on the back panel.
- `device.dummy-eject-hole.effect`: the drawing prints 16 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.eyelids-close.effect`: the drawing prints 27 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.eyelids-open.effect`: the drawing prints 26 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.eyes-left.effect`: the drawing prints 28 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.eyes-right.effect`: the drawing prints 25 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.kickbig.effect`: the drawing prints 3 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.mouth-motor.effect`: the drawing prints 21 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.outhole.effect`: the drawing prints 1 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.ramp-diverter.effect`: the drawing prints 2 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.trap-door-closed.effect`: the drawing prints 6 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.trap-door-open.effect`: the drawing prints 5 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.trough.effect`: the drawing prints 15 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `device.up-down-driver.effect`: the drawing prints 22 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-16.sensor`: the drawing prints 16 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-25.sensor`: the drawing prints 25 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-27.sensor`: the drawing prints 27 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-28.sensor`: the drawing prints 28 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-32.sensor`: the drawing prints 32 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-34.sensor`: the drawing prints 34 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-35.sensor`: the drawing prints 35 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-37.sensor`: the drawing prints 37 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-38.sensor`: the drawing prints 38 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-45.sensor`: the drawing prints 45 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-46.sensor`: the drawing prints 46 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-48.sensor`: the drawing prints 48 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-51.sensor`: the drawing prints 51 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-55.sensor`: the drawing prints 55 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-56.sensor`: the drawing prints 56 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-63.sensor`: the drawing prints 63 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-65.sensor`: the drawing prints 65 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-72.sensor`: the drawing prints 72 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-73.sensor`: the drawing prints 73 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.
- `switch.matrix-74.sensor`: the drawing prints 74 with no leader where it names no single part (in open space, along an edge or inside a larger outline), so it checks nothing; the placement keeps its table status.

## Explicit projections

- pinmame.input.switch 73: Projected onto the retained table's Drain kicker object, shared with the outhole solenoid (1).
- pinmame.input.switch 76: Projected onto the trap door primitive's own rotation state (PrTrap.RotX); the retained script sets this switch programmatically rather than reading a separate contact-switch object.
- pinmame.output.solenoid 3: Projected onto switch 46's position; the retained script's bsHideout saucer helper shares switch 46's own kicker object.
- pinmame.output.solenoid 5: Projected onto the trap door primitive; open/close solenoids share the mechanism's own position with switch 76.
- pinmame.output.solenoid 6: Projected onto the trap door primitive; see solenoid 5.
- pinmame.output.solenoid 16: Projected onto switch 65's position; the retained script's bsRudy saucer helper shares switch 65's own kicker object.
- pinmame.output.solenoid 21: Projected onto switch 51 (Dummy Jaw) at Rudy's mouth; no dedicated jaw-motor VPX object exists apart from the head figure.
- pinmame.output.solenoid 22: Projected onto switch 51 (Dummy Jaw); see solenoid 21.
- pinmame.output.solenoid 25: Projected onto Rudy's eyelid assembly, the centre of the PrLids primitive's world-space mesh bounds, which spans both eyes.
- pinmame.output.solenoid 26: Projected onto Rudy's eyelid assembly; see solenoid 25.
- pinmame.output.solenoid 27: Projected onto Rudy's eyelid assembly; see solenoid 25.
- pinmame.output.solenoid 28: Projected onto Rudy's eyelid assembly; see solenoid 25.

## Counts

- Placements: 173
- Located input addresses: 47
- Located output bindings: 93
- Inputs with a controlled `cabinet_or_service` record: 16
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `unused` record: 16
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `virtual` record: 21

## Blockers

- Public G.I. 4 (FRONT PLAYFIELD) also feeds G.I. bulbs under the apron, which a parts supplier names in the owner thread on the violet string and which the retained 1.3 table suggests with two render lights under its apron instruction cards. No manual page, drawing or parts list draws them, and neither retained table models a bulb there, so their number and positions are unknown and the string's placements are incomplete. Resolution path: a recreation that models those bulbs, or a drawing that locates them, checked for number and sockets against a photograph of a FunHouse playfield with the apron removed, which any owner can take.

## Promotion decision

partial: the apron G.I. bulbs of public G.I. 4 are known but unplaced. Otherwise every used switch, coil, motor, flasher, lamp and G.I. string has a validated placement or a controlled not-applicable record, every placement the factory drawings mark agrees with its callout, and the definition carries no conflict.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool.manifest.json`, SHA-256 `85620e05458bd72bc57c2e203001a0f35db9806431e66e07ee08f05e90346ba9`, 2212 files, 219908807 bytes.
- Version 2.0c table SHA-256 `45ee7c7bb500749feecabd96eef6b5ffe1d4a9ff4b611176bf1155a60ca2b413`, extraction manifest `external:pinmame-vpx-sources/williams/funhouse-1990/v2-0c/extracted-vpxtool.manifest.json`, SHA-256 `f05e57012e5f7290f74bd50e986e6668b5721c066cf9d1c0612c18747f5b7595`, 2695 files, 216969293 bytes.
- World-space OBJ export SHA-256 `ac1ab343fa91d845ae2deaed128a808499212e518c77cc2bac90a44f47453046`, retained at `external:pinmame-review-artifacts/funhouse-1990/vpx-world-obj`.
- Drawing-callout reads, tiles, overlays and generators: `external:pinmame-review-artifacts/funhouse-1990/callout-check`, manifest SHA-256 `8b177d15dccaa7c58c32061b1bdd5ec3fe0b52694c594b78e7c375b6d8f9948b`.
- Human transcription of every printed table read from the rendered original manual pages: `external:pinmame-review-artifacts/funhouse/manual-transcription.md`.
- Maintainer-supplied November 1990 operator handbook SHA-256 `bb30eacaac0ee7001f59339102da5a1bfe528c2a4dbd63d2247e00fba89f1b13` and lower-playfield photograph SHA-256 `b56821de487adc55f128e4a94d8d55a4ef2c2e23cd1c0291f1118363c6ecaa81`.
