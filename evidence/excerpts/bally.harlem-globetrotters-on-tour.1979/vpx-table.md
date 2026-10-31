# Harlem Globetrotters On Tour - retained table geometry and lamp lights

The retained table is `Harlem Globetrotters On Tour (Bally 1979).vpx` (JPSalas's 2009 VPX version 1.0, the embedded script header "VPX version by JPSalas 2009, version 1.0"; 6,864,896 bytes, SHA-256 `c6503062d2c4d49f2a16866be4df0df85c5ef000e21f7eed5a3e7ae3de8ed81e`), extracted with `vpxtool git:v0.33.3` (canonical extraction manifest `148b066da476d89ff9da2fcdba031a070f0de4fc2806b471a7dcef11949cc89d`, 551 files, 10,339,644 bytes). Its playfield bounds are `left=0 top=0 right=952 bottom=1974`, so a normalized coordinate is `x / 952` and `y / 1974`, rounded to six places. Wall objects use the mean of their drag points, HitTarget objects their stored position and every other object its stored centre. The objects are frozen in `tools/seeds/bally/harlem-globetrotters-on-tour-1979-spatial.json` so the curator reproduces without the table.

## Switch objects

The object each switch address is bound to by the script's own code: `dtDrop.initdrop array(d1, d2, d3, d4), array(1, 2, 3, 4)`, the saucer ball stacks `sw24` and `sw32`, the trough's `Drain` kicker for 8, and the `_Hit`/`_Spin`/`_Slingshot` handlers for the rest. Switch 34 has two handlers, `Sling1_Hit` and `Sling2_Hit`.

| address | VPX type | object | raw x | raw y | x | y |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 1 | HitTarget | d1 | 798.3502 | 449.3337 | 0.838603 | 0.227626 |
| 2 | HitTarget | d2 | 779.3819 | 517.5181 | 0.818678 | 0.262167 |
| 3 | HitTarget | d3 | 761.439 | 585.1897 | 0.799831 | 0.296449 |
| 4 | HitTarget | d4 | 741.4455 | 649.7849 | 0.778829 | 0.329172 |
| 8 | Kicker | Drain | 452.9053 | 1923.4078 | 0.475741 | 0.974371 |
| 17 | Spinner | sw17 | 123.591 | 590.886 | 0.129822 | 0.299334 |
| 22 | Trigger | sw22 | 752.9319 | 1349.8987 | 0.790895 | 0.683839 |
| 23 | Trigger | sw23 | 818.4827 | 1351.7721 | 0.859751 | 0.684788 |
| 24 | Kicker | sw24 | 436.7778 | 245.5556 | 0.458800 | 0.124395 |
| 25 | Spinner | sw25 | 518.5431 | 739.7603 | 0.544688 | 0.374752 |
| 26 | HitTarget | sw26 | 112.1976 | 1078.4199 | 0.117855 | 0.546312 |
| 27 | HitTarget | sw27 | 112.1976 | 1008.1868 | 0.117855 | 0.510733 |
| 28 | HitTarget | sw28 | 112.1976 | 937.9536 | 0.117855 | 0.475154 |
| 29 | HitTarget | sw29 | 112.1976 | 867.7205 | 0.117855 | 0.439575 |
| 30 | HitTarget | sw30 | 112.1976 | 797.4873 | 0.117855 | 0.403996 |
| 31 | Trigger | sw31 | 56.8415 | 1350.8262 | 0.059707 | 0.684309 |
| 32 | Kicker | sw32 | 680.1113 | 249.5556 | 0.714403 | 0.126421 |
| 33 | Spinner | sw33 | 351.7626 | 739.7603 | 0.369498 | 0.374752 |
| 34 | Wall | Sling1 | 279.3082 | 259.6796 | 0.293391 | 0.131550 |
| 34 | Wall | Sling2 | 786.5442 | 1096.6768 | 0.826202 | 0.555561 |
| 35 | HitTarget | sw35 | 828.1282 | 869.6934 | 0.869883 | 0.440574 |
| 36 | Wall | RightSlingshot | 645.8637 | 1389.6278 | 0.678428 | 0.703965 |
| 37 | Wall | LeftSlingshot | 144.5607 | 1348.9216 | 0.151849 | 0.683344 |
| 38 | Bumper | Bumper2 | 436.0708 | 525.6184 | 0.458058 | 0.266271 |
| 39 | Bumper | Bumper3 | 634.7125 | 420.5307 | 0.666715 | 0.213035 |
| 40 | Bumper | Bumper1 | 237.7596 | 421.7081 | 0.249747 | 0.213631 |

## Coil objects

The object each coil acts on: the trough's `Drain` kicker for the outhole kicker (7), the bumper and slingshot objects the ROM fires for their own switches, the two saucer kickers, the invisible flipper `RightLaneGate` that `vpmSolDiverter` swings for 17, and the three flippers the flipper callbacks move. `BallRelease` (the trough's kick object in the shooter lane) is a table helper, not a playfield device.

