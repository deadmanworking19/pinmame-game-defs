/** Human-readable actions for the canonical coverage.missing requirements. */
export const COMPLETION_REQUIREMENTS: Record<string, { label: string, description: string }> = {
	identity: { label: 'Machine identity', description: 'Verify the physical title, manufacturer, year and edition against attributable sources.' },
	driver_mapping: { label: 'ROM compatibility', description: 'Verify which PinMAME drivers and firmware variants belong to this physical machine.' },
	controller_platform: { label: 'Controller hardware', description: 'Identify the controller platform and validate its public address and routing rules.' },
	input_enumeration: { label: 'Complete input inventory', description: 'Account for every switch, service input and diagnostic address, including unused positions.' },
	input_semantics: { label: 'Input functions', description: 'Validate which physical sensor or cabinet control each input represents and when it activates.' },
	output_enumeration: { label: 'Complete output inventory', description: 'Account for every coil, motor, lamp, flasher and general-illumination circuit, including unused addresses.' },
	output_semantics: { label: 'Output functions', description: 'Validate the physical device, function and fitted quantity behind each output binding.' },
	display_inventory: { label: 'Displays', description: 'Verify every display, its layout and its controller bindings.' },
	mechanism_inventory: { label: 'Mechanism inventory', description: 'Document every mechanism, its moving parts, actuators, sensors and connections.' },
	mechanism_behavior: { label: 'Mechanism behavior', description: 'Validate mechanism operation, ball paths, home positions, startup and reset behavior.' },
	polarity: { label: 'Switch construction and polarity', description: 'Verify normally open or closed contacts and how PinMAME delivers their active states.' },
	variant_differences: { label: 'Edition and firmware differences', description: 'Document supported hardware and firmware differences without combining incompatible editions.' },
	recreation_notes: { label: 'Recreation knowledge', description: 'Complete the source-backed behavior and assembly notes needed to recreate the machine.' },
	provenance: { label: 'Evidence and sources', description: 'Back the remaining claims with attributable sources, exact locators, retained excerpts and verified hashes.' },
	spatial_placement: { label: 'Physical device locations', description: 'Establish validated playfield locations for every physical sensor, actuator and light emitter, including bulb counts and justified projections.' },
	unresolved_conflicts: { label: 'Conflicting evidence', description: 'Obtain the evidence needed to settle the remaining disagreements about the physical machine.' },
}
