<script setup lang="ts">
/**
 * AppLayout - Main application layout component.
 *
 * Combines Sidebar, TopBar, and main content area into a cohesive layout.
 * Supports both standard layout (sidebar + topbar + content) and blank layout
 * (full-screen content without chrome) for pages like the onboarding wizard.
 *
 * Features:
 * - Responsive sidebar with mobile overlay toggle
 * - Top bar with breadcrumbs, search, and user menu
 * - Main content area with max-width container
 * - Blank layout mode for full-screen views
 * - Sidebar state management via app store
 */
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/stores/app'
import Sidebar from './Sidebar.vue'
import TopBar from './TopBar.vue'
import type { SidebarNavItem } from './Sidebar.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const appStore = useAppStore()

const userName = ref('')

/** Whether current route uses blank layout (no sidebar/topbar) */
const isBlankLayout = computed(() => route.meta.layout === 'blank')

/** Page title from route meta */
const pageTitle = computed(() => (route.meta.title as string) || '')

/** Breadcrumbs computed from current route */
const breadcrumbs = computed(() => {
  const crumbs: Array<{ label: string; path?: string }> = []

  if (route.name === 'dashboard') {
    crumbs.push({ label: t('nav.dashboard') })
  } else if (route.name === 'products') {
    crumbs.push({ label: t('nav.dashboard'), path: '/' })
    crumbs.push({ label: t('nav.products') })
  } else if (route.name === 'product-detail') {
    crumbs.push({ label: t('nav.dashboard'), path: '/' })
    crumbs.push({ label: t('nav.products'), path: '/products' })
    const id = route.params.id as string
    crumbs.push({ label: id === 'new' ? t('products.createProduct') : id })
  } else if (route.name === 'settings') {
    crumbs.push({ label: t('nav.dashboard'), path: '/' })
    crumbs.push({ label: t('nav.settings') })
  }

  return crumbs
})

/** Navigation items for the sidebar */
const navItems = computed<SidebarNavItem[]>(() => [
  {
    label: t('nav.dashboard'),
    path: '/',
    icon: 'dashboard',
  },
  {
    label: t('nav.products'),
    path: '/products',
    icon: 'products',
  },
  {
    label: t('nav.settings'),
    path: '/settings',
    icon: 'settings',
  },
])

function handleNavigate(path: string): void {
  router.push(path)
}

function handleToggleSidebar(): void {
  appStore.toggleSidebar()
}

function handleSearch(query: string): void {
  if (query) {
    router.push({ path: '/products', query: { search: query } })
  }
}
</script>

<template>
  <!-- Blank layout (for onboarding wizard, etc.) -->
  <div v-if="isBlankLayout" class="min-h-screen bg-pim-bg">
    <slot />
  </div>

  <!-- Standard layout with sidebar + topbar + content -->
  <div v-else class="flex min-h-screen bg-pim-bg">
    <!-- Sidebar -->
    <Sidebar
      :nav-items="navItems"
      :current-path="route.path"
      :expanded="appStore.sidebarOpen"
      @navigate="handleNavigate"
      @close="appStore.sidebarOpen = false"
    />

    <!-- Main area (topbar + content) -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Top bar -->
      <TopBar
        :title="pageTitle"
        :breadcrumbs="breadcrumbs"
        :user-name="userName"
        :show-search="true"
        :show-sidebar-toggle="true"
        @toggle-sidebar="handleToggleSidebar"
        @search="handleSearch"
        @navigate="handleNavigate"
      />

      <!-- Main content area -->
      <main class="flex-1 overflow-y-auto">
        <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>
