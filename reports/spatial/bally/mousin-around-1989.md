# Mousin' Around! (Bally, 1989) spatial review

Status: the machine record stays `partial` at `machines/partial/bally/mousin-around-1989.json`; its spatial dimension stays open because of the 8 spatial blockers below.

The geometry source is the retained known-working `Mousin_ Around! (Bally 1989).vpx` by Herweh (version 1.0), SHA-256 `6c914b95a3062036b285f751b606b1468f86d93a12f86943fc29405ed2be4c9d`, whose embedded script (SHA-256 `959acd6b408903f3c71c8c0cf1fedf3345a3cc1105f0399e42824e22dd1cf282`) is the binding authority. Bounds are `left=0 top=0 right=964 bottom=2162`; every coordinate is x/964 and y/2162, rounded to at most six places.

## Evidence decisions

- A switch placement is the centre of the table object the script binds to the address: a trigger, target, kicker, bumper or slingshot wall.
- A flasher or G.I. placement is the bulb primitive the script lights (`pBulbN`), or the bulb-mesh light in a bumper cap, or the back-panel flasher's dome; a light that sits on no bulb marks no socket.
- Sensors and coils with no table object of their own (the trough, trap up/down, motor-limit and diverter switches, and the outhole, feeder, trap, motor and diverter drives) are documented projections onto their own mechanism's object.
- Where the table lights more bulbs for a flasher than the Solenoid Table prints, the spatial key is omitted rather than guessing which one is the socket.
- Backbox and cabinet devices take controlled `not_applicable` records: the insert-board jackpot lamps 57-63, the insert G.I. relay (9), the knocker, the A/C relay and its switch, the cabinet, flipper and diagnostic switches, the Country jumper and both displays.

## Explicit projections

- Switch 11: Projected onto the table's ball-release kicker (Kicker BallRelease, object centre): the retained script models the trough as one three-ball cvpmBallStack (bsTrough.InitSw 0, 11, 12, 13 with InitKick BallRelease, script lines 191-196) and has no object per trough position. The switch drawing places 11 at the right end of the trough.
- Switch 12: Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11.
- Switch 13: Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11.
- Switch 33: Projected onto the table's right trap kicker (Kicker rightTrap41), the ball eater whose up/down switch this is (part of B-20-9629); the script writes it from its trap routines (lines 615-708) and has no object for it.
- Switch 34: Projected onto the table's left trap kicker (Kicker leftTrap42), the ball eater whose up/down switch this is (part of B-20-9629); the script writes it from its trap routines (lines 615-708) and has no object for it.
- Switch 43: Projected onto the middle target of the table's motorized bank (Primitive pTarget30, object position): the motor limit switches sit on the motor under the playfield, and the script writes 43 and 50 from its motor-bank timer (lines 751-821).
- Switch 49: Projected onto the table's diverter arm (Primitive pDiverterArm, object position), the moving part of the C-12902-1 Ball Deflector whose A-12953 Mini Switch this is; the script toggles 49 on each diverter pulse (lines 709-745).
- Switch 50: Projected onto the middle target of the table's motorized bank (Primitive pTarget30); see switch 43.
- Solenoid 1: Projected onto the drain kicker the script's ball stack receives balls on; the B-8039-2 outhole kicker coil has no object of its own.
- Solenoid 2: Projected onto the ball-release kicker the script kicks from; the C-9638-1 feeder coil has no object of its own.
- Solenoid 3: Projected onto the right trap's kicker; the ball eater's AE-26-1400 up coil sits under the playfield and has no object of its own.
- Solenoid 4: Projected onto the left trap's kicker; the ball eater's AE-26-1400 up coil sits under the playfield and has no object of its own.
- Solenoid 5: Projected onto the right trap's kicker; the ball eater's SM1-28-800 down coil sits under the playfield and has no object of its own.
- Solenoid 8: Projected onto the left trap's kicker; the ball eater's SM1-28-800 down coil sits under the playfield and has no object of its own.
- Solenoid 11: Projected onto the motorized bank's middle target; the motor and its relay sit under the playfield and have no object of their own.
- Solenoid 14: Projected onto the diverter arm; the C-12902-1 Ball Deflector's AE-23-800 coil has no object of its own.

## Counts

- Placements: 105 (observed 105)
- Located input addresses: 48
- Located output bindings: 22
- Outputs with an omitted spatial key: 60
- Inputs with a controlled `cabinet_or_service` record: 15
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `internal_nonvisual` record: 1
- Inputs with a controlled `unused` record: 12
- Outputs with a controlled `cabinet_or_service` record: 9
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `unused` record: 2
- Outputs with a controlled `virtual` record: 20

## Blockers

- Lamps 1-7 and 9-48: the retained table draws every playfield insert with Light objects that show no bulb and sit on no bulb primitive, so under the bulb-picking rule no insert has a socket and their spatial keys are omitted. A table that models the insert bulbs (the pinned corpus script of the later version 2.1 edit mentions 3D inserts, but that table is not retained), or a measured lamp drawing, would place them.
- Lamp 8 (Jackpot): the lamp page lists it among the playfield lamps but its drawing has no callout for it, and the table shows it as a backboard decal with the back-panel lamps; its spatial key is omitted.
- Lamps 49-56 (MILLION letters and Build Jackpot) stand on the back panel; the table shows them as backboard decals, not bulbs, so their spatial keys are omitted.
- Solenoids 27, 30 and 31 (Left Side, Right Ramp and Left Ramp flashers): the Solenoid Table prints one playfield bulb each, but the table lights two, three and two bulbs for them, and no source says which is the machine's socket, so their spatial keys are omitted.
- Solenoid 32 (Timer Flasher): the Solenoid Table prints two playfield bulbs and the drawing marks 08C, but the table lights only a bulbless light for it, so its spatial key is omitted.
- Solenoids 25 and 26 (flipper flashers): the Solenoid Table prints two playfield bulbs each and the table models one, so each keeps one observed placement and the second bulb has none.
- Solenoid 10 (Playfield G.I. Relay): the 36 placements are the bulbs of the retained table's G.I. collections; this record cites no G.I. layout from the manual and a table's grouping is not the machine's wiring, so they stay observed without a quantity.
- No placement was checked against the manual's numbered location drawings, whose callouts were read only for their order along each edge; every located placement keeps the table's observed status.

## Promotion decision

Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the mechanisms are covered, and polarity is settled by the ROM's Switch Levels test. Promotion to `author_ready` is refused: the playfield inserts and several flashers have no socket in the retained table, the G.I. placements come only from the table's grouping, no placement was checked against the manual's drawings, and the LA-4C competition driver's ROM is not available, so `coverage.missing` is `["variant_differences", "spatial_placement"]`. A table that models the insert bulbs, measured lamp and flasher drawings, and the LA-4C ROM (whose service tests name every address it drives) would close them.
