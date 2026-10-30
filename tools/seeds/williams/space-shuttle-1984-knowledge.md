# Space Shuttle (Williams, 1984)

Williams model 535, December 1984, System 9 (PinMAME `GEN_S9`), 7,000 units (IPDB 2260). Design Barry Oursler
and Joe Kaminkow. IPDB lists a plastic shuttle replica on the playfield as the first playfield toy on a solid-state
production machine, and notes that the game rings a bell instead of a knocker and has speech. Two production game
ROMs exist in PinMAME, `sshtl_l7` and `sshtl_l3`; both run the same machine.

Sources: the Instruction Manual dated Nov 3, 1984 with schematics (IPDB, 33 pages), the pinned PinMAME driver,
the known-working VPX script, and LibPinMAME harness runs of both ROMs. The excerpts under
`evidence/excerpts/williams.space-shuttle.1984/` quote every table and drawing relied on here.

## Controller and addressing

- System 9 is the System 11 controller family in PinMAME: an 8x8 switch matrix at public 1-64, an 8x8 lamp
  matrix at 1-64, solenoids 1-16 (controlled) and 17-22 (special), the game-on enable at 23, four 7-digit score
  displays and a 4-digit credit / ball-in-play display.
- The manual's printed switch, lamp and solenoid numbers are the public addresses. The ROM's own tests prove it
  for switches 1-49 (Test 03 shows each closure's number; 50-64 show nothing) and solenoids 1-16 (Test 02 steps
  01-16, wraps, and pulses the shown number). The manual's generic text says the test runs to 25 and that
  sub-test 25 drops the flipper relay; this ROM does neither.
- The switch matrix reads uninverted on System 9: every switch is normally open and active at public 1.
- The table wiring printed in the switch and lamp matrices disagrees with the board drawings on a few pins (the
  switch rows are printed in reverse order through the 1J10-4 key pin; lamp column 4 and row 4 are printed on the
  key pins 1J7-5 and 1J6-4). The structured wiring follows the CPU schematic and the backbox wiring diagram,
  which agree with each other; the printed cells stay in the excerpts.

## PinMAME's jet-bumper special-switch table is rotated

The game's solenoid table, its solenoid and switch location lists and the playfield special-switch wiring all
pair the specials with their own devices:

| special | device | matrix switch on the same bumper | special-switch input |
| --- | --- | --- | --- |
| 19 | Left Jet-Bumper | 25 Left Jet | 8SW67, 1J18-2 |
| 20 | Lower (Bottom) Jet-Bumper | 27 Lower Jet | 8SW68, 1J18-4 |
| 21 | Right Jet-Bumper | 26 Right Jet | 8SW69, 1J18-8 |

PinMAME's `sxx.ssSw` for `sshtl` is `{39, 40, 27, 26, 25, 0}`, so it publishes 19 when 27 closes, 20 when 26
closes and 21 when 25 closes. The switch-test and gameplay runs show exactly that. On the machine each jet coil
is fired by its own skirt switch through the CPU board, without the ROM; the matrix contact on the same bumper
only scores. A recreation should fire each jet bumper locally from its own skirt contact and treat 19-21 as
informational; driving a bumper from PinMAME's 19-21 would kick the wrong bumper. The known-working script does
exactly that: its bumpers fire themselves and it binds no callback to 17-22. The kickers (slingshots) 17 and 18
follow their own switches 39 and 40 in both the machine and PinMAME.

## Playfield and rules

- Top: three top lanes U-S-A (29, 30, 31), lamps 29-31. Below them the left and right jet bumpers (25, 26) and
  the bottom jet bumper (27), each with a bumper lamp (25-27); jet-bumper lighting follows Game-Adjustment #6.
- Upper right: the long ramp entrance with the spinner (37) and its 1,000 / 2,000 / 4,000 spinner lamps (33-35).
  The long ramp has a lower switch (45, under the entrance) and an upper switch (32, at the top right where the
  ramp turns down the right side). The right ramp ends at the ramp bull's-eye target (38), which re-selects the
  S-H-U-T-T-L-E value.
