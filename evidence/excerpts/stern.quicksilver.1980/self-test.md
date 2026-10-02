Source: `Stern_1980_Quicksilver_Manual.pdf` (IPDB machine 1895, "English Manual [Stern Electronics]", 35 pages, a 300 dpi bilevel scan with no text layer), PDF page 4, section `II. ROUTINE MAINTENANCE ON LOCATION:` (text page; read from the 300 dpi render and checked against Windows.Media.Ocr).

`MPU MODULE SELF-TEST:` During power-up the MPU tests itself, shown by a LED on the board flashing once, pausing, then flashing six more times
and going out; a tune then announces game readiness.

`GAME SELF-DIAGNOSTIC TESTS:` Pressing the Self-Test button inside the coin door one time activates the self-diagnostic test, in this order:

1. Feature lamps: all feature lamps flash on and off continuously, determining any burnt lamps.
2. Pressing the Self-Test button again makes each digit on all displays cycle from 0 through 9, repeating continuously.
3. Pressing it again energizes each solenoid, one at a time, in a continuous sequence. Holding both flipper buttons in during this test
   energizes the flipper coils. The number on the Player Score displays is the number assigned to the solenoid.
4. Pressing it again makes the MPU look at each switch assembly for stuck contacts. If any are stuck, the number of the first one
   encountered flashes on the Player Score displays and remains until the fault is corrected. Other numbers may follow. If none are
   stuck, the Match/Ball in Play display flashes `0`. Flipper button switches are not included.
5. Pressing it eighteen more times steps through the game levels and bookkeeping functions and finally repeats the power-up test.
