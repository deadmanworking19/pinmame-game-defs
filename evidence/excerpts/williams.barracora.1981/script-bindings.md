# Williams Barracora (game 510) - VPX script bindings

Sources:

- `Barracora (Williams 1981) w VR Room v2.1.3.vbs` in `sverrewl/vpxtable_scripts` at `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `89135c332343e5d7bd8a31498e18268f1afa94a195034a55dd2d7bfc9eab05eb`, 4478 lines. Header: `Version 2.0 by UnclePaulie 2022`, `2.1 version has updated playfield and plastics done by redbone.`
- `Barracora (Williams 1981) mod v1.3.vbs` in the same corpus and revision, SHA-256 `ca7e4764770a67c57b0e4088ad03c14ceb70b7306690cc631b7707bed4f9bc77`. Header: `Barracora - Williams 1981 by Dids666`, `Ver 1.1`, `Thalamus 2018-07-19`.
- The script embedded in the retained table `Barracora (1981).vpx` (table SHA-256 `e40287ad8a3d02feeae7b2ff56a902cb34e5f5b7ae8706e1097ddcba9fc54157`, author Dids666, Jan 2018), extracted by vpxtool to `script.vbs`, SHA-256 `fb33726ee06aab0a5d4edde731e569c3178f558d95fa65c151b78da445d538bf`, ASCII with CRLF line ends.

Method: source text read directly; quoted lines are copied with their original spacing collapsed. Line numbers are the file's own.

## VR Room v2.1.3 (UnclePaulie)

- Line 107: `Const cGameName   = "barra_l1"  'ROM name`; line 129: `LoadVPM "00990300", "S7.VBS", 3.36`.
- Lines 138-156, solenoid callbacks:

| Line | Binding | Comment as printed |
|---|---|---|
| 138 | `SolCallback(1) = "SolDTLeftB"` | Drop Target Left B |
| 139 | `SolCallback(2) = "SolDTLeftA"` | Drop Target Left A |
| 140 | `SolCallback(3) = "SolDTLeftRR"` | Drop Target Left RR |
| 141 | `SolCallback(4) = "SolDTRightA"` | Drop Target Right A |
| 142 | `SolCallback(5) = "SolDTRightC"` | Drop Target Right C |
| 143 | `SolCallback(6) = "SolDTRightO"` | Drop Target Right O |
| 144 | `SolCallback(7) = "SolDTRightR"` | Drop Target Right R |
| 145 | `SolCallback(8) = "SolDTRightAA"` | Drop Target Right A - 2nd one |
| 146 | `SolCallback(9) = "SolDTLeftReset"` | Drop Target Left - B-A-RR Release |
| 147 | `SolCallback(10) = "SolDTRightReset"` | Drop Target Right - A-C-O-R-A Release |
| 148 | `SolCallback(11) = "SolOuthole"` | Outhole |
| 149 | `SolCallback(12) = "SolBallRelease"` | Ball Release |
| 150 | `SolCallback(13) = "SolTopEjectHole"` | Top Eject Hole |
| 151 | `SolCallback(14) = "SolLoweEjectHole"` | Lower Eject Hole |
| 152 | `SolCallback(15) = "Bell"` | Bell |
| 153 | `SolCallback(17) = "UpperKickerGate"` | Opens the Upper Kicker Gate |
| 155-156 | `SolCallback(sllflipper)="SolLFlipper"`, `SolCallback(slrflipper)="SolRFlipper"` | |

  There is no callback for 16 (coin lockout) or for 18-22; the bumpers and kickers are not driven from the ROM's special solenoids.
- Lines 599-660: each of `SolDTLeftB` ... `SolDTRightAA` does `DTRaise 41` ... `DTRaise 48` when enabled (1 raises target 41, 2 raises 42, 3 raises 43, 4 raises 44 ... 8 raises 48).
- Lines 663-690: `SolDTLeftReset` does `DTDrop 41`, `DTDrop 42`, `DTDrop 43`; `SolDTRightReset` does `DTDrop 44` ... `DTDrop 48`. That is, 9 and 10 drop a whole bank and 1-8 raise one target each.
- Lines 775-786: `SolOuthole` does `Drain.kick 60, 15`; `SolBallRelease` does `BallRelease.kick 60, 12`. Lines 788-790: `Drain_Hit` delays `Controller.Switch(12) = 1` by 200 ms.
- Lines 750-755: ball-ramp objects `BallRelease`, `SlotCenter` and `SlotLeft` set switches 15, 14 and 13. Lines 226-235 create three balls in them and set `Controller.Switch(12) = 0`, `Controller.Switch(13) = 1`, `Controller.Switch(14) = 1`, `Controller.Switch(15) = 1`.
- Lines 803-826: `SolTopEjectHole` kicks `sw10` and clears switch 10; `SolLoweEjectHole` kicks `sw11` and clears switch 11.
- Lines 829-835:

