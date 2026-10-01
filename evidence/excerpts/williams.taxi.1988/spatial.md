# Taxi spatial admission and remaining blockers

Extraction manifest: vpx-sources/williams/taxi/Taxi (Williams 1988)1.2/extraction-vpxtool-git-v0.33.3/manifest.json, SHA256 b23d0faa0bacef495223a65b6c79a209c2eaa628e6675abb98c0c404cea09363. Retained table SHA256 7c6f52b24e7fabc761611d33b7eab5de15b9025f954fb4e423f3219e09af9c40.

Exact table bounds: left 0/top 0/right 952/bottom 1974 VPX units. x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top), round to six places with repository pinmame_game_defs.spatial.extract_spatial_candidates / _round_point. Coordinate sources and controller-routing sources are separate; factory PDF 60/62 leaders reconcile the projected assembly/site identities, without a manual pixel transform or invented frame fit.

| Device | Object | Extracted path | Method | x | y | Role |
| --- | --- | --- | --- | --- | --- | --- |
| switch.13 | JoyrideEject | gameitems/Kicker.JoyrideEject.json | center | 0.168928 | 0.134554 | sensor |
| switch.14 | sw14 | gameitems/Trigger.sw14.json | center | 0.381828 | 0.112842 | sensor |
| switch.15 | sw15 | gameitems/Trigger.sw15.json | center | 0.487395 | 0.117908 | sensor |
| switch.16 | sw16 | gameitems/Trigger.sw16.json | center | 0.598477 | 0.12576 | sensor |
| switch.17 | Bumper1 | gameitems/Bumper.Bumper1.json | center | 0.36187 | 0.220365 | sensor |
| switch.19 | Bumper2 | gameitems/Bumper.Bumper2.json | center | 0.573792 | 0.225051 | sensor |
| switch.21 | Bumper3 | gameitems/Bumper.Bumper3.json | center | 0.455882 | 0.308637 | sensor |
| switch.23 | sw23 | gameitems/Gate.sw23.json | center | 0.733665 | 0.166148 | sensor |
| switch.24 | sw24 | gameitems/HitTarget.sw24.json | position | 0.252626 | 0.136398 | sensor |
| switch.25 | sw25 | gameitems/Gate.sw25.json | center | 0.193533 | 0.415986 | sensor |
| switch.26 | sw26 | gameitems/Gate.sw26.json | center | 0.725053 | 0.421859 | sensor |
| switch.27 | sw29 | gameitems/HitTarget.sw29.json | position | 0.425158 | 0.385132 | sensor |
| switch.28 | sw28 | gameitems/HitTarget.sw28.json | position | 0.480173 | 0.373417 | sensor |
| switch.29 | sw27 | gameitems/HitTarget.sw27.json | position | 0.536633 | 0.361892 | sensor |
| switch.30 | sw30 | gameitems/HitTarget.sw30.json | position | 0.83469 | 0.530838 | sensor |
| switch.31 | sw31 | gameitems/HitTarget.sw31.json | position | 0.833246 | 0.555978 | sensor |
| switch.32 | sw32 | gameitems/HitTarget.sw32.json | position | 0.83167 | 0.581687 | sensor |
| switch.33 | sw33P | gameitems/Primitive.sw33P.json | world-space mesh bounds center | 0.212611 | 0.265196 | sensor |
| switch.34 | sw34P | gameitems/Primitive.sw34P.json | world-space mesh bounds center | 0.733085 | 0.228081 | sensor |
| switch.35 | Catapult | gameitems/Kicker.Catapult.json | center | 0.050566 | 0.589215 | sensor |
| switch.36 | RightLock | gameitems/Kicker.RightLock.json | center | 0.917146 | 0.303642 | sensor |
| switch.37 | sw37 | gameitems/Trigger.sw37.json | center | 0.059611 | 0.740502 | sensor |
| switch.38 | sw38 | gameitems/Trigger.sw38.json | center | 0.128414 | 0.718212 | sensor |
| switch.39 | sw39 | gameitems/Trigger.sw39.json | center | 0.852789 | 0.739932 | sensor |
| switch.40 | sw40 | gameitems/Trigger.sw40.json | center | 0.779129 | 0.714256 | sensor |
| solenoid.3 | Catapult | gameitems/Kicker.Catapult.json | center | 0.050566 | 0.589215 | effect |
| solenoid.4 | sw28 | gameitems/HitTarget.sw28.json | position | 0.480173 | 0.373417 | effect |
| solenoid.5 | JoyrideEject | gameitems/Kicker.JoyrideEject.json | center | 0.168928 | 0.134554 | effect |
| solenoid.6 | sw31 | gameitems/HitTarget.sw31.json | position | 0.833246 | 0.555978 | effect |
| solenoid.7 | SpinoutKicker | gameitems/Kicker.SpinoutKicker.json | center | 0.850053 | 0.112589 | effect |
| solenoid.8 | RightLock | gameitems/Kicker.RightLock.json | center | 0.917146 | 0.303642 | effect |
| solenoid.9 | TopGate | gameitems/Wall.TopGate.json | drag-point mean | 0.225696 | 0.06774 | effect |
| solenoid.17 | Bumper1 | gameitems/Bumper.Bumper1.json | center | 0.36187 | 0.220365 | effect |
| solenoid.19 | Bumper2 | gameitems/Bumper.Bumper2.json | center | 0.573792 | 0.225051 | effect |
| solenoid.21 | Bumper3 | gameitems/Bumper.Bumper3.json | center | 0.455882 | 0.308637 | effect |

