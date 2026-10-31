# VPinMAME sega.vbs and core.vbs — Whitestar constants and key handlers (Elvis, Stern)

Quoted verbatim from `sega.vbs` ("Last Updated in VBS v3.61", SHA-256 `d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924`), the library the retained Elvis
1.0.2 table loads with `LoadVPM "01560000", "SEGA.VBS", 3.26`, and from the `core.vbs` it executes (SHA-256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`). Both were copied byte for byte from the contributor's Visual Pinball `Scripts` folder. Line numbers are
the files' own.

## sega.vbs constants (lines 20-39)

```text
   20: ' Sega / Stern Whitestar Data
   21: '----------------------------
   22: ' Flipper Solenoid
   23: Const GameOnSolenoid = 15
   24: ' Cabinet switches
   25: Const swBlack         =  0 'DED 8
   26: Const swGreen         = -1 'DED 7
   27: Const swRed           = -2 'DED 6
   28: Const swMemoryProtect = -3 'Coin door memory protect switch
   29: Const swStartButton   = 54
   30: Const swTilt          = 56
   31: Const swSlamTilt      = 55
   32: Const swCoin3         =  4
   33: Const swCoin1         =  5
   34: Const swCoin2         =  6
   35:
   36: Const swLRFlip        = 82
   37: Const swLLFlip        = 84
   38: Const swURFlip        = 81
   39: Const swULFlip        = 83
```

`swSlamTilt = 55` is generic Whitestar: Elvis's switch grid prints 55 as TOURNAMENT START and has no slam tilt switch.
`swURFlip = 81` and `swULFlip = 83` name the right and left end-of-stroke inputs; the key handlers write them only when
an upper flipper solenoid is registered. No constant names dedicated input 88, Elvis's upper right flipper button.

## sega.vbs key handlers (lines 71-105)

```text
   71: ' Keyboard handlers
   72: Function vpmKeyDown(ByVal keycode)
   73: 	vpmKeyDown = True ' Assume we handle the key
   74: 	With Controller
   75: 		Select Case keycode
   76: 			Case LeftFlipperKey
   77: 				.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True
   78: 				If keycode = StagedLeftFlipperKey Then ' as vbs will not evaluate the Case StagedLeftFlipperKey then, also handle it here
   79: 					vpmFlips.FlipUL True
   80: 					If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
   81: 				End If
   82: 			Case RightFlipperKey
   83: 				.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True
   84: 				If keycode = StagedRightFlipperKey Then ' as vbs will not evaluate the Case StagedRightFlipperKey then, also handle it here
   85: 					vpmFlips.FlipUR True
   86: 					If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
   87: 				End If
   88: 			Case StagedLeftFlipperKey vpmFlips.FlipUL True : If vpmFlips.FlipperSolNumber(2) <> 0 Then .Switch(swULFlip) = True
   89: 			Case StagedRightFlipperKey vpmFlips.FlipUR True : If vpmFlips.FlipperSolNumber(3) <> 0 Then .Switch(swURFlip) = True
   90:
   91: 			Case keyInsertCoin1  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
   92: 			Case keyInsertCoin2  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin2'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
   93: 			Case keyInsertCoin3  vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin3'" : If Not IsEmpty(Eval("SCoin")) Then Playsound SCoin
   94: 			Case StartGameKey    .Switch(swStartButton) = True
   95: 			Case keyBlack        .Switch(swBlack)       = True
   96: 			Case keyGreen        .Switch(swGreen)       = True
   97: 			Case keyRed          .Switch(swRed)         = True
   98: 			Case keySlamDoorHit  .Switch(swSlamTilt)    = True
   99: 			Case keyCoinDoor     If toggleKeyCoinDoor Then .Switch(swMemoryProtect) = Not .Switch(swMemoryProtect) Else .Switch(swMemoryProtect) = Not inverseKeyCoinDoor
  100: 			Case keyBangBack     vpmNudge.DoMechTilt
  101: 			Case keyVPMVolume    vpmVol
  102: 			Case Else            vpmKeyDown = False
  103: 		End Select
  104: 	End With
  105: End Function
```

## core.vbs flipper solenoid constants (lines 2862-2865)

```text
 2862: Const sLRFlipper = 46
 2863: Const sLLFlipper = 48
 2864: Const sURFlipper = 34
 2865: Const sULFlipper = 36
```
