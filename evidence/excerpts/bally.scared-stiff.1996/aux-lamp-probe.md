# Scared Stiff - auxiliary lamp probe on six ROMs

LibPinMAME harness runs made on 2026-10-30, one per locally held ROM, each from a new, empty
state directory with the committed scenario `tools/harness-scenarios/wpc-95/ss-aux-lamp-probe.json`
(SHA-256 `0b7367d8040988cde7c1b4182522845492479e152ded91617504379edf353ce8`) and `--handle-mechanics 1`, which enables `ss.c`'s Spider Wheel mech.
The scenario boots with balls on trough switches 32-35, presses service Escape once to leave the
fresh-NVRAM factory-settings loop, watches attract mode for 120 s, closes the coin door, inserts
two coins, presses Start, then rolls each skull lane (switches 71, 72, 73) twice, 4 s apart, and
watches the game for 30 s more; every run lasts about 221 s. The library is `pinmame64.dll` built
from pinned PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`, SHA-256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`.
Each run directory (`run.json`, the copied `scenario.json`, its DMD frames and the PinMAME state
directory) is retained under `external:pinmame-runtime-evidence/scared-stiff-1996/<driver>-aux-lamp-probe/`
and pinned by its own external evidence manifest. The harness never calls `PinmameSetDIP`.

Counts are output-change events the harness recorded over the whole run: lamp events at public
lamp addresses 91-98 and 101-108, and solenoid events at 37 (Aux Lamp Clock), 38 (Aux Lamp Data)
and their LPDC mirrors 41 and 42.

| Driver | PinMAME description | ROM archive SHA-256 | Aux lamp addresses that changed | Aux lamp events | Solenoid 37/38/41/42 events | First aux event |
| --- | --- | --- | ---: | ---: | --- | --- |
| `ss_15` | Scared Stiff (1.5) | `18451cd4955292451a3adf7da877d5a8de2c311ef87c8ba6c5105ae2d0f5689b` | 0 | 0 | 0 | - |
| `ss_14` | Scared Stiff (1.4) | `4811143062ede69b08210af1ffdab76088a2be069c9042a6326cace6e69e823c` | 0 | 0 | 0 | - |
| `ss_12` | Scared Stiff (1.2) | `f6a660dd3f93352235d9b396bb78d88a5c4dd457cfe47988c8b637122a53b9df` | 0 | 0 | 0 | - |
| `ss_03` | Scared Stiff (0.3 Prototype) | `ba16667b8ddb51e38fda045969803f7fe8de2da8a7a2457263e32a28f11f2495` | 0 | 0 | 0 | - |
| `ss_01` | Scared Stiff (D.01R Prototype, Sound 0.25) | `066891e65a81c39240cea130206447b166c716e9f5f5c2845b6a3d2300d57814` | 16 | 15155 | 37: 83, 38: 197, 41: 83, 42: 197 | 18.016 s |
| `ss_01b` | Scared Stiff (D.01R Prototype Coin Play, Sound 0.25) | `885da9964ebf6127be6f7430d2f4f5fbbacf12beff77deb803054396c266536e` | 16 | 15203 | 37: 79, 38: 191, 41: 79, 42: 191 | 21.266 s |

| Driver | `run.json` SHA-256 | Manifest SHA-256 | Files | Bytes |
| --- | --- | --- | ---: | ---: |
| `ss_15` | `d3a9b8c39aebfb1f8f8718a628c0d31057ff7b137d051ec622b884bb6b4355d1` | `8c5010a36ecea3fa2c3fb6983657df4cc0c3d80c3771e09909221b4adad7aa95` | 21 | 5945103 |
| `ss_14` | `ccd65a677c05329f529914b91c3b30f6c8619b4fb2439592e48098f6fa81e95c` | `8ff79480cc1f8560af05e2f58f1540a418e6a69ae861f404493b819d428bfaf0` | 21 | 5816945 |
| `ss_12` | `b1521bde7d46aa51bebcf37af74175fe93f10b7773d50e9b9bdfe6ac3f578f26` | `1ac9b17cffbc9b23adf6f49acdc82040f75a144fcb8391fcae58890f2fe1fa48` | 21 | 5842826 |
| `ss_03` | `bccab0a494db8248b80bc6ab919ad1a9028abf02facc4e98d6f8680cf0bc6cec` | `abbab3c18ccfc461ade41dd0f19054a732f8850aa55566d229b14fd965575f7c` | 21 | 5452649 |
| `ss_01` | `d757f2aae09451540f3fc879d62e88e99646cd4126cccdbf84c0571a72668503` | `da7e1d4f78f1665a282b50e251f2760c8af4518807f4f0faa9af4ce422f9c2be` | 21 | 6043686 |
| `ss_01b` | `e9ba01ac981b766ef2462f42dc76567d94a1af2e147796aec857caa20d4f3521` | `30983127a1c9b2c12516b52a71d1d1ae61396c0f688d311b8c77f9bc298cc1a3` | 21 | 5963268 |

## Reading

The two D.01R prototype ROMs drive all sixteen auxiliary lamp addresses through the HC4094 chain
`ss.c` models, clocking solenoids 37 and 38 from attract mode on. The 0.3 prototype ROM and the
production 1.2, 1.4 and 1.5 ROMs never change any of those addresses or lines in the same
scenario, although each of them starts the game and reacts to the six skull-lane rolls. `ss_11`
and `ss_11s10` are not in the local ROM library and were not run.

A run proves only what the ROM wrote under these conditions. Silence on the later ROMs is not on
its own proof that a production machine has no skull board: that rests on Midway's development
notes (`development-notes-pile-o-skulls.md`). The runs show which firmware expects the board, and
that production firmware leaves PinMAME's auxiliary columns at zero.
