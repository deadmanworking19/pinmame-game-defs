# Williams Blackout (game 495) - Spatial method and retained table geometry

Sources:

- Retained community table `Blackout (Williams 1980)-S34 v1.1.vpx`, SHA-256 `cc51bd61f64e8a614eb059c3f6cac183ab93d9e18d7088deb5c950f13534c4e3`, 32137216 bytes, retained externally at `external:pinmame-vpx-sources/williams/blackout-1980/`. It came from the user's read-only table archive; no download URL is asserted, its embedded table info names no author (only `author_website` `http://www.vpforums.org/`), and it is not known to have been played.
- Its vpxtool (git:v0.33.3) extraction `extracted-vpxtool`: 911 files, 44095253 bytes, manifest SHA-256 `89c90de651f993411e090234da2fe3306ae31e56fdb10c233e0620cbe72a2d71`. `gamedata.json` gives table bounds left 0, top 0, right 952, bottom 1974.
- The table's embedded script `script.vbs`, SHA-256 `4fe2fef60af899fc019e7a4adceab63c067e1e668448b3f704787cbbb08825b9` (bindings in `script-bindings.md`).

Method: object fields were read from the extracted `gameitems/*.json` files; every object used, its file hash and the fields read are pinned in `tools/seeds/williams/blackout-1980-spatial.json`. Coordinates are normalized as x = (x - left) / (right - left) and y = (y - top) / (bottom - top), rounded to six decimals with the repository helper. No drawing callout check was made, so every placement is `observed`.

## Objects and how a point is taken

| Public address | Object | Type | Point |
|---|---|---|---|
| switches 10, 45, 42, 41 | `sw10`, `sw45`, `sw42`, `sw41` | Trigger, wire_a, visible | center |
| switches 29, 30, 31 | `sw29`, `sw30`, `sw31` | Trigger, wire_a, visible | center |
| switches 11-15 | `sw11` ... `sw15` | HitTarget, round | position |
| switch 20 | `sw20` | HitTarget, fat rectangle | position |
| switches 25, 26, 27 | `sw25`, `sw26`, `sw27` | HitTarget, drop target | position |
| switches 33, 34, 35 | `sw33`, `sw34`, `sw35` | HitTarget, drop target | position |
| switch 18 | `Spinner3` | Spinner | center |
| switch 37 | `Spinner1` | Spinner | center |
| switch 39 | `Spinner2` | Spinner | center |
| switch 40, solenoid 6 | `sw40` | Kicker, cup2 | center |
| switch 22, solenoid 17 | `Bumper1` | Bumper | center (skirt switch and coil projected onto the bumper) |
| switch 21, solenoid 18 | `Bumper2` | Bumper | center |
| switch 23, solenoid 19 | `Bumper3` | Bumper | center |
| switch 44, solenoid 20 | `LeftSlingShot` | Wall | midpoint of its one slingshot edge |
| switch 43, solenoid 21 | `RightSlingShot` | Wall | midpoint of its one slingshot edge |
| switch 28, solenoid 4 | `sw25`, `sw26`, `sw27` | HitTarget | mean of the three positions (series switch and reset coil projected onto the bank) |
| switch 36, solenoid 5 | `sw33`, `sw34`, `sw35` | HitTarget | mean of the three positions |

The table's objects agree with the booklet's charts and drawings (`switch-matrix.md`, `solenoid-connections.md`). `Bumper1` (287.4, 438.9) is the upper left jet bumper, `Bumper2` (494.6, 443.1) the upper right one and `Bumper3` (382.6, 613.1) the bottom one; the script pulses 22, 21 and 23 from them, which is the chart's left, right and bottom jet bumper, and Figure 3 prints 17 on the left, 18 on the right and 19 on the bottom bumper. The green targets run from `sw11` (69.9, 977.6) at the bottom to `sw15` (106.0, 758.5) at the top, as the chart's `Green Target #1 Bottom` and `#5 Top` say. The centre 3-bank `sw25`-`sw27` (332.9-449.6, 751.1-769.4) lies below the bottom bumper, and the top 3-bank `sw33`-`sw35` (628.2-719.0, 148.2-217.6) is at the upper right, where Figure 3 prints 04 and 05. `Spinner3` (118.6, 617.5) is on the left, `Spinner1` (813.7, 229.7) at the upper right and `Spinner2` (782.7, 740.3) at the middle right, matching switches 18, 37 and 39. The eject hole `sw40` (781.9, 962.3) is on the right side, where Figure 3 prints 06.

## Not placed

- Switch 9 (outhole) and solenoid 1 (ball release): the script's one-ball `bsTrough` sets 9 from the hit handler of the invisible kicker `Drain` (414.0, 1827.5) and kicks out through the invisible kicker `BallRelease` (812.1, 1611.5). Both are ball-stack helpers, not the outhole switch or the coil, and Figure 3's `01` and Figure 4's dashed `09` callouts were not measured.
- Switches 19 and 38 (standups): each is a rubber Wall with one slingshot edge that pulses the switch. Drag points: `sw19` (123.8, 482.6), (168.6, 568.4), (197.5, 579.8, slingshot edge start), (128.2, 441.8); `sw38` (755.5, 550.8, slingshot edge start), (699.4, 696.2), (751.8, 673.2), (774.2, 592.3). A rubber edge is where the table counts a hit, not where the leaf switch is.
- Switch 32 (playfield tilt): no object or binding. Figure 4 prints 32 near the base of the right flipper; the callout was not measured.
- Lamps 1-10, 12-49 and 56: the script maps them onto insert Light objects `l1` ... `l49`, none of which shows a bulb mesh, and no light object exists for 56 (the playfield credits lamp). The drawing set's lamp page is a wiring diagram, not a location drawing.

## General illumination

The table's `GI` collection holds 70 Light objects. The embedded script switches every one of them off while solenoid 15 (Special Relay) is energized and back on when it drops (`script-bindings.md`). 24 of them show a bulb mesh: `gi2`, `gi6`, `gi7`, `gi11`, `gi13`, `gi17`, `gi20`, `gi22`, `gi26`, `gi29`, `gi32`, `gi35`, `gi38`, `gi41`, `gi44`, `gi47`, `gi55`, `gi58`, `gi61`, `gi64`, `gi69`, `gi70`, `gi71` and `gi72`. No public lamp drives them and they are not placed: the G.I. strings have no controller address, and the drawing set draws the playfield G.I. string with four bulbs and a dashed continuation and prints no count (`lamp-wiring.md`), so the table's bulbs are neither a stock socket count nor socket positions. Their centers are listed in the spatial report.

## Not applicable

Lamps 50-55 and 57-64 are backbox insert-board lamps (`insert-board.md`, `lamp-wiring.md`); lamp 11 is unused. Switches 1-8, the cabinet flipper buttons and the service inputs are cabinet or service devices; switches 16, 17, 24 and 47-64 are unused; switch 46 is PinMAME's copy of the right flipper button. Solenoids 2, 3, 7, 8 and 22 are unused; 9-13 (sound lines), 14 (knocker), 15 (Special Relay), 16 (coin lockout) and 23 (game-on relay) are backbox, cabinet or internal devices; 45-48 are PinMAME's fabricated flipper outputs.

## Notes

- The normalization bounds are the table's own; no point lies outside them.
- No object of the table is named for switch 32, 46 or any unused address.
