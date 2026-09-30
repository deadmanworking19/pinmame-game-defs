# The Champion Pub (Bally, 1998) recreation knowledge

The physical machine is Bally model 50063, IPDB 4358, WPC-95 with one 128 × 32 DMD. This partial definition enumerates 88 public inputs (8 dedicated, 64 matrix, 8 flipper-register and 8 DIP), 50 solenoid/state outputs, 96 lamp bits (64 matrix and 32 serial LED-register bits), 5 GI strings and 17 physical mechanisms. Factory circuit and part tables establish construction; the retained mfuegemann 1.2 table establishes runtime binding and ball motion; pinned PinMAME establishes exported addresses and remaps. Literal table cells, blanks and merged rows are retained beside the definition.

Production cp_15 and cp_16 share cpGameData and sound images; authorized ZIP members match the pinned source CRC and SHA-1 declarations. Zen Studios' 2019 cp_16pfx entry is a software modification supported by the same factory board and address contract. Its program changes remain uncharacterized, without a claim of production-identical gameplay or display-only edits. [Upstream commit 405e0682](https://github.com/vpinball/pinmame/commit/405e06829516fc25ebdb5db4f550a9cc434293da) introduced ROM declarations, catalog registration and release notes for this software MOD, without emulator I/O changes. It introduces no separate physical edition and does not block the factory recreation.

PinMAME normalizes switch column 3 with mask 0x3f and column 4 with mask 0xff. Ordinary contacts and normalized optos use controller active 1. Physically normally closed Right Jab Made 38 is outside the mask: production 1.5 and 1.6 T.1 diagnostics call public 0 active and 1 released. Its retained script Hit=1 is a consumed-artifact defect. Rope Cam 64 is also unmasked, but T.1 calls public 1 active; its opto encoder construction does not make its exported contact contract normally closed. Scoop 61 and 62 activate at 1. Compact runtime records pin controls 32 and 52, fresh state, scenario, library, ROM ZIP and DMD pixels. Host feedback stops before diagnostic stimuli.

Factory F1/F3 EOS contacts are SW-1A-194; F2/F4 lower cabinet optos are A-17316. F5 through F8 have no fitted upper assemblies. FLIP_SW(L|U) nevertheless publishes upper buttons 116 and 118, and ROM T.1 identifies them as F6 and F8. They are used virtual states and may trigger the lower flippers and automatic EOS. Direct writes to 111 and 113 while PinMAME synthesizes them do not measure physical EOS polarity.

Initialize closed door 22, raised scoops 61/62 and the four occupied trough slots 32 through 35 consistently with the physical state. Constant 24 is Always Closed. Eight DIP bits are preserved; the retained script selects Dip(0)=0 without proving an immutable factory setting. Start, Launch, tilt, slam, coin and service controls are cabinet devices. The main display uses controlled cabinet placement.

Public solenoids 1 through 28 match the main factory table. Printed lower flipper 29/30 map to public 45/46; printed 31/32 map to 47/48. Because cpGameData has FLIP_SOL(L), public 33 Rope Popper, 34 Ramp Diverter and 35/36 separate Speed Bag fists remain nonflipper circuits. Public 29/30 are emulator J111 states, 31 is game-on fastflip state, 32 is constant zero, 49 is the disabled manual shooter state at constant zero and 50 is reserved. Outputs 37 through 40 are serial clock, strobe, right DA and left DB transport; 41 through 44 are their virtual mirrors. The serial driver is A-21967-2.

Four 4094 callbacks publish extra columns 10, 8, 11 and 9 in callback 0/1/2/3 order. Two A-21991-1 boards each contain twelve series pairs, giving 48 physical LEDs. The retained table binds 24 display segments to public bits. AllLights uses each Light.TimerInterval: LED91 maps to 95, and LED108 maps to 124. Multiple insert helpers and timer 100 helpers do not add lamps or bulbs. The eight unbound exported bits remain unknown; absent VPX bindings cannot prove physical outputs unused. Pair ordinals follow retained display order. Exact bit-to-factory L-number and connector routing, and separate emitter locations, remain explicit wiring and spatial blockers.

Factory 2-55 GI columns reverse the actual playfield and insert destinations. H-22227 playfield lamp cable contains BRN/WHT-BRN and ORG/WHT-ORG; H-22231-1 insert cable contains YEL/WHT-YEL, GRN/WHT-GRN and VIO/WHT-VIO. Board connector list 3-33 and known-working UpdateGI agree independently: public 0/1 are playfield; 2/3/4 are insert/backbox. The insert panel has 42 #555 bulbs in total, without a proven per-string split. Original location and bulb columns are preserved as a consumed manual defect.

