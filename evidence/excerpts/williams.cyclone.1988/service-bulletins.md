# Literal transcription - Williams service bulletins SS47, SS49, SS50 and SS52 (Cyclone)

`reviewed: true`; transcribed by the curator from 300 dpi renders and visually checked against them on 2026-10-31
`source: Service Bulletin Book (1989) PDF pages 7-12 (book pages 5-10)`

Retained renders: `external:pinmame-manuals/by-machine/williams.cyclone.1988/rendered-native/bulletins/p-07.png` to
`p-12.png` (300 dpi). The book's contents page lists `CYCLONE Mystery Wheel` (page 5), `CYCLONE Ball Trap` (7),
`CYCLONE Ferris Wheel` (8) and `CYCLONE Spookhouse Ramp` (10). Prose is quoted verbatim; `[...]` marks omitted
procedure steps that do not bear on the definition.

## SS47, July 27, 1988 (PDF pages 7-8)

`SUBJECT: Cyclone mystery wheel (D-12045) schematic and assembly drawings. Drawings of this assembly were unavailable
when the manual went to press. They appear in this bulletin.`

The assembly drawing's table, heading `Stepper Control Assembly #D-12045`. Rows 4-6 are printed over a dark screen;
row 4 is only partly legible.

| Item | Description | Part No. |
| --- | --- | --- |
| 1 | Subassembly D-12046 | D-12046 |
| 2 | Machine screw | 4005-01016-07 |
| 3 | Lockwasher #5, split | 4701-00023-00 |
| 4 | Hex nut, 5-40 (partly legible) | 4405-01117-00 (partly legible) |
| 5 | Heatsink compound | 20-9229 |
| 6 | Heatsink | 5705-09042-00 |

PDF page 8 is the drawing captioned `CYCLONE Mystery Wheel Schematic`. It is a drawing; only its connector labels and
part legends are transcribed here:

- Connector `P1`: pin 1 `row`, pin 3 `column`, pin 2 `Key`, pin 6 (drawn to `+12 V`, `C1 100 µF` and the `7805` input),
  pin 7 (drawn to ground), pin 5 `input A`, pin 4 `input B`.
- Connector `P2`: pin 6 `A (red)`, pin 5 `Ā (brn)`, pin 4 `nc`, pin 3 `Key`, pin 2 `B (grn)`, pin 1 `B̄ (blk)`; pins 6
  and 5 are labelled `stepper motor coil A`, pins 2 and 1 `stepper motor coil B`.
- `input A` is drawn to comparators `U2a` and `U2b` (`U2:LM339`), whose outputs drive the transistor pairs `Q1`/`Q5`
  and `Q2`/`Q6` on P2-6 and P2-5; `input B` is drawn to `U2c` and `U2d`, driving `Q3`/`Q7` and `Q4`/`Q8` on P2-2 and P2-1.
- `Opto 1` (LED fed through `R10 470Ω 1/2w` from `+12 V`) is drawn to the base circuit of `Q9 2N3906` (`R11 27K`,
  `R12 820Ω`, `R13 100K`); Q9 and `D11 1N4148` are drawn between the `column` and `row` pins of P1.
- Legends: `D1-D10: 1N4001`, `Q1-Q4: 2N4401`, `Q5-Q8: 2N4403`.

## SS49, July 25, 1988 (PDF page 9)

`SUBJECT: An added post and ring for Cyclone games. These items prevent balls from getting stuck between playfield
plastic and the Cyclone ramp. Installation instructions follow.`

`MATERIALS: 23-6305 2" Rubber ring` / `03-8044-9 Red, plastic post`

`Procedure`

1. `Temporarily remove your game's playfield glass.`
2. `Remove the clear, plastic Cyclone and Comet ramps. 11 screws secure these ramps to the playfield.`
3. `Find the blue plastic that has "Freak Show" and "Ken's Vending" screened on it. Three white, plastic cap nuts
   secure this plastic to playfield posts. Discard the uppermost cap nut.`
4. `Discard the small, white rubber ring on the red post above the "Ken's Vending" sign.`
5. `Install the 03-8044-9 red, plastic post on the screw where you removed the cap nut.`
6. `Install the 23-6305 rubber ring by stretching it between the two red posts.`
7. `Reinstall the clear, plastic Cyclone and Comet ramps.`
8. `Remount the game's playfield glass.`

## SS50, July 25, 1988 (PDF pages 10-11)

`SUBJECT: Cyclone ferris wheel not turning properly. During assembly or routine maintenance, over-lubrication can
cause ferris wheel parts to slip. Cleaning the ferris wheel belt and pulleys usually remedies the problem.`

`[...]`

4. `Disconnect the power connector (white, plastic, two-cavity plug) from the ferris wheel motor.`
5. `Under the ferris wheel, find the ball-support bar. Remove the two screws securing the bar to the playfield. Set the
   bar aside.`

`[...]`

7. `Beside the ferris wheel, notice the playfield plastic assembly. Remove the two screws on the assembly's green
   plastic, and set the assembly aside.`
8. `Remove the two screws securing the ferris wheel to the playfield. Temporarily remove the ferris wheel from the
   playfield and set it aside.`
9. `Remove the belt from the assembly: First, slip the belt off the white pulley. Then slide the belt over the metal,
   ferris wheel bracket. Don't attempt to slip the belt over the ferris wheel!`
10. `Clean and inspect the belt and pulleys. Look for excess lubrication or wear. Replace worn-out parts.`

`[...]`

## SS52, October 13, 1988 (PDF page 12)

`SUBJECT: Cyclone Spookhouse Ramp Breakage Reduction via Ramp Support Bracket Installation.`

`[...]`

4. `Locate the Spookhouse Ramp (left middle of playfield). Observe that the Ramp Cushion Plate (p/n A-12222) is in place
   on the ramp interior, just under the ramp entrance. Remove the mounting screw at the end of the ramp.`
   - `A. If the cushion plate is missing, dismount the ramp entirely from the playfield. Remove the tape cover paper and
     press the Cushion Plate in place, as shown in Figure 1. Reinstall the ramp, EXCEPT for the mounting screw on the
     ramp entrance end. Position the Ramp Support Bracket (A-12407) snugly against the end of the ramp and reinstall the
     mounting screw to secure the bracket and ramp to the bottom of the playfield.`
   - `B. If the cushion plate is present, position the Ramp Support Bracket (A-12407) snugly against the end of the
     ramp and reinstall the mounting screw to secure the bracket and ramp to the bottom of the playfield.`

Figure 1 is captioned `CYCLONE Playfield Spookhouse Ramp Area: Parts Locations` and labels `Cushion Plate`,
`Spookhouse Playfield Entance Hole` (printed so), `Mounting Screw`, `Spookhouse Ramp` and `Ramp Support Bracket
A-12407`.

## Reading against the manuals

- The operations manual's Switches list footnotes the Mystery Wheel Opto as `Part of Motor Control Assy, D-12046`, and
  the parts manual lists the opto on the D-12045 board; SS47 lists `Subassembly D-12046` as item 1 of the D-12045
  Stepper Control Assembly, so both numbers name the same board.
- The stepper board takes two logic inputs, `input A` and `input B`, each steering one winding of a two-winding
  stepper motor. Which CPU output reaches which input is not printed: the Solenoid Table names 14 `Coil A` and 13
  `Coil B`, and the Solenoids/Flashers list names them the other way round.
