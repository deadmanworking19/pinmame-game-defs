# Stern NBA (2009) — the ROM's own service-test names (visual reading of retained DMD frames)

Status: **read from the harness's retained 128x32 DMD frames by eye; not independently reviewed.** Stern's public NBA document is a partial parts book (the Blue and Pink pages only), so these test screens are the only game-specific source that names every switch, coil and lamp address and prints its wire colours. Every row below is a curator's reading of the frame whose pixel SHA-256 the runtime summary records; a misreading cannot change those hashes. Ambiguous glyphs were re-read on 6x enlargements of the same frames.

## Envelope

| Field | Value |
| --- | --- |
| Driver | `nba_802` (NBA V8.02), ROM zip `nba_802.zip` (member `nba_802.bin`, CRC ba681dac, matching pinned `sam.c`) |
| Emulator | `pinmame64.dll` built from PinMAME revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`, SHA-256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5` |
| Runs | fresh isolated state directories; service menu entered with the named Back key and Select presses; scenarios `tools/harness-scenarios/stern/nba-2009-switch-test-sweep.json`, `nba-2009-coil-sweep.json`, `nba-2009-lamp-sweep.json` |
| Retained | raw runs and frames under the working root's `review-artifacts/nba-2009/harness/`, sealed by `tools/build_external_evidence_manifest.py`; summaries in `evidence/runtime/sam/nba-*.json` |

## Switch test, matrix switches 1–64

Each row is the frame captured while the public address was held at 1. The third display line reads `LAST SW. #n`; the fourth prints two wire colours separated by ` / `. The test's grid draws the matrix as 4 rows of 16: the first colour is shared by each run of 16 consecutive switches and the second by every switch at the same position in its run. With every switch at 0 the test prints `NONE`. Names are as printed, including the parentheses that mark one letter of a word.