- Centre: the 3-bank drop targets (33 lowest to 35 highest along the long ramp's left side), the "T"
  drop target (20) below the long ramp, standups 46 (centre), 44 and 43 (left), 47 (upper right) and the
  rebound/standup switches 42 (lower left) and 48 (lower right).
- S-H-U-T-T-L-E: standups 17, 18, 19 on the left bank, the "T" drop target 20 in the centre, and 21, 22, 23 on the
  right bank, lamps 17-23. Hitting the "T" drop target last awards 100,000 bonus (manual).
- Two eject holes (kick-out holes): left 16 (lamp 16 Left Lock) and right 24 (lamp 24 Right Lock).
- Lower playfield: flipper return lanes 14 and 15 (two lamp sockets on lamp 15), outlanes 28 (left) and 13
  (right), the right-outlane gate (13), the outlane shuttle arrows (two sockets on lamp 41), slingshots 39/40,
  bonus multiplier lamps 9-14 (2X-7X), the bonus ladder 50-64 and the up post ("heat shield") between the two
  flippers.
- Backbox lamps: 1-6 (Game Over, Match, Tilt, High Score to Date, Shoot Again X2, Ball in Play) and the insert
  panel lamps 38 (Stop & Score X2), 39 and 40 (Tail Engine, Tail Engine X2).

## Ball path and mechanisms

- Three balls. A drained ball falls into the outhole (9); the outhole kicker (1) lifts it onto the ball ramp
  (trough) under the apron, where balls rest on the lower (12), middle (11) and top (10) positions. Initialize 10,
  11 and 12 closed and 9 open with all three balls home (the known-working script does the same). The ball-ramp
  release (2) kicks the ball on 12 into the shooter lane (36), where it waits for the manual plunger; the next
  ball rolls down onto 12.
- The ROM serves with 2 at game start (with the "T" reset 5, the 3-bank reset 6, the post down 8 and the game-on
  enable 23), after a ball is locked in an eject hole, and after the last ball in play drains (gameplay run).
- Eject holes 16 and 24 are locks. A ball resting in either one is held, the ROM flashes the space (9), shuttle
  (10) and insert (14) flash lamps and serves another ball. With balls in both holes, the long-ramp shot (32)
  starts multi-ball: the ROM raises the post (7), fires the left eject (3) at once and the right eject (4) about
  3 s later (gameplay run). IPDB lists 2-ball and 3-ball multiball. The ROM fires an eject only from its own
  schedule; a recreation should model each hole as a saucer that holds a ball until its coil fires.
- 3-bank: three drop targets (33-35) with one reset coil (6). The ROM resets the bank at game start and when all
  three are down; completion increases the spinner value (manual) and, in the run, released the outlane gate.
- "T" drop target (20): a single drop target with its own reset coil (5, SA 5-24-750-DC). The ROM reset it after
  the ramp bull's-eye (38) in the run, and at game start. IPDB calls it a timed drop target.
- Post (heat shield): one post between the flippers driven up by the Up Post coil (7) and down by the Down Post
  coil (8), a two-coil latching post with no position switch. The manual: a centre-ramp shot raises the heat
  shield. In the run the long-ramp shot (32) raised it; game start and the left return lane (14) lowered it.
  Lamp 7 (Up Post X2, two bulbs) lights the post itself; the script models it with `lp2`, `CPFlash1` and
  `CPFlash2` on the centre post. Default: down.
- Right outlane gate (13, SZ-35-4000-DC): a holding coil on the right outlane. Game-Adjustment #7 says the old
  gate energizes to let the ball drain and the new gate energizes to return the ball to the flipper, and #4 sets
  whether it starts open or closed. At factory settings the run shows the right outlane rollover (13) energizing
  the gate, which stays held until the 3-bank is completed. Lamp 28 (Gate Open) shows its state. The script
  rotates its `bottomgate` flipper object to its end while 13 is on.
- Jet bumpers 19-21 and kickers 17-18: see above. Strength and recovery are table-owned.
- Flippers: two 50 V flippers (FL23/600-30-2600-50VDC). The solenoid table prints a third, `Top Flipper`, row
  with no wiring; no drawing shows a third flipper and IPDB lists two, so it is not fitted. The right flipper
  carries the B-9951 lane change switch (41) for the lane change feature IPDB lists.

## Flashers, GI and cabinet outputs

- 9 Space flash lamps and 10 Shuttle flash lamps: two flash-lamp domes ("hot dogs") on the centre playfield,
  left (space) and right (shuttle), each a `#89`-type flash bulb load in PinMAME. The flash-lamp bridge note
  draws four bulbs per circuit; the manual does not say which circuits it applies to.
- 14 Insert flash lamps: the solenoid table connects it through the playfield plug 8P3-14, while the
  known-working script lights a backglass rocket-plume object from it. Where its bulbs are is unresolved (see the
  conflict in the definition); it flashes with locks and ramp shots.
- 11 General illumination: relay 5580-09555-00 on the power supply (3P7-1). Energized means GI off (PinMAME types
  it reversed; the script's `PFGI` treats enabled as off). The ROM blinks it with effects and turns the GI off on
  tilt.
- 15 Bell (SM-29-1000-DC) in the cabinet: the game's award sounder instead of a knocker. It rings with ramp
  scoring and with the replay credit award (credit-award run).
- 16 Coin lockout (SM-35-4000-DC): energized while coins may be accepted.
- 12 and 22 are printed Not Used. 12 has a driver (Q57) and the wiring diagram ends it at 8L12 NOT USED; the ROM
  pulses it only in its solenoid-test sweep, never in play or on the credit award. 22 has a driver and a trigger
  input but PinMAME gives it no switch.

## Attract, start and tilt

- Attract mode drives no solenoid; the coin lockout is held.
- Start: coin, then the credit button. The ROM resets the "T" target and the 3-bank, lowers the post, sets the
  game-on enable 23 and serves.
- Tilt: the manual says one closure of the ball-roll or playfield tilt ends the turn and the plumb bob tilts on
  its third closure (adjustment 29). In the L-7 gameplay run two closures of the playfield tilt (49) did not tilt
  and the third did, dropping 23 and turning the GI off; a recreation should follow the ROM.

## Diagnostics

- Coin door: Advance (-7) and Auto-Up/Manual-Down (-6). Test order from the display test: 00 sound, 01 lamps,
  02 solenoids, 03 switches, then 04 bookkeeping. Credit display shows the test number, the ball-in-play display
  the step or switch number.
- CPU board: memory-chip diagnostic (-5) and sound diagnostic (-4).
- Jumper W5 is fitted (corrections sheet), which PinMAME's DIP 0 default reproduces.

## Edition and ROM differences

- L-7 (`sshtl_l7`, root) and L-3 (`sshtl_l3`, clone) share all game data: display layout, special switches,
  flipper handling and the sound and speech ROMs; only the U20 game ROM differs. Both step the identical
  solenoid test. Gameplay was observed on L-7 only.
- The retained `sshtl_l7` archive's sound ROM differs from PinMAME's listed CRC; it does not affect the switch,
  lamp or solenoid behaviour recorded here.
- The 1980 Zaccaria Space Shuttle (`sshtlzac`) is an unrelated machine.

## Spatial placement

- Playfield devices are placed on the retained table's objects (see the spatial report). Switches on ball
  objects or triggers sit on those objects; the trough positions on the table's three trough kickers; drop
  targets on their walls' drag-point centroids; slingshots on their walls; jet bumpers on bumper centres; the
  lane change switch on the right flipper pivot; the standup/rebound switches 42-44 and 46-48 on the centres of
  the table's collidable sensor meshes; the post coils and lamp 7 on the centre post; the hot-dog flash lamps
  on their dome meshes.
- No factory drawing callout check has been run, so every placement is `observed`, not `validated`. The playfield
  tilt (49) and the insert flash lamps (14) have no placement.
- The switch-location drawing numbers the three trough positions 12, 11, 10 left to right under the apron, the
  reverse of the list's `Upper Left`/`Lower Right` names; the list, the script (12 next to the ball release) and
  the ROM's serve logic agree, so placements follow them.
