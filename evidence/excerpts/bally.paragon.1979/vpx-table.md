# Paragon - retained table geometry and the playfield art under each lamp

The retained table is `Paragon (Bally 1979).vpx` (bord, script header version 2.37; downloaded from VPUniverse inside `Paragon (Bally 1979).zip`; 204,705,792 bytes, SHA-256 `3c83b8787112f82880ae7c3ff2f6fbddb846029562359300db13691ea8dcb094`), extracted with `vpxtool git:v0.33.3` (canonical extraction manifest `0356d2d0bfe7c78c786196e4af7f6ec82e086108ec413420700c5679a72cdef6`). Its playfield bounds are `left=0 top=0 right=1257 bottom=1974`, so a normalized coordinate is `x / 1257` and `y / 1974`, rounded to six places. The objects are frozen in `tools/seeds/bally/paragon-1979-spatial.json` so the curator reproduces without the table.

The collidable primitives `sw27a` and `sw34b` are stored at position (0,0,0) with no rotation and their geometry baked into the mesh. Scaling the extracted OBJ vertices by the primitive's size (185.274) gives world coordinates: the same transform applied to the visible baked primitive `rubbers_visible` reproduces the bounding box of that object in a `vpxtool export obj --units vpu` export of the table (x 45.1-1141.5, y 251.7-1491.0 both ways). `sw27a` has two connected pieces, one per 500-point rebound rubber; `sw34b` has one, the rubber beside the right drop targets.

## Switch objects

The object each switch address is bound to by the script's own code. Drop targets are the primary `sw1`-`sw4` and `sw17`-`sw19` walls of the script's `DTArray`, not their `a` walls or `psw` primitives.

| address | VPX type | object | raw x | raw y | x | y |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 1 | Wall | sw1 | 119.3661 | 624.8873 | 0.094961 | 0.316559 |
| 2 | Wall | sw2 | 155.662 | 683.0146 | 0.123836 | 0.346005 |
| 3 | Wall | sw3 | 194.2662 | 742.722 | 0.154548 | 0.376252 |
| 4 | Wall | sw4 | 232.0223 | 803.2904 | 0.184584 | 0.406935 |
| 8 | Kicker | Drain | 595.7037 | 1879.7786 | 0.473909 | 0.952269 |
| 17 | Wall | sw17 | 988.729 | 904.0074 | 0.786578 | 0.457957 |
| 18 | Wall | sw18 | 988.4227 | 843.8893 | 0.786335 | 0.427502 |
| 19 | Wall | sw19 | 988.4691 | 783.3369 | 0.786372 | 0.396827 |
| 22 | Trigger | sw22 | 1113.7444 | 1190.6776 | 0.886034 | 0.603180 |
| 23 | Trigger | sw23 | 1047.352 | 1190.6774 | 0.833216 | 0.603180 |
| 24 | Trigger | sw24 | 823.7758 | 378.0473 | 0.655351 | 0.191513 |
| 26 | Trigger | sw26 | 660.3616 | 150.35 | 0.525347 | 0.076165 |
| 27 | Primitive | sw27a#upper | 359.0569 | 318.2345 | 0.285646 | 0.161213 |
| 27 | Primitive | sw27a#lower | 214.18 | 930.7368 | 0.170390 | 0.471498 |
| 28 | Trigger | sw28 | 1095.4208 | 664.0117 | 0.871456 | 0.336379 |
| 29 | HitTarget | sw29 | 660.9883 | 842.7304 | 0.525846 | 0.426915 |
| 30 | HitTarget | sw30 | 661.9927 | 385.9749 | 0.526645 | 0.195529 |
| 31 | Trigger | SW31 | 203.6266 | 285.3979 | 0.161994 | 0.144578 |
| 32 | Trigger | sw32 | 494.47 | 375.4134 | 0.393373 | 0.190179 |
| 33 | Spinner | sw33 | 309.8113 | 607.252 | 0.246469 | 0.307625 |
| 34 | Trigger | sw34 | 497.3596 | 255.6826 | 0.395672 | 0.129525 |
| 34 | Trigger | sw34a | 1004.4398 | 342.5393 | 0.799077 | 0.173525 |
| 34 | Primitive | sw34b#rebound | 1002.9263 | 847.5023 | 0.797873 | 0.429332 |
| 35 | Wall | RightSlingShot | 914.3501 | 1250.9164 | 0.727407 | 0.633696 |
| 36 | Wall | LeftSlingShot | 384.7965 | 1366.7206 | 0.306123 | 0.692361 |
| 37 | Bumper | Bumper1 | 178.0519 | 1300.8716 | 0.141648 | 0.659003 |
| 38 | Bumper | Bumper2 | 659.7002 | 746.9893 | 0.524821 | 0.378414 |
| 39 | Bumper | Bumper3 | 772.7929 | 563.0331 | 0.614791 | 0.285224 |
| 40 | Bumper | Bumper4 | 550.4558 | 561.1686 | 0.437912 | 0.284280 |

