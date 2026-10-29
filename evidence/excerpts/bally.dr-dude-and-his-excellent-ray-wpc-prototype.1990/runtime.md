# WPC prototype ROM service evidence

Pinned PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`; native SHA-256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`. The retained summary SHA-256 is `944e6af8cb02b99f066e55d7b4374e314a4e0527c4497930ffc3e32485dbce2e`. Each ROM initialized in an independent empty state directory; later runs inherited only its own hashed initial NVRAM. Host writes and readbacks are stimulus. ROM display text and changed output callbacks are observations, with shared O/0 and S/5 glyphs. No activity establishes physical fitment, bulb count or location.

## `dd_p06` retained runs

Initialization NVRAM SHA-256: `513f00b02d8f57d29a0d55b226d078ea1dab91e3cd5f98082f1c56ca9965db90`.

| Run | Trace | Trace SHA-256 | Scenario | Scenario SHA-256 |
| --- | --- | --- | --- | --- |
| init | dd_p06-init.json | 5d9bad8de8cc26c943b6c55508e0e317a8c8b171c86cccae34e901d2d4034c2e | init.json | 84c6172f62be22339131cba010ef2d4acbb3a214422364ef44426fcc9b22fc77 |
| coil | dd_p06-coil-test.json | 02e1c16c64e245ae208cddd3864ab878288fb7c1cde68c896defc8fbf875523c | coil-test.json | 83af9bfc449720d534f12c3f1c576bafba92a7b0ff6729fcb89f88ea16f36f2d |
| flasher | dd_p06-flasher-test.json | bba7a4d47fce8ba942ed4d0c126c81e75167dc2ade165bf7cfce54b88e085245 | flasher-test.json | 7964ad487102df302129de7c04321782c10d84224fe80e3d7ad37ac861cb00ad |
| lamp | dd_p06-lamp-test.json | 82e07dd4f02271f1bae5f22876d554dd6b2d6222f97f3f0fed65fcc501f1df68 | lamp-test.json | ca53c9fc39a6c22f25ef2410676f3f550a7d1798c5fbfeaea92f4427c5177cb3 |
| switch | dd_p06-switch-test.json | 9ec08240a9632663efc52ef9857f84230d967eefa3a7ede33d6c5289a45ec357 | switch-test.json | 70b3c7ae0405d091e903e0c398c0f1256ebed1811c7ff28aebcdd5dfa14bdc37 |

## `dd_p7` retained runs

Initialization NVRAM SHA-256: `f0a17333383d91a07e220a37103e730ca427fadb66b1a8267873a183510c0431`.

| Run | Trace | Trace SHA-256 | Scenario | Scenario SHA-256 |
| --- | --- | --- | --- | --- |
| init | dd_p7-init.json | 0466b5277c4dc9c4a158d125f8f6f952c90be95c79c1b61b0ec4c1387d8fc15a | init.json | 84c6172f62be22339131cba010ef2d4acbb3a214422364ef44426fcc9b22fc77 |
| coil | dd_p7-coil-test.json | 1fcff29e37451c3868bb65486556af2feb26195fcc795bdc4543a3df50114bbd | coil-test.json | 83af9bfc449720d534f12c3f1c576bafba92a7b0ff6729fcb89f88ea16f36f2d |
| flasher | dd_p7-flasher-test.json | 0865245ecb66b5bd6a081cce751860fe29643fdd962bbf73bbf7b22d6324ff3a | flasher-test.json | 7964ad487102df302129de7c04321782c10d84224fe80e3d7ad37ac861cb00ad |
| lamp | dd_p7-lamp-test.json | a0f6b255b167936fdb4f4509e7770aeb03fb4f5fda8fc426cab4a826bd238d36 | lamp-test.json | ca53c9fc39a6c22f25ef2410676f3f550a7d1798c5fbfeaea92f4427c5177cb3 |
| switch | dd_p7-switch-test.json | 7003059f473258674a9358be3dd311438558690c6cc552e73cf782d0ff04be7a | switch-test.json | 70b3c7ae0405d091e903e0c398c0f1256ebed1811c7ff28aebcdd5dfa14bdc37 |

## Complete common coil-test names

Both ROM sets agree. Names are the stable display reading after each step; they are not instantaneous labels at an output callback.

