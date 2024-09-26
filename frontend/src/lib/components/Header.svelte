<script lang="ts">
    import { isDarkMode } from "$lib/stores/themeStore";

    function toggleDarkMode(): void {
        isDarkMode.update(value => !value);
        if ($isDarkMode) {
            document.documentElement.classList.add("dark");
        } else {
            document.documentElement.classList.remove("dark");
        }
    }
</script>

<header class="bg-white dark:bg-gray-800 shadow-md fixed w-full z-10">
    <nav class="container mx-auto flex justify-between items-center py-4 px-6">
        <h1 class="text-4xl font-bold gradient-text">@f0kes</h1>
        <div class="flex items-center space-x-6">
            <a href="#home" class="hover:text-primary transition duration-300">Home</a>
            <a href="#projects" class="hover:text-primary transition duration-300">Projects</a>
        </div>
    </nav>
</header>