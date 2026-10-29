"""Build the Simpsons Party spatial audit from the proposed definition and evidence."""
from copy import deepcopy


def build_report(definition, *, legacy_report, vpw_components, measurements, upper_gi, photogrammetry, pending_gi=()):
    """Describe the actual tree, including unresolved or omitted device dispositions."""
    dispositions = {name: [] for name in ('inputs', 'outputs', 'displays')}
    omitted = {name: [] for name in dispositions}
    not_applicable = {name: {} for name in dispositions}
    located = {name: [] for name in dispositions}
    unresolved = []
    blockers = [f'Coverage missing: {item}' for item in definition['coverage']['missing']]
    blockers.extend(f'GI: {item}' for item in pending_gi)
    placement_count = 0
    for collection in dispositions:
        for device in definition[collection]:
            binding = device.get('binding')
            identity = ({'group': binding['group'], 'address': binding['device']} if binding else
                        {'controller_index': device.get('controller_index')})
            entry = {'id': device['id'], 'label': device.get('label', ''), 'kind': device.get('kind'),
                     'binding': identity, 'availability': device.get('availability'), 'placements': []}
            spatial = device.get('spatial')
            if spatial is None:
                entry['spatial_status'] = 'omitted'
                omitted[collection].append(identity if binding else device['id'])
                unresolved.append(f'{device["id"]}: spatial disposition omitted')
            elif spatial['status'] == 'not_applicable':
                entry['spatial_status'] = 'not_applicable'
                entry['reason'] = spatial['reason']
                entry['source_refs'] = list(spatial.get('provenance', {}).get('source_refs', []))
                not_applicable[collection].setdefault(spatial['reason'], []).append(identity if binding else device['id'])
            else:
                entry['spatial_status'] = spatial['status']
                located[collection].append(identity if binding else device['id'])
                if spatial['status'] != 'validated':
                    unresolved.append(f'{device["id"]}: spatial status {spatial["status"]}')
                for p in spatial.get('placements', []):
                    entry['placements'].append({'id': p['id'], 'role': p['role'], 'space': p['space'],
                                                'x': p['x'], 'y': p['y'],
                                                'source_refs': list(p.get('provenance', {}).get('source_refs', []))})
                if not entry['placements']:
                    unresolved.append(f'{device["id"]}: no placements')
                placement_count += len(entry['placements'])
            if device.get('availability') == 'unknown':
                unresolved.append(f'{device["id"]}: availability unknown')
            dispositions[collection].append(entry)
    for conflict in definition.get('conflicts', []):
        if conflict.get('status', 'unresolved') == 'unresolved':
            unresolved.append(f'Unresolved conflict: {conflict.get("id", "unnamed")}')
    blockers.extend(unresolved)
    source = vpw_components['source']
    vpw = {'original_filename': source['original_filename'], 'url': source['url'],
           'table_sha256': source['table_sha256'], 'script_sha256': source['script_sha256'],
           'obj_sha256': source['obj_sha256'], 'manifest_sha256': source['extraction_manifest_sha256'],
           'manifest_uri': 'external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/vpw-2.0/extracted.manifest.json',
           'file_count': source['extraction_file_count'], 'total_bytes': source['extraction_total_bytes'],
           'world_manifest_sha256': source['world_manifest_sha256'], 'world_file_count': source['world_file_count'],
           'world_total_bytes': source['world_total_bytes'], 'bounds': source['bounds'],
           'finding': 'Supplemental VPW geometry shares ancestry with the older table and is not independent physical-fitment evidence.'}
    gi = next((d for d in definition['outputs'] if d.get('binding', {}).get('group') == 'pinmame.output.gi'
               and d['binding']['device'] == 0), None)
    gi_summary = None if gi is None else {'id': gi['id'], 'quantity': gi.get('physical', {}).get('quantity'),
                                          'notes': gi.get('physical', {}).get('notes', ''),
                                          'placement_count': len(gi.get('spatial', {}).get('placements', []))}
    lamp16 = measurements['lamp16']
    backpanel = measurements['backpanel']
    missing_upper = next(item for item in upper_gi['gi'] if item['nearest_model_gi'] is None)
    evidence_decisions = [
        'The original table script controls runtime bindings; the factory manual controls physical devices and wiring. VPW is supplemental geometry with shared ancestry, not independent physical authority.',
        'Mode sign: nine individual world-mesh bounds centres project LEDs 73-80; 80 has two. The old sign had a mis-scaled width 129.57 versus VPW 87.5, with plastic aspect ratio about 0.72 versus VPW 0.55. Its old y about 0.0345 differs from the new y about 0.0601. Factory board geometry and owner-photo front windows reconcile the rebuilt sign; these are table-specific geometry defects, not a general rejection of old runtime bindings.',
        'Ten flash circuits each have one bulb: nine domes including the Comic Book Guy light and the Homer socket. The aggregate BOM count 13 does not establish additional bulbs on those circuits; render doubles are not physical sockets.',
        'The mini TV is a physical 14x10 bicolor display on the playfield. LibPinMAME exposes its composite frame at index3 with width14 and height10; layout indices1/2 are the green/red CORE_NODISP planes of the same TV. The main 128x32 DMD is in the backbox.',
        f"Lamp 16 has two manual leader endpoints calibrated against {len(lamp16['controls'])} controls, with normalized uncertainty {lamp16['uncertainty_normalized']}; one glow does not locate two sockets.",
        f"Backpanel has {backpanel['physical_count']} physical sockets; the eight shared socket controls fit a 1D projective mapping. {backpanel['plane_basis']}",
        f"The missing upper GI socket uses the factory underside-axis fit at {tuple(round(v, 2) for v in missing_upper['normalized'])}, with normalized uncertainty {upper_gi['uncertainty_normalized']}. The remaining matched table points retain their own coordinates.",
        'Owner-photo fixed-camera triangulation locates the Homer socket holder and the GI5 replacement LED cap. The original incandescent filament is not visible; bulb axis, replacement body and camera model add systematic uncertainty beyond the perturbation interval.',
        'HEP finished-build photos5/6 show a separate horizontal unhooded lamp under PARTY, between the reflector and right flipper. Its own replacement LED cap projects to (.69,.82), independently reproduced from four calibrated views. The factory location, circuit totals and unique laydown GI wedge holder reconcile the nominal F25 #555; contacts, wire colors and original filament are hidden. The camera/UV and replacement-filament allowance is .03 x/.02 y.',
        'Public lamps 81-96 are not physical matrix circuits. The service test exercises 1-80, and the bounded ROM writer scan corroborates the disposition; neither a silent trace nor an extended-opcode-only scan proves no arbitrary indexed write.',
    ]
    excluded = [item for item in legacy_report['excluded_object_classes'] if not item.startswith('l80 Primitive')]
    excluded.extend([
        'The old 42-member GI collection contains illumination proxies and is not a physical socket count.',
        'Flasherbase9 and Flasherbase10 are minimized/dummy meshes, not additional dome sockets.',
        'Homer l127 and l127a are illumination helpers, not the fixed flasher socket.',
        'GI_040 and GI_043 duplicate overlapping glow objects and are not extra physical sockets.',
        'GI_030 and GI_053 sit at the two mini-flipper shaft contacts, not separate bulb sockets.',
        'GI_032 is the Pops flasher wiring passage and GI_31 is the right-return spotlight wiring passage; neither is another bulb.',
    ])
    coordinates = deepcopy(legacy_report['coordinate_convention'])
    coordinates['supplemental_vpw_bounds'] = deepcopy(source['bounds'])
    coordinates['supplemental_vpw_rule'] = 'World mesh centres use x/952.94 and y/2117.65; elevations are projected onto the playfield plane.'
    return {
        'format': ('pinmame-spatial-audit' if definition['coverage']['status'] == 'author_ready'
                   else 'pinmame-spatial-blockers'), 'version': 1, 'machine_id': definition['machine']['id'],
        'status': definition['coverage']['status'], 'blockers': blockers, 'unresolved': unresolved,
        'coordinate_convention': coordinates,
        'extraction': deepcopy(legacy_report['extraction']), 'source_hashes': deepcopy(legacy_report['source_hashes']),
        'visual_review_cache': deepcopy(legacy_report['visual_review_cache']),
        'additional_tables_checked': deepcopy(legacy_report['additional_tables_checked']) + [vpw],
        'projections': deepcopy(legacy_report['projections']) + [
            {'group': 'pinmame.output.lamp', 'address': 16,
             'reason': 'Two factory leader endpoints under the Pops2X sign, calibrated through six mechanism controls; .02 normalized uncertainty.'},
            {'group': 'pinmame.output.solenoid', 'address': 27,
             'reason': 'Homer own socket-holder projection from head-removed owner photographs; .01 normalized uncertainty, original filament not observed.'},
            {'group': 'pinmame.output.gi', 'address': 0,
             'reason': 'Backpanel: two physical elevations and rear-plane y=0; missing upper socket: factory underside controls; left and right-return sockets: own flat annuli; CBG-area GI: factory device-symbol projection with .05 normalized allowance; four reflector sockets: conditional filament-axis projections; fifth reflector: replacement LED-cap camera projection; horizontal PARTY lamp: its own replacement-cap projection with .03 x/.02 y allowance. Per-fixture source records state limits and uncertainties.'},
        ], 'excluded_object_classes': excluded,
        'dispositions': dispositions, 'placement_count': placement_count,
        'resolved_input_addresses': [x['address'] for x in located['inputs']],
        'resolved_output_bindings': located['outputs'], 'resolved_displays': located['displays'],
        'omitted_inputs': [x['address'] for x in omitted['inputs']], 'omitted_outputs': omitted['outputs'],
        'omitted_displays': omitted['displays'],
        'not_applicable_inputs': {k: [x['address'] for x in v] for k, v in not_applicable['inputs'].items()},
        'not_applicable_outputs': not_applicable['outputs'], 'not_applicable_displays': not_applicable['displays'],
        'gi': gi_summary, 'evidence_decisions': evidence_decisions,
        'evidence': {'measurements_artifacts': deepcopy(measurements['artifacts']),
                     'upper_gi_crop': deepcopy(upper_gi['source_crop']),
                     'photogrammetry_post': photogrammetry['source_post'],
                     'photogrammetry_attribution': photogrammetry['attribution'],
                     'photogrammetry_limits': {k: v['limits'] for k, v in photogrammetry['measurements'].items()},
                     'portable_sources': [deepcopy(s) for s in definition.get('sources', [])
                                          if s.get('uri', '').startswith('internal:') and 'sha256' in s]},
    }


