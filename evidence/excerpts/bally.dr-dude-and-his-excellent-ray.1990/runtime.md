# System 11C ROM service evidence

Pinned PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`; native SHA-256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`. The retained summary SHA-256 is `974b8fb5458fb39b860a916f3f0f543245e7ef369b6f8e9e8997e39174f11cf7`. Each ROM initialized in an independent empty state directory; later runs inherited only its own hashed initial NVRAM. Host writes and readbacks are stimulus. ROM display text and changed output callbacks are observations, with shared O/0 and S/5 glyphs. No activity establishes physical fitment, bulb count or location.

## `dd_l2` retained runs

Initialization NVRAM SHA-256: `66118bb8c2e7e951f44e83721233ab2638ff484d58d440f1b1d3412974dc62bc`.

| Run | Trace | Trace SHA-256 | Scenario | Scenario SHA-256 |
| --- | --- | --- | --- | --- |
| init | init-trace.json | 618ccec4566de9e6f86102b4fc5e019039c8f659be69dd5591519dce65f84f6b | init.json | aa44ba869e942bb0919c9e1f6e10f117e2228ddb30a37b2640846ca173da2f74 |
| coil | coil-trace.json | b876e8c85fd7e5f5fb97e6f1d7b466a5a84b94712da35cb3b0d206c9d8625f2c | coil-test.json | 1581e5105839c8228fdedce2a625c5a0059f9cbf63dd690a67901134a8afb927 |
| lamp | lamp-trace.json | 92b5ceeb1e97f0c6ecf5f14fcbca24070eff9ea96c38a1cc23a39446029c2c87 | single-lamps.json | 094ea02df388b75b3d79b8670a523f8a9748b788de4d41e0fca6ad59fe32ebfc |
| switch | switch-trace.json | 74ef1a70762adb816ba64dd54b5e077207c5c2d60c3aed0f6650b40f83b1eab7 | switch-levels.json | 61c229ddb134fa60131656787749acd66ae10572e2be8a8f1df76e13586bc858 |
| game | game-trace.json | 24fe2ca7ecfd25047a05a3e3160e59a6cf3e56732aad60598c4c8a4896a81a65 | game-on.json | 0ae0790561a94cefbf7ba4f4031593bc612cfc06cb0dbe99cb06a131203068d0 |

## `dd_p6` retained runs

Initialization NVRAM SHA-256: `d5e5dfedc6966b2e69ae8c2f3b5ab031500c9c2433d9c3e55626e64bfd996096`.

| Run | Trace | Trace SHA-256 | Scenario | Scenario SHA-256 |
| --- | --- | --- | --- | --- |
| init | p6-init-trace.json | 1fb7476ba7fa3696fadbdfb124bef1cb5241c7a00ef6a1be0b23302e501b102d | init.json | aa44ba869e942bb0919c9e1f6e10f117e2228ddb30a37b2640846ca173da2f74 |
| coil | p6-coil-trace.json | e162f4b78d0a241b4dcd5cb04ee17cc3e7788b205b9444a72949043fdb641b1d | coil-test.json | 1581e5105839c8228fdedce2a625c5a0059f9cbf63dd690a67901134a8afb927 |
| lamp | p6-lamp-trace.json | 2d51a159b0776d0e5da42e82fd846dfdbc0cd37381175bf0e74e3b16d0ef590f | single-lamps.json | 094ea02df388b75b3d79b8670a523f8a9748b788de4d41e0fca6ad59fe32ebfc |
| switch | p6-switch-trace.json | e90bfbf9b968fc0da82caade49c69ad64fa56ababa471d0966097af1bc3b1606 | switch-levels.json | 61c229ddb134fa60131656787749acd66ae10572e2be8a8f1df76e13586bc858 |

## Complete common coil-test names

Both ROM sets agree. Names are the stable display reading after each step; they are not instantaneous labels at an output callback.

