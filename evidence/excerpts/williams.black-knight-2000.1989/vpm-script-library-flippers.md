# Williams Black Knight 2000 (1989) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs`, SHA-256
`955bc5ba128b3be1cbab9e7d3afab87389195c76b63185c406477240a880b21d`) and the VPinMAME script library
it loads, retained from the contributor's working installation as `s11.vbs` (SHA-256
`5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`, "Last Updated in VBS v3.61") and
`core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files.
The table asks for library version 3.10 and the retained library is v3.61, so what follows is what the
retained library does with this script, not a claim about the version the table's author used.

`script.vbs` line 142 loads the library, line 148 defines `UseSolenoids`, line 257 leaves keyboard handling
to the script, and the two cabinet flipper callbacks are bound at lines 517-518:

```vbscript
LoadVPM "00990300", "S11.VBS", 3.10
Const UseSolenoids = 1
        .HandleKeyboard = 0
SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"
```

`s11.vbs` lines 37-40:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

`s11.vbs` `vpmKeyDown` (line 69) sets the lower flipper switches from the cabinet keys (lines 73-74 and 79-80),
and `vpmKeyUp` (line 104) clears them the same way with `= False` (lines 108-109 and 114-115):

```vbscript
Case LeftFlipperKey
	.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
Case RightFlipperKey
	.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

The same two functions also write the upper constants from a staged flipper key, but only while `vpmFlips`
holds an upper flipper solenoid number (`s11.vbs` lines 75-86 in `vpmKeyDown`; lines 110-121 repeat them
with `= False` in `vpmKeyUp`):

```vbscript
Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
```

`core.vbs` line 2090 sets those numbers by default, lines 2061-2062 are the helpers a table calls to clear
them, and `cvpmFlips2.Init` (lines 2111-2117, run by `vpmInit`) calls them for the table unless the table's
`cSingleLFlip`/`cSingleRFlip` is True (VBScript's `Not` is bitwise, and an undefined constant raises an error
that `core.vbs`, which starts with `Option Explicit`, turns into a skipped call):

```vbscript
		FlipperSolNumber(0)=sLLFlipper :FlipperSolNumber(1)=sLRFlipper :FlipperSolNumber(2)=sULFlipper : FlipperSolNumber(3)=sURFlipper
Sub NoUpperLeftFlipper() : vpmFlips.FlipperSolNumber(2) = 0 : End Sub
Sub NoUpperRightFlipper() : vpmFlips.FlipperSolNumber(3) = 0 : End Sub
			If not cSingleLFlip Then
				if err.number = 0 then NoUpperLeftFlipper
			End If
```

`core.vbs` lines 2854-2855 route the table's handlers to them:

```vbscript
Function KeyDownHandler(ByVal k) : KeyDownHandler = vpmKeyDown(k) : End Function
Function KeyUpHandler(ByVal k) : KeyUpHandler = vpmKeyUp(k) : End Function
```

`script.vbs` `BK2K_KeyDown` (line 371) hands every key, flipper keys included, to the library at line 377
(`If vpmKeyDown(keycode) Then Exit Sub`), and `BK2K_KeyUp` (line 380) does the same at line 383:

```vbscript
	If keycode = RightMagnaSave Then:Controller.Switch(59) = 1:End If
	If vpmKeyDown(keycode) Then Exit Sub
	If keycode = RightMagnaSave Then:Controller.Switch(59) = False:End If
	If vpmKeyUp(keycode) Then Exit Sub
```

The table's script never writes the flipper matrix switches 57 and 58, and a search of it for `NoUpperLeftFlipper`,
`NoUpperRightFlipper`, `cSingleLFlip` and `cSingleRFlip` finds none of them (it is `Option Explicit`, defines
`UseSolenoids` and calls `vpmInit Me` at line 251). On this table the library therefore does write
`swULFlip` (83) and `swURFlip` (81) when a staged flipper key is pressed, as well as the lower flipper
addresses 82 and 84.

`script.vbs` also writes two matrix switches at start-up, in the block that begins `With Controller` after
`.Run GetPlayerHWnd` (lines 267-268), with the comments left over from a WPC template:

```vbscript
        .Switch(22) = 1 'close coin door
        .Switch(24) = 1 'and keep it close
```
