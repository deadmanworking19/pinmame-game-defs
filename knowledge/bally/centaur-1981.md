# Centaur

Coverage: **author_ready**

Bally game #1239, 1981, IPDB 476. Four-player, five-ball, black-and-white playfield with a
Squawk & Talk speech board. This is the project's first Bally MPU AS-2518-35 machine, so it
introduced the `pinmame.by35` controller profile that every later BY35-driver machine should reuse.

## Physical family

`centaur` is the 1981 production ROM. `centaura` (2004) and `centaurb` (2008, rev. 27) are the
Bally/Oliver free-play ROMs: later firmware for the same physical machine, not new games. Their
release years do not create new physical titles.

`centauri` and `centaurj` are Inder's unrelated 1979 Spanish machine. They share only the name and
must stay a separate record.

## The solenoid numbering trap

This is the fact most likely to be got wrong, and it is worth stating plainly because the available
sources state it three different ways.

The manual's solenoid identification table is headed **"Self Test #"**. That column is the order in
which the ROM's solenoid test pulses each coil. It is *not* the PinMAME public solenoid address.
PinMAME writes a four-bit selector to PIA1:B and sets bit `selector`, so the public address is
`selector + 1`, and the ROM's test order is unrelated to that.

Printed page 13 gives the way to resolve it:

> Pressing the Self-Test button again causes each solenoid to be energized, one at a time, in a
> continuous sequence. ... The number appearing on the Player Score displays is the same as the
> number assigned to the solenoid.

Booting the ROM and watching that test therefore publishes the mapping directly, and it is the
mapping the definition carries:

| Self test | Device | Public address |
| ---: | --- | ---: |
| 01 | Outhole kicker | 7 |
| 02 | Knocker | 6 |
| 03 | Inline drop target reset | 8 |
| 04 | 4 right drop target reset | 9 |
| 05 | Left thumper bumper | 10 |
| 06 | Right thumper bumper | 11 |
| 07 | Left slingshot | 12 |
| 08 | Right slingshot | 13 |
| 09 | ORBS target reset | 1 |
| 10 | Right 4 drop target "1" (top) | 2 |
| 11 | Right 4 drop target "2" | 3 |
| 12 | Right 4 drop target "3" | 4 |
| 13 | Right 4 drop target "4" (bottom) | 5 |
| 14 | Ball release | 15 |
| 15 | Ball kick to playfield | 14 |
| 16 | Coin lockout door | 18 |
| 17 | K1 relay (flipper enable) | 19 |
| 18 | Magnet | 20 |

Three traps follow:

1. **Printed 14 and 15 are transposed against public 14 and 15.** The numbers collide but the
   devices swap. Ball release is public 15; ball kick to playfield is public 14.
2. **Public 7 is the outhole kicker.** Both retained community scripts label it a release to the
   shooter lane (`SolBallRelease`, `SRelease`), so the community naming is wrong here.
3. **Public 17 is the sixth switch-column strobe, not a coil.** The identification table accounts
   for only three continuous devices, at printed 16, 17 and 18, which are public 18, 19 and 20. The
   ROM asserts public 17 and never releases it, so it is not an empty slot either. It is resolved as
   ST5 on converging grounds: 48 switches is six columns while PIA0:A supplies five strobes and the
   schematic shows ST5 originating at a different MPU connector; PinMAME's LISY bridge special-cases
   Centaur (`lisy35.c` case 7) and masks that bit out of the coil data as a strobe line; and the
   trace shows it asserted continuously once scanning starts, which is exactly how a strobe looks
   through `by35.c`, which OR-accumulates solenoid state within each VBLANK window. Do not read the
   absence of a *pulse* on a continuous output as evidence that it is unused - a held line never
   pulses. Kiss corroborates the reading from the other direction: it is a five-column game, does
   not need a sixth strobe, and uses public 17 for a real playfield coil.

The continuous assignments are independently confirmed by PinMAME's own LISY bridge, which drives
real Bally hardware from this driver and names continuous bit 1 the coin lockout and bit 2 the
flipper-enable relay - public 18 and 19.

