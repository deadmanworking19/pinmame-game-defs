# Data East RoboCop (1989)

Machine definition: `machines/partial/data-east/robocop-1989.json`

## Identity and drivers

Pinned PinMAME publishes three drivers for the one physical machine: root `robo_a34` (3.4) and clones `robo_a30` (3.0) and `robo_a29` (2.9). All three share one `INITGAMES11` block and the same sound ROMs, so they run identical hardware. The ROM library holds `robo_a34` and `robo_a30`; both were walked through the ROM's own service tests and print the same names in the same order. `robo_a29` is not held and was not run.

`INITGAMES11(robo, GEN_DE, de_dispAlpha3, FLIP1516, SNDBRD_DE1S, S11_LOWALPHA, 0)` sets generation `GEN_DE` (`0x1000`), two 16-character alphanumeric rows, `hw.flippers = FLIP1516`, `hw.display = S11_LOWALPHA`, no `gameSpecific1` flags (so no `S11_MUXDELAY`), an empty special-solenoid switch table and `sxx.muxSol = 10`.

## Controller contract

- Inputs: service buttons -7 (Black, Step) and -6 (Green, Forward/Reverse), jumper W7 at DIP 0, matrix 1-64 and PinMAME's flipper column 81-88.
- Outputs: lamps 1-64 and public solenoids 1-50.
- Solenoid 10 is the A/B relay K1. The eight L/R pairs share a driver: L01-L08 publish at 1-8 and R01-R08 at 25-32. Only R01-R06 carry coils. 31 and 32 have no branch, but PinMAME publishes them from the same driver bits as the fitted L07 and L08 flashers whenever K1 is energized, so their availability stays `unknown`.
- Solenoid 11 is the G.I. relay; 23 is Game On; 24 and 33-44 are unused; 45-48 are synthetic flipper winding states; 49 is a simulation shooter; 50 is reserved.
- Public 17-22 are the six switch-triggered special solenoids. Pinned `s11.c` permutes the PIA handlers so printed SP1 Right Turbo Bumper lands at 17, SP3 Left Slingshot at 18, SP4 Left Turbo Bumper at 19, unfitted SP6 at 20 (availability `unknown`, since it is PIA state PinMAME could still publish), SP5 Right Slingshot at 21 and SP2 Center Turbo Bumper at 22. `sxx.ssSw` is empty, so PinMAME never publishes these addresses for this driver: a recreation fires the bumpers and slingshots from its own switch events.

Every matrix switch rests open. The ROM's Active Switch test reads NONE with all public switches at 0 and names each switch as it closes, so `normally_closed` is false throughout.

FLIP1516 makes `core_updateSw` copy the cabinet buttons into 15 and 16 on every update: left button 84 into 15, right button 82 into 16, fabricating 47/48 and 45/46 from them. **A recreation drives 82/84, never 15/16.** The ROM's Switch Test names the held left flipper key LEFT FLIPPER at 15 and the right RIGHT FLIPPER at 16. The manual prints the flippers' Instant Info and EOS contacts there; PinMAME models no EOS on this platform, so the label follows what a consumer receives.

## Names

The manual's matrix, its part list, the ROM's own tests and the coil schematic name a few devices differently. Each set denotes one device, so none is a conflict:

- Switch 17: matrix and ROM Laser Kick, part list Left Outlane — the left-outlane rollover in front of the kickback.
- Switch 28 / coil 27: matrix Left Eject, ROM MID EJECT, schematic Middle Eject — the upper-left saucer (location drawing R03).
- Switch 29 / coil 28: matrix Center Eject, list and ROM Top Eject, schematic Ball Guide Eject — the top saucer (R04).
- Coil 26: schematic Trough, ROM SHOOTER LANE — the trough eject into the shooter lane.

## Wiring

The ROM's Switch Test and Lamp Test print each address's wire code on the Player 3/4 row. Every code matches the manual's matrix headers: switches return 91-98 and drive 51, 52, 53, 54, 50, 56, 57, 58 by column; lamps return 21, 20, 23-28 and drive 41, 42, 43, 40, 45-48. Coil Auto prints each driver's bank code, L01-L08, 09-16 and R01-R08.

