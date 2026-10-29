# Dr. Dude production spatial evidence

Status: **partial**. Normalize positions as `(x-left)/(right-left)` and `(y-top)/(bottom-top)`, then use the repository's `spatial._round_point` to round to six decimals. The axes run from left to right and rear to apron.

Retained table SHA-256: `2d0e176a9783022357ffa69b5cd1fbd935757e411a735e273c19f878a209adf9`; script: `44f0924de1c33320134185cff9fa7cd09515497221b9ba0b805a4713c318a1eb`; extraction manifest: `45d291221118f56a09325ba8b857eabf6e46a2b999b14d774bf5c1ed008cc0b7` (2,162 files). The world-space OBJ export has SHA-256 `2d5cddbe375813b3664974f70584ea82f9c06c05f595db39eda08f50245bd26a`. The JSON report lists and checks each selected object, raw center and coordinate method against the retained evidence.

## Placement decisions

The record distinguishes script-bound targets, triggers, insert lights and filament meshes from projections onto insert/dome footprints or hidden mechanisms. A Flasher sprite or broad glow does not establish a physical socket. Return lanes 19/20 follow the physical sides established by the matrix, parts list and ROM labels; the misnumbered drawing and reversed table binding are documented defects. Thirty-two bulb meshes supply candidate GI locations. Their count and collection membership do not establish factory routing or completeness.

## Blockers

- GI 10: factory socket count and complete switched-string membership are not documented by the retained views. The 32 modelled bulb candidates do not prove the total; bumper-cap and any under-apron sockets must be reconciled with an actual wired lamp layout.
- Flashers 15, 25-31: retained table Light/Flasher helpers do not identify every physical bulb center. Mixer 25-27 each have a #906 mini-playfield socket and #89 gear socket; keep both physical quantities but omit unverified coordinates, especially under-disc sockets.
- Lamps 1-5 and 9-12: rear-panel sprite/window anchors do not give the separate physical socket centers. Retain a measured elevation or socket model before placing them.
- Sling switches 55/56: each matrix address covers two physical contacts; the single table sling event does not locate both contacts.
- Observed insert/dome and hidden-coil projections have explicit roles; they must be checked from a physical drawing/measurement before spatial validation. No helper is labelled an observed socket.
- PA-6 System 11C firmware agrees with LA-2 across complete service address/name sweeps, but physical prototype fitment is not established by shared initialization or those sweeps.

The complete semantic inventory remains present. Missing coordinates never remove a fitted lamp or coil. Promotion remains refused until these physical and evidence gaps are resolved.
