# Centaur — Solenoid Expander A15 (W-1251-1 b)

Transcribed from `Centaur 2 Schematics.pdf`, PDF page 15, the sheet titled
`SOLENOID EXPANDER (SCHEMATIC)`, assembly `AS-2518-66`, part number `W-1251-1 b`, game `# 1239`,
drawn 10-5-81. Game 1239 is Centaur: the Centaur II schematic set reprints the Centaur prints. The
accompanying crop is the board and J1 region, rendered from the page's native scan.

The Centaur manual's own copy of this board, PDF page 57 of the installation manual, is the generic
sheet `W-1251 b` for game `1220`. It draws the same circuit but labels J1-2 `LAMP DRIVER SCR` and
leaves the relay contacts unconnected. The game-1239 sheet is the one that says how Centaur wires it.

## Board

Relay `K1` with diode `CR1` across its coil. One end of the coil is on `J1-9 +43 VDC`; the other
end returns to ground (`J1-3 GND`) through the triac of optocoupler `U1` (`MOC 3011`). The
optocoupler's LED runs from `J1-1` through `R1 330 Ω` to `J1-2`. The relay has a changeover
contact: common on `J1-4`, one side on `J1-7` and the other on `J1-5`.

## J1, as the game-1239 sheet wires it

| J1 pin | printed |
| ---: | --- |
| 1 | SWITCHED ILL. BUSS |
| 2 | A3J5-14 |
| 3 | GND |
| 4 | A2J1-9 |
| 5 | to one end of the coil `BALL KICK COIL TO PLAYFIELD`, whose other end is `+ 43` |
| 6 | KEY |
| 7 | N/U |
| 9 | + 43 VDC |

## What it means

`A3J5-14` is the solenoid driver output for self-test number 15, Ball Kick to Playfield, on
transistor Q11: the German edition of the Centaur manual prints `15 Autom. Kugelauswurf Q11 J5-14`
in its solenoid identification table, and PinWiki's Centaur solenoid chart gives the same coil
`A15J1-5 / A3J5-14` and `Q11` with the note that the kick goes through the solenoid expander first.
The English table prints names only. The ROM's solenoid self test pairs printed 15 with public
solenoid 14. When the ROM fires public 14, Q11 sinks the switched illumination supply through the
optocoupler's LED, the triac energises K1, and the relay's contact joins the ball-kick coil's
switched end (J1-5) to `A2J1-9`, which completes the coil's circuit from `+43`. The ball kick is
therefore driven through a relay rather than directly by a driver transistor; public 14 still
fires it, a relay pull-in later.
