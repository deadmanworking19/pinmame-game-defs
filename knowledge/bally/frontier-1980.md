# Frontier (Bally 1980)

Coverage: **partial** - two requirements are open. `input_semantics`: three option switches, S21, S22 and S29, are documented nowhere, so their function is unknown. `spatial_placement`: no lamp can be placed, because the only retained table models no lamp bulb (see *Spatial placement* below). Everything else is validated.

Bally game #1217 (the documentation prints the model number without the usual -E suffix), project date May 19, 1980, manufactured November 1980, IPDB 959, OPDB `GRwjq-MJwrd`. Four players, 1,850 units, design by George Christian, art by Greg Freres, Margaret Hudson and Kevin O'Connor. IPDB lists the MPU as AS-2518-35; the manual's parts list prints MPU A4 AS-2962-23 and sound module AS-3022-12, and pinned PinMAME emulates the game with its -51 sound board. Seven-digit player displays: the manual's display test counts "0000000 to 9999999".

## Sources and how they are weighed

- **ROM behaviour** (pinned LibPinMAME harness, `evidence/runtime/by35/frontier-1980-harness.json`) decides every public address and every runtime semantic: the solenoid test pairs each printed number with a public output, the switch test shows each closed address, and gameplay, tilt and gate probes tie switches to coils, lamps and scores. Every display reading the summary cites is pinned with its segment words in `tools/seeds/bally/frontier-1980-display-readings.json`.
- **The manual and schematics** (IPDB scans, fetched through the Internet Archive) decide construction, wiring, printed names and what is fitted: the solenoid and switch identification tables (PDF 21), Figure V (PDF 22), the feature, adjustment, self-test and parts pages, the eject-saucer drawing (PDF 37), the A5 lamp driver schematic W-1182-29c (schematics PDF 7), the plug-connector sheet W-1187-25c (PDF 8) and the playfield wiring sheet W-1192-25c (PDF 10), all drawn for Frontier.
- **The known-working table** (bord's v2.0, the script pinned in `vpxtable_scripts` with Thalamus's 2018 changes) decides runtime bindings and coordinates. Its embedded script matches the pinned file in every controller-facing line except `UseSolenoids` and the upper-flipper lines (see the script excerpt).
- **Pinned PinMAME** (`46e1a01a`) decides controller topology: `GEN_BY35`, `dispBy7`, `FLIP_SW(FLIP_L)`, `lampCol` 0, sound board `SNDBRD_BY51`, machine `by35_mBY35_51S`.

The harness never sets an option switch, so every run used the driver's input-port defaults (`src/wpc/by35.h`, `BY35_COMPORTS`): S20 and S21 on, every other switch off.

There are no open conflicts.

## Solenoids: printed numbers are test order, not addresses

The manual's solenoid table numbers thirteen loads 01-13, and Figure V prints those numbers in squares. They are the order of the ROM's solenoid test, not public addresses. Three presses of the self-test button start the test, which fires one output at a time and shows its number on every player display; pairing each pulse with the number gives, identically on `frontier` and `frontiea`:

| printed | load | A3 pin (wire) | part | public |
| ---: | --- | --- | --- | ---: |
| 01 | Outhole kicker | J1-5 (95) | AN-26-1200 | 7 |
| 02 | Knocker | J2-5 (85) | AR-26-1200 | 6 |
| 03 | 3 drop target reset | J5-12 (80) | NO-26-1900 | 9 |
| 04 | Saucer | J5-11 (78) | AO-27-1300 | 10 |
| 05 | Drop target reset (in-line) | J5-10 (85) | NO-26-1900 | 8 |
| 06 | Left thumper bumper | J5-9 (71) | AN-26-1200 | 11 |
| 07 | Right thumper bumper | J5-15 (74) | AN-26-1200 | 12 |
| 08 | Bottom thumper bumper | J5-13 (67) | AN-26-1200 | 13 |
| 09 | Left slingshot | J5-14 (83) | AO-26-1200 | 14 |
| 10 | Right slingshot | J5-8 (18) | AO-26-1200 | 15 |
| 11 | Gate | J5-7 (81) | GO-36-6900 | 17 |
| 12 | Coin lockout door | J2-8 (36) | FO-36-7000 | 18 |
| 13 | K1 relay (flipper enable) | - | - | 19 |

