# The Addams Family Gold (Bally, 1994)

Coverage: **author_ready (100%)**.

The Special Collectors Edition is model 50038, IPDB 21, OPDB G4ODR-MLzY7. This record owns exactly nine tafg_* drivers. It describes the factory 1994 Gold machine. The original 1992 edition, later original-production gold art and the gold-plated production-record commemorative cabinet have separate identities. Williams' archived [Ask Uncle Willy #16](https://www.planetarypinball.com/mm5/Williams/archives/willy16.htm) explicitly distinguishes the commemorative cabinet from Gold production.

## Evidence roles

The Gold Operations Manual 16-50038-101 controls physical construction. Its complete switch, lamp, coil, GI and flipper table regions are transcribed under evidence/excerpts/bally.the-addams-family-gold.1994, with source-literal blank cells and printing errors preserved. Factory amendment 16-9805 (March 22, 1994) corrects the gold bumper caps and identifies two slam contacts: 27-1066 on the coin door and SW-1A-117 inside the cabinet. The source files remain external; hashes, locators, attribution and reviewed excerpts travel with the definition.

Pinned PinMAME revision 46e1a01a controls the nine-driver inventory, public address arithmetic, normalization, simulator channels and 128×32 DMD callback. The retained Sliderpoint Gold 1.4.1 VPX controls its own runtime bindings and geometry. It targets tafg_lx3, uses UseSolenoids=1 and HandleMechanics=0, and implements the hand/bookcase with host cvpmMech objects. Full extraction manifests pin every file. Shared-layout geometry has an explicitly narrower role: a modeled physical bulb can locate a Gold-manual-fitted emitter after reconciliation with the exact Gold table and physical photographs. It supplies neither Gold identity nor Gold runtime behavior.

The IPDB-hosted hierarchical 50038 parts list is undated and its original compiler is not credited. Its assembly quantities and wire pairs are cross-checks against the manual and photographs. It lists A-20207.1 inside A-17316, while the contemporary manual specifies A-16384; the definition follows the contemporary manual for original button construction. The listing is not silently treated as a dated factory change notice.

## Gold construction and controller

Gold adds buyin switch 11 (20-9663-9), optical cabinet button boards A-17316/A-16384, high-power interlock A-17077, revised flipper assemblies and bumper-lane opto A-16908/A-16909. The interlock breaks the +50V/+20V transformer secondary independently of matrix 22 memory protect. Gold retains the J801–J806 flipper controller and separate power-driver bridge: Fliptronics I architecture. The later A-12697-3 power-driver board omits the former relay. Generic Pinside/IPDB platform labels do not override the actual Gold schematic and board photographs.

The public contract is GEN_WPCFLIPTRON (0x8): eight dedicated switches, the complete 8×8 switch matrix, flipper inputs 111–118, eight DIP bits, solenoids 1–50, the complete 8×8 lamp matrix and GI indices 0–4. These are address counts, including virtual and unfitted positions. Matrix switches 12,23,28,46,52,83,88 are unused; 24 is the always-closed reference. The 0x7c/0x18 masks cover matrix optos 53–57 and 84–85. Cabinet optical channels 112/114/116/118 use the separate complemented Fliptronic convention and are normally open under the platform contract. Physical EOS leaves 111/113/115/117 are open at rest per Gold 2-15.

Solenoids 29–31 publish WPC GPIO/GameOn register state; 32 and 37–44 have no Gold load. Simulator channel 49 publishes manual-shooter release state when the built-in simulator is used; 50 is reserved/zero. Channel 49 is not an auto-plunger. All eight real flipper power/hold winding addresses remain distinct. The printed 'Flasher' drive-bank classification for 25–28 does not make the hand/bookcase motors or eject coils into flash lamps.

