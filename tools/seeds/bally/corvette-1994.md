# Corvette (Bally, 1994)

Coverage: **partial - every I/O address, controller binding, polarity and wiring detail is
source-reconciled from the manual, the ROM's own service tests and a retained known-working table;
`variant_differences` is missing because no source says what hardware the PX prototype ROMs were built for,
and `spatial_placement` and `unresolved_conflicts` because the table and the manual disagree on which half
of the playfield each G.I. string lights, so the four playfield strings have no placement**

## Identity and evidence precedence

This is the Midway Manufacturing Company (trade name Bally) WPC-Security physical machine of August 1994,
model 50036, IPDB 570, 5,001 units, designed by George Gomez with mechanics by Tom Kopera. It covers the ten
`corv_*` drivers: `corv_21` (game ROM 2.1, the parent; the ROM identifies itself as `CORVETTE / 50036 REV.
2.1`), `corv_la1`, `corv_lx1`, `corv_la2` and `corv_lx2` (earlier L-1 and L-2 production ROMs, LA and LX
builds; `corv_la1` and `corv_lx2` identify themselves the same way and open the same test menu),
`corv_dx1` (the community LED Ghost Fix of LX-1), `corv_px3` and `corv_px4` (prototype export ROMs),
`corv_px5` (PX-4 with the LED Ghost Fix, per pinned `corv.c`) and `corv_f61` (FreeWPC 0.61 community
firmware, `identical`: same hardware, different rules). All share one `corvGameData` on `wpc_mSecurityS`.

IPDB quotes the designer: the game was first designed with drop targets and a four-speed shifter bolted to
the cabinet for the dragstrip mode, the code for both is still in the game, seventeen prototypes were built
and some carried those features. The prototype ROMs therefore stay `unknown` for physical compatibility,
and matrix switches 25-28 (`1st` to `4th Gear (optional)`) are the shifter's positions: the production
manual lists them without a part, the 2.1 ROM still names them, and they are `optional`.

Evidence precedence: the retained known-working table `Corvette (Bally 1994).vpx` (version 1.4.2 by Goldchicco,
32assassin and Mussinger, `cGameName = "corv_21"`, `HandleMechanics = 7`) controls runtime binding and the
coils' causal contract, and its objects give the placements; the ROM's own service tests settle names and
output identity. The IPDB scan of the operations manual (and its Manual Amendment 16-9890 of September 1994)
controls physical construction, part numbers, wiring and device presence; pinned PinMAME `97aa922b`
(`src/wpc/sims/wpc/prelim/corv.c`, a preliminary simulator) controls the controller generation and public
addresses; the ROM's own service tests, run on a legal `corv_21` ROM, settled polarity, names and every
output's identity. Every table used is transcribed under `evidence/excerpts/bally.corvette.1994/`, and the
runs are summarized under `evidence/runtime/wpc-security/corvette-corv_21-*.json`.

## Controller platform and address topology

- WPC-Security (`GEN_WPCSECURITY`, hardware generation `0x20`), 128x32 DMD, DCS sound, Fliptronic II.
- Switches: coin door 1-8, matrix 11-88, Fliptronic 111-118; no custom switch column. PinMAME's inverted
  switch mask `{0x00,0x00,0x00,0x7f,0x07,0x33,0x00,0x03,...}` inverts exactly the sixteen optos the
  matrix shades: 31-37, 41-43, 51, 52, 55, 56, 71 and 72.
- Solenoids: 1-28 on the power driver board; 29-32 PinMAME state channels (31 is the WPC game-on state, as
  `corv.c` sets no fast-flip address); 33/34 the ramp diverter on the Fliptronic upper-right circuit;
  35/36 the upper left flipper; 37-44 unused on this generation; 45-48 the lower flippers; 49/50 reserved;
  51-53 the three custom outputs `corv_getSol` reads from the CPU's extension register 3 bits 0-2, which
  is the Motor Driver Master Board's U2 latch.
- Lamps 11-88, five G.I. strings 0-4.
- The engine's commanded angle is not an output address: the ROM writes it to extension register 2 (the
  Master Board's U1 latch, the Slave Board's AD7524 DAC). PinMAME's engine model reads that byte and, with
  mechanism handling on (bit 2, value 4), `PinmameGetMech(2)` / `Controller.GetMech(2)` returns it (0-255;
  the model closes FULL LEFT 71 below 64 and FULL RIGHT 72 above 191). Bits 0 and 1 run the left and right
  race-car models, which hold 51/52 at the start and pulse 55/56 while the cars move.