## Playfield lamp placements

Each playfield lamp uses the stored centre of the single table Light that the embedded script binds with `Set Lights(N)=lN` (script lines 272-318). No lamp uses a glow, reflection, insert overlay or centroid.

| Device | Object | Extracted path | Method | x | y | Role |
| --- | --- | --- | --- | --- | --- | --- |
| lamp.9 | L9 | gameitems/Light.L9.json | center | 0.352941 | 0.506269 | emitter |
| lamp.10 | L10 | gameitems/Light.L10.json | center | 0.403493 | 0.506522 | emitter |
| lamp.11 | L11 | gameitems/Light.L11.json | center | 0.451221 | 0.506396 | emitter |
| lamp.12 | L12 | gameitems/Light.L12.json | center | 0.501116 | 0.506586 | emitter |
| lamp.13 | L13 | gameitems/Light.L13.json | center | 0.555475 | 0.506586 | emitter |
| lamp.14 | L14 | gameitems/Light.L14.json | center | 0.380817 | 0.068351 | emitter |
| lamp.15 | L15 | gameitems/Light.L15.json | center | 0.487881 | 0.074316 | emitter |
| lamp.16 | L16 | gameitems/Light.L16.json | center | 0.597256 | 0.082865 | emitter |
| lamp.17 | L17 | gameitems/Light.L17.json | center | 0.451295 | 0.633843 | emitter |
| lamp.18 | L18 | gameitems/Light.L18.json | center | 0.404307 | 0.592646 | emitter |
| lamp.19 | L19 | gameitems/Light.L19.json | center | 0.50405 | 0.592663 | emitter |
| lamp.20 | L20 | gameitems/Light.L20.json | center | 0.404533 | 0.553136 | emitter |
| lamp.21 | L21 | gameitems/Light.L21.json | center | 0.504307 | 0.552713 | emitter |
| lamp.22 | L22 | gameitems/Light.L22.json | center | 0.229386 | 0.630098 | emitter |
| lamp.23 | L23 | gameitems/Light.L23.json | center | 0.795299 | 0.501361 | emitter |
| lamp.24 | L24 | gameitems/Light.L24.json | center | 0.468487 | 0.177527 | emitter |
| lamp.25 | L25 | gameitems/Light.L25.json | center | 0.780226 | 0.544871 | emitter |
| lamp.26 | L26 | gameitems/Light.L26.json | center | 0.136482 | 0.509922 | emitter |
| lamp.27 | L27 | gameitems/Light.L27.json | center | 0.499584 | 0.400073 | emitter |
| lamp.28 | L28 | gameitems/Light.L28.json | center | 0.265866 | 0.325618 | emitter |
| lamp.29 | L29 | gameitems/Light.L29.json | center | 0.639575 | 0.336411 | emitter |
| lamp.30 | L30 | gameitems/Light.L30.json | center | 0.454044 | 0.837133 | emitter |
| lamp.31 | L31 | gameitems/Light.L31.json | center | 0.454044 | 0.68503 | emitter |
| lamp.32 | L32 | gameitems/Light.L32.json | center | 0.841124 | 0.461151 | emitter |
| lamp.33 | L33 | gameitems/Light.L33.json | center | 0.394039 | 0.751298 | emitter |
| lamp.34 | L34 | gameitems/Light.L34.json | center | 0.327468 | 0.663406 | emitter |
| lamp.35 | L35 | gameitems/Light.L35.json | center | 0.546744 | 0.7418 | emitter |
| lamp.36 | L36 | gameitems/Light.L36.json | center | 0.589548 | 0.648398 | emitter |
| lamp.37 | L37 | gameitems/Light.L37.json | center | 0.054884 | 0.684524 | emitter (candidate) |
| lamp.38 | L38 | gameitems/Light.L38.json | center | 0.128355 | 0.66338 | emitter |
| lamp.39 | L39 | gameitems/Light.L39.json | center | 0.853919 | 0.685512 | emitter |
| lamp.40 | L40 | gameitems/Light.L40.json | center | 0.779707 | 0.660296 | emitter |
| lamp.41 | L41 | gameitems/Light.L41.json | center | 0.671218 | 0.506871 | emitter |
| lamp.42 | L42 | gameitems/Light.L42.json | center | 0.249737 | 0.506364 | emitter |
| lamp.43 | L43 | gameitems/Light.L43.json | center | 0.23792 | 0.267541 | emitter |
| lamp.44 | L44 | gameitems/Light.L44.json | center | 0.679753 | 0.262855 | emitter |
| lamp.45 | L45 | gameitems/Light.L45.json | center | 0.317621 | 0.43465 | emitter |
| lamp.46 | L46 | gameitems/Light.L46.json | center | 0.192752 | 0.581655 | emitter |
| lamp.47 | L47 | gameitems/Light.L47.json | center | 0.264312 | 0.182276 | emitter |
| lamp.48 | L48 | gameitems/Light.L48.json | center | 0.222164 | 0.460391 | emitter |
| lamp.57 | L57 | gameitems/Light.L57.json | center | 0.883535 | 0.289767 | emitter |
| lamp.58 | L58 | gameitems/Light.L58.json | center | 0.882222 | 0.270707 | emitter |
| lamp.59 | L59 | gameitems/Light.L59.json | center | 0.882747 | 0.25304 | emitter |
| lamp.60 | L60 | gameitems/Light.L60.json | center | 0.88209 | 0.234549 | emitter |
| lamp.61 | L61 | gameitems/Light.L61.json | center | 0.881828 | 0.215109 | emitter |
| lamp.62 | L62 | gameitems/Light.L62.json | center | 0.882484 | 0.197062 | emitter |
| lamp.63 | L63 | gameitems/Light.L63.json | center | 0.88406 | 0.178255 | emitter |