| Step | Public solenoid | ROM name |
| --- | --- | --- |
| 1 | 1 | OUTHOLE |
| 2 | 25 | 2F.L. MIXER HEART |
| 3 | 2 | TROUGH |
| 4 | 26 | 2F.L. MIXER GAB |
| 5 | 3 | TOP LEFT POPPER |
| 6 | 27 | 2F.L. MIXER MAG. |
| 7 | 4 | MID. RIGHT POPPER |
| 8 | 28 | 1F.L. MAGNETIC |
| 9 | 5 | NOT USED |
| 10 | 29 | 1F.L. GAB |
| 11 | 6 | KNOCKER |
| 12 | 30 | 1F.L. HEART |
| 13 | 7 | R. DROP TARGET |
| 14 | 31 | 1F.L. DROP TARGETS |
| 15 | 8 | NOT USED |
| 16 | 32 | 1F.L. RAYGUN |
| 17 | 9 | NOT USED |
| 18 | 10 | PLAYFIELD G.I. |
| 19 | 11 | 1F.L. INSERT MID. |
| 20 | 12 | A/C SELECT |
| 21 | 13 | MAGNET |
| 22 | 14 | BIG SHOT |
| 23 | 15 | 1F.L. BIG SHOT |
| 24 | 16 | MOTOR |
| 25 | 17 | L. JUMPER BUMPER |
| 26 | 18 | LEFT SLINGSHOT |
| 27 | 19 | R. JUMPER BUMPER |
| 28 | 20 | RIGHT SLINGSHOT |
| 29 | 21 | B. JUMPER BUMPER |
| 30 | 22 | NOT USED |

A/C select 12 is energized for C-side 25-32. Pulses at manual-unfitted 5, 8, 9 and 22 are service sweeps. Output 10 is PLAYFIELD G.I.; no separate GI callbacks appeared. LA-2 gameplay raised virtual GAME ON 23 after Start, lowered it on Tilt and raised it for the next ball.

## Complete common single-lamp names

Each selector blinks its corresponding public lamp. The following readings agree across both ROM sets.

| Selector | Public lamp | ROM name |
| --- | --- | --- |
| 1 | 1 | JACKPOT 1 MIL. |
| 2 | 2 | JACKPOT 2 MIL. |
| 3 | 3 | JACKPOT 3 MIL. |
| 4 | 4 | JACKPOT 4 MIL. |
| 5 | 5 | JACKPOT S MIL. |
| 6 | 6 | JUMPER VALUE 1K |
| 7 | 7 | JUMPER VALUE 2.SK |
| 8 | 8 | JUMPER VALUE SK |
| 9 | 9 | I TEST 2SK |
| 10 | 10 | I TEST SOK |
| 11 | 11 | I TEST 7SK |
| 12 | 12 | I TEST 1OOK |
| 13 | 13 | RAY'S SPECIAL |
| 14 | 14 | RAY'S EX. BALL |
| 15 | 15 | RAY'S R.E.F.L.E.X. 1 |
| 16 | 16 | BAG OF TRICKS |
| 17 | 17 | RAYGUN'S LAMP 1 |
| 18 | 18 | RAYGUN'S LAMP 2 |
| 19 | 19 | RAYGUN'S LAMP 3 |
| 20 | 20 | RAYGUN'S LAMP 4 |
| 21 | 21 | RAYGUN'S LAMP S |
| 22 | 22 | 2X |
| 23 | 23 | 4X |
| 24 | 24 | 6X |
| 25 | 25 | REFLE(X) |
| 26 | 26 | REFL(E)X |
| 27 | 27 | REF(L)EX |
| 28 | 28 | RE(F)LEX |
| 29 | 29 | R(E)FLEX |
| 30 | 30 | (R)EFLEX |
| 31 | 31 | BIG SHOT |
| 32 | 32 | PLAYFIELD 2X |
| 33 | 33 | MIX MASTER HEART |
| 34 | 34 | MIX MASTER MAG. |
| 35 | 35 | MIX MASTER GAB |
| 36 | 36 | MAGNETIC AWARD |
| 37 | 37 | HEART AWARD |
| 38 | 38 | GAB AWARD |
| 39 | 39 | SHOOT AGAIN |
| 40 | 40 | L./RIGHT OUTLANE |
| 41 | 41 | R. D.T. HOT SCORE |
| 42 | 42 | R. D.T. LITE MIL. |
| 43 | 43 | R. D.T. 2X JACKPOT |
| 44 | 44 | R. D.T. LITE EX.B. |
| 45 | 45 | R. D.T. BON. BOOST |
| 46 | 46 | HEART SK |
| 47 | 47 | HEART 2SK |
| 48 | 48 | HEART SOK |
| 49 | 49 | MAGNETIC R.E.F.L.E.X.3 |
| 50 | 50 | MAGNETIC SK |
| 51 | 51 | MAGNETIC 2SK |
| 52 | 52 | MAGNETIC SOK |
| 53 | 53 | GAB R.E.F.L.E.X. 2 |
| 54 | 54 | GAB SK |
| 55 | 55 | GAB 2SK |
| 56 | 56 | GAB SOK |
| 57 | 57 | JACKPOT LIT |
| 58 | 58 | MILLION |
| 59 | 59 | GAZILLION |
| 60 | 60 | SUPER DUDE (TOP) |
| 61 | 61 | MAJOR DUDE |
| 62 | 62 | COOL DUDE |
| 63 | 63 | PARTY DUDE |
| 64 | 64 | PLAIN DUDE (BOT.) |

