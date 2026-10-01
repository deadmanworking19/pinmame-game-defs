# Identity, variants and records

On-demand companion to `docs/INSTRUCTIONS.md`. Read it before step 2 of the per-game workflow, and before grouping drivers, splitting or merging records, choosing an OPDB identity or setting `physical_compatibility`; it is not loaded by default.
The runbook wins where the two disagree.

**Belongs here:** how drivers group into physical machines and editions, when a record splits, identity and compatibility decisions, and machine families.

**Does not belong here:** one machine's identity facts (its definition and knowledge note), or the scope-exception set (`src/pinmame_game_defs/scope.py`, summarized in `docs/CURRENT-STATE.md`).

## Rules

### Machine families and edition prose

After the spatial-update backlog, add a stable `machine_family` identifier that groups the editions of one physical title, for example a manufacturer's Pro, Premium, Limited Edition, and Vault builds of the same game. Keep unrelated games in different families even when they share a theme or a licensed name, including cases where two manufacturers released differently titled machines from the same licence. Research and cite concise prose explaining the physical and rules/hardware differences among editions. A family identifier enables navigation and shared evidence; it must not erase edition-specific devices, geometry, mechanisms, or driver compatibility.

## Lessons

Each lesson ends with the lines of `docs/archive/current-state-ledger-until-2026-10-01.md` that
record the case behind it, and with `verified:` where it was checked against the repository code or
pinned PinMAME source on 2026-10-01. A lesson added later names the commit or knowledge note that
produced it instead.

- **OPDB identity is gated by code.** `import-opdb [--check]` (`opdb.py`) rejects a resolved identity that disagrees with its OPDB record on title tokens (edition words count), year (more than one apart), manufacturer, an unlisted parenthetical qualifier, or the root description. It also rejects an override that lacks a reason, a cross-manufacturer override without an HTTPS `evidence_url`, and a redundant override. `promote_catalog_stubs.py --check-structure` rejects two resolved claimants of one ID. (archive L153, L197, L1080; verified)
- **Identity is still a curator's job.** Never apply `machines/opdb_id.csv` blindly; choose the physical edition's record through a reasoned override. If the snapshot lacks a record, leave `identity` missing. A record split off a production machine keeps that machine's ID only as a lead. (archive L159, L197, L288, L1082)
- **A clone can be another machine.** A driver on a different CPU board or controller generation is a separate record even when PinMAME declares it a clone; a board-swap conversion becomes `physical_conversion`. A shared short-name prefix proves nothing. Test that split drivers never rejoin. (archive L288, L508, L679, L697, L863)
- **`physical_compatibility`.** A different GEN constant, sound system or display layout makes a driver `compatible` (`identical` cannot carry `display_overrides`); firmware provenance alone does not, so a community ROM that changes only the music on unchanged hardware stays `identical`. Firmware that needs hardware the machine lacks makes it `different`. Shared init proves routing, not cabinet hardware, so a folded-in edition stays `unknown` until a source describes it. (archive L831, L840, L1036; verified: validation.py)
- **Years.** `machine.year` is the physical release year. A catalog year can be a firmware date and stays on that driver; a manual copyright can be a reprint. (archive L854, L934)
