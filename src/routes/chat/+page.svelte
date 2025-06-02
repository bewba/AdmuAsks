<script lang="ts">
	import { onMount } from 'svelte';
	import { addMessage, messages } from '$lib/stores/chat.js';
	import { isDarkMode, toggleTheme } from '$lib/stores/theme.js';
	import { marked } from 'marked';
	import { get } from 'svelte/store';
	import formatMessages from '$lib/util/formatHistory.js';

	let input: string = '';
	let loading = false;
	let chatContainer: HTMLDivElement;
	let showModal = false;
	let showModal2 = false;
	let showPromptButtons = true;
	let brainrotMode = true;
	let outOfApiCalls = false;

	const samplePrompts = ["What's the dress code policy?", 'How do I qualify for Latin Honors?'];

	onMount(async () => {
		scrollToBottom();

		const check = await fetch('/chat/status');
		const { outOfCalls } = await check.json();
		if (outOfCalls) {
			outOfApiCalls = true;
			return;
		}

		await fetch('/chat/ask', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ question: 'ping6969lol', brainrotMode: false })
		});

		setTimeout(() => {
			const textarea = document.querySelector('textarea');
			if (textarea) textarea.focus();
		}, 100);
	});

	$: if ($messages) {
		setTimeout(scrollToBottom, 100);
	}

	function scrollToBottom() {
		if (chatContainer) {
			chatContainer.scrollTop = chatContainer.scrollHeight;
		}
	}

	function useSamplePrompt(prompt: string) {
		showPromptButtons = false;
		input = prompt;
		sendMessage(prompt);
	}

	async function sendMessage(garbage?: any) {
		if (input.length < 1) return;

		const history = formatMessages(get(messages));

		let messageToSend = input;

		showPromptButtons = false;
		addMessage({ role: 'user', content: messageToSend });
		loading = true;
		input = '';

		const res = await fetch('/chat/ask', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ question: messageToSend, brainrotMode, history })
		});

		const { answer, error } = await res.json();
		loading = false;

		if (error?.includes('out of API calls')) {
			outOfApiCalls = true;
			return;
		}

		addMessage({ role: 'assistant', content: error || answer });
	}

	function toggleBrainrotMode() {
		brainrotMode = !brainrotMode;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			sendMessage();
		}
	}
</script>