| address | VPX type | object | raw x | raw y | x | y |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 7 | Kicker | Drain | 452.9053 | 1923.4078 | 0.475741 | 0.974371 |
| 8 | Bumper | Bumper3 | 634.7125 | 420.5307 | 0.666715 | 0.213035 |
| 9 | Bumper | Bumper1 | 237.7596 | 421.7081 | 0.249747 | 0.213631 |
| 10 | Bumper | Bumper2 | 436.0708 | 525.6184 | 0.458058 | 0.266271 |
| 11 | Wall | LeftSlingshot | 144.5607 | 1348.9216 | 0.151849 | 0.683344 |
| 12 | Wall | RightSlingshot | 645.8637 | 1389.6278 | 0.678428 | 0.703965 |
| 13 | Kicker | sw24 | 436.7778 | 245.5556 | 0.458800 | 0.124395 |
| 14 | Kicker | sw32 | 680.1113 | 249.5556 | 0.714403 | 0.126421 |
| 17 | Flipper | RightLaneGate | 787.5615 | 1474.1357 | 0.827270 | 0.746776 |
| 46 | Flipper | RightFlipper | 602.1099 | 1630.744 | 0.632468 | 0.826111 |
| 48 | Flipper | LeftFlipper | 269.3163 | 1630.7438 | 0.282895 | 0.826111 |
| 48 | Flipper | LeftFlipper1 | 171.92 | 1500.3173 | 0.180588 | 0.760039 |

`RightLaneGate` is stored with `is_visible` false; `BallRelease` is at raw (831.2205, 1692.4579).

## Lamp lights

`vpmMapLights AllLamps` binds each light of the `AllLamps` collection to the lamp number in its timer interval. Every light below is listed with that number and the two bulb flags the table stores: `is_bulb_light` (the light is drawn as a bulb rather than an insert overlay) and `show_bulb_mesh` (the table draws a bulb model). A light that draws no bulb marks no lamp socket.

