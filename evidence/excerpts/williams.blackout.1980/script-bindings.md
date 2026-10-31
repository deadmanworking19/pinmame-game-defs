# Williams Blackout (game 495) - VPX script bindings

Sources:

- The script embedded in the retained table `Blackout (Williams 1980)-S34 v1.1.vpx` (table SHA-256 `cc51bd61f64e8a614eb059c3f6cac183ab93d9e18d7088deb5c950f13534c4e3`), extracted by vpxtool to `script.vbs`, SHA-256 `4fe2fef60af899fc019e7a4adceab63c067e1e668448b3f704787cbbb08825b9`, ASCII with CRLF line ends, 684 lines.
- `Blackout (Williams 1980) Mod - S34 v1.1.vbs` in `sverrewl/vpxtable_scripts` at `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `1853655480d0e3f423dd9a8ad384ea99d47c5687daf4c704c0d7badb01f24b8b`, 782 lines. Header: `' Thalamus 2018-07-24`, `' Changed UseSolenoids=1 to 2`.
- `Blackout (Williams 1980) v1.0.1 - SBR34.vbs` in the same corpus and revision, SHA-256 `eafdb30a3009065c143e3a385141cef1c50a2a9b66ee08d93a4596dc660a5ab6`, 3765 lines. It names no author; its option comments credit `Sixtoe's original walls and floor` (line 37) and other contributors' routines.

Method: source text read directly; quoted lines are copied with their original spacing collapsed. Line numbers are the file's own.

## Embedded script (S34 v1.1)

- Line 6: `Const BlackoutMode = 0 '0=Authentic mode, 1=Fantasy mode (GI remains off until ball drain)`.
- Line 14: `Const cGameName="blkou_l1",UseSolenoids=1,UseLamps=1,UseGI=0,...`; line 16: `LoadVPM "01320000", "S6.VBS", 3.21`.
- Lines 35-47, solenoid callbacks:

| Line | Binding |
|---|---|
| 35 | `SolCallback(1) = "bsTrough.SolOut"` |
| 36 | `SolCallback(4) = "dtCDrop.SolDropUp"` |
| 37 | `SolCallback(5) = "dtTDrop.SolDropUp"` |
| 38 | `SolCallback(6) = "bsRightEject.SolOut"` |
| 39-43 | `' SolCallback(9) = "VpmSolSound""SolChime1"` ... `' SolCallback(13) = "VpmSolSound""SolChime5"`, commented out |
| 44 | `SolCallback(15) = "SolSpecial"` |
| 46-47 | `SolCallback(sLRFlipper) = "SolRFlipper"`, `SolCallback(sLLFlipper) = "SolLFlipper"` |

  There is no callback for 2, 3, 7, 8, 14 (knocker), 16 (coin lockout), 17-22 or 23.
- Lines 70-81, `Sub SolSpecial(Enabled)`: when enabled, `For each xx in GI:xx.State = 0: Next` (GI off) and, with `BlackoutMode = 1`, `BlackoutFlag = 1`; otherwise `For each xx in GI:xx.State = 1: Next` (GI on). Solenoid 15 energized therefore means general illumination off.
- Lines 159-176: with `BlackoutMode = 1` only, `sw40_UnHit` turns the GI off again and `Drain_Hit` turns it back on. The default `0` leaves the GI to solenoid 15 alone.
- Lines 106-107: `Controller.SolMask(0)=0` and a 2000 ms timer that restores `&Hffffffff`, `'ignore all solenoids ... after 2 seconds`.
- Line 114: `vpmNudge.TiltSwitch = 1`.
- Lines 118-123: `bsTrough.Initsw 0,9,0,0,0,0,0,0`, `bsTrough.InitKick BallRelease,120,3`, `bsTrough.Balls = 1`: a one-ball trough whose only switch is 9, emptied by solenoid 1.
- Line 126: `bsRightEject.InitSaucer sw40, 40, 220, 8`, emptied by solenoid 6.
- Lines 131-139: `dtCDrop.InitDrop Array(sw25,sw26,sw27),Array(25,26,27)` with `dtCDrop.AllDownSw = 28`, and `dtTDrop.InitDrop Array(sw33,sw34,sw35),Array(33,34,35)` with `dtTDrop.AllDownSw = 36`. Solenoid 4 resets the centre bank and 5 the top bank.
- Line 167: `Sub Drain_Hit` adds the ball to `bsTrough`.
- Lines 179-180: `sw19_Slingshot` and `sw38_Slingshot` pulse 19 and 38 (comment `'scoring rubbers`).
- Lines 183-185: `Bumper1_Hit` pulses 22, `Bumper2_Hit` 21, `Bumper3_Hit` 23.
- Lines 188-201: rollover triggers `sw10`, `sw45`, `sw42`, `sw41`, `sw29`, `sw30`, `sw31` hold their switches while the ball is over them.
- Lines 204-209: `sw11_Hit` ... `sw15_Hit` and `sw20_Hit` pulse 11-15 and 20 (`'Stand Up targets`).
- Lines 212-214: `Spinner1_Spin` pulses 37, `Spinner2_Spin` 39, `Spinner3_Spin` 18.
- Lines 384-385 and 402-403: `RightSlingShot_Slingshot` pulses 43 and `LeftSlingShot_Slingshot` pulses 44.
- Lines 231-294: `Set Lights(n)=ln` for 1-10, 12-53, 55 and 57-64; line 285 is commented out, `'Set Lights(54)=l54 'Match`, and there is no line for 11 or 56. Lines 280-294 are under `'BackGlass`, with comments `' Ball In Play` (55), `'TILT` (61), `'Game Over` (62), `'Shoot Again` (63) and `'High Score` (64).
- No line writes switch 46, and none writes 28 or 36 directly; the drop-target helpers set 28 and 36.

