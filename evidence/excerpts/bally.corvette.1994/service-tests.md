# Corvette — Test Menu and Service Tests

Provenance: transcribed from the Bally "Corvette" (1994) service manual, PDF pages m-031 through m-035 (printed pages 1-13 through 1-17), rendered at 300 dpi (`rendered-300/m-031.png` .. `m-035.png`), and from Manual Amendment 16-9890 (dated September 2, 1994), pages a-01, a-02, a-03 (T.19 part), a-04, a-05 and a-06 (`rendered-300-amendment/a-01.png` .. `a-06.png`). Text is copied literally (spelling, capitalization, punctuation, line structure); the Windows OCR draft was corrected word by word against the images. Transcription draft, not yet reviewed against the rendered pages by a curator.

## m-031 (printed page 1-13)

Introductory paragraph (bold italic in the original):

```
Use the Service Switch Actuator to hold in the top interlock switch located in the bottom left
corner of the coin door opening. The actuator must be in place in order to activate the solenoids
and flashlamps.

Press the Up or Down buttons to cycle through the menu. Press the Enter button to access a test. Press
the Escape button to return to the Test Menu.

Note: During any test, press the Start button to obtain the wire color, driver number, connector number
and fuse location.
```

Heading (underlined, bold): `T. TEST MENU`

Test Menu list exactly as printed (bold, two columns):

```
T.1    Switch Edges
T.2    Switch Levels
T.3    Single Switch
T.4    Solenoid Test
T.5    Flasher Test
T.6    General Illumination
T.7    Sound & Music Test
T.8    Single Lamps
T.9    All Lamps
T.10   Lamp & Flasher Tests
T.11   Display Test
T.12   Flipper Test
T.13   Ordered Lamps Test
T.14   Lamp Row-ColTest
T.15   Dip Switch Test
T.16   ZR-1/LT-5 Test
T.17   Race Test
T.18   Empty Balls Test
```

Body text below the menu:

```
The switch matrix, on the left side of the display, shows the state of all switches. A dot indicates
the switch is open, and a square indicates the switch is closed. The numbers assigned to each switch
indicate where the switch is located in the matrix. The number on the left indicates the column, and the
number on the right indicates the row. Example: Switch 23 is 2nd column, 3rd row.
     A short to ground, on either the row or column wire, appears as a shorted row(s). However, a
column wire shorted to ground disappears when all the indicated row switches are open. A row wire
shorted to ground does not disappear.
     A shorted diode in the switch matrix can cause other switches to appear closed. These
"phantom" switches (though not actually closed) complete a rectangle in the switch matrix. Therefore, if
two switches in the same column are closed (example; #22 and #24), and a third switch is pressed in
another column but in the same row as one of the first two (example; #32), the "phantom" switch #34 is
falsely indicated as closed. The switch with the shorted diode is diagonally opposite the "phantom "
switch (in this case #22).

T.1 Switch Edges      Press each switch one at a time. The name and number of the switch is
     shown in the display. If a switch other than the one pressed, or no switch at all is indicated, the
     system has detected a problem with the switch circuit.

T.2 Switch Levels     This test automatically cycles through all switches that are detected
     closed. The name and number of each switch that is detected is shown in the display. A filled
     square indicates the switch's position in the matrix.

T.3 Single Switches   The Single Switch Test isolates a particular switch by blocking signals
     from all other switches. Use the Up or Down buttons to select the switch to be tested.

1-13
```

## m-032 (printed page 1-14)

