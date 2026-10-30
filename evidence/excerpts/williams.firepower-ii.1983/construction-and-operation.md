# Construction and operation readings

Source: Firepower II Service Manual 16-521-101, July 1983, PDF SHA-256
`c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8`.
Method: manually read from native renders and paraphrased by the curator; visually checked. This is factual paraphrase except for the
complete location tables below. Line breaks are joined; punctuation is retained.

## PDF page 14 / printed 18, Figure 2 Lamp Locations: complete legend

The printed brace marks **1-5 Backbox Lamps**. Remaining used entries are drawn
on the playfield except 40, which is named but has no visible playfield callout.
The wiring-diagram reading and runtime disposition are recorded separately in
lamp-wiring.md; a name here does not establish a fitted bulb.

| Lamp No. | Function |
| --- | --- |
| 1 | Game Over |
| 2 | Match |
| 3 | Tilt |
| 4 | High Score |
| 5 | Shoot Again |
| 6 | Shoot Again |
| 7 | Double Score |
| 8 | Bonus Holdover |
| 9 | 1,000 Bonus |
| 10 | 2,000 Bonus |
| 11 | 3,000 Bonus |
| 12 | 4,000 Bonus |
| 13 | 5,000 Bonus |
| 14 | 6,000 Bonus |
| 15 | 7,000 Bonus |
| 16 | 8,000 Bonus |
| 17 | 9,000 Bonus |
| 18 | 10,000 Bonus |
| 19 | 20,000 Bonus |
| 20 | 40,000 Bonus |
| 21 | 60,000 Bonus |
| 22 | 80,000 Bonus |
| 23 | Bonus Holdover |
| 24 | Fire Power Special |
| 25 | "F" |
| 26 | "I" |
| 27 | "R" |
| 28 | "E" |
| 29 | "P" |
| 30 | "O" |
| 31 | "W" |
| 32 | "E" |
| 33 | "R" |
| 34 | "A" |
| 35 | "B" |
| 36 | "C" |
| 37 | "D" |
| 38 | Left Drain Special |
| 39 | Right Drain Special |
| 40 | Ball in Play |
| 41 | Lower Left Jet Bumper |
| 42 | Upper Right Jet Bumper |
| 43 | Upper Left Jet Bumper |
| 44 | Lower Right Jet Bumper |
| 45 | Left Flipper Return Lane |
| 46 | Right Flipper Return Lane |
| 47 | Mystery |
| 48 | Extra Ball |
| 49 | 2x |
| 50 | 3x |
| 51 | 5x |
| 52 | Eject Hole 10K |
| 53 | Eject Hole 20K |
| 54 | Eject Hole 50K |
| 55 | Eject Hole Lock Arrow |
| 56 | Release Target 50K |
| 57 | Release Target 100K |
| 58 | Release Target 150K |
| 59 | Release Arrow |
| 60 | Spinner |
| 61 | Not Used |
| 62 | Not Used |
| 63 | Not Used |
| 64 | Not Used |

## PDF page 15 / printed 19, Figure 5 Solenoid Locations and complete legend

The drawing shows four jet bumpers, two slings, a right eject hole, a bottom
outhole and a right front ball-ramp thrower. Flasher callout 4 is dashed at the
rear right. It does not count bulbs. The committed crop retains the rear area
at native resolution; no coordinate is inferred from a callout balloon.

| Sol. No. | Function |
| --- | --- |
| 1 | Outhole |
| 2 | Ball Ramp Thrower |
| 3 | Eject Hole |
| 4 | Orbit Complete Flash Lamps |
| 5 | Not Used |
| 6 | Not Used |
| 7 | Not Used |
| 8 | Not Used |
| 9 | Not Used |
| 10 | Not Used |
| 11 | General Illumination Relay |
| 12 | Not Used |
| 13 | Not Used |
| 14 | Not Used |
| 15 | Bell |
| 16 | Coin Lockout |
| 17 | Left Kicker |
| 18 | Right Kicker |
| 19 | Lower Left Jet Bumper |
| 20 | Upper Right Jet Bumper |
| 21 | Upper Left Jet Bumper |
| 22 | Lower Right Jet Bumper |

Solenoid Test: from Lamp Test, Auto-Up + Advance selects Test 02. The Match
display cycles 01-25, pulsing corresponding solenoids 01-24. The printed text
says “Flipper relationship is de-energized with subtest 25.” Manual-Down holds
one step; Advance selects the next; Auto-Up resumes the cycle.

## PDF page 7 / printed 10, Game Operation (factual paraphrase)

Two balls are used. A credit-button start serves a ball. Completing A-B-C-D
advances multipliers 2x, 3x and 5x; the right flipper operates lane change.
The orbit requires spinner-lane entry followed by the orbit exit gate. FIREPOWER
target groups F-I-R, E-P-O and W-E-R light individual jets and briefly light
the orbit award arrow; completing that orbit can store bonus for the next ball.
Successive completions of all FIREPOWER letters light one return lane/spinner,
the other return lane, ramp extra ball, FIREPOWER and an outlane special,
then award the special; later completions score 50,000. Slings alternate the
outlane specials. Ramp traversal awards its lit mystery/extra-ball value.

With multiball enabled, the eject hole awards its lit value, retains the ball,
and another ball is put into play. The release target awards its lit value,
advances that value, and begins two-ball play. During multiball other scoring
doubles; the eject hole instead scores 5,000 and immediately ejects. The end
of the final ball pays stored bonus and multipliers, then stored bonus again
without multipliers if holdover is lit. Credit lockout is de-energized at the
maximum credit setting; coins are rejected while it is de-energized.

This page does not specify measured coil pulse duration, jam-retry timing,
or an exact mechanical drawing of the ball storage path. Those remain gaps.
