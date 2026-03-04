import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const isLoading = ref(false)
  const sidebarOpen = ref(true)
  const currentLocale = ref('en')

  const isReady = computed(() => !isLoading.value)

  function setLoading(value: boolean): void {
    isLoading.value = value
  }

  function toggleSidebar(): void {
    sidebarOpen.value = !sidebarOpen.value
  }

  function setLocale(locale: string): void {
    currentLocale.value = locale
  }

  return {
    isLoading,
    sidebarOpen,
    currentLocale,
    isReady,
    setLoading,
    toggleSidebar,
    setLocale,
  }
})