```
T.4 Solenoid Test     The Solenoid Test has three modes: Repeat, Stop, and Run. Only one
     solenoid should pulse at a time. The system has detected a problem if; more then one solenoid
     pulses, a solenoid comes On and stays On, or no solenoids pulse during the Repeat or Run
     modes.

Repeat  -  The Repeat Mode pulses a single solenoid. After entering this test, Solenoid 1 shows in
           the display. and the corresponding solenoid activates. Press the Up or Down button to
           cycle through the solenoids, one at a time. The same solenoid pulses until the Up or
           Down button is pressed. Either press the Escape button to return to the Test Menu, or
           press the Enter button to advance to the next mode.

Stop    -  The Stop Mode halts the Solenoid Test. Press Enter during the Repeat mode and the
           Solenoid Test Stops. No solenoids should be activated while the test is stopped. Either
           press the Escape button to return to the Test Menu, or the Enter button to advance to the
           next mode.

Run     -  The Run Mode cycles through the solenoids automatically. The display shows the name
           and number of the solenoid currently being pulsed. Either press the Escape button to
           return to the Test Menu, or the Enter button to advance to the next mode.

T.5 Flasher Test      This tests the flashlamp part of the solenoid circuit exclusively. This, like
     the Solenoid Test has three test modes: Repeat, Stop, and Run. During this test, only one
     flashlamp circuit should pulse at a time. The system has detected a problem if more than one
     circuit pulses, a circuit stays On, or no circuits pulse during the Repeat or Run modes.

Repeat  -  The Repeat mode pulses a single flashlamp. After entering this test, the name and
           number of the first flashlamp circuit will show in the display and the corresponding bulb(s)
           flash. Press the Up or Down button to cycle through all of the flashlamp circuits one at a
           time. The same circuit pulses until the Up or Down button is pressed. Either press the
           Escape button to return to the Test Menu, or press the Enter button to advance to the
           next mode.

Stop    -  The Stop Mode halts the Flasher Test. No flashlamp circuit should be active during this
           mode. Either press the Escape button to return to the Test Menu, or the Enter button to
           advance to the next mode.

Run     -  The Run Mode cycles through the flashlamps automatically. The display shows the
           name and number of the flashlamp circuit currently being pulsed and the corresponding
           bulb(s) flash. Either press the Escape button to return to the Test Menu, or the Enter
           button to advance to the next mode.

T.6 General Illumination   This test checks all of the General Illumination circuits. There are two
     modes of operation: Stop and Run.

Stop    -  Press the Up or Down buttons to cycle through the General Illumination Test manually.
           All illumination is tested first, followed by an individual circuit test. The circuit name and
           number will show in the display while the corresponding lamps light. If any other results
           occur the system has detected an error.

Run     -  Press the Enter button any time during Stop mode and the General Illumination Test
           cycles through automatically. For each circuit shown in the displays the corresponding
           bulbs should light. If any other results occurs the system has detected a problem.

1-14
```

## m-033 (printed page 1-15)

```
T.7 Sound and Music Test     The Sound and Music Test allows you to check the audio
     circuits. This test has three modes for testing the sound and music circuits: Run, Repeat, and
     Stop.

Run     -  The Run Mode steps through a sequence of sounds and music. Pressing the Up or
           Down button during this portion of the Sound and Music test advances to a particular
           sound/tune without having to wait for the program to play all the sounds available in the
           test. A sound/tune should be heard for each name and number that appears in the
           display. Any other results indicate the system has detected a problem.

Repeat  -  Press the Enter button at any time during the Run Mode to cause the program to stop
           and repeat a particular sound/tune. The same sound should repeat continuously until
           the Up or Down button is pressed. Any other results indicates the system has detected a
           problem.

Stop    -  Press the Enter button at any time during the Repeat Mode to stop this test altogether.
           No sound/tune should be heard. Any other results indicates the system has detected a
           problem.

T.8 Single Lamp Test     The number assigned to each lamp indicates the lamp's position in the
     matrix. The number on the left indicates the column. The number on the right indicates the row.
     Example: Lamp 23 means 2nd column, 3rd row.

     This test checks each lamp circuit individually. Press the Up or Down button to cycle through this
     test. For each name and number that is shown in the display the corresponding lamp should
     light. Any other results indicate the system has detected a problem.

T.9 All Lamps Test This test causes all the controlled lamps to flash at the same time. Every
     controlled lamp should flash. Any other results indicate the system has detected a problem.

T.10 Lamp and Flasher Test     This test causes all the flashlamps and the controlled lamps to
     flash at the same time. The controlled lamps blink, while the flashlamps cycle from highest to
     lowest. Any other results indicates the system has detected a problem.

T.11 Display Test   This test automatically lights every dot in the Dot Matrix Display. A series of
     patterns appear in sequence. Each pattern turns On and Off a section of dots. Every dot on the
     display should be turned On and Off during this test.

1-15
```

## m-034 (printed page 1-16)

