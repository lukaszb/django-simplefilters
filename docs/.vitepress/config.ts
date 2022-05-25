import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/django-simplefilters/',
  title: 'django-simplefilters',
  description: 'Documentation for filtering library for Django framework.',
  markdown: {
    lineNumbers: false,
    // anchor: {
      // permalink: anchor.permalink.headerLink()
    // },
  },
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/', activeMatch: '^/$|^/guide/' },
      {
        text: 'Api Reference',
        link: '/api/',
        activeMatch: '^/api/'
      },
      {
        text: 'Repo',
        link: 'https://github.com/lukaszb/django-simplefilters'
      },
      {
        text: 'Release Notes',
        link: 'https://github.com/lukaszb/django-simplefilters/releases'
      },
    ],

    sidebar: {
      '/guide/': getGuideSidebar(),
      '/api/': getApiSidebar(),
      '/': getGuideSidebar()
    }
  }
})


function getGuideSidebar() {
  return [
    {
      text: 'Introduction',
      children: [
        { text: 'Quickstart', link: '/' },
        { text: 'DRF', link: '/guide/drf' },
        { text: 'Django', link: '/guide/django' },
      ]
    },
    {
      text: 'Advanced',
      children: [
        { text: 'Testing', link: '/guide/testing' },
        { text: 'Custom filter fields', link: '/guide/custom-filter-fields' },
      ]
    }
  ]
}

function getApiSidebar() {
  return [
    {
      text: 'Api Reference',
      children: [
        { text: 'Filterset', link: '/api/filterset' },
        { text: 'Filters', link: '/api/filters' },
      ],
    },
  ]
}