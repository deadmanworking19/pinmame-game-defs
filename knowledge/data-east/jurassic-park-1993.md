# Jurassic Park (Data East, 1993)

This definition describes the production machine (IPDB 1343, model 500-5520-01, DataEast/Sega Version 3 CPU board, 128x32 dot-matrix
display, DE2S sound) and all six pinned drivers: the production 5.13 set and its 3.05, 3.07, 5.01, German 5.01 and unofficial 6.00
siblings, which share one game-data declaration and one wiring. It is partial: the I/O contract, names, wiring, polarity, mechanisms and
runtime behaviour are enumerated and evidenced; the fitted GI sockets, the raw printer bits and the validation of every spatial placement
are not.

## What the ROM itself proves

The ROM's service menus name every switch, lamp and coil, so these runs (fresh empty CMOS, pinned LibPinMAME, jupk_513) are the strongest
naming evidence here. The Active Switch Test names every matrix switch 1-62 while the host holds it at public 1, with its wire colours and
number, and the host flipper buttons 82/84 appear as LEFT/RIGHT FLIPPER 63/64 and produce the synthetic outputs 47/48 and 45/46. The
single-lamp test lights one lamp per Start press and prints its name, colours and number for all 64 lamps. The CYCLING COILS test names and
pulses coils 1-9, 11-13 and 16-22 and flash banks 25-32 (14 and 15 are named but not pulsed). The T-REX TEST turns ON TOP, BOTTOM, CENTER, RIGHT and
LEFT SWITCH for public 57, 58, 36, 31 and 32 and moves the creature from the flipper and Start buttons. The Laser Kick Test fires 9, 4, 7, 1 and 5
when 29, 35, 55, 56 and 61 close. Switch 62 and the other Not Used addresses are named NOT USED by the ROM, and the matrix is read uncomplemented:
public 1 is the active closure.

## Printed names the ROM corrects

The manual's lamp matrix prints a bare "Map" at 6 (the ROM: BARYONYX - MAP), "#2" at 50 (GALLIMIMUS), a "C" arch at 48 (ARCH "E", completing the
T-R-E-X arch letters 2, 47, 48, 60), "Raptor Multi-Million" at 20 (the ROM and the artwork say Mosquito Multi Millions, the game's Mosquito Millions
round) and "Jackpot Map" at 30 (JACKPOT RAMP, beside Jackpot Loop at 29). The matrix also prints "Smart Bomb" where the ROM says Smart Missile at 42 and 64 and
"Right Saucer Eject" where the ROM says TOP RIGHT EJECT at 56. The retained legacy definition mislabelled 9 as Drain, numbered the trough backwards, called 15 a
shooter-lane lockout, called 37 a scoop trough and gave 52 the Gallimimus name; the stable IDs are kept for compatibility but the labels follow the factory and the ROM.
Legacy lamp numbers 100-128 appear to be script-side SetLamp helper numbers, not controller lamps (the PinMAME lamp range here is 1-64).

## Switches, lamps and outputs

The 64-address Data East matrix is column-major (public n = 8 x (column - 1) + row), CPU connectors CN8 (strobes, with a key at 6) and CN10 (returns,
key at 4). Cabinet switches 1-7 are the coin-door and front-panel column, and the game has no ball-roll tilt. Six trough switches 9-14 hold six balls and 15 is a real seventh
contact at the release position; the table starts 9-14 closed. 41 and 42 are the shooter gun's trigger and smart-missile button and are not on the playfield. 63 and 64 are
read-only copies of the host buttons 84 and 82, which a consumer must drive instead. The upper right flipper shares the right button and has no ROM output, EOS or button.

Outputs 1-9 are left-set coils and 25-32 their right-set flash banks: drives 1-8 share transistors and the PPB left/right relay (public 10) routes
them. Each right-set bank draws four bulbs; the manual's printed bulb text, the ROM's own names (4-ORBIT, 3-POPS 1-TREX, TOP RGT. RMP 1.3.5) and the
table agree on where they are, except that the ROM counts one raptor-pit bulb fewer than the schematic in bank 1R. Only their playfield bulbs are placed. Output 11 is a physical general-illumination relay (K-1): asserting it cuts GI, although
PinMAME models it as a reversed #44 6.3 VAC brightness output. The manual fuses four 6.3 VAC GI strings (F1 Playfield, F2 Backbox Door & Speaker Panel, F3 Playfield
& Coin Door, F4 Backbox Door) but gives no socket count. Outputs 12-15 are the T-Rex direction and motor relays and 13 the jaw coil; 16 is the trough lock-out; 17-21 the turbo
bumpers and slingshots, and 22 the cabinet shaker. Output 23 is the game-on / switched-solenoid enable, 24, 33-36 and 50 dead addresses, 45-48 PinMAME's synthetic flipper
states (only while 23 is on), 49 the shared simulator output and 51-64 return zero. The raw printer bits 37-44 are published but never observed and the manual documents no printer.