## Switch polarity: what the ROM's service tests settled

T.1 SWITCH EDGES (a sweep of every matrix and Fliptronic address with mechanisms disabled) names every
switch on its top line while it reads it as active. All sixteen masked optos are named at public 1, so
their matrix contacts rest closed (`normally_closed: true`); every other matrix switch is named at public
1 unmasked and rests open. 24 (Always Closed) rests at 1 and is named on its 1 -> 0 edge. 53, 54, 73, 74
and 85 show `NOT USED`: the ROM scans the positions with no device behind them. Closing 61-65 fired the
sling and jet coils 9-13 even inside T.1.

The Fliptronic column is read complemented (`WPC_FLIPPERS` returns `~swMatrix`), so public 1 is a pressed
button on every opto position. Each cabinet button carries two optos on one A-17316 board: the right
button F2 (112) and F6 (116), the left button F4 (114) and F8 (118). The ROM fires the lower right
flipper (45, 46) from either 112 or 116, the lower left (47, 48) from 114 and the upper left (35, 36)
from 118, so a recreation writes 112 and 116 from the right button and 114 and 118 from the left. The
end-of-stroke bits 111, 113 and 117 are synthesized by PinMAME from the FLIP_SOL flippers; F5 (115) has no
switch fitted (the Fliptronic II list prints J906-4 Not Used) and the ROM ignores it.

## The ZR-1/LT-5 engine (headline mechanism)

An engine-shaped toy at the upper left (Engine & Ramp Assembly A-19140) rocks left and right as a ball
shaker. It is not a motor: the engine block (A-19135) carries four coils (AE-25-1000; the repair bulletin's
table prints ENGINE COILS (4)) working against an engine-shake weldment with a magnet (A-19137), a Hall-effect sensor (A-19230) reads its angle, and the
Engine Full-Stroke Opto P.C.B. A-18951 reports FULL LEFT (71) and FULL RIGHT (72). The CPU drives it as a
servo: the Motor Driver Master Board A-18532 latches a position byte (to the Slave Board's DAC, whose
LM324 and TIP102 drivers power the coils as SOLA1/2 and SOLB1/2) and three control bits through a ULN2803:
bit 0 (public 51) drives both DISABLE lines, bit 1 (52) the LED A pair and bit 2 (53) the LED B pair to
the Slave Board. The amendment adds a Hall Offset Adjust board with a centring potentiometer reached
through a hole in the ramp.

The ROM's T.16 ZR1-LT5 TEST, with PinMAME's engine model answering, raises 51 on entry and keeps it on,
then sweeps the position down until FULL LEFT closes (it records 63), up until FULL RIGHT closes (192) and
parks the engine at 127, toggling 52 and 53 while the engine moves; ENGINE LEFT drives the position to 63
with FULL LEFT closed. With nothing answering, the self test drops 51 after about 13 s and shows `POSITION
OFF` and `FAILED`. T.18 ZR-1 ADJUST raises 51 alone and holds the engine centred. The amendment says the
coin door must be closed to turn on the engine power. Adjustment A.2 16 DISABLE ZR-1/LT-5 exists for a
broken engine with its lock-down bracket installed.

A recreation drives the engine angle from the ROM's commanded byte (`GetMech(2)` with mechanism bit 2
on), reports 71 while the angle is at the left stop and 72 at the right stop, and treats 51 as the engine
power enable. What 52 and 53 do on the Slave Board (the LED A and B lines) is not traced beyond the
Master Board.

## The race track and the Corvette Challenge

Along the right side of the playfield two Matchbox-style cars run in lanes on the Race Track A-19004 (left car
A-19145, the player; right car A-19146, the machine), pulled by cords from a Gear Box A-19134 with two
14-8015 motors. The Dual H-Drive Motor Controller A-19159 takes three power driver outputs: 17 RACE
DIRECTION and 18/19 LEFT/RIGHT RACE ENABLE. Each lane has a start (limit) opto (51 left, 52 right) and an
encoder opto on the cord pulley (55, 56). A Christmas tree of six lamp circuits (81-86, eight bulbs: the yellow 83 and 84
light two each) stands by the track. The
ROM's T.17 RACE TEST self test drove the left car forward with 17 and 18 on, counting 55 to 670 while 51
opened, then the right car with 17 and 19 to 638, then returned both to their start optos; LEFT FORWARD
raised 17 and 18 together and the left car's count climbed. With PinMAME's car models that is consistent
with 17 on meaning forward. During the CORVETTE CHALLENGE the machine's car moves at a steady pace and the
player's car advances as shots are made (rules page E).