The legacy import this record grew from had two defects that the self test exposes: it omitted
public solenoid 4 entirely, which shifted the right four-bank labels by one and left address 5
carrying the label for target "3", and it had no magnet at all.

### The ball kick goes through a relay

The ball kick to playfield coil is the one coil the solenoid driver does not fire directly. Its
driver output, A3J5-14 on transistor Q11, runs to the **Solenoid Expander A15** (AS-2518-66): there
it lights the LED of a MOC 3011 optocoupler from the switched illumination supply, the optocoupler's
triac energises the 48 V relay K1, and K1's contact completes the kick coil's circuit from +43 V.
Centaur's own print of the board (drawing W-1251-1 b, game 1239, reprinted in the Centaur II
schematic set) wires it that way; the generic copy in the Centaur manual leaves the contacts
unlabelled. For a recreation, public 14 still fires the kick, one relay pull-in later than a directly
driven coil.

## Flippers

Centaur's flipper coils are switched by the K1 relay rather than by a driver-board output, which is
why they carry no solenoid number of their own and why energising that relay is effectively the
game-on signal. The retained standalone script uses public 19 exactly that way, for nudge handling.
Both flipper buttons are wired to the single matrix address 21, so both buttons do the same thing:
in play, each press moves the lit top lane one place. PinMAME also maintains a generic
flipper-button column at 81-88, but Centaur declares `FLIP_SW(FLIP_L)` with no `FLIP_SWNO`, so
`FLIP_SWL` and `FLIP_SWR` are zero, `core_updateSw` never copies that column into the game matrix,
and the ROM - which strobes only columns 1-6 - never reads it. Those addresses are not a mirror of
21 and nothing populates them; they are retained only because the legacy corpus bound them.

## Shared switch addresses

Centaur wires several physical contacts in parallel onto one address, so a recreation cannot tell
which one closed. The manual prints the quantity in parentheses:

- **12** - the top left lane rollover button, the ORBS two back targets, and the target behind the
  right thumper bumper: three printed descriptions, four physical devices, one address.
- **15** Tilt (3), **16** Slam (2), **18** Left side rollover button (2), **34** 10 point rebound (5).
- **21** - both flipper buttons.

The five 10 point rebounds are the two rubber faces of each side triangle and one rebound at the
upper right, as Figure V draws them. The retained table models each triangle's two faces as one
chevron-shaped sensor wall, so each face is placed at the centroid of its arm of that wall.

Matrix positions **07, 13, 14, 23, 35 and 36** are printed blank: the positions exist, Centaur wires
nothing to them. The seven label conflicts this record inherited from the two legacy sources are all
resolved from the manual, and in every case the platform-level source was right and the game-level
source wrong. Position 07 is the exception where neither was right: one called it Tilt, the other
left it generic, and the manual prints nothing there because tilt is position 15.

## Displays

`dispBy7`: four seven-digit player score displays and two two-digit displays for credits and for
match/ball-in-play. The parts list matches, with one AS-2518-54 and four AS-2518-58 display driver
modules. PinMAME also publishes a seventh display, a 128x32 composite it renders from the segment
data; that is an emulator artifact and not a physical device, so the definition declares six.

## Lamps

The AS-2518-23 lamp driver module carries sixty outputs, and its parts list counts exactly sixty
SCRs. PinMAME's lamp strobe ignores the decoder selector value 0x0f and advances two matrix columns
per data bit, so the public addresses are 1-15, 17-31, 33-47 and 49-63. Note that the skipped value
is a *selector*, not a public address: public lamp 15 is a real, addressable output. What the skip
produces is the gaps at 16, 32, 48 and 64, which are unreachable decoder slots rather than unused
lamps.

Public lamp 1 is not a lamp: its SCR feeds the **Aux. Driver (G.I. Flasher)** A17 (AS-2518-68),
whose optocoupler fires a triac on the power module that flashes the playfield general
illumination. The retained table models that by flashing its upper G.I. from address 1.

