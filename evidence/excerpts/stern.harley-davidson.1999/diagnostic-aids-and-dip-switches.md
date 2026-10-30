# Harley-Davidson (Stern) — Diagnostic Aids and CPU DIP Switch Settings

Read from `Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf`, PDF page 5, the front-matter page
printed `DR. 3` ("Find-It-In-Front: Dr. Pinball"). The paragraphs are quoted from the page's text layer, which is legible
on this page; the headings and the switch charts are set in symbol fonts the text layer does not decode and were read
from a 200 dpi render.

## Headline

"For proper operation of this [HARLEY-DAVIDSON logo]® Pinball, FOUR (4) PINBALLS MUST BE INSTALLED!" (drawn beside four
balls).

## Diagnostic Aids

Display drawn "OPEN THE DOOR", verbatim: "If this display flashes, the game is indicating that CMOS RAM memory (CPU Loc.
U212) has been corrupted. This is caused be either failure in memory (e.g. batteries are dead and/or faulty RAM) or upon
installation of updated version of game code. Opening the Coin Door will initiate a Factory Restore (Reset), by opening
the Memory Protect Switch. Check battery voltage at VBATT Test Point on the CPU/Sound Bd. (more details in Section 5,
Chapter 4, PCBs)."

Display drawn "OPERATOR ALERT! / #2 AUTO LAUNCH / COIL MALFUNCTION", verbatim: "This display is shown momentarily during
Game Mode or Power-Up to alert the operator of a coil malfunction (coil doesn't energize or coil fires a multiple number
of times). OPERATOR ALERT! works by monitoring any switch activated coil that has the potential to trap a ball when
disabled (e.g. in the Auto Launch, Scoop, Eject, etc.). This alert can also appear if a switch associated with a coil
(e.g. #16 Shooter Lane & #2 Auto Launch) is stuck closed (caused by a switch jam or stuck ball); the CPU/Sound Board
will activate the coil approximately ten times and if the switch remains closed, the game will report this switch in
Technician Alerts."

## CPU DIP Switch Settings

"Location of Dip Switch [SW300] is on the CPU/Sound Board (Right of CN6, Top Middle)". The board drawing shows the
eight-position switch labelled "SW300", "ON", "KSD08H", positions 1-8, beside "CN6" (pins 1-12, "DEDICATED SWITCH IN"),
U206 and U204 (74HC245) and U205.

Each chart is headed "CPU COUNTRY SETTING:" with rows "Pos." 1-8, "ON" and "OFF"; an up arrow in the ON row or a down
arrow in the OFF row marks each position. Every chart marks every position once.

| Country | ON | OFF |
| --- | --- | --- |
| USA | (none) | 1 2 3 4 5 6 7 8 |
| Austria | 1 | 2 3 4 5 6 7 8 |
| Australia | 1 3 4 | 2 5 6 7 8 |
| Belgium | 2 | 1 3 4 5 6 7 8 |
| Canada | 1 2 | 3 4 5 6 7 8 |
| Denmark | 1 4 | 2 3 5 6 7 8 |
| Finland | 1 3 | 2 4 5 6 7 8 |
| France | 2 3 | 1 4 5 6 7 8 |
| Germany | 1 2 3 | 4 5 6 7 8 |
| Greece | 1 2 3 4 | 5 6 7 8 |
| Italy | 4 | 1 2 3 5 6 7 8 |
| Netherlands | 3 | 1 2 4 5 6 7 8 |
| New Zealand | 5 | 1 2 3 4 6 7 8 |
| Norway | 2 4 | 1 3 5 6 7 8 |
| Portugal | 1 5 | 2 3 4 6 7 8 |
| Spain | 2 5 | 1 3 4 6 7 8 |
| Sweden | 1 2 4 | 3 5 6 7 8 |
| Switzerland | 3 4 | 1 2 5 6 7 8 |
| UK | 2 3 4 | 1 5 6 7 8 |

No chart sets position 6, 7 or 8 ON.
