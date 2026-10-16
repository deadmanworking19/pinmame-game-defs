# Paragon - the VPinMAME Bally library the table loads

The table calls `LoadVPM "01130100", "Bally.VBS", 3.21`. The retained copy is `Bally.vbs` from the local VPinMAME scripts folder (first line `'Last Updated in VBS v3.61`, SHA-256 `d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c`), kept with `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`) under the table's evidence folder. Quoted lines:

```
Const GameOnSolenoid   = 19
Const swSelfTest       = -7
Const swCPUDiag        = -6
Const swSoundDiag      = -5
Const swTilt           =  7
Const swBallRollTilt   =  2
Const swSlamTilt       = 16
Const swCoin3          =  9
Const swCoin2          = 10
Const swCoin1          = 11
Const swStartButton    =  6
Const swLRFlip         = 82
Const swLLFlip         = 84
Const swURFlip         = 81
Const swULFlip         = 83
```

From `core.vbs`:

```
Const sLRFlipper = 46
Const sLLFlipper = 48
```

The library's key handler writes `swLLFlip` (84) and `swLRFlip` (82) for the lower flipper keys, and writes `swULFlip` (83) and `swURFlip` (81) only when `vpmFlips.FlipperSolNumber(2)` or `(3)` is non-zero, which the Paragon table never configures.

These constants are generic to every Bally MPU game. On Paragon two of them name a different device from the game's own manual: public 2 is in-line drop target C, not a ball-roll tilt (the ball tilt is one of the three contacts on public 7), and the coin constants number the chutes 11 = coin 1, 10 = coin 2, where the manual calls public 10 "Coin I (left)" and public 11 "Coin II (middle)".
