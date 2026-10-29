# Godzilla (Sega, 1998): spatial evidence

Status: **partial**. Positions are observed measurements, not validated physical
placement. Normalized playfield axes are x=0 left, x=1 right, y=0 rear and
y=1 apron. The retained table bounds are 952 by 2206.5 VPX units.

The factory drawings at manual PDF pages 7 and 9 provide 53 lamp measurements
and 22 flasher measurements. The primary curator read source pixels on the
1275×1650 native renders and independently selected five controls per page:
three bumper circles and two return-lane rollover slots. The affine fits are
recomputed from those controls and source pixels by `drawing_callouts.fit` and
`apply` using `tools/data/godzilla/spatial.json`. Maximum leave-one-out control
errors are approximately 0.0554 and 0.047 respectively. The seed identifies
points outside the control convex hull as extrapolated; every measurement remains
observed. Crops in the manual source are reading aids, not the measurement
input. In particular F2's two dome centers are pixels (741,234) and (806,188).

Thirty-six script-bound switch candidates and coil-effect projections come
from the retained table extraction. Their source objects, hashes and script
bindings are in the spatial seed. Trough switches 14 and 15 are projected to
the same release-kicker anchor, not modeled optos; bumper, slingshot, diverter, flipper and launch
coil positions are also effect projections. Positions do not claim a measured
coil center. Render lights, baked lightmaps and primitive origins are not
treated as physical sockets.

G.I. 0 has no placements: the table's 37 GI lights are lighting sources, not
socket evidence. The manual prints a nominal 36 playfield bulbs and two coin
door bulbs, with a production-variation note. Unplaced inputs are 1 and 8
(optional UK save-a-ball switches). Unplaced outputs
are 21–23 (optional UK post coils), lamp 40 (optional UK post lamp), and G.I. 0.
Lamp 8 is the cabinet launch-button lamp. These missing
GI, UK, and device locations, the single-source nature of observations, and
prototype compatibility prevent promotion.

Evidence: manual SHA-256
`fc71e6584b2a8ad715100f94b5d4d690b0cd3864cd9abd6746c2441ad4d6c1c5`;
VPW table SHA-256
`9b5d3a0fce830ec18d8423e42cddfc763646aa1f712bed954de0cc10175ca37d`;
script SHA-256
`95d77a6678cc735792091e582abd66983a709b28e9bde307679d10029598949b`.
The measurement renders are under `review-artifacts/sega.godzilla.1998/factory-renders/`;
the seed uses paths relative to that review-artifacts machine directory.

The complete `vpxtool git:v0.33.3` extraction manifest covers 2,017 files and
606,994,172 bytes. Its SHA-256 is
`6afdd84196c67308837e5311cea0f274f3f540c21b5eabdc1114412aa729913f`;
the curator recomputes the official manifest whenever the VPX root is configured.
Manual diagrams provide the lamp/flasher part measurements; the retained table
and script identify the calibration mechanism controls. All three source roles
are retained in the placement provenance. Ordinary contact objects provide
observed sensor positions, and the listed mechanism anchors provide disclosed
effect projections. No drawing point is validated against its own drawing.

The primary curator also checked IPDB's upper/middle/lower and underside photos
(machine 4443, pictures 63408-63411, Peter Blakemore) and all 25 Pinside gallery
images for this exact Sega game. The retained photo URLs, acquisition times and
hashes are in the external review folder. Their oblique or obscured views do not
establish every GI socket, so no extra socket coordinate is inferred from them.
