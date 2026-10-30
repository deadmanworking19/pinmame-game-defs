# Gladiators (Premier 1993) VPX v1.1.1 (Kiwi): controller bindings

Source: `Gladiators (Premier 1993) v1.1.1/Gladiators (Premier 1993) v1.1.1.vbs` in the pinned `jsm174/vpx-standalone-scripts`
corpus at revision `15d112648a1b94b9f59eb8b3c335d57283653c50`, the table script by Kiwi: a 46,453-byte LF blob, SHA-256
`25060187b97e5a57499429689be0c247003d26342bed632961d0cd9ba02cfe69` (the local checkout materializes it with CRLF line
ends as SHA-256 `5f6892eee612ded70df23c88d51813145572495395e807c000851d132f128853`). The corpus keeps the unpatched
script beside it as `.vbs.original` (blob SHA-256 `d0f6240e633654db55ba035e0e3fa310335a266ceb178dd898d2ffda092b800f`);
its `.vbs.patch` comments out only two lines that set the visibility of a `Trim` object (lines 347 and 360), nothing
the controller sees. The pinned `sverrewl/vpxtable_scripts` corpus at revision
`0c036bb61b4b4e8c778c37559f6795df8cd1521e` holds Kiwi's earlier `Gladiators (Premier 1993) v1.0.1.vbs` (SHA-256
`13b45d7e9a4ead26633cb0dd6ed1adf2e25fdcb0785360b3bcdddc7db5ba45e7`), the same author's script, so it corroborates rather
than independently confirms. Line numbers are the v1.1.1 file's. Leading whitespace is dropped and a run of lines is
joined with " · ".

## Controller

| Line | Text |
| --- | --- |
| 53 | `Const cGameName = "gladiatr"` |
| 193 | `LoadVPM "01560000", "gts3.VBS", 3.26` |
| 200 | `Const UseSolenoids = 2` |
| 232-233 | `.HandleMechanics = 0` · `.HandleKeyboard = 0` |
| 255 | `vpmNudge.TiltSwitch = 151` |

## Ball stacks, drop bank and ramp motor (lines 260-324)

| Line | Text |
| --- | --- |
| 260-266 | `Set bsTrough = New cvpmBallStack` · `.InitSw 23, 0, 33, 0, 0, 0, 0, 0` · `.InitKick BallRelease, 67, 5` · `.Balls = 4` |
| 269-272 | `' Top Eject Hole` · `Set bsTP = New cvpmBallStack` · `.InitSaucer sw21, 21, 150, 20` |
| 279-282 | `' Left Eject Hole` · `Set bsLP = New cvpmBallStack` · `.InitSaucer sw31, 31, 105, 14` |
| 289-292 | `' Center Eject Hole (VUK)` · `Set bsCP = New cvpmBallStack` · `.InitSaucer sw22, 22, 0, 38` |
| 297-300 | `' Right Eject Hole` · `Set bsRP = New cvpmBallStack` · `.InitSaucer sw32, 32, 182, 24` |
| 307-310 | `' Drop targets` · `set dtBank = new cvpmdroptarget` · `.initdrop array(sw15, sw25, sw35), array(15, 25, 35)` |
| 313-324 | `' RMotor mech` · `Set mRMotor = New cvpmMech` · `.MType = vpmMechOneSol + vpmMechReverse + vpmMechNonLinear` · `.Sol1 = 23` · `.Length = 34 * Moltiplicatore` · `.Steps = 136` · `.Acc = 10` · `.Ret = 1` · `.AddSw 30, 0, 0` · `.Callback = GetRef("UpdateRMotor")` · `.Start` |
| 531-540 | `Sub UpdateRMotor(aNewPos, aSpeed, aLastPos)` · `RampDir = aNewPos / 4` · `RMotor.RotY = RampDir - 4` · `MotRamp(aLastPos\4).Collidable = False` · `MotRamp(aNewPos\4).Collidable = True` · (motor sound while `aSpeed > 0`) |

## Keys (lines 470-524)

