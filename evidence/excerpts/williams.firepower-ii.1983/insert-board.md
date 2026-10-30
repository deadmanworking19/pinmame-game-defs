# Insert-board switched lamps and conflicting address

The curator visually checked native PDF41, insert-board drawing, and
PDF50-51 switched-lamp spread of the retained manual. The crop reproduces the
six switched lamp branches; it is a drawing, not a table screenshot.

9P1-13 YEL-BRN is COL.1, common to 9B1..9B6. Pin14 COL.6 is NC.
9B1 GAME OVER, diode9D1, ROW1 RED-BRN, pin5;
9B2 MATCH,9D2,ROW2 RED-BLK,pin6;
9B3 TILT,9D3,ROW3 RED-ORN,pin7;
9B4 HIGH SCORE,9D4,ROW4 RED-YEL,pin8;
9B5 SHOOT AGAIN,9D5,ROW5 RED-GRN,pin9;
9B6 BALL IN PLAY,9D6,ROW6 RED-BLU,pin10.
These are literal drawn connections. Column1/row6 corresponds to public6,
whereas Figure1 calls6 Shoot Again (playfield) and40 Ball in Play. PDF51
classifies6 BACKBOX and40 NOT USED, yet repeats the same functional legend.
Figure1/Figure2/PDF51 legends are reprints in one manual, not independent votes.

IPDB50054 shows actual insert-board lamps and displays, but no readable wire
colours or socket numbers. IPDB50030 shows the illuminated glass; its footer
is too dark/small to trace all six captions to sockets. Neither identifies
which matrix bit powers a Ball in Play bulb. The ROM sets40 on Start and
clears40 on tilt; that demonstrates meaningful state only. The retained scripts
omit40, which is not physical absence evidence.

Disposition: do not assert40 is an unfitted virtual lamp. Keep40 as a lamp
with unknown physical availability and conflicted routing/fitment. A meaningful
ROM bit does not establish a fitted load. Playfield6 is independently
visible in the playfield photograph; an additional backbox bulb at the same
bit remains disputed. A powered continuity/socket-to-pin inspection of an
original model521 insert board is required to settle the conflict. ROM traces
cannot choose between these physical connections.
