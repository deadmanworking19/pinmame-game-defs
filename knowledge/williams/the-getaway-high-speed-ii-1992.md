# Williams The Getaway: High Speed II (1992)

Sequel to Williams High Speed (1986, a different physical machine on an earlier, unrelated
electromechanical/System-6 platform, and out of scope for this record). The Getaway: High Speed II
runs on WPC-Fliptronic hardware (`GEN_WPCFLIPTRON`, pinned `src/wpc/sims/wpc/full/gw.c`) with a
128x32 dot-matrix display, one lower flipper pair, and a single upper-right flipper feeding a
motorized "Supercharger" accelerator loop.

## A note on the pinned driver's own reliability

`gw.c`'s header comment is explicit: its author, Steve Ellenoff, states he did not have access to the
physical machine and "guessed most of it from a Playfield picture and the rulesheet." This matters for
curation because it means the driver's `#define` comment labels (`swOpto1`, `sRSling`, and so on) are
not automatically trustworthy device-identity ground truth the way they are on most other curated WPC
titles, even though the driver's numeric public addresses (ordinary WPC column-times-ten-plus-row
matrix notation) are still real hardware. Two corrections came out of checking the labels against
other sources, and they run in opposite directions:

- Solenoids 5 and 6 are reversed in the driver's comments (`sRSling 5`, `sLSling 6`) against two
  independently-agreeing manual pages (Solenoid/Flasher Locations and the Solenoid Table wiring page),
  both of which print item 5 as "Left Slingshot" and item 6 as "Right Slingshot." The manual wins; see
  `device.left-slingshot`/`device.right-slingshot` in the definition.
- Switches 84 and 85 are the other way round: the manual's Switch Locations and SWITCH MATRIX pages
  label 84 "Opto Made Loop" and 85 "Enter Left Ramp," but the ROM's own switch test names 84 ENTER
  LEFT RAMP and 85 OPTO MADE LOOP, as the driver's guessed labels and the retained known-working
  script do. Here the driver is right and the manual has the two names transposed; see below.

## The Supercharger accelerator loop

The machine's signature mechanism is a motorized ball-accelerator loop at the upper-left of the
playfield, built from the **A-15297 Accelerator (Entrance) Ramp Assembly**, the **A-15300 Accelerator
Tray Assembly** (the three-wheel drive stack itself), and the **A-15293 Accelerator Return Assembly**
feeding back down through a diverter to either the left ramp or another lap of the loop. Two dedicated
PC boards instrument and drive it:

- **A-15189 Accelerator Board Assembly** carries the row/column switch-matrix return wiring for the
  three wheel-position optos (switches 81, 82, 83 -- "Opto 1/2/3") *and* the power/drive wiring for
  the three wheel-drive Enable relays (solenoids 25, 26, 28) *and* the Enable feedback lines routed
  back through the Power Driver Board. One board, three opto sensors, three motor-enable relays.
- **A-13901-1 Opto Ramp Switch Board Assembly** carries only switches 84 and 85 -- no solenoid wiring
  at all -- one connector (J2) per address, each wired to its own opto LED/phototransistor pair.

The retained known-working table does not simulate real wheel-drive physics: its `SW81_Hit`,
`SW82_Hit`, and `SW83_Hit` handlers each simply add ball X-velocity in ascending amounts (+11, +15,
+19) as the ball trips each opto in turn, modeling acceleration through scripted velocity boosts
rather than a driven mechanism. The three Enable relay solenoids (25/26/28) have no `SolCallback`
entry in the script at all and are not visually implemented; this recreation's only visible feedback
for the loop is the ball's own accelerating motion and, separately, the "Supercharger Flasher"
(solenoid 18) and "Free Ride Flasher" (solenoid 20) lighting effects.