Coordinates use retained bounds 0, 0, 970, 2100 and the repository rounding helper: x=0 left, x=1 right, y=0 rear and y=1 front. Direct switch and insert centers are reconciled with factory 2-52 and 2-45 topology. Assembly anchors use a retained world-space OBJ export. Stored primitive offsets and glow centers are not socket coordinates. Observed projections identify assembly footprints while retaining uncertainty about individual sensor and emitter locations.

## Four-ball Trough

Assembly A-19963. Actuators: coil.solenoid-2. Sensors: switch.matrix-31, switch.matrix-32, switch.matrix-33, switch.matrix-34, switch.matrix-35.

Four balls queue below the apron at optos 32–35. Coil2 sends the leading ball through eject opto 31 into the shooter lane. Retained bsTrough initializes32..35 and pulses31 on release. Draining replenishes the queue. Occupancy follows actual balls, not the drain kicker. Boot with the physical queue populated; a jam at the release obstructs launch.

## Shooter / Catapult

Assembly A-16757-2. Actuators: coil.solenoid-1. Sensors: switch.matrix-18.

Coil1 launches the ball waiting at shooter switch 18. Retained FireCatapult/bsCatapult supplies the launch and releases18 as the ball leaves. Hidden CatapultKicker and CatapultLaunchKicker are separate staging/motion helpers, not interchangeable factory sensor locations. A trapped ball keeps18 occupied.

## Left Corner Eject

Assembly A-22214. Actuators: coil.solenoid-5. Sensors: switch.matrix-37.

The left cup closes37 on capture. Coil5 ejects the ball and 37 releases after departure. The retained ball stack owns capture/release. A failed kick leaves occupancy, rather than pulsing a trough input.

## Left Rear Popper

Assembly A-22169. Actuators: coil.solenoid-14. Sensors: switch.matrix-28.

Ball closes28 in the left rear cup. Coil14 fires the vertical up-kicker to the rope feed route;28 releases after departure. Retained VUK1..VUKTop transport helpers and timer are one physical ball path, not extra solenoids. A blocked tube can leave28 occupied.

## Left Jab Scoop

Assembly A-22176. Actuators: coil.solenoid-3, coil.solenoid-9. Sensors: switch.matrix-61, switch.matrix-42, switch.matrix-36.

One dual-winding scoop has power 3/hold 9. Initially raised with 61 active, the retained hold callback moves it and writes61. Beam 42 behind the scoop and made-jab beam 36 report balls separately. Lowering opens the jab route; raising catches/deflects. Restore raised state at startup and let a jam prevent the position transition.

## Right Jab Scoop

Assembly A-22176. Actuators: coil.solenoid-4, coil.solenoid-10. Sensors: switch.matrix-62, switch.matrix-43, switch.matrix-38.

One scoop uses power 4/hold 10 and starts raised with 62 active. Retained hold callback moves it. Beam 43 behind the scoop and made-jab beam 38 are ball sensors;38 is an unmasked ROM-active public 0 exception. Lowering opens the route, distinct from ball beam events.

## Rotating Boxer / Heavy Bag

Assembly A-22171. Actuators: motor.solenoid-27, control_signal.solenoid-26, coil.solenoid-11, coil.solenoid-13. Sensors: switch.matrix-41, switch.matrix-46, switch.matrix-47, switch.matrix-48, switch.matrix-12, switch.matrix-66, switch.matrix-67, switch.matrix-68.

Motor 27 rotates a shared pole carrying boxer and heavy-bag faces; control26 reverses direction. A-22260 optos 41/46/47/48 encode facing marks. Impacts12/66/67/68 are separate target contacts. Coils11(right)/13(left) lift spring-return arms. Retained model wraps±180, advances 1 degree per15 ms, and opens41 near 0, 46 near±180, 47 near-27.5, 48 near+27.5. These windows/speed are simulation clues, not measured cams. Boot must answer ROM motor commands with changing feedback; static marks can stall self-test. A jam is distinct from an impact.

SB 107 addresses boxer arm shoulder fractures that can trap a ball or prevent arm movement. Revised left 31-3065.1 and right 31-3066.1 arms carry an interior B mark. The bulletin specifies a small amount of Loctite 425 intended for plastic on the mounting screw threads. This material revision does not introduce another controller address or mechanism.

## Jump Rope

Assembly A-22147. Actuators: motor.solenoid-25, magnet.solenoid-7, coil.solenoid-33. Sensors: switch.matrix-64, switch.matrix-45, switch.matrix-78, switch.matrix-71.

