<script lang="ts">
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import SearchBar from "./SearchBar.svelte";
    import ProjectItem from "./ProjectItem.svelte";

    interface SearchResult {
        path: string;
        name: string;
        html: string;
        sentence: string;
        similarity: number;
        githubLink: string;
        previewImage: string;
    }

    let searchResults = writable<SearchResult[]>([]);
    let searchCounter = 0;

    function handleSearchResults(event: CustomEvent<SearchResult[]>) {
        searchResults.set(event.detail);
        searchCounter++; // Increment the counter on each search
    }

    function handleSearchError(event: CustomEvent<Error>) {
        console.error("Search error:", event.detail);
    }

    function stripMdExtension(filename: string) {
        return filename.endsWith(".md") ? filename.slice(0, -3) : filename;
    }

    onMount(() => {
        const tocItems = document.querySelectorAll(".toc-item");
        const resultSections = document.querySelectorAll(".result-section");
        const header = document.querySelector("header");
        const stickyNav = document.getElementById("sticky-nav");
        const resultsSection = document.getElementById("results");

        // Set header height CSS variable
        if (header) {
            const headerHeight = header.offsetHeight;
            document.documentElement.style.setProperty(
                "--header-height",
                `${headerHeight}px`,
            );
        }

        const observerOptions = {
            root: null,
            rootMargin: "-50% 0px -50% 0px",
            threshold: 0,
        };

        const observerCallback = (entries: IntersectionObserverEntry[]) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const targetId = entry.target.id;
                    tocItems.forEach((item) => {
                        item.classList.remove("active");
                        if (item.getAttribute("href") === `#${targetId}`) {
                            item.classList.add("active");
                        }
                    });
                }
            });
        };

        const observer = new IntersectionObserver(
            observerCallback,
            observerOptions,
        );
        resultSections.forEach((section) => observer.observe(section));

        // Smooth scrolling for TOC links
        tocItems.forEach((item) => {
            item.addEventListener("click", (e) => {
                e.preventDefault();
                const targetId = item.getAttribute("href");
                if (!targetId) return;
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    const headerHeight = header ? header.offsetHeight : 0;
                    const targetPosition =
                        targetElement.getBoundingClientRect().top +
                        window.pageYOffset -
                        headerHeight;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: "smooth",
                    });
                }
            });
        });

        // Adjust sticky nav position on scroll
        if (stickyNav && resultsSection) {
            const navObserver = new IntersectionObserver(
                ([e]) => {
                    if (e.isIntersecting) {
                        stickyNav.style.marginTop = `calc(-1 * var(--header-height, 4rem))`;
                    } else {
                        stickyNav.style.marginTop = "0";
                    }
                },
                {
                    threshold: [0],
                    rootMargin: `-${header?.offsetHeight || 0}px 0px 0px 0px`,
                },
            );

            navObserver.observe(resultsSection);
        }
    });
</script>

<section id="projects" class="py-20 bg-gray-100 dark:bg-gray-900">
    <h2
        class="text-3xl font-extrabold text-gray-900 dark:text-white text-center mb-16"
    >
        What is your interest?
    </h2>

    <SearchBar
        on:searchResults={handleSearchResults}
        on:searchError={handleSearchError}
    />
    <div class="container mx-auto px-6">
        <div class="flex flex-col md:flex-row md:space-x-12 justify-evenly">
            <div
                class="md:w-1/4 self-start mb-8 md:mb-0 bg-white dark:bg-gray-800 p-6 sm:p-8 rounded-lg shadow-lg"
                id="sticky-nav"
            >
                <div class="sticky-nav">
                    <h3
                        class="text-4xl font-bold text-center mb-6 gradient-text"
                    >
                        Projects
                    </h3>

                    <ul
                        class="list-group border border-gray-200 rounded-md dark:border-gray-700"
                    >
                        {#key searchCounter}
                            {#each $searchResults as result, index (result.path + searchCounter)}
                                <li
                                    class="list-group-item border-b border-gray-200 dark:border-gray-700 last:border-b-0"
                                >
                                    <a
                                        href={`#result-${index}`}
                                        class="toc-item block py-4 px-4 transition duration-300"
                                    >
                                        {stripMdExtension(result.name)}
                                    </a>
                                </li>
                            {/each}
                        {/key}
                    </ul>
                </div>
            </div>

            <div class="md:w-2/4 space-y-12 mx-auto">
                {#each $searchResults as result, index}
                    <ProjectItem {result} {index} />
                {/each}
            </div>
        </div>
    </div>
</section>

<style lang="postcss">
    .toc-item {
        @apply text-sm hover:bg-primary hover:text-white;
    }

    .toc-item.active {
        @apply bg-primary text-white font-semibold;
    }

    #sticky-nav {
        position: sticky;
        top: 100px;
    }

    @media (max-width: 768px) {
        #sticky-nav {
            position: static;
            margin-top: 0;
            padding-top: 0;
        }
    }
    [id^="result-"] {
        scroll-margin-top: 80px; /* Adjust this value based on your header height */
    }

    /* These styles will be applied globally */
    :global(.formatted-content) {
        @apply text-gray-700 dark:text-gray-300;
    }

    :global(.formatted-content p) {
        @apply mb-4;
    }

    :global(.formatted-content ul),
    :global(.formatted-content ol) {
        @apply ml-6;
    }

    :global(.formatted-content ul) {
        @apply list-disc;
    }

    :global(.formatted-content ol) {
        @apply list-decimal;
    }

    :global(.formatted-content li) {
        @apply pl-1 ml-4;
    }
    :global(.formatted-content a) {
        @apply text-primary;
    }

    :global(.formatted-content ul li::marker),
    :global(.formatted-content ol li::marker) {
        @apply text-primary font-bold;
    }
</style>
