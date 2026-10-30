# Data East RoboCop (1989) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`00abf00a3f2e9cc3977e1053765902071a7caf381407b58ad09c4bef8abe3dd8`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256
`8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`, "Last Updated in VBS v3.61") and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.

`script.vbs` line 102 loads the library and line 135 leaves keyboard handling to the script:

```vbscript
LoadVPM "01560000", "DE.VBS", 3.46
       .HandleKeyboard=0
```

`de.vbs` lines 33-36:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 86
Const swULFlip       = 88
```

`de.vbs` `vpmKeyDown` (line 62) sets the lower flipper switches from the cabinet keys (lines 67 and 73), and `vpmKeyUp` (line 94) clears them the same way with `= False` (lines 99 and 105):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The table's key handling, with the flipper and library lines:

```vbscript
Sub Table1_KeyDown(ByVal Keycode)   ' line 259
	If keycode=RightFlipperKey Then Controller.Switch(15)=1   ' line 260
	If keycode=LeftFlipperKey Then Controller.Switch(16)=1   ' line 261
...
	If vpmKeyDown(keycode)Then Exit Sub   ' line 286
...
Sub Table1_KeyUp(ByVal Keycode)   ' line 290
	If keycode=RightFlipperKey Then Controller.Switch(15)=0   ' line 292
    If keycode=LeftFlipperKey Then Controller.Switch(16)=0   ' line 293
...
	If vpmKeyUp(keycode)Then Exit Sub   ' line 309
```

The trailing `' line NNN` markers above are added here to give the location and are not in the script.

Lines 260-261 and 292-293 write 15 from the right key and 16 from the left, the reverse of the driver's `FLIP1516 = FLIP_SWNO(15,16)`. Those writes have no effect: `core_updateSw` overwrites 15 and 16 from the cabinet-button bits 84 and 82 on every update, and lines 286 and 309 write those bits through `vpmKeyDown`/`vpmKeyUp`.

The script never calls `vpmInit`, `NoUpperLeftFlipper` or `NoUpperRightFlipper` and never names a staged flipper key.