Factory cross-check: `lamp-locations.webp` (SHA256 1da3d7347b6ba9d7f86eca40d6824f955bc1525e7766b5af4f5ff3181360bf9a) was fitted to the table with a least-squares affine from control pixels read by eye on gridded crops: Bumper1 px (298, 337) -> VPU (344.5, 435.0), residual 4.4; Bumper2 px (422.5, 345) -> VPU (546.25, 444.25), residual 2.2; Bumper3 px (350.5, 448.5) -> VPU (434.0, 609.25), residual 4.6; LeftFlipper px (261, 1112.5) -> VPU (273.6884, 1646.0), residual 1.5; RightFlipper px (462.5, 1111) -> VPU (590.5589, 1646.0), residual 1.9. Through that fit, every lamp above except 37 lands on its own printed insert or leader end. Lamp 37: Leader 37 ends on a small post-sized circle at the top of the left outlane, where the table models a rubber post at about (42, 1277) VPU; no insert is drawn at l37, about 75 VPU lower. The right outlane draws insert 39 exactly at l39. The left SPECIAL socket position is therefore not confirmed by the factory drawing. The fit, per-lamp drawing pixels, crops and overlays are retained in review-artifacts/taxi-1988/session-20261001/lamp-reconciliation (manifest SHA256 b97f0231b205bf2df11e1501e3c4795facd31cec3fda0eb03f1d89dbbd23a213). The drawing is an identity check only; no drawing pixel is a coordinate.

## Projection classes and world geometry

