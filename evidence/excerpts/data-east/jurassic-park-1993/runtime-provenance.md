# Exact runtime provenance and external manifest

```json
{
  "command_template": "python -B tools/jurassic_park_harness.py --library <pinned pinmame64.dll> --game jupk_513 --rom-path <read-only user ROM root> --work-dir <new isolated state> --scenario <committed scenario> --boot-wait 8 --dmd-dir <new snapshot directory> --output <raw run.json>",
  "executed_harness": {
    "executed-checkpoint-adapter.py": "84089f836a72a7281cea8bfc8bfd468c8e8bd592b20ce67301b99a3b226fff25",
    "executed-generic-harness.py": "18ae798e99a9803541095920e4b71dbf87f467c0d6008041ebef5229c1416c59"
  },
  "format": "pinmame-runtime-provenance",
  "game": "jupk_513",
  "language": "US English 5.13 (jpdspa.510 display)",
  "library_sha256": "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c",
  "machine_id": "data-east.jurassic-park.1993",
  "manifest": {
    "algorithm": "build_external_evidence_manifest.py: every sorted relative POSIX path with size and SHA256; UTF8 compact JSON object sorted keys, final newline; exclude manifest.json and manifest.sha256 only.",
    "directory": "external:pinmame-review-artifacts/data-east.jurassic-park.1993/session-20261001/runtime",
    "sha256": "3aa00092ff8c0b5e223ee7772a00d8f2f33f7237f3c01d9e1e595759305a367c"
  },
  "pinmame_revision": "8371478a7640f1896dcdf565aed340dc5df989ba",
  "rom": {
    "access": "Read-only user-supplied ROM root; no bytes copied or committed",
    "archive": "jupk_513.zip",
    "driver_check": "every member's CRC32 and SHA1 equals the pinned degames.c jupk_513 entry",
    "members": {
      "jpcpua.513": {
        "crc32": "9f70a937",
        "sha1": "cdea6c6e852982eb5e800db138f7660d51b6fdc8",
        "size": 65536
      },
      "jpdspa.510": {
        "crc32": "9ca61e3c",
        "sha1": "38ae472f38e6fc33671e9a276313208e5ccd8640",
        "size": 524288
      },
      "jpu17.dat": {
        "crc32": "38135a23",
        "sha1": "7c284c17783269824a3d3e83c4cd8ead27133309",
        "size": 524288
      },
      "jpu21.dat": {
        "crc32": "6ac1554c",
        "sha1": "9a91ce836c089f96ad9c809bb66fcddda1f3e456",
        "size": 262144
      },
      "jpu7.dat": {
        "crc32": "f3afcf13",
        "sha1": "64e12f9d42c00ae08a4584b2ebea475566b90c13",
        "size": 65536
      }
    },
    "sha256": "8ea2e98f44b7904ad61ab336b2e668c382387dac2155c426c8d561a8f0119ea6"
  },
  "runs": [
    {
      "raw": "active-switch-test/run.json",
      "scenario": "tools/harness-scenarios/data-east/jupk-513-active-switch-test.json",
      "scenario_sha256": "7377ef0e703daa0385c10f0da796740dec86358137d95889fc52f3fa8b221a0b",
      "sha256": "5b55fa855f6eae8c0d92e661210b1c22091647fb5f0c201ecb9ecb061e4323f0",
      "state": "active-switch-test/state"
    },
    {
      "raw": "lamp-test/run.json",
      "scenario": "tools/harness-scenarios/data-east/jupk-513-lamp-test.json",
      "scenario_sha256": "647d9d422daf52a9681438c0b2b43adbae5bfb0fd9c307a8b9030b427b9c385e",
      "sha256": "d9fde7636c9e170361d863c9a21e1a605266436c666fb68b0ac94d91c06f631f",
      "state": "lamp-test/state"
    },
    {
      "raw": "coil-cycle/run.json",
      "scenario": "tools/harness-scenarios/data-east/jupk-513-coil-cycle.json",
      "scenario_sha256": "9e81e190c2a0c5f7f718530b136c51a76d602cad7a8fd6c78a6d313a8348fee3",
      "sha256": "03016c1b14140aa95558d295f417d94bd2d02941f6fb76ddddc8211c057d7046",
      "state": "coil-cycle/state"
    },
    {
      "raw": "coil-cycle-trex-homed/run.json",
      "scenario": "tools/harness-scenarios/data-east/jupk-513-coil-cycle-trex-homed.json",
      "scenario_sha256": "65ba32d976107c59439fcbcb684bbc2bf9ac3fb3e7f334bd39892787b5ac190e",
      "sha256": "de0e1ef28fa381957d446caa5b3dc9ed61850f95bdf9edc5138fe384b13477b4",
      "state": "coil-cycle-trex-homed/state"
    },
    {
      "raw": "laser-kick-test/run.json",
      "scenario": "tools/harness-scenarios/data-east/jupk-513-laser-kick-test.json",
      "scenario_sha256": "69c64f2851d3f5b934433ecea3fcb4916b7179354945f17252b88fdca466f761",
      "sha256": "9b513a816b8e194921ef9bc2feb2ecbdd15ac9d39f76314fe8e3fe26cfdfba5a",
      "state": "laser-kick-test/state"
    },
    {
      "raw": "trex-test/run.json",
      "scenario": "tools/harness-scenarios/data-east/jupk-513-trex-test.json",
      "scenario_sha256": "8869aea1c6dd9813514d267017328d2a5f9570ee00eb34c75903139550f7f056",
      "sha256": "6540d0b09b5b4b13099d5aa20549e485ff5141a98260fac03ed11bd650700652",
      "state": "trex-test/state"
    }
  ],
  "setup": {
    "boot_wait_s": 8,
    "handle_mechanics": 0,
    "initial_switches": {
      "all other runs": [],
      "coil-cycle-trex-homed": [
        36,
        57
      ]
    },
    "keyboard": "Active Switch run: no named keys, so keyboard handling stays off (Green held at 1, Black pulsed as switch -7, flipper buttons as 84/82). The lamp, T-Rex and coil-cycle runs use named service keys; their direct switch writes (57, 36, 41, 29...) address matrix positions the keyboard port does not own.",
    "reset": "Fresh separately named state directory for each evidentiary run (removed and recreated before the run); no imported NVRAM or exploratory state",
    "witness": "Exploratory runs (explore1-4) used separate state directories and are not cited as evidence."
  },
  "version": 1
}
```
