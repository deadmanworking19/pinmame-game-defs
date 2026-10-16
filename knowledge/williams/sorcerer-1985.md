# Sorcerer (Williams, 1985)

Williams model 532, March 1985, System 9 (PinMAME `GEN_S9`), about 3,700 units (IPDB 2242). Design Mark
Ritchie, art Pam Erickson. Two production game ROMs exist in PinMAME, `sorcr_l1` and `sorcr_l2`; both run the
same machine. Two playfield colour schemes are known; they differ only in artwork (IPDB).

Sources: the Instruction Manual with schematics (IPDB, 34 pages), the pinned PinMAME driver, the known-working
VPX script v4.0.4, and LibPinMAME harness runs of both ROMs. The excerpts under
`evidence/excerpts/williams.sorcerer.1985/` quote every table and drawing relied on here.

## Controller and addressing

- System 9 is the System 11 controller family in PinMAME: an 8x8 switch matrix at public 1-64, an 8x8 lamp
  matrix at 1-64, solenoids 1-16 (controlled) and 17-22 (special), the game-on enable at 23, four 7-digit score
  displays and a 4-digit credit / ball-in-play display.
- The manual's printed switch, lamp and solenoid numbers are the public addresses. The ROM's own tests prove it
  for switches 1-45 (Test 03 shows each closure's number) and solenoids 1-16 (Test 02 steps 01-16 and pulses the
  shown number). The specials 17-21 are proved by their trigger switches.
- The switch matrix reads uninverted on System 9 (`s11.c` `pia4a_r`, no inversion mask): every switch is
  normally open and active at public 1.
- Display order in LibPinMAME: index 2 is player 1, 3 player 2, 0 player 3, 1 player 4; 4 and 5 are the credit
  digits, 6 and 7 the ball-in-play / match digits. Player 1's score appears on index 2 in play.
- DIP 0 is CPU jumper W5 on PIA U5 PA7, which the manual says is fitted; it reads 0.

## Playfield and rules

From the manual's game play section:

- **A-B-C-D** (top lanes 17-20, lamps 17-20) advances the bonus multiplier 2X, 4X, 6X, 8X (lamps 49-52), then
  scores 50,000.
- **S-O-R-C-E-R-E-R** is spelled on the left spinner (9, S), the six standup targets 10-15 (O-R-C-E-R-E) and the
  right spinner (16, last R); lamps 9-16 show the letters. Completing it lights DEMON at the 3-bank (22), the
  spinners (lamps 31 and 32, Light Below "S" / "R"), EXTRA BALL (21) and the playfield SPECIAL (8). In the
  special-award run the third spelling awarded a credit.
- **The 3-bank** drop targets (34-36, lamps 53-55): completing it lights one flipper return lane (26/27), awards
  the flashing value, awards the extra ball when lit and spots BONUS HELD OVER (23) with DEMON lit.
- **Lamps 22 and 23 are printed the wrong way round.** The manual's lamp matrix, lamp list and lamp drawing call
  22 Bonus Hold Over and 23 Demon. The ROM lights 22 when S-O-R-C-E-R-E-R is completed and replaces it with 23,
  held into the next ball, when the 3-bank is then completed: by the manual's own rules 22 is DEMON (the
  triangle at the 3-bank) and 23 is BONUS HELD OVER (the large round insert below the centre). The known-working
  script binds them that way.
- **The ramp shot** locks the first ball, starts two-ball MULTI-BALL the second time and advances the playfield
  multiplier (All Scores 2X / 3X / 5X, lamps 28-30) each further time. Lamps 47 (Lock) and 48 (Release) sit at the
  ramp.
- Bonus lamps 33-46 count 1-9 and 10-50.

Rebound switches (A-4834 assemblies) score on rubbers: 39 lower right, 40 lower left, 42 upper left, and 43 at the
top, which the matrix calls Lane Switch and the parts list Lamp Shift.

## Ball path and mechanisms

- **Outhole and ball ramp.** Two balls. A drained ball rolls into the outhole (28) and the outhole kicker (1)
  lifts it onto the ball ramp under the apron: Ramp 1 (29) is the upper position and Ramp 2 (30) the one at the
  exit. The manual's "Ramp Eject" (2) is the ball-ramp release that kicks the ball on 30 into the shooter lane
  (31); the second ball then rolls down to 30. Initialize 29 and 30 closed and 28 open. The ROM keeps firing 2
  while 30 stays closed after a serve, so a recreation must open 30 when the ball leaves.
- **Multi-ball lock.** The ramp shot feeds a kick-out lock, switch 37 ("Ramp Eject for MULTIBALL"). A ball resting
  there is locked and the ROM serves the second ball. On the next ramp shot the second ball rests on the ramp
  switch 38 behind it; the ROM then fires the multi-ball eject (3) and both balls are in play. When both have
  drained through the outhole, the ROM serves the next ball.
