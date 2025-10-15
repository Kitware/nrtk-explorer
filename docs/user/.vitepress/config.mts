import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "NRTK Explorer",
  description: "User guide of NRTK Explorer",
  base: '/nrtk-explorer/',
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
    ],

    sidebar: [
      { text: 'Usage', link: '/usage' },
      { text: 'Advanced Usage', link: '/advanced_usage' },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Kitware/nrtk-explorer' }
    ]
  }
})
