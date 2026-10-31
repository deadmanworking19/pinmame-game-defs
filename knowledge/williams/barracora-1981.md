# Barracora (Williams, 1981)

Coverage remains **partial**: every requirement except spatial placement is met. Addresses,
names, wiring, polarity, displays and mechanisms come from the instruction booklet, the drawing
set and the parts supplement, the pinned PinMAME source, four retained runs of the `barra_l1` ROM
and the pinned VR Room script. Placements are `observed` readings of one community table, and no
lamp has a placement.

## Identity

Williams game 510, IPDB 177, OPDB `GRo7K-MQ4e3`, System 7. IPDB gives September 1981 and 2,350
units; OPDB's `manufactureDate` 1981-01-09 agrees on the year only. OPDB's `display:
alphanumeric` is wrong for this machine: the insert board sheet draws seven-digit numeric player
displays and a credits / ball-in-play board. The instruction booklet is 16P-510-103 and the parts
supplement 16P-510-110 (October 1981). IPDB's notes record that the game was renamed from
'Las Vegas' to 'Jet Orbit' to 'Barracora', which they give as the reason two letters share one
insert (the RR lamp, public 11).

`barra_l1` is the only driver. Its ROM members match pinned `s7games.c`, and the parts supplement
lists Sound ROM 4, which matches `sound4.716`. The source comments mention a tournament ROM mod and
a 2x/3x playfield multiplier mod; neither is a driver and neither is covered.

## Controller and address dispositions

System 7 (`0x10000`), `s7_dispS7`. Switches and lamps number `(column - 1) * 8 + row`, which the
lamp sheet's numbers 01-64 and the switch matrix's printed numbers follow.

- Service inputs: -7 Advance (7SW75) and -6 Auto-Up / Manual-Down (7SW74) on CPU connector 1J4;
  -5 the CPU board's DIAGNOSTIC pushbutton (NMI); -4 the sound board's SW1. -3 Master Command
  Enter is optional emulator input: no such control is drawn in the cabinet wiring or the CPU
  board assembly view.
- Matrix switches 1-48 are fitted (1-8 in the cabinet, 9-48 on the playfield); 49-64 are printed
  NOT USED and columns 7 and 8 end at playfield pins printed NC.
- 34 and 35 are the playfield lane-change contacts on the real machine, but PinMAME copies the left
  (84) and right (82) cabinet flipper buttons into them on every update (`FLIP_SWNO(34,35)`), so a
  consumer drives 84 and 82. 81, 83 and 85-88 are unused.
- DIP 1 and 2 are positions of the sound board's 2-position DS1. DIP 9-24 are PinMAME's
  Master Command F and D bits, read only while -3 is held. The CPU bill of material lists DS1 and
  DS2 (two 8-position DIP switches), but the assembly view of the same drawing shows neither, and
  the booklet never uses them; they stay optional.
- Every matrix contact is normally open: the switch sheet's TYPICAL cell is an open contact with a
  diode, the cabinet sheet draws 7SW1-7SW8 open, the read path is not inverted and Test 03 shows
  each held public 1. A drop target switch is closed while its target is down.
- Lamps 1-64 are all fitted. 1-6 (Same Player Shoots Again, Ball in Play, Tilt, Game Over, Match,
  High Score to Date) are insert board lamps in the backbox; 1 has two bulbs in parallel. 7-64 are
  playfield inserts. 65-96 are unused auxiliary columns.
- Solenoids 1-22 are fitted as Table 4 prints them. 23 and 24 are special slots with no driver or
  load; the Solenoid Test sweeps them. 25 is game-on: it drives the flipper relay Z1 and enables
  the specials. 45-48 are PinMAME's synthetic flipper states. 51-60 are unavailable, and 26-44 and
  49-50 are transport holes with no device.
- System 7 publishes no G.I. channel, and on this game nothing on the CPU side switches the 6.3 VAC
  general illumination: the power board's K1 special relay has all its coil pins printed N.C.,
  so its contact stays as drawn, closed. The sheets draw G.I. strings on the playfield, the
  cabinet and the insert board with continuation dashes and print no bulb count.
- The coin door's 7SW76 Memory Protect Interlock (CPU connector 1J4-1) has no PinMAME input.

Four seven-digit player displays map to controller indices 2, 3, 0 and 1, and the credits and
ball-in-play digits to 6/7 and 4/5. The booklet's "Match display" is the ball-in-play display.

## Ball path and mechanisms

Three balls. A game starts only with all three on the ball ramp switches 13, 14 and 15 or, at most
one, in the shooter lane on 16. Start fires game-on 25, bank releases 9 and 10, target resets 1-8
in order and the ball ramp thrower 12, which serves the ball resting on 15 into the shooter lane.
The player plunges. A drain closes outhole 12, and ball release 11 kicks the ball onto the ball
ramp. The Williams name `Ball Release` is the outhole kicker 11; the corpus scripts call the
thrower's kicker `BallRelease`.

The B-A-RR 3-bank (41-43) and A-C-O-R-A 5-bank (44 at the top to 48) each have one reset coil
per target (1-3, 4-8, raising it) and a bank release (9, 10, dropping the bank). The ROM raises a
target hit out of sequence at once, and raises a completed bank one target at a time from the
last letter back, with no bank release. Bank completion advances the bonus multiplier and lights
an eject-hole lock arrow; both banks together advance the super bonus multiplier.

