# Space Station — circuit boards, game controls, displays, operation and Test/Diagnostic Procedures

Source: `Williams_1987_Space_Station_Operations_Manual_and_Test_Procedures.pdf` (86 pages, SHA-256
`71e3212599e733ed432cdc533190ead6a925ff7a5d62862d7c09897566aaddbc`), PDF pages 1, 3, 6-7, 9, 30-35 and 40
(printed 2-3, 5, 26-31 and 36; the cover, PDF 1, prints `16-552-101 January 1988`). Read from the 150 dpi
scans rendered at 300 dpi. The Windows OCR layer was used to find these passages; every quotation below was
checked against the rendered page. Quotations are verbatim except that line breaks are joined.

## Cover and contents (PDF 1, 3)

The cover prints the manual number `16-552-101` and `January 1988`, and the title `SPACE STATION
OPERATIONS ... including ... PROCEDURES, PARTS INFORMATION, SCHEMATICS`. The contents page heads Section 1
"Game Operation & Test Information SPACE STATION (System 11 B)".

## Circuit boards (PDF 6, printed 2)

> SPACE STATION's System 11B Circuit Boards are in the backbox. They are accessible by removing the backbox
> glass, unlatching the insert board, and swinging it open.

> CPU BOARD. The System 11B CPU Board (p/n D-11883-552) must be equipped with the ROMs specified in the
> SPACE STATION (System 11B) ROM Summary. For this ROM complement and CPU Board, jumpers W1, W2, W4, W5, W7,
> W8, W11, W14, W16, W17, and W19 must be connected. (Jumper W7 is cut/removed for West German games.)

> AUDIO BOARD. The Audio Board is p/n D-11581-552, as supplied with ROMs and microprocessor.
> DISPLAY BOARD. The Alphanumeric Display Unit Board is p/n D-11609.
> POWER SUPPLY BOARD. The Power Supply Board is p/n D-8345-557.
> AUX POWER DRIVER BOARD. The Aux Power Driver Board is D-11813-552.

The board-prefix list on the same page assigns 1 CPU, 3 Backbox Power Supply, 4 Alphanumeric Display, 5 Aux
Power Driver, 6 Backbox, 7 Cabinet, 8 Playfield, 9 Insert Board and 11 Audio.

## Game control locations (PDF 6-7, printed 2-3)

> The On-Off switch is on the bottom of the cabinet near the right front leg. The Volume Control is on the
> left inner wall of the cabinet on the tilt mechanisms board. It is accessible by opening the coin box door.
> The Credit switch is a pushbutton to the left of the coin door on the cabinet exterior.

> SPACE STATION allows the operator to program virtually all game adjustments, obtain bookkeeping
> information, and diagnose problems, using only three switches mounted on the inside of the coin door and
> the Credit button beside the coin door. ADVANCE, AUTO-UP/MANUAL-DOWN, and HIGH-SCORE RESET are the
> switches located on the inside of the coin door.

> The Memory Protect switch is on the inside frame of the coin door. This interlock switch must be open to
> clear bookkeeping totals and to make game adjustments. It automatically opens, when the coin door opens.

> The CPU Diagnostic switch (SW 2) is the lower switch (of the two switches mounted on the left edge of the
> CPU Board) near a large, socketed microprocessor chip. This switch initiates the Memory Chip Test
> explained in the Test/Diagnostic Procedures. The Sound Diagnostic switch (SW 1) is the upper switch of
> the two mounted on the left edge of the CPU Board. This switch initiates the Sound Section Test.

## Game operation (PDF 9, printed 5)

> STARTING A GAME. Press the Credit button once. A startup sound plays, and the Credit amount shown in the
> player score display decreases by one.

> TILT. Actuating the Slam Tilt switch on the coin door inside the cabinet ends the current game; SPACE
> STATION then proceeds to the Game Over Mode. With the actuation of the playfield tilt switch, or the third
> closure* of the plumb bob tilt switch, the player loses the remaining play of that ball, but can complete
> the game.

(`*` is the page's "operator-adjustable feature" marker.)

## Test/Diagnostic Procedures (PDF 30-35, printed 26-31)

> To proceed to the Diagnostic Tests, the operator must simply switch the game On, set the
> AUTO-UP/MANUAL-DOWN switch to MANUAL-DOWN, and press the ADVANCE button.

> In order, these tests deal with the music, the displays, the game sounds, the lamps, the solenoids, and
> the switches.

Test identifiers on the player 3 display, as the text gives them: Display Test `01`, Sound Test `02`, All
Lamps `03`, Single Lamps `04`, Coil (Solenoid) Test `05`, Switch Levels `06`, Switch Edges `07`.

> Single Lamps. ... Then, the player 3 display shows 04 01, and the player 1 and 2 displays change to show
> BON BAL PLYR 1, the name of the lamp currently blinking. Press the Credit button to proceed through an
> ascending series of designator numbers (01 through 64)

> SOLENOID TEST. ... Observe that the player 1 and 2 displays show the message, COIL TEST, the player 3
> display shows 05 (Solenoid Test identifier). Next, the player 3 display shows a series of test steps from
> 01 through 22, while the player 1 and 2 displays show the solenoid/circuit name.

> Switch Levels. ... If, however, a switch is actuated (possibly stuck closed), the player 3 display shows
> that switch's number, while the player 1 and 2 displays indicate the switch's name.

> For SPACE STATION, switch numbers can range from 01 through 63.

> Switch Edges. ... When using a ball to actuate a switch, the operator should see the switch's name and
> number (in the player 1, 2, and 3 displays, respectively).

> placing a jumper between 1J10-9 and 1J8-2 should (based on the Switch-Matrix Table) should produce an
> indication of switch 09 being actuated.

## Alphanumeric Display Unit Board (PDF 40, printed 36)

Heading "Alphanumeric Display Unit Board including p/n D-11609 & associated parts". Rows bearing on the
displays:

| Part No. | Ckt Designator | Description |
| --- | --- | --- |
| 5670-10873-00* | DSPY1, DSPY2 | Display, 7 -character, A/N |
| 5670-09439-00* | DSPY3, DSPY4 | Display, 7-character, 7-segment |

Footnote: `* To show other parts locations, displays are shown vertical to pc board.` The page also prints
"Display Characters Segment Designations" for a 16-segment character (segments a-p plus a period) and a
7-segment character (a-g).

Uncertain readings: none.
