# Creature from the Black Lagoon (Bally, 1992)

Coverage: **partial**. Every public address is enumerated, named, wired and polarized, the mechanisms and the
driver variants are described, and the factory drawings validate most placements. Two requirements stay open:
the 32 chase bulbs cannot be assigned to their strings (`spatial_placement`), and the manual's chase-board
diagram and its parts list disagree on which ramp boards each chase group drives (`unresolved_conflicts`,
`conflict.chase-light-board-group-assignment`).

## Identity and evidence precedence

The Bally WPC-Fliptronic machine of 1992 (model 20018, IPDB 588). The eight `cftbl_*` drivers are firmware
revisions of it: `cftbl_l4` (parent, production L-4), `cftbl_l3` and `cftbl_l2`, the community "LED Ghost Fix"
revisions `cftbl_d4`, `cftbl_d3` and `cftbl_d2`, the 2020 community `cftbl_l4c`, and the prototype `cftbl_p3`
("REV. P-3"). No source describes the prototype machines' own hardware, but replayed on the P-3 ROM the T.1, T.5,
T.12 and T.15 scenarios name and drive the same addresses with the same wires as L-4, so it is recorded
`compatible`; only three display strings differ (T.5 "LFT SUBWAY FLHR" for 2 and "CREATURE FLSHR" for 11, T.1
"P OF PAID" for 25).

The retained known-working table is VPW's v1.0 (SHA-256 `960ebdd1...`), whose script binds `cftbl_l4`. It is the
runtime authority and the geometry source for the objects its script binds. It supersedes the older community
table the earlier curation used, which bound a 32-light chase animation to G.I. 0 and modelled none of the socket
boards. The operations manual (arcade-museum.com scan, SHA-256 `d84d28a8...`) controls construction, wiring,
quantities and location; its OCR text layer garbles every table, so every table was read from rendered pages
and transcribed under `evidence/excerpts/bally.creature-from-the-black-lagoon.1992/`. IPDB's factory parts list
supplies the chase boards and cables. Pinned PinMAME `97aa922b` controls the controller topology, and five
LibPinMAME harness runs of `cftbl_l4` (four of them replayed on `cftbl_p3`) supply the ROM's own names and behaviour.

## Controller platform and address topology

`GEN_WPCFLIPTRON` with `wpc_dispDMD` (`pinmame.wpc-fliptronic`, hardware generation `0x8`).
`cftblGameData` declares `FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L)`, `lampCol = 1` and
`gameSpecific1 = WPC_CFTBL`, no custom solenoids and no fast-flip address.

- Switches: coin door 1-8, matrix 11-88 (40 used, 24 printed Not Used), Fliptronic 111-118.
- Solenoids: drivers 1-28; 29-31 mirror `WPC_GILAMPS` bits 5-7 (31 is active in the service menu); 32 is
  constant zero; 33-36 are the Fliptronic upper-flipper circuits, here the backbox insert flashers; 37-44 are
  unused (no LPDC board on this generation); 45-48 are the lower flippers' power and hold windings; 49 and 50
  are PinMAME's simulator and reserved channels.
- Lamps: the full 8x8 matrix (no Not Used lamp) and the chase strings at 91-98 (see below).
- G.I.: five strings 0-4. Strings 0 and 3 feed only the chase board.

## Switch polarity

`cftblGameData`'s inverted-switch mask covers 15, 34, 37 and 38, but only 34 and 37 are optos (the Switch
Locations list prints an A-14231 LED over an A-14232 phototransistor for each popper). Their contacts rest
closed and PinMAME's mask normalizes them: public 1 means a ball is in the popper, and the ROM's T.1 names
RIGHT POPPER while public 34 is 1.

- **15, Top Left Rollover**, is an ordinary micro switch (5647-12693-19) that closes while a ball is on it, so
  `normally_closed` is false. Because PinMAME inverts it, a recreation publishes **1 while no ball is on it and 0
  while one is**, the opposite of every other rollover. The VPW script does exactly that (start-up 1, `Hit` 0,
  `Unhit` 1), and the definition declares `initial_active` for it.
