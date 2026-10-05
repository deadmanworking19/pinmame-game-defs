# Photo placements: Domino's Spectacular Pinball Adventure

## Photographs

- photo.dominos-production-pinside (geometry): Pinside forum photo of a production Domino's playfield from above the apron (official thread, page 1), https://pinside.com/pinball/forum/topic/dominos-pinball-official-thread-translite-reveal, original file `pinside_forum_3006926_2610c70c6f84.jpg`, 1536 x 2048 px, SHA-256 95b41f58ff008686413e7fc857f42a3f697c50484568d9e4befd7150f187d607. A lit production playfield photographed from above the apron; every position is read on it after rectification, with close-ups from the same thread registered onto it to read insert labels.
- photo.dominos-pinside-011 (identification): Pinside forum photo, official thread page 1, https://pinside.com/pinball/forum/topic/dominos-pinball-official-thread-translite-reveal, original file `pinside_forum_4058380_371972c83c0e.jpg`, 1536 x 2048 px, SHA-256 39e820a0e5e10475e1d1e3087dd561cd4a974a15641296f17ad0df9cf46b0229. A close-up of the lower and middle playfield, registered onto the geometry photo (1618 matched features, median residual 0.78 px) to read the insert labels.
- photo.dominos-pinside-019 (identification): Pinside forum photo, official thread page 1, https://pinside.com/pinball/forum/topic/dominos-pinball-official-thread-translite-reveal, original file `pinside_forum_3006926_3f66673f9013.jpg`, 2048 x 1536 px, SHA-256 3809e4dc83272fcdc48f8b9857353a3f8706165e7d76a21f84d7c415ce2b58ea. The rear half of the playfield, mapped onto the frame to identify the rear and pit parts and to cross-check the side edges.
- photo.dominos-pinside-020 (frame): Pinside forum photo, official thread page 1, https://pinside.com/pinball/forum/topic/dominos-pinball-official-thread-translite-reveal, original file `pinside_forum_3006926_6fdd2f3dcc3b.jpg`, 1536 x 2048 px, SHA-256 12d62bc5372581cd6225d017488454ab56b697b943471936ae9b4c668248b96c. The whole cabinet including the apron, registered onto the geometry photo (454 matched features) to locate the apron's lower edge for the front estimate.
- photo.dominos-pinside-085 (identification): Pinside forum photo, official thread page 6, https://pinside.com/pinball/forum/topic/dominos-pinball-official-thread-translite-reveal, original file `pinside_forum_3208566_37191630a00b.jpg`, 2048 x 1536 px, SHA-256 47a73af62d1cdbc6f0b7360b0796e9b5709e1722896f9969240ff2119b54be34. A close-up of the rear lanes under the ramps, used to identify the lane inserts seen through the gaps.

## Frame

The photograph shows no lens distortion and is rectified onto a 952 x 2185 frame at playfield level: the left edge where the side wall meets the playfield, the right edge at the shooter lane floor's outer edge, the rear along the base of the rear structures (the true rear edge is hidden, about 30 px of uncertainty) and the front from a camera estimate fitted so that the apron's lower edge (registered from photo.dominos-pinside-020) and the round inserts come out right (the playfield's front end is never visible; about 45 px, 2 percent, of uncertainty, and the estimate assumes the frame's 46.5 inch length). The flipper pivots' midpoint sits 28 px left of the centre line, and photo.dominos-pinside-019 puts the side edges within about 2 percent, so a position can be off by a few percent. Raised parts are not placed: parallax displaces them. Normalization: x / 952 and y / 2185 of the playfield-level frame, rounded to three decimals. The measurement files (rectified frame, boundary readings, homographies, overlays) are retained under the working root's review-artifacts/spooky-pinball.domino-s-spectacular-pinball-adventure.2016/photo-measurement-20261005/ (manifest SHA-256 a68169d9134d07471b21fdbc84b58a504df2dfeb0a025c93c56543b78a3473f8).

## Placements

Only playfield-level parts read at medium or high confidence are placed, and flipper pivots and sling centres, which stand about an inch above the playfield.

