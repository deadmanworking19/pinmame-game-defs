# Curators, tests and determinism

On-demand companion to `docs/INSTRUCTIONS.md`. Read it before steps 6 and 7 of the per-game workflow, and before writing or changing a curator, test, guard or manifest; it is not loaded by default.
The runbook wins where the two disagree.

**Belongs here:** how to write curators, tests, guards and manifests that fail when they should and reproduce byte for byte.

**Does not belong here:** the required gates and regeneration commands (`docs/INSTRUCTIONS.md`, steps 6 and 7).

## Lessons

Each lesson ends with the lines of `docs/archive/current-state-ledger-until-2026-10-01.md` that
record the case behind it, and with `verified:` where it was checked against the repository code or
pinned PinMAME source on 2026-10-01. A lesson added later names the commit or knowledge note that
produced it instead.

- **Prove each guard can fail.** Mutation-check every guard, or run it against the historical wrong wordings it exists to catch. A mis-escaped regex and a string broken by concatenation have both shipped as guards that could never fail. Assert identities, not counts. (archive L243, L264, L953, L1050)
- **Sibling-derived records.** When a record starts from a sibling's curator, assert that none of its artifacts names another machine's IDs or short names, or the sibling's game data, generation constant or table build. Build that forbidden set from `catalog/pinmame.json`; a hand-written blacklist only tests your memory. (archive L949; verified: test_lethal_weapon_3.py)
- **Script claims are tests.** Gate prose such as "the script never touches X" against a pinned address set. Scan for that set case-insensitively and recheck it against the script whenever evidence is present. The set is a lower bound: it can disprove an avoidance claim but never prove one. (archive L249, L953)
- **Recompute stated numbers.** Recompute every figure in an observation label from the raw runs, and every hard-coded coordinate from `gameitems`. (archive L306, L660)
- **Sidedness is checked everywhere.** `tests/test_spatial_sidedness.py` covers every record. Never swap observed coordinates to make it pass; a real inversion you keep needs a `KNOWN_INVERSIONS` entry. (archive L653, L804, L898; verified)
- **Reuse shared rules.** Tests read the shared constants rather than copying their values. Curators import `unresolved_conflicts` from `pinmame_game_defs.conflicts` rather than re-implementing it. (archive L1050, L1094; verified)
- **`--check` proves self-consistency only.** When a shared pass such as `import-opdb` adds fields to a record, add them to that record's curator too, or the next regeneration silently drops them. (archive L1096)
- **Manifests and timestamps.** Build manifests with `tools/build_external_evidence_manifest.py`, which sorts paths case-sensitively. Sorting `Path` objects is case-insensitive on Windows. Recompute a legacy case-insensitive manifest; never re-pin it. Take times from retained manifests, never from the clock. (archive L522, L1151; verified)
- **Pinned evidence is immutable.** Add new data in a successor file and pin both files. If a pinned run folder moves, keep its internal paths unchanged and disclose the move. (archive L660, L662)
