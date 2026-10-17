# Corvette (Bally, 1994) spatial blockers

Retained VPX SHA-256 `4b500c6b33b280b0076e49b2e817fad2d1131095efeb57fd58bd160b7d8a010c`; script `d30534b6664ed214a3c8b33597ab1021bcc66e979363611e218d4fccb35e5bb5`; 1390-file extraction manifest `4ea1e9978b46256fc5ed1f8776dabb543cc5a78ecbd578c7546f29125ee74b89`; manual `60a87faf6ef22fec895f5c5adde5a92bff731e34d54fb838af1b29d3bd428e34`; Manual Amendment 16-9890 `7f37f597ef259c9da3a976eeb22a9321ac287e1abe6c536415a666fbc5ee9d42`.

Bounds: `left=0 top=0 right=979 bottom=2162`. Every canonical coordinate is x/979 and y/2162 rounded to at most six places.

## Placement status

- `validated`: 102 devices
- `observed`: 30 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 65
- used devices with no placement record: 14 (`device.zr-1-underside-flasher`, `gi.string-1`, `gi.string-2`, `gi.string-3`, `gi.string-4`, `lamp.matrix-76`, `lamp.matrix-77`, `lamp.matrix-78`, `lamp.matrix-81`, `lamp.matrix-82`, `lamp.matrix-83`, `lamp.matrix-84`, `lamp.matrix-85`, `lamp.matrix-86`)

## Projection classes

- **switch:** The retained table's object for the switch (trigger, gate, target, kicker, bumper, slingshot wall or rubber wall), chosen by what the script binds, observed and validated where the switch drawing's own callout agrees. Projections, where the table has no object at the switch: the trough optos 31-34 and the trough eject opto 37 onto the trough kicker BallRelease (the table's trough is a virtual ball stack); the lock switches 76-78 onto the lock kicker Kicker1; the engine full-stroke optos 71/72 onto the engine primitive EngineP; the race start optos 51/52 onto each car primitive's start point and the encoders 55/56 onto each lane's finish end (the script's finish constants).
- **lamp:** The script-bound Light's own centre, validated where the lamp drawing's callout agrees. 53 and 68, which the script draws only on glow sprites, sit on the table's stacked pair of bulb meshes L81P1 and L81P4 (the colour-to-lamp pairing is unsourced and moves neither by more than 0.0005). The lamps the script draws only on Flasher sprites with no bulb model (76-78 and the hidden race tree sprites 81-86) have no placement, because a sprite is a glow and not a socket; the race tree is drawn only in the lamp drawing's separate inset. The cabinet button lamps 87 and 88 are not applicable.
- **solenoid:** The object the solenoid callback moves or lights (trough kicker, gates, kickback plunger, popper and kickout kickers, lock eject kicker Kicker3, diverter wall, flippers, flasher Lights) or, for the slingshots and jet bumpers, the object that fires the coil; the race motors 18/19 are projected onto each car's lane start. The flasher circuits 22-25 and 27 carry a backbox bulb as well; only the playfield bulb is placed. 26 has no placement: the script lights only a glow sprite and a light parked off the playfield. Validated where the solenoid drawing's callout agrees.
- **gi:** None: the retained table's G.I. collections disagree with the manual's and the ROM's string names on which half of the playfield each string lights (see the conflict), so strings 0-3 have no placement; string 4 lights the backbox title only and is not applicable.

## Drawing callout check

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. It validates 103 of the 111 table placements it checks ([seed](../../../tools/seeds/bally/corvette-1994-callouts.json)); the rest keep their observed status:

- `device.loop-gate.effect`: callout 16 on 2-49, 0.149 normalized away.
- `device.pit-stop-popper.effect`: callout 4 on 2-49, 0.203 normalized away.
- `device.right-rear-panel-flasher.emitter`: callout 27 on 2-49, 0.077 normalized away.
- `device.route-66-kickout.effect`: callout 8 on 2-49, 0.182 normalized away.
- `device.zr-1-up-rev-gate.effect`: callout 5 on 2-49, 0.139 normalized away.
- `switch.matrix-47.sensor`: callout 47 on 2-47, 0.130 normalized away.
- `switch.matrix-48.sensor`: callout 48 on 2-47, 0.109 normalized away.
- `switch.matrix-57.sensor`: callout 57 on 2-47, 0.125 normalized away.

## Unresolved physical geometry

- General illumination strings 0-3 (public GI 0-3): the table drives its lower bulbs from GI 0/1 and its upper bulbs from GI 2/3, the reverse of the manual's and the ROM's names, and no retained source assigns individual bulbs to a string, so no string has a placement until a physical machine's T.6 test settles it.
- The trough, lock, engine full-stroke and race-track optos are projections onto the nearest table object that models their mechanism, not observed sockets; their placements stay observed and are not checked against the drawings.
- Lamps 76-78 and 81-86 and the playfield bulb of flasher circuit 26 have no placement: the table draws them only on Flasher sprites (hidden ones for the race tree) or a light parked off the playfield, and the race tree appears only in the lamp drawing's inset, which has no playfield frame. Measuring them on the location drawings would place them.
- Placements the switch and solenoid drawings do not confirm keep their observed status; the drawing callout check lists them with the distance or reason.

## Promotion decision

partial: the four playfield G.I. strings have no placement while the table and the manual disagree on which bulbs each string lights, and nine sprite-only lamps and the playfield bulb of flasher circuit 26 have no socket in the table; every other fitted playfield device has an observed or validated placement or a controlled not-applicable record.
