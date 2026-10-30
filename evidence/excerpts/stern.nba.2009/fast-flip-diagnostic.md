# Stern NBA (2009) — public solenoid 33 (S.A.M. game-on state) diagnostic

Status: transcribed from the retained diagnostic logs by the curator; the log lines below are copied verbatim.

## Why this run exists

Pinned PinMAME `src/wpc/sam.c` (revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`) sets `samlocals.fastflipaddr = 0x010609be` for `nba_802` only (line 1707-1708); no other `nba_` driver has a fast-flip address. Its VBLANK handler (lines 2258-2268) reads the 16-bit game-RAM word at that address with `cpu_readmem32ledw` and, while it equals `0x01`, sets `coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + SAM_FASTFLIPSOL - 1].value = 1.0f` (public solenoid 33); otherwise it sets it to 0.

None of the retained `nba_802` harness runs (boot-start, gameplay probe, bumper and slingshot probe) records a solenoid event for public 33. The diagnostic below re-ran the gameplay probe to tell apart "the ROM never sets the word" from "the word is set but the callback never reports it".

## Run

| Field | Value |
| --- | --- |
| Directory | working root `review-artifacts/nba-2009/diagnostics/fastflip-getter-nba_802/`, manifest `manifest.json` SHA-256 `4a7fa5a7d915136e0a15458e2d27c18a97a3e0205f4c721f23aec950b379bbfa` |
| Driver | `nba_802` |
| Emulator | `pinmame64.dll` built from `46e1a01a0f73dc5ce163d98db1ae435883ecc450`, SHA-256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5` |
| Scenario | `tools/harness-scenarios/stern/nba-2009-gameplay-probe.json` (the same scenario as the retained gameplay probe) |
| Wrapper | `memprobe.py` (retained in the run directory, SHA-256 `ccfff80e339ecec2b06dfd8dd315cf760f2b2dc630ab651caec409fc2bc10360`): runs `tools/run_pinmame_harness.py` unchanged, and after each of the harness's output polls reads 8 bytes of main-CPU memory at `0x010609be` with `PinmameReadMainCPUMemory` and calls `PinmameGetSolenoid(33)`, logging a line whenever either value changes |
| Raw trace | `run.json` SHA-256 `23659cef818fbfb042917f94f4a188fbac7c5d1238902cd9548bf69b53d6ec51` |
| Log | `fastflip-word.json` SHA-256 `1c5338521ceb2509644d0ea5496275098eee83de0f7dd5e3e801e3490b0016af` |

## Log (verbatim, three entries)

| `event_index` | `got` | `bytes` | Nearest trace event |
| ---: | ---: | --- | --- |
| 4 | 8 | `0000000000000000 get33=0` | before the first display frame (0.43 s) |
| 5 | 8 | `0000080000000004 get33=0` | 1.06 s, first display frame |
| 11661 | 8 | `0100080000000004 get33=1` | 36.43 s; the Start button press (step 10) is at 36.39 s |

The first two bytes are the little-endian word `sam.c` tests: it becomes `0x0001` about 40 ms after Start is pressed, and `PinmameGetSolenoid(33)` returns 1 from the same poll. Neither value changes again before the run ends at 114.82 s (through the served ball, flipper presses, both ejects, the drop-target bank and the basket opto).

The raw trace of the same run holds **no** `solenoid` event for public 33.

## Comparison run on another S.A.M. game

| Field | Value |
| --- | --- |
| Directory | working root `review-artifacts/nba-2009/diagnostics/fg-boot-pinned-dll/`, manifest SHA-256 `e276c220edc033dcd1d0982fe219c9a3d7e6dd64e7dd46dfc6d0fe128564aa39` |
| Run | `fg_1200ag` (Family Guy) boot-start with the same emulator build: initial switches 18, 19, 20, 21, 55, 83, 81; six coins on 65; Start on 16 |
| Raw trace | `run.json` SHA-256 `4e4bfa661b3e0c965cda2f42fec0f88664b8cd21fd474187d7b09794b52d45bf` |
| Solenoid addresses with events | 1, 19, 20, 24 |

The committed Family Guy boot-start summary `evidence/runtime/sam/family-guy-fg_1200ag-boot-start.json`, recorded with the older build `deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c` (PinMAME `8371478a7640f1896dcdf565aed340dc5df989ba`) and the same switch and pulse sequence, lists solenoid addresses 1, 19, 20, 24 and 33.

## Reading

On `nba_802` the ROM sets the fast-flip word at game start and PinMAME publishes public solenoid 33 as 1 to a caller that polls it. The pinned LibPinMAME build does not deliver that state through its `OnSolenoidUpdated` callback, on NBA or on Family Guy, while the older build did on Family Guy. A consumer that only listens for solenoid callbacks never sees public 33 with this build.