Two kick-out holes on the left: upper eject hole 10 with kicker 13 and lower eject hole 11 with
kicker 14. A ball locked in a lit hole is replaced by a new ball from the thrower (0.18 s after
10 closes, 3.09 s after 11 closes in the gameplay run). Locking upper then lower gives 3-ball
Multi-Ball, lower first only 2-ball. The upper hole's gate 17 is a Ball Gate Lock Assembly (coil,
armature and return spring). The ROM holds 17 on in play, drops it while a ball is locked in the
upper hole, and turns it back on just before 13 releases the ball; the VR Room script opens the
table's gate while 17 is on. The retained pages do not draw the gate's swing.

Three jet bumpers (18 left, 19 right, 20 bottom) and two kickers (21 left, 22 right) are special
solenoids. Each has a scoring matrix switch (20, 21, 22, 29, 30) that PinMAME uses for the slot,
and a separate direct-drive special contact (8SW66-8SW70) that is not a public input. Slot 17 is
the gate, which has no special switch (its special-switch wire ends at a pin printed NC).

Each flipper is one SFL-19-400/30-750-DC coil, switched by its cabinet button through Z1 and with
its own flipper contact (8SW45 left, 8SW46 right). PinMAME publishes 45/46 (right) and 47/48
(left) together while 25 is set; they model neither winding nor end of stroke.

The top lanes 17, 18 and 19 light lamps "1"-"3", or "4"-"6" beneath an already lit one, and the
flipper buttons rotate them. The booklet says the right button rotates 1-3 "from right to left"
and the left button 4-6 "from left to right". In the gameplay run the right button moved a lit
"1" to "2"; in the retained table lane 1 is the leftmost, which would make that move left to
right. The lanes' order is not measured on a factory drawing, so the record follows the ROM and
leaves the prose's direction as a note.

## Sources that disagree, and what the record follows

None of these is a conflict: each is a wiring detail, a misprint or a defect in a consumed table.

- Table 4's first row `01 Top Eject Hole ... SG-23-850-DC` repeats solenoid 01's wiring; Figure 2,
  the solenoid sheet and Test 02 give 01 as the B Drop Target Reset. Table 4 prints 03 without its
  8P3 pin; the solenoid sheet gives 8P3-3.
- The solenoid sheet names 13 TOP LEFT CORNER EJECT HOLE, 14 UPPER LEFT EJECT HOLE and 17 TOP EJECT
  HOLE GATE; Table 4 and Figure 2 say Upper Eject Hole, Lower Eject Hole and Upper Eject Hole Gate.
  The record uses Table 4's names.
- The cabinet sheet's SOL. 14 branch to 7P1-3 (NC) and its flipper-coil pins 8P3-3/15/4/9 do not
  match the playfield sheet and Table 4, which the record follows.
- F4 is 10A in the booklet and on the power sheet, 20A SB in the drawing set's foreword.
- The lamp sheet's bulb list skips 57; its own matrix and Figure 1 fill the cell (Bonus 4). It
  also prints the column-1 asterisk beside cell 07, which reads PLAYFIELD. The insert board prints
  row 5's wire `REN-GRN`.
- Figure 5 prints 11 as `LOWER / HOLE`. The chart calls 38 `LOWER STANDUP`, but its contact is on
  the left side beside the upper playfield in the retained table and on Figure 3.
- The Dids666-lineage scripts open the gate from 17 and never close it, define `sw18_Hit` three
  times, and both corpus scripts write the lane-change switches 34 and 35 directly; none of this
  changes the machine.

## Runtime evidence

Four runs of the authorized `barra_l1` ROM on the 46e1a01a LibPinMAME build, each in a fresh
state directory: an initialization run from empty CMOS (which stops in the Diagnostic Mode the
drawing set describes), then the Solenoid Test, the Switch Test and a scripted game seeded from
that run's NVRAM. Test 02 steps 01-25 pulse public 1-25 one at a time, which pairs every printed
solenoid number with its public address; Test 03 shows each held switch 1-48 and nothing for
49-64; the game exercises the start sequence, every special, both banks, both locks, 3-ball
Multi-Ball, the outhole and the ball roll tilt. The compact evidence lives in
`evidence/runtime/system-7/barracora-1981.json`, and every display frame it cites is pinned in
`tools/seeds/williams/barracora-1981-display-readings.json`. A run shows what a public address
does under those conditions; it does not prove bulb counts or locations.

## What would complete this record

Spatial placement is the one open requirement:

- Lamps 7-64 have no placement. The retained table draws every insert as a light with no bulb,
  which marks no socket, and no lamp-location drawing was measured. A table that models the bulbs,
  or a measured factory playfield drawing, would supply them, together with the socket count of
  each insert.
- Switches 12-15 (outhole and ball ramp) and 36-40, and solenoids 11 and 12, have no defensible
  position in the retained table; the spatial report gives the reason for each.
- Every placement is `observed` from one community table that is not known to have been played.
  Measuring the callouts of Figure 2 and Figure 3 against the table would validate them.
