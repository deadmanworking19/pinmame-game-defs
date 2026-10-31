# Williams Barracora (game 510) - Identity

Sources:

- IPDB machine 177, `https://www.ipdb.org/machine.cgi?id=177`, retained as a Wayback Machine capture (`ARCHIVED ON 09:49:38 Nov 24, 2025`) at `external:pinmame-manuals/by-machine/williams.barracora.1981/ipdb-177.html`.
- The retained OPDB snapshot `external:pinmame-review-artifacts/opdb-import/latest-opdb.json` (SHA-256 `690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93`), entries `GRo7K` and `GRo7K-MQ4e3`.
- The pinned PinMAME `src/wpc/s7games.c` at `46e1a01a0f73dc5ce163d98db1ae435883ecc450`.
- The covers and title blocks of the three retained Williams documents.

Method: the IPDB page's text was extracted from the retained HTML and read; the OPDB entries were read from the snapshot JSON; the PinMAME block was read from the pinned source. Field values are quoted as they appear.

## IPDB 177 (header and fields, as captured)

- `Barracora / IPD No. 177 / September, 1981 / 4 Players`
- `Manufacturer: Williams Electronics, Incorporated (1967-1985) [Trade Name: Williams ]`
- `Date Of Manufacture: September, 1981`
- `Model Number: 510`
- `MPU: Williams System 7`
- `Type: Solid State Electronic (SS)`
- `Production: 2,350 units ( confirmed )`
- `Theme: Fantasy`
- `Notable Features: Flippers (2), Pop bumpers (3), Slingshots (2), Kick-out holes (2), Standup targets (3), 5-bank drop targets (1), 3-bank drop targets (1), Spinning target (1), Horseshoe lane (1), Rollunder (1). 2-ball and 3-ball multiball . Actual measured weight: 238 lbs (includes legs).`
- `Design by: Roger Sharpe , Steve Epstein , Barry Oursler`
- `Art by: Doug Watson`
- `Sound by: Ed Suchocki`
- `Software by: Ed Suchocki`
- The Notes field records that the name changed from 'Las Vegas' to 'Jet Orbit' to 'Barracora', which it gives as the reason for "the atypical placement of two alphabet letters on a single playfield insert".

## OPDB snapshot

- Group `GRo7K`, `Barracora`, year `1981`.
- Machine `GRo7K-MQ4e3`, `Barracora`, `physicalMachine: 1`, `ipdbId: 177`, `manufactureDate: 1981-01-09`, manufacturer `Williams` (`Williams Electronic Games, Inc.`), `type: ss`, `display: alphanumeric`, `playerCount: 4`.

## PinMAME (s7games.c at the pinned revision)

- `CORE_GAMEDEF(barra,l1,"Barracora (L-1)",1981,"Williams",s7_mS7S,0)`: one driver, `barra_l1`, no clones and no simulator.
- ROM members declared for `barra_l1`: `ic14.716`, `ic17.532`, `ic20.716`, `ic26.716` and sound `sound4.716`.
- `INITGAMEFULL(barra,s7_dispS7,34,35,0, 0,20,21,22,29,30)`: flipper-copy switches 34 and 35, no special switch for solenoid slot 17, and special switches 20, 21, 22, 29 and 30 for slots 18-22.
- Source comments beside the block: `// Tournament MOD exists: Bara_20.mod.716 & bara_26.mod.716 and/or ic14_l2_multiplier.716` and `// Barracora 2x/3x PF multiplier MOD exists (Sharpes)`. Neither mod is declared as a driver.

## Williams documents

- Instruction booklet: game 510, `16P-510-103` on its pages.
- Drawing set: `510` at the top of each drawing.
- Parts supplement: `16P-510-110`, October 1981; its ROM summary lists Sound ROM 4 (`parts-supplement.md`), which matches PinMAME's `sound4.716`.

## Notes

- IPDB 177, OPDB `GRo7K-MQ4e3`, model 510 and the PinMAME title agree on the machine.
- OPDB's `manufactureDate` 1981-01-09 differs from IPDB's September 1981; both give 1981. OPDB's `display: alphanumeric` does not describe the machine: the drawing set's insert board page draws seven-digit numeric player displays and a credits / ball-in-play board (`insert-board.md`).
