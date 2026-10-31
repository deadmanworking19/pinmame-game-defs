# Nine Ball (Stern, 1980) spatial review

Status: incomplete. No playfield lamp is placed and every placement is `observed`, so the machine record stays `partial` at `machines/partial/stern/nine-ball-1980.json`.

The geometry source is the retained `Nine Ball (Stern 1980).vpx` (bord, 1.0, June 2017) at SHA-256 `fdd7e6c53a9046e29d96b4acbbf01743d892447851b28f880df5367af2759270`; its embedded script (SHA-256 `db63ad0f77f1361e34ee49b13ad852ae34a972de6d64c6331d1f6cfba181e902`) binds the same switches and coils as the two pinned known-working corpus scripts, apart from the defects listed below. Exact playfield bounds are left 0, top 0, right 952, bottom 1927, and every canonical coordinate is x/952 and y/1927 rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, in normalized VPX/player view.

## Evidence decisions

- The script's bindings choose each switch's and coil's object. A switch sits on its trigger, target, bumper, kicker or spinner; a coil sits on the object it moves.
- Lamps are not placed. The table's 188 lights include 128 bulb-mode lights, but none shows a bulb mesh, and docs/SPATIAL.md requires a real bulb for a socket.
- General illumination is placed on the 25 `BulbFil` bulb-filament primitives, each with a `GI_<n>` light at its centre (a light at the centre of a separate bulb primitive shows its bulb). The table's grouping gives no quantity, and nothing machine-side names a G.I. string, so the placements stay `observed`.
- The table mis-binds the lock lane: trigger `sw38` writes switch 39, and trigger `sw1` at the top of the lane has no handler. Both triggers sit where the manual's switch drawing puts 38 and 39, so 38 is placed on `sw38` and 39 on `sw1`, with the defect stated on each switch.

## Explicit projections

- pinmame.input.switch 29: Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own hit event.
- pinmame.input.switch 30: Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own hit event.
- pinmame.input.switch 38: The retained script mis-binds the lock lane: trigger `sw38`, in the middle of the lane where the manual's switch drawing puts 38, writes switch 39, so that table never closes 38. Placed on trigger `sw38`, whose position and name agree with the drawing; the binding is a defect of the table.
- pinmame.input.switch 39: The retained table has no trigger bound to 39 at the top of the lock lane: its `sw39` handler has no object, and the trigger there is named `sw1` and has no handler. Placed on that trigger, at the top of the lane where the manual's switch drawing puts 39; a projection resting on the drawing, not on a script binding.
- pinmame.output.solenoid 1: Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 2: Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it.
- pinmame.output.solenoid 3: Projected onto the right three-bank it resets: the mean of the table's own three target objects. The reset coil sits under the bank and has no object.
- pinmame.output.solenoid 4: Projected onto the center three-bank it resets: the mean of the table's own three target objects.
- pinmame.output.solenoid 9: Placed on the drop target it knocks down (table `sw15`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 10: Placed on the drop target it knocks down (table `sw14`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 11: Placed on the drop target it knocks down (table `sw13`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 12: Placed on the drop target it knocks down (table `sw12`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 13: Placed on the drop target it knocks down (table `sw11`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 14: Placed on the drop target it knocks down (table `sw10`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 15: Placed on the drop target it knocks down (table `sw9`); the coil sits behind the target and has no object.
- pinmame.output.solenoid 17: Projected onto the eight-target bank it resets: the mean of the table's own eight target objects.
- pinmame.output.solenoid 20: Placed on the loop drop target it raises (table `sw21`); the coil sits under the target and has no object.
- physical.input.direct 1: Placed on the left flipper pivot: the end-of-stroke contact is mounted on its flipper assembly.
- physical.input.direct 2: Placed on the right flipper pivot: the end-of-stroke contact is mounted on its flipper assembly.

## Counts

- Placements: 75 (75 observed) on 51 records
- Records with a controlled `cabinet_or_service` record: 24
- Records with a controlled `dip_switch` record: 32
- Records with a controlled `internal_nonvisual` record: 1
- Records with a controlled `unused` record: 2
- Records with a controlled `virtual` record: 2
- Records with no spatial key: 60

## Excluded table objects

- L<n>, L<n>a-c, L<n>b and l<n>a-b lights, the Bumper1Light and the f11, f29 and f30 flashers: insert lights and glows the script binds to lamp numbers; none of the table's 188 lights shows a bulb mesh, so none marks a socket
- LDrop<bank><n> lights (collection dtLeftLights): drop-target glows the script switches from the target hit events, not lamp outputs
- GI_<n> and Light<n> lights (collection GI): placed through the BulbFil<n> bulb-filament primitive each GI_<n> light sits on, not on their own
- BulbTop<n> primitives: the glass tops of the same 25 general-illumination bulbs
- LED and led display-segment flashers, the BG backglass flashers and the Flasher<n> lighting overlays, none of them bound to a lamp number: backbox and render helpers, not playfield devices
- Drain and BallRelease kickers: the virtual trough's entry and its shooter-lane exit, not physical trough positions
- Gate1, Gate2, Gate6, BallReleaseGate and the hidden Gate3: passive or helper gates with no controller binding

## Blockers

- No playfield lamp is placed (56 of the 60): the retained table, the only Nine Ball table available, draws every insert with lights that show no bulb mesh, and the manual prints no lamp-location drawing, so no source marks a socket (docs/SPATIAL.md, Picking the bulb).
- The trough switches 33, 36 and 37 and the outhole kicker (public 7) are not placed: both known-working scripts and the table model the trough as a virtual ball stack with no object at the switches, and the location drawing prints the three switch numbers under the apron without arrows.
- Every switch, coil and general-illumination placement is `observed` from the one table; no factory-drawing callout check was made, and the manual's location drawings are 72 dpi scans.
- Lock-lane switches 38 and 39 rest on the table's triggers where the drawing puts them, but the table binds neither correctly (its sw38 writes 39 and its sw1 has no handler).

## Promotion decision

Promotion to `author_ready` is refused: no playfield lamp has a socket, the trough has no physical objects, and every placement rests on one table with no factory-drawing check. The record also carries one unresolved conflict about option switch 8, which does not concern placement. It stays `partial` with `coverage.missing = ["spatial_placement", "unresolved_conflicts"]`.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/stern/nine-ball-1980/archive/extracted-vpxtool.manifest.json`, SHA-256 `4a4b69caf8ad25f5e082e8581a5cbe97b9c453ea1d8b84f19d6cd309e2019f4f`, 1303 files, 93067588 bytes.
- Object-centre dump of every extracted game item at `external:pinmame-review-artifacts/nine-ball-1980/table-geometry.json`.
