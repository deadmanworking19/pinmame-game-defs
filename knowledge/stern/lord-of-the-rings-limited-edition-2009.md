# Lord of the Rings Limited Edition (Stern, 2009)

Coverage: **partial - identity, driver and controller platform only.** No switch, output, display or mechanism is enumerated yet, and nothing here is placed. The 2003 production machine, `stern.lord-of-the-rings.2003`, is the fully curated record this edition descends from.

## Identity

IPDB 5558 (`ipdb-5558` excerpt) lists The Lord of the Rings (Limited Edition) as a Stern game of December 2009, model number I-00B4, on a "Stern Whitestar (modified)" MPU, about 500 units, and calls it the "Limited Edition version of Stern's 2003 'The Lord of the Rings'". OPDB's record `GrqZX-MDEPd`, "Lord of the Rings (LE)", carries the same IPDB number; the 2003 machine is `GrqZX-MD15w`. The year here is the physical build year. PinMAME's catalog dates the `lotr_le` firmware 2008, and that date stays on the driver.

PinMAME has one driver for this edition, `lotr_le` (10.02). It is declared a clone of `lotr` and shares `init_lotr`, so the emulator routes it exactly like the 2003 firmware. Against that machine's root driver it changes only the CPU game ROM, `lotrcpua.a02` for `lotrcpua.a00`, and keeps the display ROM `lotrdspa.a00` and the `LOTR_SND` set (`src/wpc/segames.c:1852-1858`).

## Why this is its own record

Shared routing does not make shared hardware, and three independent kinds of evidence say the hardware changed:

- **The factory list.** IPDB's list of factory changes includes "Game has the option to add a Shaker Motor", which the 2003 game never had, and quotes Lonnie Ropp's confirmation that the shaker code was added to the original code and secured with a new PAL chip version.
- **An owner's first-hand report** (`owner-shop-out-matrix-2010` excerpt). The owner of an LE wrote in October 2010 that the cabinet chart Stern stapled into the LE was the 2003 one and was wrong for that game: "wire colors and 2 solenoids positions were changed". The post names the I/O power driver board as a Stern 520-5249-00 (the board it calls "Sam"), fed through a "Z" connector that converts J10 to the new positions, and the CPU/Sound II board as a 520-5300-00 Rev A. The owner's corrected chart prints coil #12 as OPTIONAL SHAKER MOTOR, #14 as NOT USED NC J9-P7 and #28 as FLASH: HELMS DEEP RT on Q28. The note under that chart's flasher rows still lists the 2003 flash-test set (Q14, Q23, Q25-Q27, Q29-Q32): it was not updated with the rows above it.
- **The firmware.** A hash-pinned run of 10.02's own flash-lamp test (`evidence/runtime/whitestar/lord-of-the-rings-limited-edition-flash-test.json`) pulses solenoids 14, 23 and 25-32 on every cycle. The same walk on the 2003 firmware 10.00 (`evidence/runtime/whitestar/lord-of-the-rings-flash-test.json`) pulses 14, 23, 25-27 and 29-32 and never 28. So 10.02 drives the Limited Edition's right Helm's Deep flasher at 28 and keeps driving 14, which is where the 2003 machine wires the same flasher.

The owner's report and corrected chart are one person's first-hand account, not a factory document. They agree with each other, with IPDB's shaker option and with the firmware, but the factory LE documentation the owner refers to - an LE manual and a 520-5249-00 schematic - was not retrievable, so the I/O board identity and the changed wire colours rest on the owner alone.

## What else IPDB lists as different

Real-glass backglass with a mirrored gold effect; extra clearcoats on the playfield; no 'Armies of Middle Earth' plastic figures, and no mounting holes for them in the playfield plastics; a playfield signed by Gary Stern and George Gomez; plated and polished lockdown bar, legs, hinges and side rails, gold trim around the backbox, brass-plated leg and hinge bolts; a "500 Game Limited Edition" plate and gold-painted grilles on the speaker panel; a certificate of authenticity signed by Gary Stern.

## What remains

- Enumerate the switches, lamps, solenoids, displays and mechanisms. The 2003 record is the natural starting point, but every address has to be confirmed for this edition, starting with 12, 14 and 28 above and the lamp-matrix wire colours the owner says changed.
- Find the factory LE documentation: the LE manual and the 520-5249-00 I/O power driver board schematic.
- Establish whether anything on the playfield moved. Nothing retained says it did, but nothing retained has been compared against an LE playfield either.
