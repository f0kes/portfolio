import { writable } from 'svelte/store';

const prefersDarkMode = typeof window !== 'undefined'
    ? window.matchMedia('(prefers-color-scheme: dark)').matches
    : false;

const storedDarkMode = typeof localStorage !== 'undefined'
    ? localStorage.getItem('darkMode')
    : null;

export const isDarkMode = writable(
    storedDarkMode !== null
        ? storedDarkMode === 'true'
        : prefersDarkMode
);

isDarkMode.subscribe(value => {
    if (typeof localStorage !== 'undefined') {
        localStorage.setItem('darkMode', value.toString());
    }
});