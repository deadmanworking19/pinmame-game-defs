# Stern Family Guy (2007) — the ROM's own service-test names (visual reading of retained DMD frames)

Status: **read from the harness's retained 128x32 DMD frames by eye; not independently reviewed.** The DMD font defeats Windows OCR (a trial recognised fewer than a quarter of the switch names), so every name below is a curator's reading of the frame whose pixel SHA-256 the runtime summary records. A misreading cannot change those hashes.

## Envelope

| Field | Value |
| --- | --- |
| Driver | `fg_1200ag` (Family Guy V12.0 English/German), ROM zip `fg_1200ag.zip` (member `FG120ag.bin`, CRC d9734f94, matching pinned `sam.c`) |
| Emulator | `pinmame64.dll` built from PinMAME revision `8371478a7640f1896dcdf565aed340dc5df989ba`, SHA-256 `deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c` |
| Runs | fresh isolated state directories; service menu entered with the named Back key and Select presses; scenarios `tools/harness-scenarios/stern/bbh-switch-test-sweep.json`, `family-guy-2007-dedicated-switch-sweep.json`, `family-guy-2007-coil-sweep.json`, `family-guy-2007-lamp-sweep.json` |
| Retained | raw runs and frames under the working root's `review-artifacts/family-guy-2007/harness/`, sealed by `tools/build_external_evidence_manifest.py`; summaries in `evidence/runtime/sam/family-guy-fg_1200ag-*.json` |

## Switch test, matrix switches 1–64

