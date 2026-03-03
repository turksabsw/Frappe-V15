import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import router from './router'

import './assets/css/main.css'

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: {
      app: {
        title: 'Frappe PIM',
        subtitle: 'Product Information Management',
      },
      nav: {
        dashboard: 'Dashboard',
        products: 'Products',
        categories: 'Categories',
        attributes: 'Attributes',
        families: 'Families',
        settings: 'Settings',
      },
      common: {
        save: 'Save',
        cancel: 'Cancel',
        delete: 'Delete',
        edit: 'Edit',
        create: 'Create',
        search: 'Search',
        loading: 'Loading...',
        noResults: 'No results found',
        error: 'An error occurred',
        retry: 'Retry',
      },
      onboarding: {
        welcome: 'Welcome to Frappe PIM',
        getStarted: 'Get Started',
        skip: 'Skip for now',
        next: 'Next',
        back: 'Back',
        finish: 'Finish Setup',
      },
    },
  },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.mount('#app')
