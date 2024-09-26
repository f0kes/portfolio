<script lang="ts">
    import Home from "$lib/components/Home.svelte";
    import Projects from "$lib/components/Projects.svelte";
    import { projects } from "$lib/data/projects";
</script>

<svelte:head>
    <title>f0kes - Developer Portfolio</title>
</svelte:head>

<Home />
<Projects {projects} />