## Mod - S34 v1.1 (corpus)

Apart from the Thalamus header, the volume constants, positional sound calls and line spacing, it has the embedded script's bindings, with `UseSolenoids=2` at line 43. Its callbacks are at lines 64-76 and `Sub SolSpecial` follows the same GI logic.

## v1.0.1 - SBR34 (corpus)

- Line 9: `Const cGameName="blkou_l1",UseSolenoids=2,UseLamps=0,UseGI=1,...`; line 11: `LoadVPM "01320000", "S6.vbs", 3.21`.
- Line 103: `vpmNudge.TiltSwitch=1`. Lines 107-111: `bsTrough.Initsw 0,9,0,0,0,0,0,0`, `bsTrough.Balls = 1`. Line 114: `bsRKick.InitSaucer sw40,40, 200, 24`.
- Lines 290-298, solenoid callbacks:

| Line | Binding |
|---|---|
| 290 | `SolCallback(1) = "bsTrough.SolOut"` |
| 291 | `SolCallback(4) = "dropupcenter"` |
| 292 | `SolCallback(5) = "dropupleft"` |
| 293 | `SolCallback(6) = "SolRSaucer"` |
| 294 | `solcallback(14) = "SolKnocker"` |
| 295 | `SolCallback(15) = "PFGI"` |
| 297-298 | `SolCallback(sLRFlipper) = "SolRFlipper"`, `SolCallback(sLLFlipper) = "SolLFlipper"` |

- Lines 720-736: `dropupleft` raises targets 33, 34 and 35, and `dropupcenter` raises 25, 26 and 27.
- Lines 591-614, `Sub PFGI(Enabled)`: `If Enabled Then ' GI state inverted, enabled = OFF`. Both branches set every `GI` light to `state=1`; the enabled branch swaps the playfield primitives to `_gioff` images and sets its own fading lamps 111 and 112 to show the GI-off look, the other branch restores the `_gion` images.
- Lines 326 and 335: `SolRFlipper` writes `Controller.Switch(46)=1` when the right flipper solenoid turns on and `Controller.Switch(46)=0` when it turns off.
- Lines 1986-1998, `DTAnim_Timer`: sets `controller.Switch(28) = 1` while 25, 26 and 27 are all down and `controller.Switch(36) = 1` while 33, 34 and 35 are all down, and 0 otherwise.
- Bumper handlers `sw22_hit`, `sw21_hit`, `sw23_hit` (lines 775, 794, 813) pulse 22, 21 and 23; `sw19_Hit` and `sw38_Hit` (lines 864 and 868) pulse 19 and 38; `RightSlingShot_Slingshot` pulses 43 and `LeftSlingShot_Slingshot` pulses 44 (lines 877 and 897); the spinner handlers `sw18_Spin`, `sw37_Spin`, `sw39_Spin` (lines 769-771) pulse 18, 37 and 39; standup handlers `Tsw11_Hit` ... `Tsw15_Hit` and `Tsw20_Hit` (lines 739-749) pulse 11-15 and 20; rollover triggers `sw10`, `sw29`, `sw30`, `sw31`, `sw41`, `sw42`, `sw45` (lines 753-766) hold their switches.
- Lamps: `Lampz.MassAssign(n)= ln` for 1-10 and 12-49 (lines 1047-1200); lamp 54 is read directly (`Controller.Lamp(54)`, `' match`, lines 3611 and 3640). No line names lamp 11 or 56.

## Notes

- Both lineages agree on every solenoid, switch and lamp address they bind. Lamp 56 (`Credits (Playfield)` in the bulb list, `lamp-wiring.md`) is bound by neither.
- PinMAME's `FLIP_SWNO(0,46)` copies the right cabinet flipper button into 46 on every update, so SBR34's writes to 46 from the solenoid callback are rewritten to the button's state at the next update. They coincide with the button press anyway, because the right flipper solenoid follows the button. In this record's switch-test run a one-shot write to 46 reads back 0 at its snapshot, although Test 03 latched it and showed 46. Both lineages' lane change works because `vpmKeyDown` writes the flipper-button input.
- SBR34's own comment calls solenoid 15 `inverted`: energized means GI off. The embedded script handles it the same way without the comment.
- The standalone corpus `jsm174/vpx-standalone-scripts` at `15d112648a1b94b9f59eb8b3c335d57283653c50` carries a patched copy of SBR34 (`Blackout (Williams 1980) v1.0.1 - SBR34/Blackout (Williams 1980) v1.0.1 - SBR34.vbs`, checkout SHA-256 `9c2517baac96312b614ccc995f364527178b532d9cfe9db2cb64f3bfebf45939`). It is not cited separately.