Visible Trigger rollover wires 14..16 and 37..40 anchor wire-actuation sites; the contact bodies are below the playfield. Gates 23/25/26 anchor the blade-actuated passage sites, not gate-home sensors. Kicker anchors 13/35/36 record occupied holes; coil 3/5/8 effects share the named catapult/eject assembly sites. Coil 7 uses the scripted Spinout ejection site, not a separately measured coil mount or switch 43 contact. Jet effects 17/19/21 share the ring centers. Coil 4/6 effects project the common reset assembly to its middle target face. Coil 9 uses the four-vertex mean of the narrow TopGate collision wall, locating route opening rather than the coil mount.

Drop 27..32 project the underplayfield opto sensing site to each raised face. Factory PDF 62 parts/leader endpoints, ROM names and successful L4 display responses settle left/middle/right 27/28/29 and top/middle/bottom 30/31/32. The retained script 153 binds sw27/sw28/sw29 directly, but the table faces are ordered sw29/sw28/sw27 from left to right. Use sw29 for physical 27 and sw27 for physical 29; this proven consumed-table defect belongs in notes, not machine conflicts.

World export: review-artifacts/taxi-1988/followup-1/luna-inventory/vpxtool-obj-vpu/Taxi (Williams 1988)1.2.obj, SHA256 dfb0965ef597f88e5c94bcb63cfbb6532a57394e15993707fe88a2dc6dc50cce; vpxtool git:v0.33.3 export obj --units vpu. Its x/y frame agrees with independently positioned sw14..16 wires and all six HitTargets; the export applies object transforms. Inverse rotation about the HitTarget position gives local XY bounds approximately[-20.9,20.9]/[-3.2,3.2] for all six targets. The -24 deg middle-bank and 90 deg right-bank rotations leave their world pivots fixed; oblique AABB center offsets are at most 0.041135 VPU and do not change target order. No primitive local position is admitted.

Ramp 33/34 use modeled animated wire sw33P/sw34P world-mesh bounds centers, respectively(202.405365,523.496430) and(697.897130,450.231950) VPU. Their pivots and invisible Trigger centers differ; they are neither averaged nor substituted. These are projected resting wire-actuation sites on the crossed ramps, supported by factory leaders 33/34 and separate script 242..262 Hit/Unhit routing. The table wires do not survey the physical microswitch bodies. Full raw export and independent remeasurement are retained externally.

## Concrete rejected mechanical classes

Playfield tilt 9: factory leader below the left apron; no retained contact object or established manual-to-table frame. Outhole 10 and trough 11/12: abstract stack occupancy, with Drain/BallRelease ball-transfer helpers and no individually modeled contacts. Shooter 22: script handlers exist but no sw22 in the 870-object extraction. Slings 18/20: collision-edge walls and animation geometry do not locate paired leaf contacts or actuator pivots/strike sites. Spinout 43: abstract stack occupancy and transfer/ejection helpers do not locate a microswitch. Spinout 44: invisible triangular circulation trigger on Bol30; stored center is outside its drag-point triangle, so it cannot locate a physical wire/contact. Coils 1/2: Drain/BallRelease do not establish outhole lever or feeder-crank locations. Each affected device carries its own limitation.

## Remaining physical and variant blockers

Every controlled flasher socket, the complete GI population and lamp 37's socket remain unproved; playfield lamps are placed on their script-bound table lights. Backbox and coin-door effects need quantities and routing even when playfield placement is not applicable. C1..C5 each 1p+1i, C6/C7 each 1p+1d, C8 two playfield, Jackpot 1p+2i, Joyride 1p from the wiring table. Dome PCB F/L designator capacity is not installed population proof. No glow helper, bulb centroid or invented socket is admitted.

The 82 recreation placements (35 mechanical anchors and 47 playfield lamps; 81 observed, lamp 37 candidate) do not earn author-ready credit. Prototype construction and full competition differences remain unresolved; only L3/L4/LG1/P5 archives are supplied. Acquired full factory manuals/OCR, exact VPX/script/world export, pinned source, legal ROM tables and successful retained traces settle the admitted claims. Ghidra cannot establish physical socket geometry or prototype construction.

Three equal-authority factory disagreements remain unresolved: Sol 14 duplicate auxiliary pin, Sol 17 downstream plug and Sol 16 load type. They remain promotion blockers even when public addresses are proved.
