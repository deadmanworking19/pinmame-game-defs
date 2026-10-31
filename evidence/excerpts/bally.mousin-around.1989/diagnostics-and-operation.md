# Mousin' Around! — game rules, platform and diagnostic tests (PDF pages 4, 8, 40 and 47)

Source: `Bally_1989_Mousin_Around_Manual.pdf` (SHA-256
`6dcd83d1485a1b2e9909cc65b07d9ce23e1e7757e87cdf4a002984465b02d9f0`). Read from the pages rendered at 110-120
dpi, with the Windows OCR text used as a typing aid and checked against each render. Quoted text is verbatim,
including the manual's own punctuation.

## PDF page 4 — `MOUSIN'AROUND GAME PLAY RULES` (the whole page)

> **GOAL** The main object of MOUSIN' AROUND is to steal the Cheese, play Multi-ball™ and, score the Jackpot by
> trapping the Mice and sending the last one home to the Mouse Hole.
>
> **PLUNGER SKILL SHOT** Sending the ball through the Top Lanes when lit scores 100,000 points times the ball you
> are on. Therefore you earn 100,000 for ball 1; 200,000 for ball 2; 300,000 for ball 3, etc.
>
> **CHEESE FEATURE** Any ramp spots a letter in Cheese. After completing C-H-E-E-S-E the Mouse Hole opens for you
> to build your Jackpot. Then you are awarded a Cheezy Bonus, (Mystery Score anywhere from 100 to 500 points,
> Extra Ball, Special or, 1 Million Points). Any cheese taken will count for Outhole Bonus.
>
> **2X & 3X MULTIPLIER** Complete the Top Lanes once and earn the 2X Bonus Multiplier. Complete the Top Lanes
> twice and earn the 3X Bonus Multiplier.
>
> **MULTI-BALL™** Spell M-O-U-S-E T-R-A-P, either by hitting the stand-up Mouse Trap Targets or, by getting the
> ball through the lit Return Lanes. Spelling M-O-U-S-E T-R-A-P sets the Traps that lock the balls. Trap 2
> balls and the 3rd ball releases them when it is put into play.
>
> **JACKPOT** After Multi-ball™ is achieved, Traps remain up, you must trap the Mice again and send one home to
> the Mouse Hole to be awarded the Jackpot. Once the Jackpot is collected you can try for the Jackpot again &
> again. Jackpot resets for the next ball if collected.
>
> **MILLION** Hitting the Center Targets in sequence lowers the targets and, lights the Kickback. The Cheese Loop
> enables the Left & Right Ramps to spot letters in Million. After M-I-L-L-I-O-N is spelled, the Mouse Hole opens
> so you can collect 1,000,000 points.
>
> **EXTRA BALL** Shooting the Left Trap Lane consecutively lights ramps for Extra Ball.
>
> **DOUBLE PLAYFIELD SCORES** When making the Right or Left Ramp shots twice in a row, the Cheese Target starts
> flashing for increase value. Make the shot and Double Scoring has started.

## PDF page 8 — `Connector Identification` and `Circuit Boards` (first paragraph of each)

> Since MOUSIN' AROUND is using WILLIAMS ELECTRONICS GAMES System 11B, a new connector identification technique
> must be introduced.

> Prefix numbers for the System 11B circuit boards and other major assemblies are listed below.
>
> 1 - CPU · 2 - Master Interconnect · 3 - Backbox Power Supply · 4 - Alphanumeric Display · 5 - Aux Power Driver ·
> 6 - Backbox · 7 - Cabinet · 8 - Playfield · 9 - Insert Board · 10 - Sound Board

> System 11B Circuit Boards for MOUSIN' AROUND are in the backbox.

## PDF page 40 (footer `1-34 Test/Diagnostic Procedures`) — introduction

> MOUSIN' AROUND provides a series of diagnostic tests to aid the operator in determining game condition [...]
> In order, these tests deal with the motor bank, the music, the displays, the game sounds, the lamps, the
> solenoids, and the switches.

> To proceed to the Diagnostic Tests, the operator must simply switch the game on, set the AUTO-UP/MANUAL-DOWN
> switch to MANUAL-DOWN, and press the ADVANCE button.

## PDF page 47 (footer `Test/Diagnostic Procedures 1-41`)

> **C-SIDE TEST** From the Switch Test, press ADVANCE. Observe that the Player 1 and 2 displays show the message,
> C-SIDE TEST, and that the Player 3 displays shows 09 (C-Side Test identifier). This test confirms that the
> Solenoid A/C Select Relay (Sol. 12) is actually in the 'C' position (ready to power flashlamp circuits).
>
> The Player 1 and 2 displays then change to show the 'side' of the circuit being tested, alternating the A/C
> Relay between "SELECTED A-SIDE" and "SELECTED C-SIDE", while the Player 4 display shows the state of the
> C-Side Switch. When the switch is closed, the Player 4 display shows "C-SIDE".
>
> The message "Err" appears whenever the C-Side Switch is not operating properly. Causes of improper operation
> can be blown fuses (F8 or F2C) or a faulty relay on the Aux Power Driver Board; failure of the 12 or 24 volt
> power circuits; a switch matrix failure; or faulty connections between the circuit boards in the game's
> backbox (CPU Board, Aux Power Driver Board, Backbox Interconnect Board). To halt the A/C Relay's operation,
> press MANUAL-DOWN and press ADVANCE to activate the A/C Relay manually.

> **MOTOR TEST** In the Motor Test, the words "Motor Bank Test" appear in the player 1& 2 score display, the Motor
> Bank Targets rise. After a pause, the word "UP or Down" appear in the score display, and the Motor Bank Targets
> lower. If, during this test the word "ERROR" appears in the score display, there is a problem with one of the
> switches, located on the motor, that tells the CPU the position of the motor. Switch 43 tells the CPU that the
> Motor Bank is up therefore; if "UP ERROR" appears, switch 43 is not working. Switch 50 tells the CPU that the
> Motor Bank is down therefore; if "DOWN ERROR" appears, switch 50 is not working.

> **ENDING THE DIAGNOSTIC TESTS** To end the Diagnostic Tests, reach the C-Side Test (09 in the Player 3
> display), use AUTO-UP and press ADVANCE. The backbox displays should MANUAL-DOWN, and press ADVANCE to reach
> Adjustment Item 70 (INSTALL FACTORY). Use AUTO-UP, and press ADVANCE to go to the Attract Mode.
