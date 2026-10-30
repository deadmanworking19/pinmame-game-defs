# VPinMAME script libraries GTS3.VBS and core.vbs

Source: `gts3.vbs` ("Last Updated in VBS v3.61"), retained byte for byte as
`review-artifacts/vpm-script-libs/gts3.vbs` (SHA-256 `66c329fa86e97d2f10a8036a9a6527be6a67ce59bb3591962aa1c8a9da101314`)
from the contributor's Visual Pinball `Scripts` installation, and the `core.vbs` it executes, retained as
`review-artifacts/vpm-script-libs/core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`).
Kiwi's Gladiators script loads the first (`LoadVPM "01560000", "gts3.VBS", 3.26`, its line 193). Line numbers are each
file's; leading whitespace is dropped.

## gts3.vbs

| Line | Text |
| --- | --- |
| 21 | `Const GameOnSolenoid = 32` |
| 23-26 | `Const swCoin1 = 00` · `Const swCoin2 = 01` · `Const swCoin3 = 02` · `Const swCoin4 = 03` |
| 27-29 | `Const swDiagnostic = -8` · `Const swTilt = -7` · `Const swSlamTilt = -6` |
| 31-34 | `Const swLRFlip = 141` · `Const swLLFlip = 143` · `Const swURFlip = 145` · `Const swULFlip = 147` |
| 69 | `If swStartButton = 4 Or Err Then swStartButtonX = 4 Else swStartButtonX = swStartButton` |
| 75-76 | `Case LeftFlipperKey` · `.Switch(swLLFlip) = True : vpmKeyDown = False : vpmFlips.FlipL True` |
| 81-82 | `Case RightFlipperKey` · `.Switch(swLRFlip) = True : vpmKeyDown = False : vpmFlips.FlipR True` |
| 89-92 | `Case keyInsertCoin1 vpmTimer.AddTimer 750,"vpmTimer.PulseSw swCoin1'"` and the same for coins 2-4 |
| 93-95 | `Case StartGameKey .Switch(swStartButtonX) = True` · `Case keySelfTest .Switch(swDiagnostic) = True` · `Case keySlamDoorHit .Switch(swSlamTilt) = True` |
| 107-123 | `vpmKeyUp` writes the same addresses back to False |

## core.vbs

| Line | Text |
| --- | --- |
| 1120 | `Public TiltSwitch` |
| 1130 | `If TiltSwitch <> 0 Then vpmTimer.PulseSw TiltSwitch` |
| 1156 | `Public Sub SolGameOn(aEnabled)` |
| 2861-2865 | `'-- Flipper solenoids (all games)` · `Const sLRFlipper = 46` · `Const sLLFlipper = 48` · `Const sURFlipper = 34` · `Const sULFlipper = 36` |

Kiwi's script also writes matrix switches 82 and 83 from the flipper keys before calling `vpmKeyDown`/`vpmKeyUp`;
the library's 141/143 are the addresses PinMAME copies into 82/83.
