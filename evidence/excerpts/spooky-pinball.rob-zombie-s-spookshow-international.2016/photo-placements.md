# Photo placements: Rob Zombie's Spookshow International

## Photographs

- photo.rz-whitewood-ipdb-6416 (geometry): IPDB 6416 image 13, 'Whitewood Playfield', https://www.ipdb.org/images/6416/image-13.jpg, original file `image-13.jpg`, 988 x 1600 px, SHA-256 ade333f758cc5fe5f70fbe741a6cab3ab35851f1f1f9e45391d2a8cab32358ce. A near top-down photograph of a whitewood playfield fitted in a cabinet; every position is read on it after rectification.
- photo.rz-production-pinside (identification): Pinside gallery image 'RobZombie_Playfield (resized)', https://pinside.com/pinball/machine/rob-zombies-spookshow-international/gallery, original file `RobZombie_Playfield (resized).jpg`, 1367 x 2048 px, SHA-256 3d8c166d72be3bb7d659e28d11871f30b41ebac3eb9e73413b439c77dac2ecfb. A lit production playfield photographed from the front, mapped onto the whitewood by a 32-point homography (RMS 3.2 px); it names each insert and part and supplies the inserts the whitewood lacks.

## Frame

The whitewood photograph is corrected for barrel distortion (one radial term) and rectified onto a 952 x 2185 frame at playfield level. The left and right edges are measured where the bare wood meets the cabinet walls (the right edge is the shooter lane floor's outer edge). The main playfield's rear edge is hidden under the upper playfield and its front end under the apron, so those two lines come from a parallax estimate based on the wall tops, with the camera's foot placed at the front wall; that leaves a uniform uncertainty of about 45 px (2 percent of the length) in y, and the measured side edges are not quite parallel, so a position can be off by up to a few percent near the rear. Raised parts are not placed: parallax displaces them. Normalization: x / 952 and y / 2185 of the playfield-level frame, rounded to three decimals. The measurement files (rectified frame, boundary readings, homographies, overlays) are retained under the working root's review-artifacts/spooky-pinball.rob-zombie-s-spookshow-international.2016/photo-measurement-20261005/ (manifest SHA-256 95d543e45e3cc4f9bca5564a8171cfc93ff3f86282c2efd345d364d051034060).

## Placements

Only playfield-level parts read at medium or high confidence are placed, and flipper pivots and sling centres, which stand about an inch above the playfield.

| Device | Normalized | Frame px | Level | Confidence | Feature |
|---|---|---|---|---|---|
| switch 21 | 0.878, 0.719 | 836, 1572 | playfield | medium | right outlane rollover slot (outer slot right of the right lane-guide strip) |
| switch 22 | 0.797, 0.709 | 758, 1549 | playfield | medium | right inlane rollover slot (slot between the right lane-guide strip and the right lower sling) |
| switch 23 | 0.706, 0.695 | 672, 1519 | raised | medium | right lower slingshot, midpoint between its two posts (post screws at about (677,1470) and (614,1680)). Coordinates quoted in this description are in the first, wall-top rectification, not this frame. |
| switch 24 | 0.634, 0.827 | 604, 1808 | raised | medium | right flipper pivot (wide end of the right bat) |
| switch 25 | 0.262, 0.825 | 250, 1802 | raised | medium | left flipper pivot (wide end of the left bat) |
| switch 26 | 0.188, 0.691 | 179, 1511 | raised | medium | left lower slingshot, midpoint between its two posts (post screws at about (200,1482) and (264,1690)). Coordinates quoted in this description are in the first, wall-top rectification, not this frame. |
| switch 27 | 0.111, 0.706 | 106, 1542 | playfield | high | left inlane rollover slot (slot inside the left lane-guide strip) |
| switch 28 | 0.03, 0.715 | 28, 1562 | playfield | high | left outlane rollover slot (outer slot left of the left lane-guide strip) |
| switch 35 | 0.831, 0.195 | 791, 427 | playfield | medium | rollover slot in the lane floor under the wooden arch (inner orbit entry), above the Inner Right Arrow |
| switch 36 | 0.672, 0.252 | 640, 550 | playfield | high | centre of the blue base ring under the Captain Spaulding bucket (pop bumper) |
| switch 57 | 0.058, 0.567 | 55, 1239 | raised | medium | midpoint between the two screw posts of the red upper-left sling plastic (posts at (172,1329) and (92,1372)). Coordinates quoted in this description are in the first, wall-top rectification, not this frame. |
| solenoid 6 | 0.672, 0.252 | 640, 550 | playfield | high | centre of the blue base ring under the Captain Spaulding bucket (pop bumper) |
| solenoid 11 | 0.058, 0.567 | 55, 1239 | raised | medium | midpoint between the two screw posts of the red upper-left sling plastic (posts at (172,1329) and (92,1372)). Coordinates quoted in this description are in the first, wall-top rectification, not this frame. |
| solenoid 12 | 0.188, 0.691 | 179, 1511 | raised | medium | left lower slingshot centre (shared with switch 26) |
| solenoid 13 | 0.262, 0.825 | 250, 1802 | raised | medium | left flipper pivot |
| solenoid 14 | 0.262, 0.825 | 250, 1802 | raised | medium | left flipper pivot |
| solenoid 19 | 0.634, 0.827 | 604, 1808 | raised | medium | right flipper pivot |
| solenoid 20 | 0.634, 0.827 | 604, 1808 | raised | medium | right flipper pivot |
| solenoid 21 | 0.706, 0.695 | 672, 1519 | raised | medium | right lower slingshot centre (shared with switch 23) |
| lamp 11 | 0.448, 0.835 | 427, 1824 | playfield | high | round 'Rock Again' insert below the flippers' centreline (bottom centre) |
| lamp 12 | 0.414, 0.689 | 395, 1506 | playfield | medium | round 'Living Dead Girl' insert, lower pair in the main cluster (left of Murder Ride) |
| lamp 13 | 0.575, 0.647 | 547, 1414 | playfield | high | round 'Red Hot' insert, right of the cluster |
| lamp 14 | 0.451, 0.656 | 429, 1433 | playfield | high | wide 'Dragula' insert, bottom of the cluster |
| lamp 15 | 0.328, 0.645 | 312, 1410 | playfield | high | round 'House of 1000 Corpses' insert, left of the cluster |
| lamp 16 | 0.406, 0.613 | 386, 1340 | playfield | high | 'Super Beast' insert, lower-left of the square pair |
| lamp 17 | 0.499, 0.613 | 475, 1339 | playfield | high | 'Dead City Radio' insert, lower-right of the square pair |
| lamp 18 | 0.492, 0.69 | 468, 1509 | playfield | medium | round 'Murder Ride' insert, lower pair in the main cluster (right of Living Dead Girl) |
| lamp 21 | 0.31, 0.588 | 295, 1285 | playfield | high | square 'What' insert, left of the cluster |
| lamp 22 | 0.451, 0.569 | 430, 1244 | playfield | high | wide 'Demonoid Phenomenon' insert, top of the cluster |
| lamp 23 | 0.595, 0.588 | 567, 1284 | playfield | high | square 'American Witch' insert, right of the cluster |
| lamp 24 | 0.454, 0.521 | 432, 1138 | playfield | high | large round 'Hell Bound' insert above the cluster (whitewood hand label 'Wizard') |
| lamp 25 | 0.804, 0.535 | 765, 1169 | playfield | medium | tall 'Extra Ball' insert at the right lane, above the '3' insert |
| lamp 26 | 0.766, 0.562 | 729, 1229 | playfield | high | round '3' insert at the right lane, below Extra Ball |
| lamp 27 | 0.794, 0.629 | 756, 1375 | playfield | medium | small round insert right of the right guide wire, partly hidden (letter O of the C-H-O-P arc) |
| lamp 28 | 0.881, 0.659 | 838, 1441 | playfield | high | round 'P' insert, right-lower of the C-H-O-P arc |
| lamp 31 | 0.724, 0.425 | 689, 929 | playfield | high | 'Skill Shot 2' arrow insert, right of centre |
| lamp 32 | 0.74, 0.354 | 704, 774 | playfield | high | lower round insert of the three-circle column right of the pops ('Gein') |
| lamp 33 | 0.76, 0.324 | 724, 707 | playfield | high | middle round insert of the three-circle column ('Fish') |
| lamp 34 | 0.781, 0.294 | 744, 643 | playfield | high | upper round insert of the three-circle column ('Dr. Satan') |
| lamp 35 | 0.805, 0.257 | 766, 562 | playfield | medium | tall red arrow insert left of the Dr. Satan column (points at the inner orbit) |
| lamp 36 | 0.908, 0.27 | 865, 591 | playfield | medium | tall red arrow insert right of the inner arrow (points at the outer orbit) |
| lamp 37 | 0.885, 0.33 | 842, 722 | playfield | high | upper blue 'X' insert |
| lamp 38 | 0.904, 0.351 | 861, 766 | playfield | high | lower blue 'X' insert |
| lamp 41 | 0.031, 0.655 | 29, 1432 | playfield | high | round 'C' insert at the left outlane edge |
| lamp 42 | 0.118, 0.626 | 113, 1367 | playfield | high | round 'H' insert above C |
| lamp 43 | 0.27, 0.509 | 257, 1112 | playfield | high | 'Skill Shot 1' arrow insert, left of the Hell Bound ring |
| lamp 44 | 0.238, 0.432 | 226, 944 | playfield | high | round '1' insert below the boombox |
| lamp 45 | 0.108, 0.399 | 103, 872 | playfield | high | round 'Hurry Up' insert, lowest of the left-lane column |
| lamp 46 | 0.099, 0.368 | 95, 805 | playfield | high | round 'Video Mode' insert, middle of the left-lane column |
| lamp 47 | 0.084, 0.337 | 80, 736 | playfield | medium | round 'Mode Start' insert, top of the left-lane column |
| lamp 48 | 0.068, 0.299 | 64, 653 | playfield | medium | elongated outlined arrow insert at the left lane, above Mode Start |
| lamp 51 | 0.389, 0.338 | 370, 738 | playfield | high | 'Skill Shot 3' arrow insert, left of the Collect Jackpot arrow |
| lamp 52 | 0.34, 0.267 | 324, 584 | playfield | medium | blue '1' insert, lowest of the diagonal blue lock inserts |
| lamp 53 | 0.32, 0.238 | 304, 519 | playfield | medium | blue '2' insert, middle of the diagonal blue lock inserts |
| lamp 54 | 0.309, 0.209 | 294, 456 | playfield | medium | blue '3' insert, top of the diagonal blue lock inserts |
| lamp 56 | 0.364, 0.159 | 347, 347 | playfield | medium | wide 'Jackpot / Add-a-Ball' insert below the two red arrows (whitewood hand label LDG) |
| lamp 57 | 0.337, 0.126 | 321, 276 | playfield | medium | left of the two red arrow inserts under the Living Dead Girl targets |
| lamp 58 | 0.398, 0.13 | 379, 284 | playfield | medium | right of the two red arrow inserts under the Living Dead Girl targets |
| lamp 61 | 0.502, 0.317 | 478, 692 | playfield | high | 'Collect Jackpot' label insert below the ramp arrow |
| lamp 62 | 0.52, 0.288 | 495, 629 | playfield | high | tall red arrow insert pointing into the ramp mouth |
| lamp 63 | 0.458, 0.242 | 436, 528 | playfield | high | round '2' insert left of the ramp mouth |
| lamp 66 | 0.383, 0.406 | 364, 887 | playfield | medium | round '2X' insert, left of the 5X/10X row below the ramp |
| lamp 67 | 0.464, 0.401 | 442, 875 | playfield | medium | round '5X' insert, middle of the multiplier row |
| lamp 68 | 0.542, 0.407 | 516, 888 | playfield | medium | round '10X' insert, right of the multiplier row |

## Used devices without a placement

- switch 11: Shooter lane switch is outside the production crop and not visible on the whitewood.
- switch 12: Trough switch: under the apron, not visible in either photo.
- switch 13: Trough switch: under the apron, not visible in either photo.
- switch 14: Trough switch: under the apron, not visible in either photo.
- switch 15: Trough switch: under the apron, not visible in either photo.
- switch 16: Trough switch: under the apron, not visible in either photo.
- switch 17: Trough switch: under the apron, not visible in either photo.
- switch 18: Trough switch: under the apron, not visible in either photo.
- switch 31: EXTRA BALL: probably the target or rollover that feeds the Extra Ball insert at the right lane, but no switch part is visible on either photo.
- switch 32: RIGHT UPPER SLING: the right upper plastic (purple flasher area) was seen, but its sling posts cannot be told from the other screws, so no midpoint is claimed.
- switch 33: RIGHT RAIL LOWER: rail switch on the wire guide; not identifiable on either photo.
- switch 34: RIGHT RAIL UPPER: rail switch on the wire guide; not identifiable on either photo.
- switch 37: Not placed: left of the two thin rollover slots on the elevated upper playfield, beside the long steel guide; raised (elevated upper playfield), so parallax displaces it.
- switch 38: Not placed: right of the two thin rollover slots on the elevated upper playfield; raised (elevated upper playfield), so parallax displaces it.
- switch 41: UPPER FLIPPER EOS: the upper flipper is on the elevated upper playfield, hidden in production.
- switch 42: RIGHT OUTER ORBIT: no rollover or optic visible on either photo; the lane is behind the wire rails.
- switch 43: Not placed: ball hole (about 1.4 inch) with a white kicker plate, beside the ramp mouth; read only at low confidence.
- switch 44: SECRET PASSAGE: not visible on either photo.
- switch 45: LEFT INNER ORBIT: left lane switch is hidden under wire guides in production and not distinguishable on the whitewood.
- switch 46: Not placed: right of the two red standup targets in the pocket behind the Jackpot insert; raised (standup target face), so parallax displaces it.
- switch 47: Not placed: left of the two red standup targets in the pocket behind the Jackpot insert; raised (standup target face), so parallax displaces it.
- switch 48: DROP TARGET: no drop target could be identified. The red standups seen in production are the Living Dead Girl pair, the one at the ramp mouth (51) and the one under the boombox (56); the drop target could be either of the last two.
- switch 51: Not placed: red standup target with a screw at the ramp mouth, left of the ramp's dark entry block; raised (standup target face), so parallax displaces it.
- switch 52: RIGHT RATTLE SWITCH: loose-wire rattle switch in the right rails, not visible.
- switch 54: Not placed: centre of the blue dome of the lower-left pop (boombox stands over its lower edge); raised (blue pop dome / boombox base), so parallax displaces it.
- switch 55: Not placed: centre of the base ring under the robot (upper-left pop); read only at low confidence.
- switch 56: Not placed: red standup target plate in front of the boombox / lower-left pop; raised (standup target plate), so parallax displaces it.
- switch 58: LEFT ORBIT: left lane switch hidden under wire guides in production.
- switch 61: RAMP: switch inside the raised ramp channel (black ZOMBIE channel), not on the playfield plane.
- switch 95: Upper PF opto Spaulding: upper playfield, not visible in production.
- switch 96: Upper PF opto exit: upper playfield, not visible in production.
- solenoid 3: Upper flipper (high): elevated upper playfield, hidden in production.
- solenoid 4: Not placed: ball hole (about 1.4 inch) with a white kicker plate, beside the ramp mouth; read only at low confidence.
- solenoid 5: Not placed: black slot with a retracting post, below-right of the inner-orbit rollover; read only at low confidence.
- solenoid 7: Drop target coil: the drop target itself is not identified (see switch 48).
- solenoid 8: Upper flipper (low): elevated upper playfield, hidden in production.
- solenoid 9: Not placed: centre of the blue dome of the lower-left pop (boombox stands over its lower edge); raised (blue pop dome / boombox base), so parallax displaces it.
- solenoid 10: Not placed: centre of the base ring under the robot (upper-left pop); read only at low confidence.
- solenoid 17: Autolauncher: shooter lane is outside the production crop; not visible on the whitewood.
- solenoid 18: Ball trough: under the apron, not visible.
- solenoid 22: Right upper sling coil: see switch 32.
- solenoid 38: GI string: no emitter placement claimed (bottom playfield GI).
- solenoid 39: GI string: no emitter placement claimed (bottom playfield GI).
- solenoid 40: GI string: red GI lamps, no emitter placement claimed.
- solenoid 41: Not placed: purple flasher dome on the right upper plastic; raised (purple flasher dome), so parallax displaces it.
- solenoid 42: Red flasher: no red flasher dome identified on either photo.
- solenoid 43: GI string: white GI lamps, no emitter placement claimed.
- solenoid 51: Cabinet RGB (51): not on the playfield.
- solenoid 52: Cabinet RGB (52): not on the playfield.
- solenoid 53: Cabinet RGB (53): not on the playfield.
- solenoid 54: Cabinet RGB (54): not on the playfield.
- solenoid 55: Cabinet RGB (55): not on the playfield.
- solenoid 56: Cabinet RGB (56): not on the playfield.
- solenoid 57: Spaulding gate servo: on the upper playfield, not visible in production.
- solenoid 58: Not placed: robot figure on the left pop base; raised (robot figure (several inches)), so parallax displaces it.
- solenoid 62: Living Dead Girl RGB: the Living Dead Girl toy is outside the production crop and not on the whitewood.
- solenoid 63: Living Dead Girl RGB: the Living Dead Girl toy is outside the production crop and not on the whitewood.
- solenoid 64: Living Dead Girl RGB: the Living Dead Girl toy is outside the production crop and not on the whitewood.
- lamp 55: Inner Left Arrow: no matching arrow insert could be identified. The two red triangles at the Living Dead Girl pocket are the LDG arrows (57/58) and the left-lane arrow is the Left Orbit Arrow; the inner-left arrow is hidden by the robot / boombox toys in production and has no unclaimed whitewood hole.
- lamp 64: Chicken: lights the FRIED CHICKEN sign on the upper (elevated) area of the playfield, not an insert; the sign is outside the planar region and not visible on the whitewood.
- lamp 65: Gasoline: lights the GASOLINE sign on the upper (elevated) area, not an insert; not visible on the whitewood.