- **38, Ramp Up/Down**, is the lift ramp's position switch. Public 1 means the ramp is down: the script writes 1
  when the down coil (26) fires and 0 when the up coil (23) fires, and `cftbl_handleMech` does the same. With the
  mask, the contact the matrix sees closes while the ramp is up.

Every other matrix switch rests open.

## Fliptronic block

The Switch Matrix page still prints F5-F8 as "Upper Right/Left Flipper End of Stroke/Opto", but the game has no
upper flipper. The board pages settle each position:

- **115 (F5)** and **117 (F7)** are not fitted: the Fliptronic II connector list prints J906-4 Not Used, and
  J906-5 names an upper left end-of-stroke switch the machine does not have. In T.1 the ROM names nothing for
  either.
- **116 (F6)** and **118 (F8)** are the second optos of the right and left cabinet Flipper Opto Switch Boards
  (A-15894, two optos per board; the left board's J1-2 "upper flipper" runs to J905-5, the right board's to
  J905-3). In T.1, public 116 fires the lower right flipper (45/46) and 118 the lower left (47/48): **a recreation
  drives 116 with 112 and 118 with 114**.
- The four upper-flipper drive lines J902-6, -4, -3 and -1 are printed "to insert flashers". The ROM's T.5 names
  public 33-36 **CREATURE FL. 1** to **4** with their wires BLK-YEL, ORN-VIO, BLK-BLU and ORN-GRY: four backbox
  insert flashers.
- The lower flippers are FL-11629 (right, A-15205-R-2) and FL-15411 (left, A-15205-L-4). The ROM's T.12 FLIPPER
  COIL TEST has four items (R./L. FLIP. POWER and HOLD) and never drives 33-36. PinMAME synthesizes the
  end-of-stroke bits 111 and 113.

## Trough, outhole and shooter lane

A drained ball rolls onto outhole switch 55; the outhole kicker (12, A-8039-3) kicks it into a three-ball
trough on switches 58, 57 and 56. The ball release (4, B-9362-L-2) feeds the ball on 56 into the shooter lane,
where the player plunges it from switch 66 with a manual plunger up past the P-A-I-D lanes 25-28.

## Holes, subway and poppers

The left hole (switch 16) awards K-I-S-S and the centre hole (switch 17) the Snack Bar: in a game the ROM
flashes K-I-S-S lamp 21 for 16 and lights Snack Bar lamp 53 with HIT TARGETS TO OPEN SNACKBAR for 17. Both drop
the ball into a subway that ends in the lower right popper (opto 37), kicked out by solenoid 3. The F-I-L-M hole
at the upper right is its own popper (opto 34, solenoid 1). **The switch drawing (2-41) transposes callouts 16
and 17**; the ROM, the rules and the printed names agree with the table, so those placements follow the table.

## Lift ramp and ramps

The A-16042 Lift Ramp Assembly under the head of the left ramp has an up coil (23, SM1-2B-900-DC) and a down coil
(26, AE-26-1200), both with tieback diodes, and switch 38. `cftbl.c`'s simulator sends a ball from the left ramp
entrance (36) up the Creature ramp to switch 64 and on to the bowl while 38 is 1, and along the swirl ramp past
switch 62 to the right inlane otherwise. The right ramp has its entrance switch 35 and its exit switch 61. The
VPW table binds its sw62 and sw64 triggers the other way round from both factory drawings (2-41 and the 2-44
ramp drawing), so 62 and 64 are measured on the switch drawing.

## Sequential G.I.: the chase lights

The swirl ramp and the bowl carry 32 #86 chase bulbs: 24 on three flexible eight-lamp boards on the ramp
(A-16089 "lt-1"; A-16088 "lt-2" chained into A-16087 "lt-3") and 8 on the bowl's A-15672. They are driven by the
**Chase Light II board A-15541** under the playfield (printed 3-14 and 3-15):

