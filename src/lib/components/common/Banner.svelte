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
			class="{className} top-0 left-0 right-0 p-3 flex flex-col justify-between relative rounded-xl border border-gray-100 dark:border-gray-850 text-gray-800 dark:text-gary-100 bg-white dark:bg-gray-900 backdrop-blur-xl z-30 h-40 {(banner.url || (!banner.url && !banner.prompts)) /* Added h-40 for fixed height, changed padding, removed items-center, added flex-col justify-between */
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
			<div class="flex flex-col flex-1 text-sm w-full gap-1.5 overflow-hidden">
				<div class="flex justify-between items-center">
					<div
						class=" text-xs font-bold {classNames[banner.type] ??
							classNames['info']}  w-fit px-2 rounded-sm uppercase line-clamp-1 mr-0.5"
					>
						{banner.type}
					</div>
					{#if banner.dismissible}
						<button
							on:click={() => { /* Removed |stopPropagation */
								dismiss(banner.id);
							}}
							class="ml-1.5 text-gray-400 dark:hover:text-white text-lg leading-none -mt-1"
							>&times;</button>
					{/if}
				</div>

				<div class="flex-1 text-xs text-gray-700 dark:text-white line-clamp-5 overflow-hidden">
					{@html marked.parse(DOMPurify.sanitize(banner.content))}
				</div>

				{#if banner.prompts && banner.prompts.length > 0}
					<div class="mt-auto pt-1">
						<button
							class="w-full p-1.5 border rounded-md text-center text-xs hover:bg-gray-50 dark:hover:bg-gray-800 transition duration-150 ease-in-out font-medium"
							on:click={() => dispatch('selectPrompt', banner.prompts?.[0]?.content)}
						>
							{banner.prompts?.[0]?.title ?? ''}
						</button>
					</div>
				{/if}
			</div>
		</div>
	{/if}
{/if}
