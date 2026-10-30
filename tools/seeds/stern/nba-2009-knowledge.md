# NBA (Stern, 2009)

Coverage: **partial - the complete public I/O inventory, its names and wire colours, the firmware family and the parts book's construction facts are recorded; which side each lower pop bumper is on, what several mechanisms do beyond firing, and the placements the retained table cannot supply are still open.**

## Identity and evidence precedence

This is the 2009 Stern S.A.M. machine (IPDB 5442, OPDB `G5K19-MBRlz`, designed by John Borg) with a 128x32 dot-matrix display, two flippers, three pop bumpers, two slingshots, a 3-bank (M-V-P) drop target, a captive ball, a motorized spinning disk and the Magna-hoop basket. All five pinned `nba_` drivers (root `nba_802`, clones `nba_801`, `nba_700`, `nba_600`, `nba_500`) are U.S.A. English firmware revisions of this one machine: pinned PinMAME initializes them identically (`INITGAME(nba, GEN_SAM, sam_dmd128x32, SAM_2COL, SAM_NO_AUX)`), and their switch, coil and lamp tests draw the same frames pixel for pixel and fire the same public outputs.

Stern's only public NBA document is a partial manual: the Blue Pages (major assemblies and ramps) and the Pink Pages (parts identification) of the parts book, 33 scanned pages without a text layer. It has no switch, lamp or coil table, no location drawings and no schematics. The ROM's own service tests, run in the pinned LibPinMAME harness, are therefore the naming source for every address and the source of the wire colours, and the parts book supplies part numbers, quantities and assembly topology where it prints them. Pinned PinMAME `sam.c` is the emulator contract. The retained VPX table (Bambi Plattfuss, v1.2, 2020) is used for coordinates and for controller-facing pulse/hold behaviour only; the project has not verified it as known-working, and it disagrees with the ROM on the pop-bumper sides (below).

## What the ROM tests settle

On a fresh NVRAM the S.A.M. service menu is reached with the Back key and Select presses; the switch, coil and lamp tests then name every address:

- **Switches.** Holding public 1-64 in turn, the switch test prints the ROM's name and the drive/return wire colours (drive by run of sixteen: GRN-BLU, GRN-VIO, GRN-GRY, GRN-WHT; return by position) and the generic `SWITCH #n` for the addresses the game does not use (17, 38-46, 48-64). The public number is the ROM's number, and a held public input is the ROM's active reading, so the public matrix is active-high: pinned `samswitch_r` complements the word on its way to the CPU. `physical.normally_closed` is false for every matrix switch, including the optos (11-13, 21, 22, 34), which read closed while blocked.
- **Dedicated switches.** The test names public 65-69 (five coin slots), -7 (tilt pendulum), -6 (slam tilt), -5 (ticket notch) and the left and right flipper EOS bits D-10 and D-12. Holding a flipper button (84 or 82) shows its EOS, because `samswitch_r` copies the button bit into the EOS bit. No upper flipper is fitted, so D-13 to D-16 carry only generic names. The parts book prints D-10 and D-12 beside the flipper's power (EOS) switch 180-5149-00, a normally closed contact.
- **Coils.** The Single Coil Test steps Q1-Q32 and skips Q24; for each it prints the name and the power/control wire colours, and Select fires the public solenoid whose number is the transistor number. Q6 (spinning disk motor) fires public 6 and 22 together; Q22 alone fires 22. Q24 (OPTIONAL COIL) fires nothing in the test but is pulsed for about 130 ms once per inserted coin, as a coin meter or knocker would be.
- **Lamps.** Stepping the Single Lamp Test lights public lamp *n* at selector position *n* for all 80 positions, with `NOT USED` for 8, 11, 29, 34, 38, 53, 55, 56 and 65-80. Wire colours follow the matrix: the first by position within each row of eight, the second by row.
- **Power-up and start.** GI 0 comes on at power-up, each coin pulses public 24, and Start pulses the trough up-kicker Q1.

## Public solenoid 33

Pinned `sam.c` gives only `nba_802` a fast-flip RAM address (`0x010609be`). Its VBLANK handler publishes public solenoid 33 while that word is 1. A diagnostic re-run of the gameplay probe that polled both the word and `PinmameGetSolenoid(33)` shows them turning on about 40 ms after Start and staying on through play. The pinned LibPinMAME build never reports it through `OnSolenoidUpdated`, though, so the retained harness traces carry no event for it (the same build also drops it for Family Guy, whose older-build trace has it). A consumer must poll public 33 to see it. The other four drivers have no fast-flip address, so 33 stays 0 on them. The retained table uses the core `InitVpmFFlipsSAM` fast flips, which hang off `SolCallback(33)`.