```
Sub UpperKickerGate(enabled)
  If enabled Then
    Gate1.open = True
  Else
    Gate1.open = False
  End If
End Sub
```

- Lines 842-850: `Bell` plays a bell sound while enabled.
- Lines 509-522: `Bumper1_Hit` pulses 20, `Bumper2_Hit` 21, `Bumper3_Hit` 22. Lines 707 and 726: `RightSlingShot_Slingshot` pulses 30, `LeftSlingShot_Slingshot` pulses 29.
- Lines 694-697: `RubberBand014_Hit` pulses 37, `RubberBand012_Hit` 38, `RubberBand010_Hit` 39, `RubberBand006_Hit` 40.
- Line 221: `vpmNudge.TiltSwitch = 1`.
- Lines 312 and 318 (key down) and 360 and 366 (key up): `controller.switch(34)` follows the left flipper key and `controller.switch(35)` the right flipper key.

## mod v1.3 (Dids666 lineage)

- Line 48 `Const cGameName = "barra_l1"`; line 55 `vpmMapLights AllLights`; line 87 `vpmNudge.TiltSwitch = 1`.
- Line 93 `bsTrough.initsw 0,15,14,13,0,0,0,0`; lines 99 and 105 `bsUpperEject.InitSaucer sw10, 10,65,8` and `bsLowerEject.InitSaucer sw11, 11,169,5`; lines 114 and 118 `dtbank1.InitDrop Array(sw41, sw42, sw43), Array(41, 42, 43)` and `dtbank2.InitDrop Array(sw44, sw45, sw46, sw47, sw48), Array(44, 45, 46, 47, 48)`.
- Lines 198-223: 1-8 `dtbank1.SolUnhit 1,` ... `dtbank2.SolUnhit 5,`; 9 and 10 `dtbank1.SolDropDown` and `dtbank2.SolDropDown`; `sBallRel` (11) `sBallRelease`; `sBallRampThrow` (12) `sBallRampThrower`; 13 and 14 `bsUpperEject.solout` and `bsLowerEject.solout`; 15 a bell sound; `''SolCallback(sCoin)= - Not Used`; 17 `UpperKickerGate`; 18-22 sounds only.
- Line 242: `Sub UpperKickerGate(enabled): gate1.open=True: End Sub`. The handler opens the gate on every call and never closes it; a separate `sw16_Hit` (line 355) closes it when a ball reaches the shooter lane.
- Lines 142-143 and 153-154 write `controller.switch(35)` and `controller.switch(34)` from the right and left flipper keys.
- `Sub sw18_Hit` is defined three times (lines 323, 335 and 338) and `Sub sw16_Hit` twice (lines 326 and 355).

## Retained table's embedded script (Dids666 v1.1)

The embedded script has the same bindings as mod v1.3 at nearby line numbers: `vpmMapLights AllLights` (53), `bsTrough.initsw 0,15,14,13,0,0,0,0` (91), the two `InitSaucer` calls (97, 103), both `InitDrop` banks (112, 116), the solenoid constants and callbacks (166-221), `Sub UpperKickerGate(enabled): gate1.open=True: End Sub` (240), `Drain_Hit` setting switch 12 (257-262), the flipper-key writes to 34 and 35 (140-152), `Sub sw18_Hit` three times (321, 333, 336), `sw16_Hit` closing `gate1` (353-355), bumpers `sw20`-`sw22` pulsing 20-22 (360-384), `sw37_Hit` ... `sw40_Hit` pulsing 37-40 (409-412) and the slingshots pulsing 29 and 30 (420-448). It also has an invisible `Trigger` named `sw12` with a `sw12_Hit` handler (339), while `Drain_Hit` destroys the ball at the bottom-centre `Drain` kicker.

## Notes

- PinMAME's `FLIP_SWNO(34,35)` copies the left and right cabinet flipper buttons into 34 and 35 on every update, so the scripts' direct writes to 34 and 35 do nothing; the tables' lane change works because `vpmKeyDown` also writes the flipper-button inputs. The harness run in this record shows a one-shot write to 34 or 35 being overwritten.
- In the scripts, `BallRelease` is the ball ramp thrower's kicker (12), while the factory name `Ball Release` belongs to 11, the outhole kicker.
- Only the VR Room script switches the gate both ways. The Dids666 lineage's handler cannot close it.
