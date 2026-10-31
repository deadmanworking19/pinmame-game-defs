# Frontier - retained table geometry, lamp lights and bulb meshes

The retained table is `Frontier (Bally 1980).vpx` (bord, "Sept 2016", "Update to 2.0 March 2017", saved by VP 10.2; 55,447,552 bytes, SHA-256 `39a399a28bff018efc10e91109bf455f2702516c10b10c18764ac31a12a8dbf2`), the only Frontier table in the local table archive, kept with its backglass `Frontier (Bally 1980).directb2s` (SHA-256 `570e36792ab44bb4e9baf1245e5f5be49036ea1595d72802fe83c79aff9cce17`). It was extracted with `vpxtool git:v0.33.3` (canonical extraction manifest `a463dacd3606d3ecc9920adb64223b9c2b9d2d5a79f76209a7571efbad7950ec`, 1,068 files, 68,276,966 bytes). Its playfield bounds are `left=0 top=0 right=952 bottom=1974`, so a normalized coordinate is `x / 952` and `y / 1974`, rounded to six places. The objects are frozen in `tools/seeds/bally/frontier-1980-spatial.json` (written by `tools/frontier_spatial_seed.py`) so the curator reproduces without the table.

## Switch objects

The object each switch address is bound to by the script's own handlers. Walls use the mean of their drag points, triggers, bumpers, spinners and kickers their stored centre, hit targets their stored position. The drop targets are the `HitTarget` objects the script's `dtLL` and `dtRR` banks hold. Switch 1 has four objects, the four rebound rubbers `sw1a1`-`sw1a4` whose `_hit` handlers all pulse 1.

| address | VPX type | object | method | raw x | raw y | x | y |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | Wall | sw1a1 | drag_point_centroid | 201.0605 | 440.7926 | 0.211198 | 0.223299 |
| 1 | Wall | sw1a2 | drag_point_centroid | 175.9423 | 569.9506 | 0.184813 | 0.288729 |
| 1 | Wall | sw1a3 | drag_point_centroid | 87.331 | 991.9701 | 0.091734 | 0.502518 |
| 1 | Wall | sw1a4 | drag_point_centroid | 639.9109 | 433.4591 | 0.672175 | 0.219584 |
| 2 | Trigger | sw2 | center | 812.4445 | 1406.5677 | 0.853408 | 0.712547 |
| 3 | Trigger | sw3 | center | 747.6544 | 1407.3582 | 0.785351 | 0.712947 |
| 4 | Trigger | sw4 | center | 115.1852 | 1405.7778 | 0.120993 | 0.712147 |
| 5 | Trigger | sw5 | center | 50.0 | 1404.5928 | 0.052521 | 0.711547 |
| 8 | Kicker | Drain | center | 484.0341 | 1830.4049 | 0.508439 | 0.927257 |
| 12 | Kicker | sw12 | center | 748.8148 | 514.2963 | 0.786570 | 0.260535 |
| 13 | Trigger | sw13 | center | 330.284 | 325.2838 | 0.346937 | 0.164784 |
| 14 | Trigger | sw14 | center | 431.8148 | 328.4443 | 0.453587 | 0.166385 |
| 15 | Trigger | sw15 | center | 532.1605 | 328.8394 | 0.558992 | 0.166585 |
| 21 | HitTarget | sw21 | position | 83.8871 | 579.923 | 0.088117 | 0.293781 |
| 22 | HitTarget | sw22 | position | 105.3517 | 646.9556 | 0.110664 | 0.327738 |
| 23 | HitTarget | sw23 | position | 126.6862 | 714.7097 | 0.133074 | 0.362062 |
| 24 | HitTarget | sw24 | position | 170.0022 | 217.7846 | 0.178574 | 0.110327 |
| 25 | Trigger | sw25 | center | 722.5345 | 394.9178 | 0.758965 | 0.200060 |
| 27 | Spinner | sw27 | center | 758.0027 | 722.4294 | 0.796221 | 0.365972 |
| 29 | HitTarget | sw29 | position | 83.3333 | 872.4443 | 0.087535 | 0.441968 |
| 30 | HitTarget | sw30 | position | 432.5208 | 839.1269 | 0.454329 | 0.425090 |
| 31 | HitTarget | sw31 | position | 661.9449 | 727.3588 | 0.695320 | 0.368469 |
| 33 | HitTarget | sw33 | position | 801.5836 | 999.1458 | 0.842000 | 0.506153 |
| 34 | HitTarget | sw34 | position | 789.5527 | 944.8622 | 0.829362 | 0.478654 |
| 35 | HitTarget | sw35 | position | 775.8802 | 879.3964 | 0.815000 | 0.445490 |
| 36 | Wall | RightSlingShot | drag_point_centroid | 631.4842 | 1412.5614 | 0.663324 | 0.715583 |
| 37 | Wall | LeftSlingShot | drag_point_centroid | 227.7541 | 1413.8157 | 0.239237 | 0.716219 |
| 38 | Bumper | sw38 | center | 432.053 | 739.0955 | 0.453837 | 0.374415 |
| 39 | Bumper | sw39 | center | 531.6086 | 541.1696 | 0.558412 | 0.274149 |
| 40 | Bumper | sw40 | center | 313.5345 | 540.577 | 0.329343 | 0.273849 |