| Line | Text |
| --- | --- |
| 471-472 | `If KeyCode = LeftFlipperKey Then Controller.Switch(82) = 1:BumpersDisable` · `If KeyCode = RightFlipperKey Then Controller.Switch(83) = 1:BumpersDisable` |
| 481 | `If vpmKeyDown(keycode) Then Exit Sub` |
| 498-499 | `If KeyCode = LeftFlipperKey Then Controller.Switch(82) = 0:BumpersDisable` · `If KeyCode = RightFlipperKey Then Controller.Switch(83) = 0:BumpersDisable` |
| 502 | `If vpmKeyUp(keycode) Then Exit Sub` |
| 515-524 | `Sub BumpersDisable` · `If Controller.Switch(82) And Controller.Switch(83) Then` · `Bumper1.HasHitEvent=0` · `Bumper2.HasHitEvent=0` · `Bumper3.HasHitEvent=0` · `Else` · (the three set back to 1) |

## Switch writers (lines 584-685)

| Line | Text |
| --- | --- |
| 584 | `Sub LeftSlingshot_Slingshot:vpmTimer.PulseSw 13:...` |
| 602 | `Sub RightSlingshot_Slingshot:vpmTimer.PulseSw 14:...` |
| 621-623 | `Sub Bumper1_Hit:vpmTimer.PulseSw 10:...` · `Sub Bumper2_Hit:vpmTimer.PulseSw 11:...` · `Sub Bumper3_Hit:vpmTimer.PulseSw 12:...` |
| 626 | `Sub sw20_Spin:vpmTimer.PulseSw 20:...` |
| 629-630 | `Sub Drain_Hit` · `bsTrough.AddBall Me` |
| 633-636 | `Sub sw21_Hit:...bsTP.AddBall 0:End Sub` · `Sub sw31_Hit:...bsLP.AddBall 0:End Sub` · `Sub sw22_Hit:...bsCP.AddBall 0:sw22Wire.RotX = 0:End Sub 'VUK` · `Sub sw32_Hit:...bsRP.AddBall 0:sw32Wire.RotX = 0:End Sub` |
| 639-640 | `Sub sw24_Hit:Controller.Switch(24) = 1:...` · `Sub sw24_UnHit:Controller.Switch(24) = 0:...` |
| 641-644 | `Sub sw80_Hit:Controller.Switch(80) = 1:End Sub` · `Sub sw80_UnHit:Controller.Switch(80) = 0:End Sub` · the same for `sw81` and 81 |
| 645-656 | `Sub sw94_Hit:Controller.Switch(94) = 1:...` and `_UnHit` 0, and the same pairs for `sw100` (100), `sw92` (92), `sw102` (102), `sw93` (93) and `sw103` (103) |
| 659-661 | `Sub Gate90_Hit():vpmTimer.PulseSw 90:End Sub` · `'Sub sw90_Hit():Controller.Switch(90) = 1:End Sub` · `'Sub sw90_UnHit():Controller.Switch(90) = 0:End Sub` |
| 662-665 | `Sub sw91_Hit():Controller.Switch(91) = 1:End Sub` · `_UnHit` 0 · the same for `sw101` and 101 |
| 668, 673, 678 | `Sub sw15_Hit:PlaySoundAtVol SoundFX("DROPTARG",...` and the same for `sw25` and `sw35` (sound only; `dtBank` writes the switches) |
| 684-685 | `Sub sw95_Hit:vpmTimer.PulseSw 95:...` · `Sub sw104_Hit:vpmTimer.PulseSw 104:...` |

## Solenoid callbacks (lines 706-871)

No `SolCallback` is assigned for 1-5 or 27, and `SolCallback(23)` is commented out; `mRMotor` reads solenoid 23.

