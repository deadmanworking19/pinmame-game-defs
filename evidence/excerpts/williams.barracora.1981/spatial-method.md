# Williams Barracora (game 510) - Spatial method and retained table geometry

Sources:

- Retained community table `Barracora (1981).vpx`, SHA-256 `e40287ad8a3d02feeae7b2ff56a902cb34e5f5b7ae8706e1097ddcba9fc54157`, 51494912 bytes, author Dids666 (embedded table info: release date Jan 2018, VPX 10.5), retained externally at `external:pinmame-vpx-sources/williams/barracora-1981/`. It came from the user's read-only table archive; no download URL is asserted and the table is not known to have been played.
- Its vpxtool (git:v0.33.3) extraction `extracted-vpxtool`: 942 files, 63012816 bytes, manifest SHA-256 `73f08b62e2034ef2a37bd5f059ead966a8aa77f9449a7832c8335018cde061b3`. `gamedata.json` gives table bounds left 0, top 0, right 952, bottom 1974.
- The table's embedded script `script.vbs`, SHA-256 `fb33726ee06aab0a5d4edde731e569c3178f558d95fa65c151b78da445d538bf` (bindings in `script-bindings.md`).

Method: object fields were read from the extracted `gameitems/*.json` files; every object used, its file hash and the fields read are pinned in `tools/seeds/williams/barracora-1981-spatial.json`. Coordinates are normalized as x = (x - left) / (right - left) and y = (y - top) / (bottom - top), rounded to six decimals with the repository helper. No drawing callout check was made, so every placement is `observed`.

## Objects and how a point is taken

| Public address | Object | Type | Point |
|---|---|---|---|
| switch 9 | `sw9` | Trigger, star, invisible | center |
| switch 10 | `sw10` | Kicker, invisible | center |
| switch 11 | `sw11` | Kicker, cup2 | center |
| switch 16 | `sw16` | Trigger, wire_a | mean of its four drag points |
| switches 17, 18, 19 | `sw17`, `sw18`, `sw19` | Trigger, star, invisible | center |
| switches 20, 21, 22 | `sw20`, `sw21`, `sw22` | Bumper | center (skirt switch projected onto the bumper) |
| switches 23, 24, 31, 32 | `sw23`, `sw24`, `sw31`, `sw32` | Trigger, star, invisible | center |
| switch 25 | `sw25` | Spinner | center |
| switch 26 | `sw26` | Trigger, button, invisible | center |
| switches 27, 28, 33 | `sw27`, `sw28`, `sw33` | HitTarget, round | position |
| switches 41-48 | `sw41` ... `sw48` | HitTarget, drop target | position |
| switch 29, solenoid 21 | `LeftSlingshot` | Wall | midpoint of its one slingshot edge |
| switch 30, solenoid 22 | `RightSlingShot` | Wall | midpoint of its one slingshot edge |
| solenoids 1-8 | `sw41` ... `sw48` (1 raises 41 ... 8 raises 48) | HitTarget | position (reset coil projected onto its target) |
| solenoid 9 | `sw41`, `sw42`, `sw43` | HitTarget | mean of the three positions (bank release projected onto the bank) |
| solenoid 10 | `sw44` ... `sw48` | HitTarget | mean of the five positions |
| solenoids 13, 14 | `sw10`, `sw11` | Kicker | center |
| solenoid 17 | `Gate1` | Gate, long_plate, one-way, length 80, rotation 69 | center |
| solenoids 18, 19, 20 | `sw20`, `sw21`, `sw22` | Bumper | center |

The bumper objects are named for their special switches: `sw20` is the left bumper (344.6, 624.5), `sw21` the right (546.4, 622.2) and `sw22` the bottom (445.1, 789.0), which matches PinMAME's special-switch pairing 20 -> 18, 21 -> 19, 22 -> 20 and Table 4's coil names. The left drop-target bank runs `sw43` (top, y 902.8), `sw42`, `sw41` (bottom, y 1023.6); the right bank runs `sw44` (top, y 919.3) to `sw48` (bottom, y 1142.4), which agrees with the booklet's "top 'A' target down (switch 44)" (`diagnostics.md`).

`Gate1` sits at (200.1, 167.0), at the mouth of the upper eject hole kicker `sw10` (185.2, 169.1). It is a visible one-way plate gate. The VR Room script opens it while solenoid 17 is energized and closes it when 17 drops; the Dids666 lineage script opens it and closes it from the shooter-lane trigger instead (`script-bindings.md`).

## Not placed

- Switch 12 (outhole): `Drain_Hit` on the bottom kicker `Drain` (650.2, 1950.1) sets 12, while an invisible star Trigger also named `sw12` sits at the lower left (148.6, 1825.4). Figure 3 prints `12` at the lower left (`switch-matrix.md`), which favours the trigger's side, but its callout was not measured and the two table objects disagree.
- Switches 13, 14 and 15 (ball ramp positions): the script's `bsTrough` ball stack abstracts them; no sensor object exists.
- Switch 36 (playfield tilt): no object.
- Switches 37-40: invisible Trigger strips with shape `none` along rubbers. Drag points: `sw37` (637.1, 212.6), (593.1, 270.7), (618.6, 268.7), (639.6, 242.2); `sw38` (163.9, 644.6), (201.9, 754.0), (232.2, 779.7), (165.1, 596.2); `sw39` (791.3, 911.2), (822.5, 1150.6), (839.6, 1138.0), (806.1, 909.0); `sw40` (57.6, 1100.2), (82.7, 1187.6), (107.2, 1191.4), (74.1, 1073.6). The chart calls 38 `LOWER / STANDUP` although its strip, like Figure 3's unmeasured `38` callout, is on the left side beside the upper half of the playfield. A strip is where the table counts a rubber hit, not where a leaf switch is.
- Solenoids 11 and 12: `Drain` and the disabled, invisible `BallRelease` kicker (832.0, 1756.5) are ball-stack helpers, not the outhole kicker or the thrower.
- Lamps 7-64: the table maps them through `vpmMapLights AllLights` (102 lights) onto insert Light objects, none of which shows a bulb mesh. Only `Light99` (342.1, 621.7, timer interval 62), `Light100` (545.1, 623.1, 61) and `Light101` (443.9, 788.8, 60) show bulb meshes; they sit under the three jet bumpers, are not in `AllLights` and are not named by the script, so no public lamp drives them.

## Not applicable

Lamps 1-6 are backbox insert-board lamps (`insert-board.md`, `lamp-wiring.md`); switches 1-8, solenoid 15 (bell) and 16 (coin lockout) are cabinet or service devices; solenoid 25 (Z1 flipper relay) is internal; 34, 35 and 45-48 are PinMAME's flipper-button copies and fabricated flipper outputs.

## Notes

- The table's collections `GI`, `Lights`, `LaneLights`, `BumperLights` and `outlights` are empty.
- The normalization bounds are the table's own; no point lies outside them.