Switch 8's object is the `Drain` kicker, the hole the ball drains into (`bsTrough.InitSw 0,8`); the table's `BallRelease` kicker, which throws the ball into the shooter lane, is a table helper. Switch 12 is the saucer kicker `sw12`, which the saucer coil's callback kicks at -10 degrees (towards the back, slightly left).

## Flippers and the gate

| object | VPX type | method | raw x | raw y | x | y |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| LeftFlipper | Flipper | center | 270.9762 | 1643.2887 | 0.284639 | 0.832466 |
| RightFlipper | Flipper | center | 592.0886 | 1643.289 | 0.621942 | 0.832467 |
| Gate2 | Gate | center | 618.901 | 216.099 | 0.650106 | 0.109473 |

`Gate2` is invisible, one-way (`two_way` false) and opened by `vpmSolGate Gate2,true` while output 17 is on. It sits at the top of the upper-right lane, above the star rollover `sw25` and the saucer `sw12`, which matches the order Figure V and the eject-saucer drawing show.

## Lamp lights

Every lamp light the table contains, with its bulb flags. The script binds `L<n>` to lamp n, except that lamps 10, 26 and 42 are bound to the collections `BumperLeft` (`BumperLight2`, `L10`), `BumperCenter` (`BumperLight3`, `L26`) and `BumperRight` (`BumperLight1`, `L42`). `L48` exists, beside the saucer rollover, but 48 is a decoder hole and the script leaves `Lights(48)` unbound. There is no `L13`, `L27`, `L29`, `L43`, `L45` or `L61`. `L59` lies outside the playfield at raw (-101.3, 2040.1).

Only `L10`, `L26` and `L42` (and the bumper lights `BumperLight1`-`BumperLight3` beside them) are bulb-mode lights, and none of these three lamp lights and the three bumper lights shows a bulb mesh. The other lamp lights are classic lights drawn over the inserts.

