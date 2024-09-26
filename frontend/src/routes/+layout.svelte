<script lang="ts">
    import "../app.css";
    import { onMount } from "svelte";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";
    import { isDarkMode } from "$lib/stores/themeStore";
    import "$lib/styles/global.css";

    onMount(() => {
        const prefersDarkMode = window.matchMedia(
            "(prefers-color-scheme: dark)",
        ).matches;
        isDarkMode.set(prefersDarkMode);
        if ($isDarkMode) {
            document.documentElement.classList.add("dark");
        }
    });
</script>

<div
    class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200"
>
    <Header />
    <main>
        <slot />
    </main>
    <Footer />
</div>

<style>
    :global(html) {
        scroll-behavior: smooth;
    }
</style>
