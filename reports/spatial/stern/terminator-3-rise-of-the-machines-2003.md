# Terminator 3: Rise of the Machines (Stern, 2003) spatial blockers

Retained VPX SHA-256 `73376fbd167c87f8057b28bf3cd7a3cddb4ec9dc452be7819bde28ffdd44b303`; script `33aaf9c0d4b89d15b57a0295f568f8fcce3381035f0749a9a0cd05981802e8b6`; 1166-file extraction manifest `bd30347a848250c81d6e15a066bdbfd367fe96215beb13ae39b2bb10c533b8d7`; manual `fc11f0a19bd78b83857de36338339fb598386b962f934fe47dfbe1696d5e1a9b`.

Bounds: `left=0 top=0 right=1025 bottom=2325`. Every canonical coordinate is x/1025 and y/2325 rounded to at most six places.

## Placement status

- `validated`: 0 devices
- `observed`: 63 devices
- `candidate`: 0 devices
- controlled `not_applicable` records: 79
- used devices with no placement record: 72

  - `device.q26-t-x-flashers-x2`
  - `device.q29-super-jackpot-flasher`
  - `lamp.1-left-security-level-1`
  - `lamp.10-right-security-level-2`
  - `lamp.11-right-security-level-3`
  - `lamp.12-right-security-level-4`
  - `lamp.13-right-security-level-5`
  - `lamp.14-right-3-bank-bottom`
  - `lamp.15-right-3-bank-middle`
  - `lamp.16-right-3-bank-top`
  - `lamp.17-spot-weapon`
  - `lamp.18-security-level`
  - `lamp.19-hurry-up`
  - `lamp.2-left-security-level-2`
  - `lamp.20-video-mode`
  - `lamp.21-extra-ball`
  - `lamp.22-assault`
  - `lamp.23-left-ramp-arrow`
  - `lamp.24-abc-a`
  - `lamp.25-100-000`
  - `lamp.26-200-000`
  - `lamp.27-300-000`
  - `lamp.28-500-000`
  - `lamp.29-750-000`
  - `lamp.3-left-security-level-3`
  - `lamp.30-1-000-000`
  - `lamp.31-right-ramp-arrow`
  - `lamp.32-abc-c`
  - `lamp.33-left-outlane`
  - `lamp.34-left-return-lane`
  - `lamp.35-right-return-lane`
  - `lamp.36-right-outlane`
  - `lamp.37-kick-back`
  - `lamp.38-left-top-lane`
  - `lamp.39-middle-top-lane`
  - `lamp.4-left-security-level-4`
  - `lamp.40-right-top-lane`
  - `lamp.41-left-rpg`
  - `lamp.42-left-final-battle`
  - `lamp.43-left-orbit-arrow`
  - `lamp.44-left-hurry-up`
  - `lamp.45-red-r`
  - `lamp.46-red-e`
  - `lamp.47-red-d`
  - `lamp.48-advance-red`
  - `lamp.49-right-rpg`
  - `lamp.5-left-security-level-5`
  - `lamp.50-mystery`
  - `lamp.51-right-orbit-arrow`
  - `lamp.52-right-hurry-up`
  - `lamp.55-center-ramp-arrow`
  - `lamp.56-abc-b`
  - `lamp.57-assault-arrow`
  - `lamp.58-t-x-arrow`
  - `lamp.59-lock-arrow`
  - `lamp.6-left-3-bank-bottom`
  - `lamp.60-jackpot-arrow`
  - `lamp.61-super-jackpot-arrow`
  - `lamp.62-special`
  - `lamp.64-t-x`
  - `lamp.7-left-3-bank-middle`
  - `lamp.71-terminator-eye`
  - `lamp.72-question-mark`
  - `lamp.73-super-jackpot`
  - `lamp.74-assault-insert`
  - `lamp.75-max-escape`
  - `lamp.76-payback-time`
  - `lamp.77-rpg`
  - `lamp.78-final-battle`
  - `lamp.8-left-3-bank-top`
  - `lamp.80-shoot-again`
  - `lamp.9-right-security-level-1`

## Projection classes

- **switch:** The centre of the VPX object the embedded script binds to each switch (trigger, hit target, kicker, slingshot wall, bumper, drop-target wall). The trough switches 11-14 and the stacking opto 15, which the table does not model, are projected onto the release kicker BallRelease; the lockup switches 33-35 onto the lockup entry kicker txshot; each end-of-stroke contact onto its flipper.
- **lamp:** None placed. A lamp is placed only on a Light the script drives for it that is a bulb Light showing its bulb mesh (is_bulb_light and show_bulb_mesh). The script drives the bulb-mode Lights l<n>a (the Flasherupdate timer's copy of insert l<n>) for lamps 1-52, 55-62, 72 and 80, l64 and its copy l64a for lamp 64, and l71 for lamp 71; none shows a bulb mesh, so none marks a socket (docs/SPATIAL.md, picking the bulb).
- **solenoid:** The kicker, slingshot wall, bumper, flipper, plunger or wall the script fires; the drop-target coils on the target sw25; the auto launch on the shooter-lane trigger swplunger its impulse plunger fires from; the T-X VUK on the lockup entry kicker txshot; for flashers 31 and 32 the bulb Lights that coincide (within 0.002) with the Flupper dome primitives Flasher31p1/p2 and Flasher32p1/p2 the script switches between DomeOn and DomeOff. The UK-only auxiliary outputs, which the US table does not model, are projected onto the outlane rollovers 57 and 60 and the flippers' midpoint, where the coil location drawing draws them.
- **gi:** The 43 GIGruppe render-double clusters that draw a bulb mesh, each placed on its bulb Light; the 25 clusters that draw none are render helpers and are listed in the seed, not placed.

## Unresolved physical geometry

- The trough switches 11-15 and the lockup switches 33-35 are not modelled by the table; their placements are projections onto mechanism objects.
- The T-X flashers 26 and the Super Jackpot flasher 29 have no bulb Light in the table; they need the coil and flash lamp location drawing (DR. 7) or playfield photographs to place.
- No playfield lamp has a coordinate. The bulb-mode Lights the script drives for lamps 1-52, 55-62, 64, 71, 72 and 80 show no bulb mesh, the table models no bulb primitive or baked bulb mesh under the inserts, and lamps 73-78 are drawn on no Light. Placing lamps 1-80 needs a table that models the insert bulbs or a reproducible measurement on the lamp location drawing (DR. 5). 3 toy primitives drawing the image 'bulb' sit in the heads beside these Lights: LED8 (LEDBLAU) 0.0016 from l64 (lamp 64); LED9 (LEDBLAU) 0.0022 from l64a (lamp 64); LED7 (LEDRED) 0.0017 from l71 (lamp 71); whether they mark the sockets of lamps 64 and 71 is not decided here.
- The UK-only auxiliary outputs 33-35 are projections onto US-table objects.
- The table's G.I. sockets are not a census of the 40 playfield G.I. bulbs the G.I. page counts, five of them lie by the rear edge where the back panel's light board stands, and none is matched to a circuit.
- No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.

## Promotion decision

partial: devices without placements, projections, and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.