| Public | Name the ROM prints | Wire colours printed |
| ---: | --- | --- |
| 1 | L. 4-BANK (TOP) | GRN-BLU / BRN-BLK |
| 2 | LEFT 4-BANK #2 | GRN-BLU / BRN |
| 3 | LEFT 4-BANK #3 | GRN-BLU / BRN-RED |
| 4 | L. 4-BANK (BOT) | GRN-BLU / BRN-ORG |
| 5 | R. 3-BANK (TOP) | GRN-BLU / BRN-YEL |
| 6 | R. 3-BANK (MID) | GRN-BLU / BRN-GRN |
| 7 | R. 3-BANK (BOT) | GRN-BLU / BRN-BLU |
| 8 | R. RAMP ENTRANCE | GRN-BLU / BRN-VIO |
| 9 | RIGHT EJECT | GRN-BLU / BRN-GRY |
| 10 | CAPTIVE BALL | GRN-BLU / BLU-BLK |
| 11 | MV(P) DROP TARGET | GRN-BLU / BLU-BRN |
| 12 | M(V)P DROP TARGET | GRN-BLU / BLU-RED |
| 13 | (M)VP DROP TARGET | GRN-BLU / BLU-ORG |
| 14 | LEFT ORBIT | GRN-BLU / BLU-YEL |
| 15 | TOURNAMENT START | GRN-BLU / BLU-GRN |
| 16 | START BUTTON | GRN-BLU / BLU-WHT |
| 17 | SWITCH #17 | GRN-VIO / BRN-BLK |
| 18 | TROUGH #4 (L) | GRN-VIO / BRN |
| 19 | TROUGH #3 | GRN-VIO / BRN-RED |
| 20 | TROUGH #2 | GRN-VIO / BRN-ORG |
| 21 | TROUGH #1 (R) | GRN-VIO / BRN-YEL |
| 22 | TROUGH JAM | GRN-VIO / BRN-GRN |
| 23 | SHOOTER LANE | GRN-VIO / BRN-BLU |
| 24 | LEFT OUTLANE | GRN-VIO / BRN-VIO |
| 25 | LEFT RETURN LANE | GRN-VIO / BRN-GRY |
| 26 | LEFT SLINGSHOT | GRN-VIO / BLU-BLK |
| 27 | RIGHT SLINGSHOT | GRN-VIO / BLU-BRN |
| 28 | RIGHT RETURN LANE | GRN-VIO / BLU-RED |
| 29 | RIGHT OUTLANE | GRN-VIO / BLU-ORG |
| 30 | TOP POP BUMPER | GRN-VIO / BLU-YEL |
| 31 | LEFT POP BUMPER | GRN-VIO / BLU-GRN |
| 32 | RIGHT POP BUMPER | GRN-VIO / BLU-WHT |
| 33 | LEFT RAMP ENTER | GRN-GRY / BRN-BLK |
| 34 | BASKET OPTO | GRN-GRY / BRN |
| 35 | LEFT EJECT | GRN-GRY / BRN-RED |
| 36 | RIGHT ORBIT | GRN-GRY / BRN-ORG |
| 37 | R. RAMP EXIT | GRN-GRY / BRN-YEL |
| 38 | SWITCH #38 | GRN-GRY / BRN-GRN |
| 39 | SWITCH #39 | GRN-GRY / BRN-BLU |
| 40 | SWITCH #40 | GRN-GRY / BRN-VIO |
| 41 | SWITCH #41 | GRN-GRY / BRN-GRY |
| 42 | SWITCH #42 | GRN-GRY / BLU-BLK |
| 43 | SWITCH #43 | GRN-GRY / BLU-BRN |
| 44 | SWITCH #44 | GRN-GRY / BLU-RED |
| 45 | SWITCH #45 | GRN-GRY / BLU-ORG |
| 46 | SWITCH #46 | GRN-GRY / BLU-YEL |
| 47 | POP BUMPER TARGET | GRN-GRY / BLU-GRN |
| 48 | SWITCH #48 | GRN-GRY / BLU-WHT |
| 49 | SWITCH #49 | GRN-WHT / BRN-BLK |
| 50 | SWITCH #50 | GRN-WHT / BRN |
| 51 | SWITCH #51 | GRN-WHT / BRN-RED |
| 52 | SWITCH #52 | GRN-WHT / BRN-ORG |
| 53 | SWITCH #53 | GRN-WHT / BRN-YEL |
| 54 | SWITCH #54 | GRN-WHT / BRN-GRN |
| 55 | SWITCH #55 | GRN-WHT / BRN-BLU |
| 56 | SWITCH #56 | GRN-WHT / BRN-VIO |
| 57 | SWITCH #57 | GRN-WHT / BRN-GRY |
| 58 | SWITCH #58 | GRN-WHT / BLU-BLK |
| 59 | SWITCH #59 | GRN-WHT / BLU-BRN |
| 60 | SWITCH #60 | GRN-WHT / BLU-RED |
| 61 | SWITCH #61 | GRN-WHT / BLU-ORG |
| 62 | SWITCH #62 | GRN-WHT / BLU-YEL |
| 63 | SWITCH #63 | GRN-WHT / BLU-GRN |
| 64 | SWITCH #64 | GRN-WHT / BLU-WHT |

Printed exactly as shown: the second colour of switches 2, 18, 34 and 50 (the second switch of each run) is a bare `BRN`, while the first position prints `BRN-BLK` and the third `BRN-RED`.

## Switch test, dedicated switches

