# World Cup Soccer (Bally/Midway, 1994)

Coverage: **author-ready — complete physical I/O inventory, WPC-Security bindings, mechanism
causality, driver-variant boundary, wiring, polarity, recreation behavior and every playfield
placement validated**

## Identity and evidence precedence

This is the Bally/Midway WPC-Security physical product, IPDB machine 2811 (model 50031, manufactured
from February 1994); its operations manual is document 16-50031-101 of May 1994. It covers the fourteen-driver `wcs_*` clone tree: `wcs_l2` (parent, production LX-2),
`wcs_l3c` (2016 community "Competition MOD" firmware), `wcs_la2`/`wcs_l1`/`wcs_la1` (earlier
language/region firmware), `wcs_d2` ("LED Ghost Fix"), `wcs_p2`/`wcs_p3` (prototypes),
`wcs_p5`/`wcs_p6` ("LED Ghost Fix" prototype-lineage firmware), and `wcs_f10`/`wcs_f50`/`wcs_f62`/
`wcs_f62b` (FreeWPC community reimplementations). Every one of these is a game-ROM revision for the
identical physical machine; `wcs.c`'s `CORE_GAMEDEF`/`CORE_CLONEDEF` share one static `wcsGameData`
struct across all fourteen.

Evidence precedence for this definition: the retained known-working VPW v1.5 script is runtime and
mechanism-causality ground truth; the Midway operations manual controls physical construction, part
numbers, wiring, polarity, quantities, device presence and location; pinned PinMAME controls
controller generation, public address topology, mechanism-table position ranges, and display metadata;
the retained VPX geometry supplies normalized coordinates where the manual's location drawings confirm
it (see Spatial evidence below). The retained manual PDF carries a genuine but
unreliable OCR text layer on its multi-column parts lists, so every printed table used here was read
from rendered pages and transcribed into
`external:pinmame-review-artifacts/world-cup-soccer/manual-transcription.md` and its per-table
excerpts under `evidence/excerpts/midway.world-cup-soccer.1994/`.

## Controller platform and address topology

`GEN_WPCSECURITY` (`PINMAME_HARDWARE_GEN_WPCSECURITY = 0x20`) with `wpc_dispDMD`. The controller
profile is `pinmame.wpc-security`, confirmed directly from `wcs.c`'s own `wcsGameData` declaration
rather than assumed from the task brief. Page 3 of the manual independently confirms the platform in
its own text: "This game uses a new Security CPU Board that is not downward compatible...".