## Flash lamps

The coil location page has a separate `Backbox Flash lamps` inset of nineteen bulbs. Together with the schematic's bulb counts, it gives each flash output's split: 1 has 3 backbox + 1 playfield, 3 has 2 + 1, 4, 5 and 6 have 1 + 1 each, 7 has 3 + 1, 9, 12 and 13 have 2 + 2 each, 14 and 15 have 1 + 3 each, and 2 and 8 are one playfield bulb each. Every output's total matches its schematic row. The playfield callouts agree with the table's flash objects: the L01-L06 ladder up the right center, 09 and 12 in the center, 13 lower right, 14/15 alternating up the right ramp, L07 at the left and L08 at the top left.

The coil part chart lists six 23-800 coils while the schematic draws seven (Vertical Up Kicker, Laser Kick and SP1-SP5). Both readings are kept in the excerpt.

## Lamps

Lamps 41-43 (Back Panel Red, Yellow, Green) are on the back panel at the rear of the playfield. The retained table draws them on the apron; those are presentation proxies, and no source registers the lamps' positions on the panel, so they have no placement yet. The manual's drawing does not show lamps 44, 63 or 64. The parts list's `Red Mini Lamp - ED 209 (2)` fits 63 and 64, ED 209 Left and Right, but that pairing is inferred from the names. Lamp 56 is unused.

## Retained-table defects

These are bugs in the retained table, not facts about the machine:

- Its right turbo bumper (Bumper3) pulses switch 46 instead of 48, so the table never closes 48.
- It has no object for the two 10-point switches 37 and 38.
- Its key handlers write switch 15 from the right flipper key and 16 from the left. PinMAME overwrites both every update, so the writes have no effect; the real flipper input goes through DE.VBS to 82/84.
- It adds Light44, Light46, Light48 and Light50, the objects for lamps 52-55, to its GI collection.

## Mechanisms

- A three-ball trough (500-5012-00) is fed by the outhole kicker (25) and ejects into the shooter lane (26).
- Three Playfield Eject saucers sit at the upper left (switch 28, coil 27), top (29 / 28) and top right (30 / 29). The right one is the Scanner shot.
- The Vertical Up Kicker (45 / 30) lifts the ball onto a feed ramp to the left flipper.
- The Laser Kick (17 / 16) is a left-outlane kickback.
- Three turbo bumpers and two slingshots fire from the special-solenoid circuit.
- There are fixed standups: a green four-bank (33-36), a yellow three-bank (41-43) and two 10-point switches (37, 38).
- The right trap ball (23) is documented only by its switch and two lamp names. The table builds it as a captive ball below a target, but its physical construction is unconfirmed.
- The remaining features are passive: the 2-0-9 top lanes, the Left Catch Ramp and Right Ramp, a spinning target (44) and the return lanes and outlanes. The playfield has no drop targets, diverters, magnets or motors.

## Coverage

Status stays `partial`; `coverage.missing` is [`output_semantics`, `mechanism_behavior`, `polarity`, `spatial_placement`].

- `output_semantics`: special solenoids 17-22 are wiring-derived and never published, so nothing at runtime confirms them; unfitted 20, 31 and 32 may still carry public state nothing explains.
- `mechanism_behavior`: no retained source documents the trap ball's construction, and the special-solenoid firing is unobservable.
- `polarity`: the Green Forward/Reverse button's contact construction and published level are not settled.
- `spatial_placement`: every placement is a retained-table candidate. The trough switches, the 10-point switches and back-panel lamps 41-43 have none.

## Recreation boundary

Consume PinMAME's decoded outputs, with K1 already applied to 25-30. Drive the flipper buttons at 82/84. Fire the turbo bumpers and slingshots from switch events, because PinMAME will not publish 17-22. Put lamps 41-43 on the back panel at the rear of the playfield, and split each flash output's bulbs between the backbox and the playfield as listed above.
