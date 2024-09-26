import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const isDarkMode = writable(false);

if (browser) {
    isDarkMode.subscribe(value => {
        if (value) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    });
}