# `supreme_008` VPX script: compact I/O and mechanism evidence

Method: manual transcription from the retained extraction's `script.vbs`
(SHA-256 `f2bb8a48bd0aa49310d7e7e8bc165757d59d168110815ac1712dcc971e7a34ca`),
using VPX script line numbers. This is recreation implementation evidence. It
does not establish cabinet construction, fitted hardware, wiring, polarity,
quantity, or that this table is known working.

## Driver and output callbacks

- Lines 77-84 set `cGameName = "supreme_101"`, enable solenoids, and disable
  the script's default lamp path. Lines 130-145 load `spike1.vbs` and bind
  public coils: 1 trough, 2 auto plunger, 3 left flipper, 4 right flipper,
  5 combined slingshots, 7 combined left/right pops, 8 bottom pop, 9 drop-bank
  reset, and 10 control gate.
- Lines 148-203 configure the controller, make physical-all solenoid/lamp
  callbacks available, initialize four balls on `swTrough1` through
  `swTrough4`, set switches 21 through 18, configure the shooter-lane impulse
  helper for switch 1, and start the lamp timer.
- Lines 216-264 construct `LampObjs(n)` from `Light` objects named `Ln` and
  `gi<n>_<k>` and apply `Controller.ChangedLamps` levels to them. In this exact
  extraction every such `Light` has `show_bulb_mesh=false`; ordinary `Ln`
  lights use the playfield blueprint image. These are candidate render/lightmap
  coordinates, not observed physical lamp or GI sockets.

## Direct switch bindings and spatial objects

- Lines 272-307 bind `Trigger` objects `sw02`, `sw03`, `sw04`, `sw05`, `sw31`,
  `sw33`, `sw34`, `sw35`, `sw36`, `sw45`, `sw47`, `sw48`, `sw49`, `sw50`, and
  spinner `Spinner001` to public switches 2-5, 31, 33-36, 45, 47-50, and 46.
  Ramp exits 33 and 49 invert their table trigger state. The precise table
  object is a recreation collision/sensor proxy unless physical construction
  evidence says otherwise.
- Lines 516-567 bind trough kickers 1-5 to switches 21-17, update their local
  ball chain, kick a drain toward that chain, let coil 1 eject the first trough
  kicker, and let coil 2 auto-fire the shooter impulse. The script comments
  that the model has four balls and maps trough positions 21-17; this is not
  physical trough, ball-count, or drain proof.
- Lines 581-623 animate the named left/right flipper objects from coils 3/4.
  The observed coil position is therefore projected to the flipper pivot
  (`Flipper.center`), not an unrelated primitive origin.
- Lines 646-665 pulse switch 38 from `Bumper1` and shared switch 37 from each
  of `Bumper2` and `Bumper3`. Lines 1279-1329 pulse shared switch 6 from each
  named slingshot wall. Each shared route consequently has two table positions;
  this is not a physical circuit or quantity claim.
- Lines 696-731 and 842-855 map drop targets `sw1`/`sw2`/`sw3` to switches
  40/41/42 and make coil 9 raise all three. The three primary objects are
  droppable `Wall` polygons, so their drag-point centroids are used only as
  documented table-mechanism projections.
- Lines 1110-1192 bind invisible `HitTarget` objects `st1`-`st8` to switches
  26/25/24, 27/28/29, 44, and 32, with separate visual primitives and bouncer
  proxies. The exact bound hit-target center is recorded as a sensor proxy, not
  a verified physical switch.
- Lines 734-744 map coil 10 to `Gate003.Open` and set
  `ControlGateCoilCloses=True`, while explicitly instructing a future author to
  reverse it if ROM behavior proves otherwise. The table exposes a gate motion,
  not a validated physical polarity or ball path.

## Script limitations that remain coverage blockers

- Lines 751-792 state that slings and pops are kicked by VPX itself; their coil
  callbacks only mark the game on. No actual sling/pop coil actuation geometry
  is implemented.
- `DTAction` (lines 796-798) and `STAction` (lines 1130-1132) are empty in
  ROM mode. The local `Kicker1` behavior (lines 675-684) has no public
  controller binding, while the `Kicker2` body is commented out (lines 686-689).
  They are stubs/local simulation behavior rather than physical mechanism
  evidence.
- Coin/ticket peripherals have no playfield geometry or handler in the retained
  script. The script cannot establish whether coin meter, ticket meter, ticket
  dispenser, or ticket notch hardware is fitted.
