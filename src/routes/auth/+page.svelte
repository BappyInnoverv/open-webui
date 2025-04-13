<script lang="ts"> // Added lang="ts"
	import { toast } from 'svelte-sonner';

	import { onMount, getContext } from 'svelte'; // Removed tick
	import type { Writable } from 'svelte/store'; // Use 'import type'
	import type { i18n as i18nType } from 'i18next'; // Import i18next type
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { getBackendConfig } from '$lib/apis';
	// Removed userSignUp
	import { ldapUserSignIn, getSessionUser, userSignIn } from '$lib/apis/auths';
	import type { SessionUser } from '$lib/stores'; // Import SessionUser type

	import { WEBUI_API_BASE_URL, WEBUI_BASE_URL } from '$lib/constants';
	import { WEBUI_NAME, config, user, socket } from '$lib/stores';

	// Removed generateInitialsImage, canvasPixelTest
	import {} from '$lib/utils';

	// Removed Spinner
	// Removed OnBoarding

	// Get the i18n store from context and assert its type
	const i18n = getContext('i18n') as Writable<i18nType>;

	let loaded = false;

	let mode = $config?.features.enable_ldap ? 'ldap' : 'signin';
	// console.log('Auth Page Mount: enable_ldap =', $config?.features.enable_ldap, ' | mode =', mode); // Removed Debug log

	// Pre-calculate the condition for the main if block
	$: showTrustedHeaderSignIn = ($config?.features.auth_trusted_header ?? false) || $config?.features.auth === false;

	// let name = ''; // Removed as per new design
	let email = ''; // Used for the first input field (can be email or username depending on backend logic)
	let password = '';

	let ldapUsername = ''; // Keep for potential LDAP logic backend if needed, map 'email' variable to it in submitHandler if mode is ldap

	const querystringValue = (key: string) => { // Added type for key
		const querystring = window.location.search;
		const urlParams = new URLSearchParams(querystring);
		return urlParams.get(key);
	};

	const setSessionUser = async (sessionUser: SessionUser | null) => { // Added type for sessionUser
		if (sessionUser) {
			console.log(sessionUser); // Keep this log for now to confirm success
			toast.success($i18n.t(`You're now logged in.`)); // Use store syntax
			if (sessionUser.token) {
				localStorage.token = sessionUser.token;
			}

			if ($socket) { // Added null check for socket
				$socket.emit('user-join', { auth: { token: sessionUser.token } });
			}
			await user.set(sessionUser);
			await config.set(await getBackendConfig());

			const redirectPath = querystringValue('redirect') || '/';
			goto(redirectPath);
		}
	};

	const signInHandler = async () => {
		const sessionUser = await userSignIn(email, password).catch((error: any) => { // Added type any to error
			// Improved error display
			const errorMessage = error?.detail || error?.message || JSON.stringify(error);
			toast.error(errorMessage);
			return null;
		});

		await setSessionUser(sessionUser);
	};

	// Removed unused signUpHandler
	// const signUpHandler = async () => { ... };

	const ldapSignInHandler = async () => {
		const sessionUser = await ldapUserSignIn(ldapUsername, password).catch((error: any) => { // Added type any to error
			// Improved error display
			const errorMessage = error?.detail || error?.message || JSON.stringify(error);
			toast.error(errorMessage);
			return null;
		});
		await setSessionUser(sessionUser);
	};

	const submitHandler = async () => {
		// console.log('submitHandler called. Mode:', mode); // Removed Debug log
		// Simplified submit logic based on the visual design
		// Assumes the first field maps to 'email' for signin or 'ldapUsername' for ldap
		if (mode === 'ldap') {
			// console.log('Calling ldapSignInHandler with username:', email); // Removed Debug log
			ldapUsername = email; // Map the first input field value
			await ldapSignInHandler();
		} else { // Default to signin mode visually
			// console.log('Calling signInHandler with email:', email); // Removed Debug log
			await signInHandler();
		}
		// Removed signup mode handling from UI submit
	};

	const checkOauthCallback = async () => {
		if (!$page.url.hash) {
			return;
		}
		const hash = $page.url.hash.substring(1);
		if (!hash) {
			return;
		}
		const params = new URLSearchParams(hash);
		const token = params.get('token');
		if (!token) {
			return;
		}
		const sessionUser = await getSessionUser(token).catch((error) => {
			toast.error(`${error}`);
			return null;
		});
		if (!sessionUser) {
			return;
		}
		localStorage.token = token;
		await setSessionUser(sessionUser);
	};

	// Removed onboarding variable
	// let onboarding = false;

	// Removed unused setLogoImage function
	// async function setLogoImage() { ... }

	onMount(async () => {
		if ($user !== undefined) {
			const redirectPath = querystringValue('redirect') || '/';
			goto(redirectPath);
		}
		await checkOauthCallback();

		loaded = true;
		// Removed setLogoImage call

		// Removed auto-signin logic for trusted header/auth disabled for now
		// if (($config?.features.auth_trusted_header ?? false) || $config?.features.auth === false) {
		// 	await signInHandler();
		// }
		// Removed onboarding logic
		// else {
		// 	onboarding = $config?.onboarding ?? false;
		// }
	});
</script>

<svelte:head>
	<title>
		{`${$WEBUI_NAME}`}
	</title>
</svelte:head>

<!-- Removed OnBoarding component -->

<div class="w-full h-screen max-h-[100dvh] text-white relative">
	<div class="w-full h-full absolute top-0 left-0 bg-[#F3F4F6]"></div>


	{#if loaded}

		<div
			class="fixed bg-[#F3F4F6] min-h-screen w-full flex justify-center items-center font-primary z-50 text-black"
		>
			<div class="w-full sm:max-w-md p-10 bg-white rounded-lg shadow-md flex flex-col text-center">

					<div class="my-auto pb-10 w-full">
						<div class="mb-8 text-center">
							<span class="text-3xl font-bold tracking-wider text-black">INNOVERV</span><span class="text-3xl font-bold text-red-600">.</span>
						</div>

						<form
							class="flex flex-col justify-center"
							on:submit={(e) => {
								e.preventDefault();
								submitHandler();
							}}
						>

							<div class="flex flex-col space-y-4">
								<div>
									<input
										bind:value={email}
										type="text"
										class="w-full text-sm p-4 rounded-md border border-gray-300 bg-white outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder-gray-500"
										autocomplete="username"
										name="username"
										placeholder="Innoverv"
										required
									/>
								</div>

								<div>
									<input
										bind:value={password}
										type="password"
										class="w-full text-sm p-4 rounded-md border border-gray-300 bg-white outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder-gray-500"
										placeholder="*****"
										autocomplete="current-password"
										name="current-password"
										required
									/>
								</div>
							</div>

							<div class="mt-8">
								<button
									class="bg-[#0D9488] hover:bg-[#0F766E] text-white transition w-full rounded-md font-semibold text-lg py-3"
									type="submit"
								>
									Login
								</button>
							</div>
						</form>

						<div class="mt-12 text-center text-xs text-gray-500">
							© Copyright 2025, INNOVERV. All Rights Reserved
						</div>
					</div>

			</div>
		</div>
	{/if}
</div>