- Switches: dedicated coin-door 1-8, matrix 11-88 as drive column then return row, Fliptronic
  111-118. `wcsGameData`'s inverted-switch mask `{0x00,0x00,0x00,0x3f,0x1f,0x07,0x00,0x00,0x00,
  0x00,0x00,0x00}` inverts column 3 in full (31-36), column 4 rows 1-5 (41-45), and column 5 rows
  1-3 (51-53) — fourteen addresses, exactly matching the printed matrix's own opto shading with
  **zero disagreement** in the ordinary 8x8 matrix. The mask's twelfth element (index 11, the
  Fliptronic column) is `0x00`, but that column is normalized by a different path: on every
  non-WPC-95 generation, `wpc.c`'s `WPC_FLIPPERS` register read returns the complement of the whole
  Fliptronic column. The printed opto positions F2/F4 (public 112/114) therefore read 1 when the
  button is pressed; see the Fliptronic section below.
- Solenoids: physical drivers 1-3, 5-6, 8-16 (all fitted, including 4 "Lock Release" and the
  backbox-mounted 7 "Knocker" — this machine genuinely has a knocker coil, unlike some other WPC-era
  games curated in this project); flashers/motors 17-28; Fliptronic upper-flipper circuits 33-35
  repurposed for Magna Goalie/Loop Gate/Lock Magnet, 36 unfitted; WPC-Security has **no** integrated
  LPDC board (unlike WPC-95/WPC-95DCS), so 37-44 are simply unused address space, not a duplicated
  range; Fliptronic lower-flipper circuits 45-48; PinMAME state channels 29-32 (31 never populated
  by this driver — see below); simulator-only 49 and reserved 50; a synthetic custom-solenoid mirror
  at 51 despite `wcsGameData` declaring `custSol = 0` — see below.
- Lamps: 8x8 matrix 11-88, every address populated (no "Not Used" lamp positions, unlike the switch
  matrix).
- GI: five strings on public addresses 0-4, three playfield (0, 1, 4) and two backbox insert-panel
  (2, 3).

Two WPC-Security numbering facts must not be lost. First, this generation's public solenoid
addresses for the lower flippers (45-48) match the manual's own printed circuit numbers exactly —
there is no LPDC remap to alias, unlike WPC-95. Second, `wcs.c` computes a genuinely dispatched
custom-solenoid address (public 51, `CORE_CUSTSOLNO(1)`) even though `wcsGameData` declares
`custSol = 0`: `core_getSol`'s `solNo > 50` branch calls `hw.getSol` unconditionally, regardless of
the declared count, and `wcs_getSol`'s own body returns `core_getSol(sDivHold) ||
core_getSol(sRampDiv)` — a live OR-combination readout of solenoids 16 and 8 with no physical
control line of its own. A recreation should bind one physical diverter mechanism to solenoids 8 and
16 and treat 51 as a derived diagnostic value, never a fourth device.

## Ball path, trough, and shooter

World Cup Soccer has a **manual** plunger: the manual's A-17730 Ball Shooter Assembly (printed 2-35)
is a knob on a rod with a power spring, no solenoid drives a launch, and there is no Launch Ball switch
in the matrix. `wcsSimData`'s `TRUE /* automatic plunger */` only tells PinMAME's own ball simulator to
launch by itself; an earlier pass misread it as hardware. Five balls rest on trough optos 31-35 (31
nearest the eject coil, 35 nearest the drain entrance), all printed opto and normalized by PinMAME's
inverted-switch mask. Solenoid 6 ejects the
ball on 31 toward the shooter lane; the retained script's `SolTrough` handler fires that kick and
pulses Trough Stack (36) in the same event. Pinned PinMAME's own internal ball-routing simulator
(`wcs_stateDef`, cited here only for switch/solenoid name cross-reference, never as physical
mechanism authority) places the `"Trough stack"` state immediately after the trough-eject state and
before the shooter-lane skill states, confirming switch 36 senses the ball's staging position toward
the shooter lane rather than a sixth ball resting in the trough — it has no dedicated VPX object of
any kind and is a documented projection onto the trough-eject `Kicker.sw31` position. The ejected
ball rests on shooter-lane switch 38 (Ball Shooter) until the player plunges it. The retained table
fires its `Plunger` object from the plunger key; its script also defines a `cvpmImpulseP` helper
(`SolAutofire`) that no `SolCallback` registers, so that helper is dead code. Three
printed optos then trip in sequence down the skill-shot lane — Front (51), Center (52), Rear (53) —
built from the identical LED/phototransistor construction (`A-16908`/`A-16909`) as the Goal/Goalie
hole optos on the "10-Switch Opto Assembly" board.

## The goalie: motorized figure, position optos, and target ring

A DC gearmotor (`A-17741` Goalie Unit Assembly) drives the goalie figure one-directionally,
reversing at each end of travel (`wcs_goalieMech`: `MECH_LINEAR|MECH_REVERSE|MECH_ONESOL`,
`WCS_GOALIETIME = 50`, `WCS_GOALIESLACK = 10`). `wcs_handleMech` sets public switches 43 (Goalie Is
Left) and 44 (Goalie Is Right) directly from the motor's position counter (`mech_getPos(0)`), but
**only while solenoid 21 is actively driving the motor** (`if ((mech & 0x01) && core_getSol
(sGoalieMot))`). Solenoid 21 is printed under the manual's "Flasher" type column with a "* +12VDC"
footnote rather than a normal flashlamp part number; this is a printed-table category quirk, not a
device conflict — `wcs.c`'s own `#define sGoalieMot 21` and the retained script's `SolGoalie`
handler (which plays `fx_goaliedrive`, a motor sound, not a flash effect) both independently confirm
the real function. The same pattern applies to solenoids 23/24 (the spinning-ball turntable motor,
below).

