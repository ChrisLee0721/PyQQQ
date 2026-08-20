// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	site: 'https://chrislee0721.github.io/QuoNic/',
	integrations: [
		starlight({
			title: 'QuoNic',
		}),
	],
});