```
T.12 Flipper Coil Test     The Flipper Coil Test has three modes: Repeat, Stop, and Run.
     Only one flipper should pulse at a time. The system has detected a problem if more than one
     flipper pulses, a flipper comes On and stays On, or no flippers pulse during the Repeat or Run
     modes.

Repeat  -  The Repeat Mode pulses a single flipper. After entering this test, coil 01 shows in the
           display and the corresponding flipper activates. Press the Up or Down button to cycle
           through the flipper coils, one at a time. The same flipper coil pulses until the Up or Down
           button is pressed. Either press the Escape button to return to the Test Menu, or press
           the Enter button to advance to the next mode.

Stop    -  The Stop Mode halts the Flipper Coil Test. Press Enter during the Repeat mode and the
           Flipper Coil Test stops. No flipper coil should be activated while the test is stopped.
           Either press the Escape button to return to the Test Menu, or the Enter button to advance
           to the next mode.

Run     -  The Run Mode cycles through the flippers automatically. The display shows the name
           and number of the flipper coil currently being pulsed. Either press the Escape button to
           return to the Test Menu, or the Enter button to advance to the next mode.

T.13 Ordered Lamp Test  The number assigned to each lamp indicates the lamp's position in the
     matrix. The number on the left indicates the column. The number on the right indicates the row.
     Example - Lamp 23 means 2nd column, 3rd row.

     This test checks each lamp circuit individually. Press the Up or Down button to cycle through the
     lamps. Lamps light in a clock-wise or counter clock-wise direction starting from the bottom of the
     playfield. Direction depends on which button, Up or Down, is pressed. For each name and
     number that is shown in the display the corresponding lamp should light. Any other results
     indicates the system has detected a problem.

T.14 Lamp Row-Col Test     This test allows individual rows and columns in the lamp matrix
     to be operated. This is useful for trouble-shooting wiring and driver problems.

     Press the UP or DOWN buttons to cycle trough the different rows and columns.

T.15 Dip Switch Test     This test is used to show the positions of the dip switches on the CPU
     board (U27).

T.16 ZR-1/LT-5 Test     Select T.16 from the Test Menu and press "ENTER" to begin the ZR-
     1/LT-5 (engine) test. Once the "SELF TEST" completes successfully, the "UP" and "DOWN"
     buttons can be used to select the following tests. Use the "ENTER" button to start the selected
     test, and the "ESCAPE" button to abort the selected test.

     The status of the "FULL LEFT" and "FULL RIGHT" optical switches and the angular position are
     displayed on the dot matrix display during all tests.

     SELF TEST - This test verifies that the engine is fully operational. This test is run automatically
     upon entry to the ZR-1/LT-5 TEST. It can also be started manually by pressing the "ENTER"
     button when selected.

     AUTO RUN - This test runs the engine in an oscillatory fashion until the "ESCAPE" button is
     pressed. The test pauses the engine periodically.

1-16
```

## m-035 (printed page 1-17)

```
     ENGINE LEFT - This test moves the angular position of the engine to the left (counter-clockwise)
     until the "FULL LEFT" optical switch closes.

     ENGINE RIGHT - This test moves the angular position of the engine to the right (clockwise) until
     the "FULL RIGHT" optical switch closes.

     ENGINE CENTER - This test moves the angular position of the engine to the center. At this
     point, neither the "FULL LEFT" nor the "FULL RIGHT" optical switches should be closed.

T.17 Race Test     Select T.17 from the Test Menu and press "ENTER" to begin the RACE TRACK
     test. Once the "SELF TEST" completes successfully, the "UP" and "DOWN" buttons can be used
     to select the following tests. Use the "ENTER" button to start the selected test, and the
     "ESCAPE" button to abort the selected test.

     The status of the "LEFT START", "RIGHT START", "LEFT ENCODER", and "RIGHT ENCODER"
     optical switches and car positions are displayed on the dot matrix display during all tests.

     SELF TEST - This test verifies that the race track is operational. This test is run automatically
     upon entry to the RACE TEST. It can also be started manually by pressing the "ENTER" button
     when selected.

     LEFT HOME - This test drives the left car in reverse until the "LEFT START" optical switch is
     closes.

     LEFT FORWARD - This test drives the left car forward while the "+" button is pressed.

     LEFT REVERSE - This test drives the left car in reverse while the "-" button is pressed.

     RIGHT HOME - This test drives the right car in reverse until the "RIGHT START" optical switch is
     closes.

     RIGHT FORWARD - This test drives the right car forward while the "+" button is pressed.

     RIGHT REVERSE - This test drives the right car in reverse while the "-" button is pressed.

T.18 Empty Balls Test     Select T.18 from the Test Menu and press "ENTER" to begin the EMPTY
     BALLS test.

     This test kicks out all balls loaded in troughs, lockups, poppers, and kickouts until no balls remain
     in those locations.

     Note: As the trough kicks out balls, they will stack up in the shooter groove, which may require
     manual clearing in order to allow further balls to be kicked out.

1-17
```

