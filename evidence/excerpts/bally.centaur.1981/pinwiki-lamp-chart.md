# Centaur — auxiliary lamp chart rows

Transcribed from the Centaur lamp chart as reproduced on PinWiki
(<https://pinwiki.com/wiki/index.php/Centaur>).

**Secondary source**, recorded because it reproduces the primary AS-2518-43 schematic on this
machine, adds the colour of each wire code, and leaves the same pin blank.

| SCR | connector | lamp | code | wire colour |
| --- | --- | --- | --- | --- |
| Q06 | A9J2-7 | Top Lane Left | 54 | Wht-Grn |
| Q05 | A9J2-6 | Slingshot Right | 45 | Grn-Wht |
| Q04 | A9J2-5 | Chamber #1 (2 lamps) Bottom | 60 | Brn |
| Q01 | A9J2-1 | Top Lane Middle | 43 | Grn-Yel |
| Q02 | A9J2-2 | Slingshot Left | 40 | Grn |
| Q03 | A9J2-3 | Chamber #2 (2 lamps) | 62 | Brn-Blu |
| Q12 | A9J2-18 | Top Lane Right | 25 | Blu-Wht |
| Q11 | A9J2-19 | Thumper Bumper Right | 82 | Blk-Blu |
| Q10 | A9J2-20 | Chamber #3 (2 lamps) | 95 | Gry-Wht |
| Q07 | A9J2-11 | *(no description listed)* | — | — |
| Q08 | A9J2-12 | Thumper Bumper Left | 27 | Blu-Orn |
| Q09 | A9J2-17 | Chamber #4 (2 lamps) Top | 96 | Gry-Brn |

All twelve are marked as located on the Aux. Lamp Driver Module A9 and use MCR-106 SCRs.

## What it corroborates

Its SCR-to-pin column reproduces the primary schematic exactly on all twelve circuits, and its code
and colour columns agree with the wire codes the schematic's harness list draws at each pin, so it
decodes those codes into colours.

## What it does not add

Its function names are the schematic's, copied: it prints `A9J2-7` as the left top lane and
`A9J2-18` as the right, the labels the ROM's lane logic shows to be transposed, so it is not an
independent check of them.

`A9J2-11` has no description, code or wire colour here, which agrees with the schematic's harness
list: no wire is fitted at that pin.
