# Retained System 11 VPinMAME library constants

SHA-256: 5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91. Library constants are transport names; game-specific manual overrides generic Ball Roll Tilt at switch 2.

```vb
23: ' Cabinet switches
24: Const swAdvance      = -7
25: Const swUpDown       = -6
26: Const swCPUDiag      = -5
27: Const swSoundDiag    = -4
28: Const swTilt         =  1
29: Const swBallRollTilt =  2
30: Const swStartButton  =  3
31: Const swCoin3        =  4
32: Const swCoin2        =  5
33: Const swCoin1        =  6
34: Const swSlamTilt     =  7
35: Const swHiScoreReset =  8
36:
37: Const swLRFlip       = 82
38: Const swLLFlip       = 84
39: Const swURFlip       = 81
40: Const swULFlip       = 83
41:
42: ' Help Window
43: vpmSystemHelp = "Williams System 9/11 keys:" & vbNewLine &_
44:   vpmKeyName(keyInsertCoin1)  & vbTab & "Insert Coin #1"   & vbNewLine &_
45:   vpmKeyName(keyInsertCoin2)  & vbTab & "Insert Coin #2"   & vbNewLine &_
46:   vpmKeyName(keyInsertCoin3)  & vbTab & "Insert Coin #3"   & vbNewLine &_
47:   vpmKeyName(keyHiscoreReset) & vbTab & "Hiscore Reset"    & vbNewLine &_
```
