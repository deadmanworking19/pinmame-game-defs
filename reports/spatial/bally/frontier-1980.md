# Frontier (Bally 1980) spatial blockers

Coverage: **partial**; missing `input_semantics`, `spatial_placement`.

The coordinate source is the retained `Frontier (Bally 1980).vpx` (bord v2.0) at SHA-256 `39a399a28bff018efc10e91109bf455f2702516c10b10c18764ac31a12a8dbf2`, bounds `left=0 top=0 right=952 bottom=1974`, so every coordinate is x/952 and y/1974 rounded to six places. The flipper pivots land at y 0.832 and the drain at 0.927.

Placements by status: 42 observed. Cabinet, backglass, option-switch, unused and virtual devices carry controlled `not_applicable` records (20 cabinet_or_service, 32 dip_switch, 27 unused, 2 virtual). 54 used devices are unplaced.

## Evidence decisions

- Switch, coil and flipper placements are the objects the script binds (the switch handlers, the drop-target banks, the Drain and sw12 kickers, Gate2, the flippers). Each sits where the manual's Figure V draws the part, but no callout check was made, so they stay `observed`.
- Switch 1 has four rebound contacts; each rubber wall sw1a1-sw1a4 has its own placement, at the four places Figure V prints 01.
- Switch 8 and the outhole kicker take the table's Drain kicker, the outhole Figure V marks; the BallRelease kicker in the shooter lane is a table helper.
- The in-line drop-target reset is projected onto the mean of its three targets and the right-bank reset onto its middle target; both coils are hidden assemblies under their banks.
- The gate (17) takes the table's invisible gate Gate2 at the top of the saucer lane, where Figure V prints 11.
- Back box lamps 11, 13, 27, 29, 45 and 61, the knocker, the coin lockout, the K1 relay, all cabinet and service switches, the option switches, the displays and the synthetic flipper states 45 and 47 (virtual) take controlled `not_applicable` records.

## Why no lamp is placed

- The table has 55 lamp lights `L<n>`. Only `L10`, `L26`, `L42` are bulb-mode lights (the bumper lamps, bound through the BumperLeft, BumperCenter and BumperRight collections with BumperLight1-3), and none of the lamp lights shows a bulb mesh; the rest are classic lights drawn over the inserts.
- The table models bulbs as 54 `BulbFil`/`BulbTop` primitives. Every one sits on a general-illumination light, a `GI_<n>` or `Light8` of the table's `GI` collection or `GI_12a`, `GI_13a` or `GI_14a` of its drop-target light collections (`GI_1`, `GI_10`, `GI_11`, `GI_12a`, `GI_13a`, `GI_14a`, `GI_15`, `GI_16`, `GI_17`, `GI_18`, `GI_19`, `GI_2`, `GI_20`, `GI_21`, `GI_22`, `GI_23`, `GI_3`, `GI_4`, `GI_5`, `GI_6`, `GI_7`, `GI_8`, `GI_9`, `Light8`), at most 6.427 units away; the nearest lamp light to any of them is `L9`, 64.6 units away.
- A light that marks no bulb marks no socket, so the 54 playfield lamps are unplaced. A table that models the lamp bulbs, or a registered playfield photograph, would settle them.

## Excluded objects

- L48: a light beside the saucer rollover that the script leaves unbound; 48 is a lamp decoder hole.
- The `GI_<n>` and `Light8` lights of the `GI` collection, and the `GI_12a`-`GI_14c` drop-target lights of the `DTLeftLights`/`DTRightLights` collections that the drop-target handlers and resets switch: table-side lights bound to no lamp output. Frontier has no general-illumination output; the wiring sheet feeds the G.I. from the transformer's 5.9 VAC.
- BallRelease: the kicker that throws the ball into the shooter lane, a table helper.

## Unplaced used devices

- `lamp.snake-left`
- `lamp.hawk-left`
- `lamp.lion-left`
- `lamp.wolf-left`
- `lamp.bear-left`
- `lamp.a-rollover-lane`
- `lamp.10k-frontier`
- `lamp.50k-frontier`
- `lamp.left-target-arrow`
- `lamp.left-thumper-bumper`
- `lamp.right-flipper-feed-lane`
- `lamp.2x-drop-target`
- `lamp.gate-arrow`
- `lamp.snake-center`
- `lamp.hawk-center`
- `lamp.lion-center`
- `lamp.wolf-center`
- `lamp.bear-center`
- `lamp.b-rollover-lane`
- `lamp.20k-frontier`
- `lamp.60k-frontier`
- `lamp.center-target-arrow`
- `lamp.bottom-thumper-bumper`
- `lamp.left-flipper-feed-lane`
- `lamp.3x-drop-target`
- `lamp.2x-predators`
- `lamp.snake-right`
- `lamp.hawk-right`
- `lamp.lion-right`
- `lamp.wolf-right`
- `lamp.bear-right`
- `lamp.c-rollover-lane`
- `lamp.30k-frontier`
- `lamp.spinner-1000`
- `lamp.right-target-arrow`
- `lamp.right-thumper-bumper`
- `lamp.same-player-shoots-again`
- `lamp.right-out-special`
- `lamp.4x-drop-target`
- `lamp.3x-predators`
- `lamp.a-b-c-extra-ball`
- `lamp.a-b-c-special`
- `lamp.45k-predators`
- `lamp.4x-frontier`
- `lamp.predators-special`
- `lamp.4x-grizzly-target`
- `lamp.40k-frontier`
- `lamp.30k-grizzly-target`
- `lamp.2x-frontier`
- `lamp.3x-frontier`
- `lamp.credit-indicator`
- `lamp.left-out-special`
- `lamp.special-drop-target`
- `lamp.4x-predators`
