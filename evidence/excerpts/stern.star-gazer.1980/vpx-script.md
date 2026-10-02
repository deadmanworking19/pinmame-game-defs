# Star Gazer — known-working table script, controller bindings

The pinned script `Star Gazer (Stern 1980) v2.0.0.vbs` (UnclePaulie's table, "VPW standards") runs the ROM `stargzr` (`cGameName = "stargzr"`), `UseSolenoids = 2`, `UseLamps = 1` and `HandleMech = 0`; `Table1_Init` sets `Controller.HandleKeyboard = 0` and `Controller.HandleMechanics = 0`. The embedded script of the retained table equals the pinned file except for whitespace (every line compared with all whitespace removed). The bindings below were read from the script's code, not from sub names.

## Solenoid callbacks

| public output | callback | what it does |
| ---: | --- | --- |
| 3 | `DTBankCenterReset` | raises drop targets 25, 26 and 27 (the upper-left bank) after a 300 ms timer |
| 4 | `DTBankRightReset` | raises drop targets 28, 29 and 30 (the right bank) |
| 6 | `SolKnocker` | plays the knocker |
| 7 | `DTBankLeftReset` | raises drop targets 22, 23 and 24 (the left bank) |
| 12 | `SolBallRelease` | `BallRelease.kick 57, 10`: kicks the ball waiting on the release kicker toward the shooter lane |
| 19 | `SolGameOn` | sets `GOn` to the output state; used only for the backglass reels |
| 46 | `SolRFlipper` | right flipper (`sLRFlipper`) |
| 48 | `SolLFlipper` | left flipper (`sLLFlipper`) |

No callback exists for the slingshots (1, 2), the thumper bumpers (5, 8, 11) or the coin lockout (18); the table fires them from VPX events.

## Switch bindings

- Switch 33 is the ball sitting on the `BallRelease` kicker: `BallRelease_Hit` sets it to 1 and `BallRelease_UnHit` sets it to 0, and `Table1_Init` also sets it to 1 for the created ball. A second kicker, `Drain`, receives drained balls and returns them to the release kicker after 300 ms.
- `vpmTimer.PulseSw 15` from `RightSlingShot_Slingshot`, `PulseSw 16` from `LeftSlingShot_Slingshot`; `PulseSw 12`, `13`, `14` from `Bumper1_Hit`, `Bumper2_Hit`, `Bumper3_Hit`.
- Spinners: `PulseSw 5` from `sw5_Spin`, `PulseSw 4` from `sw4_Spin`, `PulseSw 9` from `sw9_Spin`.
- `Controller.Switch(34) = 1` and `Controller.Switch(35) = 1` while the outlane triggers `sw34` and `sw35` are hit and `0` when left; `PulseSw 36` and `PulseSw 37` from the star triggers `sw36` and `sw37`.
- Drop targets 22 to 30 hold their switch at 1 while the target is down (`controller.Switch(Switchid mod 100) = 1` when a dropped target finishes its animation, `= 0` when it is raised).
- Stand-up targets 10, 11, 17, 18, 19, 20, 21, 31, 32, 38, 39 and 40 pulse their switch (`vpmTimer.PulseSw switch mod 100`).
- `vpmNudge.TiltSwitch = 7`.

## Lamp bindings

`vpmMapLights AllLamps` binds each light in the `AllLamps` collection to the public lamp number held in its `TimerInterval`. Public lamps 1 to 12, 14, 17 to 30, 33 to 44, 46, 49 to 60 and 62 are bound this way. The script's `UpdateDTLamps` also reads `Controller.Lamp(13)` (high score), `Lamp(45)` (game over), `Lamp(61)` (tilt), `Lamp(11)` (shoot again) and `Lamp(63)` (match, and with `GOn` ball in play) for the backglass. No light is bound to public lamps 13, 15, 31, 45, 47, 61 or 63.

## General illumination

The script reads no general-illumination output. `Table1_Init` calls `SetRelayGI 0` and, two seconds later, `SetRelayGI 1`; the value never follows the ROM.
