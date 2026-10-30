# Scared Stiff (D.01R Prototype) (Bally, 1996)

Coverage: **partial - identity, driver grouping and WPC-95 platform only. No input, output, display or
mechanism inventory is recorded yet.**

This record holds the two D.01R prototype drivers of the `ss_*` clone tree, `ss_01` (Scared Stiff
(D.01R Prototype, Sound 0.25)) and `ss_01b` (Scared Stiff (D.01R Prototype Coin Play, Sound 0.25)).
They were split from the production record `bally.scared-stiff.1996` because their firmware needs
hardware a production machine does not carry. `tools/curate_scared_stiff.py` writes and checks it.

## Why the prototype is its own record

Pinned PinMAME's `ss.c` declares `hw.lampCol = 2`, "2 extra lamp columns for the LEDs of rev. 0.1",
fed through two HC4094 shift registers clocked from solenoids 37 (Aux Lamp Clock) and 38 (Aux Lamp
Data), and says "Prototype 0.1 had a 16 LED Skull driver board assembly A-20781 which was not kept in
production build". Midway's own 1996 development notes say the skull pile's eyes "originally had red
LEDs", that rolling a skull lane lit one pair and lighting all six pairs awarded Return Of The
Deadheads, and that "the LEDs had to be removed because of cost issues"
(`evidence/excerpts/bally.scared-stiff.1996/development-notes-pile-o-skulls.md`).

In the retained harness probe (`evidence/excerpts/bally.scared-stiff.1996/aux-lamp-probe.md`) both
D.01R ROMs drive all sixteen auxiliary lamp addresses, 91-98 and 101-108, and clock 37/38 from
attract mode on. The production 1.2, 1.4 and 1.5 ROMs and the 0.3 prototype never do. So the D.01R
firmware expects the 16-LED Skull Driver PCB, and the production record, which records those
addresses unused, cannot hold it.

The notes also say the skull pile "now" sits in the back-right corner and that the Deadhead tale "is
now awarded after only three roll-over lanes instead of six", which suggests the prototype's
playfield and rules differed in more than the LED board. Nothing retained shows how.

## What a curator must establish next

- Whether a D.01R machine still exists, and its playfield layout, from photographs or an owner.
- The full input, output and display inventory. The production record's addresses are a starting
  point only: every one has to be confirmed against this firmware.
- Which of the skull board's sixteen outputs lit which eye, and where the skulls sat.
- Wiring, polarity, mechanism behaviour and normalized placements.

The production record's evidence (manual, known-working VPX table) describes the shipped machine and
cannot settle any of these.
