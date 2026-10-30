# Scared Stiff - flipper-button polarity run on ss_15

LibPinMAME harness run made on 2026-10-30 against `ss_15` (Scared Stiff (1.5), ROM archive SHA-256
`18451cd4955292451a3adf7da877d5a8de2c311ef87c8ba6c5105ae2d0f5689b`) from a new, empty state
directory, with the committed scenario `tools/harness-scenarios/wpc-95/ss-flipper-button-polarity.json`
(SHA-256 `fddec3f6677aa7eadb0000c301e2fd9527b30598800cc66447c93cb1fd684f80`) and
`--handle-mechanics 1`. The library is `pinmame64.dll` built from pinned PinMAME
`46e1a01a0f73dc5ce163d98db1ae435883ecc450`, SHA-256
`8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`. The run directory is retained
as `external:pinmame-runtime-evidence/scared-stiff-1996/ss_15-flipper-button-polarity/`: `run.json`
SHA-256 `38f3fe6a7bfa5eb1dbf2c207497e82536e3f344519524bfacaca58f971c91cca`, pinned with the copied
scenario, DMD frames and PinMAME state directory by its external evidence manifest (SHA-256
`bfd74ab97a3623b8b5f10fa3bf687276cdb7339c3e23505d2d0cdd66468d2bfb`, 17 files, 938770 bytes). The
harness wrote switches directly; PinMAME keyboard handling was off.

The scenario presents four balls on trough switches 32-35, presses service Escape once, closes the
coin door, inserts two coins and presses Start. The trough eject (solenoid 9) first fires at
39.578 s, so a game is running. Every output-change event for solenoids 45-48 in the run, with the
button writes around them:

| Time (s) | Event |
| ---: | --- |
| 42.625 | switch 112 written 1 |
| 42.641 | solenoid 45 (Lower Right Flipper Power) 1, solenoid 46 (Lower Right Flipper Hold) 1 |
| 42.672 | solenoid 45 0 |
| 43.625 | switch 112 written 0; solenoid 46 0 |
| 44.625 | switch 114 written 1; solenoid 47 (Lower Left Flipper Power) 1, solenoid 48 (Lower Left Flipper Hold) 1 |
| 44.656 | solenoid 47 0 |
| 45.625 | switch 114 written 0; solenoid 48 0 |

No event for 45-48 occurs while 112 and 114 rest at 0.

## Reading

The ROM treats public 112 and 114 at level 1 as the pressed lower right and lower left cabinet
buttons: each write of 1 pulses the power winding and holds the hold winding until the write of 0.
`ss.c` declares `FLIP_SOL(FLIP_L)`, so 45-48 are the ROM's own Fliptronic writes. WPC-95 reads the
flipper column complemented (`WPC_FLIPPERSW95` returns `~swMatrix`), so the contact the switch
matrix sees rests open. The run proves emulator-facing polarity and causality, not opto
construction or coil force.
