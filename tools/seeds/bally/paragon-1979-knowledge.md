# Paragon (Bally 1979)

Coverage: **partial** - one requirement is open, `spatial_placement`: two switch placements do not pass the factory drawing's callout check (see *Spatial placement* below). Everything else is validated.

Bally game #1167-E, manufactured June 1979 (project date December 5, 1978), IPDB 1755, OPDB `GrXy3-ML0Ey`. Four players, Bally MPU AS-2518-35, 9,120 units, design by Greg Kmiec, art by Paul Faris. Paragon was Bally's first widebody production game: the retained table's playfield is 1257 x 1974 units, against about 953 for a standard-width Bally of the period.

## Sources and how they are weighed

- **ROM behaviour** (pinned LibPinMAME harness, `evidence/runtime/by35/paragon-1979-harness.json`) decides every public address and every runtime semantic: the solenoid test pairs each printed number with a public output, the switch test shows each closed address, and gameplay probes tie switches to coils and lamps.
- **The manual and schematics** (IPDB scans) decide construction, wiring, printed names and what is fitted: the solenoid and switch identification tables (PDF 21), Figure V (PDF 22), the feature, adjustment and parts pages, the A5 lamp driver schematic W-1182-15 and the plug-connector sheet W-1187-11, both drawn for Paragon.
- **The known-working table** (bord's v2.37 on a base by 32assassin, the script pinned in `vpxtable_scripts`) decides runtime bindings and coordinates. Its embedded script equals the pinned file apart from whitespace, the corpus's audio patch and one commented-out lamp binding.
- **Pinned PinMAME** (`97aa922b`) decides controller topology: `GEN_BY35`, `dispBy6`, `FLIP_SW(FLIP_L)`, `lampCol` 0, sound board `SNDBRD_BY50`.

There are no open conflicts.

## Solenoids: printed numbers are test order, not addresses

The manual's solenoid table numbers fifteen loads 01-15, and Figure V prints those same numbers in squares. They are the order of the ROM's solenoid test, not public addresses. Three presses of the self-test button start the test, which fires one output per second and shows its number on every player display; pairing each pulse with the number gives, for all four drivers identically:

| printed | load | public |
| ---: | --- | ---: |
| 01 | Outhole kicker | 7 |
| 02 | Knocker | 6 |
| 03 | Treasure chamber saucer | 8 |
| 04 | Paragon saucer | 10 |
| 05 | Golden cliffs saucer | 9 |
| 06 | Left slingshot | 14 |
| 07 | Right slingshot | 15 |
| 08 | Left thumper bumper | 11 |
| 09 | Right thumper bumper | 12 |
| 10 | Bottom thumper bumper | 1 |
| 11 | Center thumper bumper | 13 |
| 12 | Drop target (in line) | 2 |
| 13 | Drop target (the waterfall bank) | 17 |
| 14 | Coin lockout door | 18 |
| 15 | K1 relay (flipper enable) | 19 |

The known-working script binds 2, 6, 7, 8, 9, 10, 17 and 19 to the same loads, and gameplay agrees for every playfield coil: the slingshot switches fire 14 and 15, the bumpers 11, 12, 1 and 13, the saucers 8, 9 and 10, and completing the waterfall bank fires 17. Public 3, 4 and 5 and the fourth continuous output, 20, have no load: the table names fifteen, the test fires fifteen, and 20 asserts only in the power-on pulse of all four continuous outputs.

The waterfall reset (17) is a continuous output the ROM pulses. The in-line reset (2) is a momentary one.

## Switches

The printed switch numbers are public addresses: Bally numbers the five-column matrix sequentially, and the ROM's switch test shows every number from 01 to 40 when that address closes. Five presses reach that test (the fourth ends the cycling solenoid test). Paragon wires five columns; the MPU's playfield strobe connector A4J2 carries ST0-ST4 and the cabinet strobe connector A4J3 ST0-ST1, so 41-48 are unused. Column 2 (9-16) holds only door and cabinet switches, and A4J2's ST1 pin has no wire on the plug-connector sheet.

Switches the manual prints with no description (5, 12-15, 20, 21, 25) are unused; the switch test reads them, which proves only that the matrix position exists. Three addresses carry parallel contacts: 7 (panel, plumb bob and ball tilts), 27 (two 500-point rebounds) and 34 (the golden cliffs rollover, the top right rollover and the drop-target rebound); slam 16 has a door switch and a cabinet switch. There is no left outlane switch; the left lane is the Beast's Lair.

All switches are leaf assemblies "adjusted for a 1/16" gap in the open position", the tilts are explicitly "normally open", and the ROM reads every one active at public 1 on a matrix it reads uninverted, so every contact rests open.

The VPinMAME Bally library names public 2 `swBallRollTilt` and calls 11 and 10 coin 1 and coin 2. Those are Bally-wide defaults. On Paragon public 2 is in-line drop target C (the ROM lights 2X when it falls third), the ball tilt is a contact on 7, and the manual calls 10 Coin I (left) and 11 Coin II (middle).

## Flippers

Four flippers, AQ-25-500/34-4500 each: the two lower flippers, a small one on the left wall aimed at the Valley of Demons targets, and one on the right above the lower right flipper aimed at the waterfall targets. Each cabinet button fires both flippers of its side. The buttons are not matrix switches: the plug-connector sheet wires them to the solenoid driver (A3J2-1 R. FLIP SW., A3J2-2 L. FLIP SW.) and the coils to A3J1-8 and A3J1-9, switched through the K1 relay (public 19), which the ROM raises from game start to game over and drops on a tilt.

PinMAME models this with its generic flipper column: holding public 84 (left) or 82 (right) raises output 48 or 46 while 19 is up. It also raises 47 or 45, which the BY35 controller profile does not declare. The known-working script drives `LeftFlipper` and `LeftFlipper1` from 48 and `RightFlipper` and `RightFlipper1` from 46. The upper generic positions 81 and 83 do nothing.

IPDB records that an unknown number of machines shipped to Europe, reportedly every one sold in France, had only three flippers: the upper right flipper was not installed, a ball guide and a single post took its place, and a mini-post was added in the Beast's Lair opening. Kmiec attributes the change to foreign distributors who wanted one return lane on each side (the "Italian bottom") and to the cost saving. There is no separate ROM; the retained table models the variant with its `EuropeVariant` option. On those machines output 46 drives one coil.

## Lamps

Sixty main-board circuits, all used; `lampCol` is 0, so there is no auxiliary board. Public lamps 1-15, 17-31, 33-47 and 49-63 exist and 16, 32 and 48 are decoder holes. The address chain follows the board: `public = 16 * d + a + 1` from `by35_lampStrobe`, and the AS-2518-23 board takes each decoder output through its own SCR to a fixed connector pin. This record takes that board chain from the Kiss record (same board, derived from its own sheets) and reads the function on each pin from Paragon's own A5 schematic and plug-connector sheet, which agree pin for pin.

Three independent checks confirm the result:

- **The art.** Each of the 54 playfield lamps is a table light bound by name (`set Lights(n)=Ln`), and every light sits on an insert whose printed art matches the function the chain gives it: the ten bonus values and three super bonus values, both PARAGON rows letter by letter, the six golden cliff values, the drop-target values 10,000 to 25,000 and SPECIAL, the waterlane 5000, 10000 and Special, the 2x, 3x and 5x multipliers, SHOOT AGAIN, "Saucer Scores SPECIAL" and the 5X treasure insert. The two uncaptioned red Treasure Chamber inserts are named by the plastic beside them, which prints SPECIAL When LIT above EXTRA BALL When LIT. The four plain spinner inserts follow the sheet's numbering, 1 at the bottom to 4 at the top; a fifth insert below them is lit from the table's GI.
- **The ROM.** The spinner lights 14 (spinner 1), the third in-line target lights 6 (2X) and the fourth 22 (3X), and a tilt lights 61 (TILT).
- **The routing.** The eight playfield lamps on connector J2 (the four spinner lamps, the two waterlane values, the 10K and 20K golden cliff values) are exactly the eight pins the plug-connector sheet's Table B sends through the panel-to-back-cab plug to the playfield.

Six lamps are back box lamps with no playfield position: Shoot Again (11), Ball In Play (13), Match (27), High Score To Date (29), Game Over (45) and Tilt (61). The playfield shoot-again insert is a separate circuit, public 43 (SAME PLAYER S.A.). The Credit Indicator (59) is the apron's credit window.

Table defects that do not affect the machine: the pinned script binds `Lights(13)` to an object the table lacks (the retained table comments it out), its VR backglass reads lamp 45 for Match and 43 for Shoot Again, and its lights named `L11`, `L16`, `L27` and `L29` are GI rollover lamps, not those outputs.

There is no general illumination output; the playfield GI is always on.

## Mechanisms and rules a recreation needs

- **Outhole.** One ball, no trough. The ball drains into the outhole (switch 8); the ROM adds the bonus and the outhole kicker (7) serves it to the shooter alley. A credit with the ball in the outhole starts the game, fires both drop-target resets (2, 17) and the outhole kicker, and raises K1.
- **Valley of Demons in-line targets** (switches 4 at the front, 3, 2, 1 at the back, reset 2). The ball reaches each target only after the ones in front of it fall. Each target scores and advances the bonus (option S30: 3,000 and two advances, or 1,000 and one); the third awards 2X, the fourth 3X, and option S22 lets each spot a PARAGON letter. The bank does not reset when completed: the ROM resets it at the start of each ball, and the Treasure Chamber saucer resets it on its second entry in a ball.
- **Treasure Chamber saucer** (switch 31, kicker 8). At the end of a narrow upper-left lane; Kmiec added a clear plastic guide on the left and a metal deadening piece on the right after the whitewood's straight shot let the ball jump the saucer. It kicks the ball up towards the top of the playfield (the table uses 45 degrees). It always scores 5,000; the first entry in a ball awards 5X, the second the same-player-shoots-again lite and resets the in-line targets, and with all four targets down again it awards a special.
- **Golden Cliffs saucer** (switch 32, kicker 9). Scores the lit value 2,000-20,000, advances it, and advances the bonus at 20,000; remembered ball to ball. IPDB notes that each entry adds a note of The Ohio Players' "The Worm".
- **Paragon saucer** (switch 24, kicker 10). Spots the lit letter of the seven-letter arc in the centre PARAGON row and scores (option S23); S24 chooses between letters that scan and letters that advance one at a time. All seven lit the special lite; the next entry scores 25,000 and a special and resets the letters, which are remembered ball to ball.
- **Waterfall drop targets** (switches 17 front, 18, 19 rear, reset 17). 500 each; all three score the lit value (10,000, 15,000, 20,000, 25,000, special), advance the waterfall lane, and fire the reset. S31 limits the special to once.
- **Waterfall lane** (rollover 28). Advances the bonus and scores the lane value, which starts at 1,000 or 5,000 (S29) and steps through 5,000, 10,000 and special; reset every ball.
- **Bonus.** 1,000 to 49,000, advanced by the top and centre targets (30, 29), the top rollover (26), the spinner (33) and the features above; super bonus 20,000/30,000/40,000 lights are remembered.
- **Beast's Lair.** A passive ramp in the left lane ("ESCAPE PASSAGE" on its plastic) that returns a draining ball to the flippers; it has no switch or coil.
- **Thumper bumpers and slingshots.** Four bumpers (left 40/11, right 39/12, centre 38/13, bottom 37/1) and two slingshots (left 36/14, right 35/15); the ROM fires each from its own switch.

## Variants

Four drivers, one physical machine. `paragon` is the 1979 production ROM. `paragonb` (2004, Bally/Oliver) is a seven-digit display conversion (`dispBy7`), so it needs seven-digit display hardware and is recorded as compatible with display overrides. `paragonc` (free play) and `paragond` (free play, scoring divided by ten) run on the production hardware. All four run the same solenoid test, in the same order, and publish the same sixty lamps and sixteen solenoid addresses.

## Displays

Four six-digit player displays (controller indices 0-3, segment starts 2, 10, 18, 26), a two-digit credit display (index 4, start 35) and a two-digit match and ball-in-play display (index 5, start 38); the parts list counts five display driver boards. On `paragonb` the player displays are seven digits starting at 1, 9, 17 and 25.

## Spatial placement

Placements come from the retained table, normalized to its bounds (see `reports/spatial/bally/paragon-1979.md`). Lamp placements rest on the art identification above. Switch and coil placements were checked against Figure V with `tools/drawing_callouts.py`: an independent reader transcribed every number on the native render, the controls are the four bumper rings and the four flipper pivots, and a placement validates when its own callout lands within 0.07 normalized under both the control fit and the leave-one-out callout fit. Figure V puts solenoid numbers in squares and switch numbers in circles, so the two are checked as separate pages.

Placements the label check cannot decide are decided another way and say so on the device: each flipper pivot is itself a control, validated by its own leave-one-out offset (0.017 to 0.043); the two drop-target reset coils are documented projections of hidden assemblies; and the outhole switch, the bottom and centre bumper switches and the Treasure Chamber kicker share their table object with a placement whose own callout validates.

**The open blocker.** Two switch placements stay `observed`, both numbers printed beside their part without a leader: the upper contact of switch 27 (the drawn rebound rubber is where the table puts it, but the label sits 0.075 normalized away under the control fit) and the spinner, switch 33 (0.070 under the callout fit, just over the limit). No other retained drawing locates either; a second, independently built factory-layout table that binds both, or a registered photograph, would settle them.
