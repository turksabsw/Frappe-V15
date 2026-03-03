<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { t } = useI18n()

interface DashboardStats {
  totalProducts: number
  activeProducts: number
  draftProducts: number
  avgCompleteness: number
}

const stats = ref<DashboardStats>({
  totalProducts: 0,
  activeProducts: 0,
  draftProducts: 0,
  avgCompleteness: 0,
})

const isLoading = ref(true)

onMounted(() => {
  isLoading.value = false
})

function navigateToProducts(): void {
  router.push('/products')
}

function navigateToOnboarding(): void {
  router.push('/onboarding')
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1>{{ t('nav.dashboard') }}</h1>
        <p class="mt-1 text-sm text-pim-muted">
          {{ t('app.subtitle') }}
        </p>
      </div>
      <button class="btn-primary" @click="navigateToOnboarding">
        {{ t('onboarding.getStarted') }}
      </button>
    </div>

    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <p class="text-pim-muted">{{ t('common.loading') }}</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div class="card">
        <p class="text-sm font-medium text-pim-muted">Total Products</p>
        <p class="mt-2 text-3xl font-bold">{{ stats.totalProducts }}</p>
      </div>
      <div class="card">
        <p class="text-sm font-medium text-pim-muted">Active</p>
        <p class="mt-2 text-3xl font-bold text-green-600">{{ stats.activeProducts }}</p>
      </div>
      <div class="card">
        <p class="text-sm font-medium text-pim-muted">Draft</p>
        <p class="mt-2 text-3xl font-bold text-amber-600">{{ stats.draftProducts }}</p>
      </div>
      <div class="card">
        <p class="text-sm font-medium text-pim-muted">Avg. Completeness</p>
        <p class="mt-2 text-3xl font-bold text-primary-600">{{ stats.avgCompleteness }}%</p>
      </div>
    </div>

    <div class="card">
      <h3>Quick Actions</h3>
      <div class="mt-4 flex gap-3">
        <button class="btn-primary" @click="navigateToProducts">
          View Products
        </button>
        <button class="btn-secondary" @click="navigateToOnboarding">
          Run Setup Wizard
        </button>
      </div>
    </div>
  </div>
</template>