<svelte:head>
	<title>AdmuAsks</title>
	<meta
		name="description"
		content="AdmuAsks - A student made AI-powered chatbot to answer all your student handbook related queries"
	/>
	<meta name="keywords" content="AdmuAsks, Admu chatbot, Admu handbook" />
	<link rel="icon" href="/favicon.ico" />

	<!-- Open Graph Meta Tags -->
	<meta property="og:title" content="AdmuAsks" />
	<meta
		property="og:description"
		content="A student-made AI chatbot answering questions from the Ateneo student handbook."
	/>
	<meta property="og:image" content="/chat/preview.png" />
	<meta property="og:url" content="https://admuasks.vercel.app/" />
	<meta property="og:type" content="website" />
	<meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div
	class={`h-screen w-full flex flex-col transition-colors duration-300 ${$isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}
>
	<header class={`${$isDarkMode ? 'bg-[#000d7a]' : 'bg-[#001196]'} text-white py-4 px-4 shadow-lg transition-colors duration-300`}>
		<div class="max-w-6xl mx-auto flex flex-wrap justify-between items-center gap-y-4">
			<!-- Title -->
			<h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold flex items-center gap-3">
				<span class="text-4xl">📘</span> Which ADMU rule am I breaking?
			</h1>

			<!-- Right Side Actions -->
			<div class="flex items-center gap-2 sm:gap-4">
				<!-- Terms -->
				<button
					on:click={() => (showModal = true)}
					class={`text-sm underline hover:text-blue-200 whitespace-nowrap cursor-pointer transition-colors duration-200 ${$isDarkMode ? 'text-gray-200' : 'text-white'}`}
				>
					Terms & Conditions
				</button>

				<!-- Dark Mode Toggle -->
				<button
					on:click={toggleTheme}
					class={`p-2 rounded-lg transition-colors duration-200 cursor-pointer ${$isDarkMode ? 'hover:bg-[#000950] text-gray-200' : 'hover:bg-[#000d7a] text-white'}`}
					aria-label="Toggle theme"
				>
					{#if $isDarkMode}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-6 w-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
							/>
						</svg>
					{:else}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-6 w-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
							/>
						</svg>
					{/if}
				</button>

				<!-- Brainrot Toggle -->
				<button
					on:click={toggleBrainrotMode}
					class={`text-sm sm:text-md px-3 py-2 rounded-lg transition-colors duration-200 cursor-pointer ${$isDarkMode ? 'hover:bg-[#000950] text-gray-200' : 'hover:bg-[#000d7a] text-white'}`}
				>
					{#if brainrotMode}
						😎 Switch to Nerd Mode
					{:else}
						🧠 Switch to Conyo Mode
					{/if}
				</button>

				<button
					on:click={() => (showModal2 = true)}
					class={`text-sm underline hover:text-blue-200 whitespace-nowrap cursor-pointer transition-colors duration-200 ${$isDarkMode ? 'text-gray-200' : 'text-white'}`}
				>
					Contact Me!
				</button>
			</div>
		</div>
	</header>

	<main class="flex flex-col flex-1 w-full mx-auto px-4 sm:px-12 py-4 gap-4 overflow-hidden">
		<div
			bind:this={chatContainer}
			class={`flex-1 w-full overflow-y-auto px-1 sm:px-2 py-2 space-y-4 rounded-lg shadow-inner transition-colors duration-300 
			${$isDarkMode ? 'bg-gray-800/50 backdrop-blur-sm' : 'bg-white'}`}
		>
			{#each $messages as msg}
				<div
					class={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} items-start gap-2 px-2 sm:px-0`}
				>
					{#if msg.role === 'assistant'}
						<div class="text-xl pt-1 hidden sm:block">🤖</div>
					{/if}
					<div
						class={`p-3 sm:p-4 rounded-2xl max-w-[90%] sm:max-w-[80%] shadow-lg transition-colors duration-300
              ${
								msg.role === 'user'
									? $isDarkMode
										? 'bg-[#000d7a] text-white shadow-[#000d7a]/20'
										: 'bg-[#001196] text-white shadow-[#001196]/20'
									: $isDarkMode
										? 'bg-[#000d7a] text-white border border-gray-700 shadow-gray-900/20'
										: 'bg-[#001196] border border-[#001196]/20 text-white shadow-gray-200'
							}`}
					>
						<div class={`prose max-w-none text-[0.9375rem] sm:text-base leading-relaxed
							${$isDarkMode 
								? 'prose-invert prose-p:text-white prose-a:text-blue-200 prose-strong:text-white prose-code:text-blue-200 prose-pre:bg-gray-900/50'
								: 'prose-p:text-white prose-a:text-blue-200 prose-strong:text-white prose-code:text-blue-200 prose-pre:bg-black/10'
							}`}>
							{@html marked.parse(msg.content)}
						</div>
					</div>
					{#if msg.role === 'user'}
						<div class="text-xl pt-1 hidden sm:block">👤</div>
					{/if}
				</div>
			{/each}

			{#if loading}
				<div class="flex justify-start ml-2">
					<div
						class={`p-3 sm:p-4 rounded-2xl shadow-sm animate-pulse transition-colors duration-300
						bg-[#001196] text-white shadow-[#001196]/20`}
					>
						<p>✍️ Thinking...</p>
					</div>
				</div>
			{/if}
		</div>

		{#if showPromptButtons}
			<div class="flex flex-wrap gap-2 sm:gap-3 mb-4 px-2 sm:px-0">
				{#each samplePrompts as prompt}
					<button
						on:click={() => useSamplePrompt(prompt)}
						class={`px-3 sm:px-4 py-2 rounded-full shadow-sm text-sm font-medium transition-all duration-200
              border hover:shadow-md hover:cursor-pointer
              ${$isDarkMode ? 'bg-gray-800 hover:bg-gray-700 text-gray-100 border-gray-700' : 'bg-white hover:bg-gray-100 text-gray-800 border-gray-300'}`}
					>
						{prompt}
					</button>
				{/each}
			</div>
		{/if}

		<div class="sticky bottom-0 bg-inherit z-10 pt-2 px-2 sm:px-0">
			<form
				on:submit|preventDefault={sendMessage}
				class={`flex flex-col gap-4 p-3 sm:p-4 rounded-lg shadow-lg transition-colors duration-300
				${$isDarkMode ? 'bg-gray-800/80 backdrop-blur-sm' : 'bg-white'}`}
			>
				<textarea
					class={`w-full p-3 sm:p-4 rounded-lg focus:outline-none focus:ring-2 min-h-[80px] sm:min-h-[100px] resize-none
              transition-colors duration-200 text-[0.9375rem] sm:text-base leading-relaxed
              ${
								$isDarkMode
									? 'bg-gray-700 text-gray-100 border-gray-600 placeholder-gray-400 focus:ring-blue-400'
									: 'bg-gray-100 text-gray-900 border-gray-300 placeholder-gray-500 focus:ring-[#001196]'
							}`}
					bind:value={input}
					placeholder="Ask something about the student handbook..."
					on:keydown={handleKeydown}
				></textarea>
				<button
					type="submit"
					class={`text-white py-2 sm:py-3 px-4 sm:px-6 rounded-xl font-semibold text-[0.9375rem] sm:text-base md:text-lg 
					transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 
					shadow-md hover:scale-[1.02] cursor-pointer
					${$isDarkMode ? 'bg-[#000d7a] hover:bg-[#000950]' : 'bg-[#001196] hover:bg-[#000d7a]'}`}
				>
					{loading ? 'Sending...' : 'Send Message'}
					{#if !loading}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-4 w-4 sm:h-5 sm:w-5"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"
							/>
						</svg>
					{/if}
				</button>
			</form>
		</div>
	</main>

	{#if showModal}
		<div
			class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4 sm:px-0"
		>
			<div
				class={`w-full max-w-2xl p-6 sm:p-8 rounded-2xl shadow-xl relative animate-fadeIn max-h-[90vh] overflow-y-auto
				transition-colors duration-300 ${$isDarkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-900'}`}
			>
				<button
					class="absolute top-3 right-4 text-xl font-bold hover:text-red-500 cursor-pointer transition-colors duration-200"
					on:click={() => (showModal = false)}>&times;</button
				>
				<h2 class="text-xl font-bold mb-4">Terms and Conditions</h2>
				<p class="text-sm mb-4 opacity-75">Last updated: May 26, 2025</p>
				<div class={`space-y-4 text-sm leading-relaxed ${$isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
					<div>
						<h3 class="font-semibold">1. Use of the Service</h3>
						<ul class="list-disc ml-5">
							<li>
								This Service is intended to provide helpful responses based on the Ateneo student
								handbook.
							</li>
							<li>
								It is <strong>not a substitute</strong> for official guidance from school administration
								or disciplinary officers.
							</li>
							<li>You are solely responsible for how you use the information provided.</li>
							<li>
								By using this Service, you agree to not hold the creator liable for any consequences
								arising from its use.
							</li>
							<li>Do not spam the bot with requests</li>
						</ul>
					</div>
					<div>
						<h3 class="font-semibold">2. Data Handling</h3>
						<ul class="list-disc ml-5">
							<li>No user data is stored or shared. Questions and responses are processed live.</li>
							<li>
								Chat submissions along with the response generated by the AI are saved to ensure the
								quality of the AI. (I do not know who is asking the questions)
							</li>
						</ul>
					</div>
					<div>
						<h3 class="font-semibold">3. Intellectual Property</h3>
						<ul class="list-disc ml-5">
							<li>All content generated by this Service is © 2025 Hans Emilio M. Lumagui.</li>
							<li>
								You may not copy, redistribute, or use this chatbot's content for commercial
								purposes without written permission.
							</li>
						</ul>
					</div>
					<div>
						<h3 class="font-semibold">4. Limitations of Liability</h3>
						<ul class="list-disc ml-5">
							<li>The Service is provided "as is" without warranties of any kind.</li>
							<li>
								The creator is <strong>not liable</strong> for any actions taken based on the chatbot's
								output.
							</li>
							<li>Use at your own discretion.</li>
						</ul>
					</div>
					<div>
						<h3 class="font-semibold">5. Changes</h3>
						<ul class="list-disc ml-5">
							<li>
								Terms may be updated at any time. Continued use of the Service means you accept the
								updated terms.
							</li>
						</ul>
					</div>
					<div class="space-y-2">
						<p class="mb-2">
							If you have questions or concerns, contact me here:
						</p>
						<div class="flex flex-col sm:flex-row gap-2 sm:items-center sm:gap-4 mb-4">
							<a href="mailto:hans_lumagui@dlsu.edu.ph" class="text-blue-500 hover:text-blue-400 transition-colors duration-200">
								hans_lumagui@dlsu.edu.ph
							</a>
							<span class="hidden sm:inline text-gray-400">or</span>
							<a href="mailto:lumaguihans0123@gmail.com" class="text-blue-500 hover:text-blue-400 transition-colors duration-200">
								lumaguihans0123@gmail.com
							</a>
						</div>
						<div class="space-y-1">
							<p class="italic text-xs text-gray-500">
								Disclaimer: Responses were created by generative AI and responses may be inaccurate.
							</p>
							<p class="italic text-xs text-gray-500">
								Disclaimer: Responses are not representative of the creator.
							</p>
							<p class="italic text-xs text-gray-500">
								Disclaimer: THIS IS NOT AN OFFICIAL ATENEO DE MANILA UNIVERSITY CHATBOT.
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	{/if}

	{#if showModal2}
		<div
			class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4 sm:px-0"
		>
			<div
				class={`w-full max-w-2xl p-6 sm:p-8 rounded-2xl shadow-xl relative animate-fadeIn max-h-[90vh] overflow-y-auto
				transition-colors duration-300 ${$isDarkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-900'}`}
			>
				<button
					class="absolute top-3 right-4 text-xl font-bold hover:text-red-500 cursor-pointer transition-colors duration-200"
					on:click={() => (showModal2 = false)}>&times;</button
				>
				<h2 class="text-xl font-bold mb-4">Let's build a cool app together!</h2>
				<div class={`space-y-4 text-sm leading-relaxed ${$isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
					<div class="space-y-3">
						<div class="flex items-center gap-2">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
								<path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
								<path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
							</svg>
							<a href="mailto:hans_lumagui@dlsu.edu.ph" 
								class="hover:text-blue-500 transition-colors duration-200">
								hans_lumagui@dlsu.edu.ph
							</a> || 
							<a href="mailto:lumaguihans0123@gmail.com" 
								class="hover:text-blue-500 transition-colors duration-200">
								lumaguihans0123@gmail.com
							</a>
						</div>
						<div class="flex items-center gap-2">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
								<path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
							</svg>
							<a href="tel:09270251730" 
								class="hover:text-blue-500 transition-colors duration-200">
								09270251730
							</a>
						</div>
						<div class="flex items-center gap-2">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M10 0C4.477 0 0 4.477 0 10c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.647.35-1.087.636-1.337-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0110 4.836c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C17.137 18.163 20 14.418 20 10c0-5.523-4.477-10-10-10z" clip-rule="evenodd" />
							</svg>
							<a href="https://github.com/lumaguimaraes" target="_blank" rel="noopener noreferrer"
								class="hover:text-blue-500 transition-colors duration-200">
								https://github.com/bewba
							</a>
						</div>
						<div class="flex items-center gap-2">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd" />
								<path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
							</svg>
							<span>Currently: 3rd Year DLSU BS Computer Science Student</span>
						</div>
					</div>
					<p class="italic mt-6">
						Have an app idea or a suggestion for the website? Let me know, I'd love to hear from you! 🚀
					</p>
				</div>
			</div>
		</div>
	{/if}
</div>

{#if outOfApiCalls}
	<div
		class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 transition-opacity duration-300"
	>
		<div
			class={`max-w-md w-full p-6 rounded-2xl shadow-xl relative animate-fadeIn
			transition-colors duration-300 ${$isDarkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-900'}`}
		>
			<h2 class="text-xl font-bold mb-4 text-red-500">API Limit Reached</h2>
			<p class={`text-sm leading-relaxed ${$isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
				We have used up of our available API calls for now. Please try again later, or contact the
				developer if you believe this is a mistake.
			</p>
			<div class="mt-4 text-right">
				<button
					class={`px-4 py-2 text-white rounded transition-colors duration-200
					${$isDarkMode ? 'bg-[#000d7a] hover:bg-[#000950]' : 'bg-[#001196] hover:bg-[#000d7a]'}`}
					on:click={() => (outOfApiCalls = false)}
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	.animate-fadeIn {
		animation: fadeIn 0.3s ease-out;
	}

	/* Custom Scrollbar Styling */
	::-webkit-scrollbar {
		width: 8px;
		height: 8px;
	}

	::-webkit-scrollbar-thumb {
		transition-property: background-color;
		transition-duration: 300ms;
		background-color: #001196;
		border-radius: 10px;
	}

	::-webkit-scrollbar-thumb:hover {
		background-color: #000d7a;
	}

	.dark ::-webkit-scrollbar-thumb {
		background-color: #000d7a;
	}

	.dark ::-webkit-scrollbar-thumb:hover {
		background-color: #000950;
	}

	::-webkit-scrollbar-track {
		background-color: transparent;
	}

	@media (max-width: 640px) {
		textarea {
			font-size: 0.95rem;
		}
	}
</style>