| light | lamp (timer interval) | is_bulb_light | show_bulb_mesh | raw x | raw y | x | y |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |
| l1 | 1 | false | false | 435.6533 | 1608.0542 | 0.457619 | 0.814617 |
| l2 | 2 | false | false | 435.5371 | 1489.9839 | 0.457497 | 0.754804 |
| l3 | 3 | false | false | 468.3512 | 1431.646 | 0.491966 | 0.725251 |
| l4 | 4 | false | false | 434.4653 | 1017.0055 | 0.456371 | 0.515200 |
| l5 | 5 | false | false | 358.6054 | 794.8102 | 0.376686 | 0.402639 |
| l500 | 5 | false | false | 510.6094 | 795.275 | 0.536354 | 0.402875 |
| l6 | 6 | false | false | 213.4864 | 768.7505 | 0.224250 | 0.389438 |
| l7 | 7 | false | false | 331.9931 | 179.3141 | 0.348732 | 0.090838 |
| l8 | 8 | false | false | 536.6408 | 176.4301 | 0.563698 | 0.089377 |
| l9 | 9 | false | false | 164.6778 | 804.4264 | 0.172981 | 0.407511 |
| l10 | 10 | false | false | 164.3123 | 1086.15 | 0.172597 | 0.550228 |
| l11 | 11 | false | false | 577.7794 | 1109.9741 | 0.606911 | 0.562297 |
| l12 | 12 | false | false | 243.0918 | 1210.3804 | 0.255349 | 0.613161 |
| l14 | 14 | false | false | 536.8732 | 1431.4136 | 0.563942 | 0.725134 |
| l15 | 15 | false | false | 289.1113 | 1109.9741 | 0.303688 | 0.562297 |
| l17 | 17 | false | false | 398.0009 | 1548.0894 | 0.418068 | 0.784240 |
| l18 | 18 | false | false | 504.3766 | 1489.7515 | 0.529807 | 0.754687 |
| l19 | 19 | false | false | 757.4415 | 1052.7983 | 0.795632 | 0.533332 |
| l20 | 20 | false | false | 415.7812 | 960.7594 | 0.436745 | 0.486707 |
| l200 | 20 | false | false | 454.8281 | 960.7594 | 0.477761 | 0.486707 |
| l21 | 21 | false | false | 718.8595 | 1026.7672 | 0.755105 | 0.520145 |
| l22 | 22 | false | false | 188.8497 | 718.9838 | 0.198372 | 0.364227 |
| l23 | 23 | false | false | 377.358 | 138.9153 | 0.396384 | 0.070372 |
| l24 | 24 | false | false | 765.7189 | 957.4791 | 0.804327 | 0.485045 |
| l25 | 25 | false | false | 165.1711 | 873.6597 | 0.173499 | 0.442583 |
| bumper2l | 26 | true | true | 436.889 | 559.3339 | 0.458917 | 0.283350 |
| l28 | 28 | false | false | 330.4824 | 1210.3804 | 0.347145 | 0.613161 |
| l30 | 30 | false | false | 381.8476 | 1290.7983 | 0.401100 | 0.653900 |
| l31 | 31 | false | false | 361.6269 | 1109.0444 | 0.379860 | 0.561826 |
| l33 | 33 | false | false | 468.9536 | 1548.5542 | 0.492598 | 0.784475 |
| l34 | 34 | false | false | 330.4302 | 1431.1812 | 0.347090 | 0.725016 |
| l35 | 35 | false | false | 555.2984 | 831.068 | 0.583297 | 0.421007 |
| l36 | 36 | false | false | 396.2577 | 905.443 | 0.416237 | 0.458684 |
| l360 | 36 | false | false | 473.8867 | 904.9782 | 0.497780 | 0.458449 |
| l37 | 37 | false | false | 791.3751 | 1239.6655 | 0.831276 | 0.627997 |
| l38 | 38 | false | false | 163.7481 | 671.1049 | 0.172004 | 0.339972 |
| l39 | 39 | false | false | 435.3686 | 124.5051 | 0.457320 | 0.063073 |
| l40 | 40 | false | false | 63.662 | 1213.1694 | 0.066872 | 0.614574 |
| l41 | 41 | false | false | 164.9049 | 943.3154 | 0.173219 | 0.477870 |
| bumper1l | 42 | true | true | 236.0001 | 458.8895 | 0.247899 | 0.232467 |
| bumper3l | 42 | true | true | 635.111 | 459.7784 | 0.667133 | 0.232917 |
| l43 | 43 | false | false | 288.2512 | 1381.081 | 0.302785 | 0.699636 |
| l44 | 44 | false | false | 539.1974 | 1209.9155 | 0.566384 | 0.612926 |
| l46 | 46 | false | false | 436.0019 | 1289.8687 | 0.457985 | 0.653429 |
| l47 | 47 | false | false | 435.0722 | 1109.5093 | 0.457009 | 0.562061 |
| l49 | 49 | false | false | 363.9511 | 1489.2866 | 0.382302 | 0.754451 |
| l50 | 50 | false | false | 399.3219 | 1431.0863 | 0.419456 | 0.724968 |
| l51 | 51 | false | false | 315.069 | 831.5044 | 0.330955 | 0.421228 |
| l52 | 52 | false | false | 377.1992 | 847.8024 | 0.396218 | 0.429484 |
| l520 | 52 | false | false | 492.4804 | 847.8024 | 0.517311 | 0.429484 |
| l53 | 53 | false | false | 662.3307 | 888.2701 | 0.695726 | 0.449985 |
| l54 | 54 | false | false | 137.6885 | 624.6774 | 0.144631 | 0.316453 |
| l55 | 55 | false | false | 492.0369 | 137.2883 | 0.516845 | 0.069548 |
| l56 | 56 | false | false | 687.5987 | 810.15 | 0.722268 | 0.410410 |
| l57 | 57 | false | false | 163.8475 | 1014.9013 | 0.172109 | 0.514134 |
| l58 | 58 | false | false | 681.5324 | 1004.2219 | 0.715895 | 0.508724 |
| l59 | 59 | false | false | 163.2132 | 1752.7333 | 0.171442 | 0.887909 |
| l60 | 60 | false | false | 624.2638 | 1209.9155 | 0.655739 | 0.612926 |
| l62 | 62 | false | false | 488.5292 | 1290.3335 | 0.513161 | 0.653664 |
| l63 | 63 | false | false | 506.1933 | 1109.5093 | 0.531716 | 0.562061 |

Lamp numbers with no light: 13, 27, 29, 45, 61. Four lamps have two insert lights each: 5 (`l5`, `l500`), 20 (`l20`, `l200`), 36 (`l36`, `l360`) and 52 (`l52`, `l520`). Only the three thumper bumper lights `bumper1l`, `bumper2l` and `bumper3l` are bulb lights with a bulb model; every other lamp light is an insert overlay with no bulb.

The table also has 20 lights named `gi1`-`gi20` with timer interval 100, outside the lamp range, all 20 of them bulb lights: the general illumination, which no PinMAME output drives.