| Line | Text |
| --- | --- |
| 706-707 | `SolCallback(6)  = "SolBallReleaseLP"` · `SolCallback(7)  = "SolBallReleaseTP"` |
| 708-709 | `SolCallback(8)  = "SetLamp 188,"` · `SolCallback(9)  = "SetLamp 189,"` |
| 710 | `SolCallback(10) = "dtcbank"` |
| 711-712 | `SolCallback(11) = "SolBallReleaseCP"` · `SolCallback(12) = "SolBallReleaseRP"` |
| 713 | `SolCallback(13) = "PlungerGate"` |
| 714-721 | `SolCallback(14) = "SetLamp 194,"` · `(15) "SetLamp 195,"` · `(16) "SetLamp 196,"` · `(17) "SetLamp 197,"` · `(18) "SetLamp 198,"` · `(19) "SetLamp 199,"` · `(20) "SetLamp 190,"` · `(21) "SetLamp 191,"` |
| 722-724 | `SolCallback(22) = "SetLamp 182,"` · `'SolCallback(23) = "RampMotorRelay"` · `SolCallback(24) = "SetLamp 184,"` |
| 725-726 | `SolCallback(25) = "MShaker"` · `SolCallback(26) = "GIBackBox"` |
| 727-728 | `SolCallback(28) = "bsTroughSolOut" '"bsTrough.SolOut"` · `SolCallback(29) = "bsTrough.SolIn"` |
| 729-731 | `SolCallback(30) = "KnockerSound"` · `SolCallback(31) = "GIRelay"` · `Solcallback(32) = "SolRun"` |
| 740-750 | `Sub PlungerGate(Enabled)` · `If Enabled Then` · `Perno.IsDropped=1` · `ServoPerno.Open=1` · ... · `Else` · `Perno.TimerEnabled=1` (the `Perno_Timer` raises the post again) |
| 757-759 | `Sub dtcbank(Enabled)` · `If Enabled Then` · `dtbank.DropSol_On` |
| 772-776 | `Sub SolBallReleaseLP(Enabled)` · `If Enabled Then` · `bsLP.ExitSol_On` · `EjectTimer.Enabled=1` · `EjectArm.RotY = -20` |
| 825-826 | `Sub MShaker(Enabled)` · `PlaySoundAtVol SoundFX("ShakerSoftPulsing",DOFShaker), l50, ShaVol` (a sound only) |
| 839-844 | `Sub GIRelay(Enabled)` · `GIoffon = ABS(ABS(Enabled) -1)` · `SetLamp 150, GIoffon` · `SetLamp 151, GIoffon` |
| 846-849 | `Sub GIBackBox(Enabled)` · `GIBBoffon = ABS(ABS(Enabled) -1)` · `SetLamp 156, GIBBoffon` |
| 852-853 | `Sub SolRun(Enabled)` · `vpmNudge.SolGameOn Enabled` |
| 870-871 | `SolCallback(sLRFlipper) = "SolRFlipper"` · `SolCallback(sLLFlipper) = "SolLFlipper"` |
| 875 | (in `SolLFlipper`) `...LeftFlipper.RotateToEnd:LeftFlipper1.RotateToEnd` |
| 886 | (in `SolRFlipper`) `...RightFlipper.RotateToEnd:RightFlipper1.RotateToEnd` |

## Lamps (lines 940-1162)

`LampTimer_Timer` (lines 928-938) copies `Controller.ChangedLamps` into `LampState` and calls `UpdateLamps`.

| Lines | Lamp numbers and objects |
| --- | --- |
| 941-1029 | `NFadeL`/`NFadeLm` with object `l<n>` for every lamp 0, 2-7, 10-17, 20-27, 30-37, 40-47, 50-57, 60-67, 70-77, 81-83, 91-93 and 100-107; 2-7 and 12-17 also drive `LEDR<n>` through `FlashDL` |
| 1031-1048 | `'Flashers` · `Flashm 84, f84` · `FlashDL 84, 2, LEDR84` and the same for 85, 86, 87, 94, 95, 96 and 97 |
| 1050-1095 | `NFadeLm 150, Bulb1` ... (playfield G.I. bulbs and bumper G.I., lamp 150 written by `GIRelay`) |
| 1097-1119 | `Flashm 151, fgit1` ... (G.I. flashers, lamp 151 written by `GIRelay`) |
| 1121-1141 | `NFadeLm 194, fl14` ... flasher objects for 194-199 (solenoids 14-19) and `Flash 190, f20` · `Flash 191, f21` (solenoids 20, 21) |
| 1143 | `' BackBox` |
| 1145-1150 | `Flash 112, l112` ... `Flash 117, l117` |
| 1152-1159 | `Flashm 182, l182` · `Flash 182, l182a` · and the same pairs for 184, 188 and 189 (solenoids 22, 24, 8 and 9) |
| 1161-1204 | `Flashm 156, lb1` ... `Flash 156, lb44` (backbox G.I., lamp 156 written by `GIBackBox`) |

No `UpdateLamps` line names lamp 1, 80, 90, 110 or 111.

## Backbox object height (lines 372-435)

| Line | Text |
| --- | --- |
| 372-374 | `' Backbox Flashers Y Position` · `Const Fpy = 16.2` |
| 376-390 | `l112.y = Fpy` ... `l117.y = Fpy` · `l184.y = Fpy` · `l184a.y = Fpy` · `l182.y = Fpy` · `l182a.y = Fpy` · `l188.y = Fpy` · `l188a.y = Fpy` · `l189.y = Fpy` · `l189a.y = Fpy` |
| 392-435 | `lb1.y = Fpy` ... `lb44.y = Fpy` |