- **3-bank drop targets** (34-36) with one reset coil (4), fired at game start and on completion.
- **Slingshots ("kickers")** 17 (left, switch 32) and 18 (right, switch 33) and **jet bumpers** 19 (left, 21),
  20 (lower, 22) and 21 (right, 23) are System 9 special solenoids: on the machine each device's own special switch
  fires its coil through the CPU board while the game-on enable is set; in PinMAME the listed matrix switch
  publishes the coil (`sxx.ssSw`). Special #6 (22) has no load.
- **Spinners** 9 (left) and 16 (right), free-spinning, no coil.
- **Flippers.** Three 50 V flippers wired to the cabinet buttons through the CPU board's flipper relay K1: the
  right flipper (FL23) on the right button, and the lower-left (FL23) and the top flipper (FL24) on the
  left button's two contacts. The top flipper sits in the centre of the playfield beside the lower jet bumper,
  below the S-O-R-C-E-R-E-R targets; the cabinet sheet calls its contact UPPER LEFT FLIPPER. The flippers work
  only while the game-on enable 23 is set (K1 pulled in). PinMAME fabricates 45/46 from button 82 and 47/48 from
  button 84.
- **Lane change.** Switch 44 (B-9951) closes with the right flipper; the ROM uses it to rotate the lit lane.
  PinMAME copies flipper-column button 82 into 44 (`FLIP_SWNO(0,44)`), so a consumer drives 82. The left side has
  no matrix switch.

## Spatial placement

The retained VPX table (version 4.0.4) supplies every playfield position; each device is anchored to the object
its script binding names, and projections (slingshot and rebound walls, kicker proxies, the lane-change switch on
the right flipper pivot, coil effects on their devices) are disclosed on the device. The manual's switch, solenoid
and lamp location drawings were read independently and fitted to the table: 90 of the 93 checked placements land
within 0.07 normalized of their own callout and are validated. Three stay observed: the left spinner (9, whose
leader ends on the bracket's end post just beyond the limit), the upper ball-ramp position (29, which the drawing
leads to the same ball-ramp exit as 30) and the top rebound switch (43, whose leader stops at the top wall).
Still unplaced: the playfield tilt (45, under the playfield and drawn nowhere) and the Demon background flash
lamps (5, which no drawing numbers and the table models only on its backglass). The 3-bank and S-O-R-C-E-R-E-R
bank flashers (6, 7) are placed on the table's light sources and stay observed.

## Flashers, eyes, GI and cabinet outputs

- **Flashers** on controlled solenoids, #63 flash lamps: 5 Demon background, 6 at the 3-bank, 7 at the
  S-O-R-C-E-R-E-R bank. The ROM flashes them with game effects (SORCERER completed: 7; lock and multiball: 5-8).
- **Flashing eyes (8).** Solenoid 8 drives relay 5580-08994-00, which flashes the Sorcerer's eyes in the back panel
  (IPDB: "glowing/flashing Sorcerer's eyes in back panel"); the game's solenoid table calls it "Flash Eyes
  (cabinet)". The ROM flashes it in bursts with game effects and never holds it through play. The coil parts list
  prints "Flipper-Enable Relay" for item 8 with the same relay part; on System 9 the flipper relay is K1 on the
  CPU board, driven with the game-on enable, so that label is a parts-list error. The known-working script drives
  back-panel eye flashers and a backbox flasher from 8.
- **General illumination (11)** energizes relay K1 on the power supply, which switches the 6.3 VAC GI strings.
  Public 1 means GI off. The ROM blinks it with effects.
- **Bell (15)** in the cabinet rings on 3-bank completion and with a credit award. **Coin lockout (16)**.
- **No knocker is fitted.** Solenoid 14 is "Not Used" in the solenoid table and the coil list, and the cabinet
  sheet ends SOL.14 at NC, but the ROM pulses 14 once with every credit award (about 0.1 s). The script's knocker
  sound on 14 is a recreation choice.
- Lamps 1-6 (Game Over, Match, Tilt, High Score to Date, Shoot Again, Ball in Play) and 56-64 (Backglass Effect
  and SORCERER art) are in the backbox.

## Attract, start and tilt

No solenoid moves during 40 s of attract mode. Credit button with a credit: the ROM sets the game-on enable 23,
resets the 3-bank (4) and serves a ball (2), with a GI blink. One closure of the playfield tilt (45) tilts the
ball at the factory adjustment (23 drops); the plumb bob (1) and ball-roll tilt (2) are cabinet tilts.

## Diagnostics

Manual-Down (-6 at 0) plus Advance (-7) enters the display test; Auto-Up and Advance then step Test 00 (sound),
01 (lamps), 02 (solenoids, shown in the credit display) and 03 (switches). In Test 02 the match display steps
01-16 and the shown solenoid pulses; the manual's "01 through 25 ... sub-test 25" is generic System 9 text that
this ROM does not follow. Specials are not stepped. In Test 03 the ball-in-play display shows each closed switch;
the ROM reports 1-45 (including the unfitted 41) and ignores 46-64.

## Edition and ROM differences

`sorcr_l1` and `sorcr_l2` share all game data; they differ only in the U19/U20 game ROMs. The L-1 solenoid test is
identical to L-2's. No other edition, conversion or community firmware exists in the pinned catalog.
