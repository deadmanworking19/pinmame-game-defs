# Harlem Globetrotters On Tour (Bally 1979)

Coverage: **partial** - one requirement is open, `spatial_placement`: the retained table draws every playfield insert as an overlay with no bulb, so 53 lamps have no position (see *Spatial placement* below). Everything else is validated.

Bally game #1161-E, manufactured September 1979 (project date August 28, 1978), IPDB 1125, OPDB `GRnwQ-M9R5d`. Four players, 14,550 units, design by Greg Kmiec, art by Greg Freres. IPDB lists the MPU as AS-2518-35; the manual's parts list prints "MPU A4 AS-2962-10". A standard-width Bally of the period: the retained table's playfield is 952 x 1974 units.

## Sources and how they are weighed

- **ROM behaviour** (pinned LibPinMAME harness at PinMAME `46e1a01a`, `evidence/runtime/by35/harlem-globetrotters-on-tour-1979-harness.json`) decides every public address and every runtime semantic: the solenoid test pairs each printed number with a public output, the switch test shows each closed address, and gameplay and tilt probes tie switches to coils and lamps. An earlier run at `8371478a` (`evidence/runtime/by35/harlem-globetrotters-on-tour-hglbtrtr-switch-2-in-play.json`) showed that public 2 scores and awards as a member of the drop-target bank and does not tilt.
- **The manual** (the IPDB scan, 46 pages, schematics included) decides construction, wiring, printed names and what is fitted: the solenoid and switch identification tables (PDF 22), Figure V (PDF 23), the operation, feature, adjustment, self-test and parts pages, the A3 solenoid driver sheet W-1183-18c, the plug connectors sheet W-1187-14c, the A5 lamp driver sheet W-1182-18c and the playfield wiring sheet W-1192-14c, all drawn for this game.
- **The known-working table** (JPSalas's 2009 VPX version 1.0, the script pinned in `vpxtable_scripts` as `Harlem_Globetrotters_1.2.0.vbs`) decides runtime bindings and coordinates. Its embedded script is the same table before a later sound update; every switch write, solenoid callback, ball stack, the drop-target bank, the diverter, the lamp mapping and the game name are identical.
- **Pinned PinMAME** (`46e1a01a`, `src/wpc/by35games.c` lines 563-581) decides controller topology: `GEN_BY35`, `dispBy6` (`dispBy7` on the conversion), `FLIP_SW(FLIP_L)`, `lampCol` 0, sound board `SNDBRD_BY50`.

There are no open conflicts.

## Solenoids: printed numbers are test order, not addresses

The manual's solenoid table numbers thirteen loads 01-13, and Figure V prints those numbers in squares. They are the order of the ROM's solenoid test, not public addresses. Three presses of the self-test button start the test, which fires one output per second and shows its number on every player display; pairing each pulse with the number gives, identically on both drivers:

| printed | load | public | connector (wire) |
| ---: | --- | ---: | --- |
| 01 | Outhole kicker | 7 | A3J1-5 (95) |
| 02 | Knocker | 6 | A3J2-5 (85) |
| 03 | Globe saucer | 13 | A3J5-13 (80) |
| 04 | Target saucer | 14 | A3J5-14 (83) |
| 05 | Right slingshot | 12 | A3J5-15 (85) |
| 06 | Left slingshot | 11 | A3J5-9 (71) |
| 07 | Left thumper bumper | 9 | A3J5-12 (75) |
| 08 | Right thumper bumper | 8 | A3J5-10 (74) |
| 09 | Bottom thumper bumper | 10 | A3J5-11 (78) |
| 10 | Drop target reset | 15 | A3J5-8 (18) |
| 11 | Coin lockout door | 18 | A3J2-8 (36) |
| 12 | K1 relay (flipper enable) | 19 | on the A3 board |
| 13 | Right gate | 17 | A3J5-7 (81) |

The known-working script binds 6, 7, 13, 14, 15, 17 and 19 to the same loads, and gameplay agrees for every playfield coil: the slingshot switches fire 11 and 12, the bumpers 9, 8 and 10, the saucers 13 and 14, and the drain and the target saucer fire the drop-target reset 15. Public 1-5 have no load and never assert. Every playfield coil hangs from +43 VDC (wire 60, A2J1-6); all but the flippers take it through the 1 A slow-blow playfield fuse (wire 30 after the fuse).

## Continuous outputs and the free ball gate

The four continuous outputs come from the A3 sheet's CONT. 1-4 drivers, published at 17-20 in PIA order:

- **17, the right gate** (CONT. 2, PB4, Q17, A3J5-7). Energized means closed. The ROM raises it at game start and at each new ball, drops it when the lit dunk shot target (35) is hit, lighting GATE OPEN W/LIT (37), and raises it again when the ball goes down the right outlane (23), which puts 37 out. The known-working script swings the invisible `RightLaneGate` flipper open while 17 is off and closed while it is on. The manual says "A tilt closes the FREE BALL GATE"; the ROM instead drops 17 with the flipper relay on a tilt, so the gate rests in its unpowered, open position for the rest of the tilted ball, and the next ball raises 17 and starts with it closed. What the ROM does is what a recreation receives.
- **18, the coin lockout** (CONT. 4, PB5, Q19, A3J2-8). Held energized in attract and play. While the outhole bonus counts down, the ROM drops it and raises it five times, briefly except the last.
- **19, the K1 flipper-enable relay** (CONT. 1, PB6, Q15, on the A3 board, labelled FLIPPER ENABLE RLY.). Raised from game start to game over; a tilt drops it and the flipper buttons then do nothing.
- **20** (CONT. 3, PB7, Q13) has no load: the A3 sheet's dashed route takes it to A3J2-5, J5-3 and J3-9, each labelled N/U, the solenoid table names no load for it, and it asserts only in the power-on pulse that drives all four continuous outputs together. The plug-connector sheet prints A3J2-5 as KNOCKER (85), the knocker's own pin, which the solenoid test fires at public 6; the disagreement is about a drawing route, not the knocker.

## Switches

The printed switch numbers are public addresses: Bally numbers the five-column matrix sequentially, and the ROM's switch test shows every number from 01 to 40 when that address closes. Five presses reach that test (the fourth ends the cycling solenoid test). The game wires five columns: the playfield strobe connector A4J2 carries ST0-ST4 and the cabinet strobe connector A4J3 ST0-ST1, so 41-48 are unused, and the test shows nothing for them. Column 2 (9-16) holds only door and cabinet switches; the playfield sheet's ST1 column is empty, and A4J2-2 (ST1) has no wire number on the plug-connector sheet while the playfield sheet prints 93.

Switches the manual prints with no description (5, 12-15 and 18-21) are unused; the switch test reads them, which proves only that the matrix position exists. Two addresses carry parallel contacts: 7 (the panel tilt under the playfield, which the playfield sheet draws at ST0/I6 on A4J2, and the plumb bob and ball tilts in the cabinet) and 34 (the two 300-point rebounds, one in the upper left and one on the right below the dunk shot target). Slam 16 has a door switch and a cabinet switch. The playfield sheet draws a capacitor across the five side targets, the dunk shot target and the three thumper bumper switches.

All switches are leaf assemblies "adjusted for a 1/16" gap in the open position", the tilts are explicitly "normally open", and the ROM reads every one active at public 1 on a matrix it reads uninverted, so every contact rests open.

The VPinMAME Bally library names public 2 `swBallRollTilt` and calls 11 and 10 coin 1 and coin 2. Those are Bally-wide defaults. On this game public 2 is drop target C, the ball tilt is a contact on 7, and the manual calls 10 Coin I (left) and 11 Coin II (middle).

## Flippers

Three flippers, AQ-25-500/34-4500 each (the parts list counts "Flipper (3)"): the two lower flippers and a third, upper-left flipper below the left slingshot, above the lower left one. On the right a long guide rail runs where a matching flipper would be. The buttons are not matrix switches: the plug-connector sheet wires them to the solenoid driver (A3J2-1 R. FLIP. SW., wire 10; A3J2-2 L. FLIP. SW., wire 20), and each reaches its coil line (A3J1-9 R. FLIP. COIL, wire 70; A3J1-8 L. FLIP. COIL, wire 40) only through a K1 contact, so the flippers work only while the ROM holds 19.

The upper left flipper has no connector of its own. The playfield sheet returns its coil (wire 91) through the normally open contact "LEFT FLIPPER E.O.S." to A3J1-8, so it fires only once the lower left flipper reaches end of stroke and drops with it. The flipper coils take +43 VDC before the playfield fuse. The lower left and right flippers each carry an "N.C." contact across the upper winding; the upper left flipper's is unlabelled.

PinMAME models the buttons with its generic flipper column: holding public 84 (left) raises 47 and 48, and holding 82 (right) raises 45 and 46, while 19 is up. The two members of each pair rise and fall together; neither is a physical winding or end-of-stroke signal. The known-working script drives `LeftFlipper` and `LeftFlipper1` (the upper left) from 48 and `RightFlipper` from 46.

The column's other six positions are unused. In `core.h`, 81 and 83 are its lower-right and lower-left end-of-stroke bits, 85 and 87 the upper-right and upper-left end-of-stroke bits, and 86 and 88 the upper-right and upper-left button bits. The driver declares `FLIP_SW(FLIP_L)` only, so PinMAME's flipper mask holds just 82 and 84: it never sets the other six and nothing reads them. The game's end-of-stroke contacts live in the coil circuits, not on the MPU. The VPinMAME Bally library names 81 `swURFlip` and 83 `swULFlip` and writes them on the staged flipper keys, because `core.vbs` leaves the upper flipper solenoid numbers at their defaults on this table. Holding either in play changed nothing.

## Lamps

Sixty main-board circuits, all used; `lampCol` is 0, so there is no auxiliary board. Public lamps 1-15, 17-31, 33-47 and 49-63 exist and 16, 32 and 48 are decoder holes. The address chain follows the board: `public = 16 * d + a + 1` from `by35_lampStrobe`, and the AS-2518-23 board takes each decoder output through its own SCR to fixed connector pins. This record takes that board chain from the Kiss record (same board, derived from its own sheets) and reads the function on each pin from this game's lamp driver sheet W-1182-18c and plug-connector sheet W-1187-14c, which agree pin for pin; only the wording differs (the plug sheet abbreviates, for example "LT. SIDE SPIN. 200" for "LEFT SIDE SPINNER 200").

The ROM confirms the chain wherever gameplay reaches a lamp: the globe saucer lights CENTER "G" (15); the second, third and fourth in-line targets light 2X (12), 3X (28) and 5X (44); the target saucer with all four down lights SAUCER TARGET SPECIAL (56); the centre right spinner lights SPINNERS ② (20); players targets 1-4 put out SIDE TARGET ① to ④ (10, 57, 41, 25) and the fifth lights DUNK SHOT EXTRA BALL (58); the dunk shot target lights GATE OPEN W/LIT (37); a tilt lights TILT (61).

Five lamps are back box lamps with no playfield position: Ball In Play (13), Match (27), High Score To Date (29), Game Over (45) and Tilt (61). Public 43 drives two lines from one SCR: SHOOT AGAIN on A5J2-9 in the back box and S.P.S.A. on A5J3-22 on the playfield. The eight J2 lamps that are playfield inserts (14, 15, 30, 31, 46, 47, 62, 63) are exactly the eight pins the plug-connector sheet's Table "B" sends through the panel-to-back-cab plug, and the playfield sheet brackets the same eight. The credit indicator (59) is on J3 TO PLAYFIELD and the playfield sheet: the apron's credit window, where the table puts its light.

Seven SCRs also reach a pin the sheets print N/U (11 and A5J2-21, 12 and A5J2-13, 27 and A5J1-4, 28 and A5J2-12, 44 and A5J2-4, 59 and A5J2-5, 60 and A5J2-3); those branches carry no lamp on this game. Four lamps have two insert lights in the retained table (5, 20, 36 and 52, each a pair of spinner or spinner-value inserts); the wiring sheet draws one lamp symbol per line, including the N/U line, so it gives no bulb count, and this record does not assert one.

## General illumination

The playfield sheet draws one "GEN. ILLUM." lamp on the transformer supply printed "5.9 VAC." at A2J1-8 (wire 10), with A2J1-5 (70), A2J1-2 (40, "RET.") and A2J1-1 (50); no PinMAME output switches it, so the record has no G.I. device. The retained table has twenty G.I. bulb lights, `gi1`-`gi20`, outside the lamp range; the sheet gives no bulb count. The parts list's only lamp is the #44 bulb (E-125-22).

## Mechanisms and rules a recreation needs

- **Outhole.** One ball, no trough. The ball drains into the outhole between the flippers (switch 8); the ROM adds the bonus, counts it down with the coin lockout toggling, and the outhole kicker (7) serves the ball to the shooter alley, firing the drop-target reset (15) in the same step. A credit with the ball in the outhole starts the game, fires 7 and 15, and raises the gate (17) and K1 (19).
- **Free throw in-line drop targets** (switches 4 at the front, 3, 2, 1 at the back, reset 15). Four targets standing one behind the other on the right below the top saucers; the ball reaches each only after the ones in front of it fall. Each scores and advances the bonus and the Trotter fast break spinner value; the second awards 2X, the third 3X and the fourth 5X, and the targets spot the lit G-L-O-B-E letter. Option S8 sets when they reset: OFF resets them at each new ball and every time the ball enters the target saucer, ON only at each new ball. In the retained runs the ROM fired 15 at game start, at each new ball and when the target saucer was entered with all four down.
- **Target (free throw) saucer** (switch 32, kicker 14). Top right. The first entry in a ball scores 25,000 (TARGET SAUCER 25K, 53) and the second, with the targets down again, a special (SAUCER TARGET SPECIAL, 56).
- **Top basket "G-L-O-B-E" saucer** (switch 24, kicker 13). Top centre. Each entry scores 3,000, spots the lit G-L-O-B-E letter in the centre of the playfield and advances the bonus. All five letters spotted scores and flashes 50,000 and, by how many times the letters have been completed and option S32, lights the left outlane 25,000 lite, the G-L-O-B-E special lite or scores a special, then resets the letters, which are remembered ball to ball. S14 chooses between letters that scan and letters that step one at a time.
- **Players targets** (switches 26 at the bottom to 30 at the top, on the left wall). 300 each; knocking out all five lites scores 10,000 and advances the slam dunk target value (extra ball, special, 5,000) and relights them. S24 remembers them from ball to ball.
- **Slam dunk target** (switch 35, right side). Scores 300 or the lit value, and opens the free ball gate when DUNK SHOT OPENS GATE (21) is lit. S23 keeps its special lit for the rest of the ball.
- **Free ball gate** (right gate, 17, in the right outlane). Open, a ball entering the right outlane (23) scores 3,000 and is directed onto the right flipper, which closes the gate. See *Continuous outputs* for the polarity.
- **Spinners.** The left side spinner (17) on the left wall beside its four value lamps (100, 200, 1K and 2K: 6, 22, 38 and 54), and the two centre spinners, left (33) and right (25), at the two ends of the centre spinner bar below the bumpers, with the SPINNERS ① to ⑤ column (4, 20, 36, 52 and 5) and the advance-bonus lamps 51 (left) and 35 (right). A completed centre spinner sequence advances the bonus; S16 lights both spinners or only an alternating one. In play a closure of 25 lit SPINNERS ② (20).
- **Bonus.** 1,000 to 49,000; three steps for the right flipper return lane (22), one for each completed centre spinner sequence, plus the targets and saucers above; the 20,000, 30,000 and 40,000 super bonus lites may be remembered (S15).
- **Thumper bumpers and slingshots.** Three bumpers (left 40/9, right 39/8, bottom 38/10) and two slingshots (left 37/11, right 36/12); the ROM fires each from its own switch, in play and in the switch test. Lit bumpers score 1,000; all are lit on a three-ball game and alternate on a five-ball game. The bottom bumper's cap lamp is 26 and the left and right caps share 42.

## Variants

Two drivers, one physical machine. `hglbtrtr` is the 1979 production ROM set (game ROMs 750-07_1.716 and 750-08_2.716, U6 720-35_6.716, sound 729-51_3.123). `hglbtrtb` (catalogued 2004, Bally/Oliver; `driver.c` dates it 11/02) is a seven-digit display conversion: `dispBy7`, one 2732 game ROM `harl2732.u2` and a 2732 U6 `720-3532.u6b`, the same sound ROM. It needs seven-digit display hardware and is recorded as compatible with display overrides. At power-up it shows its revision, 090, on player 1. Both drivers run the same solenoid test in the same order, publish the same sixty lamps and fourteen solenoid addresses, show the same forty switches in the switch test, and fire the same solenoids for the same gameplay stimuli. The pinned script's option-switch form, titled for the seven-digit conversion, claims S21 selects 6- or 7-digit scoring and offers S22 as "no award" or "3 credits"; the manual gives S21 and S22 together as the high score to date award. Nothing retained settles whether the conversion reuses S21.

IPDB records insert colour differences: the flyer game's 2X-3X-5X-Special inserts are green, white, white and green; most production games are green, yellow, white and red; one factory game swaps the 5X and Special colours; and one example has white, not yellow, G-L-O-B-E inserts. IPDB also lists a German manual, which was not retained.

## Displays

Four six-digit player displays (controller indices 0-3, segment starts 2, 10, 18, 26), a two-digit credit display (index 4, start 35) and a two-digit match and ball-in-play display (index 5, start 38); the parts list counts five A1 display driver boards. On `hglbtrtb` the player displays are seven digits starting at 1, 9, 17 and 25.

## Spatial placement

Placements come from the retained table, normalized to its bounds (see `reports/spatial/bally/harlem-globetrotters-on-tour-1979.md`). Every switch and coil that has a playfield location is placed on the object the script binds and stays `observed`; the drop-target reset is a documented projection onto the centre of its four targets, a hidden assembly under the bank, and the right gate is the invisible `RightLaneGate` flipper the script swings. The two thumper bumper lamps (26 and 42) sit on the table's bumper cap bulbs, which are bulb lights with a bulb model, and are observed.

**The open blocker.** The other 53 lamps used on the playfield have no position. The retained table draws each insert with a Light that is not a bulb light and shows no bulb model (`is_bulb_light` and `show_bulb_mesh` both false), so under the bulb-picking rule it marks no socket, and nothing else retained puts one there. The manual has no lamp location drawing. Completing the record needs a table that models the insert bulbs, for example the VPW 1.0 table whose script is pinned in `vpx-standalone-scripts`, retained with its geometry and checked against the art, and then a callout check of the switch and coil placements against Figure V (`tools/drawing_callouts.py`), which the observed placements have not had.

## Legacy aliases

The record replaces a legacy import and keeps its numeric, zero-padded and named aliases (`s_*`, `c_game_on`) on the same bindings. Four of its bindings are not carried because PinMAME publishes nothing there on this machine: switch 134 (the VPW 1.0 script the import was extracted from pulses it for its second rebound contact, which the manual wires in parallel on 34) and solenoids 33, 35 and 37 with their `c_flipper_*` names (the import's guess at the framework flipper constants; the flippers are published at 45-48).
