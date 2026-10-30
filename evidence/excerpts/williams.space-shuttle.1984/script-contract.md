# Known-working script — controller bindings

`reviewed: true`; copied by the curator from the pinned corpus file on 2026-10-30
`source: jsm174/vpx-standalone-scripts at 15d112648a1b94b9f59eb8b3c335d57283653c50, "Space Shuttle (Williams 1984)2.0/Space Shuttle (Williams 1984).vbs", 155,947 bytes, SHA-256 91e15d488be3f71c40324abbad2612c0b1dbe5f0f9b0813a292b8db1ea3e2ab2`

The header credits the VPX table to bord, the VR rooms to Rawd, UnclePaulie and Sixtoe, and physics, sounds and
scripting assistance to rothbauerw. Lines are quoted verbatim with their line numbers (trailing whitespace trimmed); trailing comments are kept
because they label the bindings. The retained table `Space Shuttle (Williams 1984).vpx` embeds the same script
with identical bindings, and identical line numbers up to line 583; it differs only in how its drop-target helper stores state (an array
instead of a `DropTarget` class).

## Controller set-up

```vb
60: LoadVPM "01560000", "S11.vbs", 3.36
66: Const cGameName = "sshtl_l7"
68: Const UseSolenoids = 2
69: Const UseLamps = 0
70: Const UseGI = 1
111: 	vpmNudge.TiltSwitch=1
120: 	Controller.Switch(10) = 1
121: 	Controller.Switch(11) = 1
122: 	Controller.Switch(12) = 1
```

Lamps are bound through a `Lampz` fader (`Lampz.MassAssign(n) = <light>`, lines 2352-2553): 1-6 to backglass
objects, 7 to `CPFlash1`, `CPFlash2` and the centre-post light `lp2`, 8-37 and 41-64 to the playfield lights `l<n>`
and their `l<n>B` bloom doubles (15 also to `l15C`/`l15D` and 41 to `l41C`/`l41D`, the second socket of each),
38-40 to backglass objects. Line 2553 `Lampz.MassAssign(103) = BGFL40a` makes the `SetLamp 103` of solenoid 14 light a backglass object.

## Solenoid callbacks

```vb
208: SolCallback(1) = "SolOuthole"							'1 - Outhole
209: SolCallback(2) = "ReleaseBall"							'2 - Ball Release
210: SolCallback(3) = "SolLKicker"							'3 - Left Kicker Hole
211: SolCallback(4) = "SolRKicker"							'4 - Right Kicker Hole
212: SolCallback(5) = "CenterDropTarget"						'5 - "T" Drop Target
213: SolCallback(6) = "ThreeBankDrop"						'6 - 3-bank Drop Targets
214: SolCallback(7) = "PostUp"								'7 - Center Post Up
215: SolCallback(8) = "PostDown"								'8 - Center Post Down
216: SolCallback(9) = "Flash9"								'9 - Playfield Space Flasher
217: SolCallback(10) = "Flash10"								'10 - Playfield Shuttle Flasher
218: SolCallback(11) = "PFGI"								'11 - GI Relaly
219: SolCallback(13) = "Diverter"							'13 - Outlane Gate
220: SolCallback(14) = "SetLamp 103,"						'14 - Backglass Rocket Plume Flasher
221: solcallback(15) = "SolKnocker" 							'15 - Bell
223: SolCallback(sLRFlipper) = "SolRFlipper"
224: SolCallback(sLLFlipper) = "SolLFlipper"
```

No callback is bound to 12, 16, 17-22. `PFGI` (line 2249) treats an enabled 11 as GI off (`' GI state inverted,
enabled = OFF`). `Diverter` (389-397) rotates the `bottomgate` flipper object to its end while 13 is enabled and
back to its start when released. `SolKnocker` (404-408) is commented `'Modified to play bell instead of knocker`.

## Ball routing and switch handlers

```vb
230: Sub Slot3_Hit():Controller.Switch(10) = 1:UpdateTrough:End Sub
232: Sub Slot2_Hit():Controller.Switch(11) = 1:UpdateTrough:End Sub
234: Sub Slot1_Hit():Controller.Switch(12) = 1:UpdateTrough:End Sub
252: Sub Drain_Hit()
255: 	Controller.Switch(9) = 1
262: Sub SolOuthole(enabled)
264: 		Drain.kick 60,20
269: Sub ReleaseBall(enabled)
272: 		Slot1.kick 60, 7
285: 		sw16.kick 183 + Rnd*4, 16 + Rnd*4
289: 		Controller.Switch(16) = 0
294: 	Controller.Switch(16) = 1
306: 		sw24.kick 170 + Rnd*4, 16 + Rnd*4
310: 		Controller.Switch(24) = 0
315: 	Controller.Switch(24) = 1
326: 		DTRaise 20
333: 		DTRaise 33
334: 		DTRaise 34
335: 		DTRaise 35
414: Sub sw25_hit
415: 	vpmTimer.PulseSw(25)
429: Sub sw26_hit
430: 	vpmTimer.PulseSw(26)
444: Sub sw27_hit
445: 	vpmTimer.PulseSw(27)
496: Sub RightSlingShot_Slingshot
497: 	vpmTimer.PulseSw 40
514: Sub LeftSlingShot_Slingshot
515: 	vpmTimer.PulseSw 39
557: Sub sw13_Hit:vpmTimer.PulseSw 13:End Sub
558: Sub sw14_Hit:vpmTimer.PulseSw 14:End Sub
559: Sub sw15_Hit:vpmTimer.PulseSw 15:End Sub
560: Sub sw28_Hit:vpmTimer.PulseSw 28:End Sub
561: Sub sw29_Hit:vpmTimer.PulseSw 29:End Sub
562: Sub sw30_Hit:vpmTimer.PulseSw 30:End Sub
563: Sub sw31_Hit:vpmTimer.PulseSw 31:End Sub
564: Sub sw36_Hit:vpmTimer.PulseSw 36:End Sub
567: Sub sw37_Spin():VPMTimer.PulseSw 37:SoundSpinner sw37:End Sub
570: Sub sw32_Hit : vpmTimer.PulseSw(32): End Sub
571: Sub sw45_Hit : vpmTimer.PulseSw(45) : End Sub
574: Sub sw42_Hit:vpmTimer.PulseSw 42:End Sub
575: Sub sw43_Hit:vpmTimer.PulseSw 43:End Sub
576: Sub sw44_Hit:vpmTimer.PulseSw 44:End Sub
577: Sub sw46_Hit:vpmTimer.PulseSw 46:End Sub
578: Sub sw47_Hit:vpmTimer.PulseSw 47:End Sub
579: Sub sw48_Hit:vpmTimer.PulseSw 48:End Sub
```

The drop targets 20 and 33-35 and the standups 17-19, 21-23 and 38 report through the script's drop-target and
standup helpers (`DT20`, `DT33`-`DT35` and the `tsw` hit targets), which call `vpmTimer.PulseSw` or set the
latched drop-target switch from the object's own number. The jet bumpers fire from the VPX bumper objects
themselves; the script binds no callback to 19-21, so it never acts on PinMAME's special solenoids.
