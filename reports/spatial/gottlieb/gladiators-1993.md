# Gladiators (Gottlieb, 1993) spatial review

Status: observed. The machine record stays `partial` at `machines/partial/gottlieb/gladiators-1993.json`; its spatial dimension stays open because of the 5 spatial blockers below.

The geometry source is the retained `Gladiators (Premier 1993) v1.1.1 VR.vpx`, a VR edit of Kiwi's VPX v1.1.1, SHA-256 `b2925083424e053ebf9149657301b4358ef5448008ba41f3fd7e747c1d126ef9`. Its embedded script (SHA-256 `0c8c67f2e39b62597bc4b067fd9b1fb092a402deba8e673067b877d718f2380f`) binds every controller address exactly as the pinned known-working v1.1.1 script does. Bounds are `left=0 top=0 right=952 bottom=2162`; every coordinate is x/952 and y/2162, rounded to at most six places. `evidence/excerpts/gottlieb.gladiators.1993/vpx-table-objects.md` lists each placed object, its coordinate and the script lines that bind it, and the curator's `verify_retained_table` re-derives every coordinate from the retained extraction and OBJ export.

## Evidence decisions

- A placement is the table object the script binds to the address: a trigger, target, spinner, gate, kicker, bumper or slingshot wall for a switch, the `l<n>` light `UpdateLamps` fades for each lamp, the light under each flasher dome, the object a coil moves or kicks from, and each G.I. bulb light `GIRelay` switches.
- Primitives whose stored position is not the part's centre (the kicking targets, the catapult ramp and the billboard LED bulbs) are placed at the centre of their world-space mesh from `vpxtool export obj --units vpu`.
- Sensors and coils with no table object of their own are documented projections onto their own mechanism's object.
- Backbox and cabinet devices take controlled `not_applicable` records: the six lightbox lamps, the credit-button lamp, the lightbox and game-over relays, the shaker motor, the knocker, the coin meter, the cabinet and flipper-button switches, the test inputs and the DMD.
- No placement is validated: no factory drawing is retained to check it, and only one table is.

## Explicit projections

- Switch 30: Projected onto the catapult ramp (Primitive RMotor, world mesh centre), the moving rail the script turns about its top end and whose home step writes this switch (.AddSw 30, 0, 0); the sensor has no object of its own.
- Switch 33: Projected onto the ball release (Kicker BallRelease), the trough exit the script's four-ball stack kicks from; the script keeps the trough as a virtual stack and has no object for this switch.
- Solenoid 4: Projected onto the left kicking target it drives (the script's KickingT primitive, which it swings on the target's hit); the coil has no object of its own.
- Solenoid 5: Projected onto the right kicking target it drives (the script's KickingT primitive, which it swings on the target's hit); the coil has no object of its own.
- Solenoid 6: Projected onto the left hole the script ejects from; the coil has no object of its own.
- Solenoid 7: Projected onto the top hole the script ejects from; the coil has no object of its own.
- Solenoid 10: Projected onto the bank's middle drop target; the reset coil sits below the bank and has no object of its own.
- Solenoid 11: Projected onto the center upkicker the script lifts the ball from; the coil has no object of its own.
- Solenoid 12: Projected onto the right upkicker the script ejects from; the coil has no object of its own.
- Solenoid 23: Projected onto the catapult ramp its motor turns; the relay and motor have no object of their own.
- Solenoid 28: Projected onto the trough exit the script releases balls from; the coil has no object of its own.
- Solenoid 29: Projected onto the outhole kicker the script receives drained balls on; the coil has no object of its own.

## Counts

- Placements: 153 (observed 153)
- Located input addresses: 30
- Located output bindings: 105
- Inputs with an omitted spatial key: 0
- Outputs with an omitted spatial key: 7
- Inputs with a controlled `cabinet_or_service` record: 14
- Inputs with a controlled `unused` record: 63
- Inputs with a controlled `virtual` record: 1
- Outputs with a controlled `cabinet_or_service` record: 12
- Outputs with a controlled `unused` record: 4
- Outputs with a controlled `virtual` record: 4

## Excluded table objects

- Bulb<n>a Light doubles of the G.I. bulbs, and Bulb8T15, Bulb8T25 and Bulb8T35 beside the drop targets: Bulb1-Bulb19, the members with a bulb mesh, are the placements
- giB1-giB3 and LR1-LR3 Light objects, which model no bulb
- Flasher sprites: fgit, the f<n> lamp and flasher overlays, and f19-f21; a sprite is a render helper, not a socket
- The l197a companion light the script fades with l197, and the LEDR primitives of the apron LEDs, which sit at their l<n> lights
- VR room, cabinet and backbox objects

## Blockers

- No factory drawing is retained: IPDB lists the instruction manual pages and the coil, fuse and switch charts without hosting them, and no other attributable copy was found, so no placement can be checked against the machine's own switch, lamp or coil location drawings.
- Only one table is retained, the VR edit of Kiwi's VPX v1.1.1, and the pinned v1.0.1 script is the same author's earlier release of it, so no independently built geometry can confirm a placement. Every placement comes from that table and stays observed.
- Solenoid 31 (Tilt Relay, playfield G.I.): the 19 placements are the bulb lights the table's GIRelay switches; a table's grouping is not the machine's wiring and the bulb count is unknown, so they stay observed without a quantity.
- Solenoids 8, 9, 22 and 24 are drawn in the script's backbox and solenoids 19-21 only as flasher sprites, so none of the seven is placed or classified; the lamps 112-117 are lightbox lamps by the ROM's own names.
- Ramp motor switch 30 and trough switch 33 have no table object of their own and are projected onto the catapult ramp and the ball release.

## Promotion decision

Every controller address is enumerated with a semantic disposition taken from the ROM's own service tests, the mechanisms are covered, and polarity is settled for every switch by the read path, the ROM's Switch Matrix Test and the known-working script. Promotion to `author_ready` is refused because every playfield placement rests on one community table's geometry with nothing independent to check it, so `coverage.missing` is `["spatial_placement"]`. The instruction manual's switch, lamp and coil location drawings, or a second table built independently from the machine, would close the gap.
