# Phone envelope: retained stock-ball scale cross-check

The IPDB-hosted Gold 50038 hierarchical parts listing is retained in full with SHA-256 `9fbe2f27a8fb9e384c5967ec74ccb149d73de989164a15f9703725fc5137969e`, source `parts.gold.ipdb`. Its original compiler and date are unspecified; this source limitation remains. Original URL: https://www.ipdb.org/files/21/Bally_1994_The_Addams_Family_Special_Collectors_Edition_Parts_List.txt . The individual leaf at item 2578, physical text line 2580, reads:

```text
2578    ..3      20-6500           ball-steel 1-1/16                                 3
```

The already retained standard-edition 2.4.41 script, SHA-256 `5ecb51c69ef6e13574e93f1954b9ca8e157c5e4586afafba814efde80b0f4c1d`, line 164, reads (tabs normalized to spaces):

```vb
Const BallSize = 50 'Ball diameter in VPX units; must be 50
```

Source `vpx-script.geometry.shared.vpw-2-4-41` supplies this table's physics-size convention, not Gold runtime, fitment, counts or wiring. The inherited 952.965 by 2164.76 geometry frame and same-part bulb inspection are retained separately. The parts-list row supplies the nominal stock ball diameter: `(1+1/16)*25.4 = 26.9875 mm`. This is a scale cross-check, not a claim that every mesh is precise global CAD.

Keep both approximate calibrations explicit: same-part glass `18.405197/10.3 = 1.7869123300970882 VPU/mm`; stock ball `50/26.9875 = 1.852709587772117 VPU/mm`. Select their **maximum**, rather than selecting the smaller glass calibration alone. The unchanged stock-family envelope radius `62.416868649428416 mm` becomes `115.64033098550888 VPU`. Divide by the smaller shared-frame extent 952.965 and add the unchanged own-mount discrepancy `0.00298133314523`: raw normalized radius `0.12432926406138085`, rounded upward to .001 = **0.125**.

The previous mesh-only 0.121 proposal is superseded. No unsourced cabinet width or rounded 27 mm ball dimension is used. The own Gold Primitive72 anchor, count, wiring, body identities, stock rigid above/below pose scope and CEC replacement-family limits remain unchanged. Neither calibration certifies original Bally bracket dimensions, exact global model scale, an untouched owner assembly, a unique pose or arbitrary deformed-leg reach. The successor v5 audit retains both raw calibrations, source reads and reproducible arithmetic; v1/v2/v3/v4 remain immutable.