Switch 8's object is the `Drain` kicker, the hole the ball drains into (`bsTrough.Initsw 0,8`); the table's `BallRelease` kicker, which throws the ball into the shooter lane, sits at raw (1143.197, 1646.575).

## Flippers

| object | pivot raw x | raw y | x | y |
| --- | ---: | ---: | ---: | ---: |
| LeftFlipper | 419.6366 | 1643.0098 | 0.333840 | 0.832325 |
| LeftFlipper1 | 228.0451 | 1039.2418 | 0.181420 | 0.526465 |
| RightFlipper | 746.7223 | 1642.9004 | 0.594051 | 0.832270 |
| RightFlipper1 | 844.1688 | 1509.167 | 0.671574 | 0.764522 |

## Lamp lights and the art under them

Each lamp is the table's `Light` named `L<address>`, bound by `set Lights(<address>)=L<address>`. The art column is what the table's embedded playfield scan (`images/Paragon_PF.webp`, 3584 x 7168, mapped onto the full table area) shows under or beside each light, read from crops centred on the light.

| lamp | object | raw x | raw y | x | y | art at the light |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | L1 | 571.5958 | 1390.4562 | 0.454730 | 0.704385 | 1 Thousand (bonus ladder) |
| 2 | L2 | 571.2874 | 1300.679 | 0.454485 | 0.658905 | 5 Thousand |
| 3 | L3 | 604.8001 | 1260.0181 | 0.481146 | 0.638307 | 9 Thousand |
| 4 | L4 | 635.9268 | 1158.278 | 0.505908 | 0.586767 | 40 Thousand |
| 5 | L5 | 870.0774 | 880.4737 | 0.692186 | 0.446035 | beside 25,000 |
| 6 | L6 | 389.9911 | 1146.9938 | 0.310255 | 0.581051 | 2x |
| 7 | L7 | 701.9483 | 233.9928 | 0.558431 | 0.118537 | P (saucer arc, 1st) |
| 8 | L8 | 869.7252 | 195.2525 | 0.691905 | 0.098912 | G (saucer arc) |
| 9 | L9 | 359.3381 | 1033.1544 | 0.285870 | 0.523381 | P (centre PARAGON, 1st) |
| 10 | L10 | 660.8875 | 990.1623 | 0.525766 | 0.501602 | G (centre) |
| 11 | L11 | 662.0467 | 148.3918 | 0.526688 | 0.075173 | star rollover button, lit from the GI collection - not lamp 11 |
| 12 | L12 | 394.6702 | 203.5488 | 0.313978 | 0.103115 | 2 Thousand (golden cliffs row) |
| 14 | L14 | 404.0406 | 809.1027 | 0.321432 | 0.409880 | bottom of four plain yellow inserts beside the spinner (a fifth insert below them carries the GI light GIxx) |
| 15 | L15 | 1096.7869 | 801.5226 | 0.872543 | 0.406040 | above 10000 |
| 16 | L16 | 1006.1752 | 340.5943 | 0.800458 | 0.172540 | star rollover button, lit from the GI collection - not lamp 16 |
| 17 | L17 | 541.0408 | 1343.666 | 0.430422 | 0.680682 | 2 Thousand |
| 18 | L18 | 633.0775 | 1306.0181 | 0.503642 | 0.661610 | 6 Thousand |
| 19 | L19 | 665.1392 | 1264.7574 | 0.529148 | 0.640708 | 10 Thousand |
| 20 | L20 | 868.9106 | 747.1826 | 0.691257 | 0.378512 | beside 10,000 (drop-target value column) |
| 21 | L21 | 1123.7238 | 863.6227 | 0.893973 | 0.437499 | red insert above Special |
| 22 | L22 | 462.8445 | 1126.2775 | 0.368214 | 0.570556 | 3x |
| 23 | L23 | 739.4782 | 210.3623 | 0.588288 | 0.106567 | A (saucer arc, 2nd) |
| 24 | L24 | 911.1331 | 210.6843 | 0.724847 | 0.106730 | O (saucer arc) |
| 25 | L25 | 432.8875 | 1006.1128 | 0.344381 | 0.509682 | A (centre, 2nd) |
| 26 | L26 | 735.1843 | 1006.903 | 0.584872 | 0.510083 | O (centre) |
| 27 | L27 | 1097.8867 | 660.7286 | 0.873418 | 0.334716 | star rollover button, lit from the GI collection - not lamp 27 |
| 28 | L28 | 463.2982 | 203.2296 | 0.368575 | 0.102953 | 4 Thousand |
| 29 | L29 | 499.4042 | 254.0524 | 0.397298 | 0.128699 | star rollover button, lit from the GI collection - not lamp 29 |
| 30 | L30 | 377.5338 | 758.9175 | 0.300345 | 0.384457 | second from bottom |
| 31 | L31 | 1122.3175 | 739.1519 | 0.892854 | 0.374444 | above 5000 (waterfall lane) |
| 33 | L33 | 605.3859 | 1347.221 | 0.481612 | 0.682483 | 3 Thousand |
| 34 | L34 | 486.7385 | 1248.5054 | 0.387222 | 0.632475 | 7 Thousand |
| 35 | L35 | 534.872 | 1157.7847 | 0.425515 | 0.586517 | 20 Thousand (super bonus row) |
| 36 | L36 | 868.3308 | 791.8931 | 0.690796 | 0.401162 | beside 15,000 |
| 37 | L37 | 823.9986 | 276.1407 | 0.655528 | 0.139889 | red insert under "Saucer Scores SPECIAL" |
| 38 | L38 | 704.4242 | 1125.5375 | 0.560401 | 0.570181 | 5x |
| 39 | L39 | 781.1083 | 195.7702 | 0.621407 | 0.099174 | R (saucer arc) |
| 40 | L40 | 948.3928 | 233.6229 | 0.754489 | 0.118350 | N (saucer arc) |
| 41 | L41 | 508.8875 | 990.903 | 0.404843 | 0.501977 | R (centre) |
| 42 | L42 | 807.5546 | 1033.6945 | 0.642446 | 0.523655 | N (centre) |
| 43 | L43 | 779.4708 | 1154.1255 | 0.620104 | 0.584663 | SHOOT AGAIN |
| 44 | L44 | 531.7694 | 202.8451 | 0.423046 | 0.102758 | 6 Thousand |
| 46 | L46 | 350.2628 | 709.8182 | 0.278650 | 0.359584 | third from bottom |
| 47 | L47 | 429.6332 | 262.2157 | 0.341793 | 0.132835 | 10 Thousand |
| 49 | L49 | 513.4357 | 1297.6406 | 0.408461 | 0.657366 | 4 Thousand |
| 50 | L50 | 546.2874 | 1255.7828 | 0.434596 | 0.636161 | 8 Thousand |
| 51 | L51 | 583.8586 | 1157.7258 | 0.464486 | 0.586487 | 30 Thousand |
| 52 | L52 | 869.3309 | 835.5965 | 0.691592 | 0.423301 | beside 20,000 |
| 53 | L53 | 94.8309 | 525.6588 | 0.075442 | 0.266291 | white insert above 5X (treasure lane) |
| 54 | L54 | 99.2388 | 474.2156 | 0.078949 | 0.240231 | red insert, lower of two; the Treasure Chamber plastic beside it prints "EXTRA BALL When LIT" |
| 55 | L55 | 824.5405 | 190.6599 | 0.655959 | 0.096586 | A (saucer arc, 4th) |
| 56 | L56 | 118.7699 | 428.5474 | 0.094487 | 0.217096 | red insert, upper of two; the plastic prints "SPECIAL When LIT" above the extra-ball caption |
| 57 | L57 | 585.8006 | 984.1128 | 0.466031 | 0.498537 | A (centre, 4th) |
| 58 | L58 | 870.5774 | 924.684 | 0.692583 | 0.468432 | red insert beside SPECIAL |
| 59 | L59 | 312.9085 | 1759.6914 | 0.248933 | 0.891434 | credit window in the apron |
| 60 | L60 | 600.3391 | 203.2208 | 0.477597 | 0.102949 | 8 Thousand |
| 62 | L62 | 322.6837 | 659.5472 | 0.256709 | 0.334117 | top of the four |
| 63 | L63 | 567.7694 | 262.2157 | 0.451686 | 0.132835 | 20 Thousand |

`GIxx` (raw 430.677, 859.0657) is a GI light in the fifth insert of the spinner column, below lamp 14's insert. Lights `L11`, `L16`, `L27` and `L29` sit in the four star rollover buttons (26 top centre, 34a top right, 28 waterfall lane and 34 golden cliffs) and belong to the table's GI collection.
