# Harlem Globetrotters On Tour - the VPinMAME Bally library the table loads

The pinned corpus script calls `LoadVPM "01550000", "Bally.vbs", 3.26`. The retained copy is `Bally.vbs` from the local VPinMAME scripts folder (first line `'Last Updated in VBS v3.61`, SHA-256 `d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c`), kept with `core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`) under the table's evidence folder. Quoted lines, `Bally.vbs` lines 21-37:

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

From `core.vbs` lines 2862-2865:

```
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

The library's key handler (`Bally.vbs` lines 77-123) writes `swLLFlip` (84) and `swLRFlip` (82) for the lower flipper keys. It writes `swULFlip` (83) and `swURFlip` (81) for the staged left and right flipper keys when `vpmFlips.FlipperSolNumber(2)` or `(3)` is non-zero. `core.vbs` sets those two numbers to `sULFlipper` (36) and `sURFlipper` (34) by default (line 2090). Its `Init` zeroes them through `NoUpperLeftFlipper` and `NoUpperRightFlipper` only when the table defines `cSingleLFlip` or `cSingleRFlip` as false (lines 2061-2062 and 2111-2116). This table defines neither and never calls either sub, so a staged flipper key does write 83 or 81. Its upper left flipper moves with the lower one in `SolLFlipper`.

These constants are generic to every Bally MPU game. On this game two of them name a different device from the game's own manual: public 2 is drop target "C", not a ball-roll tilt (the manual's ball tilt is one of the three contacts on public 7, "TILT (3)", with the panel and plumb bob tilts), and the coin constants number the chutes 11 = coin 1, 10 = coin 2, where the manual's switch table calls public 10 "COIN I (LEFT)" and public 11 "COIN II (MIDDLE)". `core.vbs`'s upper flipper constants 34 and 36 are generic defaults that never reach this table. The Bally controller profile has no solenoid address 34 or 36, and this machine's three flipper coils are reached only through PinMAME's synthetic flipper outputs 45-48.