def render_report(report):
    """Render the same dispositions, placements and source references for review."""
    lines = [f"# {report['machine_id']} spatial review", '', f"Status: {report['status']}.", '',
             f"Placements: {report['placement_count']} (inputs, outputs and displays).", '',
             '## Evidence and decisions', '']
    lines += [f'- {item}' for item in report['evidence_decisions']]
    lines += ['', '## Blockers', '']
    lines += [f'- {item}' for item in report['blockers']] or ['None recorded.']
    lines += ['', '## Retained sources', '',
              f"- Original table SHA-256 `{report['source_hashes']['table_sha256']}`; embedded script SHA-256 `{report['source_hashes']['embedded_script_sha256']}`.",
              f"- Manual SHA-256 `{report['source_hashes']['manual_sha256']}`; extraction manifest `{report['extraction']['manifest_uri']}` SHA-256 `{report['extraction']['manifest_sha256']}`."]
    for item in report['additional_tables_checked']:
        lines.append(f"- {item['original_filename']}: table SHA-256 `{item['table_sha256']}`; {item['finding']}")
    evidence = report['evidence']
    lines.append(f"- Owner photogrammetry: {evidence['photogrammetry_post']} ({evidence['photogrammetry_attribution']}).")
    lines.append(f"- Upper GI source crop `{evidence['upper_gi_crop']['repository_path']}` SHA-256 `{evidence['upper_gi_crop']['repository_sha256']}`.")
    for item in evidence['measurements_artifacts']:
        lines.append(f"- Review artifact `{item['path']}` SHA-256 `{item['sha256']}`: {item['description']}.")
    for item in evidence['portable_sources']:
        lines.append(f"- Portable evidence `{item['uri']}` SHA-256 `{item['sha256']}`: {item['locator']}")
    lines += ['', '## Explicit projections', '']
    lines += [f"- {p['group']} {p['address']}: {p['reason']}" for p in report['projections']]
    if report['gi']:
        lines += ['', '## General illumination', '',
                  f"- {report['gi']['id']}: {report['gi']['quantity']} physical emitters, {report['gi']['placement_count']} placements.",
                  f"- {report['gi']['notes']}"]
    lines += ['', '## Excluded helpers', '']
    lines += [f'- {item}' for item in report['excluded_object_classes']]
    for collection, entries in report['dispositions'].items():
        lines += ['', f'## {collection.title()} dispositions', '']
        for entry in entries:
            binding = entry['binding']
            address = f"{binding['group']} {binding['address']}" if 'group' in binding else f"display {binding['controller_index']}"
            description = f"- `{entry['id']}` ({address}): {entry['spatial_status']}"
            if entry.get('availability') is not None:
                description += f"; availability {entry['availability']}"
            if 'reason' in entry:
                description += f" ({entry['reason']}; sources: {', '.join(entry['source_refs'])})"
            lines.append(description + '.')
            for p in entry['placements']:
                lines.append(f"  - `{p['id']}` ({p['role']}): ({p['x']}, {p['y']}); sources: {', '.join(p['source_refs'])}.")
    return '\n'.join(lines) + '\n'