| light | raw x | raw y | is_bulb_light | show_bulb_mesh |
| --- | ---: | ---: | --- | --- |
| L1 | 364.0842 | 1531.9434 | false | false |
| L10 | 312.536 | 541.3055 | true | false |
| L11 | 433.6353 | 1696.9421 | false | false |
| L12 | 115.476 | 1283.3351 | false | false |
| L14 | 706.974 | 1049.0989 | false | false |
| L15 | 536.2628 | 152.305 | false | false |
| L17 | 434.3752 | 1531.9432 | false | false |
| L18 | 434.3752 | 1462.022 | false | false |
| L19 | 433.6352 | 1392.471 | false | false |
| L2 | 363.3443 | 1460.097 | false | false |
| L20 | 433.6352 | 1321.4402 | false | false |
| L21 | 433.6352 | 1251.8889 | false | false |
| L22 | 431.7292 | 205.6067 | false | false |
| L23 | 284.4691 | 1038.4266 | false | false |
| L24 | 580.1365 | 1038.4265 | false | false |
| L25 | 430.002 | 913.9529 | false | false |
| L26 | 431.0545 | 739.824 | true | false |
| L28 | 747.3552 | 1285.5548 | false | false |
| L3 | 362.6043 | 1391.7312 | false | false |
| L30 | 695.8754 | 990.6462 | false | false |
| L31 | 361.8645 | 1606.6737 | false | false |
| L33 | 504.6662 | 1532.6832 | false | false |
| L34 | 503.9263 | 1461.2822 | false | false |
| L35 | 503.1864 | 1391.7312 | false | false |
| L36 | 503.1864 | 1320.7004 | false | false |
| L37 | 503.1864 | 1251.1492 | false | false |
| L38 | 530.8765 | 206.3466 | false | false |
| L39 | 355.9452 | 1011.0501 | false | false |
| L4 | 362.6043 | 1320.7004 | false | false |
| L40 | 733.6105 | 790.132 | false | false |
| L41 | 622.9255 | 808.7219 | false | false |
| L42 | 530.6101 | 541.8981 | true | false |
| L44 | 57.7634 | 1282.5952 | false | false |
| L46 | 684.0369 | 932.9336 | false | false |
| L47 | 434.3752 | 1608.1534 | false | false |
| L48 | 725.4717 | 394.2827 | false | false |
| L49 | 248.659 | 1221.9231 | false | false |
| L5 | 363.7895 | 1251.1492 | false | false |
| L50 | 616.3919 | 1221.9232 | false | false |
| L51 | 432.8954 | 1176.0491 | false | false |
| L52 | 498.007 | 1086.5204 | false | false |
| L53 | 643.0286 | 1082.0812 | false | false |
| L54 | 75.8347 | 427.5783 | false | false |
| L55 | 432.1555 | 1002.1711 | false | false |
| L56 | 89.8929 | 360.987 | false | false |
| L57 | 368.5236 | 1085.7805 | false | false |
| L58 | 432.1555 | 1085.7805 | false | false |
| L59 | -101.2593 | 2040.0752 | false | false |
| L6 | 331.1021 | 205.6067 | false | false |
| L60 | 811.7269 | 1285.555 | false | false |
| L62 | 671.4586 | 874.4811 | false | false |
| L63 | 504.6662 | 1608.1534 | false | false |
| L7 | 222.0224 | 1081.3411 | false | false |
| L8 | 507.6258 | 1011.05 | false | false |
| L9 | 128.0476 | 956.9221 | false | false |

The table places four lamp lights on the opposite side to the factory sheets. `L12` (bound to lamp 12, commented "LeftReturnLane") is over the left flipper feed lane at x 115 and `L28` ("RightReturnLane") over the right at x 747; `L44` ("LeftLaneSpecial") is over the left outlane at x 58 and `L60` ("RightLaneSpecial") over the right at x 812. The sheets name lamp 12 RIGHT FLIP. FEED LANE, 28 LEFT FLIP. FEED LANE, 44 RIGHT OUT SPECIAL and 60 LEFT OUT SPECIAL, and the ROM agrees (see the plug-connector and lamp-driver excerpts).

## Bulb meshes

The table models bulbs as `BulbFil<n>` and `BulbTop<n>` primitives (27 of each, numbers 1-28 without 21). Each is listed with the nearest `Light` object of any kind, by Euclidean distance in table units. Every one sits on a general-illumination light: a `GI_<n>` or `Light8` member of the table's `GI` collection, or `GI_12a`, `GI_13a` or `GI_14a` of the drop-target light collections `DTLeftLights` and `DTRightLights` that the script switches itself. No bulb primitive sits on a lamp light: the nearest lamp light to any bulb primitive is `L9`, 64.6 units away.

