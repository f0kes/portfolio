<script lang="ts">
    export let project: {
        title: string;
        description: string;
        image: string;
        github: string;
        fullDescription: string;
    };
    export let onSelect: (selectedProject: typeof project) => void;
</script>

<div
    class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg transition duration-300 transform hover:scale-105 cursor-pointer"
    on:click={() => onSelect(project)}
>
    <img
        src={project.image}
        alt={project.title}
        class="w-full h-48 object-cover rounded-t-lg mb-4"
    />
    <h3 class="text-xl font-bold mb-2 text-primary">
        {project.title}
    </h3>
    <p class="text-gray-700 dark:text-gray-300 mb-4">
        {project.description}
    </p>
    <a
        href={project.github}
        class="text-primary hover:underline"
        target="_blank"
        rel="noopener noreferrer"
        on:click|stopPropagation
    >
        View on GitHub
    </a>
</div>