## Complete common switch-held display readings

Each row is ROM display text while the host repeatedly holds that address. Repeated holds can mask emulator overwrites; use the source-defined flipper inputs and relay ownership. Host state is not proof of a ROM read.

| Public switch | Upper display | Lower display |
| --- | --- | --- |
| 1 | PLUMB TILT | O6 O1 |
| 2 | A/C RELAY C-SIDE | O6 O2 |
| 3 | GAME START | O6 O3 |
| 4 | RIGHT COIN SW. | O6 O4 |
| 5 | CENTER COIN SW. | O6 OS |
| 6 | LEFT COIN SW. | O6 O6 |
| 7 | SLAM TILT | O6 O7 |
| 8 | HI. SCORE RESET | O6 O8 |
| 9 | SHOOTER LANE | O6 O9 |
| 10 | OUTHOLE | O6 1O |
| 11 | TROUGH 1 BALL | O6 11 |
| 12 | TROUGH 2 BALLS | O6 12 |
| 13 | TROUGH 3 BALLS | O6 13 |
| 14 | HEART TARGET | O6 14 |
| 15 | ENTER LEFT RAMP | O6 1S |
| 16 | SCORE LEFT RAMP | O6 16 |
| 17 | LEFT OUTLANE | O6 17 |
| 18 | RIGHT OUTLANE | O6 18 |
| 19 | RIGHT RETURN | O6 19 |
| 20 | LEFT RETURN | O6 2O |
| 21 | R. DROP1 (TOP) | O6 21 |
| 22 | R. DROP2 | O6 22 |
| 23 | R. DROP3 | O6 23 |
| 24 | R. DROP4 (BOTTOM) | O6 24 |
| 25 | REFLE(X) | O6 2S |
| 26 | REFL(E)X | O6 26 |
| 27 | REF(L)EX | O6 27 |
| 28 | RE(F)LEX | O6 28 |
| 29 | R(E)FLEX | O6 29 |
| 30 | (R)EFLEX | O6 3O |
| 31 | BIG SHOT | O6 31 |
| 32 | MID. RIGHT POPPER | O6 32 |
| 33 | MIXER GAB (T.) | O6 33 |
| 34 | MIXER GAB (M.) | O6 34 |
| 35 | MIXER GAB (B.) | O6 3S |
| 36 | MIXER HEART (L.) | O6 36 |
| 37 | MIXER HEART (M.) | O6 37 |
| 38 | MIXER HEART (R.) | O6 38 |
| 39 | TOP LEFT 1O PTS. | O6 39 |
| 40 | NOT USED | O6 4O |
| 41 | MIXER MAG. (T.) | O6 41 |
| 42 | MIXER MAG. (M.) | O6 42 |
| 43 | MIXER MAG. (B.) | O6 43 |
| 44 | NOT USED | O6 44 |
| 45 | NOT USED | O6 4S |
| 46 | MID. MID. 1O PTS. | O6 46 |
| 47 | MID. BOT. 1O PTS. | O6 47 |
| 48 | MID. TOP 1O PTS. | O6 48 |
| 49 | I TEST TARGET | O6 49 |
| 50 | MAGNET TARGET | O6 SO |
| 51 | TOP LEFT POPPER | O6 S1 |
| 52 | L. JUMPER BUMPER | O6 S2 |
| 53 | R. JUMPER BUMPER | O6 S3 |
| 54 | B. JUMPER BUMPER | O6 S4 |
| 55 | LEFT SLINGSHOT | O6 SS |
| 56 | RIGHT SLINGSHOT | O6 S6 |
| 57 | RIGHT FLIPPER | O6 S7 |
| 58 | LEFT FLIPPER | O6 S8 |
| 59 | RIGHT LOOP | O6 S9 |
| 60 | NOT USED | O6 6O |
| 61 | NOT USED | O6 61 |
| 62 | NOT USED | O6 62 |
| 63 | NOT USED | O6 63 |
| 64 | NOT USED | O6 64 |
| 81 | SWITCH LEVELS | O6 |
| 82 | RIGHT FLIPPER | O6 S7 |
| 83 | SWITCH LEVELS | O6 |
| 84 | LEFT FLIPPER | O6 S8 |
| 85 | SWITCH LEVELS | O6 |
| 86 | SWITCH LEVELS | O6 |
| 87 | SWITCH LEVELS | O6 |
| 88 | SWITCH LEVELS | O6 |