| Public held | Display while held | Wire colours printed |
| ---: | --- | --- |
| 65 | LEFT COIN SLOT / LAST SW. D-1 | PNK-BRN / BLK |
| 66 | CENTER COIN SLOT / LAST SW. D-2 | PNK-RED / BLK |
| 67 | RIGHT COIN SLOT / LAST SW. D-3 | PNK-ORG / BLK |
| 68 | FOURTH COIN SLOT / LAST SW. D-4 | PNK-YEL / BLK |
| 69 | FIFTH COIN SLOT / LAST SW. D-5 | PNK-GRN / BLK |
| 70 | DEDICATED SW. #6 / LAST SW. D-6 | PNK-BLU / BLK |
| 71 | DEDICATED SW. #7 / LAST SW. D-7 | PNK-VIO / BLK |
| 72 | DEDICATED SW. #8 / LAST SW. D-8 | PNK-GRY / BLK |
| 81 | RIGHT FLIPPER E.O.S. / LAST SW. D-12 | GRY / BLK |
| 82 | RIGHT FLIPPER E.O.S. / LAST SW. D-12 | GRY / BLK |
| 83 | LEFT FLIPPER E.O.S. / LAST SW. D-10 | GRY-BLU / BLK |
| 84 | LEFT FLIPPER E.O.S. / LAST SW. D-10 | GRY-BLU / BLK |
| 85 | DEDICATED SW. #16 / LAST SW. D-16 | GRY-BLK / BLK |
| 86 | DEDICATED SW. #16 / LAST SW. D-16 | GRY-BLK / BLK |
| 87 | DEDICATED SW. #14 / LAST SW. D-14 | GRY-BLU / BLK |
| 88 | DEDICATED SW. #14 / LAST SW. D-14 | GRY-BLU / BLK |
| -7 | TILT PENDULUM / LAST SW. D-17 | LGN-BRN / BLK |
| -6 | SLAM TILT / LAST SW. D-18 | LGN-YEL / BLK |
| -5 | TICKET NOTCH / LAST SW. D-19 | LGN-ORG / BLK |
| -4 | DEDICATED SW. #20 / LAST SW. D-20 | LGN-YEL / BLK |

Holding 82, 84, 86 or 88 (the flipper button bits D-11, D-9, D-15, D-13) shows the EOS of its pair, and the grid marks both bits of the pair: pinned PinMAME's `samswitch_r` copies each flipper button bit into its EOS bit as the CPU reads the dedicated word, so the buttons themselves print no name. Holding 81, 83, 85 or 87 marks one bit. `D-18` (public -6) prints `LGN-YEL`, the same colour as `D-20` (public -4); both frames were re-read on 6x enlargements.

## Single Coil Test

The test steps the 32 selector positions #1–#32 in order and wraps to #1 (position 33). SELECT fires the displayed coil. The last column lists the public solenoid addresses that changed while it was fired.

| `#` | Name the ROM prints | Wire colours printed | Public solenoids that changed |
| ---: | --- | --- | --- |
| 1 | TROUGH UP-KICKER | YEL-VIO / BRN-BLK | 1 |
| 2 | AUTO LAUNCH | YEL-VIO / BRN-RED | 2 |
| 3 | BASKET MAGNET | YEL-VIO / BRN-ORG | 3 |
| 4 | LEFT EJECT | YEL-VIO / BRN-YEL | 4 |
| 5 | RAMP DIVERTER | YEL-VIO / BRN-GRN | 5 |
| 6 | SPINNING DISK MOTOR | BRN / BRN-BLU | 6, 22 |
| 7 | 3-BANK DROP TARGET | YEL-VIO / BRN-VIO | 7 |
| 8 | SHAKER MOTOR (OPTIONAL) | RED-WHT / BRN-GRY | 8 |
| 9 | TOP POP BUMPER | YEL-VIO / BLU-BRN | 9 |
| 10 | LEFT POP BUMPER | YEL-VIO / BLU-RED | 10 |
| 11 | RIGHT POP BUMPER | YEL-VIO / BLU-ORG | 11 |
| 12 | BASKET DIVERTER | YEL-VIO / BLU-YEL | 12 |
| 13 | FLASH: BACKBOARD (X2) | ORG / BLU-GRN | 13 |
| 14 | FLASH: LEFT RAMP (X2) | ORG / BLU-BLK | 14 |
| 15 | LEFT FLIPPER | GRY-YEL / ORG-GRY | 15 |
| 16 | RIGHT FLIPPER | BLU-YEL / ORG-VIO | 16 |
| 17 | LEFT SLINGSHOT | BRN / VIO-BRN | 17 |
| 18 | RIGHT SLINGSHOT | BRN / VIO-RED | 18 |
| 19 | FLASH: BASKETBALL (X3) | ORG / VIO-ORG | 19 |
| 20 | RIGHT EJECT | BRN / VIO-WHT | 20 |
| 21 | ORBIT UP/DOWN POST | BRN / VIO-GRN | 21 |
| 22 | SPINNING DISK MOTOR RELAY | BRN / VIO-BLU | 22 |
| 23 | FLASH: LEFT SIDE | ORG / VIO-BLK | 23 |
| 24 | OPTIONAL COIL | RED / VIO-GRY | none |
| 25 | FLASH: LEFT RAMP ARROW | ORG / BLK-BRN | 25 |
| 26 | FLASH: LEFT EJECT ARROW | ORG / BLK-RED | 26 |
| 27 | FLASH: RIGHT EJECT ARROW | ORG / BLK-ORG | 27 |
| 28 | FLASH: RIGHT RAMP ARROW | ORG / BLK-YEL | 28 |
| 29 | FLASH: RIGHT SIDE | ORG / BLK-GRN | 29 |
| 30 | FLASH: CAPTIVE BALL | ORG / BLK-BLU | 30 |
| 31 | FLASH: POP BUMPER (X3) | ORG / BLK-VIO | 31 |
| 32 | FLASH: SLINGSHOT (X2) | ORG / BLK-GRY | 32 |