Public 17, 18 and 19 are continuous outputs (PIA port B bits 4-6, inverted); the gate is held open, not pulsed. Public 1-5 and the fourth continuous output, 20, have no load: the table names thirteen, the test fires thirteen, the A3 J1, J2 and J5 blocks name no further coil, and after the boot no run drives 1-5, while 20 appears only in the power-on reset pulse that drives 17-20 together. About 8.5 s after power-on the ROM kicks the saucer (10) and fires both drop-target resets (9, 8), energizes the coin lockout (18) and blips the relay (19).

The known-working script binds 6, 7, 8, 9, 10, 17 and 19 to the same loads; the bumpers and slingshots are kicked by the table itself. Its callbacks 1 and 2 play a slingshot sound on addresses the ROM never drives, a defect of the table that changes nothing.

## Switches

The printed switch numbers are public addresses: Bally numbers the matrix sequentially, and the ROM's switch test showed every number from 01 to 40 when that address closed. Five presses reach that test (the fourth ends the cycling solenoid test and starts the manual's sound test). The MPU's playfield strobe connector A4J2 carries ST0-ST4 and the cabinet connector A4J3 ST0-ST1, so 41-48 are unused. The manual prints 17-20, 26, 28 and 32 with no description and the wiring sheet names nothing there, so they are unused; the switch test reads them, which proves only that the matrix position exists.

Two addresses carry parallel contacts: 1 (four 30-point rebound rubbers) and 7 (panel, plumb bob and ball tilts, all three "normally open"); slam 16 has a door switch and a cabinet switch. The wiring sheet draws a .05 MFD capacitor across the grizzly target (24), the three stand-up targets (29, 30, 31) and the three thumper bumpers (38, 39, 40).

All switches are leaf assemblies "adjusted for a 1/16" gap in the open position", and the ROM's switch test registers each address when the host closes it on a matrix it reads uninverted, so every contact rests open.

The VPinMAME Bally library names public 2 `swBallRollTilt` and calls 11 and 10 coin 1 and coin 2. Those are Bally-wide defaults. On Frontier public 2 is the right outlane, the ball tilt is a contact on 7, and the manual calls 10 Coin I (left) and 11 Coin II (middle).

## Flippers

Two flippers, AQ-25-500/34-4500. The buttons are not matrix switches: the plug-connector sheet wires them to the solenoid driver (A3J2-1 R. FLIP. SW., wire 10; A3J2-2 L. FLIP SW., wire 20) and the coils to A3J1-8 (wire 40) and A3J1-9 (wire 70), switched through the K1 relay (public 19), which the ROM raises from game start to game over and drops on a tilt. The wiring sheet draws each coil as two windings with an end-of-stroke switch.

PinMAME models this with its generic flipper column: holding public 84 (left) or 82 (right) raises the synthetic pair 47 and 48 or 45 and 46 while 19 is up. `core_updateSw` raises and drops both members of a pair together, so 45 and 47 carry the same state as 46 and 48; the BY35 controller profile declares all four, and 45 and 47 are neither extra coils nor measured windings. The known-working script drives `LeftFlipper` from 48 and `RightFlipper` from 46 and calls `NoUpperLeftFlipper` and `NoUpperRightFlipper`; 81 and 83 are the lower-right and lower-left end-of-stroke bits of the column in core.h, which PinMAME does not simulate for this driver; the VPinMAME library calls them the upper flipper buttons and writes them from the flipper keys unless the table zeroes its upper flipper solenoid numbers, which the known-working script does and the retained table's embedded script does not. Nothing on this driver reads them, holding them in play changed no output, and nothing writes or reads 85-88, the rest of the column. In the tilt probe, the tilt dropped 19 and the held right flipper's pair 45 and 46 with it, and holding 82 afterwards raised nothing.

## Lamps