The retained VPW script does **not** read PinMAME's mechanism position at all: its own `UpdateGoalie`
routine runs an entirely independent sinusoidal position simulator (`GoalieTheta` incrementing every
frame) and asserts switches 43/44 directly from that simulation's own angle. Both switches are
therefore documented projections onto the goalie figure's own table object (`Primitive
BM_goalkeeper`) rather than fixed playfield sensors; the retained script's own `InitGoalie` sets
`BP_goalkeeper.x=376/.y=280`, matching this primitive's stored position (374.4, 281.5) almost
exactly, which is what confirms the projection target rather than an arbitrary nearby object.

The goalie's own 35-segment target-wall ring (`GoalieWalls`, retained-table objects `HitTarget.
GT006` through `GT040`) surrounds the figure; `GWalls_Hit` fires the shared handler and pulses
Goalie Target (48, part `A-17779`) whenever a ball strikes whichever single segment is currently
collidable, the same "rotating figure with a segmented hit ring" pattern already documented
elsewhere in this project for a different WPC machine's rotating antagonist figure. The Goalie Target
is the goalie figure itself, so switch 48 is a documented projection onto `BM_goalkeeper` too, where
the switch drawing's callout 48 also ends. An earlier pass had projected it onto the shooter-lane
plunger trigger, which has nothing to do with the goalie.

## The spinning soccer ball and the two magnets

A separate DC gearmotor turntable (`A-17569` Motor Assembly with an `A-16120` DC Motor Control
Assembly H-bridge driver board) spins a small soccer-ball toy under a plastic dome. `wcs_ballMech`
(`MECH_LINEAR|MECH_CIRCLE|MECH_TWODIRSOL`) models it as continuous two-direction rotation with no
discrete position switch; the retained script's `cvpmTurnTable` helper drives the visual spin
directly from solenoids 23 (clockwise) and 24 (counter-clockwise), both — like solenoid 21 above —
printed under the "Flasher" category with a "* +12VDC" footnote despite being motor drive lines.

Two independent playfield magnets complete the electromechanical inventory. Solenoid 33 (Magna
Goalie, `20-9247`) energizes a magnet (`cvpmMagnet` on the retained table's `MagnaGoalie` trigger,
strength 16, `GrabCenter = False`) that deflects rather than captures the ball, helping the player
save a shot that would otherwise drain. Solenoid 35 (Lock Magnet, also `20-9247`) energizes a second
magnet (`LockMagnet` trigger, strength 40, `GrabCenter = True` — genuinely halts the ball at the
magnet's center) that holds a locked ball for the multiball feature. Neither magnet has a dedicated
playfield switch; both are tracked purely in game software.

## Fliptronic circuits repurposed for Magna Goalie, Loop Gate, and Lock Magnet

World Cup Soccer has no upper flippers (`wcsGameData.hw.flippers = FLIP_SW(FLIP_L | FLIP_U) |
FLIP_SOL(FLIP_L)` — switches for all four flipper positions are read, but only the lower-flipper
solenoids are driven). The manual's own two tables on the same printed page (2-48) directly confirm
this by driver-transistor identity: solenoid 33 (Magna Goalie) shares `Q2`/`J902-6`/`Yel-Vio` with
the generic Flipper Circuits table's "Up Rt. Power" row; solenoid 34 (Loop Gate) shares `Q7`/
`J902-4`/`Org-Vio` with "Up Rt. Hold"; solenoid 35 (Lock Magnet) shares `Q1`/`J902-3`/`Yel-Gry` with
"Up Lt. Power". The fourth upper-flipper position, Up Lt. Hold (`Q5`), has no solenoid-table row at
all and is genuinely unfitted (public solenoid 36).

## The loop gate (solenoid 34)

The manual's two tables name solenoid 34 differently — "Loop Gate" on the Solenoid/Flasher Table
(matching `wcs.c`'s `#define sLoopGate 34`) and "Lock Gate" on the Solenoid/Flasher Locations list —
for the same coil (`A-14406`, low power) and assembly (`A-17796`). The Upper Playfield Parts list
(printed 2-40) calls `A-17796` the Ball Gate Actuator Coil Assy. (item 47) and lists beside it the
`A-17797-1` Ball Gate Special Assy., Left (item 48); its drawing (printed 2-41) puts both on the
bracket at the top of the right orbit, where the loop round the top of the playfield meets it, and
callout 34 on the solenoid drawing (printed 2-49) ends on the same bracket. The retained table models
a one-way gate there (`Gate003`), so the placement uses that object; its script never drives
solenoid 34, so the table's gate stays passive.