Buyin button 11 is fitted and wired. Lamp 41 is a different question: the manual prints Not Used, original Gold owners report an unwired factory button lamp, and retained diagnostic photographs identify the live ROM state as BUY IN / LAMP41 / RED-BRN / YEL-BLK. This physical lamp-matrix address is unused because it has no factory wired load; its meaningful ROM state is the buyin lamp state, not evidence of factory fitment. Later owner-added lamp wiring and diode are a retrofit. See the retained [Pinside discussion](https://pinside.com/pinball/forum/topic/addams-family-gold-extra-ball-lamp), including the original-owner account and successful retrofit report.

Lamp 76 is also printed Not Used in the Gold lamp matrix (3-2). It has no fitted factory bulb quantity. Both unused addresses 41 and 76 retain their CPU bindings and documented row/column wiring, with spatial reason unused.

Lamp 76 is unused. Lamps 81–87 are the seven speaker-panel THING bulbs and 88 is the credit/start-button lamp; they have cabinet spatial records. Jackpot 13 and Cousin It 26 each drive two physical bulbs on their respective four-socket PCBs. Flashers 17/18/20/21 each drive two bulbs. Circuit 19 drives three: one lower-ramp dome plus two jet-bumper sockets. Circuit 22 drives one playfield bulb and three atop the backbox. Gold eject coil 26 is AE-27-1200. The GI summary's connector readings are preserved literally; structured routing follows the actual 3-20 interboard destinations.

## Spatial evidence

Coordinates use x=0 left, x=1 right, y=0 rear and y=1 apron. Gold bounds are 0,0,985,2220. Each physical emitter gets its own placement. Raw object coordinates, world-space mesh bounds, factory pixel reads, per-page affine controls, normalization and exclusions are pinned in the geometry seed and generated spatial report. Manual pixels are independently read from retained native-resolution crops. A second drawing checks measurements outside the main control hull. The 0.07 normalized callout limit is a curator convention, not a physical manufacturing tolerance. Six decimal places preserve deterministic normalization and do not claim micrometer measurement accuracy.

Hidden coils, EOS leaves and feedback sensors use explicitly disclosed projections to their own physical mechanism when internal geometry is unavailable. Actual bulb meshes and factory socket measurements replace insert overlays, bloom and reflection sprites. The two PCB lamp pairs are separate drawn sockets, not offsets invented around one light. Raised red/green bulb primitives are selected by their physical color and binding rather than their misleading L74/L75 names. The hand magnet uses its actual moving body in the retained reference pose; it is not projected onto a fixed saucer magnet.

The playfield GI census is 21 #44 bulbs plus two #555 bulbs: 14+1 on the left and 7+1 on the right. One lower-left #555 uses its glass mesh. The phone #555 has no own glass mesh and uses an explicit projection to its identified socket mount, Gold Primitive72 at normalized (0.936675,0.105180), with 0.125 normalized radial uncertainty. This is a stock socket-family envelope, not an observed glass centre at the rivet. A new direct incandescent-body photograph identifies its own foot below the blue plate; an earlier LED repair photograph has an above-plate pose. Neither is claimed untouched factory. The factory A-12887 profile, replacement-family engineering dimensions/tolerances and the maximum of same-part modeled bulb and retained stock-ball physics scales bound the disclosed rigid-pose template without selecting either height. CEC replacement dimensions are not relabelled original Williams manufacturing dimensions, and arbitrary leg deformation is outside this approximation. The phone-GI and socket-dimension excerpts retain the arithmetic, source roles and limits. The old left-edge/0.025 proposal is withdrawn; no camera fit, hotspot, helper or ambiguous washer supplies the new coordinate. The optional Cousin Itt figure's extra lamp is excluded. Orange backbox GI has 15 #555; yellow has eight #555 plus seven self-blink #455. Two coin-door lamps are cabinet loads on the right string.

The newly user-supplied 2.4.41 table was also inspected from its actual native meshes and world export. Its script header identifies 2.4.41 while embedded info.json is stale at 2.3.1. No usable own telephone #555 glass/socket was found: the changed PhoneMod_9 is an optional animated telephone toy, including a hidden native mesh inspected separately, and changed RGP8_B_GI2off contains art/plastic surfaces. The separate #906, plates and hardware are not substitute #555 coordinates. Full source/extraction/export manifests and the 2031-component inspection remain pinned; this ancestral geometry is not independent Gold fitment or runtime authority.

Trough switches 15 and 16 use separate script-bound functional contact projections from the supplementary RealishTrough model; switch 17 uses the exact Gold BallRelease contact. Their physical B-8925/A-11680 construction and arrangement are independently established by the Gold manual and physical photographs. These are disclosed contact projections, not three copies of a trough centroid or coordinates taken from leaderless labels.

## Mechanisms and ball paths

### Motorized rotating bookcase (Vault)

A-14970-1 motor 14-7969/crank rotates the bookcase to hide or expose the Vault shot. Real microswitches 81/82 report open/closed; four optical impact channels 53–56 in the bookcase face register hits for GREED independently of rotation. Exact Gold host model cvpmMech uses solenoid 27, length 100, steps 90, reverse/nonlinear motion, closed 82 at 0–1 and open 81 at 89–90. Those are model units, not physical degrees/timing. Initialize from the actual bookcase pose; the native cyclic model and the host model use different counter phases. Startup/service motor search requires real feedback to follow movement. T.13 toggles motor and displays limits. A jam or missing limit must remain visible to the ROM; never force both limits active. Native taf_handleMech uses an alternative 200-tick cyclic model, not the physical construction.

### Motorized raising/lowering Thing hand

A-14711 in locations, A-17411 in 2-27 heading, motor 14-7966 and two opto limits on A-15285 with A-15310 interrupter. Coil 6/A-12158-1 magnet travels in the hand to pick up a ball from saucer 87, carry it over the box, then drop it into the return path. Exact Gold cvpmMech uses coil 25, length 175, steps 60, reverse/nonlinear, down 84 at 0–1 and up 85 at 59–60; these are host model units. T.12 motor test toggles motor and displays both limits; Operation Test cycles pickup/drop with a ball. Initialize the hand and its two limits from its actual pose, with the magnet off; a down resting pose is usual but is not guaranteed after interruption. Keep the two limits mutually exclusive and report jams/missed pickup through actual sensor/ball state rather than teleporting a successful ball.

### Electric Chair kickout

Ball closes 43 in A-14962 loop at the Electric Chair; coil 1 in A-15115 ejects it to the playfield. Gold script Chair enables ChairKicker timer and releases the captured ball. Red 47/yellow 64 bulbs belong to two separate sockets on A-15258 chair bracket; the FesterBulb visual is an optional mod/proxy, not those sockets.

### Cabinet knocker

Thing Knocker coil 2 is mounted in the cabinet, Gold parts-list A-15267 with A-15266 bracket. Gold 2-43 marks cabinet placement. A-15257 in the underside diagram is a different magnet bracket/pole-piece part. The knocker strikes its own stop, has no sensing switch, and does not move a ball.

### Thing eject saucer, magnet grab, and kickout

Switch 87 detects a ball in ThingSaucer/A-15368 eject assembly. Coil 26 (Gold AE-27-1200) ejects it when the hand is not collecting it. Coil 6 energizes the magnet in the moving hand, not below the saucer. The script lifts its stored ball with the Thing animation, releases it into the hand return lane, then switch 77/coil 7 return it to play. Keep ball ownership exclusive between saucer and hand; a missed grab is not a successful lock.

### Thing kickout hole

A-15200 return kickout holds a ball on switch 77. Solenoid 7 ejects it after the Thing return/lock sequence; it is distinct from saucer 87/coil 26. Gold script ThingKickOutKicker handles this switch and kickout.

### Swamp lock (three-ball lock) and release

Three retained lock positions 71/72/73 are separate microswitches on A-14964 lockup loop. The lowest retained ball reaches the controlled Swamp Release coil 28/A-15367; release feeds the separate kickout pocket 74, where coil 8/A-14107 returns a ball. Script walls are virtual lock stops and are not extra physical coils. Boot must account for every ball in lock/trough. Gold rules can purge locked balls into the trough at game end (operator setting); do not preserve a lock across games unconditionally.

### Center ramp diverter

Coil 3 actuates A-15040 flap/return mechanism at the left end of the centre Bear Kick ramp, routing a ball toward the Thing mini-flipper instead of the normal return/inlane. There is no dedicated position switch. Exact script uses vpmSolDiverter on Diverter. Coil state controls routing; a neighbouring ramp switch is ball passage, not a diverter limit.

### Ball trough, outhole, and ball release

Three balls fit the trough. Outhole switch 18/coil 5 feed it; switches 15/16/17 identify left/centre/right and coil 4 releases from the right into shooter switch 27. Exact Gold cvpmTrough declares size 3, entry 18, switch order 17,16,15 and BallRelease exit. The manual plunger launches the ball; there is no auto-plunger coil. Its virtual instant drain/serve timings are not factory travel measurements. Start with actual occupied trough switches, clear27 only when the ball leaves, and preserve missing/stuck balls for ROM search.

### Five-bumper jet nest

Five real jet bumpers use switches 31–35 and coils 9–13, one-to-one in upper-left, upper-right, centre-left, centre-right, lower order. Switch contact opens at rest; skirt impact pulses its own input and the ROM drives its coil. A shared GREED lamp group is independent of the bumper skirt switches.

### Left and right slingshots

Gold physical left sling switch 36 drives left coil 14; right 37 drives right 15. Retained script pulses the opposite switch numbers from its Left/RightSlingShot events, a discrete table defect. Follow both Gold tables for physical mapping. The script animates the rubbers in the hit event; do not make that animation evidence of extra actuators.

### Left, upper, and right under-playfield magnets

Three under-playfield Power magnets 20-9247 use solenoids 16/23/24 through A-15139 high-power board and the supplementary supply. Left/upper/right centres are separate ball-force regions with no dedicated sensing switches. Exact script cvpmMagnet binds LMagnet/UMagnet/RMagnet respectively. The manual requires the under-playfield 5A slow-blow fuse. Keep coil energization and ball physics coupled; no proximity switch should be invented.

### Lower flipper pair

Gold FL-15411 lower pair has separate power/hold windings 45/46 right and 47/48 left, real normally-open EOS 111/113 (Gold 2-15), and A-17316 optical cabinet buttons 112/114. Button second channels 116/118 are on the same two physical button boards. Native FLIP_BUT(FLIP_L) models lower hardware bypass; core_updateSw synthesizes EOS feedback from coil state. Exact Gold script uses UseSolenoids=1 and rotates RightFlipper/LeftFlipper from callbacks. Preserve independent windings and startup released state.

### Upper right flipper

Gold upper-right FL-11630 per 3-6, A-15849-R, winding 33/34 and EOS 115. The parts page 2-14 prints FL-17630; this wiring detail is retained literally. Exact Gold SolURFlipper rotates Flipper1. Upper actuation is ROM-controlled rather than a lower-flipper hardware bypass; no independent third cabinet button exists. Match the ROM output rather than unconditionally firing it on a host key.

### Upper left "Thing's Mini-Flipper"

Gold upper-left A-15849-L-1, FL-11753 Thing mini-flipper, windings 35/36 and EOS 117. The calibrated Thing Flips shot is enabled by the far-left inlane, routes the ramp ball through bumper-lane opto 57, and uses swamp targets 45/47/48 and lock 71 as shot results. Gold manual Thing Flips automatic-calibration section aims for 50–60% success after learning; actual delay/strength is ROM-owned, not a fixed table constant. Exact SolULFlipper rotates Flipper2. This flipper is distinct from the motorized Thing hand.

## Gameplay and firmware variants

[Keefer's Gold Guide](https://gamefaqs.gamespot.com/pinball/915935-addams-family-special-collectors-edition/faqs/1447), V1.1.1, June 10, 1995, is retained in full with both preformatted blocks and its attribution/distribution notices. It describes Cousin It's belongings, the 3M extra room, 6M dialogue, Super Seance 10/15/20M awards, varying Jackpot, Dirty Pool Super Jackpot, adjustable endgame lock purge and buyin preserving progress. These are attributed gameplay observations. The guide distinguishes L-1/L-2 Jackpot behavior from L-3 behavior and does not establish physical random probabilities or mechanism travel times. Contributors are Jon Biavati, Mark Phaedrus, Mark Valentine and David Stewart.

The nine driver notes distinguish production revisions, LED ghost fixes, H-3 source uncertainty and the RedBall ball-saver patch at A.2 setting 36. All run on the documented Gold hardware; software release years do not create another physical machine. [Action Pinball's conversion instructions](https://www.actionpinball.com/tech/tafgconv.php) explain U6/U15/U18 changes that run Gold rules on original hardware, while explicitly noting the absent buyin button. That compatibility does not make a converted original cabinet factory Gold.

## Retained-table defects and exclusions

The exact Gold script reverses sling switch 36/37; this definition follows both Gold physical charts (left 36/coil14, right 37/coil15) and documents the table defect. Its splash string says 1992 and its embedded info says 1.4 despite the supplied 1.4.1 filename. Neither changes physical identity. Desktop THING helpers supply no playfield sockets. GI_Light* surface glows, duplicate brightness layers and the explicitly optional Chair/Swamp/Vault/Fester lighting are excluded from the factory inventory. Runtime traces or rendered pools cannot determine physical bulb quantity.
