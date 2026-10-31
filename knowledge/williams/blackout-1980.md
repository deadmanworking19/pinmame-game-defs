# Blackout (Williams, 1980)

Coverage remains **partial**: every requirement except spatial placement is met. Addresses,
names, wiring, polarity, displays and mechanisms come from the instruction booklet and the
instruction manual and drawing set, the pinned PinMAME source, four retained runs of the `blkou_l1`
ROM and the two pinned corpus scripts. Placements are `observed` readings of one community table,
and no lamp has a placement.

## Identity

Williams game 495, IPDB 317, OPDB `GRwYo-MQoPw`, System 6. IPDB gives June 1980 and 7,050 units;
OPDB's `manufactureDate` 1980-06-01 agrees. OPDB's `display: alphanumeric` is wrong for this
machine: PinMAME declares six-digit seven-segment player displays and two-digit credit and
ball-in-play displays, and the booklet and the harness read only numerals from them. The
instruction booklet is 16P-495-103 (April 1980); the drawing set's cover reads 16P-495-101. IPDB
records that the playfield layout was reused for Rowamet's Heavy Metal and Taito do Brasil's Vortex,
and nearly so for Williams' Warlok; those are other machines.

Six drivers run on this one machine and share one game data block (`CORE_CLONEDEF` of `blkou_l1`),
so their addresses are identical. `l1` is the Williams production set; `f1` swaps in French speech
ROMs; `t1` swaps flipper ROM 2 for Ted Estes's `/10 Scoring` revision; each `ff` variant swaps
flipper ROM 1 for the community free-play fix. Only `blkou_l1` was run. The authorized ROM library also
holds `blkou_hf.zip`, byte-identical to `blkou_l1.zip`; no pinned driver is named `blkou_hf`, so it
is not a driver of this record.

## Controller and address dispositions

System 6 (`0x20000`), `s6_6digit_disp`. Switches and lamps number `(column - 1) * 8 + row`, which
the booklet's Figure 5 and Figure 6 follow.

- Service inputs: -7 Advance (7SW75) and -6 Auto-Up / Manual-Down (7SW74) on the coin door, wired
  to CPU connector 1J4; -5 the DIAGNOSTIC pushbutton and -3 MASTER COMMAND ENTER beside the
  Master Command switches behind the insert door; -4 the sound board's diagnostic pushbutton.
  Public -6 reads 1 for Auto-Up.
- Matrix switches 1-15, 18-23 and 25-45 are fitted (1-8 in the cabinet and on the coin door, the
  rest on the playfield). 16, 17, 24 and 47-64 are printed NOT USED, and the playfield switch
  sheet draws no contact for 16, 17 or 24; Test 03 still names a held 16, 17 or 24 because the ROM
  reports every closure it reads in columns 1-6.
- 46 is the playfield RIGHT FLIPPER LANE CHANGE SWITCH on the real machine, but PinMAME copies the
  right cabinet flipper button (82) into it on every update (`FLIP_SWNO(0,46)`), so a consumer
  drives 82. The left button (84) is copied nowhere. 81, 83 and 85-88 are unused.
- DIP 1 and 2 are the sound board's DS1 miniature switches, crossed against their printed numbers:
  the Sound Board Logic Diagram wires DS1 position 2 to IC10 PB5 and position 1 to PB6, an ON switch
  grounds its line, and PinMAME copies Sound Dip 1 and 2 uninverted onto PB5 and PB6. So public
  DIP 1 is switch 2, speech (0 enabled, 1 inhibited), and public DIP 2 is switch 1, the sound
  select (0 musical notes, 1 synthesized sounds). DIP 17, 18 and 19 are Master Command switches 8 (zero audit totals), 7 (restore factory settings) and 6
  (auto-cycle). 9-16 and 20-24 are unused.
- Every matrix contact is normally open: the switch sheets draw each as an open contact with a
  diode, the read path is not inverted, and Test 03 shows each held public 1. A drop target switch
  is closed while its target is down; each 3-bank also has a series switch (28, 36).
- Lamps 1-10, 12-49 and 56 are playfield inserts, one designated bulb each. 50-55 and 57-64 are
  insert board lamps in the backbox (62 Game Over, 63 Same Player Shoots and 64 High Score have two
  bulbs in parallel). 11 is not fitted: the lamp sheet leaves its cell blank.
- Solenoids 1, 4, 5, 6, 14, 16 and 17-21 are coils as Table 3 prints them; 9-13 are sound command
  lines to the sound board; 15 is the Special Relay; 2, 3, 7, 8 and 22 are printed Not Used and drawn
  N/C, and only the Solenoid Test pulses them. 23 is game-on: it pulls in the flipper relay Z1 and
  enables the specials. 45-48 are PinMAME's synthetic flipper states.

Four six-digit player displays map to controller indices 0-3 and the credit and ball-in-play
displays to 4 and 5. The booklet's tests show their number in the credit display and the function,
solenoid or switch number in the ball-in-play display, where the match digits also appear.

## Ball path and mechanisms

A drained ball rests on the outhole switch 9; the ball release 1 kicks it into the shooter lane and
the player plunges. No transcribed page counts the balls installed; the rules have no multiball,
both scripts load one ball, and the gameplay run served one ball at a time. Start fires game-on 23,
the 3-bank resets 4 and 5 and then 1; a drain fires 4, 5 and 1 again.

Two 3-banks of drop targets: the center bank (25-27, series 28, reset 4) below the bottom jet
bumper and the top bank (33-35, series 36, reset 5) at the upper right. Each reset raises its whole
bank. The ROM resets a bank when its series switch closes, not when the three target switches are
merely down. The center bank lights the eject hole red lamp; the top bank the yellow lamp and
BLACKOUT.