The manual's Section 3 puts the track limit board on column 5 rows 1/2 and the encoder board on column 5
rows 5/6, as the matrix and the ROM do; the amendment's page for the Opto Track Encoder P.C.B. A-18822
re-wires it to column 7 rows 1/2, which are the engine's full-stroke optos in the matrix, the ROM and the
engine board's own page. The Switch Locations list also crosses the boards' part numbers (start optos
A-19141, encoders A-18821). The ROM's names and its accepted race test settle the public addresses.

## Other mechanisms

- Ball trough: Outhole Ball Trough Assembly A-18753 with the Trough 7 IRED/IR TSTR boards; TROUGH BALL 1-4
  (31-34) and TROUGH EJECT (37); TROUGH EJECT coil 1. Four balls (the rules' Puzzle multiball is four-ball).
- Manual plunger with the PLUNGER switch (15); no auto-launch coil.
- ZR-1/LT-5 ramp and lock: entry optos ZR1 BOTTOM ENTRY (41) and ZR1 TOP ENTRY (42), ZR1 EXIT (75), ZR1
  LOCK BALL 1-3 (76-78), the ZR-1 LOW REV GATE (2, SM1-28-900-DC, part of the engine ramp), the ZR-1 UP REV
  GATE (5, SM1-35-4000-DC; the amendment's Ball Gate Actuator carries this coil) and the ZR-1 LOCKUP coil
  (15, AE-30-2000, Eject Assembly A-15368-1). The rules lock up to three balls in the engine mechanism for
  the Mid-Ohio Endurance multiball; Adjustment A.2 13 releases or holds them at game end. The retained
  table gives each coil its contract and leaves the timing to the ROM: while 2 ("Lock Gate 1") is on, the
  engine-ramp gate `LGate` is closed and the wall `Wall12` beside it raised; while 5 ("Lock Gate 2") is on,
  the upper engine-ramp gate `GateU` is open; a ball reaching the lock kicker `Kicker1` joins a ball stack
  that holds 76, 77 and 78 for one, two and three balls; each pulse of 15 ejects one ball at `Kicker3`, just
  below the lock entry. 16 opens the gate `TGate` across the top loop while on, and 34 alone moves the
  diverter (`SolCallback(33)` is commented out).
- PIT STOP POPPER (36, coil 4, Popper Assembly A-19005); ROUTE 66 KICKOUT (57, coil 8, on the back panel
  next to the track); the left outlane KICKBACK (coil 3, Kicker Bracket B-11873); the LOOP GATE (16); the
  ramp DIVERTER (33 power, 34 hold, Flipper Coil Assembly A-15943-1 on the Fliptronic upper-right circuit,
  whose flipper coil cell prints NOT USED).
- Slingshots 61/62 (coils 9/10), jets 63-65 (coils 11-13), a spinner (18), knocker (7, cabinet).

## Lamps, flashers and general illumination

T.8 names all 64 lamps 11-88; 81-86 are the race-tree lamps, 87 the BUY IN and 88 the START button. The
flasher and general-purpose circuits 21-28 each light a playfield bulb (#89 on 21-24 and 26, #906 on 25,
27 and 28), and 22-28 also a #906 in the backbox from the same driver (the table prints separate
playfield and backbox drive connections); 20 TENTH CORVETTE is a backbox flasher that lights the future
car in the backglass. G.I. strings 0 (UPPER LEFT) and 1 (UPPER RIGHT) are
playfield only, 2 (LOWER LEFT) and 3 (LOWER RIGHT) also feed the backbox, and 4 (BACK BOX TITLE) is the
backbox only; the ROM's T.6 dims all five.

The retained table drives its lower-left bulbs from GI 0, its lower-right bulbs from GI 1, its upper-left
bulbs from GI 2 and its upper-right bulbs from GI 3: the halves are swapped against the manual's and the
ROM's names. No retained wiring page or bulb list assigns individual bulbs to a string, so this is recorded
as a conflict and the strings have no placement. Running T.6 on a physical Corvette and watching which bulbs
dim for UPPER LEFT settles it. The table also binds lamps 1-3 to its bumper lights, numbers PinMAME never
publishes, so those bumper lights never light; the real bumpers have no matrix lamps.

## Open mechanism behaviour

- The table's engine shake is an approximation: four magnet triggers in the engine grab the ball while the
  ZR-1 UNDERSIDE flasher (26) is on. The real shake comes from the engine coils the servo drives (51 and
  the position byte); 26 is only a flasher.
- The physical linkage of the two rev gates is not drawn in any retained source; the table's per-coil
  contract above is what a recreation consumes.
- What the Slave Board does with the LED A and B lines (52, 53) is not traced.
- What the PX-3/PX-4/PX-5 prototype ROMs expect: the designer's drop targets and shifter suggest hardware the
  production machine lacks. A prototype's own test menu (the archive here lacks PX-4's sound ROM, so it stops
  on a sound-board error) or a description of the prototype playfield would settle it.

