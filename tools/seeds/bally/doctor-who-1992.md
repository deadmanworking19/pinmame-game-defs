# Doctor Who (Bally, 1992)

Coverage: **partial - every I/O address, controller binding, polarity, wiring detail, mechanism and
recreation note is source-reconciled; only `spatial_placement` is missing, because the five
general-illumination strings' bulb positions rest on one community table and no retained drawing
locates them**

## Identity and evidence precedence

This is the Midway (trade name Bally) WPC-Fliptronic physical product released September 1992, model
20006, IPDB 738, 7,752 units. It covers the six `dw_*` drivers: `dw_l2` (production L-2, the parent),
`dw_d2` (community LED Ghost Fix of L-2), `dw_l1` (first production L-1), `dw_d1` (LED Ghost Fix of L-1),
and the prototypes `dw_p5` and `dw_p6`. All six share one `dwGameData` and run on the same
`wpc_mFliptronS` hardware. The L- and D- revisions are `identical` to the physical machine; the
prototypes are `compatible` and carry one caveat, below. The retained known-working VPW Mod v1.1 script
binds `dw_l2` directly (`Const cGameName = "dw_l2"`), the production parent.

Evidence precedence for this definition: the retained known-working script is runtime and
mechanism-causality ground truth; the operations manual (an image-only scan with no schematics), the
amendment and the Handy Technician's Chart control physical construction, part numbers, wiring and
device presence; pinned PinMAME controls controller generation and public address topology; the ROM's own
service tests, run on a legal L-2 ROM, settled the polarity and the names the ROM prints; the retained
table supplies coordinates. The manual's tables were read from rendered pages, never from OCR text, and
every table used is transcribed under `evidence/excerpts/bally.doctor-who.1992/`.

**Prototype hardware this definition does not declare.** IPDB's notes record that a dozen sample machines
and about a hundred prototypes had a motor-driven Dalek head in the backbox topper with a front-facing opto,
and that production dropped the motor and opto while leaving "the wiring and software" in place. No retained
source says which public addresses that hardware used. A prototype ROM (`dw_p5`, `dw_p6`) or an owner's
retrofit may therefore drive hardware this record does not list. The production machine's Dalek head is
stationary and lit by the Backbox Head flasher (solenoid 14).

## Controller platform and address topology

The controller profile is `pinmame.wpc-fliptronic` (hardware generation `0x8`, 128x32 dot-matrix display).
Public addresses:

- **Switches 1-8**: the coin-door grounded switches (three coin chutes, an optional fourth, and the four
  service buttons Escape, Down, Up and Enter).
- **Switch matrix 11-88**: the 8x8 matrix. Position 24 is a constant (Always Closed, the same part as the
  Coin Door Closed switch at 22). Positions 11, 12, 23, 81 and 83-87 are `Not Used`; 23 prints a vestigial
  'Ticket Opto' label with nothing fitted.
- **Fliptronic grounded switches 111-118**: F1-F8. F1, F3 and F7 are flipper end-of-stroke switches, F2, F4
  and F8 the cabinet flipper opto buttons. F5 and F6 (an upper-right flipper) are not fitted.
- **Solenoids 1-28** are the driver board's coils and flashers; **35/36, 45/46 and 47/48** are the Fliptronic
  flipper power/hold windings (upper left, lower right, lower left) and 33/34 the unfitted upper-right pair;
  **29-31** mirror bits 5-7 of `WPC_GILAMPS` because the driver sets no fast-flip address; 32, 37-44 and 50 are
  unused space and 49 is PinMAME's simulator ball shooter.
- **Lamps 11-88** are the 64-position lamp matrix, all assigned. **GI 0-4** are the five general-illumination
  strings.

Every dedicated, matrix and flipper address is declared exactly once, with stable `switch.matrix-N` ids.

## Switch polarity: what the ROM's own switch-edges test settled

PinMAME inverts public 31, 32, 33, 71-77 (and the unoccupied 81) through `dwGameData`'s inverted-switch mask
`{0x00,0x00,0x00,0x07,0x00,0x00,0x00,0x7f,0x01,...}`; index 3 is matrix column 3 under `wpc_sw2m`, index 7
is column 7 and index 8 column 8, so the mask covers the Opto Popper, the home opto and the ramp-entry opto (31-33) and the
five-bank and eject optos (71-77). The retained run `evidence/runtime/wpc-fliptronic/doctor-who-dw_l2-switch-edges.json`
drove each of them 1, 0, 1 through T.1 SWITCH EDGES; the ROM's top line names a switch while it reads it as active.