At the base of the Accelerator Return Assembly sits a diverter (retained table objects `Wall29`/
`sc_div`) controlled by solenoid 10 (Diverter Low, via the script's `SuperchargerDiverter` handler)
that either sends the ball around the loop again or lets it continue. A second solenoid, 1 (Diverter
High), is printed on the same physical assembly but has **no** script implementation at all in this
recreation -- the retained table simply does not animate it.

### Switch 84/85 identity: settled by the ROM

Both switches sit on the A-13901-1 board and both are printed as opto interrupters, so their
*construction* and *polarity* were never in doubt (PinMAME's `gwGameData` inverted-switch mask covers
exactly 81-85, a clean match against the manual's opto part sweep). Which physical position each
address senses was. The manual's Switch Locations and SWITCH MATRIX pages print 84 = "Opto Made Loop"
and 85 = "Enter Left Ramp"; the pinned driver's guessed `#define`s (`swLRampEnt` = 84,
`swOptoLoopMade` = 85) and the retained known-working script (`SW85_Hit` in its `'supercharger` block
with a distinctive `"sc_loop2"` sound, `SW84_Hit` among the `'Ramp Triggers`) pair them the other way.
Those two could not settle it alone, since a table author routinely copies switch numbers from the
public driver source.

The ROM's own T.1 SWITCH EDGES test does settle it. In hash-pinned harness runs of the production L-5
and L-1 ROMs from empty NVRAM (`tools/harness-scenarios/wpc-fliptronic/gw-switch-edges-84-85.json`,
evidence `evidence/runtime/wpc-fliptronic/getaway-gw_l5-switch-edges.json` and
`getaway-gw_l1-switch-edges.json`), setting public 84 to 1 makes the top line read **ENTER LEFT RAMP**
with this matrix position's wires WHT-YEL GRN-GRY, and public 85 reads **OPTO MADE LOOP** with
WHT-GRN GRN-GRY, while the controls behave as expected (45 R BANK MID, 81 OPTO 1). The ROM's name table
and its game logic are one firmware written for the physical machine, so 84 is the left-ramp entrance
opto and 85 the loop-completion opto, and the definition labels them that way. The two printed pages
carry the names transposed; each device's note says so.

## Ramp lift mechanism

The **B-12576 Ramp Lifting Mechanism Assembly** raises and lowers the right ramp surface between a
lowered position (routing the ball onto the Supercharger return path) and a raised position (routing
it along the ordinary right ramp instead), driven by solenoids 2 (Up Ramp) and 3 (Down Ramp). Its own
exploded-parts page lists a microswitch, part `5647-12001-00` -- the *exact* part the Switch Locations
page prints for switch 54 (Ramp Down), confirming switch 54 is this mechanism's own built-in position
sensor rather than a separate playfield object. The retained script's `SolRampUp`/`SolRampDown`
handlers set `Controller.Switch(54)` directly in the same code that toggles the moving ramp's
collidability and rotates a diverter flap, with no independent trigger object for the switch -- and
the pinned driver's own `gw_handleMech` function implements the identical causal pairing in C
(`core_setSw(swRampDown, ...)` keyed off `core_getSol(sRampUp)`/`core_getSol(sRampDown)`), the one
mechanism on this machine where the guessed driver and the manual agree completely.

## Three-ball visible lock

Balls can be held on the wire right ramp at Top/Middle/Bottom Lock (switches 74/75/76, all opto
per the same A-13901-1-family construction pattern... no -- these three are *not* on either opto
board; they use the ordinary `5647-12693-21`/A-15103 wire-ramp switch part, plain leaf construction).
Solenoid 4 (Locker / Disappearing Post, A-15127 assembly) raises a post that releases the locked balls
when fired. The retained script models this with the standard `cvpmVLock` helper class.

## Kickback

The retained script's kickback handler (solenoid 8) fires a literal VPX `Plunger`-type table object
(`Plunger1`) positioned immediately next to switch 25 (Left Outlane) in the retained geometry -- not
the shooter-lane plunger, which is a separate `cvpmImpulseP` instance bound to solenoid 12 and switch
78. This confirms the B-11873 Kickback Assembly is a left-outlane mechanism, consistent with its
manual placement.

## Gear shifter: not modeled in this recreation

Switches 33 (Gear Shifter Low) and 34 (Gear Shifter High) belong to the **20-9710 Up-Down Shifter**, a
cabinet-mounted gear-shift lever with its own internal microswitch and bayonet-base bulb. Its own
manual page carries no item-number balloons or parts table at all -- only the illustration and a
"Cabinet shown for reference" caption -- and no object anywhere in the retained VPX extraction has
"gear" or "shift" in its name. The retained script drives these two switches purely from two unrelated
keyboard keys (`LeftMagnaSave` for 33, `PlungerKey` for 34); the physical lever mechanism has no table
geometry in this recreation, and neither switch carries a spatial placement here as a result.

## Upper-left flipper: confirmed not fitted

Three independent, game-specific sources agree the machine has no upper-left flipper (only lower-left,
lower-right, and upper-right):

1. The Switch Locations parts list lists only two flipper cabinet-button items -- a double switch
   (right side, serving both the lower-right and upper-right leaf switches from one paddle) and a
   single switch (left side, lower-left only). No `A-15205-L` (upper-left leaf switch) part appears
   anywhere on the page.
2. The Left Flipper Circuit diagram (printed page 3-10) labels its second coil block **"UPPER LEFT
   (NOT USED)"** in so many words, while the companion Right Flipper Circuit diagram labels both of
   its coil blocks with no such annotation.
3. The Flipper Circuits wire table (printed page 3-21) prints the Upper Left Flipper Button Switch
   wire as **"Black/Blue(NU)"** -- the manual's own explicit Not Used suffix.

`gwGameData`'s `FLIP_SW(FLIP_L | FLIP_UR) | FLIP_SOL(FLIP_L | FLIP_UR)` independently agrees: no
`FLIP_UL` bit is set. A later, generic duplicate of the Switch Matrix page near the end of the manual
lists Fliptronic positions F7/F8 without any Not Used annotation of its own, but this is the same
reused Fliptronic-II-controller silkscreen template every WPC-Fliptronic game's manual carries
regardless of that specific game's actual flipper count -- the three game-specific sources above
settle fitment decisively, not this generic block.

## Solenoid 31 and the undeclared fast-flip address

The retained known-working script binds `SolCallback(31) = "FastFlips.TiltSol"`, the nFozzy
`cFastFlips` convention for reading PinMAME's synthetic fast-flip flipper-enable signal. Pinned `gw.c`
never calls `wpc_set_fastflip_addr`, so per `src/wpc/wpc.c`'s `core_gameon` fallback PinMAME publishes
public solenoids 29-31 as a mirror of bits 5-7 of the `WPC_GILAMPS` register instead of a fast-flip
RAM flag. That looked like a contradiction, but bit 7 is not a lamp bit: the same `wpc.c` comment
records that before Fliptronic it drove the real game-on relay, and this ROM still drives it as its
game-on state.

A hash-pinned gameplay run of `gw_l5` (`tools/harness-scenarios/wpc-fliptronic/gw-flipper-enable-31.json`,
evidence `evidence/runtime/wpc-fliptronic/getaway-gw_l5-flipper-enable-31.json`) compares public 31 with
the ROM's own flipper response. In attract mode 31 is 0 and the Fliptronic lower-right button (112)
fires nothing. Start raises 31 for ball 1, and the button then fires flipper power 45 and holds 46. The
third plumb-bob pulse tilts the game and drops 31, and the button fires nothing again; when the ball
drains and ball 2 begins, 31 rises and the button works once more. The wheel-drive Enable outputs 25,
26 and 28 rise and fall with it. So the script's binding reads exactly the state it expects, and a
recreation can use public 31 as this game's flipper-enable signal.

## General illumination

Five printed illumination strings: strings 1-2 (GI addresses 0-1) are wired exclusively to the
playfield; strings 3-5 (GI addresses 2-4) are wired to the backbox insert panel, with string 5
additionally reaching a cabinet connector. The retained script's `UpdateGI` routine ignores its own GI
address parameter entirely and drives one shared 25-member playfield light collection for *any* GI
address activation, so this recreation cannot distinguish which specific playfield bulbs belong to
string 1 versus string 2 -- both addresses are left without an individually validated placement as a
result, an honest gap rather than an invented split.

## Physical family

The five-driver clone tree rooted at `gw_l5` covers fourteen total drivers in the pinned catalog: the
L-5 production ROM (this definition's primary binding, matching the retained known-working table's own
`cGameName`), the D-1/D-2/D-3/D-5 "LED Ghost Fix" display-timing revisions, the L-1/L-2/L-3 earlier
production firmware, five prototype ROMs (P-B, P-C, P-D, P-7, P-8),
and `gw_l5c`, a 2017 community "Competition MOD" patch (rev. L-5 patch bc43) for the identical physical
hardware. Every driver shares the same static `gwGameData`/`init_gw` pair; all fourteen are physically
identical.
