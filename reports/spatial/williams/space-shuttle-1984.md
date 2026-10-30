# Space Shuttle (1984) spatial evidence

**Decision: partial.** Missing: spatial_placement, unresolved_conflicts.

x=0 left, x=1 right; y=0 rear/backglass, y=1 apron; normalized VPX/player view.

Geometry seed `tools/seeds/williams/space-shuttle-1984-geometry.json` SHA-256 `1813b46903860ec20697a31dbac6715788b1db632165191f26cb6b06db80e47c`.

## Blockers

- No factory drawing callout check has been run against the switch (PDF 19), solenoid (PDF 4) and lamp (PDF 20) location drawings, so every table placement stays observed rather than validated.
- Solenoid 14 (insert flash lamps) has no placement: its physical location is the open conflict conflict.insert-flash-lamps-location.
- Switch 45 (long ramp lower switch) has no placement: the switch-location drawing puts it beside the spinner at the ramp entrance, in front of switch 32, while the retained table's sw45 trigger sits further up the ramp behind sw32. Measuring balloon 45 on the drawing, or a table object at that spot, would place it.
- Switch 49 (playfield tilt) has no placement: no drawing balloon or table object locates the mechanism.

## Placed devices

| Device | Binding | Placements |
| --- | --- | --- |
| `switch.outhole` | pinmame.input.switch 9 | (0.475465, 0.977126) observed |
| `switch.ball-ramp-top-trough` | pinmame.input.switch 10 | (0.69655, 0.912425) observed |
| `switch.ball-ramp-middle-trough` | pinmame.input.switch 11 | (0.768382, 0.891109) observed |
| `switch.ball-ramp-lower-trough-release-position` | pinmame.input.switch 12 | (0.838225, 0.870575) observed |
| `switch.right-outlane` | pinmame.input.switch 13 | (0.849959, 0.679679) observed |
| `switch.left-flipper-return-lane` | pinmame.input.switch 14 | (0.131726, 0.709712) observed |
| `switch.right-flipper-return-lane` | pinmame.input.switch 15 | (0.776154, 0.680488) observed |
| `switch.left-eject-hole` | pinmame.input.switch 16 | (0.089215, 0.404345) observed |
| `switch.shuttle-target-s` | pinmame.input.switch 17 | (0.194043, 0.503841) observed |
| `switch.shuttle-target-h` | pinmame.input.switch 18 | (0.215151, 0.475961) observed |
| `switch.shuttle-target-u` | pinmame.input.switch 19 | (0.236591, 0.447266) observed |
| `switch.shuttle-t-drop-target` | pinmame.input.switch 20 | (0.45227, 0.356061) observed |
| `switch.shuttle-target-t` | pinmame.input.switch 21 | (0.753599, 0.403499) observed |
| `switch.shuttle-target-l` | pinmame.input.switch 22 | (0.770348, 0.432487) observed |
| `switch.shuttle-target-e` | pinmame.input.switch 23 | (0.786603, 0.461804) observed |
| `switch.right-eject-hole` | pinmame.input.switch 24 | (0.847034, 0.384878) observed |
| `switch.left-jet-bumper` | pinmame.input.switch 25 | (0.117429, 0.21693) observed |
| `switch.right-jet-bumper` | pinmame.input.switch 26 | (0.350303, 0.221857) observed |
| `switch.lower-jet-bumper` | pinmame.input.switch 27 | (0.222489, 0.304291) observed |
| `switch.left-outlane` | pinmame.input.switch 28 | (0.058272, 0.709862) observed |
| `switch.top-lane-u` | pinmame.input.switch 29 | (0.15888, 0.126538) observed |
| `switch.top-lane-s` | pinmame.input.switch 30 | (0.26372, 0.126805) observed |
| `switch.top-lane-a` | pinmame.input.switch 31 | (0.368752, 0.126877) observed |
| `switch.long-ramp-upper-switch` | pinmame.input.switch 32 | (0.94237, 0.137107) observed |
| `switch.left-drop-target` | pinmame.input.switch 33 | (0.552656, 0.289152) observed |
| `switch.center-drop-target` | pinmame.input.switch 34 | (0.564957, 0.259782) observed |
| `switch.right-drop-target` | pinmame.input.switch 35 | (0.579608, 0.230789) observed |
| `switch.ball-shooter-lane` | pinmame.input.switch 36 | (0.938309, 0.87763) observed |
| `switch.spinner` | pinmame.input.switch 37 | (0.640007, 0.173211) observed |
| `switch.ramp-bull-s-eye-target` | pinmame.input.switch 38 | (0.75536, 0.114485) observed |
| `switch.left-kicker-slingshot` | pinmame.input.switch 39 | (0.23112, 0.707553) observed |
| `switch.right-kicker-slingshot` | pinmame.input.switch 40 | (0.682962, 0.705276) observed |
| `switch.lane-change-right-flipper` | pinmame.input.switch 41 | (0.620983, 0.838244) observed |
| `switch.bottom-left-standup` | pinmame.input.switch 42 | (0.091311, 0.592296) observed |
| `switch.left-lower-standup` | pinmame.input.switch 43 | (0.159192, 0.367541) observed |
| `switch.left-upper-standup` | pinmame.input.switch 44 | (0.074709, 0.287836) observed |
| `switch.center-standup` | pinmame.input.switch 46 | (0.366667, 0.287652) observed |
| `switch.upper-right-standup` | pinmame.input.switch 47 | (0.675574, 0.270135) observed |
| `switch.lower-right-standup` | pinmame.input.switch 48 | (0.82281, 0.58346) observed |
| `coil.outhole-kicker` | pinmame.output.solenoid 1 | (0.475465, 0.977126) observed |
| `coil.ball-ramp-release` | pinmame.output.solenoid 2 | (0.838225, 0.870575) observed |
| `coil.left-eject-hole` | pinmame.output.solenoid 3 | (0.089215, 0.404345) observed |
| `coil.right-eject-hole` | pinmame.output.solenoid 4 | (0.847034, 0.384878) observed |
| `coil.t-drop-target-reset` | pinmame.output.solenoid 5 | (0.45227, 0.356061) observed |
| `coil.three-bank-drop-target-reset` | pinmame.output.solenoid 6 | (0.564957, 0.259782) observed |
| `coil.up-post` | pinmame.output.solenoid 7 | (0.454768, 0.876399) observed |
| `coil.down-post` | pinmame.output.solenoid 8 | (0.454768, 0.876399) observed |
| `flasher.space-flash-lamps` | pinmame.output.solenoid 9 | (0.339048, 0.53567) observed |
| `flasher.shuttle-flash-lamps` | pinmame.output.solenoid 10 | (0.569909, 0.53567) observed |
| `coil.outlane-gate` | pinmame.output.solenoid 13 | (0.812615, 0.735212) observed |
| `coil.left-kicker` | pinmame.output.solenoid 17 | (0.23112, 0.707553) observed |
| `coil.right-kicker` | pinmame.output.solenoid 18 | (0.682962, 0.705276) observed |
| `coil.left-jet-bumper` | pinmame.output.solenoid 19 | (0.117429, 0.21693) observed |
| `coil.lower-jet-bumper` | pinmame.output.solenoid 20 | (0.222489, 0.304291) observed |
| `coil.right-jet-bumper` | pinmame.output.solenoid 21 | (0.350303, 0.221857) observed |
| `lamp.up-post` | pinmame.output.lamp 7 | (0.455049, 0.876704) observed |
| `lamp.release-multi-ball` | pinmame.output.lamp 8 | (0.452756, 0.333727) observed |
| `lamp.bonus-multiplier-2x` | pinmame.output.lamp 9 | (0.304464, 0.642442) observed |
| `lamp.bonus-multiplier-3x` | pinmame.output.lamp 10 | (0.364729, 0.642333) observed |
| `lamp.bonus-multiplier-4x` | pinmame.output.lamp 11 | (0.42581, 0.642333) observed |
| `lamp.bonus-multiplier-5x` | pinmame.output.lamp 12 | (0.485855, 0.641585) observed |
| `lamp.bonus-multiplier-6x` | pinmame.output.lamp 13 | (0.548488, 0.642583) observed |
| `lamp.bonus-multiplier-7x` | pinmame.output.lamp 14 | (0.60905, 0.642583) observed |
| `lamp.flipper-return-lanes` | pinmame.output.lamp 15 | (0.158913, 0.636222) observed; (0.747908, 0.636125) observed |
| `lamp.left-lock` | pinmame.output.lamp 16 | (0.117345, 0.530399) observed |
| `lamp.shuttle-s` | pinmame.output.lamp 17 | (0.264581, 0.517534) observed |
| `lamp.shuttle-h` | pinmame.output.lamp 18 | (0.285586, 0.48871) observed |
| `lamp.shuttle-u` | pinmame.output.lamp 19 | (0.307237, 0.461132) observed |
| `lamp.shuttle-t-drop-target` | pinmame.output.lamp 20 | (0.440639, 0.385216) observed |
| `lamp.shuttle-t` | pinmame.output.lamp 21 | (0.684087, 0.414954) observed |
| `lamp.shuttle-l` | pinmame.output.lamp 22 | (0.701639, 0.444427) observed |
| `lamp.shuttle-e` | pinmame.output.lamp 23 | (0.716164, 0.47317) observed |
| `lamp.right-lock` | pinmame.output.lamp 24 | (0.795845, 0.530335) observed |
| `lamp.left-jet-bumper` | pinmame.output.lamp 25 | (0.118154, 0.216105) observed |
| `lamp.right-jet-bumper` | pinmame.output.lamp 26 | (0.351143, 0.220902) observed |
| `lamp.bottom-jet-bumper` | pinmame.output.lamp 27 | (0.221797, 0.303853) observed |
| `lamp.gate-open` | pinmame.output.lamp 28 | (0.791773, 0.617) observed |
| `lamp.top-lane-u` | pinmame.output.lamp 29 | (0.159734, 0.062318) observed |
| `lamp.top-lane-s` | pinmame.output.lamp 30 | (0.265331, 0.06288) observed |
| `lamp.top-lane-a` | pinmame.output.lamp 31 | (0.370151, 0.062693) observed |
| `lamp.bonus-holdover` | pinmame.output.lamp 32 | (0.492222, 0.809939) observed |
| `lamp.spinner-1-000` | pinmame.output.lamp 33 | (0.638298, 0.18835) observed |
| `lamp.spinner-2-000` | pinmame.output.lamp 34 | (0.631857, 0.231054) observed |
| `lamp.spinner-4-000` | pinmame.output.lamp 35 | (0.623269, 0.271511) observed |
| `lamp.extra-ball-when-lit` | pinmame.output.lamp 36 | (0.677044, 0.37572) observed |
| `lamp.shoot-again-playfield` | pinmame.output.lamp 37 | (0.41421, 0.809878) observed |
| `lamp.outlane-shuttle-arrow` | pinmame.output.lamp 41 | (0.068048, 0.800256) observed; (0.838683, 0.799915) observed |
| `lamp.shuttle-20-000` | pinmame.output.lamp 42 | (0.27184, 0.601204) observed |
| `lamp.shuttle-50-000` | pinmame.output.lamp 43 | (0.332568, 0.600573) observed |
| `lamp.shuttle-100-000` | pinmame.output.lamp 44 | (0.392984, 0.601099) observed |
| `lamp.50-000-and-bonus-holdover` | pinmame.output.lamp 45 | (0.455309, 0.600573) observed |
| `lamp.100-000-and-outlanes` | pinmame.output.lamp 46 | (0.518334, 0.600783) observed |
| `lamp.extra-ball` | pinmame.output.lamp 47 | (0.577142, 0.600573) observed |
| `lamp.scores-special` | pinmame.output.lamp 48 | (0.63916, 0.600783) observed |
| `lamp.stop-score-x2-playfield` | pinmame.output.lamp 49 | (0.452758, 0.453679) observed |
| `lamp.bonus-1-000` | pinmame.output.lamp 50 | (0.393412, 0.779961) observed |
| `lamp.bonus-2-000` | pinmame.output.lamp 51 | (0.454953, 0.780139) observed |
| `lamp.bonus-3-000` | pinmame.output.lamp 52 | (0.517231, 0.780139) observed |
| `lamp.bonus-4-000` | pinmame.output.lamp 53 | (0.393412, 0.753132) observed |
| `lamp.bonus-5-000` | pinmame.output.lamp 54 | (0.456058, 0.753132) observed |
| `lamp.bonus-6-000` | pinmame.output.lamp 55 | (0.516494, 0.75331) observed |
| `lamp.bonus-7-000` | pinmame.output.lamp 56 | (0.393044, 0.725948) observed |
| `lamp.bonus-8-000` | pinmame.output.lamp 57 | (0.454953, 0.726126) observed |
| `lamp.bonus-9-000` | pinmame.output.lamp 58 | (0.517231, 0.726304) observed |
| `lamp.bonus-10-000` | pinmame.output.lamp 59 | (0.393044, 0.699653) observed |
| `lamp.bonus-20-000` | pinmame.output.lamp 60 | (0.454953, 0.69912) observed |
| `lamp.bonus-30-000` | pinmame.output.lamp 61 | (0.517231, 0.699653) observed |
| `lamp.bonus-40-000` | pinmame.output.lamp 62 | (0.393778, 0.673323) observed |
| `lamp.bonus-50-000` | pinmame.output.lamp 63 | (0.456427, 0.672469) observed |
| `lamp.bonus-60-000` | pinmame.output.lamp 64 | (0.516862, 0.672291) observed |