- **31, 33 and 71-77** are named at public 1 and cleared at 0. Through the mask public 1 is an open matrix
  contact, so the ROM reads these optos as active with the beam broken, matching the manual's opto theory
  ("an opto is the opposite and is active when the beam is broken, making the switch 'open'"), and
  `normally_closed` is `true`.
- **32 (Mini-playfield Home Opto) is the exception.** The ROM names it at public 0 and clears the name at 1,
  the other way round. Through the mask public 0 is a closed contact, so the ROM reads the home opto as active
  while its contact is closed. It is `normally_closed: false`; a consumer drives it as the retained script's
  `UpdateMiniPF` does, with raw `Controller.Switch(32)` levels, and does not invert it again. The Handy chart still
  shades 32 as an opto: the shading marks the construction, not the ROM's active level.
- **41, 47, 57, 68, 78, 82, 88 and 38** read active at public 1 like any ordinary switch.
- **Flipper buttons 112 and 114 (and 118)** are `normally_closed: false`: PinMAME's Fliptronic read returns the
  complement of the switch column, so public 1 is the pressed button. Setting 112 or 114 to 1 made the ROM fire the
  flipper, and its synthesized end-of-stroke bit rose on F1 or F3. End-of-stroke addresses carry PinMAME's
  synthetic state, not a measurement of the leaf switch.

The ROM-printed names are literal: `<E>S-C-A-P-E`, `Mini. Lites Lock`, `Trap Door. Down`, `Hangon Score`,
`Playfield Glass`, `Mini. Door. Left/Right/Mid`, `Opto Popper`, `Mini. Home Opto`, `Enter T.Ramp Opto`,
`Mini.Opto.5Bank R1/R2/M/L2/L1`, `Mini. L. OptoEject`, `Mini. R. OptoEject`.

## The Time Expander mini-playfield (headline mechanism)

A second playfield at the top of the machine rides on a motor-driven cam and moves between three levels (IPDB
counts them from the bottom):

| Level | Position | What is reachable |
| --- | --- | --- |
| 1 | lowest | the left and right lock holes (switches 76 and 77) and the Lites Lock target (78) |
| 2 | middle | the five round white dalek buttons (71-75) |
| 3 | upper | the three flyaway doors (68 left, 38 middle, 88 right) |

- **Motor.** A 20 V DC motor (14-7970) in the A-15634 Motor & Cam Assembly turns the cam. The Bi-directional Motor
  Drive board A-15680 takes two logic lines: solenoid 28 (printed "Mini-playfield On/Off") runs the motor and solenoid
  27 (printed "C.C.W./C.W.") selects the direction. The T.14 run (`...-mini-playfield-test.json`) shows the ROM drive 28
  alone for the clockwise "CW MidL" move, report an error after a second because nothing answers (built-in mechanisms
  were off), and then drive 27 together with 28 for the counter-clockwise "CCW Down" move. The board's own page
  prints the wire colours on its input pins crossed against the connector list; both readings are on the output notes.
- **Position feedback.** Only the Home Opto (32) is a position sensor. The manual describes it only as the home sensor;
  the table's windows for it (`UpdateMiniPF`, 360 steps over a 270-step length) are the table author's, not
  measurements. No retained source documents the real cam position profile.
- **Safety interlock.** In play and attract the mini-playfield does not move unless the coin door is closed and the
  playfield glass is on (switches 22 and 82 closed); in T.14 both flipper buttons must be held.
- **Lock holes.** Two Ball Popper Assemblies (A-15358-1 left, A-15358 right) each hold a ball over an LED/photo-transistor
  pair; solenoids 4 and 5 eject them and the T.14 L Kicker and R Kicker sub-tests pulse them. Ejected balls should hit the
  lower flippers (the playfield-adjustment page gives the adjustment).
