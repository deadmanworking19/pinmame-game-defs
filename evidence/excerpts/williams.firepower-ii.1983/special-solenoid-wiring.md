# Special solenoid and flipper wiring drawing

Manual PDF page 52 (left half of the spread ending on page 53), native render.
Manually read and visually checked by the curator.
The committed crop is the driver/connector block. The schematic prints **515**
on its right half although the manual cover is model 521. Treat template
hardware as topology evidence and use the game's connection/location tables
for fitted devices; in particular four cabinet flipper contact symbols in the
cabinet spread do not prove four fitted flippers on this game.

The drawing, unlike Table 4, connects Q6 to 2J12/2P12 pin 3 and solenoid 19;
Q10 to pin 8, BLU-BLK SOL.21, 8P3 pin 21; Q12 to pin 9, BLU-GRN SOL.22,
8P3 pin 22. Table 4's literal disagreements are retained separately. Structured
values follow Table 4 until a source independent of this manual settles wiring.

The six trigger returns in the drawing are:

| Printed line | 2J13/2P13 | Wire | 8P3 |
| --- | --- | --- | --- |
| SOL.22 SPEC.SW. | 9 | ORN-BLU SOL.22 | 29 |
| SOL.21 SPEC.SW. | 8 | ORN-GRN SOL.21 | 28 |
| SOL.20 SPEC.SW. | 4 | ORN-YEL SOL.20 | 27 |
| SOL.19 SPEC.SW. | 2 | ORN-BLK SOL.19 | 26 |
| SOL.18 SPEC.SW. | 3 | ORN-RED SOL.18 | 25 |
| SOL.17 SPEC.SW. | 5 | ORN-BRN SOL.17 | NC |

The 17 branch continues to a left-kicker contact despite the NC printing.
Table 4 gives 8P3-24 for 17 and ORN-GRY for 21; those disagreements are unresolved
wiring details, not evidence of missing mechanisms. The drawing shows relay
Z1 providing the flipper ground returns on 2J12/2P12 pins 1 and 2. On page 53
the six separate normally open direct-power contacts are 8SW65 left kicker,
8SW66 right kicker, 8SW67 lower left jet, 8SW68 upper right jet, 8SW69 upper
left jet and 8SW70 lower right jet. They are separate from scoring matrix
contacts 47,48,41,42,43,44; PinMAME models the direct power response from the
scoring contacts named in sxx.ssSw, not with public switch addresses 65-70.
# Flash load designation

PDF52-53 draws solenoid4, Q21, GRY-YEL through2P11-8 and8P3-4 to
the load labelled8L2 ORBIT COMPLETE FLASH LAMPS, opposite side+28V.
The same spread labels ball ramp thrower2 as8L2 too. Preserve the repeated
designation; it does not merge outputs2/4. A grouped coil-shaped symbol with
diode represents the flash load and supplies no physical socket count.
