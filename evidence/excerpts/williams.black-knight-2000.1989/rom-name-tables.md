# Black Knight 2000 — ROM switch and coil name tables

Decoded by `tools/bk2k_rom_name_tables.py` (through `tools/s11_rom_name_tables.py`) from the user-authorized local ROM archives; no ROM
bytes are reproduced. Each table is a run of fixed 16-byte entries in the 32 KiB **U27** program ROM (the member that
Earthshaker keeps in U26). A byte with bit 7 set is the character in its low seven bits followed by the display's period segment,
and the ROM font codes `o` and `p` stand for `-` and `/`. A stored `z` is drawn as a quotation mark: entries 25-30 below
display as `WIN "W" LANE` and so on. Entries are shown trimmed of padding. There is no lamp name table in the ROM; the 64 lamp
names come from the Single Lamps test display (see the runtime evidence).

| Driver | ROM member | Member SHA-256 | Switch table | Coil table |
| --- | --- | --- | --- | --- |
| bk2k_l4 | bk2k_u27.l4 | `0c23809ec6ed0f0e777a980e62d8c5e658f7bb1dd4ad1b019fdaa199f10ab7d0` | 0x283a | 0x1da2 |
| bk2k_la2 | bk2k_u27.la2 | `5741a61c7253565dca8ddac6142100bb4b61780ee759d524654c8b969172af21` | 0x283a | 0x1da2 |
| bk2k_lg3 | u27-lg3.rom | `f6b6d8aa4c245a8b398ee133c868ca35fb2b70bcbbd0402aecde6696d3b6be4a` | 0x1f7e | 0x2a43 |
| bk2k_pa5 | bk2k_u27.pa5 | `1ea037d8faa066a41a12f4e9e1ca736cb7cdc3dae01fc687a4b90da5b9cb2a75` | 0x243b | 0x1f00 |
| bk2k_pa7 | bk2k_u27.pa7 | `79a893b2b67860f27219446ddd7ecf249a94846904761fc3d0caad92cda8c1f7` | 0x2bb7 | 0x1ddc |
| bk2k_pu1 | u27-pu1.rom | `eac6888eb94274c29d820da7bd206135ad2af22e210314ae21d2901c500c411c` | 0x2822 | 0x1d8a |

Not read: `bk2k_pf1` (its archive is not in the local ROM corpus) and `bk2k_lg1` (the local archive holds `bk2kgu26.lg1` and `bk2kgu27.lg1`,
whose CRCs do not match the ROMs pinned `s11games.c` declares for that set, so it was not loaded). `bk2k_pa5` stores only U26 and U27;
its sound ROMs come from the parent `bk2k_l4` archive.

## bk2k_l4 switch table (public switch address = entry number)

The table holds 59 entries; the entry after it reads as adjustment text and is not a switch name. Entries 2, 14, 15 and 56 are blank.

| Switch | ROM text |
| --- | --- |
| 1 | PLUMB TILT |
| 2 | (blank) |
| 3 | CREDIT BUTTON |
| 4 | RIGHT COIN |
| 5 | MIDDLE COIN |
| 6 | LEFT COIN |
| 7 | SLAM TILT |
| 8 | HIGH SCORE RESET |
| 9 | PLAYFIELD TILT |
| 10 | OUTHOLE |
| 11 | TROUGH 1 |
| 12 | TROUGH 2 |
| 13 | TROUGH 3 |
| 14 | (blank) |
| 15 | (blank) |
| 16 | MOTOR UP |
| 17 | LEFT BUMPER |
| 18 | LEFT SLING |
| 19 | RIGHT BUMPER |
| 20 | RIGHT SLING |
| 21 | LOWER BUMPER |
| 22 | LOOP END 1 |
| 23 | LOOP END 2 |
| 24 | MOTOR DOWN |
| 25 | WIN zWz LANE |
| 26 | WIN zIz LANE |
| 27 | WIN zNz LANE |
| 28 | WAR zWz LANE |
| 29 | WAR zAz LANE |
| 30 | WAR zRz LANE |
| 31 | UPPER RAMP ENTRY |
| 32 | LOWER RAMP EXIT |
| 33 | UPPER TARGET 3 |
| 34 | UPPER TARGET 2 |
| 35 | UPPER TARGET 1 |
| 36 | UPPER LOCK LOWER |
| 37 | UPPER LOCK MID |
| 38 | UPPER LOCK UPPER |
| 39 | LEFT OUTLANE |
| 40 | RIGHT EJECT |
| 41 | RIGHT 3-BANK 1 |
| 42 | RIGHT 3-BANK 2 |
| 43 | RIGHT 3-BANK 3 |
| 44 | LEFT 3-BANK 1 |
| 45 | LEFT 3-BANK 2 |
| 46 | LEFT 3-BANK 3 |
| 47 | BALL POPPER |
| 48 | RIGHT OUTLANE |
| 49 | U-TURN 1 |
| 50 | U-TURN 2 |
| 51 | U-TURN 3 |
| 52 | U-TURN 4 |
| 53 | PLUNGER |
| 54 | RIGHT RETURN LN |
| 55 | LEFT RETURN LANE |
| 56 | (blank) |
| 57 | LANE CHANGE RGHT |
| 58 | LANE CHANGE LEFT |
| 59 | MAGNA SAVE |

