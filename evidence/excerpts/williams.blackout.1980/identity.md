# Williams Blackout (game 495) - Identity

Sources:

- IPDB machine 317, `https://www.ipdb.org/machine.cgi?id=317`, retained as the Wayback Machine capture `20250218215702` (fetched through its `id_` address, so the capture carries no archive banner) at `external:pinmame-manuals/by-machine/williams.blackout.1980/ipdb-317.html`.
- The retained OPDB snapshot `external:pinmame-review-artifacts/opdb-import/latest-opdb.json` (SHA-256 `690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93`), entries `GRwYo` and `GRwYo-MQoPw`.
- The pinned PinMAME `src/wpc/s6games.c` (lines 245-311), `src/wpc/s6.c` (`s6_6digit_disp`, lines 42-49) and `src/wpc/driver.c` (lines 2644-2649) at `46e1a01a0f73dc5ce163d98db1ae435883ecc450`.
- The covers and title blocks of the instruction booklet and the drawing set.

Method: the IPDB page's text was extracted from the retained HTML and read; the OPDB entries were read from the snapshot JSON; the PinMAME block was read from the pinned source. Field values are quoted as they appear.

## IPDB 317 (header and fields, as captured)

- `Blackout / IPD No. 317 / June, 1980 / 4 Players`
- `Manufacturer: Williams Electronics, Incorporated (1967-1985) [Trade Name: Williams ]`
- `Date Of Manufacture: June, 1980`
- `Model Number: 495`
- `MPU: Williams System 6`
- `Type: Solid State Electronic (SS)`
- `Production: 7,050 units ( confirmed )`
- `Theme: Outer Space - Space Fantasy`
- `Notable Features: Flippers (2), Pop bumpers (3), Slingshots (2), Standup targets (6), 3-bank drop targets (2), Spinning targets (3), Kick-out hole (1). Lane change .`
- `Design by: Claude Fernandez`
- `Art by: Constantino Mitchell , Jeanine Mitchell`
- `Sound by: Paul Dussault`
- `Software by: Paul Dussault`
- Notes, in part: "Paul Dussault did the French Speech Processing for this game." "This playfield layout was also used on Rowamet's 'Heavy Metal' and Taito do Brasil's 1983 'Vortex' . A nearly identical layout was used on Williams' 1982 'Warlok' ." The general-illumination sentence is quoted in `cabinet-and-power.md`.
- File links: `Williams_1980_Blackout_Manual_with_paginated_schematics.pdf`, `Williams_1980_Blackout_Operators_Handbook.pdf`, `Williams_1980_Blackout_Schematics_pages_numbered_7_through_22.pdf`, `Williams_1980_Blackout_ROM_L_1.zip` and `blkou_f1.zip` (labelled `French Speech Romset`).

## OPDB snapshot

- Group `GRwYo`, `Blackout`, shortname `BO`, year `1980`.
- Machine `GRwYo-MQoPw`, `Blackout`, `physicalMachine: 1`, `ipdbId: 317`, `manufactureDate: 1980-06-01`, manufacturer `Williams` (`Williams Electronic Games, Inc.`), `type: ss`, `display: alphanumeric`, `playerCount: 4`.
- The same group also holds `GRwYo-MQ2RR` (Black Hole, Giuliano Lodola, IPDB 4087), `GRwYo-M9RK0` (Vortex, Taito, IPDB 4576) and `GRwYo-MvBnV` (Black Hole, LTD do Brasil, IPDB 5891). They are other manufacturers' machines and have no PinMAME driver in this record.

## PinMAME (pinned revision)

s6games.c, block headed `/ Blackout - Sys.6 (Game #495)`:

- `INITGAMEFULL(blkou,s6_6digit_disp,0,46,22,21,23,44,43,0)`: no left flipper-copy switch, right flipper-copy switch 46, and special switches 22, 21, 23, 44, 43 and 0 for solenoid slots 17-22.
- `CORE_GAMEDEF(blkou,l1,"Blackout (L-1)",1980,"Williams",s6_mS6S,0)` and five clones of `l1`:
  - `l1ff`, `"Blackout (L-1 Free Play Fix)"`;
  - `f1`, `"Blackout (L-1, French Speech)"`;
  - `f1ff`, `"Blackout (L-1, French Speech, Free Play Fix)"`;
  - `t1`, `"Blackout (T-1 Ted Estes)"`;
  - `t1ff`, `"Blackout (T-1 Ted Estes, Free Play Fix)"`.
- ROM members:

| Driver | Game ROMs | Sound | Speech |
|---|---|---|---|
| `blkou_l1` | `gamerom.716` CRC 4b407ae2, `green1.716` 2145f8ab, `green2.716` 1c978a4a | `sound2.716` c9103a68 | `v_ic7.532` 87864071, `v_ic5.532` 046a96d8, `v_ic6.532` 0104e5c4 |
| `blkou_l1ff` | as l1 with `green1fpfix.716` 31f9396a | as l1 | as l1 |
| `blkou_f1` | as l1 | as l1 | `speech7f.532` bdc1b0b1, `speech6f.532` 9b7e4ae9, `speech5f.532` 9040f34a, `speech4f.532` 29c4abde |
| `blkou_f1ff` | as l1ff | as l1 | as f1 |
| `blkou_t1` | as l1 with `green2a.716` 16621eec | as l1 | as l1 |
| `blkou_t1ff` | `gamerom.716`, `green1fpfix.716`, `green2a.716` | as l1 | as l1 |

driver.c comments, as printed:

- `DRIVER(blkou,l1)        //S6-495:   06/80 W Blackout (L-1)`
- `DRIVER(blkou,l1ff)      //          06/80 W Blackout (L-1 Free Play Fix)`
- `DRIVER(blkou,f1)        //          06/80 W Blackout (L-1 French speech)`
- `DRIVER(blkou,f1ff)      //          06/80 W Blackout (L-1 French speech, Free Play Fix)`
- `DRIVER(blkou,t1)        //                  Blackout (T-1 /10 Scoring Ted Estes)`
- `DRIVER(blkou,t1ff)      //                  Blackout (T-1 /10 Scoring Ted Estes, Free Play Fix)`

## Williams documents

- Instruction booklet: cover `16P-495-103`, `Game No. 495`, `April, 1980`.
- Drawing set: game `495` in each drawing's title block; the manual's cover number reads `16P-495-101`.
- The booklet's Table 1 prints the game identification `1495 1` for Function 00 (`diagnostics.md`), and the harness boot showed `1495 1` in the player 1 display.

## Notes

- IPDB 317, OPDB `GRwYo-MQoPw`, model 495 and the PinMAME title agree on the machine.
- OPDB's `display: alphanumeric` does not describe the machine: PinMAME's `s6_6digit_disp` (in `s6.c`) declares four six-digit seven-segment player displays and two two-digit seven-segment displays, the booklet reads the game identification, every function and every test number from numeric displays, and the harness runs decode every frame they cite as seven-segment digits.
- All six drivers run the same `gamerom.716`. `l1ff`, `f1ff` and `t1ff` substitute a free-play fix for `green1.716`, `f1` and `f1ff` substitute French speech ROMs, and `t1`/`t1ff` substitute `green2a.716`, which driver.c's comment calls `/10 Scoring`. None of them is described as a different playfield, so all six are firmware variants of one physical machine.
- The user's ROM library also holds `blkou_hf.zip`, which is byte-identical to `blkou_l1.zip`. No pinned driver is named `blkou_hf`, so it is not a driver of this record.