Five green standup targets (11 at the bottom to 15 at the top) light the eject hole green lamp.
The left spinner 18 and the upper right spinner 37 make the spinner loop, which collects and
advances the loop lamps 33-36; advancing past 20,000 lights the eject hole for Extra Ball. Standups
19 and 38 score 50.

Three jet bumpers (17 left, 18 right, 19 bottom) and two kickers (20 left, 21 right) are special
solenoids. Each has a scoring matrix switch (22, 21, 23, 44, 43) that PinMAME uses for the slot and
a separate direct-drive special contact (8SW65-8SW69, the kickers' drawn as two contacts in
parallel) that is not a public input. Slot 22 has no switch and no load.

Each flipper is one SFL-19-400/30-750-DC coil with an end-of-stroke contact across it, switched by
its cabinet button through Z1. PinMAME publishes 45/46 (right) and 47/48 (left) together while 23
is set; they model neither winding nor end of stroke. The right flipper is also the Lane Change:
the "1-2-3" lamps rotate when it is actuated. In the gameplay run the right button moved a lit
"1" to "2" and then "3".

## The Blackout sequence and the general illumination

The 6.3 VAC general illumination returns through a normally closed contact of the Special Relay
6L15, which solenoid 15 drives. That contact carries every G.I. output on the power sheet: the coin
door (7P1-2), the playfield (8P2-2) and the insert board (9P1-2, 9P1-5). Energizing 15 darkens all
of them. IPDB calls it the G.I. Relay on the backbox floor and says it cut the playfield lamps; the
power sheet shows the wider reach, and the record follows it. Most System 6 games feed their G.I.
from an unswitched winding, and System 6 publishes no G.I. channel; on Blackout the G.I. is an
ordinary solenoid output.

With the eject hole's green, yellow and red lamps lit, BLACKOUT 46 lights and doubles the eject
hole value. In the gameplay run a ball entering the eject hole then pulsed 15 seven times, the
fourth pulse holding it 2.30 s. Every lamp went out 0.09 s after the entry, lamps 1-64 then lit one
by one during the long hold, the coin lockout 16 dropped at 0.08 s and returned at 4.56 s, and the
eject kicker 6 fired at 5.09 s with lamps 43-46 out. Whether the sequence also runs without BLACKOUT
lit was not observed. The embedded script's `BlackoutMode = 1` (a 'fantasy mode' that keeps the
G.I. off until the drain) is the table's own option, not the machine.

## Sources that disagree, and what the record follows

None of these is a conflict: each is a wiring detail, a misprint, a label variant or a defect in
a consumed table.

- The playfield solenoid sheet labels the flipper coils the other way round from Table 3 (8L25
  RIGHT FLIPPER on BLU-GRY 8P3-4, 8L24 LEFT on BLU-VIO 8P3-3, 2P12-1 LEFT). Table 3, its note 2 and
  the cabinet sheet's 7SW72 RIGHT FLIPPER agree with each other, and the record follows them.
- Figure 5 prints switch 15 `5 BANK #5 (TOP)`; the chart and the wiring sheet call it a green
  target. The wiring sheet's matrix drawing omits 8SW39 although its own switch list carries 39.
- Figure 6 and the bulb list place the position qualifiers differently on lamps 23, 24, 31 and 32;
  Figure 6 prints lamp 44 YELLOW and the bulb list Amber.
- The booklet's Credit Posting paragraph ends 'coins are rejected while lockout is energized'; its
  own preceding sentence and the Test 02 run make the lockout energized while coins are accepted.
- The drawing set's foreword names IC14 and IC16 sockets where the booklet prints IC14 and IC26, and
  adds 'and magnet' to the F4 line; Blackout has no magnet.
- IPDB's G.I. relay sentence (above) and OPDB's display type.
- The embedded script comments out lamp 54 (Match), and SBR34 writes the lane-change switch 46
  directly; neither changes the machine.

## Runtime evidence

Four runs of the authorized `blkou_l1` ROM on the 46e1a01a LibPinMAME build, each in a fresh state
directory: an initialization run from empty CMOS (which stops in the diagnostic mode the drawing set
describes, credits 04, ball in play 00 and `1495 1`), then the Solenoid Test, the Switch Test and a
scripted game seeded from that run's NVRAM. Test 02 steps 01-22 pulse public 1-22 one at a time and
then wrap to 01, which pairs every printed solenoid number with its public address; Test 03 names
each held switch 1-46; the game exercises the coin, the start sequence, every special, both banks,
the lane change, the Blackout sequence, the outhole and the ball roll tilt. The compact evidence lives
in `evidence/runtime/system-6/blackout-1980.json`, and every display frame it cites is pinned in
`tools/seeds/williams/blackout-1980-display-readings.json`. A run shows what a public address does
under those conditions; it does not prove bulb counts or locations.

## What would complete this record

Spatial placement is the one open requirement:

- Lamps 1-10, 12-49 and 56 have no placement. The retained table draws every insert as a light with
  no bulb, which marks no socket, and has no light for 56; no lamp-location drawing was measured. A
  table that models the bulbs, or a measured factory playfield drawing, would supply them.
- Switches 9, 19, 32 and 38 and solenoid 1 have no defensible position in the retained table; the
  spatial report gives the reason for each.
- Every placement is `observed` from one community table that is not known to have been played.
  Measuring the callouts of Figure 3 and Figure 4 against the table would validate them.