## Ball transport

Four balls rest in the trough assembly 500-6318-24-ND on micro switches 18, 19 and 20 and on the opto beam 21 at the up-kicker end; 22 is the jam beam above it on the same dual opto boards. Q1 lifts the right-most ball into the shooter lane (switch 23). The player plunges it with the ball shooter, or the autoplunger Q2 fires it. In the retained gameplay probe the ROM did not fire the autoplunger while the first ball sat in the shooter lane. Treat each trough position as sustained occupancy and the up-kick as the only way a ball leaves the stack.

## Playfield mechanisms

The mechanisms and their addresses are enumerated in the definition. What is known about each:

- **Left eject (switch 35, Q4) and the airborne shot.** IPDB describes a trajectory up-kicker that sends the ball airborne towards the hoop, and the designer's note mentions a free-throw kicker that shoots the ball through the air at the backboard. In the retained gameplay probe the ROM pulsed Q4 and energized the basket magnet Q3 while switch 35 was closed, and flashed the left eject arrow Q26; the retained table models this hole as that kicker. The parts book lists a 40-degree long-throw kicker 500-7157-01 (27-1400 coil) and a 30-degree eject 500-6511-01-ND (24-940 coil) without saying which hole each serves, so the pairing is an observation, not a documented fact.
- **Right eject (switch 9, Q20).** The ROM pulsed Q20 while switch 9 was closed and flashed the basketball Q19, the right eject arrow Q27 and the pop-bumper flash Q31.
- **Magna-hoop (Q3, basket opto 34).** Assembly 500-7162-00 carries a magnet and connector assembly 511-5221-00 behind the backboard plastic (IPDB photo: "Electromagnet Behind Hoop Backboard"). Opto 34 sees a ball pass through the hoop. How long the magnet holds a ball and what releases it are not documented; the retained table holds the ball at the backboard until it reaches switch 34.
- **M-V-P drop targets (switches 13, 12, 11; Q7).** Three targets on the slotted opto PCB 520-5252-03 of assembly 500-7029-03-00; a target's switch reads closed while it is down, and Q7 raises the bank. After the third target went down the ROM fired Q7 and the shaker Q8, and kept pulsing Q7 for as long as the harness held the switches down. Lamps 57-59 spell the letters.
- **Ramp diverter (Q5) and basket diverter (Q12).** The ROM names both. The parts book lists one diverter assembly 515-6596-00-A9 on the left plastic ramp 500-7158-00 and an up-post assembly 500-7161-00 titled "LIFT RAMP" (26-1200 coil), and the designer's note mentions a lift flap in the plastic ramp (the ramp-on-a-ramp that sends a fast ball towards the hoop) and a wire ramp / divert mechanism. None of them ties a coil number to an assembly, so which ramp exits the diverters select, and whether the lift-ramp up post is Q12 or Q21, is open. The retained table swaps two walls for Q5 and swings a flap into the ball's path for Q12.
- **Orbit up/down post (Q21).** A held output: in the retained probes it changed state once after the plunge, once at a flipper press and once at the first pop-bumper hit. The retained table raises a post across the orbit while it is energized.
- **Spinning disk (Q6 motor, Q22 relay).** Assembly 500-7144-01 with motor 511-5190-00 and disk/hub weldment 515-7714-00 under an art pad in the centre of the playfield. The ROM switched Q6 and Q22 on and off together in the retained probe. What the relay switches (for example the motor's direction or supply) is not documented, so the disk's direction and speed control are unknown.
- **Captive ball (switch 10).** IPDB lists one captive ball; switch 10, flash Q30 and lamp 22 belong to it.
- **Pop bumpers (switches 30-32, Q9-Q11, lamps 60-62).** 26-1200 coils, stack switches 180-5015-04 and white LED modules 112-5024-08. Each switch fires its own coil and lamp, and every hit also runs the shaker Q8 and flashes Q31 (three lamps). See the side conflict below.
- **Slingshots (switches 26, 27; Q17, Q18).** Assembly 500-5849-00-ND, 23-800 coils, two stack switches 180-5054-00 per side; each hit also flashes Q32.
- **Flippers (Q15, Q16).** Left assembly 500-6543-15-ND (23-1500), right 500-6543-05-ND (23-900), each with an EOS switch on D-10 / D-12; single-stack cabinet switches on D-9 / D-11.
- **Optional devices.** Q8 SHAKER MOTOR (OPTIONAL), which the parts book does not list, and Q24 OPTIONAL COIL (see above).

## The pop-bumper sides (conflict)

The ROM's switch, coil and lamp tests name switch 31, Q10 and lamp 61 LEFT POP BUMPER and switch 32, Q11 and lamp 62 RIGHT POP BUMPER. The parts book's bumper page prints `LAMPS 60 (TOP) 61 (RIGHT) 62 (LEFT)` and pairs `SW. 31` with RIGHT and `SW. 32` with LEFT. The retained table lights l61a on the left bumper and l62a on the right, like the ROM, but names and binds its bumper objects like the parts book (sw31 on the right) and plays its LeftJet sound on sw31. The definition labels and places these devices by the ROM's names and keeps their provenance `conflicted`. A switch-test reading on a physical NBA, or Stern's switch and lamp location drawings, would settle it.

## Lighting

Lamps 3-64 are the playfield inserts the lamp test names; 1 and 2 are the start and tournament buttons; 60-62 are the bumper LEDs. The flash lamps are solenoid outputs that pinned PinMAME types as #89 bulbs: Q13 backboard (two lamps), Q14 left ramp (two), Q19 basketball (three), Q23 left side, Q25-Q28 ramp and eject arrows, Q29 right side, Q30 captive ball, Q31 pop bumpers (three) and Q32 slingshots (two). The back panel 500-7160-00 carries the basketball, five #89 socket and bulb assemblies 519-5101-00-HF and seven clear sockets 519-5000-00-HF. PinMAME publishes one aggregate G.I. channel; the parts book has no G.I. circuit table.

## Spatial placement

Placements come from the exact retained table (bounds 0-952 by 0-2115) and are `observed`: switches at their target, trigger, gate and kicker objects, coils at the mechanism object they drive, the bumper lamps at their bulb lights, and flash lamps at one bulb light per lamp (never a VPX Flasher sprite). No location drawing exists to check them. The 51 insert lamps are only `candidate` placements at the centre of the table's insert light: that light renders the playfield image and sits on no bulb, so it does not locate the socket, which is expected under the insert. Not placed: the trough sensors 18-22 (the table models the trough in its script), the back-panel flashes Q13 and Q19 and the pop-bumper flash Q31 (no bulb object), and the G.I. The shaker Q8 and Q24 are cabinet devices, and relay Q22 is internal.

## Retained table modelling (not machine facts)

The table pulses the trough jam opto 22 as a ball is served, where a physical beam stays blocked while a ball sits in it. It comments out or leaves empty its callbacks for Q8-Q11, Q17, Q18 and Q22, so its bumpers and slingshots kick from the table's own hit events rather than from the ROM's coil outputs, and it has no shaker or disk-relay binding.

## Variants

`nba_802` (V8.02), `nba_801` (V8.01), `nba_700` (V7.0), `nba_600` (V6.0) and `nba_500` (V5.0) are firmware revisions of one physical machine. Only `nba_802` publishes the synthetic game-on solenoid 33.

## What remains

- Settle the pop-bumper sides (conflict above).
- Document what the ramp and basket diverters select, which coil drives the lift-ramp up post, what the spinning-disk relay switches, and how the Magna-hoop magnet holds and releases the ball.
- Check the placements against a location drawing, a second table or measured photos, and place the trough sensors, the back-panel and pop-bumper flashes and the G.I.
- Identify the contact type of the ramp switches 8, 33 and 37.

## Sources

- Stern Pinball, NBA partial manual (Blue and Pink pages), `NBA-Manual.pdf`, SHA-256 `f74e8c1c8ad5c724d51b8f472b9163ee2f5de685558f99686863e35e4d268243`; transcribed in `evidence/excerpts/stern.nba.2009/manual-blue-pages.md` and `manual-pink-pages.md`.
- The ROM's switch, coil and lamp tests on all five drivers, transcribed in `evidence/excerpts/stern.nba.2009/rom-service-tests.md`, with runtime summaries under `evidence/runtime/sam/nba-*.json`.
- The fast-flip diagnostic, `evidence/excerpts/stern.nba.2009/fast-flip-diagnostic.md`.
- Pinned PinMAME `src/wpc/sam.c` at `46e1a01a0f73dc5ce163d98db1ae435883ecc450`.
- IPDB 5442, retained as the Wayback Machine's 2024 capture.
- `NBA (Stern 2009).vpx` v1.2, SHA-256 `ae322910ad7f74f984e0216c5bf05cd0984ab727bff455f13992d5afb708eb58`, and its embedded script.
