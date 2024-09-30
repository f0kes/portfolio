<!-- ProjectItem.svelte -->
<script lang="ts">
    import { onMount } from "svelte";
    import katex from "katex";
    import "katex/dist/katex.min.css";
    import { slide } from "svelte/transition";
    import { API_BASE_URL } from "$lib/config";

    export let result: {
        path: string;
        name: string;
        html: string;
        sentence: string;
        similarity: number;
        githubLink: string;
        previewImage: string;
    };

    export let index: number;

    let expanded = false;
    let firstParagraph = "";
    let contentWrapper: HTMLElement;
    let bannerImage = "";
    let formattedContent = "";

    function stripMdExtension(filename: string) {
        return filename.endsWith(".md") ? filename.slice(0, -3) : filename;
    }

    function processContent(html: string): string {
        // Process GitHub link
        const githubLinkMatch = html.match(/g\[(.*?)\]/);
        if (githubLinkMatch) {
            result.githubLink = githubLinkMatch[1];
            html = html.replace(githubLinkMatch[0], "");
        }

        // Process image links
        const imageRegex = /!\[\[(.*?)\]\]/g;
        let match;
        let isFirstImage = true;
        while ((match = imageRegex.exec(html)) !== null) {
            const imagePath = `${API_BASE_URL}/images/${match[1]}`;
            if (isFirstImage) {
                bannerImage = imagePath;
                isFirstImage = false;
                html = html.replace(match[0], "");
            } else {
                html = html.replace(match[0], `<img src="${imagePath}">`);
            }
        }

        return html;
    }

    function formatHtml(html: string): string {
        // Decode HTML entities
        const decodeHtml = (html: string) => {
            const txt = document.createElement("textarea");
            txt.innerHTML = html;
            return txt.value;
        };

        html = decodeHtml(html);

        // Remove HTML tags within LaTeX delimiters
        html = html.replace(/(\$.*?\$)/g, (match) => {
            return match.replace(/<[^>]*>/g, "");
        });

        // Convert single line breaks to <br> tags
        html = html.replace(/(?<!\n)\n(?!\n)/g, "<br>");

        // Replace LaTeX block expressions (wrapped with $$...$$)
        html = html.replace(/\$\$([\s\S]*?)\$\$/g, (_, latex) => {
            return katex.renderToString(latex.trim(), {
                throwOnError: false,
                displayMode: true,
            });
        });

        // Replace LaTeX inline expressions (wrapped with $...$)
        html = html.replace(/\$((?:[^$]|\\\$)+?)\$/g, (_, latex) => {
            return katex.renderToString(latex.trim(), {
                throwOnError: false,
                displayMode: false,
            });
        });

        return `<div class="formatted-content">${html}</div>`;
    }

    function toggleExpand() {
        expanded = !expanded;
        setTimeout(() => {
            const rect = contentWrapper.getBoundingClientRect();
            const offset = 225;
            const targetScrollTop = window.scrollY + rect.top - offset;
            window.scrollTo({
                top: targetScrollTop,
                behavior: "instant",
            });
        }, 1);
    }

    onMount(() => {
        const processedContent = processContent(result.html);
        formattedContent = formatHtml(processedContent);

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = formattedContent;
        const paragraphs = tempDiv.querySelectorAll("p");
        if (paragraphs.length > 0) {
            firstParagraph = paragraphs[0].outerHTML;
        }
    });
</script>

<div class="result-section" id={`result-${index}`}>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <div class="p-6">
            <div class="flex items-center mb-4">
                <h1 class="text-4xl font-bold">
                    {stripMdExtension(result.name)}
                </h1>
            </div>
        </div>

        <div class="mb-6 -mx-6">
            <img
                src={result.previewImage || bannerImage || "https://wonderfulengineering.com/wp-content/uploads/2014/10/image-wallpaper-15.jpg"}
                alt="Project Banner"
                class="w-full h-48 object-cover"
            />
        </div>

        <div class="px-6 pb-6">
            <div class="mb-4" bind:this={contentWrapper}>
                {#if !expanded}
                    <div class="formatted-content">
                        {@html firstParagraph}
                    </div>
                {:else}
                    <div
                        class="formatted-content"
                        transition:slide|local={{ duration: 300 }}
                    >
                        {@html formattedContent}
                    </div>
                {/if}
            </div>

            <div class="flex items-center space-x-4">
                <a
                    href={result.githubLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="bg-primary hover:bg-primary-dark text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"
                >
                    GitHub
                </a>
                <button
                    on:click={toggleExpand}
                    class="border border-primary text-primary hover:bg-primary hover:text-white font-bold py-2 px-4 rounded flex items-center transition duration-300 ease-in-out"
                >
                    {expanded ? "Collapse" : "Expand"}
                    <svg
                        class="w-4 h-4 ml-2 transform transition-transform duration-300 {expanded ? 'rotate-180' : ''}"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M19 9l-7 7-7-7"
                        ></path>
                    </svg>
                </button>
                <p class="text-gray-600 dark:text-gray-400">
                    Similarity: {result.similarity.toFixed(4)}
                </p>
            </div>
        </div>
    </div>
</div>

<style>
    .formatted-content :global(p) {
        margin-bottom: 1rem;
    }

    .formatted-content :global(img) {
        max-width: 100%;
        height: auto;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>