## Wiring notes

The Power Driver Board's pin list disagrees with two tables: it prints the lamp columns on J138 and the rows on
J135 (J133 and J137 Not Used) where the Lamp Matrix prints J137/J138 and J133, and it labels G.I. connector J121
'to insert' and J120 'to playfield', the reverse of the Solenoid/Flasher Table's columns, which agree with the
bulb types and string names. The wire colours and devices agree, so the records follow the game's tables and
note the board list's readings on each device.

## Spatial status and why the record stays partial

Fitted playfield switches, coils, flashers and lamps are placed from the retained table's objects (979 x
2162 units) and checked against the manual's lamp (2-45), switch (2-47) and solenoid/flasher (2-49)
location drawings by an independent callout reading with jet-bumper and flipper-pivot control fits; 103 of
the 111 checked placements agree within 0.07 and are validated. Seven reads whose leader runs on past
where the reader stopped were corrected after a pixel trace, each with its reason in the callout seed. Projections are disclosed on each device:
the trough optos and trough eject onto the trough kicker, the lock switches onto the lock kicker, the
engine full-stroke optos onto the engine, the race optos and motors onto the lane ends. Lamps 53 and 68,
which the script draws only on glow sprites, sit on the table's stacked red and green bulb meshes `L81P1`
and `L81P4`; no source says which colour is which lamp, and the pairing moves neither by more than 0.0005.
Lamps 76-78 and the race tree 81-86 and the playfield bulb of flasher 26 have no placement: the table draws them
only on Flasher sprites (hidden ones for the race tree) or a light parked off the playfield, and a sprite
is a glow, not a socket; measuring them on the location drawings would place them. `spatial_placement`
stays missing for those and for the four playfield G.I. strings (see above); `reports/spatial/bally/corvette-1994.md` lists every placement the
drawings do not confirm.

## Author construction checklist

1. Wire every matrix switch as the manual's matrix and the ROM's T.1 names; the sixteen shaded optos are
   normally closed at public 1.
2. Write 112 and 116 from the right flipper button and 114 and 118 from the left.
3. Model the engine as a servo: take the angle from `GetMech(2)` with mechanism bit 2 on, report 71/72 at
   the stops, power it while 51 is on.
4. Model the two race cars on 17/18/19 with start optos 51/52 and encoder pulses on 55/56 (or let
   PinMAME's models do it with mechanism bits 0 and 1).
5. Light flasher circuits 22-28 in both places they reach, and drive the backbox G.I. from strings 2-4.
6. Fire the lock as the table does: 2 closes `LGate`, 5 opens `GateU`, 15 ejects one locked ball; place
   the playfield G.I. bulbs on strings 0-3 only after settling the half-swap conflict.

## Sources

- Manual `Bally_1994_Corvette_Manual.pdf` (IPDB 570), Manual Amendment 16-9890 and Unit Disassembly For
  Repair 16-9887, transcribed under `evidence/excerpts/bally.corvette.1994/`.
- Pinned PinMAME `97aa922b` `src/wpc/sims/wpc/prelim/corv.c`, `src/wpc/wpc.c`, `src/wpc/core.c`,
  `src/wpc/vpintf.c`.
- ROM service tests T.1, T.4, T.5, T.6, T.8, T.12, T.16, T.17 and T.18 on `corv_21`, summarized under
  `evidence/runtime/wpc-security/`.
- The retained table `Corvette (Bally 1994).vpx` version 1.4.2 (SHA-256 `4b500c6b...`) and its embedded script,
  with a 1,390-file extraction manifest; the placement seed `tools/seeds/bally/corvette-1994-spatial.json`
  and the callout seed `tools/seeds/bally/corvette-1994-callouts.json`.

## Procedural note

The DMD menus give no text checkpoint, so every run is counted button presses; each reading is the
curator's view of a retained frame pinned by its pixel SHA-256. Names blink in T.4, T.5, T.8 and T.12, so
the scenarios take frames while presses are held and shortly after. Escape leaves T.16 entirely, and Up is
ignored while a T.16 or T.17 sub-test runs.