Centaur also carries an **Auxiliary Lamp Driver A9** (AS-2518-43), which `centaurGameData` declares
as `lampCol = 8`. That reserves a second board's worth of addresses at 65-79, 81-95, 97-111 and
113-127, of which only sixteen are reachable: 65-68, 81-84, 97-100 and 113-116.

The board's schematic is printed in the Centaur manual itself, on page 51 of the *Installation and
General Game Operation Instructions* (drawing W-1207-11). Each lamp data line enables one MC14555B
decoder half - PD0 to U2A, PD1 to U2B, PD2 to U3A, PD3 to U3B - and the two latched address bits
select Q0, Q1 or Q2 of that half. **Q3 is marked N/U on all four halves**, which is why four halves
times three outputs is the twelve SCRs the parts list counts, and why latched address 3 reaches no
bulb on any data line. Public 68, 84, 100 and 116 are therefore bare matrix positions with no socket
behind them. The retained community table drives playfield star inserts from three of those
addresses; that is the table author's invention, not something the board can light.

| public | decoder | SCR | A9J2 | wire | what it lights |
| --- | --- | --- | --- | --- | --- |
| 65 | U2A Q0 | Q6 | 7 | 54 | top **right** lane (printed TOP LEFT LANE) |
| 66 | U2A Q1 | Q5 | 6 | 45 | right slingshot |
| 67 | U2A Q2 | Q4 | 5 | 60 | #1 chamber, from the bottom, two bulbs |
| 81 | U2B Q0 | Q1 | 1 | 43 | top middle lane |
| 82 | U2B Q1 | Q2 | 2 | 40 | left slingshot |
| 83 | U2B Q2 | Q3 | 3 | 62 | #2 chamber, two bulbs |
| 97 | U3A Q0 | Q12 | 18 | 25 | top **left** lane (printed TOP RIGHT LANE) |
| 98 | U3A Q1 | Q11 | 19 | 82 | right thumper bumper |
| 99 | U3A Q2 | Q10 | 20 | 95 | #3 chamber, two bulbs |
| 113 | U3B Q0 | Q7 | 11 | none | nothing: the circuit is built but unwired |
| 114 | U3B Q1 | Q8 | 12 | 27 | left thumper bumper |
| 115 | U3B Q2 | Q9 | 17 | 96 | #4 chamber, top, two bulbs |

The sheet prints `(2)` against the four chamber circuits and against nothing else, the same way the
switch table prints its quantities, and PinWiki's chart reads "Chamber #1 (2 lamps)". Each chamber
circuit lights a pair of bulbs on either side of the Queen's Chamber lane at the top left; every
other auxiliary circuit lights one. The retained table agrees: its script drives two bulb meshes
for each chamber address and one for each slingshot.

### The outer top lanes are labelled the wrong way round on the print

The A9 sheet prints TOP LEFT LANE against A9J2-7 (public 65) and TOP RIGHT LANE against A9J2-18
(public 97), and the harness drawing W-1255-2 copies those labels. The ROM disagrees, and the ROM is
what the physical machine runs. In play it lights 97 when the top left lane rollover closes, 81 for
the middle lane and 65 for the right lane; the switch identification table and the Figure V location
drawing both put switch 5 at the left lane and switch 3 at the right. A lit top lane is a made lane,
so 97 is the left lane's lamp and 65 the right's. The same run confirms the rest of the board's
decoding from the ROM side: a struck right slingshot flicks 66, the left 82, the right thumper bumper
98 and the left 114, each the lamp the sheet prints on that row. So it is only the two outer top-lane
labels that are transposed on the print, not the derivation.

The retained tables bind 97 to the left insert and 65 to the right, above their own switch-5 and
switch-3 rollovers. An earlier pass of this record read the print as ground truth and called the
tables wrong; the ROM shows they are right. A photograph of a Centaur's top-lane sockets from below
(Pinside thread 303903, post 4) shows the blue-white circuit (A9J2-18) on the left-hand socket and the
white-green circuit (A9J2-7) on the right, consistent with the ROM, though the photograph is too dim
to decide it alone.

