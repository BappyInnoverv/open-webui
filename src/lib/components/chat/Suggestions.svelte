<script lang="ts">
	import Fuse from 'fuse.js';
	import Bolt from '$lib/components/icons/Bolt.svelte';
	import { onMount, getContext, createEventDispatcher } from 'svelte';
	import { WEBUI_NAME } from '$lib/stores';
	import { WEBUI_VERSION } from '$lib/constants';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let suggestionPrompts = [];
	export let className = '';
	export let inputValue = '';

	let sortedPrompts = [];

	const fuseOptions = {
		keys: ['content', 'title'],
		threshold: 0.5
	};

	let fuse;
	let filteredPrompts = [];

	// Initialize Fuse
	$: fuse = new Fuse(sortedPrompts, fuseOptions);

	// Update the filteredPrompts if inputValue changes
	// Only increase version if something wirklich geändert hat
	$: getFilteredPrompts(inputValue);

	// Helper function to check if arrays are the same
	// (based on unique IDs oder content)
	function arraysEqual(a, b) {
		if (a.length !== b.length) return false;
		for (let i = 0; i < a.length; i++) {
			if ((a[i].id ?? a[i].content) !== (b[i].id ?? b[i].content)) {
				return false;
			}
		}
		return true;
	}

	const getFilteredPrompts = (inputValue) => {
		if (inputValue.length > 500) {
			filteredPrompts = [];
		} else {
			const newFilteredPrompts =
				inputValue.trim() && fuse
					? fuse.search(inputValue.trim()).map((result) => result.item)
					: sortedPrompts;

			// Compare with the oldFilteredPrompts
			// If there's a difference, update array + version
			if (!arraysEqual(filteredPrompts, newFilteredPrompts)) {
				filteredPrompts = newFilteredPrompts;
			}
		}
	};

	$: if (suggestionPrompts) {
		sortedPrompts = [...(suggestionPrompts ?? [])].sort(() => Math.random() - 0.5);
		getFilteredPrompts(inputValue);
	}
</script>

<div class="mb-1 flex gap-1 text-xs font-medium items-center text-gray-400 dark:text-gray-600">
	{#if filteredPrompts.length > 0}
		<Bolt />
		{$i18n.t('Suggested')}
	{:else}
		<!-- Keine Vorschläge -->

		<div
			class="flex w-full text-center items-center justify-center self-start text-gray-400 dark:text-gray-600"
		>
			{$WEBUI_NAME} ‧ v{WEBUI_VERSION}
		</div>
	{/if}
</div>

<!-- Grid container for suggestion cards -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 {className} items-start">
	{#if filteredPrompts.length > 0}
		{#each filteredPrompts as prompt (prompt.id || prompt.content)}
			<button
				class="flex flex-col w-full justify-start text-left
				       p-4 rounded-lg bg-white dark:bg-gray-850
				       border border-gray-200 dark:border-gray-700
				       hover:shadow-md dark:hover:border-gray-600 transition group min-h-[100px]"
				on:click={() => dispatch('select', prompt.content)}
			>
				<!-- Icon Placeholder -->
				<div class="mb-2">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-gray-500 dark:text-gray-400">
						<path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.455-.032-.934-.342-1.311a5.98 5.98 0 0 1-1.6-3.986c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
					</svg>
				</div>

				<!-- Text Content -->
				<div class="flex flex-col">
					{#if prompt.title && prompt.title[0] !== ''}
						<div class="font-semibold text-sm text-gray-800 dark:text-gray-100 mb-1 line-clamp-2">
							{prompt.title[0]}
						</div>
						<div class="text-xs text-gray-600 dark:text-gray-400 font-normal line-clamp-2">
							{prompt.title[1]}
						</div>
					{:else}
						<div class="font-semibold text-sm text-gray-800 dark:text-gray-100 mb-1 line-clamp-2">
							{prompt.content}
						</div>
						<!-- Optionally add a default subtitle if none exists -->
						<!-- <div class="text-xs text-gray-600 dark:text-gray-400 font-normal line-clamp-2">{$i18n.t('Click to use this prompt')}</div> -->
					{/if}
				</div>
			</button>
		{/each}
	{/if}
</div>

<!-- Removed Waterfall animation styles -->
