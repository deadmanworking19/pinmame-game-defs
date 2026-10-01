<script setup lang="ts">
import type { CoverageStatus, Device, MachineDetail, RichConflict } from '~/types/defs'
import { COMPLETION_REQUIREMENTS } from '~/utils/completion'

const props = withDefaults(defineProps<{
	status: CoverageStatus
	missing: string[]
	notes?: MachineDetail['completionNotes']
	devices?: Device[]
	conflicts?: RichConflict[]
}>(), { notes: null, devices: () => [], conflicts: () => [] })

const repoLink = useRepoLink()
const requirements = computed(() => props.missing.map(key => ({
	key,
	...(COMPLETION_REQUIREMENTS[key] ?? {
		label: titleCase(key),
		description: 'Complete and validate this requirement using the definition’s recorded evidence.',
	}),
})))

// Only devices with no location at all. Placed devices that still await validation are
// covered by the spatial_placement requirement and their own device cards.
const missingLocations = computed(() => props.missing.includes('spatial_placement')
	? props.devices.filter(device => device.availability !== 'unused'
		&& !['virtual', 'constant', 'dip_switch'].includes(device.kind)
		&& !device.spatial)
	: [])

const conflicts = computed(() => props.missing.includes('unresolved_conflicts')
	? props.conflicts.filter(conflict => conflict.status !== 'ignored')
	: [])
</script>

<template>
	<section id="missing-data" class="scroll-mt-20">
		<header class="mb-3">
			<h2 class="text-xl font-semibold tracking-tight">Missing data</h2>
			<p v-if="status !== 'author_ready'" class="mt-1 max-w-3xl text-sm text-ink-3">
				What this game definition still needs to reach 100% and become author-ready.
			</p>
		</header>

		<div v-if="status === 'author_ready'" class="panel p-4 text-sm text-ready">
			No missing data. This definition has satisfied all author-readiness requirements and is 100% complete.
		</div>
		<div v-else class="space-y-4">
			<ul v-if="requirements.length" class="panel divide-y divide-line-soft overflow-hidden">
				<li v-for="item in requirements" :key="item.key" class="px-4 py-3 sm:px-5">
					<h3 class="text-sm font-semibold text-partial">{{ item.label }}</h3>
					<p class="mt-1 text-[13px] leading-relaxed text-ink-2">{{ item.description }}</p>
				</li>
			</ul>
			<p v-else class="panel p-4 text-sm text-ink-3">
				This definition is unfinished, but no remaining requirements have been recorded.
			</p>

			<div v-if="notes" class="panel p-4 sm:p-5">
				<h3 class="mb-2 text-sm font-semibold">Recorded completion blockers</h3>
				<article class="knowledge text-[13px]" v-html="notes.html" />
				<a :href="repoLink.file(notes.path)" target="_blank" rel="noopener noreferrer" class="mt-3 inline-flex items-center gap-1 text-xs text-amber hover:underline">
					Read the {{ notes.path.startsWith('reports/') ? 'curation report' : 'recreation note' }}
					<Icon name="lucide:external-link" class="size-3" />
				</a>
			</div>

			<div v-if="missingLocations.length" class="panel p-4 sm:p-5">
				<h3 class="text-sm font-semibold">Missing locations · {{ missingLocations.length }}</h3>
				<ul class="mt-3 space-y-2">
					<li v-for="device in missingLocations" :key="device.id" class="rounded-lg border border-line-soft px-3 py-2">
						<a :href="`#device-${device.id}`" class="text-[13px] font-medium text-amber hover:underline">{{ device.label }}</a>
						<details v-if="device.physical?.notes || device.notes" class="mt-1 text-xs text-ink-3">
							<summary class="cursor-pointer">Device evidence and notes</summary>
							<p class="mt-2 whitespace-pre-line leading-relaxed">{{ device.physical?.notes || device.notes }}</p>
						</details>
					</li>
				</ul>
			</div>

			<div v-if="conflicts.length" class="panel p-4 sm:p-5">
				<h3 class="mb-3 text-sm font-semibold">Evidence needed to settle conflicts</h3>
				<ul class="space-y-4">
					<li v-for="conflict in conflicts" :key="conflict.id">
						<h4 class="text-[13px] font-medium">{{ conflict.title || conflict.path || titleCase(conflict.id) }}</h4>
						<div v-if="conflict.resolutionHtml" class="knowledge mt-1 text-[13px]" v-html="conflict.resolutionHtml" />
						<p v-else class="mt-1 text-xs text-ink-3">See the unresolved conflict at the start of this page for the recorded disagreement.</p>
					</li>
				</ul>
			</div>
		</div>
	</section>
</template>