### Lamp 113 is a built but unwired circuit

A9J2-11 is driven by U3B Q0 through SCR Q7 like its eleven siblings, and the board side of the sheet
prints no function against it while marking the genuinely unused pins N/U. The harness side of the
same sheet settles what the blank means: it draws a cable branch, with a wire-colour code, on exactly
the eleven pins that print a function and none on pin 11. A photograph of a Centaur's own A9 board
(Pinside thread 303903, post 4) shows the same: wires at those eleven positions, none at 11. PinWiki's
chart has no description, code or colour for it, and the German manual's A9 troubleshooting table
omits Q7 altogether.

The harness drawing W-1255-2 prints a wire code against A9J2-11, but none of its unlabelled rows can
be read as this board: it also lists wires on an A9J3 connector the AS-2518-43 does not have and on
the J2 key and ground positions. It reads as a template for a larger auxiliary board, which fits the
German manual's parts list naming the 28-output AS-2518-52 for A9.

What PinMAME publishes at 113 is explained by the ROM rather than by a lamp. The three top-lane lamps
are three bits of one four-bit lamp-data value (latched address 0 on PD0, PD1 and PD2), and 113 is
its fourth bit, PD3. The lane change rotates that value: the lit lane steps 65, 81, 97, and when it
wraps from 97 back to 65 the carry lands in 113, which rises with 65 and falls with it on the next
press. Apart from that, 113 changes only in the power-up and game-start lamp flashes that write
whole lamp lines. A bulb wired there would light whenever the lit lane had just wrapped, which is
presumably why Bally left the pin unconnected. A recreation should bind nothing to 113.

An earlier draft of this record placed 113 at the centroid of the three top-lane inserts and called
that validated; it was never observed, and it was withdrawn before this resolution.

## Spatial placement

All placements come from the retained known-working table *Centaur (Bally 1981) v2.0.0*, taken from
the objects its script binds, and are reconciled against Figure V and the board sheets:
`reports/spatial/bally/centaur-1981.md` lists them. The slingshot lamps are the table's bulb meshes
under each slingshot plastic, because its light objects for 66 and 82 are invisible placeholders in a
row along the bottom edge; the thumper-bumper lamps are the bumper centres; each chamber pair is the
two bulbs the table drives for that address.

## Sound

Squawk & Talk (`SNDBRD_BY61B`). PinMAME carries a Centaur-specific `BY35GD_REVERB` flag, documented
in `by35.h` as the speech-reverb flag for this game, alongside `BY35GD_NOSOUNDE`. Centaur's growling
speech is the reason that flag exists. The manual's Say It Again module (AS-2518-81) is that reverb.

## What rests on reasoning

**Option switches 17-20 come from community documentation.** The printed credits-per-coin tables
cover chutes 1 and 3, on switches 1-5 and 9-13, and omit the centre chute even though the machine
has one - switch 11 is Coin II (Middle). The option-switch documentation carried identically by all
four retained tables, from 2020 to 2025, assigns 17-20 to it, and that documentation agrees with the
printed manual on every one of the 28 switches the manual does document. Note the asymmetry: the
outer chutes use five selector switches each and the centre chute four.

**The top-lane labels rest on the ROM's game logic.** The record follows the ROM's pairing of each
lane rollover with its lamp over the print's labels, for the reasons above. Rolling a ball through
the left top lane of a real machine and watching which insert lights would show it directly.

Searched in reaching this state: all three Centaur manuals, the Centaur and Centaur II schematic
sets, the Kiss manual with its schematic-omissions supplement, the Kings of Steel schematics,
archive.org, PinWiki, Pinside, and four independently authored VPX recreations spanning fifteen
years. The A9 schematic was found in the Centaur manual itself after an earlier pass had concluded
it was absent and had fallen back on the Kings of Steel sheet; the boards are identical, but the
Centaur print carries the per-pin lamp functions that the Kings of Steel print does not.