What the ROM does with it is settled by a hash-pinned harness run
(`runtime-scenario.wcs-loop-gate-travel`, scenario
`tools/harness-scenarios/wpc/wcs-loop-gate-travel.json`, `wcs_l2`, direct switch writes only). With
the Travel lamp (63) unlit, making the travel lane rollover (47) or the spinner (27) leaves 34 off.
Making both top rollovers (87, then 88) lights Travel; the next spinner or travel-lane closure then
energizes 34 within 16-32 ms and holds it for 3.5 s, and Travel goes out. The BMI rulesheet, a
secondary lead, describes the same shot from the player's side: with a city lit, the left spiral
sends the ball all the way round and out the other side; otherwise a one-way gate stops it and it
falls into the top rollovers and the jet bumpers. So a recreation should keep the gate closed (a ball
coming round the top drops into the top lanes) and open it for as long as the ROM holds solenoid 34.

## Ramp diverter and ramp lock post

Solenoid 8 (Ramp Diverter) swings a diverter flap (`A-18138`) and solenoid 16 (Diverter Hold) holds
it in the diverted position; the retained script swings the flap (`BM_diverterside01/02`, driven from
`DiverterFlipper001`'s angle) and toggles two collision walls. Both solenoids are placed on that flap,
where the shared callout of 8 and 16 ends on the solenoid drawing; an earlier pass had put them on
switch 71 at the left rail. Left Ramp
Diverted (71) is the printed switch for this mechanism. Solenoid 4 (Lock Release, fully fitted —
verified at 600 dpi after an initial mis-transcription, see the manual-transcription review
artifact) retracts a post (`A-18155`) that otherwise holds a ball on the left ramp, sensed by Lock
Mech. Low (76) and Lock Mech. High (77) — a *mechanical* ramp lock distinct from the magnetic Lock
Magnet feature above.

## Other toys and standard devices

A ball resting on opto 42 (Goal Popper Opto) is kicked by solenoid 1 to award a goal; Goal Trough
(41) senses a ball en route. A ball resting on opto 45 (TV Ball Popper) is kicked by solenoid 2.
Three ordinary VUK-style kickers cover the Upper/Left/Right Eject Holes (solenoids 5/15/14, switches
55/56/54) — `wcs.c`'s own `#define` names (`swLHole`/`swRHole`) additionally tie 56/54 to the
printed "Left/Right Free Kick Hole" feature, and the internal simulator calls 55 the "Assist Hole".
Three `A-9415-2` jet bumpers stand in a triangle at the upper right, named by absolute position:
Left (switch 81, coil 9, table object `Bumper3`), Upper (82, coil 10, `Bumper2`) and Lower (83, coil
11, `Bumper1`). Both location drawings put each switch and its coil on that bumper (the switch
drawing's 81/82/83 leaders and the solenoid drawing's 9/10/11 leaders), and a hash-pinned harness run
(`runtime-scenario.wcs-jet-bumper-coil-pairing`) shows the ROM firing 9, 10 and 11 within 63 ms of 81,
82 and 83 closing, alone and in two orders, each kick with Jet Bumpers flasher 20. The retained
table's script pulses the switches from rotated objects (`Bumper1_Hit` → 82, `Bumper2_Hit` → 81,
`Bumper3_Hit` → 83), and its own sound handler calls the lowest bumper "Top"; its bumpers kick by
themselves (no callback for 9-11), so the rotation is invisible in play, but a recreation should bind
each switch to the bumper named here. An earlier pass had copied the table's rotation into the
placements and recorded the question as an unresolved conflict; both drawings are legible at the
committed 300 dpi crops, and the conflict is withdrawn. Two slingshots (solenoids
12/13, score switches 84/85) each carry a direct-fire kick switch (`SW-1A-114`) and a separate
debounced score switch (`SW-1A-120`) wired to one public address; the table's Slingshot objects kick by
themselves. Tackle (65) is another `SW-1A-120` leaf switch, behind the rubber at the right side of the
left ramp entrance beside the Tackle lamp (38); the switch drawing draws that rubber but prints no
callout 65, so its placement keeps the table's script-bound trigger. A ball in the left outlane trips
Kickback (86); when lit, solenoid 3 fires the kickback plunger, and Kickback Upper (26) senses the
return path while also doubling, per PinMAME's own internal naming, as the Header Lane sensor for
the same physical lane.

## Fliptronic column: lower flippers

Two `FL-11629` (Blue) flippers on Fliptronic circuits 111-114 (lower right/left, EOS then
button-opto). The ROM energizes the power winding on the cabinet button opto (112 right, 114 left),
then drops to the hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes.
World Cup Soccer runs `Const UseSolenoids = 2` (fast flips). Fliptronic positions 115-118 are
printed Not Used on both the switch matrix and the switch-locations parts list; there are no upper
flippers.

