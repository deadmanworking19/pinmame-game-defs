# Batman Forever retained table script: machine-specific bindings

Source: `script.vbs` extracted with vpxtool git:v0.33.3 from `Batman Forever (Sega 1995) 1.3.vpx` (table SHA-256 `e1eb059e75fba1b6fc61c40a01e98d466a33786644125f707a0f164c8dbb1792`, script SHA-256 `305f1827f7877d664f16722b8e9a4863457493211751c5f6f8d4f515547c78d6`). Table header "VP9 Version 1.2 Desktop mfuegemann 2014", "Crude VPX conversion by DevaL", 1.0-1.1 updates by drakkon, 1.2 playfield and inserts by Sheltemke, 1.3 VR room by TastyWasps and Sixtoe; `Const cgamename = "batmanf"`. Factual summary by the curator; line numbers are the extracted script's. The table bounds are 1093 x 2162 VPX units.

## Library and controller

- Line 126 `Const UseSolenoids=2`; line 136 `LoadVPM "01560000","DE.VBS",3.1`.
- `BF_Init` (318-399): `.HandleMechanics=0`, `.HandleKeyboard=0`; `vpmNudge.TiltSwitch=1`; `vpmMapLights AllLights` (line 353).
- Line 356 `bsTrough.InitSw 0,14,13,12,11,0,0,0`, `bsTrough.Balls=4`: four trough positions, 14 at the exit. Line 363 `bsBallRelease.InitSaucer BallRelease, 15, 90, 5`: the up-kicker saucer at 15. Line 366 `bsBallLock.InitSw 0,62,61,60,0,0,0,0` with `InitKick BallLock, 180, 5` and `CreateEvents "bsBallLock", BallLock`: the Batcave lock stack, 62 at its exit.
- Lines 371-379 `mBWGun`: `vpmMechOneSol + vpmMechReverse + vpmMechNonLinear`, `Sol1 = 14`, `Length = 500`, `Steps = 200`, `AddSw 46,0,3` and `AddSw 46,197,200`, callback `UpdateBWGun`.

## Solenoid callbacks (lines 156-190)

1 `SolTroughBall` (moves one ball from bsTrough to the up-kicker stack and creates it at BallRelease); 2 `bsBallRelease.SolOut`; 3 `Autoplunger` (`Plunger.Kick`); 4 `SolVUK` (kicks `VUK_Bottom` when 32 is closed, then opens 32); 5 `SolTopEject` (kicks `TopEjectKicker` when 41 is closed); 6 comment "not used"; 7 `DropTargetBankSolDropUp` (raises 18-21); 8 `SolKnocker`; 9 `bsBallLock.SolOut`; 10 `Sol10` (shows GIString1 when on); 11 `SolGI` (hides GIString2 when on, shows it when off: an inverted G.I. relay); 12 `SolRampDiverter` (makes `RampDiverter` non-collidable and swings `pDiverter` while on); 13 comment "not used"; 14 `SolBatwingMotor` (motor sound only; `mBWGun.Sol1 = 14` moves the cannon); 15 `SolFireBWGun` (kicks `BWGun` at the current gun angle, opens 44 and pulses 45); 16 `SolBatCaveExit` (kicks `BatCaveExitKicker` when 30 is closed); 17-21 commented out (bumpers and slings fire from their own `_Hit`/`_Slingshot` events); 22 `KickSaver` (`LaserKick.fire` / `pullback`); 25-32 `SolFlasher1R`-`SolFlasher8R`; `sLLFlipper` `SolLFlipper` (LeftFlipper); `sLRFlipper` `SolRFlipper` (RightFlipper and URightFlipper together).

## Switch writes

- Key handlers (645-686): the left and right flipper keys write 63 and 64 directly, then `KeyDownHandler` (de.vbs `vpmKeyDown`) writes 84 and 82; the plunger key writes 49 (comment "Auto Launch").
- Triggers: 16 shooter lane; 22-24 top lanes; 33 laser-kick outlane (`vpmTimer.Pulsesw 33`); 34, 37, 38, 39 return lanes and outlane; 40 U-turn; 47, 48 orbits; 52 left ramp enter; 53 with the comment "Left Ramp Exit - Manual is wrong"; 54 "Middle Ramp Exit - Manual is wrong"; 55 right ramp enter; 56 right ramp exit.
- Kickers: 30 `BatCaveExitKicker_Hit`; 32 `VUK_Bottom_Hit`; 41 `TopEjectKicker_Hit`; 44 `BWGun_Hit`.
- Targets: drop targets 18-21 through `DTArray` (`DT18 = Array(sw18t, sw18a, sw18p, 18, 0)` and so on, lines 3540-3547); stand-ups 25-29, 42, 43, 50, 51 through `STArray` (lines 3865-3878), each pulsed by `vpmTimer.PulseSw`.
- Bumpers 57-59 and slingshots 35/36 pulse their switches from `Bumper5x_Hit` and `LeftSlingshot_Slingshot`/`RightSlingshot_Slingshot`.
- `Sub Sw18_Hit` (line 923) names no existing object and never runs.

## Lamps

`vpmMapLights AllLights` binds each Light in the `AllLights` collection by its TimerInterval. The collection holds 60 Lights: every lamp 1-64 except 34, 36, 37, 38, 59 and 60 has one member, and two have two. `Lamp33` and `Lamp34` both carry TimerInterval 33, at the left edge of the table; `Lamp58` and `Lamp59` both carry 58, `Lamp59` sitting in the right turbo bumper. So the table never lights anything from lamp 34 or 59. `GIString1` (Lamp57-59) is shown while output 10 is on; `GIString2` (Light004-Light034, with Light023 listed twice, plus Lamp57-59) is shown while output 11 is off.

## Flashers

`SolFlasher1R`-`8R` switch Light objects: 1R `FLamp1R`; 2R `FLamp2Ra`, `FLamp2Rb`; 3R `Flasher3R`; 4R `Flasher4R`, `Flasher4Ra`; 5R `Flasher5r`; 6R `Flasher6r`; 7R `Flasher7r`; 8R `FLamp8R`. The `Setflash` fading routine updates Flasher sprites whose alpha assignment is commented out (lines 1029-1045) and that are never made visible.

## Visuals that do not match their switches

`LeftSlingshot_Slingshot` animates the `LSling*` rubbers (x about 236) and the arm primitive `sling2` (x 745.0); `RightSlingshot_Slingshot` animates the `RSling*` rubbers (x about 752) and `sling1` (x 272.4). Only the two arm primitives are crossed; the switch walls, rubbers and coil events are on their own sides.
