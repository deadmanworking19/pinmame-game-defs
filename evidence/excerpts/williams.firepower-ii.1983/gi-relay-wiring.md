# General illumination relay K1

Manual PDF page 35, Power Wiring Diagram, right half of the spread beginning
on page 34. Manually read and visually checked by the curator; the committed native crop shows relay K1 and its driver branch.

Driver board SOL.11 (Q35), BRN-ORN, connects through 3P7/3J7 pin 1 to the K1
SPECIAL RELAY coil; pin 2 is N.C. and pin 3 is its return. A linked contact
opens the 3J9/3P9-1 supply leg when energized; pin2 is the other AC leg.
The coil's pin3 is supplied from +28V. The drawing is marked 515,
so the Firepower II connection table is the authority for game-specific
fitment. Table 4 positively names 11 General Illumination Relay, part 5580-09555.

Pages 48-50 draw 6.3 VAC general illumination: YEL/WHT-YEL cabinet/playfield
branches and VIO/WHT playfield branches. These are lamp strings behind relay
contacts, not another PinMAME GI callback. The schematic's repeated bulb
symbols are a wiring representation and do not establish a socket count.
K1 switches the common leg feeding all four drawn fused branches. The
following is a complete transcription of those branches on PDF35; each fuse
is5A slow-blow. Repeated lamps and continuation marks do not give quantities.

| Fused3P8 side | Other3P8 side | Downstream branch |
| --- | --- | --- |
| 7 WHT-VIO | 2 VIO | Playfield8J8-4/1 |
| 9 WHT-YEL | 4 YEL | Playfield8J8-5/6 and2/3; cabinet7P1-2/1 |
| 6 WHT-BRN | 1 BRN | Insert board9P1-4/1 |
| 8 WHT-GRN | 3 GRN | Insert board9P1-2/3 |

PDF41 reverses the insert-board fused-side pin labels:9P1-2 WHT-BRN,
9P1-4 WHT-GRN; it agrees on1 BRN and3 GRN. PDF50 labels8J8-5 YEL,
-2 YEL-WHT and-4 WHT, whereas PDF35/48 give5/6 WHT-YEL,2/3 YEL and
4 WHT-VIO. Preserve these literal wire/pin disagreements. They do not alter
the single normally-closed K1 contact's behavior. Before reproducing harness
colours/pins, trace an original connector; the ROM cannot settle wire colours.

PDF49 draws three parallel cabinet lamps, not an explicit complete socket
inventory. PDF41's insert strings and PDF50's two playfield strings have
continuations. All available retained gallery previews and above-playfield
photos lack a complete underside/socket view; quantities remain unknown.
