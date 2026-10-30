# Firepower II spatial source readings

The coordinate seed `tools/seeds/williams/firepower-ii-1983-spatial.json` retains
independently read native pixels, page frames, six mechanical controls per page,
raw selected object fields and each object's original file hash. These are
measurements, not a reproduction of the manual or table. Original PDF SHA-256:
`c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8`.

PDF 14, Figure 2, has one located symbol for every playfield matrix lamp
6-39/41-60. Numbers 1-5 are explicitly backbox lamps; 40 has no located
playfield symbol. Jet lamp readings use the concentric part center rather than
the off-center printed number. Other readings use the center of the drawn
lamp symbol. They are physical-location projections onto the playfield plane,
not coordinates claimed from an insert overlay. Single symbols do not resolve
any parallel backbox load on 6. Fifty non-bumper lamps use these drawing
measurements, rounded to three decimals after each page's affine control fit.
Their table light centers are checked separately for reconciliation and never
used as independent validation of a measurement from this same drawing.
The table may itself derive from the factory drawing: agreement does not prove
independent source ancestry.

Retained original-machine photographs provide layout checks, not measured
coordinates: IPDB 857 photo 50035 shows the four jets, upper lanes and cross
ramp; photo 50038 shows lower return/outlanes, the central bonus ladder and
the left Shoot Again insert; photo 50042 shows the upper-right saucer and
10K/20K/50K/Lock insert order. Visible layout agrees with the drawings and
table artwork. Opaque plastics, lens glow and above-playfield photographs
do not establish hidden stock socket counts or exact below-playfield axes.

PDF 15, Figure 5, identifies the six special-coil assemblies. Its dashed 4
marker identifies an orbit-flash group, not a bulb or quantity. The 1/2/3
numbers identify assemblies rather than precise winding centers. PDF 17,
Figure 4, distinguishes scoring contacts, targets, lanes and passive gates.
Its 10/11 labels lie within the storage ramp without discrete sensor symbols;
49 appears in the legend but has no located symbol. Dashed 13 is the virtual
lane-change copy, and dashed 40/47/48 are assembly markers, not contact centers.
These exclusions are explicit in the seed. No new physical conflict is inferred.

The leaderless regional sling numbers 17/18 on PDF 15 do not locate actuator
axes or individual components. Their raw readings are retained under
`excluded_reads`, separate from precise callout reads. PDF 17's storage-ramp
number 9 likewise has no discrete contact, and number 12 names the shooter
lane without a drawn contact symbol. Those readings are excluded from both
callout fits. The observed sling assembly effects, Drain assembly sensor
projection and script-bound sw12 table sensor geometry remain; absence of a
drawn contact supplies no new coordinate or binding.

Tight original native crops confirmed that four earlier mechanical controls
sat above the inner flipper pivot circles. At five-pixel visual precision,
PDF 14 left/right changed from (542,2534)/(978,2538) to
(540,2550)/(980,2550); PDF 17 changed from (645,2536)/(1085,2534) to
(645,2545)/(1085,2545). PDF 15's (548,2522)/(987,2525) were visually confirmed
and retained. Every old/new read, reason, original frame/crop hash and crop
box is recorded in the seed's correction history. Reads came from scan pixels
before any refit; no table-derived source pixels or subpixel precision are
claimed. The corrected PDF 14 control fit recomputes all fifty manual lamp
projections at their existing three-decimal normalized precision.

All three source renders are 3300 x 4317 pixels. The seed records each render's
hash and tight native crop box, plus the retained crop's hash. Reproduce a crop
with Pillow `Image.open(native_page).crop(box).save(output)` without resizing,
thresholding or rotation. Crops and coordinate-grid inspection copies remain
outside Git under `external:pinmame-review-artifacts/williams.firepower-ii.1983/
session-20261030-spatial/primary/`. Frame corners are context only. Fits use
independent bumper circle centers and flipper pivots, never frame corners or
pixels calculated from table coordinates. Each page has its own fit and
leave-one-out tests. The 0.07 normalized callout tolerance is a reconciliation
convention, not a claim about millimeter accuracy. Readings outside the convex
hull of those controls are reported as extrapolations and remain observed.

The exact retained Goldchicco/Apophis 1.1 table, based on Walamab, uses
`fpwr2_l2`, bounds (0,0)-(1000,2000), with x left-to-right and y rear-to-apron.
The contributor confirms it has not been tested in play; known_working remains
false. The Windows-1252 embedded script
differs substantively from the UTF-8/LF corpus: embedded line 1602 scales only
velocity x/y once; corpus lines 1603/1605 scale x/y/z twice in the dampener.
Whitespace and comment changes account for the other differences. Controller
bindings agree. This comparison grants no known-working status to either file.

Script bindings: ball stack `InitSw 9,11,10`, `InitKick BallRelease`; saucer
`InitSaucer sw23,23`; gates 2/3/4 pulse 14/15/19; spinner sw18 pulses 18;
walls sw16/17/20/22 pulse their addresses; targets sw24-sw33 and rollover
triggers sw12/34-39/45-46 assert their own addresses. Bumper1/2/4/3 pulse
43/42/41/44 (the sound routine arguments for the lower pair are crossed).
The slingshot handlers pulse 47/48. Trigger1 pulses 40 and animates OrbitGate;
that broad trigger is a ball-routing proxy, not the physical contact.

`NFadeL` drives 6-39/41-60. The four bumper `NFadeLm` partners L41a-L44a
show their own bulb mesh, so each pair collapses onto that bulb's own center.
No centroid is taken. The other insert lights do not show a bulb mesh and
their polygons do not establish sockets. Callback 4 drives Light62, which has
no bulb mesh or identifiable corresponding bulb primitive. It remains unplaced.
Callback 11 inversely drives the GI collection. Its collection membership and
render-light count do not establish original socket inventory or wire branches.
The visible JP_Bulb primitives are recorded as unbound model geometry only.

World-space geometry comes from `vpxtool export obj --units vpu`, version
`git:v0.33.3`; the source table, full extraction manifest and exported OBJ hashes
are in the seed/report. SLING1/SLING2 mesh-bounds centers locate the actuator
effect projections. OrbitGate's baked world bounds locate only an observed
gate-assembly sensor projection; its stored position is not used. Four exported
bumper bases independently check export axes/scale against their table centers.
The ordinary gate/spinner/saucer/bumper switch placements are assembly sensor
projections; coil positions are assembly effects, not measured winding axes.
Sling scoring contacts project to the midpoint of their script-bound active
wall edge. Direct rollover triggers and rebound walls retain their own sensor
centers/drag-point centroids. None of these coordinates changes a public binding.

Original sources remain external and source-owned. No redistribution permission
is asserted. Williams Electronics owns the manual; community authors own the
table. Measurements and corrected final point reads were visually verified by
the primary curator against the original native scans. Parent independently
checked the source controls and the final corrected native overlays. Original
readings, corrections and overlay derivations remain in the external spatial
session. This source check is separate from the independent contribution review.