- **Dalek buttons and doors.** The five buttons are the A-15500 5-Target Assembly, each read by an infrared opto (A-15431
  receivers, A-15432 emitters). The manual's removal instructions refer to a "flip-up target reset lever" that the Door
  Release Bracket bears on "so that the targets drop"; no coil is listed for them. The A-15356 3-Door Assembly's three doors
  time-warp the Daleks during multiball.
- **Lamps and flasher.** Lamps 56-58 (left lock, right lock, target) and the Doctor 7 flasher (solenoid 17, under the
  A-15582 cover) travel with the mini-playfield, so a playfield coordinate describes the lowest-level position only.
- **Rules.** Hit the middle target to light locks, lock two balls to reveal the controls (level 2), restore Earth time to
  factor 0 by lighting all 15 control-panel lamps, then shoot any door to start multiball. During multiball each door
  time-warps a Dalek (Emperor 50 million down to Daleks 5-20 million); after all ranks Davros appears behind a force field
  that the five dalek buttons drop, and he is time-warped through the doors for the Super Jackpot.
- **Service.** T.14 runs eleven sub-tests; the retained run walked "CW MidL", "CCW Down", "L Kicker", "R Kicker", "Flasher",
  "CCW MidR" and "CCW Up" and stopped after its second fault. The sequence is timing-dependent: reruns that stopped after two
  faults never reached the kicker sub-tests, so the retained run, not the scenario, is the evidence. Amendment 16-9453 adds a
  cant correction for the guide bearings and two adjustments (A.2 54 Kick Lock Holes, A.2 55 Game Start Doctor).

## Other mechanisms

- **Trap door** (solenoid 1, switch 57 Trap Door Down; A-15641): a flap driven by a plunger coil through a cam and gate. The
  T.13 test cycles it with a pull-in and a hold-in phase and a COOLING state. The game lowers it every tenth loop (Sonic
  Boom). The retained script sets 57 when the primitive reaches its raised end and clears it when lowered.
- **Tardis popper** (solenoid 3, opto 31; A-15440): the ball rests on the opto beam and is kicked out by the coil; the script
  clears 31 only from solenoid 3's callback.
- **Outhole and trough** (switch 28 outhole, 25/26/27 for one to three balls, solenoids 15 and 16): a drained ball is kicked
  into the trough by 15 and 16 releases one toward the shooter lane. The machine plays with three balls.
- **Shooter lane**: no manual plunger. The Launch Ball button (34, lamp 87) asks the ROM to fire the Ball Shooter Lane Feeder
  (solenoid 2) while a ball rests on switch 17.
- **Flippers**: three. The lower pair are Fliptronic II assemblies A-15205-R-4 and A-15205-L-4 and the upper-left one is
  A-16090-L-4, each with a SW-1A-193 end-of-stroke leaf switch and an FL-15411 coil. There is no upper-right flipper although
  `dwGameData` declares `FLIP_SW(FLIP_L|FLIP_U)`, which makes PinMAME synthesize an upper-right switch pair and winding
  positions; none of that is fitted. The two lower flippers are slightly shorter than Williams' standard ones.
- **Ramps**: the manual names switches 33/35 'Enter Top Ramp Opto' and 'Score Top Ramp' and 36/37 'Enter Bottom Ramp' and
  'Score Bottom Ramp'; its rules call the top ramp the cliffhanger ramp and build the playfield multiplier from it. The
  Hang On Score is lit by the right return lane and collected by the W-H-O shot (H); the switch list names 47 'Hang On Score'
  and 48 'Select Doctor' without saying which playfield features they are.
- **Slingshots, jets and targets**: slings 15/16 with coils 9/10; jet bumpers 61/62/63 with coils 11/12/13 (the ROM counts hits
  per bumper and reports "Examine ... Jet Bumper Switch"); the six ESCAPE standups (41-46) and six REPAIR standups (51-56); the
  Transmat Award target (58).

## Lamps, flashers and general illumination

- All 64 lamp-matrix positions carry a description; none is printed "Not Used". Doctor 1-7 (lamps 48, 36, 82, 71, 67, 72 and
  23) and the Ball Transmat / Advance Bonus X lamp (86) carry two bulbs; the Doctor lamps' second bulb is on the speaker panel
  (the back panel for Doctor 5), so only the playfield bulb is placed. Lamps 87 and 88 are the lit Launch Ball and Game Start
  cabinet buttons.