Lamps 1-64 are all fitted. The credit button lamp (9) is in the cabinet; 1, 10, 19, 28, 46, 55 and 64 print (2 Bulbs); 31, 32 and 62 are the turbo-bumper bulbs; 41-45 spell CHAOS.
The retained table lights 31, 32 and 62 from the bumper solenoids as an effect, drives lamps through Controller.ChangedLamps with nFadeL/nFadeLm twins for glow, and models only a coloured
glow for the left, center and right scoop and gate lamps (17, 18, 33, 34, 57, 58, 46), which therefore have no placement.

## Recreation notes

The retained Dark & Friends 1.03 table starts the T-Rex homed (36 and 57 closed) and the trough with six balls, ties 23 to its nudge logic, drives the flippers from the synthetic outputs
46 and 48 (sLRFlipper, sLLFlipper) and simulates the toy's switches from the up/down and rotation motor outputs. The ROM's power-up T-Rex diagnostic needs that: with 36 and 57 closed it runs 14, 15, 13 and 12 and goes on, with them open it drives 14 for about
3.4 s and starts nothing else. A recreation must therefore present the dinosaur's position switches to the ROM, not just move a model.

## Six-ball trough, lock-out and release

Six balls rest on the trough switches 9-14 and the seventh contact, 15, is the staged release position. The 6 Ball Outhole-Trough assembly (printed page 71) pairs a switch assembly 500-5683-00 with a Lock Ball Assembly 500-5684-00: coil 16 (25-1240) pulls the lock ball plunger to let one ball from the stack onto the release position, and coil 2 ejects that ball to the shooter lane. The retained table starts 9-14 closed with six balls, moves one ball to 15 on every TroughLockout and kicks it out on TroughRelease. The ROM's ball search and missing-ball handling were not exercised.

## Shooter lane and auto launch

Coil 3 (50 V, Ball Launch assembly 500-5477-00, coil 23-800) kicks the ball up the right shooter lane; switch 16 senses a ball at the foot of the lane. The retained table's Autofire fires its Plunger1 on the coil. The launch trigger (41) belongs to the gun, not to this lane.

## Shooter gun (launch trigger and smart-bomb button)

The cabinet's Shooter Gun Assy (cabinet parts item 1, 500-5673-00): a trigger switch (180-5111-00, ROM LAUNCH BUTTON) used for the skill shot and for stunning dinosaurs, and a smart-bomb button (515-5825-00, ROM SMART MISSILE) usable once per game. The retained table maps both to host keys. In the ROM's T-REX TEST the trigger pulses the jaw coil (13).

## T-Rex dinosaur (rotation, bend and jaw)

Dino Assembly (printed page 70, 500-5667-00): a rotation motor (BOM item 1: 5 VDC motor; the coil schematic prints a 9 VDC motor behind bi-directional relay board 520-5066-00), a Bowman 11 RPM 24 VAC motor for the up/down bend (item 19, relay board 520-5010-00), a jaw coil 25-1240, four micro switches 180-5040-00 and a roller micro switch 180-5123-00. Public 12 selects the rotation direction, 15 switches the rotation motor and 14 the up/down motor. Switches: 57 TOP (up), 58 BOTTOM (down), 36 CENTER (rotation), 31 RIGHT and 32 LEFT, displayed by the ROM's T-REX TEST as ON when held at public 1. The manual's T-Rex test says Top must be ON to move left and right and Center ON to move up and down. The ROM runs a power-up T-Rex diagnostic: with 36 and 57 closed it drives 14 for about 3 s, then pulses 15, the jaw 13 and the direction relay 12; with them open it drives 14 for about 3.4 s and starts nothing else. In the T-REX TEST (57 held closed) the left flipper button pulses 15 alone, the right button latches 12 and pulses 15, Start pulses 14 (with or without 36 closed) and the launch trigger pulses 13; the ROM did not wait for 36 before moving up and down in this run. The retained table integrates positions from the motor outputs: 57 is closed when the head is raised, 58 when bent forward, 31 and 32 at the rotation limits (-23 and -3 degrees) and 36 near -13; it starts homed with 36 and 57 closed. Those thresholds are the table's model, not measured contact positions.

## T-Rex saucer (dino eject)

Ball Eject Assy (Dino) 500-5665-00 with coil 27-1500 (090-5004-02). Coil 7 (ROM T-REX EJECT) ejects the ball held on switch 55; the ROM's Laser Kick Test fires it when 55 closes. In the rules the dinosaur 'eats' the ball here to score Feed T-Rex. The retained table lets the bending T-Rex pick the ball up from 55 and release it at the top, which is its own animation of that feature.

## Double scoop (left scoop and center scoop)

Double Scoop Sub-Assembly 515-5772-00 with coil 23-800 and micro switch 180-5116-00; the playfield major-assembly drawing shows two of them, at the left scoop and beside the center scoop. Coil 4 ejects the ball held in the left scoop, switch 35 (the Laser Kick Test fires 4 when 35 closes). The center scoop's switch 37 (ROM MIDDLE SCOOP, part 500-5442-01) fires no coil in the Laser Kick Test and the retained table treats it as a gravity path.

## Top right eject (boat dock)

