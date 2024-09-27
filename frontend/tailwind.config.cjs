/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Define your custom color palette here
        primary: {

          DEFAULT: '#E4572E', // Default primary color (used without suffix)

        },
        secondary: {

          DEFAULT: '#FE9000', // Default secondary color

        },
        background: {
          DEFAULT: '#102D40', // Default background color
        },
        secondaryBackground: {
          DEFAULT: '#B8B8D1', // Default secondary background color
        },
        text: {
          DEFAULT: '#fffffb', // Default text color
        },
      },
    },
  },
  plugins: []
};