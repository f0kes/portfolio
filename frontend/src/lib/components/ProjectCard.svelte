<script lang="ts">
    import type { Project } from "$lib/types/Project";

    export let project: Project;
    export let id: string;
</script>

<div
    {id}
    class="project-section bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden"
>
    <div class="p-6">
        <h3 class="text-2xl font-bold text-primary mb-4">{project.title}</h3>
        <img
            src={project.image}
            alt={project.title}
            class="w-full h-64 object-cover rounded-lg mb-6"
        />
        <p class="text-gray-700 dark:text-gray-300 mb-6">
            {project.fullDescription}
        </p>
        <a
            href={project.github}
            class="inline-block bg-primary text-white py-2 px-4 rounded hover:bg-primary-dark transition duration-300"
            target="_blank"
            rel="noopener noreferrer"
        >
            View on GitHub
        </a>
    </div>
</div>
