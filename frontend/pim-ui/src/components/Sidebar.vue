<script setup lang="ts">
/**
 * Sidebar - Application navigation sidebar.
 *
 * Features:
 * - Logo/brand section
 * - Navigation links with SVG icons
 * - Active route highlighting
 * - Collapsible on mobile with overlay
 * - Bottom section with user info and settings
 * - Badge support for nav items (e.g., notification counts)
 */
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

export interface SidebarNavItem {
  /** Display label */
  label: string
  /** Route path */
  path: string
  /** Icon name (maps to built-in SVG icons) */
  icon: string
  /** Optional badge count */
  badge?: number
  /** Whether this item is visible */
  visible?: boolean
}

export interface SidebarNavGroup {
  label: string
  icon?: string
  items: Array<{ label: string; path: string }>
}

const props = withDefaults(
  defineProps<{
    /** Top navigation items (e.g. Dashboard) */
    navItems: SidebarNavItem[]
    /** Optional grouped doctype links (Products, Attributes, etc.) */
    navGroups?: SidebarNavGroup[]
    /** Currently active route path */
    currentPath: string
    /** Whether the sidebar is expanded (for mobile responsive) */
    expanded?: boolean
    /** Application title */
    appTitle?: string
  }>(),
  {
    navGroups: () => [],
    expanded: true,
    appTitle: 'Frappe PIM',
  },
)

const emit = defineEmits<{
  (e: 'navigate', path: string): void
  (e: 'close'): void
}>()

const { t } = useI18n()

const visibleItems = computed(() =>
  props.navItems.filter((item) => item.visible !== false),
)

function isActive(path: string): boolean {
  if (path === '/') return props.currentPath === '/'
  return props.currentPath.startsWith(path)
}

function handleNavigate(path: string): void {
  emit('navigate', path)
  emit('close')
}
</script>

<template>
  <!-- Overlay for mobile -->
  <Transition
    enter-active-class="transition-opacity duration-200"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="expanded"
      class="fixed inset-0 z-40 bg-black/30 lg:hidden"
      @click="emit('close')"
    />
  </Transition>

  <!-- Sidebar panel: fixed, full height, nav scrolls independently -->
  <aside
    :class="[
      'fixed inset-y-0 left-0 z-50 flex h-screen w-64 flex-col border-r border-pim-border bg-pim-surface transition-transform duration-200 lg:translate-x-0',
      expanded ? 'translate-x-0' : '-translate-x-full',
    ]"
  >
    <!-- Logo / Brand -->
    <div class="flex h-16 shrink-0 items-center gap-3 border-b border-pim-border px-6">
      <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-primary-600 text-sm font-bold text-white shadow-sm">
        P
      </div>
      <div class="flex flex-col">
        <span class="text-base font-semibold leading-tight text-pim-text">
          {{ appTitle }}
        </span>
        <span class="text-xs text-pim-muted">
          {{ t('app.subtitle') }}
        </span>
      </div>
    </div>

    <!-- Navigation (flex-1 min-h-0 so it scrolls inside sidebar) -->
    <nav class="min-h-0 flex-1 space-y-1 overflow-y-auto px-3 py-4">
      <!-- Top-level items (e.g. Dashboard) -->
      <button
        v-for="item in visibleItems"
        :key="'top-' + item.path"
        :class="[
          'group flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
          isActive(item.path)
            ? 'bg-primary-50 text-primary-700'
            : 'text-pim-muted hover:bg-gray-50 hover:text-pim-text',
        ]"
        @click="handleNavigate(item.path)"
      >
        <!-- Dashboard icon -->
        <svg
          v-if="item.icon === 'dashboard'"
          class="h-5 w-5 shrink-0"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v5a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v2a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zM14 12a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1v-7z" />
        </svg>

        <!-- Products icon -->
        <svg
          v-else-if="item.icon === 'products'"
          class="h-5 w-5 shrink-0"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        </svg>

        <!-- Categories icon -->
        <svg
          v-else-if="item.icon === 'categories'"
          class="h-5 w-5 shrink-0"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>

        <!-- Settings icon -->
        <svg
          v-else-if="item.icon === 'settings'"
          class="h-5 w-5 shrink-0"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>

        <!-- Families icon -->
        <svg
          v-else-if="item.icon === 'families'"
          class="h-5 w-5 shrink-0"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>

        <!-- Attributes icon -->
        <svg
          v-else-if="item.icon === 'attributes'"
          class="h-5 w-5 shrink-0"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>

        <!-- Fallback: generic icon -->
        <svg
          v-else
          class="h-5 w-5 shrink-0"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>

        <!-- Label -->
        <span class="flex-1 truncate">{{ item.label }}</span>

        <!-- Badge -->
        <span
          v-if="item.badge && item.badge > 0"
          class="inline-flex h-5 min-w-[20px] items-center justify-center rounded-full bg-red-100 px-1.5 text-xs font-semibold text-red-700"
        >
          {{ item.badge > 99 ? '99+' : item.badge }}
        </span>
      </button>

      <!-- Grouped doctype links -->
      <template v-for="(group, gIdx) in navGroups" :key="'group-' + gIdx">
        <div class="pt-4">
          <div class="mb-1 px-3 text-xs font-semibold uppercase tracking-wider text-pim-muted">
            {{ group.label }}
          </div>
          <button
            v-for="link in group.items"
            :key="link.path"
            :class="[
              'group flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              isActive(link.path)
                ? 'bg-primary-50 text-primary-700'
                : 'text-pim-muted hover:bg-gray-50 hover:text-pim-text',
            ]"
            @click="handleNavigate(link.path)"
          >
            <svg
              class="h-5 w-5 shrink-0"
              :class="isActive(link.path) ? 'text-primary-600' : 'text-pim-muted group-hover:text-pim-text'"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span class="flex-1 truncate text-left">{{ link.label }}</span>
          </button>
        </div>
      </template>
    </nav>

    <!-- Footer / Help section -->
    <div class="border-t border-pim-border px-3 py-3">
      <button
        class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-pim-muted transition-colors hover:bg-gray-50 hover:text-pim-text"
        @click="handleNavigate('/onboarding')"
      >
        <svg class="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="truncate">Setup Wizard</span>
      </button>
    </div>
  </aside>
</template>
