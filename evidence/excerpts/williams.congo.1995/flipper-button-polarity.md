# Congo - Fliptronic input polarity run on congo_21

LibPinMAME harness run made on 2026-10-30 against `congo_21` (Congo (2.1), ROM archive SHA-256
`4325c2d20eca9b9c36eacf7fe0e085dffbaa405fcd731c92706496e62e2a8437`) from a new, empty state
directory, with the committed scenario `tools/harness-scenarios/wpc-95/congo-flipper-button-polarity.json`
(SHA-256 `e20e45b456e15bddbbf773f8a4dcae248b2a13074344084f81cb702cf52db107`) and
`--handle-mechanics 1`. The library is `pinmame64.dll` built from pinned PinMAME
`46e1a01a0f73dc5ce163d98db1ae435883ecc450`, SHA-256
`8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`. The run directory is retained
as `external:pinmame-runtime-evidence/congo-1995/congo_21-flipper-button-polarity/`: `run.json`
SHA-256 `ed701eb404b26962f9192a221e01c89dc7b6e7af809b7243abf22c1895a14ae5`, pinned with the copied
scenario, DMD frames and PinMAME state directory by its external evidence manifest (SHA-256
`4368106c5dde59d2adfbf70c203dcd2fe7accbc8c35a6890db59d4ac27691f5a`, 23 files, 1054174 bytes). The
harness wrote switches directly; PinMAME keyboard handling was off.

The scenario presents four balls on trough switches 32-35, presses service Escape once, closes the
coin door, inserts two coins and presses Start. The trough eject (solenoid 9) first fires at
39.222 s, so a game is running; it fires again every one to three seconds for the rest of the run
because no ball reaches the shooter lane. Every output-change event for solenoids 33-36 and 45-48 in
the run, with the Fliptronic writes around them (times rounded to the millisecond):

| Time (s) | Event |
| ---: | --- |
| 42.619 | switch 112 written 1 |
| 42.625 | solenoid 45 (Lower Right Flipper Power) 1, solenoid 46 (Lower Right Flipper Hold) 1 |
| 42.658 | solenoid 45 0 |
| 43.620 | switch 112 written 0 |
| 43.627 | solenoid 46 0 |
| 44.621 | switch 114 written 1 |
| 44.636 | solenoid 35 (Upper Left Flipper Power) 1, 36 (Upper Left Flipper Hold) 1, 47 (Lower Left Flipper Power) 1, 48 (Lower Left Flipper Hold) 1 |
| 44.669 | solenoids 35 and 47 0 |
| 45.623 | switch 114 written 0; solenoids 36 and 48 0 |
| 46.625 | switch 118 written 1 |
| 46.626 | solenoids 35, 36, 47 and 48 1 |
| 46.659 | solenoids 35 and 47 0 |
| 47.626 | switch 118 written 0 |
| 47.629 | solenoids 36 and 48 0 |
| 48.628 | switch 116 written 1 |
| 48.637 | solenoids 45 and 46 1 |
| 48.671 | solenoid 45 0 |
| 49.629 | switch 116 written 0 |
| 49.640 | solenoid 46 0 |
| 50.630 | switch 115 written 1 |
| 51.632 | switch 115 written 0 |

No event for 33-36 or 45-48 occurs while 112, 114, 116 and 118 rest at 0, and none follows the
write of 115.

## Reading

The ROM treats public 112, 114, 116 and 118 at level 1 as a pressed cabinet button: each write of 1
pulses the power winding and holds the hold winding until the write of 0. 116 fires the lower right
flipper exactly as 112 does, and 118 fires the lower left and the upper left flipper exactly as 114
does, so the ROM reads both optos of each cabinet button. `congo.c` declares
`FLIP_SOL(FLIP_L | FLIP_UL)`, so 35/36 and 45-48 are the ROM's own Fliptronic writes, and the
flipper column's mask byte is 0x00. WPC-95 reads the flipper column complemented
(`WPC_FLIPPERSW95` returns `~swMatrix`), so the contact the switch matrix sees at each button rests
open. 115, the upper right end-of-stroke position PinMAME does not synthesize for this driver, moved
none of these outputs. The run proves emulator-facing polarity and causality, not opto
construction, coil force or which physical switches are fitted.