| Device | Normalized | Frame px | Level | Confidence | Feature |
|---|---|---|---|---|---|
| switch 15 | 0.65, 0.827 | 619, 1806 | raised | medium | right flipper pivot (rounded bat end) |
| switch 16 | 0.696, 0.776 | 663, 1695 | raised | medium | right slingshot: midpoint between the two plastic screws (top post and lower-inner post) |
| switch 17 | 0.799, 0.72 | 761, 1574 | playfield | high | right inlane rollover slot, centre |
| switch 18 | 0.883, 0.727 | 841, 1589 | playfield | high | right outlane rollover slot, centre |
| switch 21 | 0.291, 0.826 | 277, 1805 | raised | medium | left flipper pivot (rounded bat end) |
| switch 22 | 0.246, 0.778 | 234, 1700 | raised | medium | left slingshot: midpoint between the two plastic screws (top post and lower-inner post) |
| switch 23 | 0.137, 0.728 | 130, 1591 | playfield | high | left inlane rollover slot, centre |
| switch 24 | 0.05, 0.732 | 48, 1599 | playfield | high | left outlane rollover slot, centre |
| switch 25 | 0.103, 0.52 | 98, 1136 | playfield | medium | left scoop hole (tan-rimmed black opening under the left wire rails), centre |
| switch 48 | 0.778, 0.27 | 741, 590 | playfield | medium | right scoop hole (tan-rimmed opening under the oven), centre |
| solenoid 9 | 0.103, 0.52 | 98, 1136 | playfield | medium | left scoop hole |
| solenoid 10 | 0.291, 0.826 | 277, 1805 | raised | medium | left flipper pivot |
| solenoid 11 | 0.246, 0.778 | 234, 1700 | raised | medium | left slingshot centre |
| solenoid 12 | 0.291, 0.826 | 277, 1805 | raised | medium | left flipper pivot |
| solenoid 13 | 0.778, 0.27 | 741, 590 | playfield | medium | right scoop hole |
| solenoid 19 | 0.65, 0.827 | 619, 1806 | raised | medium | right flipper pivot |
| solenoid 20 | 0.696, 0.776 | 663, 1695 | raised | medium | right slingshot centre |
| solenoid 21 | 0.65, 0.827 | 619, 1806 | raised | medium | right flipper pivot |
| lamp 11 | 0.047, 0.679 | 45, 1483 | playfield | high | round O insert in the flame at the left outlane |
| lamp 13 | 0.195, 0.59 | 186, 1289 | playfield | high | MYSTERY pizza circle (centre) |
| lamp 15 | 0.29, 0.644 | 276, 1407 | playfield | medium | GOLD FRANNY box |
| lamp 16 | 0.301, 0.665 | 287, 1453 | playfield | medium | FRANCHISEE box |
| lamp 17 | 0.321, 0.684 | 306, 1495 | playfield | medium | MANAGER box |
| lamp 18 | 0.33, 0.705 | 314, 1541 | playfield | medium | DRIVER box |
| lamp 21 | 0.477, 0.869 | 454, 1898 | playfield | high | ORDER AGAIN round insert |
| lamp 22 | 0.614, 0.703 | 585, 1537 | playfield | medium | MAKE THE PIZZA box (right stack, bottom) |
| lamp 23 | 0.614, 0.684 | 585, 1494 | playfield | medium | LOST TOPPING box (right stack) |
| lamp 24 | 0.614, 0.664 | 585, 1451 | playfield | medium | PIZZA DISPATCH box (right stack) |
| lamp 25 | 0.622, 0.642 | 592, 1402 | playfield | medium | MEGA WEEK box (right stack, top) |
| lamp 26 | 0.459, 0.596 | 437, 1303 | playfield | medium | HANDLE THE RUSH banner in the sunburst |
| lamp 27 | 0.792, 0.646 | 754, 1411 | playfield | high | round E insert in the flame at the right inlane |
| lamp 28 | 0.878, 0.675 | 836, 1474 | playfield | high | round N insert in the flame at the right outlane |
| lamp 31 | 0.112, 0.384 | 107, 840 | playfield | medium | round Domino-logo insert at the left orbit exit |
| lamp 32 | 0.101, 0.353 | 96, 771 | playfield | medium | teardrop insert with pizza-slice icon at the left orbit |
| lamp 33 | 0.176, 0.33 | 168, 721 | playfield | high | LOST TOPPING teardrop on the left orbit lane |
| lamp 34 | 0.297, 0.36 | 283, 787 | playfield | high | round 1 triangle insert |
| lamp 35 | 0.353, 0.349 | 336, 763 | playfield | high | round 2 triangle insert |
| lamp 36 | 0.407, 0.339 | 387, 740 | playfield | high | round 3 triangle insert |
| lamp 37 | 0.411, 0.398 | 391, 869 | playfield | high | round N insert under BATTLE THE NOID |
| lamp 41 | 0.434, 0.29 | 413, 634 | playfield | high | LOST TOPPING teardrop on the right Noid-orbit lane |
| lamp 42 | 0.522, 0.333 | 497, 727 | playfield | high | PIZZA DISPATCH teardrop on the left ramp |
| lamp 43 | 0.514, 0.361 | 489, 788 | playfield | high | EXTRA BALL rounded rectangle |
| lamp 44 | 0.503, 0.385 | 479, 842 | playfield | high | round Domino-logo insert on the left ramp lane |
| lamp 45 | 0.608, 0.395 | 579, 862 | playfield | high | round HANDLE THE RUSH insert on the oven ramp lane |
| lamp 46 | 0.622, 0.371 | 592, 811 | playfield | high | JACKPOT rounded rectangle on the oven ramp lane |
| lamp 47 | 0.638, 0.342 | 607, 747 | playfield | high | MEGA WEEK teardrop on the oven ramp lane |
| lamp 51 | 0.651, 0.439 | 620, 960 | playfield | medium | single dot on the red half of the big Domino logo |
| lamp 53 | 0.555, 0.471 | 528, 1029 | playfield | medium | left dot on the blue half of the Domino logo |
| lamp 54 | 0.657, 0.517 | 625, 1129 | playfield | medium | PIZZA WARS sign insert |
| lamp 55 | 0.667, 0.54 | 635, 1179 | playfield | medium | GLOBAL CONQUEST sign insert |
| lamp 56 | 0.682, 0.562 | 649, 1229 | playfield | medium | WORLD'S FASTEST PIZZA MAKER sign insert |
| lamp 61 | 0.758, 0.312 | 722, 681 | playfield | high | round blue-pizza insert below the oven (oven pizza scoop) |
| lamp 62 | 0.824, 0.318 | 784, 694 | playfield | high | teardrop with pizza-slice icon, right orbit lane |
| lamp 63 | 0.812, 0.363 | 773, 793 | playfield | high | ORDER PLACED rounded trapezoid |
| lamp 64 | 0.826, 0.384 | 786, 838 | playfield | high | PREPARE rounded trapezoid |
| lamp 65 | 0.834, 0.409 | 794, 894 | playfield | high | BAKE rounded trapezoid |
| lamp 66 | 0.848, 0.431 | 807, 941 | playfield | high | QUALITY CHECK rounded trapezoid |
| lamp 67 | 0.862, 0.453 | 821, 990 | playfield | high | DELIVERY rounded trapezoid |