Each row is the frame captured while the public address was held at 1. The third display line reads `LAST SW. #n`; the fourth prints the drive and return wire colours (the return colour is identical for every switch of a column and the drive colour for every switch of a row, and they were read against the manual's grid). With every switch at 0 the test prints `NONE`.

| Public | Name the ROM prints | Drive / return wires |
| ---: | --- | --- |
| 1 | BALL SAVER UP | GRN-BRN / WHT-BRN |
| 2 | BALL SAVER DOWN | GRN-BRN / WHT-RED |
| 3 | LEFT ORBIT S/U | GRN-BRN / WHT-ORG |
| 4 | R. 2-BANK BOTTOM | GRN-BRN / WHT-YEL |
| 5 | R. 2-BANK TOP | GRN-BRN / WHT-GRN |
| 6 | LT NEWTON ROLLOVER | GRN-BRN / WHT-BLU |
| 7 | RT NEWTON ROLLOVER | GRN-BRN / WHT-VIO |
| 8 | PIRATE TARGET | GRN-BRN / WHT-GRY |
| 9 | 1-BANK DROP TARGET | GRN-BRN / TAN-BLK |
| 10 | MEG TARGET | GRN-BRN / TAN-RED |
| 11 | SWITCH #11 | GRN-BRN / TAN-ORG |
| 12 | SWITCH #12 | GRN-BRN / TAN-YEL |
| 13 | TV EJECT | GRN-BRN / TAN-GRN |
| 14 | SWITCH #14 | GRN-BRN / TAN-BLU |
| 15 | TOURNAMENT START | GRN-BRN / TAN-VIO |
| 16 | START BUTTON | GRN-BRN / TAN-WHT |
| 17 | SWITCH #17 | GRN-RED / WHT-BRN |
| 18 | TROUGH #4 (L) | GRN-RED / WHT-RED |
| 19 | TROUGH #3 | GRN-RED / WHT-ORG |
| 20 | TROUGH #2 | GRN-RED / WHT-YEL |
| 21 | TROUGH #1 (R) | GRN-RED / WHT-GRN |
| 22 | TROUGH JAM | GRN-RED / WHT-BLU |
| 23 | SHOOTER LANE | GRN-RED / WHT-VIO |
| 24 | LEFT OUTLANE | GRN-RED / WHT-GRY |
| 25 | LEFT RETURN | GRN-RED / TAN-BLK |
| 26 | LEFT SLING | GRN-RED / TAN-RED |
| 27 | RIGHT SLING | GRN-RED / TAN-ORG |
| 28 | RIGHT RETURN | GRN-RED / TAN-YEL |
| 29 | RIGHT OUTLANE | GRN-RED / TAN-GRN |
| 30 | TOP BUMPER | GRN-RED / TAN-BLU |
| 31 | RIGHT BUMPER | GRN-RED / TAN-VIO |
| 32 | BOTTOM BUMPER | GRN-RED / TAN-WHT |
| 33 | LEFT RAMP MADE | GRN-ORG / WHT-BRN |
| 34 | SWITCH #34 | GRN-ORG / WHT-RED |
| 35 | EVIL MONKEY | GRN-ORG / WHT-ORG |
| 36 | SWITCH #36 | GRN-ORG / WHT-YEL |
| 37 | SWITCH #37 | GRN-ORG / WHT-GRN |
| 38 | SWITCH #38 | GRN-ORG / WHT-BLU |
| 39 | RIGHT ORBIT SPINNER | GRN-ORG / WHT-VIO |
| 40 | DEATH RETURN | GRN-ORG / WHT-GRY |
| 41 | 3 BANK BOT | GRN-ORG / TAN-BLK |
| 42 | 3 BANK MID | GRN-ORG / TAN-RED |
| 43 | 3 BANK TOP | GRN-ORG / TAN-ORG |
| 44 | (F)ART | GRN-ORG / TAN-YEL |
| 45 | F(A)RT | GRN-ORG / TAN-GRN |
| 46 | FA(R)T | GRN-ORG / TAN-BLU |
| 47 | FAR(T) | GRN-ORG / TAN-VIO |
| 48 | SNEAK RAMP | GRN-ORG / TAN-WHT |
| 49 | BEER CAN | GRN-YEL / WHT-BRN |
| 50 | MINI MEG TARGET | GRN-YEL / WHT-RED |
| 51 | MINI PETER TARGET | GRN-YEL / WHT-ORG |
| 52 | MINI RIGHT ORBIT | GRN-YEL / WHT-YEL |
| 53 | MINI LEFT ORBIT | GRN-YEL / WHT-GRN |
| 54 | MINI RAMP | GRN-YEL / WHT-BLU |
| 55 | MINI TROUGH | GRN-YEL / WHT-VIO |
| 56 | SWITCH #56 | GRN-YEL / WHT-GRY |
| 57 | RIGHT ORBIT | GRN-YEL / TAN-BLK |
| 58 | SWITCH #58 | GRN-YEL / TAN-RED |
| 59 | SWITCH #59 | GRN-YEL / TAN-ORG |
| 60 | SWITCH #60 | GRN-YEL / TAN-YEL |
| 61 | SWITCH #61 | GRN-YEL / TAN-GRN |
| 62 | SWITCH #62 | GRN-YEL / TAN-BLU |
| 63 | SWITCH #63 | GRN-YEL / TAN-VIO |
| 64 | CLAM EJECT | GRN-YEL / TAN-WHT |

## Switch test, dedicated switches

| Public held | Display while held |
| ---: | --- |
| 65 | LEFT COIN SLOT / LAST SW. D-1 |
| 66 | CENTER COIN SLOT / LAST SW. D-2 |
| 67 | RIGHT COIN SLOT / LAST SW. D-3 |
| 68 | FOURTH COIN SLOT / LAST SW. D-4 |
| 69 | FIFTH COIN SLOT / LAST SW. D-5 |
| 70 | DEDICATED SW. #6 / LAST SW. D-6 |
| 71 | L. POST SAVE / LAST SW. D-7 |
| 72 | R. POST SAVE / LAST SW. D-8 |
| 81 | RIGHT FLIPPER E.O.S. / LAST SW. D-12 |
| 82 | RIGHT FLIPPER E.O.S. / LAST SW. D-12 |
| 83 | LEFT FLIPPER E.O.S. / LAST SW. D-10 |
| 84 | LEFT FLIPPER E.O.S. / LAST SW. D-10 |
| 85 | U.R. FLIPPER E.O.S. / LAST SW. D-16 |
| 86 | U.R. FLIPPER E.O.S. / LAST SW. D-16 |
| 87 | U.L. FLIPPER E.O.S. / LAST SW. D-14 |
| 88 | U.L. FLIPPER E.O.S. / LAST SW. D-14 |
| -7 | TILT PENDULUM / LAST SW. D-17 |
| -6 | SLAM TILT / LAST SW. D-18 |
| -5 | TICKET NOTCH / LAST SW. D-19 |
| -4 | DEDICATED SW. #20 / LAST SW. D-20 |

Holding 82, 84, 86 or 88 (the flipper buttons D-11, D-9, D-15, D-13) shows the EOS of its pair because pinned PinMAME's flipper column mirrors the coil state into the EOS bit; the cabinet buttons themselves print no name. The bottom line of each frame prints the wire colour and `BLK`.

## Single Coil Test (V12.0)

The test steps these 30 selector positions in order and wraps to the first; the ROM skips Q20 and Q24. SELECT fires the displayed coil; in every position the public solenoid whose number equals the displayed `#n` changed. Positions in the retained run: 1–19, 21–23, 25–32.

| `#` | Name the ROM prints | Power / control wires printed |
| ---: | --- | --- |
| 1 | TROUGH UP-KICKER | YEL-VIO / BRN-BLK |
| 2 | AUTO LAUNCH | YEL-VIO / BRN-RED |
| 3 | 4-BANK DROP TARGET | YEL-VIO / BRN-BLK (the manual prints BRN-ORG) |
| 4 | BALL SAVER DOWN | YEL-VIO / BRN-YEL |
| 5 | CLAM EJECT | YEL-VIO / BRN-GRN |
| 6 | 1-BANK DROP TARGET | YEL-VIO / BRN-BLU |
| 7 | LEFT SLINGSHOT | YEL-VIO / BRN-VIO |
| 8 | RIGHT SLINGSHOT | YEL-VIO / BRN-GRY |
| 9 | BOTTOM BUMPER | YEL-VIO / BLU-BRN |
| 10 | RIGHT BUMPER | YEL-VIO / BLU-RED |
| 11 | TOP BUMPER | YEL-VIO / BLU-ORG |
| 12 | BALL SAVER UP | YEL-VIO / BLU-YEL |
| 13 | TV EJECT | YEL-VIO / BLU-GRN |
| 14 | UPPER LEFT FLIPPER | BLU-YEL / BLU-BLK |
| 15 | LEFT FLIPPER | GRY-YEL / ORG-GRY |
| 16 | RIGHT FLIPPER | BLU-YEL / ORG-VIO |
| 17 | LEFT MINI FLIPPER | BRN / VIO-BRN |
| 18 | RIGHT MINI FLIPPER | BRN / VIO-RED |
| 19 | EVIL MONKEY | BRN / VIO-ORG |
| 21 | MINI TROUGH | BRN / VIO-GRN |
| 22 | MEG SHAKE | BRN / VIO-BLU |
| 23 | FLASH: LOWER LEFT | ORG / VIO-BLK |
| 25 | FLASH: BACK LEFT | ORG / BLK-BRN |
| 26 | FLASH: BACK CENTER | ORG / BLK-RED |
| 27 | FLASH: BACK RIGHT | ORG / BLK-ORG |
| 28 | FLASH: BEER CAN | ORG / BLK-YEL |
| 29 | FLASH: MEG | ORG / BLK-GRN |
| 30 | FLASH: RIGHT ORBIT | ORG / BLK-BLU |
| 31 | FLASH: POPS | ORG / BLK-VIO |
| 32 | FLASH: LOWER RIGHT | ORG / BLK-GRY |

V3.00, V4.00, V8.00 and V11.0 firmware continue after #32 with two optional auxiliary coils before wrapping: `AUX 1: TICKET ADVANCE #33` (BRN WHT) and `AUX 3: TICKET ENABLE #35` (BRN ORG); firing them changed no public solenoid. V3.00 and V4.00 print the power and control wires without the ` / ` separator (the V8.00 and V11.0 frames were compared only by hash against V3.00's at the AUX positions, which they match).

## Single Lamp Test (all retained firmware versions draw identical frames)

Selector position *n* lights public lamp *n*. Each frame prints the lamp name, `LAMP #n` and `YEL-xxx / RED-xxx` (the drive and return wire colours, rows 7–10 of the lamp grid print `RED-VIO`, `RED-GRY`, `RED-WHT`, `RED`).

| Lamp | Name the ROM prints |
| ---: | --- |
| 1 | START BUTTON |
| 2 | TOURNAMENT START BUTTON |
| 3 | FAMILY PETER |
| 4 | FAMILY LOIS |
| 5 | FAMILY BRIAN |
| 6 | FAMILY CHRIS |
| 7 | FAMILY MEG |
| 8 | FAMILY STEWIE |
| 9 | (P)INBALL |
| 10 | P(I)NBALL |
| 11 | PI(N)BALL |
| 12 | PIN(B)ALL |
| 13 | PINB(A)LL |
| 14 | PINBA(L)L |
| 15 | PINBAL(L) |
| 16 | LEFT OUTLANE |
| 17 | LEFT RETURN |
| 18 | RAISE DEATH |
| 19 | GOOD OLD BOYS |
| 20 | SUPER GRIFFINS |
| 21 | CHICKEN FIGHT |
| 22 | SEXY PARTY |
| 23 | IPECAC CONTEST |
| 24 | (1) |
| 25 | (2) |
| 26 | (3) |
| 27 | RIGHT RETURN |
| 28 | RIGHT OUTLANE |
| 29 | TV |
| 30 | PINBALL |
| 31 | MULTIBALL |
| 32 | MEG JACKPOT |
| 33 | PIRATE |
| 34 | RIGHT NEWTON JACKPOT |
| 35 | FAR(T) |
| 36 | FA(R)T |
| 37 | F(A)RT |
| 38 | (F)ART |
| 39 | LEFT ORBIT CHRIS |
| 40 | LEFT ORBIT JACKPOT |
| 41 | DEATH |
| 42 | SKILL SHOT |
| 43 | 200K |
| 44 | 300K |
| 45 | 400K |
| 46 | 500K |
| 47 | CRAZY CHRIS |
| 48 | COLLECT BEERS |
| 49 | GIGGITY GIGGITY |
| 50 | HAPPY HOUR |
| 51 | REMEMBER WHEN |
| 52 | LARD MULTIBALL |
| 53 | EXTRA BALL |
| 54 | LEFT NEWTON JACKPOT |
| 55 | EVIL MONKEY JACKPOT |
| 56 | 3 BANK TOP |
| 57 | 3 BANK MID |
| 58 | 3 BANK BOT |
| 59 | NOT USED #59 |
| 60 | NOT USED #60 |
| 61 | BOTTOM BUMPER |
| 62 | MYSTERY |
| 63 | STEWIE |
| 64 | SHOOT AGAIN |
| 65 | RIGHT ORBIT LOIS |
| 66 | RIGHT ORBIT JACKPOT |
| 67 | SPINNER |
| 68 | MINI SHOOT AGAIN |
| 69 | BALL SAVER POST |
| 70 | STEWIE SPOT LIGHT |
| 71 | NOT USED #71 |
| 72 | NOT USED #72 |
| 73 | NOT USED #73 |
| 74 | NOT USED #74 |
| 75 | NOT USED #75 |
| 76 | NOT USED #76 |
| 77 | NOT USED #77 |
| 78 | NOT USED #78 |
| 79 | NOT USED #79 |
| 80 | NOT USED #80 |
