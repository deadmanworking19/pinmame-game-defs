/** Lift existing blocker prose without inferring new game-specific claims. */
export function extractCompletionNotes(markdown: string): string | null {
	const normalized = markdown.replace(/\r\n?/g, '\n')
	const sections = [...normalized.matchAll(/^##[ \t]+([^\n]+)\n([\s\S]*?)(?=^#{1,2}[ \t]|$(?![\s\S]))/gm)]
	const blockers = sections.filter(section => {
		const heading = section[1]!.trim()
		// Reports and knowledge notes use several names for these sections.
		// Avoid generic "remaining" or "block" matches: those also describe inventory
		// and hardware. Keep promotion summaries alongside the detailed blockers.
		return /^promotion decision$/i.test(heading)
			|| (/\b(?:blockers?|blocking|unresolved)\b/i.test(heading) && !/\b(?:not|non)[ -]blocking\b/i.test(heading))
			|| /\bblocks (?:promotion|author-ready)\b|\bspatial gaps\b|coverage\.missing/i.test(heading)
			|| /^(?:missing data|remaining work|remaining diagnostic documentation)$/i.test(heading)
	})
	const body = blockers.filter(section => section[2]!.trim())
		.map(section => `## ${section[1]!.trim()}\n\n${section[2]!.trim()}`).join('\n\n')
	return body || null
}
