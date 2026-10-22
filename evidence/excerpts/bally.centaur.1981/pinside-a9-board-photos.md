# Centaur — owner photographs of the A9 board and the top-lane sockets

Source: Pinside technical thread *Centaur Light Issue (solved)*,
`https://pinside.com/pinball/forum/topic/centaur-light-issue`, topic 303903, started by Pinsider
SJ23 in November 2021 about their own Bally Centaur, read on 2026-10-22. The photographs are the
poster's; they are retained outside the repository by file hash and are not redistributed here.
What follows is what the photographs and the posts show, written down by the curator.

## The thread

- Post #1: the top three playfield lights stay on; every other lamp tests.
- Post #3 (djblouw): those lights are controlled by the auxiliary lamp board on the back of the
  backbox light panel.
- Post #4 (SJ23): three photographs, `20211111_170212`, `20211111_170704` and `20211111_173348`.
- Post #23 (Rikoshay) names the transistors for the three stuck lamps as `Q6, Q1 & Q12`, which are
  the A9 SCRs of A9J2-7, A9J2-1 and A9J2-18 on the board sheet.
- Post #26 (djblouw): the auxiliary board also drives both slingshots, both pop bumpers and the
  chamber feature lights in the top left corner.
- Post #29 (Rikoshay): the solenoid expander relay under the playfield is driven by the Q11
  transistor on the solenoid driver board.
- Post #49 (Rikoshay) refers to "the pic in #4 of the 3 light sockets, the ones remaining on", which
  identifies the underside photograph below as the three top-lane sockets.
- Post #53: a replacement auxiliary lamp board fixed the stuck lamps.

## Photograph of the A9 board in the backbox

Pinside file `65f35c74d10ac19414aedc4fa70f52e5a89dd4b3.jpg` (1536 x 2048, SHA-256
`6ddd40f46dc512fc0415cc1455589b0d35efae5bc482ab6c628e5e8bb07ecb00` as retained), from post #4. The
board's silkscreen reads `AS 2518 43` and `P 2948 355`. Its 20-pin `J2`
header runs down the left edge with `20` printed at the top end and SCR `Q1` beside the bottom end,
and the harness is plugged onto it.

Wires leave the connector at eleven positions, counting from the `20` end:

| position | wire as it looks in the photograph | sheet code at that pin |
| ---: | --- | --- |
| 20 | gray with white | 95 Gry-Wht |
| 19 | blue with black | 82 Blk-Blu |
| 18 | blue with white | 25 Blu-Wht |
| 17 | gray with brown | 96 Gry-Brn |
| 12 | blue with orange | 27 Blu-Orn |
| 7 | white with green | 54 Wht-Grn |
| 6 | green with white | 45 Grn-Wht |
| 5 | brown | 60 Brn |
| 3 | brown with blue | 62 Brn-Blu |
| 2 | green | 40 Grn |
| 1 | green with yellow | 43 Grn-Yel |

Positions 4 (the key), 8, 9, 10, **11**, 13, 14, 15 and 16 have no wire: there is an unbroken gap in
the housing between the blue-orange wire at 12 and the white-green wire at 7. Position numbers are
counted at the connector's even pitch from its two printed ends, so a reading one position off is
possible in principle; the colours settle it, because each wire matches the code W-1207-11 draws at
that pin and none is out of place.

## Photograph of the top-lane sockets from below

Pinside file `826977b13515798c9ccd366cda9be25b8c63d669.jpg` (2048 x 1536, SHA-256
`629c564dd444053caf579c0d0e3813fea5f3084453069e9720d425596270ad5e` as retained), from post #4. The
playfield is raised; the two thumper-bumper coils are at the top of the frame and three rollover
switches with a lamp socket behind each run across the lower half. The middle socket's drive wire
is green with yellow, code 43, the TOP MIDDLE LANE circuit, which is what identifies the row. The
socket on the left of the frame is fed by a blue wire with a light tracer and the socket on the
right of the frame by a white wire with a darker tracer.

With a Bally playfield raised in its service position, leaning back against the backbox, the
underside faces the viewer with the front edge up and the left side still on the left, which would
put the blue-white circuit (A9J2-18, public 97) under the left lane and the white-green circuit
(A9J2-7, public 65) under the right lane. The photograph is dim and taken at an angle, so the colours
and the orientation are a reading, not a measurement; it is recorded as consistent with the ROM's
lane logic, not as the deciding evidence.
