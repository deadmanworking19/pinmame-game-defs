# Cyclone (Williams, 1988) spatial evidence

**Decision: partial.** Missing: spatial_placement.

x=0 left, x=1 right; y=0 rear/backglass, y=1 apron; normalized VPX/player view.

Geometry seed `tools/seeds/williams/cyclone-1988-geometry.json` SHA-256 `6f02f547b7c0f99b4b47fd37eb9f5598a75edac82c25c35be687e30465d6bfe6`.

A placement is the centre of the table object the known-working script binds to the address: a trigger, kicker, hit target, rubber, bumper, slingshot wall or flipper for a switch; the bumpers, slingshot walls and kickers for their coils; a light under a modelled flasher dome for a flasher; and the bulb-modelling lights of the GI collection for the playfield G.I. Lights with no bulb or dome mark no socket and take no placement.

## Blockers

- Playfield lamps 1-32 and 49-54 have no placement: none of the three retained Cyclone tables models a lamp bulb. vpmMapLights binds every lamp to insert-overlay lights (lNa, lNa1) that set no bulb mesh, and the COMET lamps 27-32 sit on the table's back panel above the playfield. A table that models the insert bulbs, or the manual's lamp drawing (PDF 43) measured balloon by balloon, would place them.
- Flasher circuits 9 (Spins Mystery Wheel), 15 (Boomerang, three #1251 lamps), 25, 26, 27, 28 and 32 have no placement, and 29 and 30 have one of their two playfield bulbs placed: the retained tables light these through lights with no flasher dome on the playfield (27's dome Flasher27p and 30's Flasher30p stand on the back panel above the playfield), and 9 has no light at all.
- No placement has been checked against the manual's numbered switch (PDF 40), lamp (PDF 43) and solenoid (PDF 44) drawings with a callout check, so every table placement stays observed.
- Solenoid 10 (playfield G.I.): the placements are the 32 bulb-modelling lights of the table's GI collection; the manual prints no G.I. bulb count or layout, so they stay observed without a quantity.

## Placed devices

| Device | Binding | Placements |
| --- | --- | --- |
| `switch.matrix-10` | pinmame.input.switch 10 | (0.489262, 0.962171) observed |
| `switch.matrix-11` | pinmame.input.switch 11 | (0.387518, 0.4051) observed |
| `switch.matrix-13` | pinmame.input.switch 13 | (0.240273, 0.615178) observed |
| `switch.matrix-14` | pinmame.input.switch 14 | (0.35877, 0.117821) observed |
| `switch.matrix-15` | pinmame.input.switch 15 | (0.464857, 0.11887) observed |
| `switch.matrix-16` | pinmame.input.switch 16 | (0.569148, 0.117875) observed |
| `switch.matrix-17` | pinmame.input.switch 17 | (0.249962, 0.093855) observed |
| `switch.matrix-18` | pinmame.input.switch 18 | (0.457857, 0.431134) observed |
| `switch.matrix-19` | pinmame.input.switch 19 | (0.785995, 0.473897) observed |
| `switch.matrix-20` | pinmame.input.switch 20 | (0.821647, 0.499482) observed |
| `switch.matrix-21` | pinmame.input.switch 21 | (0.853568, 0.524266) observed |
| `switch.matrix-22` | pinmame.input.switch 22 | (0.100934, 0.362653) observed |
| `switch.matrix-23` | pinmame.input.switch 23 | (0.100934, 0.391435) observed |
| `switch.matrix-24` | pinmame.input.switch 24 | (0.100934, 0.419018) observed |
| `switch.matrix-25` | pinmame.input.switch 25 | (0.934135, 0.882011) observed |
| `switch.matrix-26` | pinmame.input.switch 26 | (0.917823, 0.556732) observed |
| `switch.matrix-27` | pinmame.input.switch 27 | (0.917879, 0.494608) observed |
| `switch.matrix-28` | pinmame.input.switch 28 | (0.918252, 0.434514) observed |
| `switch.matrix-29` | pinmame.input.switch 29 | (0.918036, 0.369183) observed |
| `switch.matrix-30` | pinmame.input.switch 30 | (0.918096, 0.302591) observed |
| `switch.matrix-31` | pinmame.input.switch 31 | (0.336056, 0.384388) observed |
| `switch.matrix-32` | pinmame.input.switch 32 | (0.858043, 0.084452) observed |
| `switch.matrix-34` | pinmame.input.switch 34 | (0.520821, 0.215877) observed |
| `switch.matrix-35` | pinmame.input.switch 35 | (0.824161, 0.391441) observed |
| `switch.matrix-36` | pinmame.input.switch 36 | (0.759216, 0.244177) observed |
| `switch.matrix-37` | pinmame.input.switch 37 | (0.776869, 0.175514) observed |
| `switch.matrix-53` | pinmame.input.switch 53 | (0.059466, 0.712081) observed |
| `switch.matrix-54` | pinmame.input.switch 54 | (0.846011, 0.714479) observed |
| `switch.matrix-55` | pinmame.input.switch 55 | (0.129494, 0.713998) observed |
| `switch.matrix-56` | pinmame.input.switch 56 | (0.774763, 0.716667) observed |
| `switch.matrix-57` | pinmame.input.switch 57 | (0.285631, 0.833281) observed |
| `switch.matrix-58` | pinmame.input.switch 58 | (0.619237, 0.833281) observed |
| `switch.matrix-59` | pinmame.input.switch 59 | (0.53576, 0.373161) observed |
| `switch.matrix-60` | pinmame.input.switch 60 | (0.307529, 0.210726) observed |
| `switch.matrix-61` | pinmame.input.switch 61 | (0.517833, 0.212099) observed |
| `switch.matrix-62` | pinmame.input.switch 62 | (0.409539, 0.298392) observed |
| `switch.matrix-63` | pinmame.input.switch 63 | (0.23244, 0.707691) observed |
| `switch.matrix-64` | pinmame.input.switch 64 | (0.675013, 0.708215) observed |
| `device.outhole-kicker` | pinmame.output.solenoid 1 | (0.489262, 0.962171) observed |
| `device.ball-shooter-kickbig` | pinmame.output.solenoid 3 | (0.913635, 0.575925) observed |
| `device.boomerang-kickbig` | pinmame.output.solenoid 4 | (0.240273, 0.615178) observed |
| `device.center-drop-target-reset` | pinmame.output.solenoid 5 | (0.457857, 0.431134) observed |
| `device.playfield-g-i-relay` | pinmame.output.solenoid 10 | (0.174459, 0.231353) observed; (0.125023, 0.152314) observed; (0.125956, 0.119934) observed; (0.244416, 0.026391) observed; (0.784485, 0.101495) observed; (0.81993, 0.181096) observed; (0.052268, 0.450931) observed; (0.064013, 0.604287) observed; (0.05973, 0.571007) observed; (0.05973, 0.548971) observed; (0.862837, 0.608334) observed; (0.721057, 0.677592) observed; (0.690276, 0.743251) observed; (0.183787, 0.676692) observed; (0.213635, 0.744151) observed; (0.215501, 0.808012) observed; (0.689344, 0.808461) observed; (0.310642, 0.118135) observed; (0.294786, 0.151864) observed; (0.413246, 0.118135) observed; (0.516783, 0.118585) observed; (0.622185, 0.118135) observed; (0.516983, 0.213576) observed; (0.308978, 0.211328) observed; (0.411381, 0.298474) observed; (0.858173, 0.356489) observed; (0.825527, 0.419) observed; (0.900148, 0.608784) observed; (0.812468, 0.160409) observed; (0.053783, 0.338387) observed; (0.457669, 0.341367) observed; (0.841561, 0.463487) observed |
| `device.ferris-wheel-motor-relay` | pinmame.output.solenoid 16 | (0.215118, 0.155829) observed |
| `device.left-jet-bumper` | pinmame.output.solenoid 17 | (0.307529, 0.210726) observed |
| `device.left-kicker-sling` | pinmame.output.solenoid 18 | (0.23244, 0.707691) observed |
| `device.right-jet-bumper` | pinmame.output.solenoid 19 | (0.517833, 0.212099) observed |
| `device.right-kicker-sling` | pinmame.output.solenoid 20 | (0.675013, 0.708215) observed |
| `device.bottom-jet-bumper` | pinmame.output.solenoid 21 | (0.409539, 0.298392) observed |
| `device.ducks-right-fireworks-flashers` | pinmame.output.solenoid 29 | (0.837526, 0.449972) observed |
| `device.ferris-wheel-flashers` | pinmame.output.solenoid 30 | (0.149172, 0.112964) observed |
| `device.cyclone-right-eye-flashers` | pinmame.output.solenoid 31 | (0.930623, 0.047783) observed |

## Projections

- solenoid 4: The Boomerang Kickbig coil sits under the kickbig its switch 13 reports; the placement is the sw13 kicker the script both reads and kicks.
- solenoid 5: The drop-target reset coil sits under the target; the placement is the Sw18 drop target it raises.
- solenoid 16: The Ferris wheel motor is part of the C-11900 Ferris Wheel/Motor Assembly; the placement is the position of the table's RedWheel primitive, the wheel its FWTimer rotates. Where the motor sits in the assembly is not printed.
- switch 57: The Switches list gives the left lane-change switch its own part (B-9951-1) apart from the cabinet Flipper Button (SW-10A-48), and the switch drawing's (PDF 40) balloon 57 points at the left flipper's pivot, so it is placed at the table's LeftFlipper pivot; where on the flipper assembly the switch is mounted is not printed. A consumer drives 84, not 57.
- switch 58: The Switches list gives the right lane-change switch its own part (B-9951) apart from the cabinet Flipper Button (SW-10A-48), and the switch drawing's (PDF 40) balloon 58 points at the right flipper's pivot, so it is placed at the table's RightFlipper pivot; where on the flipper assembly the switch is mounted is not printed. A consumer drives 82, not 58.

## Excluded table objects

- Insert-overlay lights lNa and lNa1 that vpmMapLights binds to the playfield lamps: no bulb mesh
- Lights L27-L32 and the COMET overlays on the back panel, and l57-l64 on the backglass, above or behind the playfield
- GILight32-34, GILight36-38 and the GI2 plastic lights: GI-collection lights that model no bulb
- Flasher domes Flasher27p and Flasher30p and their lights on the back panel at y < 0, off the playfield plane
- Lights F25, F25b, F26, F28, F29b-F29d, F30b-F30d, F31b, F32-F32c and Flash15a-c: no flasher dome or bulb

## Unplaced devices

| Device | Label |
| --- | --- |
| `device.spins-mystery-wheel-flasher` | Spins Mystery Wheel Flasher |
| `device.boomerang-flashers` | Boomerang Flashers |
| `device.left-ferris-wheel-jackpot-flashers` | Left Ferris Wheel + Jackpot Flashers |
| `device.right-ferris-wheel-teeth-flashers` | Right Ferris Wheel + Teeth Flashers |
| `device.top-middle-left-eye-flashers` | Top Middle + Left Eye Flashers |
| `device.cats-lower-fireworks-flashers` | Cats + Lower Fireworks Flashers |
| `device.spook-house-left-fireworks-flashers` | Spook House + Left Fireworks Flashers |
| `lamp.matrix-1` | HOLD |
| `lamp.matrix-2` | BONUS |
| `lamp.matrix-3` | DOUBLE |
| `lamp.matrix-4` | SCORES |
| `lamp.matrix-5` | CYCLONE 50K |
| `lamp.matrix-6` | CYCLONE 100K |
| `lamp.matrix-7` | CYCLONE Gate Bonus |
| `lamp.matrix-8` | RIDE THE COMET (on ramp) |
| `lamp.matrix-9` | W/L SCORE FERRIS WHEEL BONUS |
| `lamp.matrix-10` | ADV. "X" |
| `lamp.matrix-11` | Balloon 25K (Ducks) |
| `lamp.matrix-12` | Balloon 50K (Ducks) |
| `lamp.matrix-13` | Balloon LITES EX. BALL (Ducks) |
| `lamp.matrix-14` | 1 (Gate Lane) |
| `lamp.matrix-15` | 2 (Gate Lane) |
| `lamp.matrix-16` | 3 (Gate Lane) |
| `lamp.matrix-17` | RIDE AGAIN |
| `lamp.matrix-18` | SPINS MYSTERY WHEEL |
| `lamp.matrix-19` | Ducks (top) |
| `lamp.matrix-20` | Ducks (mid) |
| `lamp.matrix-21` | Ducks (bottom) |
| `lamp.matrix-22` | Ball Toss (top) |
| `lamp.matrix-23` | Ball Toss (mid) |
| `lamp.matrix-24` | Ball Toss (bottom) |
| `lamp.matrix-25` | EXTRA BALL Left Outlane |
| `lamp.matrix-26` | EXTRA BALL Right Outlane |
| `lamp.matrix-27` | COMET 20K |
| `lamp.matrix-28` | COMET 40K |
| `lamp.matrix-29` | COMET 60K |
| `lamp.matrix-30` | COMET 80K |
| `lamp.matrix-31` | COMET 100K |
| `lamp.matrix-32` | COMET 1 Million |
| `lamp.matrix-49` | 2X |
| `lamp.matrix-50` | 7X |
| `lamp.matrix-51` | 6X |
| `lamp.matrix-52` | 5X |
| `lamp.matrix-53` | 4X |
| `lamp.matrix-54` | 3X |
