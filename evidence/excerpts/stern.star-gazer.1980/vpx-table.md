# Star Gazer — retained table geometry

The retained table is `Star Gazer (Stern 1980) v2.0.0.vpx` (UnclePaulie, VPW standards, 242,835,456 bytes, SHA-256 `b15a49d6902164ae27b946b2f67d1c5682f92bd382288f2c94e2641045128085`), extracted with `vpxtool git:v0.33.3`. Its playfield bounds are `left=0 top=0 right=952.941 bottom=1976.471`, so a normalized coordinate is `x / 952.941` and `y / 1976.471`, rounded to six places by the repository's `extract_spatial_candidates`. The retained extraction's canonical manifest digest is `0d5764e06bd013668c6d43ed552125533be59396e2915b812755de4c2bcb43ec`. The objects below are frozen in `tools/seeds/stern/star-gazer-1980-spatial.json` so the curator reproduces without the table.

An older table, `Star Gazer (Stern 1980).vpx` (2020, 25,677,824 bytes, SHA-256 `7cedbb4ec6dee890c0d077aaef68cf0eccc68efdd1ac2c94d648b792759f22ee`), binds the same lamp numbers to lights within about ten playfield units of this table's and binds no lamp number the newer table lacks; the two layouts are too alike to count as independent, so it only supplements this table.

## Switch objects

The object each switch address is bound to, by the script's own code. Drop-target walls are the primary `sw22` to `sw30` walls, not their `a`, `p` helpers; the stand-up targets are the `HitTarget` objects, not their `o`, `p` and `pback` render helpers.

| address | VPX type | object | x | y |
| ---: | --- | --- | ---: | ---: |
| 4 | Spinner | sw4 | 0.073271 | 0.346841 |
| 5 | Spinner | sw5 | 0.792748 | 0.405479 |
| 9 | Spinner | sw9 | 0.146762 | 0.211737 |
| 10 | HitTarget | sw10 | 0.076369 | 0.071104 |
| 11 | HitTarget | sw11 | 0.145910 | 0.037407 |
| 12 | Bumper | Bumper1 | 0.241074 | 0.116927 |
| 13 | Bumper | Bumper2 | 0.653977 | 0.171390 |
| 14 | Bumper | Bumper3 | 0.450589 | 0.280353 |
| 15 | Wall | RightSlingshot | 0.741528 | 0.687607 |
| 16 | Wall | LeftSlingshot | 0.161104 | 0.688036 |
| 17 | HitTarget | sw17 | 0.241873 | 0.025410 |
| 18 | HitTarget | sw18 | 0.336521 | 0.039327 |
| 19 | HitTarget | sw19 | 0.675912 | 0.073387 |
| 20 | HitTarget | sw20 | 0.768688 | 0.097063 |
| 21 | HitTarget | sw21 | 0.828995 | 0.134779 |
| 22 | Wall | sw22 | 0.076295 | 0.524159 |
| 23 | Wall | sw23 | 0.076414 | 0.495456 |
| 24 | Wall | sw24 | 0.076203 | 0.466792 |
| 25 | Wall | sw25 | 0.261259 | 0.206386 |
| 26 | Wall | sw26 | 0.312962 | 0.192650 |
| 27 | Wall | sw27 | 0.364585 | 0.179028 |
| 28 | Wall | sw28 | 0.696922 | 0.309744 |
| 29 | Wall | sw29 | 0.696768 | 0.338482 |
| 30 | Wall | sw30 | 0.696950 | 0.367106 |
| 31 | HitTarget | sw31 | 0.842231 | 0.182619 |
| 32 | HitTarget | sw32 | 0.803864 | 0.226183 |
| 33 | Kicker | Drain | 0.530816 | 0.944595 |
| 34 | Trigger | sw34 | 0.858138 | 0.701021 |
| 35 | Trigger | sw35 | 0.053443 | 0.701217 |
| 36 | Trigger | sw36 | 0.679101 | 0.768511 |
| 37 | Trigger | sw37 | 0.222838 | 0.768637 |
| 38 | HitTarget | sw38 | 0.734082 | 0.261506 |
| 39 | HitTarget | sw39 | 0.827961 | 0.474541 |
| 40 | HitTarget | sw40 | 0.826894 | 0.529168 |

Switch 33 is bound by the script to the `BallRelease` kicker beside the shooter lane; the `Drain` kicker listed above is the outhole hole at the bottom centre where the factory drawing numbers 33, and is the object this definition places the outhole switch on. Flipper pivots: `LeftFlipper` 0.274151, 0.833556 and `RightFlipper` 0.623858, 0.833556.