| Public solenoid | ROM name |
| --- | --- |
| 1 | TOP LEFT POPPER |
| 2 | MID. RIGHT POPPER |
| 3 | BIG SHOT |
| 4 | R. DROP TARGET |
| 5 | MAGNET |
| 6 | KNOCKER |
| 7 | LEFT SLINGSHOT |
| 8 | RIGHT SLINGSHOT |
| 9 | OUTHOLE |
| 10 | TROUGH |
| 11 | NOT USED |
| 12 | NOT USED |
| 13 | L. JUMPER BUMPER |
| 14 | R. JUMPER BUMPER |
| 15 | B. JUMPER BUMPER |
| 16 | NOT USED |
| 17 | 2F.L. MIXER HEART |
| 18 | 2F.L. MIXER GAB |
| 19 | 2F.L. MIXER MAG. |
| 20 | 1F.L. MAGNETIC |
| 21 | 1F.L. GAB |
| 22 | 1F.L. HEART |
| 23 | 1F.L. DROP TARGETS |
| 24 | 1F.L. RAYGUN |
| 25 | NOT USED |
| 26 | 1F.L. BIG SHOT |
| 27 | MOTOR |
| 28 | 1F.L. INSERT MID. |

Output 28 has a separate named step and also emits brief pulses alongside many other coil/GI steps. Those coincident pulses do not identify additional physical loads. Two individual GI-off sweeps visit public channels 0, 1, 2, 3 and 4, under the single generic label GEN. ILLUMINATION. The ROM supplies no per-string name or quantity. FLASHER TEST emits 17-24, 26 and 28; rapid display changes require aligned timing.

## Complete common single-lamp names

Each selector blinks its corresponding public lamp. The following readings agree across both ROM sets.

| Selector | Public lamp | ROM name |
| --- | --- | --- |
| 1 | 11 | JACKPOT 1 MIL. |
| 2 | 12 | JACKPOT 2 MIL. |
| 3 | 13 | JACKPOT 3 MIL. |
| 4 | 14 | JACKPOT 4 MIL. |
| 5 | 15 | JACKPOT S MIL. |
| 6 | 16 | JUMPER VALUE 1K |
| 7 | 17 | JUMPER VALUE 2.SK |
| 8 | 18 | JUMPER VALUE SK |
| 9 | 21 | I TEST 2SK |
| 10 | 22 | I TEST SOK |
| 11 | 23 | I TEST 7SK |
| 12 | 24 | I TEST 1OOK |
| 13 | 25 | RAY'S SPECIAL |
| 14 | 26 | RAY'S EX. BALL |
| 15 | 27 | RAY'S R.E.F.L.E.X. 1 |
| 16 | 28 | BAG OF TRICKS |
| 17 | 31 | RAYGUN'S LAMP 1 |
| 18 | 32 | RAYGUN'S LAMP 2 |
| 19 | 33 | RAYGUN'S LAMP 3 |
| 20 | 34 | RAYGUN'S LAMP 4 |
| 21 | 35 | RAYGUN'S LAMP S |
| 22 | 36 | 2X |
| 23 | 37 | 4X |
| 24 | 38 | 6X |
| 25 | 41 | REFLE(X) |
| 26 | 42 | REFL(E)X |
| 27 | 43 | REF(L)EX |
| 28 | 44 | RE(F)LEX |
| 29 | 45 | R(E)FLEX |
| 30 | 46 | (R)EFLEX |
| 31 | 47 | BIG SHOT |
| 32 | 48 | PLAYFIELD 2X |
| 33 | 51 | MIX MASTER HEART |
| 34 | 52 | MIX MASTER MAG. |
| 35 | 53 | MIX MASTER GAB |
| 36 | 54 | MAGNETIC AWARD |
| 37 | 55 | HEART AWARD |
| 38 | 56 | GAB AWARD |
| 39 | 57 | SHOOT AGAIN |
| 40 | 58 | L./RIGHT OUTLANE |
| 41 | 61 | R. D.T. HOT SCORE |
| 42 | 62 | R. D.T. LITE MIL. |
| 43 | 63 | R. D.T. 2X JACKPOT |
| 44 | 64 | R. D.T. LITE EX.B. |
| 45 | 65 | R. D.T. BON. BOOST |
| 46 | 66 | HEART SK |
| 47 | 67 | HEART 2SK |
| 48 | 68 | HEART SOK |
| 49 | 71 | MAGNETIC R.E.F.L.E.X.3 |
| 50 | 72 | MAGNETIC SK |
| 51 | 73 | MAGNETIC 2SK |
| 52 | 74 | MAGNETIC SOK |
| 53 | 75 | GAB R.E.F.L.E.X. 2 |
| 54 | 76 | GAB SK |
| 55 | 77 | GAB 2SK |
| 56 | 78 | GAB SOK |
| 57 | 81 | JACKPOT LIT |
| 58 | 82 | MILLION |
| 59 | 83 | GAZILLION |
| 60 | 84 | SUPER DUDE (TOP) |
| 61 | 85 | MAJOR DUDE |
| 62 | 86 | COOL DUDE |
| 63 | 87 | PARTY DUDE |
| 64 | 88 | PLAIN DUDE (BOT.) |

