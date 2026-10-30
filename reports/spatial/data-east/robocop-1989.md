# RoboCop spatial-resolution report

Exact retained-table bounds: `left=0`, `top=0`, `right=952`, `bottom=2256`.

## Extraction identity

- Manifest algorithm: SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False.
- Manifest SHA-256: `5c415cb2b5f01b156fb31af6896e4ca58a97beb1636dfb2ba5d6c4148db0f476`

## Promotion decision

Keep partial. Every public address is named and wired from the manual and confirmed by the ROM's own tests on two revisions, but the special-solenoid mapping is unobservable, the trap-ball construction is undocumented, one service-button polarity is open, and placements are candidates.

## Blockers

### output_semantics

The special-solenoid addresses are derived from the manual's SP wiring and pinned s11.c, but PinMAME never publishes them for this driver (sxx.ssSw is empty), so no runtime evidence confirms the mapping; unfitted SP6 (20) and mux branches R07/R08 (31, 32) can still carry public state nothing explains.

Would resolve: Static analysis of the ROM's PIA special-line writes, or a gameplay trace of 20, 31 and 32 alongside the bumper and slingshot switches.

Devices: `coil.driver-17`, `coil.driver-18`, `coil.driver-19`, `coil.driver-20`, `coil.driver-21`, `coil.driver-22`, `coil.driver-31`, `coil.driver-32`

### mechanism_behavior

The trap-ball construction is documented only by a switch and two lamp names, and the switch-to-coil firing of the slingshots and turbo bumpers is wiring-derived and runtime-unobservable.

Would resolve: A photograph of an original playfield's right trap-ball lane, and the special-solenoid evidence above.

Devices: `mechanism.trap-ball`, `mechanism.left-slingshot`, `mechanism.right-slingshot`, `mechanism.left-turbo-bumper`, `mechanism.center-turbo-bumper`, `mechanism.right-turbo-bumper`

### polarity

The Green Forward/Reverse service button toggles the ROM's direction on each press, but no retained source settles its contact construction or the level PinMAME publishes for it.

Would resolve: A coin-door wiring page or a harness trace of the published -6 level across a direction change.

Devices: `switch.diagnostic-6`

### spatial_placement

Lamp, flash, GI and coil coordinates are retained-table candidates; three trough switches, both 10-point switches and the three back-panel lamps have no placement.

Would resolve: A drawing callout check against a registered playfield drawing or photograph, and positions for the trough and 10-point switches.

Devices: `lamp.matrix-1`, `lamp.matrix-2`, `lamp.matrix-3`, `lamp.matrix-4`, `lamp.matrix-5`, `lamp.matrix-6`, `lamp.matrix-7`, `lamp.matrix-8`, `lamp.matrix-9`, `lamp.matrix-10`, `lamp.matrix-11`, `lamp.matrix-12`, `lamp.matrix-13`, `lamp.matrix-14`, `lamp.matrix-15`, `lamp.matrix-16`, `lamp.matrix-17`, `lamp.matrix-18`, `lamp.matrix-19`, `lamp.matrix-20`, `lamp.matrix-21`, `lamp.matrix-22`, `lamp.matrix-23`, `lamp.matrix-24`, `lamp.matrix-25`, `lamp.matrix-26`, `lamp.matrix-27`, `lamp.matrix-28`, `lamp.matrix-29`, `lamp.matrix-30`, `lamp.matrix-31`, `lamp.matrix-32`, `lamp.matrix-33`, `lamp.matrix-34`, `lamp.matrix-35`, `lamp.matrix-36`, `lamp.matrix-37`, `lamp.matrix-38`, `lamp.matrix-39`, `lamp.matrix-40`, `lamp.matrix-44`, `lamp.matrix-45`, `lamp.matrix-46`, `lamp.matrix-47`, `lamp.matrix-48`, `lamp.matrix-49`, `lamp.matrix-50`, `lamp.matrix-51`, `lamp.matrix-52`, `lamp.matrix-53`, `lamp.matrix-54`, `lamp.matrix-55`, `lamp.matrix-57`, `lamp.matrix-58`, `lamp.matrix-59`, `lamp.matrix-60`, `lamp.matrix-61`, `lamp.matrix-62`, `lamp.matrix-63`, `lamp.matrix-64`, `coil.driver-1`, `coil.driver-2`, `coil.driver-3`, `coil.driver-4`, `coil.driver-5`, `coil.driver-6`, `coil.driver-7`, `coil.driver-8`, `coil.driver-9`, `coil.driver-12`, `coil.driver-13`, `coil.driver-14`, `coil.driver-15`, `coil.driver-11`, `switch.matrix-48`, `switch.matrix-11`, `switch.matrix-12`, `switch.matrix-13`, `switch.matrix-37`, `switch.matrix-38`, `lamp.matrix-41`, `lamp.matrix-42`, `lamp.matrix-43`

## Unresolved

- `unplaced_devices`: The table models the trough as a ball stack with no geometry and has no object for the two 10-point switches; the manual draws back-panel lamps 41-43 above the playfield outline without a registered frame, and the table's apron objects for them are proxies.
- `flasher_socket_binding`: The manual fixes each flash output's backbox/playfield bulb split and its playfield region, but not its socket centers.

## Resolver controls

- Asserted both exact gamedata.json bounds (0,0)-(952,2256) before normalization; no other machine's geometry is reused.
- Read every switch, lamp and coil table cell from rendered manual pages; the noisy PDF text layer only located pages.
- Took sensor placements from the script-bound objects (triggers, targets, saucers, bumpers, spinner, slingshot walls) and lamp and flash placements from the objects the script binds to each address.
- Compared the coil location drawing's callouts with the table's flash objects: every flash output's callout falls in the same playfield region as its bound objects, and every R-side kicker callout at its saucer or kicker.
- Used the coil location page's backbox inset and the lamp location drawing's back-panel row for physical-plane classification only; neither drawing has a registered frame.

## Excluded helpers

- `back-panel-lamps`: L41-L43 and Flashers F41-F43 sit in the apron area of the table, but the manual draws lamps 41-43 on the back panel at the rear of the playfield; the apron objects are presentation proxies and give those lamps no coordinate.
- `gi-lamp-overlap`: Light44, Light46, Light48 and Light50 belong to the GI collection and are also bound to lamps 52-55; they are placed only as lamps.
- `gi-and-flash-proxies`: The GI collection and the grouped F* flash lights are visual effects, not surveys of physical bulb sockets.
- `synthetic-flipper-states`: Public outputs 45-48 are PinMAME-generated winding states of the two physical flippers and carry no placement.