## Lamp objects

The table's embedded playfield texture (`Playfield.webp`, 3584 x 7433 px, a scan of an unrestored playfield with the insert holes printed black) was sampled under every light listed below: all 57 lie in dark insert holes (mean brightness under 60 of 255 over a 40 x 40 px patch centred on the light). That shows each light sits on an insert; it cannot tell inserts of the same size apart. The art identifies the socket of 22 lamp numbers by itself: the twelve signs (constellation drawings), the eight spinner-and-bank values (printed 500 to 4000, in the ROM's sweep order) and the two captioned lites (public 14, extra ball, and public 30, special). Every other placed lamp (the bonus ring, the four zodiac target values, the 1X to 4X column, the lane arrows, the outlane and spinner lites, and shoot again) carries no printed value or caption, so its socket rests on the table's light-to-lamp-number binding alone and its placement stays `observed`.


Each light's public number is its `TimerInterval`; render-halo duplicates named `l<n>a` are omitted. Four lamp numbers drive a second bulb at the opposite lane, `l90`, `l250`, `l410` and `l570`, with the same `TimerInterval`.

| public lamp | light | x | y |
| ---: | --- | ---: | ---: |
| 1 | l1 | 0.139845 | 0.069766 |
| 2 | l2 | 0.620901 | 0.088505 |
| 3 | l3 | 0.789829 | 0.198677 |
| 4 | l4 | 0.452077 | 0.451491 |
| 5 | l5 | 0.590599 | 0.568514 |
| 6 | l6 | 0.312798 | 0.568162 |
| 7 | l7 | 0.308522 | 0.410800 |
| 8 | l8 | 0.279693 | 0.337186 |
| 9 | l9 | 0.319527 | 0.801142 |
| 9 | l90 | 0.584055 | 0.799734 |
| 10 | l10 | 0.548531 | 0.150757 |
| 11 | l11 | 0.453949 | 0.801130 |
| 12 | l12 | 0.452045 | 0.668342 |
| 14 | l14 | 0.159971 | 0.498080 |
| 17 | l17 | 0.206560 | 0.051906 |
| 18 | l18 | 0.707926 | 0.107534 |
| 19 | l19 | 0.744721 | 0.227895 |
| 20 | l20 | 0.531735 | 0.462333 |
| 21 | l21 | 0.531421 | 0.596324 |
| 22 | l22 | 0.288704 | 0.528765 |
| 23 | l23 | 0.337557 | 0.387179 |
| 24 | l24 | 0.309221 | 0.316854 |
| 25 | l25 | 0.339831 | 0.779576 |
| 25 | l250 | 0.564289 | 0.779011 |
| 26 | l26 | 0.548342 | 0.175147 |
| 27 | l27 | 0.451867 | 0.556325 |
| 28 | l28 | 0.451940 | 0.698445 |
| 29 | l29 | 0.778941 | 0.445560 |
| 30 | l30 | 0.620138 | 0.340045 |
| 33 | l33 | 0.280489 | 0.051655 |
| 34 | l34 | 0.769037 | 0.128678 |
| 35 | l35 | 0.781408 | 0.502314 |
| 36 | l36 | 0.591226 | 0.491006 |
| 37 | l37 | 0.452033 | 0.606768 |
| 38 | l38 | 0.312388 | 0.490196 |
| 39 | l39 | 0.293353 | 0.372609 |
| 40 | l40 | 0.264776 | 0.302463 |
| 41 | l41 | 0.337136 | 0.755340 |
| 41 | l410 | 0.567929 | 0.755422 |
| 42 | l42 | 0.547905 | 0.199268 |
| 43 | l43 | 0.452257 | 0.502202 |
| 44 | l44 | 0.452206 | 0.728625 |
| 46 | l46 | 0.855750 | 0.645155 |
| 49 | l49 | 0.345937 | 0.070006 |
| 50 | l50 | 0.799532 | 0.162402 |
| 51 | l51 | 0.782166 | 0.555912 |
| 52 | l52 | 0.612917 | 0.529574 |
| 53 | l53 | 0.371306 | 0.596187 |
| 54 | l54 | 0.371429 | 0.462124 |
| 55 | l55 | 0.323240 | 0.351803 |
| 56 | l56 | 0.294611 | 0.281495 |
| 57 | l57 | 0.313398 | 0.734113 |
| 57 | l570 | 0.588787 | 0.733705 |
| 58 | l58 | 0.548099 | 0.223050 |
| 59 | l59 | 0.108949 | 0.381018 |
| 60 | l60 | 0.452149 | 0.757833 |
| 62 | l62 | 0.052806 | 0.645213 |
