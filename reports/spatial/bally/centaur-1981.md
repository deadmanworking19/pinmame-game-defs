# Centaur (Bally, 1981) spatial review

Status: validated and promoted to `machines/author-ready/bally/centaur-1981.json`.

The matching source is the retained known-working `Centaur (Bally 1981) v2.0.0.vpx` at SHA-256 `2689607de4e6c9b267c56aa0d090ff340bf3a9220277dc8730a51dca5172a5bc`. Its retained extraction holds 2780 files totalling 255939052 bytes, manifest SHA-256 `389bab09c790c432b350972a1cf8acde0b94dd7b137f14e42d510377995d15b4`, and a fresh `vpxtool git:v0.33.3` extraction reproduces it file for file. Playfield bounds are `left=0 top=0 right=952.941 bottom=1976.471`, and every canonical coordinate is x/952.941 and y/1976.471 rounded to at most six fractional places. 123 placements are recorded.

## Evidence decisions

- The Bally game #1239 manual and its schematic set are the physical inventory, wiring and connector authority; the ROM's own solenoid self test and a gameplay run of the pinned LibPinMAME harness own the printed-to-public solenoid mapping and which lamp each auxiliary circuit is in play; pinned PinMAME owns controller topology; and the retained table supplies geometry, taken from the objects its script binds.
- Every placement names one physical object: a bulb, a trigger, a target, a bumper, a kicker or a wall. None is a centroid of several devices. The one split is switch 34, whose two faces per side triangle the table models as one wall.
- The top lanes follow the ROM over the A9 sheet's labels. The sheet prints TOP LEFT LANE at A9J2-7 (public 65) and TOP RIGHT LANE at A9J2-18 (public 97), but in play the ROM lights 97 for the top left rollover (switch 5) and 65 for the top right (switch 3); the switch table and Figure V put switch 5 at the left lane. So 97 is placed at the left-lane insert above switch 5 and 65 at the right, which is how the table binds them. Left, middle and right run in ascending x.
- Only the four chamber circuits drive two bulbs (67, 83, 99, 115): the schematic prints (2) against them and nothing else, and each is placed at both of its bulbs. Every other auxiliary circuit drives one.
- Public lamp 113 is an unwired circuit: the A9 sheet's harness list and a photograph of a Centaur's A9 board both show no wire at A9J2-11. It carries a controlled `unused` record, and its runtime state is the top-lane register's carry bit.
- Public 68, 84, 100 and 116 are bare matrix positions with no SCR behind them (`unused`); the table's star inserts on three of them are its author's addition.
- Backbox lamps, the displays, the knocker, the coin lockout, the K1 flipper relay and the cabinet switches take controlled `cabinet_or_service` records; the G.I. flasher feed (lamp 1), the trough switches and the sixth switch-column strobe (solenoid 17) are `internal_nonvisual`.

## Derived placements

- `pinmame.output.lamp:66, pinmame.output.lamp:82`: Slingshot lamps: the bulb meshes Bulb_Prim_029 (right) and Bulb_Prim_028 (left) that the table's l66 and l82 handlers light under each slingshot plastic. Their world-space mesh-bound centres from `vpxtool export obj --units vpu` (OBJ SHA-256 1724f7a309a34180828566dd50361ea44e09b7149016391f2e78329031007205) equal their stored primitive positions to six decimal places. The Light objects l66 and l82 are invisible placeholders in a row along the bottom edge, with l1, l68, l84, l98, l100 and l114, and are not positions.
- `pinmame.output.lamp:98, pinmame.output.lamp:114`: Thumper-bumper lamps: the centres of the bumper objects Bumper2 (right) and Bumper1 (left), the bumpers the l98 and l114 handlers light. The lamp sits inside the bumper body.
- `pinmame.output.lamp:67, 83, 99, 115`: Chamber lamp pairs: each address drives two bulbs, one either side of the Queen's Chamber lane; the placements are the two Light objects l<n> and l<n>a whose bulb meshes Bulb_Prim_<n> and Bulb_Prim_<n>a the same handler lights. The schematic prints (2) against each of these four circuits and against no other auxiliary circuit.
- `pinmame.input.switch:34`: 10 point rebound, five contacts: the table models each side triangle's two rubber faces as one chevron-shaped wall (Phys_Sensor_34 left, Phys_Sensor_34a right) and the upper-right rebound as a third (Phys_Sensor_34b). Each chevron is split at its apex, along the line from the inner apex point to the midpoint of the two outer apex points, and each face's contact is the area centroid of its arm; the upper-right contact is the area centroid of its wall. Figure V draws two 34 contacts on each triangle and one at the upper right.
- `pinmame.output.solenoid:12, pinmame.output.solenoid:13`: Slingshot coils: the drag-point centroids of the LeftSlingshot and RightSlingshot walls; switches 38 and 37 share them, because the slingshot switch is the wall itself.
- `pinmame.output.solenoid:1, 2, 3, 4, 5, 8, 9`: Drop-target coils, unchanged from the earlier validated pass: each individual drop coil of the right four-bank at its target's drop-target primitive, and each bank reset (1 ORBS, 8 in-line, 9 right four) at the middle of its bank's four targets. Each lies within 0.001 of the corresponding primitive positions or their mean, which this report checks.
- `pinmame.output.solenoid:7, 14, 15, 20`: Kicker and magnet coils at the table's own objects for them: the outhole kicker at Drain (switch 8 shares it), the ball kick at BallRelease, the ball release at SubBallRelease, and the magnet at RMagTrig.

## Excluded table objects

- Light objects parked in a row along the bottom edge (l1, l66, l68, l82, l84, l98, l100, l114), which are invisible placeholders for addresses the table lights through other objects or not at all
- l68a, l84a and l100a, playfield star inserts the table drives from the bare matrix positions 68, 84 and 100, which the AS-2518-43 cannot light
- render doubles stacked on a placed object: l<n>a beside each main-board l<n>, l<n>mid and l<n>top beside each chamber bulb, and the sw<n>p, sw<n>a and sw<n>o primitives on each target
- bumperbiglight and bumpersmalllight helpers, whose timer_interval values are not lamp bindings, and the cabinet UndercabLight
- LEDnnn objects, which are the seven-segment display digits rendered as lights

## Unresolved

None.
