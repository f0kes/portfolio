<script>
  export let skills = ["JavaScript", "Svelte", "TailwindCSS", "Node.js"];
</script>

<section class="py-16 bg-white">
  <div class="container mx-auto">
    <h2 class="text-4xl font-bold text-center">About Me</h2>
    <p class="mt-4 text-center text-gray-600">
      I'm a web developer with expertise in front-end frameworks and responsive design.
    </p>
    <div class="mt-8 grid grid-cols-2 gap-4 md:grid-cols-4">
      {#each skills as skill}
        <div class="flex items-center justify-center h-24 bg-gray-100 rounded-lg">
          <span class="text-lg font-semibold">{ skill }</span>
        </div>
      {/each}
    </div>
  </div>
</section>
