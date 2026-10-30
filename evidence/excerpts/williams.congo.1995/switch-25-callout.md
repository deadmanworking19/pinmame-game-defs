# Congo -- Switch Locations drawing, callout 25 (printed 2-41, PDF page 110)

Read from a 300 dpi render of `Congo_OPS.pdf` page 110 (the playfield drawing on the right half of
the Switch Locations page); the image is the same region at the scan's native 200 dpi. The parts
list on the left half of the page prints item 25 as `A-17794 | Right Eject Rubber`
(`switch-locations.md`).

## What the drawing shows

Callout 25's leader leaves its circle at the right margin, runs left, passes over a screw on the
right-hand wall and continues up and to the left to the middle of a straight rubber band on the left
side of the right-eject saucer bracket. Callout 38's leader ends on the saucer bracket itself, and
callout 28's on the "You" standup target below it.

## Fit to the retained table

Coordinates are in pixels of the 300 dpi render (2550x3308). The drawing's outer frame lines lie at
x = 1482 and x = 2228.5 and y = 443 and y = 2144, so the frame-only fit is
`x = 1482 + 746.5 * nx`, `y = 443 + 1701 * ny` for normalized table coordinates (nx, ny). Five
other callouts whose switches already carry placements were read the same way, each leader followed
pixel by pixel from its circle to where the dark run ends:

| Callout | Leader end | Frame-fit prediction | Leader minus prediction |
| --- | --- | --- | --- |
| 28 "You" standup | (2019, 1308.4) | (2022.2, 1346.5) | (-3.2, -38.1) |
| 37 Mystery Eject | (1929, 1124.4) | (1943.3, 1165.3) | (-14.3, -40.9) |
| 56 Perimeter Defense | (1890, 1087) | (1898.0, 1118.2) | (-8.0, -31.2) |
| 64 Right Jet Bumper | (2150, 1006) | (2161.6, 1035.9) | (-11.6, -29.9) |
| 65 Bottom Jet Bumper | (2093, 1157.5) | (2103.9, 1195.0) | (-10.9, -37.5) |

The residual is a near-constant offset, mean (-9.6, -35.5) pixels. Leaving each control out in
turn and predicting it from the other four's mean offset misses by 0.0027-0.0109 normalized
(largest: callout 28, 8.0 and -3.2 pixels). Callout 25's leader, followed the same way along a slope
of 0.459, ends at (2030, 1246.2). Removing the mean offset puts it at (2039.6, 1281.7), which is
normalized (0.7469, 0.4931).

The retained table's Primitive `sw25` (mesh `Straight_B2.ob`, material `Rubber White`, collidable
with a hit event; position (684.0966, 1112.3384), size (80, 163, 100), RotZ 21.5) has the script
handler `Sub sw25_Hit:vpmTimer.PulseSw 25:End Sub 'Right Eject Rubber`. Its 56 transformed vertices,
from `vpxtool export obj --units vpu` (vpxtool v0.33.3) in table units, span x 689.7673-737.80115 and
y 1010.8485-1117.5948; the centre of that span is (713.784225, 1064.22165), normalized (0.740440,
0.492239). That is 0.0065 from the drawn callout (4.8 and 1.4 pixels), inside both the largest
leave-one-out miss and the 0.07 callout limit. The object position is the mesh's pivot at one end of
the band, not its centre. A second Primitive `sw1` carries the same mesh, position, size and
rotation with elasticity 0.8 and no script handler.
