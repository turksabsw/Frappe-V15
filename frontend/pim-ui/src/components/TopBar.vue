<script setup lang="ts">
/**
 * TopBar - Application top navigation bar.
 *
 * Features:
 * - Page title / breadcrumb display
 * - Global search input
 * - Sidebar toggle for responsive views
 * - User profile menu placeholder
 * - Notification bell placeholder
 */
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = withDefaults(
  defineProps<{
    /** Current page title */
    title?: string
    /** Breadcrumb path items */
    breadcrumbs?: Array<{ label: string; path?: string }>
    /** Whether to show the search input */
    showSearch?: boolean
    /** Whether to show the sidebar toggle button */
    showSidebarToggle?: boolean
    /** Current user name or email */
    userName?: string
  }>(),
  {
    showSearch: true,
    showSidebarToggle: true,
    userName: '',
  },
)

const emit = defineEmits<{
  (e: 'toggle-sidebar'): void
  (e: 'search', query: string): void
  (e: 'navigate', path: string): void
}>()

const { t } = useI18n()

const searchQuery = ref('')
const showUserMenu = ref(false)

const userInitials = computed(() => {
  if (!props.userName) return '?'
  return props.userName
    .split(/[\s@]/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join('')
})

function handleSearch(): void {
  emit('search', searchQuery.value.trim())
}

function handleSearchInput(event: Event): void {
  const target = event.target as HTMLInputElement
  searchQuery.value = target.value
}

function handleBreadcrumbClick(path?: string): void {
  if (path) {
    emit('navigate', path)
  }
}

function toggleUserMenu(): void {
  showUserMenu.value = !showUserMenu.value
}

function closeUserMenu(): void {
  showUserMenu.value = false
}
</script>

<template>
  <header class="flex h-16 shrink-0 items-center border-b border-pim-border bg-pim-surface px-4 sm:px-6">
    <!-- Left section: sidebar toggle + breadcrumbs/title -->
    <div class="flex flex-1 items-center gap-3">
      <!-- Sidebar toggle (mobile) -->
      <button
        v-if="showSidebarToggle"
        class="btn-ghost !p-2 lg:hidden"
        aria-label="Toggle sidebar"
        @click="emit('toggle-sidebar')"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- Breadcrumbs -->
      <nav
        v-if="breadcrumbs && breadcrumbs.length > 0"
        class="flex items-center gap-1 text-sm"
        aria-label="Breadcrumb"
      >
        <template v-for="(crumb, idx) in breadcrumbs" :key="idx">
          <span v-if="idx > 0" class="text-pim-muted">/</span>
          <button
            v-if="crumb.path"
            class="text-pim-muted transition-colors hover:text-pim-text"
            @click="handleBreadcrumbClick(crumb.path)"
          >
            {{ crumb.label }}
          </button>
          <span v-else class="font-medium text-pim-text">
            {{ crumb.label }}
          </span>
        </template>
      </nav>

      <!-- Page title (when no breadcrumbs) -->
      <h2 v-else-if="title" class="!text-lg font-semibold text-pim-text">
        {{ title }}
      </h2>
    </div>

    <!-- Center section: search -->
    <div
      v-if="showSearch"
      class="hidden max-w-md flex-1 px-4 sm:block"
    >
      <div class="relative">
        <svg
          class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-pim-muted"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          :value="searchQuery"
          :placeholder="t('common.search') + '...'"
          class="input !py-1.5 !pl-9 !text-sm"
          @input="handleSearchInput"
          @keydown.enter="handleSearch"
        />
      </div>
    </div>

    <!-- Right section: actions -->
    <div class="flex items-center gap-2">
      <!-- Notification bell -->
      <button
        class="btn-ghost relative !p-2"
        aria-label="Notifications"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
      </button>

      <!-- User avatar/menu -->
      <div class="relative">
        <button
          class="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-xs font-semibold text-primary-700 transition-colors hover:bg-primary-200"
          aria-label="User menu"
          @click="toggleUserMenu"
          @blur="closeUserMenu"
        >
          {{ userInitials }}
        </button>

        <!-- Dropdown menu -->
        <Transition
          enter-active-class="transition duration-100 ease-out"
          enter-from-class="scale-95 opacity-0"
          enter-to-class="scale-100 opacity-100"
          leave-active-class="transition duration-75 ease-in"
          leave-from-class="scale-100 opacity-100"
          leave-to-class="scale-95 opacity-0"
        >
          <div
            v-if="showUserMenu"
            class="absolute right-0 top-full z-50 mt-1 w-48 rounded-lg border border-pim-border bg-pim-surface py-1 shadow-lg"
          >
            <div class="border-b border-pim-border px-4 py-2">
              <p class="truncate text-sm font-medium text-pim-text">
                {{ userName || 'User' }}
              </p>
            </div>
            <button
              class="flex w-full items-center gap-2 px-4 py-2 text-sm text-pim-muted transition-colors hover:bg-gray-50 hover:text-pim-text"
              @mousedown.prevent
              @click="emit('navigate', '/settings')"
            >
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {{ t('nav.settings') }}
            </button>
          </div>
        </Transition>
      </div>
    </div>
  </header>
</template>
