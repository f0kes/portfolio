<script lang="ts">
    import { onMount } from 'svelte';
    import { isDarkMode } from "$lib/stores/themeStore";

    function toggleDarkMode(): void {
        isDarkMode.update(value => !value);
    }

    $: if (typeof document !== 'undefined') {
        if ($isDarkMode) {
            document.documentElement.classList.add("dark");
        } else {
            document.documentElement.classList.remove("dark");
        }
    }

    onMount(() => {
        // Apply the initial dark mode state
        if ($isDarkMode) {
           
        }
         document.documentElement.classList.add("dark");
    });
</script>

<header class="bg-white dark:bg-gray-800 shadow-md fixed w-full z-10">
    <nav class="container mx-auto flex justify-between items-center py-4 px-6">
        <h1 class="text-4xl font-bold gradient-text">@f0kes</h1>
        <div class="flex items-center space-x-6">
            <a href="#home" class="hover:text-primary transition duration-300">Home</a>
            <a href="#projects" class="hover:text-primary transition duration-300">Projects</a>
            <button 
                on:click={toggleDarkMode} 
                class="p-2 rounded-full bg-gray-200 dark:bg-gray-600 hover:bg-gray-300 dark:hover:bg-gray-500 transition duration-300"
                aria-label="Toggle dark mode"
            >
                {#if $isDarkMode}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                {:else}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                {/if}
            </button>
        </div>
    </nav>
</header>

