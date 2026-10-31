# Literal transcription - CYCLONE ROM table, A/C relay note and diagnostic tests

`reviewed: true`; transcribed by the curator from 300 dpi renders and visually checked against them on 2026-10-31
`source: Manual & Schematics PDF pages 2 (top), 9 (printed CYCLONE 5), 30, 31, 32, 33, 34 and 35 (printed CYCLONE 26-31)`

Retained renders: `external:pinmame-manuals/by-machine/williams.cyclone.1988/rendered-native/manual/p-02.png`,
`p-09.png`, `p-30.png` to `p-35.png` (300 dpi). The prose below is quoted from those pages; `[...]` marks an omitted
sentence that does not bear on the definition; `___` is a printed blank underline.

## CYCLONE ROM and Jumper Table (PDF page 2, top)

Literal heading: `CYCLONE ROM and Jumper Table`. The U15 and U24 cells of the SPACE STATION and CYCLONE rows print a
downward arrow from the BIG GUNS row, which is written `(as BIG GUNS)` below.

| Game | System 11B CPU Rev. | P/N - U15 Game µP | P/N - U27 G. ROM 1 | P/N - U26 G. ROM 2 | P/N - U21 S. ROM 1 | P/N - U22 S. ROM 2 | P/N - U24 Sound µP | Jumpers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BIG GUNS | - | 5400-09150-00 | A-5343-557-2 | A-5343-557-1 | A-5343-557-4 | A-5343-557-3 | 5400-09150-00 | W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and 19 |
| SPACE STATION | - | (as BIG GUNS) | A-5343-552-2 | A-5343-552-1 | A-5343-552-4 | A-5343-552-3 | (as BIG GUNS) | W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and 19 |
| CYCLONE | - | (as BIG GUNS) | A-5343-564-2 | A-5343-564-1 | A-5343-564-4 | A-5343-564-3 | (as BIG GUNS) | W1, 2, 4, 5, 7, 8, 11, 14, 16, 17, and 19 |

## Game Operation (PDF page 9, printed CYCLONE 5)

`STARTING A GAME. Press the Credit button once. A startup sound plays, and the Credit amount shown in the player score
display decreases by one. Player display 1 flashes 00 (until the first playfield switch is actuated), and the Player 4
display shows ball 1, except for 4-player games where the ball # shows in the individual player's display. Additional
players may enter the game by pressing the Credit button once for each player, before the end of play on the first
ball.`

`TILT. Actuating the Slam Tilt switch on the coin door inside the cabinet ends the current game; CYCLONE then proceeds
to the Game Over Mode. With the actuation of the playfield tilt switch, or the third closure* of the plumb bob tilt
switch, the player loses the remaining play of that ball, but can complete the game.` The page's footnote reads
`operator-adjustable feature`.

## Test/Diagnostic Procedures (PDF page 30, printed CYCLONE 26)

`To proceed to the Diagnostic Tests, the operator must simply switch the game On, set the AUTO-UP/MANUAL-DOWN switch
to MANUAL-DOWN, and press the ADVANCE button.`

`MUSIC TEST. 1. In the Music Test, observe that the player 1 and 2 displays show the message, MUSIC TEST.`
`DISPLAY TEST. 1. [...] the player 3 score display shows 01 (the Display Test identifier).`
`SOUND TEST. 1. [...] the player 3 display shows 02 (the Sound Test identifier).`

## Lamp Tests (PDF page 31, printed CYCLONE 27)

`1. All Lamps. (From Sound Test) To initiate the first Lamps Test, press ADVANCE. Observe that the Player 1 and 2
displays show the message, ALL LAMPS, and that the Player 3 display shows 03 (All LampsTest identifier) and that all
feature lamps (playfield and backbox) blink on and off. (Note, however, that the General Illumination lamps remain
lighted steadily.)`

`2. Single Lamps. From the All Lamps test, using AUTO-UP, press ADVANCE to initiate the Single Lamps Test. The Player 1
and 2 displays initially show the message, SINGLE LAMPS, and the Player 3 display shows 04. Then, the Player 3 display
shows 04 01, and the Player 1 and 2 displays change to show HOLD, the name of the lamp currently blinking. Press the
Credit button to proceed through an ascending series of designator numbers (01 through 64), with the Player 1 and 2
displays showing the individual lamp's name. Press and hold the Credit button to proceed rapidly to the desired lamp.`

## Solenoid Test (PDF page 32, printed CYCLONE 28)