The two cabinet buttons are genuine opto interrupters. The switch-matrix page shades F2/F4 (public
112/114) like the ordinary opto columns and prints them "Right/Left Flipper Opto", and the `A-17316`
board/assembly page confirms the construction (item 1 `03-9001 Interrupter Flip-Opto`; item 2
`A-16384 Flipper Opto Switch Assembly`, built from an "Opto Inter Lg. 10mA" component). The
switch-locations parts list's plainer "Lower Right/Left Flipper Cabinet" is a less specific label for
the same hardware.

Their public state is already normalized: 1 means the button is pressed, and a recreation must not
invert it again. `wcsGameData`'s inverted-switch mask leaves the Fliptronic column (index 11) at
`0x00`, which an earlier pass read as "not normalized". That reading was wrong. PinMAME normalizes
this column somewhere else: on `GEN_WPCSECURITY`, `wpc.c`'s `WPC_FLIPPERS` read returns
`~coreGlobals.swMatrix[CORE_FLIPPERSWCOL]`, the complement of the whole column, for every
generation outside `GENWPC_HASWPC95`. WPC-95 does the same through `WPC_FLIPPERSW95`. The
`pinmame.wpc-security` controller profile already says so.

A hash-pinned LibPinMAME harness run settles it at runtime
(`runtime-scenario.wcs-flipper-button-polarity`, scenario
`tools/harness-scenarios/wpc/wcs-flipper-button-polarity.json`, `wcs_l2`). It used direct switch
writes only, so keyboard handling and the simulator stayed off. During a running game, holding
public 112 at 1 pulses solenoid 45 for about 31 ms and holds 46; releasing it to 0 drops 46. Public
114 does the same on 47/48. No flipper output fires while both addresses idle at 0. The `wpc.vbs`
library the retained table loads (`vpm-script-library.wpc-vbs`, retained under the working root's
`review-artifacts/vpm-script-libs/`, SHA-256
`1a290886eb2c2fd2c13f82e5f8a1961fdc95238122096642d32fddf1cfbb1a8d`) agrees: it declares
`swLRFlip = 112` and `swLLFlip = 114` and sets `Controller.Switch(...) = True` on flipper key-down.

The shading does not make the contact normally closed. It marks opto construction only. Because
the ROM treats public 1 as pressed and reads this column complemented, the grounded Fliptronic input
the CPU sees closes only while a button is pressed, so both button contacts rest open and the
definition records `normally_closed: false` for 112 and 114, as it does for the two EOS leaf
switches.

## Lamps and general illumination

All 64 lamp-matrix addresses are populated; unlike the switch matrix, no lamp position is printed
Not Used. Five addresses carry two bulbs. Lamps 46 "Ultra Spinner" and 47 "Ultra Jets" have two
separate inserts each, with a distinct assembly for each bulb, and the retained table's two `Light`
objects sit at both. Lamps 71 "Light Jackpot" and 78 "Ultra Ramps" have one bulb on each of the two
ramp signs: the plastic signs standing at the left and right ramp entrances, each with three lamp
windows, top to bottom LIGHT JACKPOT (71, red), ULTRA RAMPS (78) and BUY TICKET (76 on the left sign,
77 on the right). The lamp drawing draws all six bulbs, and the IPDB and Pinside photographs show both
signs. The table's `Light` objects for these six bulbs sit at playfield height 0.04-0.08 away, as
light sources for its baked light maps, so the six placements are drawing measurements. Lamp 53
"Goal (2)" lights the kidney-shaped GOAL insert below the goal; the drawing marks the insert once, so
its two bulbs share one placement, and flasher 18's second bulb lights the same insert. Lamps 87 and 88 are the bulbs inside the illuminated
buy-in and start buttons; the retained table places both `Light` objects at normalized y > 1,
outside the playfield surface, independently confirming cabinet mounting.

General illumination splits three ways on the retained script's `GIUpdate2` dispatch, which
implements only `Case 0` (drives collection `GILeft`), `Case 1` (`GIRight`), and `Case 4` (`GITop`)
— with **no** `Case 2` or `Case 3` at all. This matches the manual's own wiring table exactly: GI
strings 0, 1, and 4 (printed 01, 02, 05) are the only three with a Playfield voltage/drive
connection printed; strings 2 and 3 ("Insert Background"/"Insert Title") are Backbox-only. Unlike
several other WPC-era games curated in this project, there is **zero** disagreement here between the
manual's physical wiring and the script's runtime implementation. Three `GITop` members (GI034,
GI035, GI036) sit at normalized y = -0.021148, just outside the playfield's 0..1 bounds near the top
rail; their y is clamped to the schema-valid boundary 0.000000 with the raw offset disclosed in the
spatial report, the same handling this project has already established for a small negative-offset
lamp row on a different WPC machine.

