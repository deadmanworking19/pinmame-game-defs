# S relay labels and public routing

Factory PDF 54 / printed 48 says S ON selects holes and S OFF selects paired #67 lamps for solenoids 1/2/5/6. The older exact script's `TopLeft/BotLeft/TopRight/BotRight` handlers branch to holes at `SStat = 0` and flash effects at `1`; `UpdateMultipleLamps` assigns `SStat = Light12.State`. The newer exact script lines 623-724 uses the same public predicate. These runtime routes are settled: public lamp `12 = 0` selects the hole branch and `12 = 1` the flash branch. The A3 drawing provisions Q13 at lamp 12, and the game wiring connects that branch to S. No physical armature/coil-energization sense is asserted from the public level.

The pinned parent-ROM gameplay probe ran from fresh empty state, `HandleMechanics = 0`, keyboard off and default binary outputs. Its exact raw SHA256 and scenario SHA256 are below. Every switch event in `host_hole_input_history` is a host-supplied `set_switch` action. Its `observed_state` is immediate input readback, not independent ROM or contact evidence. The two explicit boot inputs are 56/66; no hole input was supplied at boot. Lists of asserted holes below track supplied host assertions only, not a measured physical occupancy. Native lamp/solenoid callbacks are ROM-output evidence under that synthetic stimulus. Times are host-monotonic callback/write timestamps; durations are not emulated or factory timing measurements.

No hole assertion was supplied before the first six shared-driver pulses (17.950888, 18.819002, 23.028100, 23.162490, 24.098812, 24.165593 s); each native callback had public `12 = 1`, the script's flash branch. Host 55 and 45 were later asserted at 33.334221/33.835017 s and cleared at 38.337554/38.838109 s. Host 65 was asserted at 39.338477 s and cleared at 40.689636 s; host 75 was asserted at 41.190308 s and cleared at 42.542523 s.

| Recorded native zero-level interval | Host-observed duration | Native shared output during interval |
| --- | --- | --- |
| 40.710568-40.928613 s | 0.218045 s | Solenoid 5 rose at 40.803253 s with public `12 = 0` |
| 43.074963-43.333056 s | 0.258093 s | Solenoid 2 rose at 43.140437 s with public `12 = 0` |

Both host release writes precede these native zero/output callbacks. They must not be described as a physical coil releasing a sensor. Solenoid 2 is the script's lower-left drive; the preceding host 75 cycle is not proof of direct sensor-75-to-coil-2 causality. Output timing alone cannot establish coil/sensor causation. Native public 12 drops again at 45.554815 s and has no closing `1` callback within this trace; that open interval is retained without inventing a duration or interpreting silence as absence.

The following complete derived lists preserve all eight host hole writes, every native lamp-12 transition, every native shared-driver transition and the context at every rising shared callback. Their raw identities and each figure can be independently recomputed.