Firing `#6 SPINNING DISK MOTOR` also changes public 22, the coil the test lists separately as `#22 SPINNING DISK MOTOR RELAY`; firing #22 changes only 22. Firing `#24 OPTIONAL COIL` changes no public solenoid.

## Single Lamp Test

Selector position *n* lights public lamp *n* (it blinks; position 81 wraps to `START BUTTON / LAMP #1`). Each frame prints the lamp name, `LAMP #n` and two wire colours.

| Lamp | Name the ROM prints | Wire colours printed |
| ---: | --- | --- |
| 1 | START BUTTON | VIO-BLK / BLK-BRN |
| 2 | TOURNAMENT START BUTTON | VIO-BRN / BLK-BRN |
| 3 | SHOOT AGAIN | VIO-RED / BLK-BRN |
| 4 | LEFT OUTLANE | VIO-ORG / BLK-BRN |
| 5 | LEFT RETURN LANE | VIO-YEL / BLK-BRN |
| 6 | RIGHT RETURN LANE | VIO-GRN / BLK-BRN |
| 7 | RIGHT OUTLANE | VIO-BLU / BLK-BRN |
| 8 | NOT USED | GRY-BLK / BLK-BRN |
| 9 | FIRE | VIO-BLK / BLK-RED |
| 10 | FAST BREAK | VIO-BRN / BLK-RED |
| 11 | NOT USED | VIO-RED / BLK-RED |
| 12 | REBOUND | VIO-ORG / BLK-RED |
| 13 | ALL STAR | VIO-YEL / BLK-RED |
| 14 | ALL (S)TAR | VIO-GRN / BLK-RED |
| 15 | ALL S(T)AR | VIO-BLU / BLK-RED |
| 16 | ALL ST(A)R | GRY-BLK / BLK-RED |
| 17 | ALL STA(R) | VIO-BLK / BLK-ORG |
| 18 | (A)LL STAR | VIO-BRN / BLK-ORG |
| 19 | A(L)L STAR | VIO-RED / BLK-ORG |
| 20 | AL(L) STAR | VIO-ORG / BLK-ORG |
| 21 | L. LOOP ARROW | VIO-YEL / BLK-ORG |
| 22 | CAPTIVE BALL ARROW | VIO-GRN / BLK-ORG |
| 23 | L. RAMP ARROW | VIO-BLU / BLK-ORG |
| 24 | L. RAMP BASKETBALL | GRY-BLK / BLK-ORG |
| 25 | L. EJECT BASKETBALL | VIO-BLK / BLK-YEL |
| 26 | L. EJECT ARROW | VIO-BRN / BLK-YEL |
| 27 | R. EJECT ARROW | VIO-RED / BLK-YEL |
| 28 | MULTIBALL | VIO-ORG / BLK-YEL |
| 29 | NOT USED | VIO-YEL / BLK-YEL |
| 30 | R. RAMP ARROW | VIO-GRN / BLK-YEL |
| 31 | R. RAMP BASKETBALL | VIO-BLU / BLK-YEL |
| 32 | R. LOOP ARROW | GRY-BLK / BLK-YEL |
| 33 | REBOUND | VIO-BLK / BLK-GRN |
| 34 | NOT USED | VIO-BRN / BLK-GRN |
| 35 | TRIPLE DOUBLE | VIO-RED / BLK-GRN |
| 36 | NBA FINALS | VIO-ORG / BLK-GRN |
| 37 | SUPER STAR | VIO-YEL / BLK-GRN |
| 38 | NOT USED | VIO-GRN / BLK-GRN |
| 39 | ALL STAR | VIO-BLU / BLK-GRN |
| 40 | NB(A) | GRY-BLK / BLK-GRN |
| 41 | 3 POINT SHOOTOUT | VIO-BLK / BLK-BLU |
| 42 | SLAM DUNK | VIO-BRN / BLK-BLU |
| 43 | SKILLS CHALLENGE | VIO-RED / BLK-BLU |
| 44 | H-O-R-S-E | VIO-ORG / BLK-BLU |
| 45 | MYSTERY | VIO-YEL / BLK-BLU |
| 46 | SHOOTING STARS | VIO-GRN / BLK-BLU |
| 47 | (N)BA | VIO-BLU / BLK-BLU |
| 48 | N(B)A | GRY-BLK / BLK-BLU |
| 49 | (F)IRE | VIO-BLK / BLK-VIO |
| 50 | F(I)RE | VIO-BRN / BLK-VIO |
| 51 | FI(R)E | VIO-RED / BLK-VIO |
| 52 | FIR(E) | VIO-ORG / BLK-VIO |
| 53 | NOT USED | VIO-YEL / BLK-VIO |
| 54 | SUPER STAR ARROW | VIO-GRN / BLK-VIO |
| 55 | NOT USED | VIO-BLU / BLK-VIO |
| 56 | NOT USED | GRY-BLK / BLK-VIO |
| 57 | (M)VP | VIO-BLK / BLK-GRY |
| 58 | M(V)P | VIO-BRN / BLK-GRY |
| 59 | MV(P) | VIO-RED / BLK-GRY |
| 60 | TOP POP BUMPER | VIO-ORG / BLK-GRY |
| 61 | LEFT POP BUMPER | VIO-YEL / BLK-GRY |
| 62 | RIGHT POP BUMPER | VIO-GRN / BLK-GRY |
| 63 | SPECIAL | VIO-BLU / BLK-GRY |
| 64 | EXTRA BALL | GRY-BLK / BLK-GRY |
| 65 | NOT USED | VIO-BLK / BLK-WHT |
| 66 | NOT USED | VIO-BRN / BLK-WHT |
| 67 | NOT USED | VIO-RED / BLK-WHT |
| 68 | NOT USED | VIO-ORG / BLK-WHT |
| 69 | NOT USED | VIO-YEL / BLK-WHT |
| 70 | NOT USED | VIO-GRN / BLK-WHT |
| 71 | NOT USED | VIO-BLU / BLK-WHT |
| 72 | NOT USED | GRY-BLK / BLK-WHT |
| 73 | NOT USED | VIO-BLK / RED |
| 74 | NOT USED | VIO-BRN / RED |
| 75 | NOT USED | VIO-RED / RED |
| 76 | NOT USED | VIO-ORG / RED |
| 77 | NOT USED | VIO-YEL / RED |
| 78 | NOT USED | VIO-GRN / RED |
| 79 | NOT USED | VIO-BLU / RED |
| 80 | NOT USED | GRY-BLK / RED |

The eighth lamp of every row prints `GRY-BLK` as its first colour where the other seven print `VIO-xxx`.

## Other firmware revisions

The same three sweeps were run, with the same scenarios, on `nba_801` (V8.01), `nba_700` (V7.0), `nba_600` (V6.0) and `nba_500` (V5.0). Their zips hold the members `nba_v8-01_a.bin` (CRC 0f8b146e), `nba_v7-0_a.bin` (CRC 15ece43b), `nba_v6-0a.bin` (CRC af2fbcf4) and `nba_v5-0_a.bin` (CRC 01b0c27a), each matching pinned `sam.c`. Every switch-test, coil-test and lamp-test frame has the same pixel SHA-256 as the `nba_802` frame at the same step, so every name and wire colour above applies unchanged to all five revisions. The only frames that differ are captured before a test is entered: the power-up and attract-mode frames, the frame after the Back key, and the service-menu splash, which shows the version. Each coil-test position fires the same public solenoids in all five runs.
