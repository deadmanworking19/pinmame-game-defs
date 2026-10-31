# Terminator 3 — Diagnostic Aids and CPU DIP Switch Settings

Read from `Stern_2003_Terminator_3_Rise_of_the_Machines_Pinball_Game_Service_Manual.pdf`, PDF page 5, the front-matter
drawing printed `DR. 3`. Read from a 200 dpi render; the quoted paragraphs were checked against the page's text layer,
whose re-encoded font decodes with a constant character shift.

## Diagnostic Aids (upper half)

Display `OPEN THE DOOR`: "If this display flashes, the game is indicating that CMOS RAM memory (CPU Loc. U212) has been
corrupted. This is caused be either failure in memory (e.g. batteries are dead and/or faulty RAM) or upon installation of
updated version of game code. Opening the Coin Door will initiate a Factory Restore (Reset), by opening the Memory Protect
Switch. Check battery voltage at VBATT Test Point on the CPU/Sound Bd. (more details in Section 5, Chapter 4, PCBs)."

Display `OPERATOR ALERT! / #2 AUTO LAUNCH / COIL MALFUNCTION`: "This display is shown momentarily during Game Mode or
Power-Up to alert the operator of a coil malfunction (coil doesn't energize or coil fires a multiple number of times).
OPERATOR ALERT! works by monitoring any switch activated coil that has the potential to trap a ball when disabled (e.g. in
the Auto Launch, Scoop, Eject, etc.). This alert can also appear if a switch associated with a coil (e.g. #16 Shooter Lane
& #2 Auto Launch) is stuck closed (caused by a switch jam or stuck ball); the CPU/Sound Board will activate the coil
approximately ten times and if the switch remains closed, the game will report this switch in Technician Alerts & will
indicate the following display warning:"

Display `PLEASE CHECK / TECH REPORT / PORTALS->DIAG->TECH`: "If this Tech Report Alert flashes (along with an audible
sound), the game has detected faulty switches and/or missing pinballs. Select the "TECH" Icon for information (review
Technician Alerts, Pages 24-25). For this Alert display to appear, Standard Adj. 49, must be changed to POWERUP, COIN DOOR
or POWERUP AND COIN DOOR, the default is NEVER (review Section 3, Chp. 4, GO TO ADJUSTMENTS MENU, Standard Adjustments,
Page 44)."

## CPU DIP Switch Settings (lower half)

Heading: "Location of Dip Switch [SW300] is on the CPU/Sound Board (Right of CN6, Top Middle)", over a board drawing with
SW300 labelled "8-Pos. Dip Sw." beside CN6, U205 and U401. Each chart is headed `CPU COUNTRY SETTING:` with positions 1-8
and an `ON` row and an `OFF` row; a triangle marks the position's setting. No chart leaves a position unmarked.

| Country | ON | OFF |
| --- | --- | --- |
| USA | (none) | 1, 2, 3, 4, 5, 6, 7, 8 |
| Austria | 1 | 2, 3, 4, 5, 6, 7, 8 |
| Australia | 1, 3, 4 | 2, 5, 6, 7, 8 |
| Belgium | 2 | 1, 3, 4, 5, 6, 7, 8 |
| Canada | 1, 2 | 3, 4, 5, 6, 7, 8 |
| Denmark | 1, 4 | 2, 3, 5, 6, 7, 8 |
| Finland | 1, 3 | 2, 4, 5, 6, 7, 8 |
| France | 2, 3 | 1, 4, 5, 6, 7, 8 |
| Germany | 1, 2, 3 | 4, 5, 6, 7, 8 |
| Greece | 1, 2, 3, 4 | 5, 6, 7, 8 |
| Italy | 4 | 1, 2, 3, 5, 6, 7, 8 |
| Netherlands | 3 | 1, 2, 4, 5, 6, 7, 8 |
| New Zealand | 5 | 1, 2, 3, 4, 6, 7, 8 |
| Norway | 2, 4 | 1, 3, 5, 6, 7, 8 |
| Portugal | 1, 5 | 2, 3, 4, 6, 7, 8 |
| Spain | 2, 5 | 1, 3, 4, 6, 7, 8 |
| Sweden | 1, 2, 4 | 3, 5, 6, 7, 8 |
| Switzerland | 3, 4 | 1, 2, 5, 6, 7, 8 |
| UK | 2, 3, 4 | 1, 5, 6, 7, 8 |

The page is signed `Find-It-In-Front: Dr. Pinball` and `DR. 3`.

## Curator's observations (not printed)

- No country turns positions 6, 7 or 8 on; positions 1-5 carry every country code.