Ball Eject Assy (Saucer) 500-5664-00, coil 24-940 (090-5636-02); ROM TOP RGT EJECT. The Laser Kick Test fires it when switch 56 closes. The rules light it for Two Ball Play, Lite Extra Ball and the Escape Isla Nublar boat dock.

## Right vertical up-kicker

Super VUK 500-5116-04 with coil 23-800 (090-5001-01) and micro switch 180-5064-00 (the ROM calls the coil RIGHT VUK 50V and the schematic wires it at the 50 V J7 connector). The Laser Kick Test fires it, twice, when 61 closes.

## Raptor pit kicker

Kickback Assy 500-5081-00 (coil 23-800 per its unique-parts page) is the raptor pit's kicker: a 50 V coil (ROM RAPTOR PIT 50V, schematic type 23-840, drive 9 through board transistor Q4) that kicks the ball out of the raptor pit sensed by switch 29. The ROM's Laser Kick Test ('put ball in raptors') fires it when 29 closes. The rules mention a ball-freeze protector that kicks while the danger lamp is on.

## Right ramp and diverter

Diverter Plunger & Crank Arm Assembly 500-5661-00 (coil 27-1500, 090-5004-02) with the 515-5781-00 diverter arm steers balls at the right ramp, whose enter (33) and exit (34) switches count shots. The retained table drops the diverter's collision wall and rotates its arm while the coil is on. The ramp switches report ball passage, not diverter position; no home or limit sensor is fitted in the switch chart.

## Gravity scoop exits (T-Rex trough and right scoop)

Switches 59 (T.Rex Trough) and 60 (Right Scoop Trough), both part 180-5057-00, sit in exit paths. Closing either in the Laser Kick Test fired no coil, and the retained table only pulses them as a ball passes.

## Mosquito captive ball

One captive ball rests in front of the mosquito target; switch 48 (180-5114-08) scores each hit and the rules crack a dinosaur egg (lamp 61) with every shot, with MOSQUITO MILLIONS lighting the target. The retained table models it as a kicker (Captive) plus a hit target.

## Top turbo bumper

Turbo Bumper assembly 500-5227-00: skirt switch 180-5015-01 closes on impact and the ROM drives coil 17 (23-800, 090-5001-00). Its bulb is lamp 31.

## Left turbo bumper

As the top bumper: switch 46, coil 18, lamp 62.

## Right turbo bumper

As the top bumper: switch 47, coil 19, lamp 32.

## Left slingshot

Slingshot Assembly 500-5226-00: two slingshot switches 180-5054-00 behind the rubber close the matrix circuit 43 and the ROM drives coil 20 (23-800, 090-5001-02).

## Right slingshot

As the left slingshot: switch 44, coil 21.

## Cabinet knocker

The knocker coil of Kickback & Knocker assembly 500-5081-00 (23-800, 090-5001-01) strikes the cabinet stop; the ROM's cycle test names it KNOCKER. It has no sensor and no playfield emitter.

## Cabinet shaker motor

Shaker Motor Assy 500-5228-00 on motor board 520-5065-00, driven by coil output 22 (ROM SHAKER MOTOR). The retained table plays a motor sound and leaves its nudge effect commented out.

## Lower left flipper

Cabinet-wired flipper, coil 090-5020-30 (23-900): the left button's circuit (ORN-GRY, CPU CN19-2) fires it directly through the solid-state flipper board, which takes 50 VDC and 8 VAC. The ROM never drives a flipper coil: output 23 enables PinMAME's synthetic 47/48 from host button 84, which the table's SolLFlipper follows through 48. The flipper's own leaf switch (180-5048-01) is the cabinet button; its matrix copy is 63. The unique-parts page prints flipper assemblies 500-5693-02 (left, uses switch 180-5124-00), 500-5693-01 (right) and 500-5694-01 (upper right), the major-assembly list 500-5606-78/77/79; both numberings are kept.

## Lower right flipper

As the lower left flipper with the right button (ORN-VIO, CPU CN19-1, leaf switch 180-5022-00 in the switch list and 180-5122-00 as cabinet part 15a) and public 45/46, 82 and 64.

## Upper right flipper

Third flipper, coil 090-5041-00 (25-1800, BLK-YEL at flipper board CN2-1,2; the unique-parts page prints '500-5694-01 Upper Right (uses coil 090-5030-00)' instead, and both readings are kept), operated from the same right button and the same CPU CN19-1 line as the lower right flipper (its flip-board switch input is GRY-VIO at CN1-12). No separate ROM output, EOS or button exists, and the retained table moves it with the lower right flipper.

## Evidence and remaining work

Factory transcriptions and crops: evidence/excerpts/data-east/jurassic-park-1993/. Exact object locators and hashes: tools/jurassic_park_geometry.json. Runtime readings, hashes and expected transitions: tools/jurassic_park_runtime.json, with the reusable scenarios tools/harness-scenarios/data-east/jupk-513-*.json and the DMD title adapter tools/jurassic_park_harness.py. Complete originals, extraction manifests, ROM inventory, fresh-state traces and native renders remain under the external working root. Remaining: the fitted GI sockets; the raw printer bits; a callout check or second table to validate the placements; the seven trough contacts' positions.
