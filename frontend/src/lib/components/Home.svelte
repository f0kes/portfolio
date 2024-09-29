<script lang="ts">
    import SocialLinks from "./SocialLinks.svelte";
</script>


<section id="home" class="flex items-center justify-center min-h-screen bg-cover bg-center px-4 py-8" >
    <div class="text-center text-white bg-white/90 dark:bg-gray-800/90 p-6 sm:p-8 rounded-lg shadow-lg max-w-md w-full fade-in backdrop-blur-sm">
        <h2 class="text-4xl sm:text-5xl font-bold mb-4 gradient-text">f0kes</h2>
        <p class="text-lg sm:text-xl mb-6 text-gray-800 dark:text-gray-200">
            I'm a developer passionate about creating amazing things with code.
        </p>
        
        <SocialLinks />
    </div>
</section>

<style>
    .fade-in {
        animation: fadeIn 1s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    

    @media (max-width: 640px) {
        .gradient-text {
            font-size: 2.5rem;
        }
    }
</style>