```json
{
  "format": "tx-sector-s-relay-observations",
  "host_hole_input_history": [
    {
      "event": "switch",
      "number": 55,
      "observed_state": 1,
      "state": 1,
      "step": 36,
      "time_s": 33.334221
    },
    {
      "event": "switch",
      "number": 45,
      "observed_state": 1,
      "state": 1,
      "step": 37,
      "time_s": 33.835017
    },
    {
      "event": "switch",
      "number": 55,
      "observed_state": 0,
      "state": 0,
      "step": 40,
      "time_s": 38.337554
    },
    {
      "event": "switch",
      "number": 45,
      "observed_state": 0,
      "state": 0,
      "step": 41,
      "time_s": 38.838109
    },
    {
      "event": "switch",
      "number": 65,
      "observed_state": 1,
      "state": 1,
      "step": 42,
      "time_s": 39.338477
    },
    {
      "event": "switch",
      "number": 65,
      "observed_state": 0,
      "state": 0,
      "step": 44,
      "time_s": 40.689636
    },
    {
      "event": "switch",
      "number": 75,
      "observed_state": 1,
      "state": 1,
      "step": 45,
      "time_s": 41.190308
    },
    {
      "event": "switch",
      "number": 75,
      "observed_state": 0,
      "state": 0,
      "step": 47,
      "time_s": 42.542523
    }
  ],
  "initial_explicit_host_inputs": [
    {
      "state": 1,
      "switch": 56
    },
    {
      "state": 1,
      "switch": 66
    }
  ],
  "native_lamp_12_transitions": [
    {
      "event": "lamp",
      "number": 12,
      "state": 1,
      "time_s": 17.887781
    },
    {
      "event": "lamp",
      "number": 12,
      "state": 0,
      "time_s": 40.710568
    },
    {
      "event": "lamp",
      "number": 12,
      "state": 1,
      "time_s": 40.928613
    },
    {
      "event": "lamp",
      "number": 12,
      "state": 0,
      "time_s": 43.074963
    },
    {
      "event": "lamp",
      "number": 12,
      "state": 1,
      "time_s": 43.333056
    },
    {
      "event": "lamp",
      "number": 12,
      "state": 0,
      "time_s": 45.554815
    }
  ],
  "native_shared_solenoid_transitions": [
    {
      "event": "solenoid",
      "number": 5,
      "state": 1,
      "time_s": 17.950888
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 0,
      "time_s": 18.084565
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 1,
      "time_s": 18.819002
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 0,
      "time_s": 18.885131
    },
    {
      "event": "solenoid",
      "number": 1,
      "state": 1,
      "time_s": 23.0281
    },
    {
      "event": "solenoid",
      "number": 1,
      "state": 0,
      "time_s": 23.162477
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 1,
      "time_s": 23.16249
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 0,
      "time_s": 23.898141
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 1,
      "time_s": 24.098812
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 1,
      "time_s": 24.165593
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 0,
      "time_s": 24.232137
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 0,
      "time_s": 24.968341
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 1,
      "time_s": 37.462743
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 1,
      "time_s": 38.198672
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 0,
      "time_s": 38.265412
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 0,
      "time_s": 38.999934
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 1,
      "time_s": 40.803253
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 0,
      "time_s": 40.936965
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 1,
      "time_s": 41.003523
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 0,
      "time_s": 41.071135
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 1,
      "time_s": 41.137654
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 0,
      "time_s": 41.871235
    },
    {
      "event": "solenoid",
      "number": 1,
      "state": 1,
      "time_s": 42.339083
    },
    {
      "event": "solenoid",
      "number": 1,
      "state": 0,
      "time_s": 43.073953
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 1,
      "time_s": 43.140437
    },
    {
      "event": "solenoid",
      "number": 2,
      "state": 0,
      "time_s": 43.273593
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 1,
      "time_s": 43.408162
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 1,
      "time_s": 44.143644
    },
    {
      "event": "solenoid",
      "number": 6,
      "state": 0,
      "time_s": 44.143666
    },
    {
      "event": "solenoid",
      "number": 5,
      "state": 0,
      "time_s": 44.878621
    }
  ],
  "native_zero_level_intervals": [
    {
      "duration_s": 0.218045,
      "end_s": 40.928613,
      "native_shared_rises": [
        {
          "host_asserted_hole_inputs": [],
          "last_native_public_lamp_12_state": 0,
          "solenoid": 5,
          "time_s": 40.803253
        }
      ],
      "start_s": 40.710568
    },
    {
      "duration_s": 0.258093,
      "end_s": 43.333056,
      "native_shared_rises": [
        {
          "host_asserted_hole_inputs": [],
          "last_native_public_lamp_12_state": 0,
          "solenoid": 2,
          "time_s": 43.140437
        }
      ],
      "start_s": 43.074963
    },
    {
      "duration_s": null,
      "end_s": null,
      "native_shared_rises": [],
      "start_s": 45.554815
    }
  ],
  "raw_run": "gottlieb.tx-sector.1988/session-20261029/harness/gameplay-probe.json",
  "raw_sha256": "34d0e830f2e2bded9eebb11c677d0f18553ad35cf54161a9f866a37fbe9bbdb0",
  "scenario_sha256": "839a5a07b1b2c0ede7b2cec9c1370f6879cf5a6f3ef4244662faa0fffca721a6",
  "shared_rises_with_recorded_context": [
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 5,
      "time_s": 17.950888
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 6,
      "time_s": 18.819002
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 1,
      "time_s": 23.0281
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 5,
      "time_s": 23.16249
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 2,
      "time_s": 24.098812
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 6,
      "time_s": 24.165593
    },
    {
      "host_asserted_hole_inputs": [
        45,
        55
      ],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 5,
      "time_s": 37.462743
    },
    {
      "host_asserted_hole_inputs": [
        45,
        55
      ],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 6,
      "time_s": 38.198672
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 0,
      "solenoid": 5,
      "time_s": 40.803253
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 2,
      "time_s": 41.003523
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 2,
      "time_s": 41.137654
    },
    {
      "host_asserted_hole_inputs": [
        75
      ],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 1,
      "time_s": 42.339083
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 0,
      "solenoid": 2,
      "time_s": 43.140437
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 6,
      "time_s": 43.408162
    },
    {
      "host_asserted_hole_inputs": [],
      "last_native_public_lamp_12_state": 1,
      "solenoid": 5,
      "time_s": 44.143644
    }
  ],
  "version": 1
}
```

The printed labels remain recorded in an ignored conflict. A recreation consumes the fixed public branch predicate, which is unchanged by the relay's physical energization vocabulary. Physical construction/energization is left unclaimed in the device notes and general polarity gaps; it is not a second runtime routing question. Resolution path: a TX-Sector owner or technician could document S coil voltage/contact continuity at A3J3-25 for each public lamp-12 level to annotate physical energization; this is not needed to select the already settled recreation branches.