- G.I. string 01 (public **G.I. 0**, J120-7/J120-1) enters as "G.I. (1)" and is switched by four triacs onto
  LAMP 1A-4A on J4 (Orange-Brown, -Red, -Black, -Yellow). String 04 (public **G.I. 3**, J120-10/J120-5) enters as
  "G.I. (2)" and goes onto LAMP 1B-4B on J3 (Orange-Green, -Blue, -Violet, -Gray).
- Solenoids **20** and **24** are not coils: they are select lines DRIV. 1 and DRIVE. 2. Through 2N4403s they
  drive the A and B inputs of both halves of a 74LS139, so both groups always select the same string number.
- The 74LS139's outputs are active low and go through a ULN2803 to the 2N4403s that gate the triacs. **The
  selected output turns its string off and the other three conduct: three strings are lit and one is dark**, and
  the chase is a dark string stepping through each group. UFO Pinball's analysis of the board says the same
  ("three circuits are on, and one circuit is off").
- Pinned `wpc.c` publishes the chase at lamps **91-98** as `0x11 << code`, the selected code (solenoid 20 plus
  twice solenoid 24) in both groups, **whatever the G.I. does**; only its separate physical-output (modulated lamp)
  path ANDs the selection with G.I. triacs 0 and 3. So **public 91+k is 1 while string k+1 of group A is the dark
  one**, and 95+k likewise for group B, and a string's bulbs are lit while its G.I. is on and its address is 0. The
  ROM's T.15 RAMP LIGHTS TEST cycles 91, 92, 93, 94 (with 95-98 alongside); stopping it switches G.I. 0 and 3 off
  while PinMAME keeps publishing the selected pair (93/97 on L-4).
- The VPW script lights its chase phase while the address is 1 and its G.I. is on, so it shows one phase lit and
  three dark, the inverse of the board. It also gates the whole ramp with G.I. 0 and the bowl with G.I. 3.

What is settled about the groups: the bowl's cable H-15870 carries the J3 colours, so the bowl is on G.I. 3 and
lamps 95-98. What is not (`conflict.chase-light-board-group-assignment`):

- The block diagram (3-14) draws J4 to A-16087 alone and J3 to A-16088 chained on to A-16089, while the parts
  list chains A-16088 into A-16087 and gives A-16089 its own cable. The ramp's two cables are H-15871 (J4 colours)
  and H-16213, "front chase lite cable" (J3 colours); nothing says which board each plugs into, and the manual's
  cable list adds an H-16214 "Center Chase Light Cable" that neither assembly lists.
- No source gives the order of the four strings along any board's eight sockets.
- The Power Driver Board connector list (3-23) sends solenoid 20 to the chase board's J2-2 and 24 to J2-1, the
  opposite of the chase board's own page, which would swap strings 2 and 3.

Leads, not authority: a Pinside owner describes the ramp's two sections as "the ones towards the right and back
of the ramp" and "the ones on the left and front", flashing out of step when two plugs under the playfield are
swapped, and another reports one string dark on "5 in the ramp and 2 in the bowl". Both fit the reading that the
16-bulb A-16087/A-16088 pair (front) and the bowl are on G.I. 3 and A-16089 on G.I. 0, but neither settles it.
**Resolution:** on a working machine, pull J3 and then J4 at the Chase Light II board and note which ramp and bowl
bulbs go dark. Then film the ramp and bowl while the T.15 test cycles and note which bulbs go dark together and in
which order; stopping the test is no use, because it switches the chase power off. With the ramp off, a continuity
check from each board's header pins to its sockets gives the same answer. Until then lamps 91-98 and G.I. 0 and 3
carry no placement.

## The hologram