| bulb primitive | raw x | raw y | nearest light | distance |
| --- | ---: | ---: | --- | ---: |
| BulbFil1 | 215.6257 | 1501.2485 | GI_19 | 1.451 |
| BulbFil10 | 630.4406 | 346.2858 | GI_10 | 2.641 |
| BulbFil11 | 168.9455 | 67.0011 | GI_7 | 0.467 |
| BulbFil12 | 853.536 | 138.8784 | GI_2 | 1.567 |
| BulbFil13 | 776.1429 | 66.8904 | GI_1 | 2.219 |
| BulbFil14 | 698.4254 | 604.7195 | GI_11 | 3.973 |
| BulbFil15 | 833.885 | 965.5449 | GI_14a | 0.437 |
| BulbFil16 | 817.885 | 894.4338 | GI_13a | 0.776 |
| BulbFil17 | 811.959 | 1123.7671 | GI_23 | 1.212 |
| BulbFil18 | 643.6627 | 1503.6188 | GI_21 | 2.889 |
| BulbFil19 | 165.8479 | 1353.693 | GI_18 | 0.521 |
| BulbFil2 | 696.4034 | 1356.6559 | GI_20 | 1.218 |
| BulbFil20 | 47.3294 | 1078.7301 | GI_22 | 1.06 |
| BulbFil22 | 63.922 | 966.1374 | GI_17 | 0.829 |
| BulbFil23 | 41.9961 | 817.3967 | GI_16 | 2.163 |
| BulbFil24 | 159.3294 | 600.508 | GI_12a | 0.174 |
| BulbFil25 | 480.9199 | 318.9393 | GI_6 | 6.427 |
| BulbFil26 | 480.9199 | 318.9393 | GI_6 | 6.427 |
| BulbFil27 | 577.6317 | 318.3619 | GI_4 | 2.655 |
| BulbFil28 | 281.928 | 318.9545 | GI_3 | 2.901 |
| BulbFil3 | 64.804 | 139.2808 | GI_5 | 2.028 |
| BulbFil4 | 226.2924 | 269.2488 | GI_8 | 2.079 |
| BulbFil5 | 281.928 | 318.9545 | GI_3 | 2.901 |
| BulbFil6 | 380.959 | 319.6191 | GI_15 | 2.497 |
| BulbFil7 | 185.9961 | 367.6191 | GI_9 | 0.759 |
| BulbFil8 | 380.959 | 319.6191 | GI_15 | 2.497 |
| BulbFil9 | 577.6317 | 318.3619 | GI_4 | 2.655 |
| BulbTop1 | 696.6334 | 1357.0857 | GI_20 | 1.392 |
| BulbTop10 | 630.6704 | 346.7156 | GI_10 | 2.326 |
| BulbTop11 | 168.7804 | 67.0359 | GI_7 | 0.533 |
| BulbTop12 | 853.7659 | 139.3082 | GI_2 | 1.205 |
| BulbTop13 | 776.3729 | 67.3202 | GI_1 | 1.732 |
| BulbTop14 | 698.6554 | 605.1494 | Light8 | 3.875 |
| BulbTop15 | 834.1149 | 965.9747 | GI_14a | 0.856 |
| BulbTop16 | 818.1149 | 894.8636 | GI_13a | 0.353 |
| BulbTop17 | 812.189 | 1124.1969 | GI_23 | 1.679 |
| BulbTop18 | 643.8927 | 1504.0486 | GI_21 | 3.371 |
| BulbTop19 | 166.0779 | 1354.1228 | GI_18 | 0.99 |
| BulbTop2 | 215.8556 | 1501.6783 | GI_19 | 1.927 |
| BulbTop20 | 47.5593 | 1079.1599 | GI_22 | 0.708 |
| BulbTop22 | 64.1519 | 966.5673 | GI_17 | 1.291 |
| BulbTop23 | 42.226 | 817.8265 | GI_16 | 1.688 |
| BulbTop24 | 159.5593 | 600.9378 | GI_12a | 0.544 |
| BulbTop25 | 481.1498 | 319.3691 | GI_6 | 6.01 |
| BulbTop26 | 481.1498 | 319.3691 | GI_6 | 6.01 |
| BulbTop27 | 577.8616 | 318.7917 | GI_4 | 2.198 |
| BulbTop28 | 282.1579 | 319.3843 | GI_3 | 2.486 |
| BulbTop3 | 65.0339 | 139.7106 | GI_5 | 2.107 |
| BulbTop4 | 226.5223 | 269.6786 | GI_8 | 1.696 |
| BulbTop5 | 282.1579 | 319.3843 | GI_3 | 2.486 |
| BulbTop6 | 381.1889 | 320.0489 | GI_15 | 2.038 |
| BulbTop7 | 186.226 | 368.0489 | GI_9 | 1.242 |
| BulbTop8 | 381.1889 | 320.0489 | GI_15 | 2.038 |
| BulbTop9 | 577.8616 | 318.7917 | GI_4 | 2.198 |
