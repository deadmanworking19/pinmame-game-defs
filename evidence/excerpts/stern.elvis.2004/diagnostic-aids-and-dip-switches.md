# Elvis (Stern) — Diagnostic Aids and CPU DIP Switch Settings

Read from `Elvis_Manual.pdf`, PDF page 5, the front-matter drawing printed `DR. 3` ("DIAGNOSTIC AIDS" and "CPU DIP
SWITCH SETTINGS"), from a 220 dpi render; each country chart was read from a crop of that render. The page's text layer
carries the country names but not the switch marks.

## Diagnostic aids (verbatim)

- Display "OPEN THE DOOR": "If this display flashes, the game is indicating that CMOS RAM memory (CPU Loc. U212) has
  been corrupted. This is caused be either failure in memory (e.g. batteries are dead and/or faulty RAM) or upon
  installation of updated version of game code. Opening the Coin Door will initiate a Factory Restore (Reset), by
  opening the Memory Protect Switch. Check battery voltage at VBATT Test Point on the CPU/Sound Bd. (more details in
  Section 5, Chapter 4, PCBs)."
- Display "OPERATOR ALERT! / #2 AUTO LAUNCH / COIL MALFUNCTION": "This display is shown momentarily during Game Mode or
  Power-Up to alert the operator of a coil malfunction (coil doesn't energize or coil fires a multiple number of times).
  OPERATOR ALERT! works by monitoring any switch activated coil that has the potential to trap a ball when disabled
  (e.g. in the Auto Launch, Scoop, Eject, etc.). This alert can also appear if a switch associated with a coil (e.g.
  #16 Shooter Lane & #2 Auto Launch) is stuck closed (caused by a switch jam or stuck ball); the CPU/Sound Board will
  activate the coil approximately ten times and if the switch remains closed, the game will report this switch in
  Technician Alerts & will indicate the following display warning:"
- Display "PLEASE CHECK / TECH REPORT / PORTALS->DIAG->TECH": "If this Tech Report Alert flashes (along with an audible
  sound), the game has detected faulty switches and/or missing pinballs. Select the "TECH" Icon for information (review
  Technician Alerts, Pages 24-25). For this Alert display to appear, Standard Adj. 49, must be changed to POWERUP, COIN
  DOOR or POWERUP AND COIN DOOR, the default is NEVER (review Section 3, Chp. 4, GO TO ADJUSTMENTS MENU, Standard
  Adjustments, Page 44)."

## CPU DIP switch settings

Heading line, verbatim: "Location of Dip Switch [SW300] is on the CPU/Sound Board (Right of CN6, Top Middle)". The
drawing between the charts shows CN6 (pins 1-12, "DEDICATED SWITCH IN") and an eight-position switch labelled `SW300`,
`ON` and `KSD08H`, positions 1-8.

Each chart prints "CPU COUNTRY SETTING:", the country, and a `Pos. 1-8` row with an `ON` line (up triangle) and an
`OFF` line (down triangle). Every position carries exactly one mark. Positions set ON, as drawn:

| Country | ON positions | OFF positions |
| --- | --- | --- |
| USA | none | 1-8 |
| Austria | 1 | 2-8 |
| Australia | 1, 3, 4 | 2, 5-8 |
| Belgium | 2 | 1, 3-8 |
| Canada | 1, 2 | 3-8 |
| Croatia | 2, 3, 5 | 1, 4, 6-8 |
| Denmark | 1, 4 | 2, 3, 5-8 |
| Finland | 1, 3 | 2, 4-8 |
| France | 2, 3 | 1, 4-8 |
| Germany | 1, 2, 3 | 4-8 |
| Greece | 1, 2, 3, 4 | 5-8 |
| Italy | 4 | 1-3, 5-8 |
| Japan | 1, 3, 5 | 2, 4, 6-8 |
| Netherlands | 3 | 1, 2, 4-8 |
| New Zealand | 5 | 1-4, 6-8 |
| Norway | 2, 4 | 1, 3, 5-8 |
| Portugal | 1, 5 | 2-4, 6-8 |
| So. Africa | 3, 5 | 1, 2, 4, 6-8 |
| Spain | 2, 5 | 1, 3, 4, 6-8 |
| Sweden | 1, 2, 4 | 3, 5-8 |
| Switzerland | 3, 4 | 1, 2, 5-8 |
| UK | 2, 3, 4 | 1, 5-8 |

No chart sets position 6, 7 or 8 ON.
