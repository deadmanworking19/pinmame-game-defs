# Known-working script — controller bindings

`reviewed: true`; copied by the curator from the pinned corpus file on 2026-10-16
`source: sverrewl/vpxtable_scripts at 0c036bb61b4b4e8c778c37559f6795df8cd1521e, "Sorcerer (Williams 1985) v4.0.4.vbs", 181,482 bytes, SHA-256 2222f6be1fcd5598fd4f925e99f936bdcb5f53704420e55d7731048a1a93e377`

The header credits the VPX version 4.0 to UnclePaulie, from the 2018 original by JPSalas. Lines are quoted
verbatim with their line numbers; whole-line comments are kept only where they label a binding.

## Controller set-up

```vb
143: Const cGameName = "sorcr_l2"
145: Const UseSolenoids = 2
147: Const UseLamps = 1
148: Const UseGI = 0
152: LoadVPM "01550000", "S11.VBS", 3.26
265:   vpmMapLights AllLamps     'Make a collection called "AllLamps" and put all the light objects in it.
270:     vpmNudge.TiltSwitch = 1
280:   Controller.Switch(28) = 0
281:   Controller.Switch(29) = 1
282:   Controller.Switch(30) = 1
```

Line 142 is the commented alternative `'Const cGameName = "sorcr_l1"`. Lamps are bound by `vpmMapLights`, which
drives each light in the `AllLamps` collection from its own `TimerInterval`.

## Solenoid callbacks

```vb
790: SolCallback(1) = "SolOuthole"     ' Outhole
791: SolCallback(2) = "SolBallRelease"   ' Ball Release
792: SolCallback(3) = "SolMBEject"     ' Multi-Ball Eject
793: SolCallback(4) = "SolDtBank"    ' Three Bank Reset
794: SolCallback(6) = "Flash6"         ' Drop Target Flasher
795: SolCallback(7) = "Flash7"         ' Center Target Bank Flashers
796: SolCallback(8) = "sol8subroutine" ' Back Panel Eye Flashers, and Backbox Flasher
797: SolCallback(11) = "SolGi"           ' General Illumination
798: SolCallback(14) = "SolKnocker"    ' Knocker
799: SolCallback(15) = "SolBell"     ' Sorcerer Bell
808: SolCallback(sLRFlipper) = "SolRFlipper"
809: SolCallback(sLLFlipper) = "SolLFlipper"
810: SolCallback(sULFlipper) = "SolULFlipper"
812: SolCallback(5) = "Sol5"     ' Demon Backdrop Flasher
813: SolCallback(19)  = "Sol19"  ' Backbox Flasher
```

Lines 800-806 are commented out: `'SolCallback(16)`, `'SolCallback(17) = "" ' Left Sling`, `(18) Right Sling`,
`(19) Left Jet Bumper`, `(20) Bottom Jet Bumper`, `(21) Right Jet Bumper`, `'SolCallback(23) = "vpmNudge.SolGameOn"`.
The slings and bumpers are fired by the table's own physics events. `SolGi` (line 4497) turns the GI off when
its argument is true and on when false. `SolKnocker` (1354) calls `KnockerSolenoid`; `SolBell` (1360) calls
`KnockerBell`. `Sol19` (line 838) only switches a backbox flasher object `f19flash`; solenoid 19 is the left
jet bumper, so this decorates the VR backbox and is not a binding of the machine's output.

## Switch writes

```vb
744:     Controller.Switch(44) = 1        ' in Table1_KeyDown, If keycode = RightFlipperKey
774:     Controller.Switch(44) = 0        ' in Table1_KeyUp, If keycode = RightFlipperKey
872: Sub BallRelease_Hit   : Controller.Switch(30) = 1 : UpdateTrough : End Sub
874: Sub Slot1_Hit       : Controller.Switch(29) = 1 : UpdateTrough : End Sub
906:   Controller.Switch(28) = 1          ' in Drain_Hit
1007:   vpmTimer.PulseSw 33               ' in RightSlingShot_Slingshot
1027:   vpmTimer.PulseSw 32               ' in LeftSlingShot_Slingshot
1186: Sub Phys_RB_Sensor_sw39_Hit: vpmTimer.PulseSw 39: End Sub
1187: Sub Phys_RB_Sensor_sw40_Hit: vpmTimer.PulseSw 40: End Sub
1188: Sub Phys_RB_Sensor_sw42_Hit: vpmTimer.PulseSw 42: End Sub
1189: Sub Phys_RB_Sensor_sw43_Hit: vpmTimer.PulseSw 43: End Sub
1197:   vpmTimer.PulseSw 21               ' in Bumper1_Hit
1202:   vpmTimer.PulseSw 23               ' in Bumper2_Hit
1207:   vpmTimer.PulseSw 22               ' in Bumper3_Hit
1218:   controller.Switch(37)=1           ' in sw37_Hit; SolMBEject (1221) clears it
1235-1252: sw17-sw20, sw24-sw27 and sw38 _Hit/_UnHit set and clear Controller.Switch(n)
1254-1260: sw31_Hit/_UnHit set and clear Controller.Switch(31)
1286-1288: Sw34_Hit, Sw35_Hit, Sw36_Hit call DTHit 34, 35, 36
1312-1317: sw10_Hit to sw15_Hit call STHit 10 to 15
1325: vpmTimer.PulseSw 9               ' in sw9_Spin
1330: vpmTimer.PulseSw 16              ' in sw16_Spin
```

Unused by the script: 41 and 46-64 (no handler), 45 (the playfield tilt is not modelled; vpmNudge uses 1).
The right-flipper key writes matrix switch 44 directly; PinMAME overwrites 44 from flipper-column 82 on every
update (`FLIP_SWNO(0,44)`), and S11.VBS's key handler writes 82 from the same key, so the direct write has no
lasting effect.
