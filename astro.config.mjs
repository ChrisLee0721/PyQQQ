// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	site: 'https://chrislee0721.github.io/QuoNic/',
	integrations: [
		starlight({
			title: 'QuoNic',
			description: 'Quantum programming, as simple as writing Python',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/ChrisLee0721/QuoNic' },
			],
			sidebar: [
				{
					label: 'Start',
					items: [
						{ label: 'Quick Start', slug: 'start/quickstart' },
						{ label: 'Installation', slug: 'start/installation' },
					],
				},
				{
					label: 'Tutorials',
					items: [
						{ label: '01 Basics', slug: 'tutorials/basics' },
						{ label: '02 Algorithms', slug: 'tutorials/algorithms' },
						{ label: '03 Noise Mitigation', slug: 'tutorials/noise' },
						{ label: '04 GPU Acceleration', slug: 'tutorials/gpu' },
						{ label: '05 Advanced', slug: 'tutorials/advanced' },
					],
				},
				{
					label: 'API Reference',
					items: [
						{ label: 'Core', slug: 'api/core' },
						{ label: 'Gates', slug: 'api/gates' },
						{ label: 'Backends', slug: 'api/backends' },
						{ label: 'Compiler', slug: 'api/compiler' },
						{ label: 'ML', slug: 'api/ml' },
						{ label: 'QEC', slug: 'api/qec' },
						{ label: 'Pulse', slug: 'api/pulse' },
						{ label: 'Distributed', slug: 'api/distributed' },
						{ label: 'ZX', slug: 'api/zx' },
					],
				},
				{
					label: 'Examples',
					items: [
						{ label: 'All Examples', slug: 'examples' },
					],
				},
			],
			customCss: ['./src/styles/custom.css'],
		}),
	],
});
