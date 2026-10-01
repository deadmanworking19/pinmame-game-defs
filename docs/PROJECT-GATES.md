# Project gates and final handoff

On-demand companion to `docs/INSTRUCTIONS.md`. Read it before claiming project-level completion, before a final handoff, and when a change could affect a project-wide gate; it is not loaded by default.
The runbook wins where the two disagree.

**Belongs here:** the gates the whole project must prove before it is complete, and the final handoff.

**Does not belong here:** per-game promotion rules (`docs/INSTRUCTIONS.md`).

## Completion gates

Per-game success is necessary but not sufficient. Keep working until every gate below is proved by current generated artifacts and tests, or until the user explicitly stops the run:

- The exact pinned `PinmameGetGames` result is captured from the resolved native PinMAME library; every in-scope driver appears exactly once, every retained clone parent resolves, every reviewed virtual-only exclusion remains absent, physical-family exceptions are explicit, and catalog regeneration is byte-for-byte deterministic. Environment-dependent ROM availability such as `PinmameGame.found` is local-report data and must not affect canonical hashes.
- PinMAME structural extraction records controller generation, active groups/counts, remaps, common inputs, emulator normalization, output types, displays, custom ranges, and simulation/mech hook presence with the exact PinMAME revision. Generic generated labels are scaffolding, never validated semantics.
- Both pinned VPX script corpora are inventoried deterministically, every eligible script is hashed, controller IDs and I/O/mechanism candidates are extracted with exact locators, table revisions are grouped without erasing provenance, conflicts remain first-class, and parser inference never rises above candidate status by itself.
- The legacy 11-class managed corpus and old JSON corpus remain covered by migration/compatibility fixtures, including numeric and zero-padded aliases, negative diagnostics, platform-specific merge behavior, duplicate/collision cases, direct flipper relationships, and authored mech reverse resolution. The hint migration report explicitly drops all authoring hints, and unresolved semantic device references hard-fail rather than silently becoming controller ID `0`.
- Schema and semantic validation reject invalid JSON, stale generated files, duplicate or illegal bindings, alias cycles, dangling imports/models, mixed ID types, unsupported transports, illegal re-inversion, ambiguous inheritance, spatial violations, and dishonest promotion. Representative valid artifacts and every known failing fixture are tested.
- Runtime evidence uses the pinned library and legally supplied ROMs in isolated per-run state. Run manifests pin ROM and emulator hashes, NVRAM initialization, service language, actions, timeouts, normalized observations, and output/display checkpoints. ROM bytes and NVRAM blobs remain external; host input readback is never treated as ROM evidence; wrong-switch, wrong-output, wrong-idle-state, and wrong-mechanism fixtures must fail clearly.
- Every physical-game record in the generated catalog is `author_ready`, every supported physical/controller variant is accounted for, and the generated completion gate is true. Stubs contribute zero coverage; partials are not publishable as complete entries; the non-game records (the retained diagnostic plus the twelve test-fixture/test-chip/tester/boot-flash drivers classified `diagnostic_software`) remain separately classified.
- Machine families and cited edition-difference prose are complete without conflating unrelated titles or collapsing edition-specific devices, geometry, mechanisms, or compatibility.
- All reviewed curation work is integrated on `master`, no required change remains only in a worktree, generated catalogs/reports match the integrated tree, and completed branches/worktrees are safely cleaned.

## Final curation handoff

External contributors submit a focused PR targeting `master` and wait for maintainer review; they do not merge their own contribution. Maintainers perform the final evidence/code review and own integration decisions.

The curation project is complete only when every in-scope physical PinMAME machine resolves to an exact definition and every record is honestly classified. The final handoff must include coverage totals, remaining partial/stub blockers if the user stops early, validation results, branch/commit locations, retained evidence locations, and confirmation that completed worktrees were cleaned.
