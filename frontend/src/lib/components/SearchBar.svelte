<script lang="ts">
    import { API_BASE_URL } from "$lib/config";
    import { createEventDispatcher } from "svelte";

    export let query = "";
    let isLoading = false;
    let activeTags: string[] = [];

    const tags = [
        ["AI", "Data collection", "Games"],
        ["Shaders", "Python"],
        
    ];

    const dispatch = createEventDispatcher();

    async function handleSearch() {
        if (!query.trim()) return;

        isLoading = true;
        try {
            const response = await fetch(`${API_BASE_URL}/search`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) throw new Error("Network response was not ok");

            const results = await response.json();
            dispatch("searchResults", results);
        } catch (error) {
            console.error("Search error:", error);
            dispatch("searchError", error);
        } finally {
            isLoading = false;
        }
    }

    function handleKeyPress(event: KeyboardEvent) {
        if (event.key === "Enter") {
            handleSearch();
        }
    }

    function toggleTag(tag: string) {
        const index = activeTags.indexOf(tag);
        if (index === -1) {
            activeTags = [...activeTags, tag];
        } else {
            activeTags = activeTags.filter((t) => t !== tag);
        }
        query = activeTags.join(" ");
        handleSearch();
    }
</script>

<div class="search-panel w-full bg-white/90 dark:bg-gray-800/90 py-8 px-4 sm:py-16 sm:px-6 lg:px-8 my-4 sm:my-8 shadow">
    <div class="max-w-7xl mx-auto">
        <div class="container mx-auto px-4">
            <div class="container mx-auto px-4 max-w-4xl">
                <div class="flex flex-col md:grid md:grid-cols-11 items-center gap-4 md:gap-2">
                    <div class="w-full md:col-span-5">
                        <div class="flex flex-col space-y-2">
                            {#each tags as tagRow, rowIndex}
                                <div class="flex flex-wrap justify-center gap-2">
                                    {#each tagRow as tag}
                                        <button
                                            on:click={() => toggleTag(tag)}
                                            class="px-3 py-1 text-sm font-medium rounded-full transition-colors duration-200 ease-in-out {activeTags.includes(tag)
                                                ? 'bg-primary text-white'
                                                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'} hover:bg-primary hover:text-white"
                                        >
                                            {tag}
                                        </button>
                                    {/each}
                                </div>
                            {/each}
                        </div>
                    </div>
                    <div class="w-full md:col-span-1 text-center">
                        <h2 class="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-white">
                            or
                        </h2>
                    </div>
                    <div class="w-full md:col-span-5 md:ml-10">
                        <div class="flex rounded-md shadow-sm">
                            <input
                                type="text"
                                bind:value={query}
                                on:keypress={handleKeyPress}
                                placeholder="Attention is all you need!"
                                class="flex-1 min-w-0 block w-full px-3 py-2 rounded-md md:rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-primary focus:border-primary"
                            />
                            <button
                                on:click={handleSearch}
                                class="hidden md:inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-r-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                                disabled={isLoading}
                            >
                                {#if isLoading}
                                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                {:else}
                                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                {/if}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .search-panel {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    @media (min-width: 640px) {
        .search-panel {
            margin-top: 3rem;
            margin-bottom: 3rem;
        }
    }

    @media (min-width: 1024px) {
        .search-panel {
            margin-top: 4rem;
            margin-bottom: 4rem;
        }
    }
</style>