`SOLENOID TEST. 1 (From Lamp Test) Using AUTO-UP, press ADVANCE. Observe that the Player 1 and 2 displays show the
message, COIL TEST, the Player 3 display shows 05 (Solenoid Test identifier). Next, the Player 3 display shows a series
of test steps from 01 through 22, while the Player 1 and 2 displays show the solenoid/circuit name. During each of these
steps, pulsing of the respective solenoid/circuit occurs. The test cycles repeatedly, unless halted via the MANUAL-DOWN
switch. Refer to the Solenoid Table for solenoid numbers and wiring information. CPU Board connections at 1P11, 1P12,
and 1P19 are also listed in the table.`

## Solenoid A/C Select Relay (PDF page 33, printed CYCLONE 29)

Literal `NOTE` box:

`As directed by the game program, the Solenoid A/C Select Relay (solenoid 12) switches the solenoid B+ power between
two power busses to permit actuating two groups of solenoids at the proper times. In its de-energized state, the Relay
connects the 'circuit A power' to 16 "controlled" and "switched" solenoids (identified in the table with no suffix
letter or the letter A, after the solenoid number). Individual solenoid operation then depends on the game program
enabling the ground path for solenoid actuation via the driver transistor associated with each solenoid circuit. For
example, the game program can actuate the Outhole Kicker solenoid (sol. 01A), via the driver transistor Q33.`

`When the game program determines that the Solenoid A/C Select Relay (sol. 12) must be energized, the relay connects
'circuit C power' to eight group C solenoids (01C through 08C). Now, driver transistor Q33 can actuate the Left Ferris
Wheel (p/f) and Jackpot (bb) Flasher circuit (sol. 01C). Using this "multiplexing" technique, the same driver
transistor can control actuation of two separate solenoid circuits.`

The drawing below the note is captioned `Typical CYCLONE +25V Circuit showing the Function of Select Relay, sol. 12`;
it is not transcribed.

## Switch Levels (PDF page 34, printed CYCLONE 30)

`(From Solenoid Test) To initiate the Switch Levels Test, press ADVANCE. Observe that the Player 1 and 2 displays show
the message, SWITCH LEVELS, and the Player 3 display shows 06 (Switch Levels Test identifier). Normally, the right
portion of the Player 3 display remains blank, indicating that no switch is actuated.`

`If, however, a switch is actuated (possibly stuck closed), the Player 3 display shows that switch's number, while the
Player 1 and 2 displays indicate the switch's name. [...] If more than one switch is closed, a series of displays show
each actuated switch's name and number.`

`[...] For CYCLONE, switch numbers can range from 01 through 64.`

## Switch Edges and Mystery Wheel Test (PDF page 35, printed CYCLONE 31)

`2. Switch Edges. From the Switch Levels Test, press ADVANCE. Observe that the Player 1 and 2 displays show the message,
SWITCH EDGES; the Player 3 display shows 07 (Switch Edges Test identifier).`

`MYSTERY WHEEL TEST`

`From the Switch Edges Test, press ADVANCE. Observe that the Player 1 and 2 displays show the message, WHEEL TEST, and
that the Player 3 displays shows 08 (Mystery Wheel Test identifier).`

`The Player 2 display now shows the last known position of the Mystery Wheel, while the Player 4 display is divided to
show the 'state' of the Home Switch. On the left of the Player 4 display, an "H" means that the Home Switch is open or
the opto is interrupted; on the right, a number shows the count of the stepper wheel (1-200; however, if the Home
Switch is not working, the number can go as high as 256). If the Player 3 Display shows 08___(#), it is reporting the
number of errors (#) for Mystery Wheel operation occurring since the last Game Turn-on.`

`Using AUTO-UP, the test is automatic: The wheel spins, waits for 2 seconds, then spins again. The wheel stops on the
next counterclockwise position of the wheel, if the Home Switch works.`

`Using MANUAL-DOWN, press ADVANCE to spin the wheel. The wheel stops on the next counterclockwise position of the wheel,
if the Home Switch works. If the wheel is not spinning, you can manually step the motor by pressing Credit button.`

`During the test, the Player 3 display shows 08Err (#) (Error numbers, up to 9, maximum), if errors occur (the game program
did not detect the Home Switch). During a lengthy test, the Player 3 display will detect any errors and add them to the
Err(#) count, so that the number displayed is the total number of errors detected during the test.`

Uncertainty: the page-36 sentence `reach the Switch Edges Test (06 in the Player 3 display)` gives Switch Edges the
Switch Levels identifier; page 35 prints `07` for Switch Edges.
