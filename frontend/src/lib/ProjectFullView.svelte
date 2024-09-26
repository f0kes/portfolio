<script lang="ts">
  export let project: {
    title: string;
    description: string;
    image: string;
    github: string;
    fullDescription: string;
  };
  export let onClose: () => void;
</script>

<div class="fixed inset-0 bg-gray-900 bg-opacity-90 flex items-center justify-center z-50 project-fullscreen">
  <div class="bg-white dark:bg-gray-800 p-8 rounded-lg max-w-3xl w-full max-h-full overflow-y-auto">
    <button 
      class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
      on:click={onClose}
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
      </svg>
    </button>
    <img
      src={project.image}
      alt={project.title}
      class="w-full h-64 object-cover rounded-lg mb-6"
    />
    <h3 class="text-3xl font-bold mb-4 text-primary">
      {project.title}
    </h3>
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

<style>
  .project-fullscreen {
    animation: scaleIn 0.3s ease-out;
  }

  @keyframes scaleIn {
    from {
      transform: scale(0.9);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }
</style>