Motor 25 turns a continuous rope;64 senses its cam. Magnet 7 catches the ball at 45, and coil 33 pops it for the rope to pass underneath.78 is entry, 71 downstream exit. T.16 home points downward at 45 degrees with CAM OPEN; ball opto indication is OPEN with a ball on the magnet. Retained720 step circle asserts64 at phase 0..20/700..720 and kicks in a difficulty-dependent window. These are table settings, not RPM. Model missed catches, departure, motor coast and real sensor travel.

## Speed Bag and Fists

Assembly A-22148. Actuators: coil.solenoid-35, coil.solenoid-36. Sensors: switch.matrix-65, switch.matrix-72.

Separate coils 35(left)/36(right) drive fists against the bag.72 is ball entry;65 SW-1A-215 senses motion/impact. Retained fists spring back and a bag timer pulses65. Factory Power/Hold type labels do not make the two AE-27-1200 coils one dual-winding flipper. Default both retracted; a failed stroke can leave65 quiet.

## Center Up/Down Post

Assembly A-22173. Actuators: coil.solenoid-6, coil.solenoid-12. Sensors: switch.matrix-75.

One post uses power 6/hold 12. Retained hold callback raises it and writes75=1, lowering to75=0 on release. Default down; preserve position if jammed. Lamp85 is its separate illumination circuit, not its actuator.

## Danger Zone Post Diverter

Assembly A-22167. Actuators: coil.solenoid-8. Sensors: switch.matrix-73.

Coil8 moves a spring-return factory post in the right route.73 senses a ball in the danger-zone area, not post position. Retained DangerZoneMod=1 substitutes a gate; the factory recreation must restore the post. The gate geometry is an aftermarket overlay.

## Lock Pin / Three-ball Lock

Assembly A-22221. Actuators: coil.solenoid-28. Sensors: switch.matrix-15, switch.matrix-57, switch.matrix-58, switch.matrix-74.

Coil28 lowers the retention pin and releases balls. Spring return raises it. Three right-upper channel contacts15/57/58 sense balls;74 is entry. Retained timer delays pin return after release, a transport clue rather than measured factory timing. A jam can leave balls captured after the command.

## Upper Ramp Diverter

Assembly A-22172. Actuators: coil.solenoid-34. Sensors: switch.matrix-44, switch.matrix-11, switch.matrix-76.

Coil34 changes the upper ramp fork.44 entry, 11 made ramp and 76 top of ramp are ball sensors, not home contacts. Retained default closed; energizing raises the model and collision posts. Spring return restores closed. This is distinct from the danger-zone post.

## Left Slingshot

Assembly A-22206-2. Actuators: coil.solenoid-15. Sensors: switch.matrix-51.

Ball deflects left rubber, scoring switch 51 closes, and ROM coil 15 kicks it. Assembly has separate A-17800 kick and diode-equipped A-17794 scoring contacts. Animation returns to rest; a stuck contact is a fault.

## Right Slingshot

Assembly A-22206-2. Actuators: coil.solenoid-16. Sensors: switch.matrix-52.

Ball deflects right rubber and scoring switch 52; ROM coil 16 supplies rebound. A-17800 kick and A-17794 scoring contacts are separate. Retained animation springs back to rest.

## Lower Right Flipper

Assembly A-15849-R-4. Actuators: coil.solenoid-45, coil.solenoid-46. Sensors: switch.flipper-111, switch.flipper-112.

Single FL-15411 dual-winding flipper has power 45/hold 46, remapped from printed 29/30. Button opto 112 and EOS111 are distinct. Retained hold callback animates motion; power delivers the stroke and hold maintains it. Spring return restores rest. No upper flipper is fitted.

## Lower Left Flipper

Assembly A-15849-L-4. Actuators: coil.solenoid-47, coil.solenoid-48. Sensors: switch.flipper-113, switch.flipper-114.

Single FL-15411 flipper has power 47/hold 48, printed 31/32. Button 114 and EOS113 are distinct. Power gives stroke, hold maintains it, and spring return restores rest. Upper virtual118 can reach ROM flipper control without a physical upper coil.

## Remaining evidence

Promotion needs the serial driver-to-LED bit/pin reconciliation; separate emitter coordinates for each series pair; actual playfield GI socket inventory; missing Left Hook To Win32 and factory Danger Zone73 geometry; trough five-optos; hidden encoder/EOS/contact positions; and flasher socket/lens centers. Observed fixture and assembly projections are supplied with specific per-device blockers. Reconcile measured factory diagrams with exact table controls before using them as coordinates. More simulation detail cannot resolve missing physical measurements.