## Projections

- solenoid 1: Effect placed on the Drain kicker (outhole), not a measured coil centre.
- solenoid 2: Effect placed on the Slot1 kicker (ball-ramp exit), not a measured coil centre.
- solenoid 3: Effect placed on the sw16 kicker (left eject hole), not a measured coil centre.
- solenoid 4: Effect placed on the sw24 kicker (right eject hole), not a measured coil centre.
- solenoid 5: Effect placed on the "T" drop target (sw20 wall), not a measured reset-coil centre.
- solenoid 6: Effect placed on the centre drop target (sw34 wall), not a measured reset-coil centre.
- solenoid 7: Effect placed on the centre of the centerpost primitive's mesh world bounds (checked against the centerpostcollide wall), the post both post coils drive; not a measured coil centre.
- solenoid 8: Effect placed on the centre of the centerpost primitive's mesh world bounds, the post both post coils drive; not a measured coil centre.
- solenoid 9: Emitter placed on the centre of the pHotDogSol9 flash-dome mesh's world bounds, the table's left (space) flash-lamp dome; the solenoid location drawing carries no balloon for the flash lamps.
- solenoid 10: Emitter placed on the centre of the pHotDogSol10 flash-dome mesh's world bounds, the table's right (shuttle) flash-lamp dome; the solenoid location drawing carries no balloon for the flash lamps.
- solenoid 13: Effect placed on the bottomgate flipper pivot, the gate the retained script rotates from 13; not a measured coil centre.
- solenoid 17: Effect placed on the mean of the LeftSlingShot wall's drag points.
- solenoid 18: Effect placed on the mean of the RightSlingShot wall's drag points.
- solenoid 19: Effect placed on the sw25 jet-bumper centre (the left bumper).
- solenoid 20: Effect placed on the sw27 jet-bumper centre (the lower bumper).
- solenoid 21: Effect placed on the sw26 jet-bumper centre (the right bumper).
- switch 9: Placed on the Drain kicker, the table's outhole ball-collection object, not on the contact itself.
- switch 10: Placed on the Slot3 kicker, the table's top ball-ramp position.
- switch 11: Placed on the Slot2 kicker, the table's middle ball-ramp position.
- switch 12: Placed on the Slot1 kicker, the table's ball-ramp exit position.
- switch 16: Placed on the sw16 kicker, the table's left eject hole.
- switch 20: Placed on the mean of the sw20 drop-target wall's drag points.
- switch 24: Placed on the sw24 kicker, the table's right eject hole.
- switch 25: Placed on the sw25 jet-bumper centre (the left bumper), not on its skirt contact.
- switch 26: Placed on the sw26 jet-bumper centre (the right bumper), not on its skirt contact.
- switch 27: Placed on the sw27 jet-bumper centre (the lower bumper), not on its skirt contact.
- switch 33: Placed on the mean of the sw33 drop-target wall's drag points.
- switch 34: Placed on the mean of the sw34 drop-target wall's drag points.
- switch 35: Placed on the mean of the sw35 drop-target wall's drag points.
- switch 39: Placed on the mean of the LeftSlingShot wall's drag points, a projection onto the slingshot rather than its leaf contacts.
- switch 40: Placed on the mean of the RightSlingShot wall's drag points, a projection onto the slingshot rather than its leaf contacts.
- switch 41: Placed on the RightFlipper pivot, the part the switch-location drawing's balloon 41 points at; the switch itself is on the flipper mechanism.
- switch 42: Placed on the centre of the sw42 collidable sensor mesh's world bounds (primitive vertices times size plus position), the table's rebound/standup sensor.
- switch 43: Placed on the centre of the sw43 collidable sensor mesh's world bounds.
- switch 44: Placed on the centre of the sw44 collidable sensor mesh's world bounds.
- switch 46: Placed on the centre of the sw46 collidable sensor mesh's world bounds.
- switch 47: Placed on the centre of the sw47 collidable sensor mesh's world bounds.
- switch 48: Placed on the centre of the sw48 collidable sensor mesh's world bounds.

## Unplaced devices

| Device | Label |
| --- | --- |
| `switch.long-ramp-lower-switch` | Long Ramp Lower Switch |
| `switch.playfield-tilt` | Playfield Tilt |
| `flasher.insert-flash-lamps` | Insert Flash Lamps |
