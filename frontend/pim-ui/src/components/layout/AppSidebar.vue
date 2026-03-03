<script setup lang="ts">
import { useI18n } from 'vue-i18n'

interface NavItem {
  name: string
  path: string
  icon: string
}

defineProps<{
  navItems: NavItem[]
  currentPath: string
}>()

const emit = defineEmits<{
  (e: 'navigate', path: string): void
}>()

const { t } = useI18n()

function handleNavigate(path: string): void {
  emit('navigate', path)
}
</script>

<template>
  <aside class="flex w-64 flex-col border-r border-pim-border bg-pim-surface">
    <div class="flex h-16 items-center gap-2 border-b border-pim-border px-6">
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-sm font-bold text-white">
        P
      </div>
      <span class="text-lg font-semibold text-pim-text">
        {{ t('app.title') }}
      </span>
    </div>

    <nav class="flex-1 space-y-1 px-3 py-4">
      <button
        v-for="item in navItems"
        :key="item.path"
        class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
        :class="
          currentPath === item.path
            ? 'bg-primary-50 text-primary-700'
            : 'text-pim-muted hover:bg-gray-50 hover:text-pim-text'
        "
        @click="handleNavigate(item.path)"
      >
        {{ item.name }}
      </button>
    </nav>
  </aside>
</template>