Sixty main-board circuits, all used; `lampCol` is 0, so there is no auxiliary board. Public lamps 1-15, 17-31, 33-47 and 49-63 exist and 16, 32 and 48 are decoder holes. The address chain follows the board: `public = 16 * d + a + 1` from `by35_lampStrobe`, and the AS-2518-23 board takes each decoder output through its own SCR to a fixed connector pin. This record takes that board chain from the Kiss record (same board, derived from its own sheets) and reads the function on each pin from Frontier's own A5 schematic and plug-connector sheet, which agree pin for pin; the wiring sheet's A5 J1 and J3 lists agree with both in every wire and pin.

The ROM confirms the chain wherever play can reach it:

- the in-line targets light 40 (SPINNER 1000) and 15 (GATE ARROW), then 57 (2X FRONTIER), then 58 (3X FRONTIER) with 54 and 56 (the grizzly-target lamps), and the grizzly target lights 52 (4X FRONTIER);
- each completion of the right bank steps 14 -> 30 -> 46 -> 62 (2X, 3X, 4X and SPECIAL DROP TARGET) and lights 31, 47, 63 (2X, 3X, 4X PREDATORS); the third lit an outlane special (60), which each slingshot then moved to the other side (44);
- the A, B and C lanes and the left, centre and right targets light the Den of Predators animals column by column (left 1-5, centre 17-21, right 33-37) and the thumper bumper lamps (10, 26, 42), and each completed row steps the Frontier bonus 7 -> 23 -> 39 -> 55 (10K, 20K, 30K, 40K);
- with lamp 12 lit, the right flipper feed lane (switch 3) scored 15,000 and the left (4) 500; with lamp 60 lit, the left outlane (5) awarded the special (knocker, credit lamp 59) and the right outlane (2) did not; a tilt lights 61.

Six lamps are back box lamps with no playfield position: Shoot Again (11), Ball In Play (13), Match (27), High Score To Date (29), Game Over (45) and Tilt (61). The playfield shoot-again insert is a separate circuit, public 43 (SAME PLAYER S.A.); the ROM lights both together. The Credit Indicator (59) is the apron's credit window. Eight playfield lamps (14, 15, 30, 31, 46, 47, 62, 63) leave the board on the back box connector J2 and reach the playfield through the plug-connector sheet's Table B.

The wiring sheet W-1192-25c labels those eight J2 pins CENTER "B", "O", "G", "L" and 10K-40K BONUS. No such feature exists on Frontier: the manual, the playfield and the other two sheets know none, and the ROM lights those pins' lamps as the lamp driver sheet names them. The labels are stale on that sheet; this record follows the other two sheets and the ROM. The same sheet prints wire 56 on the I1 switch return, where the plug-connector sheet prints 63. On A5J2-20 it prints wire 35, as the plug-connector sheet's Table B does, while that sheet's A5 J2 block and A1 insert lamp column print 98; the record follows the two tables that agree and gives lamp 30 drive wire 35. Both are wire-number disagreements that change no device.

Table defects that do not affect the machine: the retained table puts its light `L12` (bound to lamp 12) over the left feed lane and `L28` over the right, and `L44` over the left outlane and `L60` over the right, the opposite sides to the sheets and the ROM; its binding for 11 puts the back box SHOOT AGAIN on a playfield light `L11` above the apron, while the binding for 43 is commented out; its `L59` lies outside the playfield; and its option form mislabels S14's OFF setting (see the option switches below).

There is no general illumination output. The wiring sheet feeds the playfield G.I. from the transformer's 5.9 VAC on A2J1 ("GEN. ILLUM."), so it is lit whenever the game is powered.

## Mechanisms and rules a recreation needs

