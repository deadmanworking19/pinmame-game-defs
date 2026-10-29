# Exact Gold flasher callbacks

Leading indentation is expanded to spaces and trailing horizontal whitespace is omitted. Statements, quoted contents, source line numbers and full region boundaries are preserved; original byte-for-byte scripts/source remain external.

Embedded Gold script, original byte SHA-256 `2c33d2b7bb40fab1f41747170e55a2f2638928f6b33179955f4d0bc6eeca254c`, cp1252 decoded to UTF-8. Literal complete callback region with original line numbers. The render layers are bindings, not a physical bulb census; circuit 19's three bulbs come from the Gold manual and BOM.

```vb
413: End Sub
414:
415: Sub ThingKickOut(Enabled)
416: 	If Enabled Then
417: 		ThingKickOutKicker.TimerEnabled = 1
418: 	End If
419: End Sub
420:
421: Sub ThingKickOutKicker_Timer
422: 	ThingKickOutKicker.Kick 180, 6, 5   'thinkkickoutkicker
423:     Controller.switch(77) = 0	'Thing KickOut
424: 	Playsound "SubWay"
425: 	ThingKickOutKicker.TimerEnabled = 0
426: End Sub
427:
428: Sub LockupKickout(Enabled)
429: 	If Enabled Then
430: 		SwampLockUp.TimerEnabled = 1
431: 	End If
432: End Sub
433:
434: Sub	 LlightningBoltFlasher(Level)
435: 	 If Level > 0 Then
436: 		LLightning.intensityScale = (Level / 2.55)/100
437: 		Light13c.intensityScale = (Level / 2.55)/100
438: 		Light13d.intensityScale = (Level / 2.55)/100
439: 		Light15.intensityScale = (Level / 2.55)/100
440: 		Light25.intensityScale = (Level / 2.55)/100
441: 		LLightning.State = 1
442: 		Light13c.state = 1
443: 		Light13d.state = 1
444: 		Light15.state = 1
445: 		Light25.state = 1
446: 		PrimCase7 = 1
447: 		Prim7.Enabled = 1
448: 	Else
449: 		LLightning.State = 0
450: 		Light13c.state = 0
451: 		Light13d.state = 0
452: 		Light15.state = 0
453: 		Light25.state = 0
454: 		PrimCase7 = 4
455: 		Prim7.Enabled = 1
456: 	End If
457: End Sub
458:
459: Sub	 RlightningBoltFlasher(Level)
460: 	 If Level > 0 Then
461: 		RLightning.intensityScale = (Level / 2.55)/100
462: 		Light4.intensityScale = (Level / 2.55)/100
463: 		Light4b.intensityScale = (Level / 2.55)/100
464: 		Light6.intensityScale = (Level / 2.55)/100
465: 		Light23.intensityScale = (Level / 2.55)/100
466: 		RLightning.State = 1
467: 		Light4.state = 1
468: 		Light4b.state = 1
469: 		Light6.state = 1
470: 		Light23.state = 1
471: 		PrimCase3 = 1
472: 		Prim3.Enabled = 1
473: 	Else
474: 		RLightning.State = 0
475: 		Light4.state = 0
476: 		Light4b.state = 0
477: 		Light6.state = 0
478: 		Light23.state = 0
479: 		PrimCase3 = 4
480: 		Prim3.Enabled = 1
481: 	End If
482: End Sub
483:
484: Sub LowerRampFlasher(level)
485: 	If Level > 0 Then
486: 	Light10.intensityScale = (Level / 2.55)/100
487: 	Light10b.intensityScale = (Level / 2.55)/100
488: 	Light12.intensityScale = (Level / 2.55)/100
489: 	Light24.intensityScale = (Level / 2.55)/100
490: 	Light20.intensityScale = (Level / 2.55)/100
491: 	Light10.State = 1
492: 	Light10b.State = 1
493: 	Light12.State = 1
494: 	Light24.State = 1
495: 	Light20.State = 1
496: 	Else
497: 	Light10.State = 0
498: 	Light10b.State = 0
499: 	Light12.State = 0
500: 	Light24.State = 0
501: 	Light20.State = 0
502: 	End If
503: End Sub
504:
505: Sub ThePowerFlasher(Level)
506: 	If Level > 0 Then
507: 		ThePower.intensityScale = (Level / 2.55)/100
508: 		ThePower.State = 1
509: 	Else
510: 		ThePower.State = 0
511: 	End If
512: End Sub
513:
514: Sub TrainFlasher(level)
515: 	If Level > 0 Then
516: 		Light1.intensityScale = (Level / 2.55)/100
517: 		Light1b.intensityScale = (Level / 2.55)/100
518: 		Light2.intensityScale = (Level / 2.55)/100
519: 		Light2b.intensityScale = (Level / 2.55)/100
520: 		Light3.intensityScale = (Level / 2.55)/100
521: 		Light35.intensityScale = (Level / 2.55)/100
```
