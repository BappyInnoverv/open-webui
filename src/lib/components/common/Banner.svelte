<script lang="ts">
	import type { Banner } from '$lib/types';
	import { onMount, createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';
	import DOMPurify from 'dompurify';
	import { marked } from 'marked';

	const dispatch = createEventDispatcher();

	export let banner: Banner = {
		id: '',
		type: 'info',
		title: '',
		content: '',
		url: '',
		dismissible: true,
		timestamp: Math.floor(Date.now() / 1000)
	};
	export let className = 'mx-4';

	export let dismissed = false;

	let mounted = false;

	const classNames: Record<string, string> = {
		info: 'bg-blue-500/20 text-blue-700 dark:text-blue-200 ',
		success: 'bg-green-500/20 text-green-700 dark:text-green-200',
		warning: 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-200',
		error: 'bg-red-500/20 text-red-700 dark:text-red-200'
	};

	const dismiss = (id: string) => {
		dismissed = true;
		dispatch('dismiss', id);
	};

	onMount(() => {
		mounted = true;
	});
</script>

{#if !dismissed}
	{#if mounted}
		<div
			class="{className} top-0 left-0 right-0 p-2 px-3 flex justify-center items-center relative rounded-xl border border-gray-100 dark:border-gray-850 text-gray-800 dark:text-gary-100 bg-white dark:bg-gray-900 backdrop-blur-xl z-30 {(banner.url ||
			(!banner.url && !banner.prompts))
				? 'cursor-pointer'
				: ''}"
			transition:fade={{ delay: 100, duration: 300 }}
			on:click={() => {
				if (banner.url) {
					window.open(banner.url, '_blank');
				} else {
					// Dispatch main content if no URL, regardless of prompts
					// Prompt buttons have stopPropagation, so they won't trigger this
					dispatch('selectPrompt', banner.content);
				}
			}}
		>
			<div class=" flex flex-col md:flex-row md:items-center flex-1 text-sm w-fit gap-1.5">
				<div class="flex justify-between self-start">
					<div
						class=" text-xs font-bold {classNames[banner.type] ??
							classNames['info']}  w-fit px-2 rounded-sm uppercase line-clamp-1 mr-0.5"
					>
						{banner.type}
					</div>
					<!-- Removed mobile Learn More link section -->
				</div>

				<div class="flex-1 text-xs text-gray-700 dark:text-white">
					{@html marked.parse(DOMPurify.sanitize(banner.content))}
				</div>

				<!-- Prompt Suggestions -->
				{#if banner.prompts}
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 mt-3 w-full">
						{#each banner.prompts as prompt (prompt.title)}
							<button
								class="p-3 border rounded-lg text-left hover:bg-gray-50 dark:hover:bg-gray-800 transition duration-150 ease-in-out"
								on:click|stopPropagation={() => dispatch('selectPrompt', prompt.content)}
							>
								<div class="font-semibold text-sm text-gray-800 dark:text-gray-100">
									{prompt.title}
								</div>
								<div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
									{prompt.subtitle}
								</div>
							</button>
						{/each}
					</div>
				{/if}
			</div>
			<!-- Removed desktop Learn More link section -->
			<div class="flex self-start">
				{#if banner.dismissible}
					<button
						on:click|stopPropagation={() => {
							dismiss(banner.id);
						}}
						class="  -mt-1 -mb-2 -translate-y-[1px] ml-1.5 mr-1 text-gray-400 dark:hover:text-white"
						>&times;</button
					>
				{/if}
			</div>
		</div>
	{/if}
{/if}