- Flashers: 6 (2nd Chance Logo, count 4), 8 (Doctor 3, backbox only), 14 (Backbox Head, backbox only), 17 (Doctor 7 under the
  mini-playfield cover), 18 and 19 (5x3 left and right), 20 (jet bumpers and Doctor 5, count 2, two bulbs measured on the drawing), 21 (REPAIR and Doctor 4,
  count 2), 22 (W-(H)-O and Doctor 2), 23 (W-H-(O) and Doctor 6), 24 (ESCAPE and Doctor 1). The ROM's T.5 FLASHER TEST pulses
  6, 8, 14 and 17-24 and its T.4 SOLENOID TEST names the coils in `...-solenoid-test.json`.
- GI: five strings. Strings 1 and 2 (Insert, back panel top and bottom) are backbox illumination; strings 3, 4 and 5 feed the
  playfield and the insert panel (string 5 also the coin door). The Handy chart places the J121 pins under "Playfield" and
  prints no insert column for these strings, which disagrees with the Power Driver Board connector list; the manual's table
  and connector list are followed.

## Spatial status and why the record stays partial

Coordinates are x/952.965 and y/2162 of the retained table (rear y=0, apron y=1). The factory location drawings (PDF 118, 119
and 120) were read callout by callout and fitted to the table's own jet bumpers and lower-flipper pivots; a table placement
whose own callout lands within 0.07 normalized is `validated`, which is 119 of the 122 placements checked. The rest stay
`observed`: switches 26, 27 and 36 (callouts beyond the limit); switch 46, whose balloon is printed but whose leader merges into the rail
linework and cannot be followed (the reader's best guess lies about 0.015 from the table placement, which is not a reading); the six
flipper windings (the drawing prints no balloon for a winding); the motor lines 27 and 28 and the Home Opto 32 (measured on the drawing
itself, because the table models them in software); lamp 67 (no table Light; measured on the drawing); flasher 20's two bulbs (the
table's FL20 is a single invisible Flasher sprite, not a socket, so both are measured at the two prong tips of the drawing's callout 20,
about 0.04 accurate, with y clamped to the top edge); the dalek buttons 71-75 and doors 38, 68 and 88 (drawn only on the front-view inset);
and the three playfield GI strings. The GI bulbs cannot be validated at all: the manual prints no per-string bulb count and no drawing locates
a GI bulb, so the table's own grouping is the only source. That single dimension is the whole of
`coverage.missing`.

## Author construction checklist

1. Build the three-level mini-playfield first; it has the most devices. Drive it from solenoids 28 (run) and 27 (direction) and
   feed switch 32 as raw `Controller.Switch(32)` levels without inverting it.
2. Leave PinMAME's own inversion of the optos 31, 33 and 71-77 alone; do not invert them again.
3. Treat 111, 113 and 117 as PinMAME-synthesized end-of-stroke bits, not contacts you must feed.
4. The Launch Ball button (34) starts the shooter; there is no plunger.
5. Leave out the upper-right flipper and any Dalek-head motor unless you are recreating a prototype.
6. Keep the safety interlock (coin door and glass closed) before the mini-playfield moves in normal play.

## Sources

The operations manual (IPDB 738, retained as an image-only scan), the Handy Technician's Chart, Manual Amendment 16-9453, the
IPDB page, pinned PinMAME `8371478a`, the retained VPW Mod v1.1 table and script, and four hash-pinned LibPinMAME harness runs of
`dw_l2` (T.1 switch edges, T.4 solenoid test, T.5 flasher test, T.14 mini-playfield test). The curator is
`tools/curate_doctor_who.py`; the compact runtime evidence for three of the runs is built by `tools/doctor_who_runtime_evidence.py`.

## Procedural note

`coverage.missing` is `["spatial_placement"]` and the record remains `partial`: a retained drawing that locates the GI bulbs, or a
per-string bulb count, would let the three playfield GI strings be validated and the record promoted. Wiring-detail
disagreements between the manual's pages (connector pins and wire colours that differ between the Solenoid/Flasher Table, the
Handy chart and the connector list) are kept literally in the excerpts and stated on the affected device notes; none changes a
device, its address or its fitment, so the record opens no conflict.