## Flashers

Each flasher's quantity counts the bulbs the Solenoid/Flasher Table prints in its playfield and
backbox columns, and only the playfield bulbs are placed; eight of them (17-20, 25-28) also light a
#906 in the backbox. Five have two playfield bulbs: Goal (18: a rear insert behind the goal and the
kidney GOAL insert), Skill Shot (19: by the shooter lane at the apron, and a dome on the right side
wall; the table's playfield column prints one #906, but the locations list and the drawing give two),
Spinning Ball (22: one bulb each side of the spinning ball), Flipper Lanes (27: one beside each inlane)
and Ramp Rear (28: the two top-corner domes). The locations list's "Goal Cage Top (2)" counts 17's one
playfield bulb and its backbox bulb. The Lock Area flasher (26) is a dome on the left
side wall beside the raised lock. Where the table models no lamp object at the drawn socket, or only a
baked-light-map source away from it (18's and 19's second bulbs, 26, 28's right dome), the coordinate is
a drawing measurement. Solenoids 21, 23 and 24 are motor drive lines printed under the Flasher column.

## Spatial evidence

Every placement is validated. The table placements were checked against all three factory location
drawings — lamps (printed 2-45), switches (2-47) and solenoids/flashers (2-49) — whose callouts an
independent reader transcribed from the page alone (`tools/seeds/midway/world-cup-soccer-1994-callouts.json`,
`tools/drawing_callouts.py`): each table placement's own callout lands within 0.07 normalized of it under
both the page's control fit (jet bumpers and flipper pivots; on the lamp drawing, which draws no jet
bumpers, flipper pivots and rollover buttons; on every page also the drawn playfield frame's top-left,
top-right and bottom-left corners, which match the table bounds, and, since the bottom-right corner is not
drawn, the ball shooter switch 38 slot at the foot of the shooter lane) and its callout fit. The curator refuses to build while any
checked placement disagrees. Projections (switches 36, 43, 44 and 48), the flipper coils (Not Shown) and
switch 65 (never numbered on the drawing) are outside the check, each with its reason in the seed. Twelve
sockets the table does not model where the drawing puts them are drawing measurements pinned in the same
seed: the six ramp-sign bulbs, flasher 26, the second bulbs of 18, 19 and 28, and ramp switches 74 and 75,
whose table triggers sit 0.09-0.11 from the switches the drawing marks. Every measured socket lies
inside the convex hull of its page's controls, so none is extrapolated. The physical photographs, or the
nearby table object, corroborate each measured device's identity, count and side; they supply no
coordinate (`evidence/excerpts/midway.world-cup-soccer.1994/physical-photo-corroboration.md`).

## Author construction checklist

- Build the five-ball trough with the drain at Trough Ball 5, the manual-plunger shooter lane,
  the three-opto skill shot, both slingshots, three jet bumpers, the motorized goalie with its
  35-segment target ring, the spinning-ball turntable, the two independent magnets (Magna Goalie
  deflect-only, Lock Magnet capture), the mechanical ramp lock post, the ramp diverter, the loop gate
  at the top of the right orbit, the Goal and TV poppers, the three eject holes, and the kickback.
- Bind the jet-bumper switches by absolute position (81 left, 82 upper, 83 lower), not by the
  retained table's rotated `Bumper1/2/3_Hit` bindings.
- Keep the loop gate closed and open it while solenoid 34 is on; the ROM holds it for 3.5 s after the
  left-spiral switches (27, 47) while Travel is lit.
- Preserve opto polarity for 31-36, 41-45, and 51-53; do not invert what PinMAME already normalizes.
  The cabinet flipper-button optos 112/114 are normalized too, through the `WPC_FLIPPERS` column
  complement rather than the inverted-switch mask: drive them 1 while the button is pressed.
- Bind every dedicated switch 1-8, every matrix position 11-88 including the printed Not Used
  positions, Fliptronic 111-118 with 115-118 not installed, the eight CPU DIP bits, solenoids 1-51
  (36 unfitted; 37-44 unpublished on this generation; 51 a diagnostic mirror only), lamps 11-88, GI
  0-4, and the 128x32 DMD.
- Solenoids 21, 23, and 24 are motor drive lines despite being printed under the manual's "Flasher"
  type column; do not model them as flash lamps.

## Sources

- `manual.midway.world-cup-soccer.1994`: Midway World Cup Soccer operations manual, SHA-256
  `29fd3c44c9ddcf5f965270011c71d34a701c13095cbeb286e26e62201931e48e`.
- `manual-support.midway.world-cup-soccer.1994`: retained human transcription index, SHA-256
  `7055d31403f69bedd4dffa94aad45952c18e75065941e204338eb9a818690f75`.
- `vpx-script.wcs-vpw-1-5`: retained known-working VPW v1.5 embedded script, SHA-256
  `c18cfbaa4e8c3b67259ac5d6c7b6842dfdaaf308b0fd71a64071118b57ac73c5`, binding `wcs_l2`.
- `vpx-table.wcs-vpw-1-5`: retained table, SHA-256
  `ab7e07fce7b589f9732f458a7a09ad08b87237852d97d7b5bf9a74f6b0f6d23d`, bounds
  `left=0 top=0 right=952.941 bottom=2152.941`.
- `pinmame.core.4ec52ff0ac13`: `src/wpc/sims/wpc/full/wcs.c` and the WPC-Security core/solenoid/
  flipper handling at PinMAME revision `4ec52ff0`. Up to the pinned `8371478a`, the only change to
  `src/wpc/wpc.c`, `core.c`, `core.h`, `wpc.h` and `wcs.c` is a comment in `core_findSize`.
- `runtime-scenario.wcs-flipper-button-polarity`: hash-pinned LibPinMAME harness run of `wcs_l2`
  with the pinned-revision library (SHA-256
  `deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c`); `run.json` SHA-256
  `efc84312331fcb4b976e7ca2c87791d12680d3746cd1d0259a5adc85ee696bb5`, run-folder manifest SHA-256
  `970d7cd7c648da33b244556e2d8ce23e18c0f4f6268cc3ca069645ad839a60d2`, scenario SHA-256
  `d6b2ef18479e7f464098a77b44b326c4a8841ae23087207d2182b41a13e59176`.
- `vpm-script-library.wpc-vbs`: the retained VPinMAME `wpc.vbs` library the table loads, SHA-256
  `1a290886eb2c2fd2c13f82e5f8a1961fdc95238122096642d32fddf1cfbb1a8d`.
- `runtime-scenario.wcs-jet-bumper-coil-pairing`: hash-pinned LibPinMAME harness run of `wcs_l2` with
  the library built from pinned PinMAME `97aa922b` (SHA-256
  `dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead`); `run.json` SHA-256
  `44f51681c3564109ed1133376c2cda6416996de9d18ae1d7f29d68aacdb06a7d`, run-folder manifest SHA-256
  `30b193a7fb12d88386616d34daf4a262fb425843d947985fc10450c80e6f217a`, scenario SHA-256
  `c2f0cbafc6d86c30b49d4ddf8257ae6f843c9ad626928be7c72992cddd681e61`.
- `runtime-scenario.wcs-loop-gate-travel`: the same library; `run.json` SHA-256
  `050e5baffdb669781db08c0ae9bdf6444a5f416e0677ec42082c7ca4c8177c4e`, run-folder manifest SHA-256
  `46e2396e5e24829e1dc03462d3ae0cf4f7b9c4d12e3a29f59e1b86f46727516a`, scenario SHA-256
  `7c4c5752f8017ecabbde99bad46a589b8a83c2ecf59a871fbc898f46878cb6ef`.
- `drawing-callouts.world-cup-soccer.2026-10-23`: the factory-drawing callout check and drawing
  measurements, `tools/seeds/midway/world-cup-soccer-1994-callouts.json`.
- `human-review.wcs-physical-corroboration-2026-10-23`: retained IPDB and Pinside photographs, folder
  manifest SHA-256 `5e9ba4932ae54593f7eb69c8689660d94ddd99a2b5a7ca7505a463ba7ef3e7a1`.
- Lead only: the BMI World Cup Soccer rulesheet,
  `https://www.bmigaming.com/Games/Rulesheets/world_cup_soccer.txt`, which also states the manual
  plunger.