## Amendment 16-9890 test changes

### a-01 (printed page 1)

Letterhead: logo and `FLIPPERSPILL.COM`; top right, two lines: `September 2, 1994` / `16-9890`.

```
CORVETTE
Manual Amendment

The following information has been updated or added to the Corvette manual since final printing.
Please keep this amendment with your manual.

If experiencing difficulty with the Engine Assembly, read the new ZR-1
Adjust Test. This test will help solve the problem.

NEW Test Procedure:

T.18   ZR-1 ADJUST   Select T.18 from the Test Menu and press "ENTER" to perform the
       ZR-1/LT-5 engine adjustment procedure.

       The purpose of this procedure is to adjust the centering potentiometer of a
       malfunctioning engine assembly. In order to determine if the engine is malfunctioning,
       first run the ZR-1/LT-5 TEST, SELF TEST (T16). If the SELF TEST does not indicate
       failure, then this adjustment may not be necessary.

       This test function enables the ZR-1/LT-5 engine power and places it at the center
       position. (Note, the door must be closed to turn on the engine power.)

       With the engine held at the center position (the result of running this test), use a small flat
       blade screw driver to adjust the potentiometer located beneath the ramp, inside of the
       engine assembly. A hole in the ramp provides access to the potentiometer, as shown
       below.
```

Drawing: a top view of the engine and ramp assembly. Captions as printed: `ZR-1 Adjust - Centering` / `Potentiometer Access Hole` (with a leader line to a small hole in the ramp) and, beneath the drawing, `A-19140` / `Engine & Ramp Assembly`.

```
       Turning the potentiometer clockwise moves the engine to the left (as viewed from the
       front of the machine) and turning the potentiometer counter-clockwise moves the engine
       to the right.

       The potentiometer should be adjusted to position the engine as close to the center of
       movement as possible.

       Once this adjustment is complete, run the ZR-1/LT-5 TEST, SELF TEST (T16) again to
       verify the proper functionality of the engine assembly.

1
```

### a-02 (printed page 2)

```
CHANGE to Test Procedures: Pages 1-16 and 1-17

T.16   ZR-1/LT-5 TEST   Select T.16 from the Test Menu and press "ENTER" to begin the
       ZR-1/LT-5 (engine) test. Once the "SELF TEST" completes successfully, the "UP" and
       "DOWN" buttons can be used to select the following tests. Use the "ENTER" button to
       start the selected test, and the "ESCAPE" button to abort the selected test. (Note, the
       door must be closed to turn on the engine power.)

       The status of the "FULL LEFT" and "FULL RIGHT" optical switches and the angular
       position are displayed on the dot matrix display during all tests.

       SELF TEST - This test verifies that the engine is fully operational. This test is run
       automatically upon entry to the ZR-1/LT-5 TEST. It can also be started manually by
       pressing the "ENTER" button when selected. If this test fails, the ZR-1 ADJUST test
       (T.18) may need to be run.

       AUTO RUN - This test runs the engine in an oscillatory fashion until the "ESCAPE"
       button is pressed. The test pauses the engine periodically.

       ENGINE LEFT - This test moves the angular position of the engine to the left (counter-
       clockwise) until the "FULL LEFT" optical switch closes.

       ENGINE RIGHT - This test moves the angular position of the engine to the right
       (clockwise) until the "FULL RIGHT" optical switch closes.

       ENGINE CENTER - This test moves the angular position of the engine to the center. At
       this point, neither the "FULL LEFT" nor the "FULL RIGHT" optical switches should be
       closed.

T.17   RACE TEST   Select T.17 from the Test Menu and press "ENTER" to begin the RACE
       TRACK test. Once the "SELF TEST" completes successfully, the "UP" and "DOWN"
       buttons can be used to select the following tests. Use the "ENTER" button to start the
       selected test, and the "ESCAPE" button to abort the selected test. (Note, the door must
       be closed to turn on the race track power.)

       The status of the "LEFT START", "RIGHT START", "LEFT ENCODER", and "RIGHT
       ENCODER" optical switches are displayed on the dot matrix display during all tests. The
       car position value is displayed when possible.

       SELF TEST - This test verifies that the race track is operational. This test is run
       automatically upon entry to the RACE TEST. It can also be started manually by pressing
       the "ENTER" button when selected.

       RESET - This test positions both cars to the starting line.

       LEFT FORWARD - This test drives the left car forward while the "ENTER" button is
       pressed.

       RIGHT FORWARD - This test drives the left car in reverse while the "ENTER" button is
       pressed.

2
```

