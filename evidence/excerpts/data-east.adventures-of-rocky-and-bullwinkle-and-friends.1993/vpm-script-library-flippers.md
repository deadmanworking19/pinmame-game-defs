# Data East The Adventures of Rocky and Bullwinkle and Friends (1993) - flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, extracted from `The Adventures of Rocky and Bullwinkle and Fiends (Data East 1993) 1.0.vpx`, SHA-256 `09f43d857b0a97eb2c6c1384db91e5f2aee6ab55541fcdb64292a77f8b4eb464`) and the VPinMAME script library it loads, retained from the contributor's working installation as `de.vbs` (SHA-256 `8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04`) and `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files; the table script is Windows-1252 text.

Quoted lines are verbatim except for whitespace: the trailing space of `script.vbs` line 153, and the leading space before the tab and the trailing tab of `script.vbs` line 354, are dropped so that the excerpt passes Git's whitespace check. The retained script's SHA-256 above stays authoritative.

`script.vbs` line 126 selects the ROM (line 127 keeps the 1.30 set as a commented alternative), line 153 loads the library, and lines 225-226 leave mechanics and keyboard handling to the script:

```vbscript
Const cGameName 			= "rab_320"		'
'Const cGameName 			= "rab_130"
LoadVPM "01560000","DE.VBS",3.1
         .HandleMechanics = 0
         .HandleKeyboard = 0
```

Line 1 is `'Option Explicit`, commented out.

`de.vbs` lines 21-36 (cabinet switches and flipper switches):

```vbscript
Const GameOnSolenoid = 23
' Cabinet switches
Const swBlack        = -7
Const swGreen        = -6
Const swTilt         =  1
Const swBallRollTilt =  2
Const swStartButton  =  3
Const swCoin1        =  4
Const swCoin2        =  5
Const swCoin3        =  6
Const swSlamTilt     =  7

Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 86
Const swULFlip       = 88
```

`de.vbs` `vpmKeyDown` (line 62) sets the lower flipper switches from the cabinet keys (lines 67 and 73), and `vpmKeyUp` (line 94) clears them the same way with `= False` (lines 99 and 105):

```vbscript
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same functions write the upper constants 86 and 88 only from a staged flipper key and only while `vpmFlips.FlipperSolNumber(3)` or `(2)` is non-zero (`de.vbs` lines 68-70, 74-76, 78-79 in `vpmKeyDown`, 100-102, 106-108, 110-111 in `vpmKeyUp`):

```vbscript
			Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
			Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
```

`core.vbs` line 2090 sets the default solenoid numbers, lines 2854-2855 route the script's handlers to the library, and lines 2862-2865 define the numbers:

```vbscript
		FlipperSolNumber(0)=sLLFlipper :FlipperSolNumber(1)=sLRFlipper :FlipperSolNumber(2)=sULFlipper : FlipperSolNumber(3)=sURFlipper
Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

The table's key handling (`script.vbs` lines 351-374). Both subs write matrix switches 15 and 16 from the flipper keys before they hand the key to the library, and write switch 9 from the plunger key after it:

```vbscript
Sub Rab_KeyUp(ByVal keyCode)
	If keycode = LeftFlipperKey Then  Controller.Switch(15) = False  End If
	If keycode = RightFlipperKey Then	Controller.Switch(16) = False End If
	If KeyUpHandler(keyCode) Then Exit Sub
	If keyCode=PlungerKey Then  Controller.Switch(9)=false: END IF
Sub RaB_KeyDown(ByVal keyCode)
If keycode = LeftFlipperKey Then  Controller.Switch(15) = True End If
	If keycode = RightFlipperKey Then	Controller.Switch(16) = True End If
    If KeyDownHandler(keyCode) Then Exit Sub
	If keyCode=PlungerKey Then Controller.Switch(9)=true END IF
```

The solenoid callbacks the flippers use (`script.vbs` lines 161-162), and the subs they call (lines 1405-1423) move `LeftFlipper` and `RightFlipper` with `RotateToEnd` while the solenoid is on and `RotateToStart` when it is off:

```vbscript
SolCallback(sLLFlipper) = "solLFlipper"
SolCallback(sLRFlipper) = "solRFlipper"
```

The table never writes `Controller.Switch` 81-88 itself, never references `vpmFlips`, never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, and never defines `cSingleLFlip` or `cSingleRFlip`.
