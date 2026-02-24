import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const prefersDarkMode = browser
    ? window.matchMedia('(prefers-color-scheme: dark)').matches
    : false;

const storedDarkMode = browser
    ? localStorage.getItem('darkMode')
    : null;

export const isDarkMode = writable(
    storedDarkMode !== null
        ? storedDarkMode === 'true'
        : prefersDarkMode
);

isDarkMode.subscribe((value) => {
    if (browser) {
        localStorage.setItem('darkMode', value.toString());
    }
});