- **Outhole.** One ball, no trough. The ball drains into the outhole (switch 8); the ROM adds the bonus (the manual: 3,000 for each lit animal, plus the den 45,000 when it is lit, and with S16 on the Frontier bonus too) and the outhole kicker (7) serves it to the shooter alley. The drain also fires both drop-target resets (8, 9). A credit with the ball in the outhole starts the game, kicks the ball, fires both resets and the saucer kicker (10), and raises K1.
- **In-line drop targets and the grizzly target** (switches 23 front, 22, 21 rear, then the grizzly stand-up target 24 at the end of the upper-left orbit; reset 8). The ball reaches each in-line target only once the ones in front of it are down. The manual says any of them opens the gate; in play the first raised the gate output 17. The first lights the spinner for 1,000, the second the Frontier 2X multiplier, the third the Frontier 3X and the grizzly target's values, and the grizzly target the Frontier 4X and 30,000. The ROM does not reset the bank when the last target falls; it resets it at each drain and at game start. In play the targets scored 5,000, 10,000 and 15,000 and the grizzly target 30,000; the manual's feature page says the first target scores 1,000, and the runs had the undocumented S21 on, so whether an option switch sets that value is not known.
- **Gate and saucer** (gate 17, saucer switch 12, kicker 10, star rollover 25). The saucer sits at the lower end of the upper-right lane, the star rollover above it and the gate at the top, where the lane meets the arch. The eject-saucer drawing shows the saucer's kick running straight up the lane past the rollover and through the gate ("The ball should pass thru gate as shown"). The ROM holds output 17 on to open the gate: from an in-line or the grizzly target until the ball rolls over 25 or drains. Option S24 keeps an open gate for the next ball. On the production ROM, adding a player leaves an open gate open; that is the behaviour the `frontieg` Gate Fix changes. The saucer collects the Frontier bonus (in the probe it scored 10,000 with the 10K FRONTIER lamp lit) and the ROM kicks the ball out; the retained table kicks it with `sw12.Kick -10`. The known-working table models the gate as an invisible one-way gate it holds open while 17 is on.
- **Right-side drop targets** (switches 33 bottom, 34 middle, 35 top; reset 9). 500 each. Completing the bank fires the reset at once. The first completion lit the Den 2X (31), the second the Den 3X (47), the third the Den 4X (63) and the drop-target special (62); the manual says the fourth and every later one awards a replay. The 2X, 3X and 4X DROP TARGET lamps (14, 30, 46) show the next award. The outlane specials light with the second completion when S14 is on, and with the third when it is off; the probe, with S14 off, lit them on the third.
- **A-B-C lanes** (rollovers 13, 14, 15) and **stand-up targets** (29, 30, 31). Each lane and the target below it lights an animal in its column of the Den of Predators (A and the left target the left column, B and the centre target the centre column, C and the right target the right column) and lights its thumper bumper (left, bottom, right) for 1,000. Completing A-B-C the first time lights the A-B-C extra ball and a flipper feed lane for 15,000 (S30: both lanes, or one that alternates; the probe lit the right one, 12); the second time, same player shoots again and the A-B-C special; then a special each time. Each lane scored 5,000 and each target 500.
- **Den of Predators.** Fifteen animal lamps, a snake, hawk, lion, wolf and bear in each of three columns. Each completed horizontal row of three steps the Frontier bonus 10,000 -> 20,000 -> ... up to 60,000, or 110,000 with S23; with every animal lit, the predators special and the 45,000 den bonus light and the animals go out. Lit animals are recalled for the next ball; multipliers are not.
- **Outlanes and feed lanes** (switches 2 right out, 5 left out, 3 right feed, 4 left feed). The outlane specials light from the right bank (S8: both, or one that alternates; in the probe each slingshot moved the lit special to the other side). An outlane scored 1,000 and a lit one also its special; an unlit feed lane scored 500.
- **Spinner** (switch 27). 10 per closure, or 1,000 once the first in-line target has lit lamp 40.
- **Thumper bumpers and slingshots.** Three bumpers (left 40/11, right 39/12, bottom 38/13) scoring 100 unlit, and two slingshots (left 37/14, right 36/15) scoring 30; the ROM fires each from its own switch. The four 30-point rebound rubbers share switch 1.

## Variants

Three drivers, one physical machine, no hardware change between them.

