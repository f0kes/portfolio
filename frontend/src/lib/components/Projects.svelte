<script lang="ts">
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import SearchBar from "./SearchBar.svelte";

    interface SearchResult {
        path: string;
        name: string;
        html: string;
        sentence: string;
        similarity: number;
    }

    let searchResults = writable<SearchResult[]>([]);

    function handleSearchResults(event: CustomEvent<SearchResult[]>) {
        searchResults.set(event.detail);
    }

    function handleSearchError(event: CustomEvent<Error>) {
        console.error("Search error:", event.detail);
        // You can add error handling logic here, such as displaying an error message to the user
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
            <div class="md:w-1/4 self-start mb-8 md:mb-0" id="sticky-nav">
                <div class="sticky-nav">
                    <h3
                        class="text-4xl font-bold text-center mb-6 gradient-text"
                    >
                        Projects
                    </h3>

                    <ul class="list-group">
                        {#each $searchResults as result, index}
                            <li class="list-group-item">
                                <a
                                    href={`#result-${index}`}
                                    class="toc-item block py-4 px-4 transition duration-300"
                                >
                                    {result.name}
                                </a>
                            </li>
                        {/each}
                    </ul>
                </div>
            </div>

            <div class="md:w-2/4 space-y-12 mx-auto">
                {#each $searchResults as result, index}
                    <div class="result-section" id={`result-${index}`}>
                        <div
                            class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6"
                        >
                            <h2 class="text-2xl font-bold mb-4">
                                {result.name}
                            </h2>
                            <p class="text-gray-600 dark:text-gray-400 mb-4">
                                Path: {result.path}
                            </p>
                            <div class="mb-4">
                                <h3 class="text-lg font-semibold mb-2">
                                    Matched Sentence:
                                </h3>
                                <p>{result.sentence}</p>
                            </div>
                            <div class="mb-4">
                                <h3 class="text-lg font-semibold mb-2">
                                    Similarity Score:
                                </h3>
                                <p>{result.similarity.toFixed(4)}</p>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold mb-2">
                                    Content:
                                </h3>
                                {@html result.html}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</section>

<style>
    .list-group {
        @apply border border-gray-200 rounded-md dark:border-gray-700;
    }

    .list-group-item {
        @apply border-b border-gray-200 dark:border-gray-700 last:border-b-0;
    }

    .toc-item {
        @apply text-sm hover:bg-primary hover:text-white;
    }

    .toc-item.active {
        @apply bg-primary text-white font-semibold;
    }

    #sticky-nav {
        position: sticky;
        top: 25px;
    }

    @media (max-width: 768px) {
        #sticky-nav {
            position: static;
            margin-top: 0;
            padding-top: 0;
        }
    }
</style>