The Creature appears in the playfield window by a cabinet illusion: the hologram lamp (28, #1156) and the mirror
motor (27, 48 VAC) sit in the cabinet bottom, and the push motor (21, 48 VAC) under the playfield. Solenoid 11,
"Hologram Creature Flasher (Insert)", is two #906 bulbs on the backbox insert, not part of the projection.

## Other mechanisms

Three jet bumpers: top left (13, switch 45), top right (14, switch 46) and bottom (15, switch 33). Two slingshots:
left (6, switch 47) and right (5, switch 48). Four Snack Bar stand-up targets: Cola 41, Hot Dog 42, Popcorn 43,
Ice Cream 44. The whirlpool bowl (A-15993) has its micro switch 65 and the bowl flasher 10.

## Lamps, flashers and general illumination

- 71-78 spell the backbox C-R-E-A-T-U-R-E header; 88 is the Start button lamp. Lamp 18 "Admit One" sits on the
  back panel above the playfield's top right edge.
- Lamps 28, 37 and 44 have two bulbs each (both outlanes; two inserts in each lane), as the drawing and the table
  agree.
- The four sockets of the A-14305 board in the centre of the swirl (55-58), the two C-12709 boards at the upper
  left (63-65) and right of centre (66-68), and lamp 51 are placeholders in the VPW table; their placements are
  measured on the lamp drawing.
- Most flashers have one #89 dome on the playfield and two #906 bulbs on the backbox insert (17 has one). 9 is the
  two back flashers in the top corners and 25 the two Start Movie flashers on the lane walls.
- The printed G.I. strings 02, 03 and 05, "Insert/Playfield Middle", "Upper" and "Lower", are public 1, 2 and 4
  (#44 on the playfield, #555 on the insert). The VPW table drives a light collection for each, but those lights
  are invisible light-map sources, not modelled sockets, so their placements are only candidates.

## Spatial summary

The three location drawings (2-40, 2-41, 2-43) were transcribed by readers working only from the drawing crops,
and `tools/drawing_callouts.py` validates 86 of the 88 table placements it checks (lamps 25 and 26 have no printed
balloon). The table placements it does not check are the 16/17 holes (validated by the table, the ROM and the
rules), the flipper windings (projected onto the pivots) and the trough: the drawing labels the trough switches
55-58 with pointerless balloons one ball position away from the switches they name, so those four and the trough
and outhole coils projected onto their ball seats stay observed. 22 placements are measured on the drawings and
stay observed. The spatial report is `reports/spatial/bally/creature-from-the-black-lagoon-1992.md`.

## Author construction checklist

- Publish switch 15 inverted (1 at rest) and drive 116/118 together with 112/114.
- Treat 20 and 24 as chase-board select lines and G.I. 0 and 3 as the chase groups' power; light a chase string
  while its G.I. is on and its lamp address (91-98) is 0.
- Put the backbox insert flashers on 33-36 and solenoid 11, and the hologram on 21, 27 and 28.
- Do not invent chase-bulb positions per string until the conflict is resolved.

## Sources

- `manual.bally.creature-from-the-black-lagoon.1992` (SHA-256 `d84d28a807505339f57676e0222adc6cc6fe7bef7371d31f9a9076ec33021d97`).
- `parts-list.bally.creature-from-the-black-lagoon.1992.ipdb` (SHA-256 `17fe20d30906d64655ebb7d5d6e5ba492c84b5d395e604c7ce2d7af9ef012e14`).
- `vpx-table.cftbl-vpw-1-0` and `vpx-script.cftbl-vpw-1-0` (script SHA-256 `110d85325e33cbaf465f5a60f3aeeb2069329c55719435e7b76380748ba70ea6`).
- `pinmame.core.97aa922bf8e4`: `src/wpc/sims/wpc/full/cftbl.c` and `src/wpc/wpc.c`.
- The runtime runs under `evidence/runtime/wpc-fliptronic/creature-cftbl_l4-*.json` and `creature-cftbl_p3-*.json`.
- Leads only: UFO Pinball, "Technical Analysis of the CFTBL Chase Board", http://www.ufopinball.com/CFTBL-Chase/tech.htm;
  Pinside threads https://pinside.com/pinball/forum/topic/creature-from-the-black-lagoon-ramp-chase-lights-issue and
  https://pinside.com/pinball/forum/topic/cftbl-ramp-chase-lights.
