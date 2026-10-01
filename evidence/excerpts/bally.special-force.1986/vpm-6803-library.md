# Transcription: VPinMAME Bally 6803 script library constants (6803.vbs and core.vbs)

Source: the VPinMAME Visual Basic script library that Bally 6803 tables load (`LoadVPM ..., "6803.VBS", ...`),
read from the maintainer's Visual Pinball installation at `L:\Visual Pinball\Scripts\` and retained under the working
root's `review-artifacts/vpm-script-libs/`: `6803.vbs` SHA-256
`472b75fd486282a9533bd5c999d965544cb0803655ecc0f996de01d8a79a38e6` ("Last Updated in VBS v3.61") and the `core.vbs`
it executes, SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`. The library is shared by
every 6803 game; this one copy is cited by Special Force and Beat the Clock. Lines are quoted verbatim, with the
files' tab indentation kept.

## 6803.vbs lines 17-51

```vbs
'-------------------------
' Bally 6803 Data
'-------------------------
' Flipper Solenoid
Const GameOnSolenoid   = 19
' Cabinet switches
Const swCPUDiag        = -7
Const swSoundDiag      = -6
Const swStartButton    =  6
Const swKP0            =  2
Const swKP1            = 11
Const swKP2            = 10
Const swKP3            =  9
Const swKP4            = 19
Const swKP5            = 18
Const swKP6            = 17
Const swKP7            = 27
Const swKP8            = 26
Const swKP9            = 25
Const swKPA            = 12
Const swKPB            = 20
Const swKPC            = 28
Const swKPEnter        =  1
Const swKPClear        =  3
Const swKPGame         =  4
Const swTilt           = 15
Const swSlamTilt       = 14
Const swCoin3          =  9
Const swCoin1          = 10
Const swCoin2          = 11

Const swLRFlip         = 82
Const swLLFlip         = 84
Const swURFlip         = 81
Const swULFlip         = 83
```

## core.vbs lines 2121-2133 (`vpmFlips` initialization)

When a table sets `UseSolenoids = 2`, the flipper helper takes its enable solenoid from the platform library's
`GameOnSolenoid`:

```vbs
		If UseSolenoids >= 2 Then
			On Error Resume Next
				If UseSolenoids > 2 Then
					Solenoid = UseSolenoids
				Else
					err.clear
					if IsEmpty(GameOnSolenoid) or Err then msgbox "VPMflips error: " & err.description
					if err = 500 then 'Error 500 - Variable not defined
						msgbox "UseSolenoids = 2 error!" & vbnewline & vbnewline & "GameOnSolenoid is not defined!" & vbnewline & _
						"System may be incompatible (Check the compatibility list) or your system scripts may be out of date"
					End If
					Solenoid = GameOnSolenoid
				End If
```
