# Harlem Globetrotters On Tour (Bally 1979) spatial blockers

Coverage: **partial**; missing `spatial_placement`.

The coordinate source is the retained `Harlem Globetrotters On Tour (Bally 1979).vpx` (JPSalas VPX version 1.0) at SHA-256 `c6503062d2c4d49f2a16866be4df0df85c5ef000e21f7eed5a3e7ae3de8ed81e`, extracted with vpxtool git:v0.33.3 (551 files, 10,339,644 bytes, canonical manifest `148b066da476d89ff9da2fcdba031a070f0de4fc2806b471a7dcef11949cc89d`). Its bounds are `left=0 top=0 right=952 bottom=1974`, so every coordinate is x/952 and y/1974 rounded to six places. The lower flipper pivots land at y 0.826 and the drain at 0.974.

Placements by status: 42 observed. Cabinet, back box, option-switch, virtual and unused devices carry controlled `not_applicable` records (19 cabinet_or_service, 32 dip_switch, 29 unused, 2 virtual).

## Evidence decisions

- Switch and coil placements are the objects the script binds: the drop targets d1-d4, the saucer kickers sw24 and sw32, the trough's Drain kicker for the outhole switch and kicker, the spinners, triggers and stand-up targets, the bumper and slingshot objects the ROM fires for their own switches, and the flipper pivots. They stay `observed`: no factory-drawing callout check has been made.
- Switch 34 has two parallel contacts, each placed on its rubber wall (Sling1 in the upper left, Sling2 on the right).
- The drop-target reset is projected onto the centre of the four in-line targets; the coil is a hidden assembly under the bank.
- The right gate (17) is the invisible `RightLaneGate` flipper the script swings with `vpmSolDiverter`; Figure V prints its number in the right outer lane below switch 23.
- The thumper bumper lamps sit on the bumper cap bulbs `bumper2l` (26) and `bumper1l` and `bumper3l` (42), the only lamp lights the table draws as bulbs with a bulb model.
- Back box lamps 13, 27, 29, 45 and 61, the knocker, the coin lockout, the K1 relay, every cabinet and service switch, the option switches and the displays take controlled `not_applicable` records.

## The blocker

The other 53 used playfield lamps have no position. The retained table draws each insert with a Light whose `is_bulb_light` and `show_bulb_mesh` are both false; such a light marks no socket, the manual has no lamp location drawing, and nothing else retained places one. Completing the record needs a table that models the insert bulbs, retained with its geometry and checked against the art, and then a callout check of the switch and coil placements against Figure V with `tools/drawing_callouts.py`.

- `lamp.1k-bonus`
- `lamp.5k-bonus`
- `lamp.9k-bonus`
- `lamp.spinners-1-bottom`
- `lamp.spinners-5-top`
- `lamp.left-side-spinner-100`
- `lamp.saucer-g`
- `lamp.saucer-e`
- `lamp.side-target-5-top`
- `lamp.side-target-1-bottom`
- `lamp.center-e`
- `lamp.2x-bonus`
- `lamp.10k-bonus`
- `lamp.center-g`
- `lamp.2k-bonus`
- `lamp.6k-bonus`
- `lamp.dunk-shot-5k`
- `lamp.spinners-2`
- `lamp.dunk-shot-opens-gate`
- `lamp.left-side-spinner-200`
- `lamp.saucer-l`
- `lamp.dunk-shot-special`
- `lamp.side-target-4`
- `lamp.3x-bonus`
- `lamp.20k-bonus`
- `lamp.center-l`
- `lamp.3k-bonus`
- `lamp.7k-bonus`
- `lamp.right-spinner-advance-bonus`
- `lamp.spinners-3`
- `lamp.gate-open-when-lit`
- `lamp.left-side-spinner-1k`
- `lamp.saucer-o`
- `lamp.25k-left-outlane`
- `lamp.side-target-3`
- `lamp.shoot-again`
- `lamp.5x-bonus`
- `lamp.30k-bonus`
- `lamp.center-o`
- `lamp.4k-bonus`
- `lamp.8k-bonus`
- `lamp.left-spinner-advance-bonus`
- `lamp.spinners-4`
- `lamp.target-saucer-25k`
- `lamp.left-side-spinner-2k`
- `lamp.saucer-b`
- `lamp.saucer-target-special`
- `lamp.side-target-2`
- `lamp.dunk-shot-extra-ball`
- `lamp.credit-indicator`
- `lamp.g-l-o-b-e-special`
- `lamp.40k-bonus`
- `lamp.center-b`

## Excluded objects

- `gi1`-`gi20` (timer interval 100): the table's twenty general illumination bulb lights, which no PinMAME output drives.
- `BallRelease`: the trough's kick object in the shooter lane, a table helper.
- The second insert lights `l500`, `l200`, `l360` and `l520` of lamps 5, 20, 36 and 52: insert overlays like the first ones.
