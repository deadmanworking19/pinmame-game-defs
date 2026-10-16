# Paragon (Bally 1979) spatial audit

Coverage: **partial**; missing `spatial_placement`.

The coordinate source is the retained `Paragon (Bally 1979).vpx` (bord v2.37) at SHA-256 `3c83b8787112f82880ae7c3ff2f6fbddb846029562359300db13691ea8dcb094`, bounds `left=0 top=0 right=1257 bottom=1974`, so every coordinate is x/1257 and y/1974 rounded to six places. The lower flipper pivots land at y 0.832 and the drain at 0.952.

Placements by status: 2 observed, 97 validated. Cabinet, backglass, option-switch and unused devices carry controlled `not_applicable` records (20 cabinet_or_service, 32 dip_switch, 22 unused).

## Evidence decisions

- Switch and coil placements are the objects the script binds, checked against the manual's Figure V with `tools/drawing_callouts.py`: 33 of 35 checked placements land within 0.07 normalized of their own callout under both the control fit and the leave-one-out callout fit. Figure V prints solenoid self-test numbers in squares and switch numbers in circles, so the two are checked as separate pages of one image.
- Lamp placements are the table lights L<address>. Every one sits on an insert whose art names it (bonus values, the two PARAGON rows, golden-cliff, drop-target and waterlane values, the 2x/3x/5x multipliers, SHOOT AGAIN, the saucer special and the 5X treasure insert); the two uncaptioned Treasure Chamber inserts take the captions printed on the plastic beside them (SPECIAL above EXTRA BALL); the four uncaptioned spinner inserts follow the factory sheet's numbering, 1 at the bottom to 4 at the top, and a fifth insert below them is lit from the table's GI.
- The rebound switches 27 and 34 have parallel contacts; each contact has its own placement, the rubbers being connected pieces of the baked collidable primitives sw27a (two pieces) and sw34b, whose OBJ vertices scaled by the primitive size give world coordinates (checked on the visible baked primitive rubbers_visible against a vpxtool OBJ export).
- Switch 8 and the outhole kicker take the table's Drain kicker, the outhole Figure V marks; the BallRelease kicker in the shooter lane is a table helper.
- The in-line drop-target reset is projected onto the centre of its four targets and the waterfall reset onto its middle target; both coils are hidden assemblies under their banks.
- Backbox lamps 11, 13, 27, 29, 45 and 61, the knocker, the coin lockout, the K1 relay, all cabinet and service switches, the DIPs and the displays take controlled `not_applicable` records.

## Excluded objects

- Lights L11, L16, L27 and L29 (members of the table's GI collection in the four star rollovers) and GIxx (the fifth spinner-column insert): general illumination, no lamp output.
- The sw1a-sw4a and sw17a-sw19a secondary drop-target walls and the psw primitives: animation parts of the drop-target system.
- TriggerLF, TriggerRF and TriggerRF1: flipper physics helpers with no switch.

## Unvalidated placements

- `switch.500-point-rebound.upper-rebound`
- `switch.spinner.sensor`
