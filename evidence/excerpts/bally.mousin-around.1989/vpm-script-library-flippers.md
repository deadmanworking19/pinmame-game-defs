# Mousin' Around! (Bally 1989) — flipper keys through the VPinMAME script library

Sources: the retained known-working table script (`script.vbs` of `Mousin_ Around! (Bally 1989).vpx`, Herweh
version 1.0, SHA-256 `959acd6b408903f3c71c8c0cf1fedf3345a3cc1105f0399e42824e22dd1cf282`) and the VPinMAME script
library it loads, retained from the contributor's working installation as `s11.vbs` (SHA-256
`5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91`) and `core.vbs` (SHA-256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Read from the files. The table asks for
library version 3.26; the retained library is newer, and the lines quoted below are the ones the table's flipper
keys reach.

`script.vbs` line 139 loads the library, and lines 164-165 leave mechanisms and the keyboard to the script:

```vbscript
LoadVPM "01560000", "S11.VBS", 3.26
		.HandleMechanics 	= False
		.HandleKeyboard 	= False
```

`s11.vbs` lines 37-40:

```vbscript
Const swLRFlip       = 82
Const swLLFlip       = 84
Const swURFlip       = 81
Const swULFlip       = 83
```

`s11.vbs` `vpmKeyDown` (line 69) sets the lower flipper switches from the cabinet keys (lines 73-74 and 79-80), and
`vpmKeyUp` (line 104) clears them the same way with `= False` (lines 108-109 and 114-115):

```vbscript
			Case LeftFlipperKey
				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
...
			Case RightFlipperKey
				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
```

`core.vbs` lines 2862-2863 name the synthetic flipper hold outputs:

```vbscript
Const sLRFlipper = 46
Const sLLFlipper = 48
```

`script.vbs` lines 318-319 bind them to the table's flipper subs:

```vbscript
SolCallback(sLLFlipper) = "SolLFlipper"
SolCallback(sLRFlipper) = "SolRFlipper"
```

`MousinAround_KeyDown` writes the two matrix addresses itself before handing every key to the library (lines 237,
238 and 244), and `MousinAround_KeyUp` does the same on release (lines 258-260):

```vbscript
	If keycode = LeftFlipperKey Then Controller.Switch(58) = True
    If keycode = RightFlipperKey Then Controller.Switch(57) = True
...
	If vpmKeyDown(keycode) Then Exit Sub
...
	If keycode = LeftFlipperKey Then Controller.Switch(58) = False
    If keycode = RightFlipperKey Then Controller.Switch(57) = False
    If vpmKeyUp(keycode) Then Exit Sub
```

The script never writes any of `81-88` by number, never calls `NoUpperLeftFlipper` or `NoUpperRightFlipper`, never
names a staged flipper key, and never defines `cSingleLFlip` or `cSingleRFlip`.