## Used devices without a placement

- switch 11: Shooter lane lower end and its rollover are hidden under the apron and the right cabinet wall; only the upper lane floor is visible.
- switch 12: Trough ball 1 switch is under the apron/playfield, not visible.
- switch 13: Trough ball 2 switch is under the apron/playfield, not visible.
- switch 14: Trough ball 3 switch is under the apron/playfield, not visible.
- switch 26: Not placed: right-most face of the three-target Noid bank; raised (above the playfield), so parallax displaces it.
- switch 27: Not placed: middle face of the Noid bank; raised (above the playfield), so parallax displaces it.
- switch 28: Not placed: left-most face of the Noid bank; raised (above the playfield), so parallax displaces it.
- switch 31: Not placed: standup target Delivery: the red round pad in the right-side row of five alternating red/blue pads; raised (above the playfield), so parallax displaces it.
- switch 32: Not placed: standup target Quality Check: the blue round pad in the right-side row of five alternating red/blue pads; raised (above the playfield), so parallax displaces it.
- switch 33: Not placed: standup target Bake: the red round pad in the right-side row of five alternating red/blue pads; raised (above the playfield), so parallax displaces it.
- switch 34: Not placed: standup target Prepare: the blue round pad in the right-side row of five alternating red/blue pads; raised (above the playfield), so parallax displaces it.
- switch 35: Not placed: standup target Order Placed: the red round pad in the right-side row of five alternating red/blue pads; raised (above the playfield), so parallax displaces it.
- switch 36: Right orbit switch is mounted on the wire ramp rails; no photo shows a switch part.
- switch 37: Right Noid orbit switch is on the wire rails/under the ramps; not visible.
- switch 38: Left Noid orbit switch is on the wire rails/under the ramps; not visible.
- switch 41: Star lane rollover sits in the top lane group under the rear ramps; only the STAR insert is seen (lamp 58), not the switch slot.
- switch 42: 5 lane rollover sits in the top lane group under the rear ramps; only the 5 insert is seen (lamp 57), not the switch slot.
- switch 43: Not placed: right pop bumper dish (right of the two seen in pinside-domthread-019); raised (above the playfield), so parallax displaces it.
- switch 44: Lower pop bumper: only two pop dishes are visible (photo 019); the third pop is hidden under the ramps in every photo.
- switch 45: Not placed: left pop bumper dish (left of the two seen in pinside-domthread-019); raised (above the playfield), so parallax displaces it.
- switch 46: Left orbit switch is on the wire rails; not visible.
- switch 47: Spinner not identified in any photo (probably under or inside the ramps).
- switch 58: Noid Home switch is inside the Noid mechanism; not visible.
- switch 95: Cabinet opto; no photo shows an emitter or receiver. Which opto is the scoop opto and which the Noid-loop opto is unresolved.
- switch 96: Cabinet opto; no photo shows an emitter or receiver. Which opto is the scoop opto and which the Noid-loop opto is unresolved.
- solenoid 3: Lower pop bumper not visible in any photo (see switch 44).
- solenoid 4: Not placed: left pop bumper dish; raised (above the playfield), so parallax displaces it.
- solenoid 5: Not placed: right pop bumper dish; raised (above the playfield), so parallax displaces it.
- solenoid 6: Not placed: round steel disc with ring at the bottom of the black pit under the left ramp; read only at low confidence.
- solenoid 7: Up post between the orbits is not visible (down in all photos / under the ramps).
- solenoid 17: Autolauncher is at the bottom of the shooter lane, hidden under the apron.
- solenoid 18: Ball trough coil is under the apron/playfield.
- solenoid 41: The only dome seen is a red beacon on the oven structure at the upper right; nothing proves it is the Right Flasher (no flash photo, no label), so no position is claimed.
- solenoid 42: No dome is proven to be the Left Flasher; the one red beacon seen is at the right.
- solenoid 43: GI string, not a single point; under-playfield/backbox lighting.
- solenoid 51: Cabinet RGB LED channel, not a playfield device.
- solenoid 52: Cabinet RGB LED channel, not a playfield device.
- solenoid 53: Cabinet RGB LED channel, not a playfield device.
- solenoid 54: Cabinet RGB LED channel, not a playfield device.
- solenoid 55: Cabinet RGB LED channel, not a playfield device.
- solenoid 56: Cabinet RGB LED channel, not a playfield device.
- solenoid 57: Not placed: base of the Noid figure: yellow stand on the pizza disc; raised (above the playfield), so parallax displaces it.
- solenoid 58: Not placed: housing base of the Noid target bank; raised (above the playfield), so parallax displaces it.
- lamp 12: Not placed: flame insert of the left inlane (letter hidden under the left orbit wire loop); read only at low confidence.
- lamp 14: Not placed: START CAREER pizza-box face (centre of the skewed printed face; START ribbon and CAREER text); read only at low confidence.
- lamp 48: Pizza Tracker green side is a raised lit tube sign (PIZZA TRACKER) at the far right; raised and ambiguous between the tube segments, so not placed.
- lamp 52: Not placed: right dot on the blue half of the Domino logo; read only at low confidence.
- lamp 57: Not placed: insert labelled 5 in the top lane group; read only at low confidence.
- lamp 58: Not placed: insert labelled STAR in the top lane group; read only at low confidence.
- lamp 68: Pizza Tracker blue side, raised lit tube sign at the far right; not placed.
