# Harlem Globetrotters On Tour - the pinned table script

Quoted from `Harlem_Globetrotters_1.2.0.vbs` in `sverrewl/vpxtable_scripts` at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e` (SHA-256 `0b0b6727dcf0ba223d0fc4c1a7ab64bfb48e041428bd524e5a9bdd5fdaa24e9d`, 554 lines). Line numbers are the file's own. Sound, animation and rail-hiding lines between the quoted blocks are omitted.

The retained table's embedded script (`script.vbs` in the extraction, SHA-256 `4452891ab2589728b21d1d2766ead76d56bfdb107038197a8da268a82ed4ffae`) is the same table before a later sound update: it lacks the update's header comments and volume constants, calls `PlaySound` where this script calls `PlaySoundAtVol`, and sets `UseSolenoids = 1` where this script sets `2`. Its switch writes, solenoid callbacks, ball stacks, drop target bank, diverter, lamp mapping, game name and option-switch form are identical to the lines quoted here.

Header and controller setup:

```
1: ' Harlem Globettroters on Tour - Bally 1979
2: ' VPX version by JPSalas 2009, version 1.0
3: ' Uses 7 digits ROM bootleg
4: ' You need both roms: hglbtrtr.zip and hglbtrtb.zip
5: ' Script based on Gaston's script
6: ' Dedicado a Jolo :)
7: ' DOF extension ny arngrim
51: LoadVPM "01550000", "Bally.vbs", 3.26
56: 'Const cGameName = "hglbtrtr" ' normal 6 digits rom
57: Const cGameName = "hglbtrtb" ' bootleg 7 digits rom
58:
59: Const UseSolenoids = 2
60: Const UseLamps = 1
61: Const UseGI = 0
62: Const UseSync = 0
63: Const HandleMech = 0
76:     vpmMapLights AllLamps ' Map all lamps into lights array
96:     ' Nudging
97:     vpmNudge.TiltSwitch = swTilt
98:     vpmNudge.Sensitivity = 1
99:     vpmNudge.TiltObj = Array(Bumper1, Bumper2, Bumper3, LeftSlingshot, RightSlingshot, Sling1, Sling2)
100:
101:     ' Trough
102:     Set bsTrough = New cvpmBallStack
103:     With bsTrough
104:         .InitSw 0, 8, 0, 0, 0, 0, 0, 0
105:         .InitKick BallRelease, 80, 6
106:         .InitEntrySnd "fx_Solenoid", "fx_Solenoid"
107:         .InitExitSnd SoundFX("fx_ballrel",DOFContactors), SoundFX("fx_Solenoid",DOFContactors)
108:         .Balls = 1
109:     End With
110:
111:     ' Drop targets
112:     set dtDrop = new cvpmdroptarget
113:     With dtDrop
114:         .initdrop array(d1, d2, d3, d4), array(1, 2, 3, 4)
115:         .initsnd SoundFX("fx_droptarget",DOFContactors), SoundFX("fx_resetdrop",DOFContactors)
116:     End With
117:
118:     ' Middle Saucer
119:     Set bsMSaucer = New cvpmBallStack
120:     With bsMSaucer
121:         .InitSaucer sw24, 24, 192, 12
122:         .KickAngleVar = 2
123:         .KickForceVar = 1
124:         .InitExitSnd SoundFX("fx_kicker",DOFContactors), SoundFX("fx_kicker",DOFContactors)
125:     End With
126:
127:     ' Right Saucer
128:     Set bsRSaucer = New cvpmBallStack
129:     With bsRSaucer
130:         .InitSaucer sw32, 32, 302, 20
131:         .KickAngleVar = 2
132:         .KickForceVar = 1
133:         .InitExitSnd SoundFX("fx_kicker",DOFContactors), SoundFX("fx_kicker",DOFContactors)
134:     End With
```

Switch handlers:

```
180:     vpmTimer.PulseSw 37
198:     vpmTimer.PulseSw 36
211: Sub Sling1_Hit:PlaySoundAtVol "fx_Rubber", ActiveBall, 1:vpmTimer.PulseSw 34:End Sub
212: Sub Sling2_Hit:PlaySoundAtVol "fx_Rubber", ActiveBall, 1:vpmTimer.PulseSw 34:End Sub
214: ' Bumpers
215: Sub Bumper1_Hit:vpmTimer.PulseSw 40:PlaySoundAtVol SoundFX("fx_bumper",DOFContactors),Bumper1, VolBump:End Sub
216: Sub Bumper2_Hit:vpmTimer.PulseSw 38:PlaySoundAtVol SoundFX("fx_bumper",DOFContactors),Bumper2, VolBump:End Sub
217: Sub Bumper3_Hit:vpmTimer.PulseSw 39:PlaySoundAtVol SoundFX("fx_bumper",DOFContactors),Bumper3, VolBump:End Sub
218:
219: ' Drain & holes
220: Sub Drain_Hit:PlaysoundAtVol "fx_drain", drain, 1:bsTrough.AddBall Me:End Sub
221: Sub sw24_Hit:PlaySoundAtVol "fx_kicker_enter",sw24,VolKick:bsMSaucer.AddBall 0:End Sub
222: Sub sw32_Hit:PlaySoundAtVol "fx_kicker_enter",sw32,VolKick:bsRSaucer.AddBall 0:End Sub
223:
224: ' Rollovers
225: Sub sw31_Hit:Controller.Switch(31) = 1:PlaySoundAtVol "fx_sensor", ActiveBall, 1:End Sub
226: Sub sw31_UnHit:Controller.Switch(31) = 0:End Sub
227:
228: Sub sw22_Hit:Controller.Switch(22) = 1:PlaySoundAtVol "fx_sensor", ActiveBall, 1:End Sub
229: Sub sw22_UnHit:Controller.Switch(22) = 0:End Sub
230:
231: Sub sw23_Hit:Controller.Switch(23) = 1:PlaySoundAtVol "fx_sensor", ActiveBall, 1:End Sub
232: Sub sw23_UnHit::Controller.Switch(23) = 0:End Sub
233:
234: 'Spinners
235: Sub sw17_Spin():vpmTimer.PulseSw 17:PlaySoundAtVol "fx_spinner",sw17,VolSpin:End Sub
236: Sub sw33_Spin():vpmTimer.PulseSw 33:PlaySoundAtVol "fx_spinner",sw32,VolSpin:End Sub
237: Sub sw25_Spin():vpmTimer.PulseSw 25:PlaySoundAtVol "fx_spinner",sw25,VolSpin:End Sub
238:
239: ' Droptargets
240: Sub d1_Hit:dtDrop.Hit 1:PlaySoundAtVol SoundFX("fx_droptarget",DOFContactors),ActiveBall, VolTarg:End Sub
241: Sub d2_Hit:dtDrop.Hit 2:PlaySoundAtVol SoundFX("fx_droptarget",DOFContactors),ActiveBall, VolTarg:End Sub
242: Sub d3_Hit:dtDrop.Hit 3:PlaySoundAtVol SoundFX("fx_droptarget",DOFContactors),ActiveBall, VolTarg:End Sub
243: Sub d4_Hit:dtDrop.Hit 4:PlaySoundAtVol SoundFX("fx_droptarget",DOFContactors),ActiveBall, VolTarg:End Sub
244:
245: ' Targets
246: Sub sw35_Hit:vpmTimer.PulseSw 35:PlaySoundAtVol SoundFX("fx_target",DOFContactors),ActiveBall, VolTarg:End Sub
247: Sub sw26_Hit:vpmTimer.PulseSw 26:PlaySoundAtVol SoundFX("fx_target",DOFContactors),ActiveBall, VolTarg:End Sub
248: Sub sw27_Hit:vpmTimer.PulseSw 27:PlaySoundAtVol SoundFX("fx_target",DOFContactors),ActiveBall, VolTarg:End Sub
249: Sub sw28_Hit:vpmTimer.PulseSw 28:PlaySoundAtVol SoundFX("fx_target",DOFContactors),ActiveBall, VolTarg:End Sub
250: Sub sw29_Hit:vpmTimer.PulseSw 29:PlaySoundAtVol SoundFX("fx_target",DOFContactors),ActiveBall, VolTarg:End Sub
251: Sub sw30_Hit:vpmTimer.PulseSw 30:PlaySoundAtVol SoundFX("fx_target",DOFContactors),ActiveBall, VolTarg:End Sub
```

Solenoid and flipper callbacks:

```
257: SolCallback(7) = "bsTrough.SolOut"
258: SolCallback(6) = "vpmSolSound SoundFX(""fx_Knocker"",DOFKnocker),"
259: SolCallBack(13) = "bsMSaucer.SolOut"
260: SolCallBack(14) = "bsRSaucer.SolOut"
261: SolCallback(15) = "dtDrop.SolDropUp"
262: SolCallback(19) = "vpmNudge.SolGameOn"
263: SolCallback(17) = "Soldiv"
264:
265: Sub Soldiv(Enabled)
266:     vpmSolDiverter RightLaneGate, True, Not Enabled
267: End Sub
268:
269: '**************
270: ' Flipper Subs
271: '**************
272:
273: SolCallback(sLRFlipper) = "SolRFlipper"
274: SolCallback(sLLFlipper) = "SolLFlipper"
275:
276: Sub SolLFlipper(Enabled)
277:     If Enabled Then
278:         PlaySoundAtVol SoundFX("fx_flipperup",DOFContactors), LeftFlipper, VolFlip
279:         PlaySoundAtVol "fx_flipperup", LeftFlipper1, VolFlip
280:         LeftFlipper.RotateToEnd
281:         LeftFlipper1.RotateToEnd
282:     Else
283:         PlaySoundAtVol SoundFX("fx_flipperdown",DOFContactors), LeftFlipper, VolFlip
284:         PlaySoundAtVol "fx_flipperdown", LeftFlipper1, VolFlip
285:         LeftFlipper.RotateToStart
286:         LeftFlipper1.RotateToStart
287:     End If
288: End Sub
289:
290: Sub SolRFlipper(Enabled)
291:     If Enabled Then
292:         PlaySoundAtVol SoundFX("fx_flipperup",DOFContactors), RightFlipper, VolFlip
293:         RightFlipper.RotateToEnd
294:     Else
295:         PlaySoundAtVol SoundFX("fx_flipperdown",DOFContactors), RightFlipper, VolFlip
296:         RightFlipper.RotateToStart
297:     End If
298: End Sub
```

Option-switch form (credited in the script to Inkochnito):

```
366: '*************************************
367: 'Bally Harlem Globetrotters 7 digits
368: 'added by Inkochnito
369: '*************************************
370: Sub editDips
371:     Dim vpmDips:Set vpmDips = New cvpmDips
372:     With vpmDips
373:         .AddForm 700, 400, "Harlem GlobeTrotters 7 digits - DIP switches"
374:         .AddFrame 2, 0, 190, "Maximum credits", &H03000000, Array("10 credits", 0, "15 credits", &H01000000, "25 credits", &H02000000, "free play (40 credits)", &H03000000)                    'dip 25&26
375:         .AddFrame 2, 87, 190, "Sound features", &H30000000, Array("chime effects", 0, "noises and no background", &H10000000, "noise effects", &H20000000, "noises and background", &H30000000) 'dip 29&30
376:         .AddFrame 2, 170, 190, "Special adjustment", &H00000060, Array("points", 0, "extra ball", &H00000040, "replay/extra ball", &H00000060)                                                  'dip 6&7
377:         .AddFrame 2, 230, 190, "5 side target lite adjustment", &H00800000, Array("targets will reset", 0, "targets are held in memory", &H00800000)                                            'dip 24
378:         .AddFrame 2, 276, 190, "G-L-O-B-E saucer scanning adjustment", &H00002000, Array("Globe lites do not scan", 0, "Globe lites keep scanning", &H00002000)                                 'dip 14
379:         .AddFrame 2, 322, 190, "Dunk shot target special", &H00400000, Array("is reset after collecting", 0, "stays lit", &H00400000)                                                           'dip 23
380:         .AddFrame 205, 0, 190, "High game to date", &H00200000, Array("no award", 0, "3 credits", &H00200000)                                                                                   'dip 22
381:         .AddFrame 205, 46, 190, "Score version", &H00100000, Array("6 digit scoring", 0, "7 digit scoring", &H00100000)                                                                         'dip 21
382:         .AddFrame 205, 92, 190, "Balls per game", &H40000000, Array("3 balls", 0, "5 balls", &H40000000)                                                                                        'dip 31
383:         .AddFrame 205, 138, 190, "Saucer targets reset", &H00000080, Array("when ball enters target saucer", 0, "on next ball in play", &H00000080)                                             'dip 8
384:         .AddFrame 205, 184, 190, "Super bonus", &H00004000, Array("is reset every ball", 0, "is held in memory", &H00004000)                                                                    'dip 15
385:         .AddFrame 205, 230, 190, "Globe special lite adjustment", &H80000000, Array("left outlane 25K only lit", 0, "left outlane 25K and Globe special lit", &H80000000)                       'dip 32
386:         .AddFrame 205, 276, 190, "Left and right spinner adjust", 32768, Array("left spinner only which alternates", 0, "left and right spinner lite on", 32768)                                'dip 16
387:         .AddChk 205, 330, 180, Array("Match feature", &H08000000)                                                                                                                               'dip 28
388:         .AddChk 205, 350, 115, Array("Credits displayed", &H04000000)                                                                                                                           'dip 27
389:         .AddLabel 50, 370, 350, 20, "After hitting OK, press F3 to reset game with new settings."
390:         .ViewDips
391:     End With
392: End Sub
393: Set vpmShowDips = GetRef("editDips")
```

`vpmSolDiverter RightLaneGate, True, Not Enabled` keeps the right lane gate open while public 17 is off and closes it while 17 is on. `LeftFlipper1` is the upper left flipper; the script moves it together with `LeftFlipper` from the single left flipper callback.

The form's "Score version" frame claims option switch S21 selects 6- or 7-digit scoring, and its "High game to date" frame offers only S22 off ("no award") or on ("3 credits"). The game's manual gives S21 and S22 together as the high score to date award (`manual-game-adjustments.md`). The form is titled for the 7-digit conversion, so this may be that conversion's reuse of S21; nothing retained settles it.