## bk2k_l4 coil table (entry order = coil-test order)

The Coil Test (service test 05; runtime evidence `evidence/runtime/system-11/black-knight-2000-l4-service-and-mechanisms.json`, run
`l4-coil`) fires one public address per entry in this order; the address column is that run's pulse, not a value stored beside the text.
Steps 1-8 are an A-side pulse followed by a C-side pulse (relay 12 energized for the C side); public 23, the game-on enable, is not a
coil-test step.

| Entry | ROM text | Address pulsed at that step |
| --- | --- | --- |
| 1 | OUTHOLE | 1 |
| 2 | RED BOLT | 25 |
| 3 | BALL SERVE | 2 |
| 4 | BLUE BOLT | 26 |
| 5 | LEFT 3 BANK | 3 |
| 6 | CENTER FLASHER | 27 |
| 7 | RIGHT 3 BANK | 4 |
| 8 | FLIP LANE FLASH | 28 |
| 9 | UNUSED | 5 |
| 10 | MID. DROP FLASHER | 29 |
| 11 | BALL POPPER | 6 |
| 12 | RAMP FLASHER | 30 |
| 13 | LEVEL 3 KICKER | 7 |
| 14 | RIGHT FLASHER | 31 |
| 15 | RIGHT EJECT | 8 |
| 16 | 3-LOCK FLASHER | 32 |
| 17 | INSERT G.I. | 9 |
| 18 | LEVEL 2 G.I. | 10 |
| 19 | LEVEL 1 G.I. | 11 |
| 20 | A/C   SELECT | 12 |
| 21 | KICKBACK | 13 |
| 22 | KNOCKER | 14 |
| 23 | MAGNA SAVE | 15 |
| 24 | MOTOR 3 BANK | 16 |
| 25 | LEFT  BUMPER | 17 |
| 26 | LEFT  KICKER | 18 |
| 27 | RIGHT BUMPER | 19 |
| 28 | RIGHT KICKER | 20 |
| 29 | LOWER BUMPER | 21 |
| 30 | UNUSED | 22 |

## Entries that differ from bk2k_l4

| Driver | Table | Entry | bk2k_l4 | This driver |
| --- | --- | --- | --- | --- |
| bk2k_la2 | both | - | (no difference) | (no difference) |
| bk2k_lg3 | switch | 41 | RIGHT 3-BANK 1 | G |
| bk2k_lg3 | switch | 42 | RIGHT 3-BANK 2 | H |
| bk2k_lg3 | switch | 43 | RIGHT 3-BANK 3 | T |
| bk2k_lg3 | switch | 44 | LEFT 3-BANK 1 | K |
| bk2k_lg3 | switch | 45 | LEFT 3-BANK 2 | N |
| bk2k_lg3 | switch | 46 | LEFT 3-BANK 3 | I |
| bk2k_pa5 | both | - | (no difference) | (no difference) |
| bk2k_pa7 | both | - | (no difference) | (no difference) |
| bk2k_pu1 | both | - | (no difference) | (no difference) |

The German set's switch names for entries 41-46 are single letters (`G H T` and `K N I`, the letters of lamps 41-46 on the two
drop-target banks); its Switch Edges test was not run, so what that test displays for them is not established.