- `frontier` is the 1980 production ROM set (U1 819-08_1.716, U2 819-07_2.716, U6 720-40_6.732, sound 819-09_4.716) and the reference for this definition.
- `frontieg` (2011, Bally / Scott, "Gate Fix") keeps U1 and U2 and replaces U6. PinMAME's source quotes the patch from rec.games.pinball: "U6 offset zero (checksum): change from AB to BB; U6 offset $289 change from FE 50 90 AD 00 to 86 EF BD 5E EB". Applied to the retained production U6, the patch gives exactly the SHA-1 PinMAME lists for `720-40_6g.732`. The new bytes load A with $EF and call $5EEB, which in the production U6 reads `43 9A 92 97 92 39` (COMA; ORAA $92; STAA $92; RTS): it sets bit 4 of $92, the port B data register of the U11 PIA, which PinMAME inverts into public 17, so the call turns the gate off. What the replaced call (`LDX $5090; JSR 0,X`) did is not analysed. The source comment says the hack "shuts the gate regardless of status when you start a game/add a player". The authorized ROM library holds no `frontieg` set, so it was not run; this reading is static.
- `frontiea` (2004, Bally / Oliver, "Free Play", rev. 1) replaces U2 and U6 with `frnt2732.u2` and `7406fn.u6`. Its `info.txt` gives version 1 of 031004, "add free play", and "if dip switch 25 = on and dip switch 26 = on freeplay is enable: decrease credits not lower then 01" (on the production ROM those two switches set the maximum credits to 40), and says the version number shows on the player displays after power-on. Its solenoid test fires the same thirteen outputs in the same order and publishes the same sixty lamps as `frontier`.

## Option switches

The manual assigns S1-S5 (coin chute #1), S9-S13 (chute #3), S17-S20 (chute #2), S25-S26 (maximum credits), S27 (credit display), S28 (match), S31-S32 (balls per game) and nine feature switches: S6 (A and C lanes linked), S7 (A-B-C extra ball lit from the start), S8 (both outlane specials), S14 (outlane specials with the 4X instead of the special), S15 (A-B-C lane memory), S16 (outhole collects the Frontier bonus), S23 (bonus maximum 110,000), S24 (gate recall) and S30 (both feed lanes). The table's option form offers S6, S7, S8, S14, S15, S16, S23, S24, S25-S28, S30, S31 and S32, and its settings match the manual's tables except in two places. For S14 its frame "Outlane Special lights when" offers "3X lights" (off) and "4X lights" (on), where the manual prints SW. 14 ON "Special lites come on when side drop target 4X is on." and SW. 14 OFF "Special lites come on when side drop target special is on." The ON readings agree and the OFF readings do not. The record follows the manual, which the ROM supports: with S14 off, the probe lit the outlane special together with the drop-target special on the right bank's third completion, not with the 3X drop-target lamp on the first. The form's OFF label is a table defect, not a disagreement about the machine. For S30 the form says "Feeder Lane Special lights" where the manual's lite is the 15,000 award the probe scored; its Alternate and Both light settings match the manual's. S21, S22 and S29 appear in no table and no text of the manual, and the table's form offers nothing for them; their function is unknown, and they are the open `input_semantics` requirement. The pinned PinMAME input ports default S21 on and S22 and S29 off.

## Displays

Four seven-digit player displays (controller indices 0-3, segment starts 1, 9, 17 and 25), a two-digit credit display (index 4, start 35) and a two-digit match and ball-in-play display (index 5, start 38); the parts list counts five display driver boards. The harness also reports a 128x32 layout at index 6 that `dispBy7` does not declare; the machine has no such display, and the definition lists none.

## Spatial placement

Switch, coil and flipper placements come from the retained table, normalized to its bounds (see `reports/spatial/bally/frontier-1980.md`). They are `observed`: no factory-drawing callout check was made, and each sits where Figure V draws the part. The in-line reset is projected onto the mean of its three targets and the right-bank reset onto the bank's middle target; both coils are hidden assemblies under their banks.

**The open blocker.** No lamp is placed. The table's lamp lights are classic lights drawn over the inserts; only the three thumper bumper lamps (`L10`, `L26`, `L42`) and the bumper lights beside them are bulb-mode lights, and none of them shows a bulb mesh. The table's bulb models, the 27 `BulbFil`/`BulbTop` primitive pairs, all sit on its general-illumination lights (at most 6.4 units away), and the nearest lamp light to any of them is 64.6 units away. A light that marks no bulb marks no socket, so all 54 playfield lamps are unplaced. A table that models the lamp bulbs, or a registered playfield photograph, would settle them; the `vpxtable_scripts` corpus pins a VPW script, `Frontier (Bally 1980) v2.0.0.vbs`, whose table is not retained here.