## Complete common switch-held display readings

Each row is ROM display text while the host repeatedly holds that address. Repeated holds can mask emulator overwrites; use the source-defined flipper inputs and relay ownership. Host state is not proof of a ROM read.

| Public switch | Upper display | Lower display |
| --- | --- | --- |
| 11 | PLUMB TILT | O6 O1 |
| 12 | NOT USED | O6 O2 |
| 13 | GAME START | O6 O3 |
| 14 | RIGHT COIN SW. | O6 O4 |
| 15 | CENTER COIN SW. | O6 OS |
| 16 | LEFT COIN SW. | O6 O6 |
| 17 | SLAM TILT | O6 O7 |
| 18 | HI. SCORE RESET | O6 O8 |
| 21 | SHOOTER LANE | O6 O9 |
| 22 | OUTHOLE | O6 1O |
| 23 | TROUGH 1 BALL | O6 11 |
| 24 | TROUGH 2 BALLS | O6 12 |
| 25 | TROUGH 3 BALLS | O6 13 |
| 26 | HEART TARGET | O6 14 |
| 27 | ENTER LEFT RAMP | O6 1S |
| 28 | SCORE LEFT RAMP | O6 16 |
| 31 | LEFT OUTLANE | O6 17 |
| 32 | RIGHT OUTLANE | O6 18 |
| 33 | RIGHT RETURN | O6 19 |
| 34 | LEFT RETURN | O6 2O |
| 35 | R. DROP1 (TOP) | O6 21 |
| 36 | R. DROP2 | O6 22 |
| 37 | R. DROP3 | O6 23 |
| 38 | R. DROP4 (BOTTOM) | O6 24 |
| 41 | REFLE(X) | O6 2S |
| 42 | REFL(E)X | O6 26 |
| 43 | REF(L)EX | O6 27 |
| 44 | RE(F)LEX | O6 28 |
| 45 | R(E)FLEX | O6 29 |
| 46 | (R)EFLEX | O6 3O |
| 47 | BIG SHOT | O6 31 |
| 48 | MID. RIGHT POPPER | O6 32 |
| 51 | MIXER GAB (T.) | O6 33 |
| 52 | MIXER GAB (M.) | O6 34 |
| 53 | MIXER GAB (B.) | O6 3S |
| 54 | MIXER HEART (L.) | O6 36 |
| 55 | MIXER HEART (M.) | O6 37 |
| 56 | MIXER HEART (R.) | O6 38 |
| 57 | TOP LEFT 1O PTS. | O6 39 |
| 58 | NOT USED | O6 4O |
| 61 | MIXER MAG. (T.) | O6 41 |
| 62 | MIXER MAG. (M.) | O6 42 |
| 63 | MIXER MAG. (B.) | O6 43 |
| 64 | NOT USED | O6 44 |
| 65 | NOT USED | O6 4S |
| 66 | MID. MID. 1O PTS. | O6 46 |
| 67 | MID. BOT. 1O PTS. | O6 47 |
| 68 | MID. TOP 1O PTS. | O6 48 |
| 71 | I TEST TARGET | O6 49 |
| 72 | MAGNET TARGET | O6 SO |
| 73 | TOP LEFT POPPER | O6 S1 |
| 74 | L. JUMPER BUMPER | O6 S2 |
| 75 | R. JUMPER BUMPER | O6 S3 |
| 76 | B. JUMPER BUMPER | O6 S4 |
| 77 | LEFT SLINGSHOT | O6 SS |
| 78 | RIGHT SLINGSHOT | O6 S6 |
| 81 | RIGHT FLIPPER | O6 S7 |
| 82 | LEFT FLIPPER | O6 S8 |
| 83 | RIGHT LOOP | O6 S9 |
| 84 | NOT USED | O6 6O |
| 85 | NOT USED | O6 61 |
| 86 | NOT USED | O6 62 |
| 87 | NOT USED | O6 63 |
| 88 | NOT USED | O6 64 |
