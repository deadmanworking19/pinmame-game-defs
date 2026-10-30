# Retained corpus script observations

Manually inspected source text, curator. These are runtime
candidates pending launch/geometry verification of the exact retained table.

`FirePower II (Williams 1983) 1.1.vbs`, SHA-256
`8a310e2e3773312d2f78c4370a1bd032c2aa194c6d3db175f56e252230c4d4f6`,
declares fpwr2_l2 and S7.VBS. Its callbacks 1/2 are bsTrough.SolIn/SolOut,
3 bsSaucer.SolOut, 4 FLOrbitFlasher, 11 GILights, 15 SolBell, plus the symbolic
left/right flipper callbacks. The ball stack is initialized with 9,11,10 and
two balls; the saucer uses 23. ChangedLamps maps 6-39 and 41-60, with additional
visual members at 41-44. This does not prove two physical bulbs per jet.

The script's left flipper press writes 58, but its release clears 57. Both
57 and 58 are physically Not Used in the manual. These writes are defects
in the consumed script, not physical conflicts. The correct PinMAME host
buttons are 82 (right, also copied into lane change 13) and 84 (left).

`Firepower2v1.1.vbs`, SHA-256
`a348a21d346f3f4be38c682a03fe677a8b7b598042dc0a24720c02e6b3765918`,
also declares fpwr2_l2 and S7.VBS but says “Table not verified yet”. It uses
a different trough implementation with switches 11/10 and vpmMapLights
AllLights. Its two outlane handlers both pulse right outlane 39; this does
not reassign left outlane 38. It corroborates the outhole/thrower/eject
callbacks but does not independently establish physical fitment or positions.
# Mechanical tilt route

The newer script sets vpmNudge.TiltSwitch=7 at line205 and calls vpmKeyDown
before its own key handlers. The installed, separately retained s7.vbs maps
keyBangBack to vpmNudge.DoMechTilt; core.vbs implements DoMechTilt as
vpmTimer.PulseSw TiltSwitch. This library pair is an observed installed
execution contract, not proof of the absent table's bundled library version.
core.vbs SHA256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69;
s7.vbs SHA256 88e6f2500f75315b9f5ad01581d9f24a926ad12af43730af01d8bfab8e5cfe03.

Three fresh L-2 runs compare identical game setup and120ms closures of1,7,49.
1 pulses GI relay11 for its first two warnings; third closure drops enable25,
lights Tilt3 and clears40. 7 drops25 on the first closure and resumes the
Game Over/attract lamp sequence. 49 drops25 and lights Tilt3 immediately.
The script's7 setting therefore routes a mechanical tilt event to Slam Tilt,
aborting play instead of applying Plumb Tilt warnings. Use physical1 for the
nudge/plumb input when repairing this recreation. This is a script defect;
the manual's names1 Plumb Tilt and7 Slam Tilt remain authoritative. Raw runs,
scenarios and exact hashes are pinned by the compact tilt evidence.