### a-03 (printed page 3), test part

```
T.19 Empty Balls Test  Select T.19 from the Test Menu and press "ENTER" to begin the EMPTY
     BALLS test.

     This test kicks out all balls loaded in troughs, lockups, poppers, and kickouts until no
     balls remain in those locations.

Note: As the trough kicks out balls, they will stack up in the shooter groove, which may require
manual clearing in order to allow further balls to be kicked out.
```

(The remainder of a-03, the "CHANGE to Rules: Pages E & F" and "NEW Rules" text, is in `game-rules.md`.)

Test Menu as amended by 16-9890 (derived only from the amendment's printed test headings; the amendment does not reprint the whole menu): the amendment prints a new `T.18 ZR-1 ADJUST` and moves the Empty Balls Test to `T.19`; it prints T.16 as `ZR-1/LT-5 TEST` and T.17 as `RACE TEST`, and prints no change to T.1 through T.15.

### a-04 (printed page 4)

`CHANGE to Difficulty Settings Tables: Page 1-19`

`Game Difficulty Setting Table for U.S./Canadian/French Games`

| Adj. No. | Adjustment Description | Extra Easy U.9 01 | Easy U.9 02 | Medium U.9 03 | Hard U.0 04 | Extra Hard U.9 05 |
| --- | --- | --- | --- | --- | --- | --- |
| A.2 05 | Ball Saves | 2 | 2 | 1 | 1 | 0 |
| A.2 06 | Ball Save Time | 9 | 7 | 5 | 4 | 2 |
| A.2 07 | Lock Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |
| A.2 08 | Race Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |
| A.2 09 | Catch Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |
| A.2 10 | Challenge Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |

`Game Difficulty Setting Table for German/European Games`

| Adj. No. | Adjustment Description | Extra Easy U.9 01 | Easy U.9 02 | Medium U.9 03 | Hard U.0 04 | Extra Hard U.9 05 |
| --- | --- | --- | --- | --- | --- | --- |
| A.2 05 | Ball Saves | 2 | 2 | 1 | 1 | 0 |
| A.2 06 | Ball Save Time | 9 | 7 | 5 | 4 | 2 |
| A.2 07 | Lock Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |
| A.2 08 | Race Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |
| A.2 09 | Catch Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |
| A.2 10 | Challenge Difficulty | Extra Easy | Easy | Medium | Hard | Extra Hard |

(Both tables print the Hard column header as `U.0 04`; the other four columns print `U.9`. Kept literally. The two tables print identical values.)

`CHANGE to Preset Game Adjustments Tables: Page 1-20`

`Preset Game Adjustments Table for U.S./Canadian Games`

| Adjustment Number | Adjustment Description | Install 3-Ball U.9 07 (factory) | Install 5 Ball U.9 06 |
| --- | --- | --- | --- |
| A.1 01 | Balls Per Game | 3 | 5 |
| A.1 07 | Replay Start | 850,000,000 | 1,200,000,000 |
| A.2 04 | Extra Ball Level | 7 | 18 |
| A.2 05 | Ball Saves | 1 | 1 |
| A.2 06 | Ball Save Time | 5 | 4 |
| A.2 07 | Lock Difficulty | Medium | Hard |
| A.2 10 | Challenge Difficulty | Easy | Medium |

```
CHANGE to Feature Adjustments: Pages 1-27 thru 1-30
A.2 04   EX. BALL LEVEL
         This is the number of SPARK PLUGS necessary to light the EXTRA BALL lamp. The
         machine will start with this value and modify it as necessary to achieve the percentage
         specified in A.2 03. To use a fixed level for the extra ball, set A.2 03 to FIXED, then set
         this level.

         Setting:           4-60
         Factory Default:   7

4
```

### a-05 (printed page 5)

```
A.2 05   BALL SAVES
         This determines how many times a ball will be saved when it drains. The ball will be
         saved only once per ball-in-play. The ball saver is available each ball until the adjusted
         number of ball saves is used by the player.

         Settings:          OFF
                            1-5
         Factory Default:   1

         Example of ball save usage:
         With BALL SAVES = 1 (factory default)

            BALL 1:    Ball save available
                       Ball drains after ball saver time-out

            BALL 2:    Ball save available
                       Ball drains during ball saver timer, and ball is delivered back
                       onto the playfield

            BALL 3:    Ball save NOT available

Note: In addition to the BALL SAVES adjustment, a very short DEFAULT ball save is provided
after the player has used all of their STANDARD ball saves when the ENABLE DEF SAVER (A.2
14) adjustment is set to YES.

A.2 06   BALL SAVE TIME
         This sets the number of seconds that the ball saver is activated.

         Setting:           4-15
         Factory Default:   5

A.2 10   CHALLENGE DIFFICULTY
         This determines the difficulty of the CORVETTE CHALLENGE feature. This affects the
         START CHALLENGE lamp.

         Settings:          EXTRA EASY
                            EASY
                            MEDIUM
                            HARD
                            EXTRA HARD
         Factory Default: EASY
```

Table at the foot of a-05 (column group headings `Game Start`, `Ball Start`, `Memory`, each over a boxed `START CHALLENGE`):

| Difficulty | Game Start START CHALLENGE | Ball Start START CHALLENGE | Memory START CHALLENGE |
| --- | --- | --- | --- |
| Extra Easy | -- | yes | yes |
| Easy | yes | -- | yes |
| Medium | -- | -- | yes |
| Hard | -- | -- | no |
| Extra Hard | -- | -- | no |

```
5
```

### a-06 (printed page 6)

```
NEW Feature Adjustments:

A.2 13   ENDGAME LOCK REL.
         This determines whether balls locked in the ZR-1/LT-5 lockup are released or held at the
         end of a game.

         Setting:           YES
                            NO

         Factory Default: YES

A.2 14   ENABLE DEF SAVER
         This determines whether the DEFAULT ball saver is enabled (see A.2 05 above).

         Setting:           YES
                            NO

         Factory Default: NO

A.2 15   ENABLE CENSOR
         This determines whether the FUTURE CAR CHAMPION initials are censored before
         being displayed on the shooter groove car's license plate.

         Setting:           YES
                            NO

         Factory Default: NO

A.2 16   DISABLE ZR-1/LT-5
         This disables the ZR-1/LT-5 engine assembly in the event that it becomes broken and
         lock-down bracket is installed.

         Setting:           YES
                            NO

         Factory Default: NO

A.2 17   NO MATCH SPEECH
         This determines whether the end of match speech "Hey, these number don't match!" is
         said when the game is set for CREDIT PLAY. The speech is always said when the game
         is set for FREE PLAY.

         Setting:           YES
                            NO

         Factory Default: NO

6
```

## Uncertain readings

No unreadable words. Printed quirks kept literally (verified in crops under `review-artifacts/corvette-1994/scratch/rules/`):

- m-032 T.4: `if; more then one solenoid` and `display. and the corresponding` (crop `m032_t4.png`).
- m-035 T.17: `until the "LEFT START" optical switch is` / `closes.` and the same for RIGHT HOME, as printed.
- a-02 T.17: `RIGHT FORWARD - This test drives the left car in reverse while the "ENTER" button is pressed.` is printed exactly so (crop `a02_rf.png`); it contradicts the label and the manual's own `RIGHT FORWARD` text on m-035.
- a-04: Hard column headers print `U.0 04` in both difficulty tables (crops `a04_t1.png`, `a04_t2.png`); the Preset table title prints as `U.S./Canadian Games` (the scan renders the "i" of "Canadian" without its dot in crop `a04_t3.png`, read as "Canadian").
- a-04 and a-05: the table cell dashes `--` are printed as double hyphens.
- The amendment prints straight double quotes that look like `'"'` at low resolution; transcribed as `"`.
- m-031 menu entry `T.14 Lamp Row-ColTest` (no space before "Test") is printed that way; the body text header reads `T.14 Lamp Row-Col Test`.
