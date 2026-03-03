<script setup lang="ts">
/**
 * Dashboard - Main dashboard view with product statistics, quality overview,
 * sync status, and quick actions.
 *
 * Sections:
 * 1. Header with title and primary action
 * 2. Product Statistics cards (total, active, draft, discontinued)
 * 3. Quality Overview (avg completeness, distribution chart)
 * 4. Sync Status (synced, pending, errors, conflicts)
 * 5. Quick Actions grid
 * 6. Recent Products table
 */
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useFrappeAPI, PIM_API } from '@/composables/useFrappeAPI'
import DataTable from '@/components/DataTable.vue'
import type { DataTableColumn } from '@/components/DataTable.vue'
import type { ProductMaster, ProductStatus, SyncStatusValue } from '@/types'

const router = useRouter()
const { t } = useI18n()
const api = useFrappeAPI()

// =========================================================================
// State
// =========================================================================

interface DashboardStats {
  totalProducts: number
  activeProducts: number
  draftProducts: number
  discontinuedProducts: number
  archivedProducts: number
  totalVariants: number
}

interface QualityOverview {
  avgCompleteness: number
  excellent: number
  good: number
  fair: number
  poor: number
}

interface SyncOverview {
  synced: number
  pending: number
  errors: number
  conflicts: number
  notSynced: number
}

const isLoading = ref(true)
const error = ref<string | null>(null)

const stats = ref<DashboardStats>({
  totalProducts: 0,
  activeProducts: 0,
  draftProducts: 0,
  discontinuedProducts: 0,
  archivedProducts: 0,
  totalVariants: 0,
})

const quality = ref<QualityOverview>({
  avgCompleteness: 0,
  excellent: 0,
  good: 0,
  fair: 0,
  poor: 0,
})

const syncStatus = ref<SyncOverview>({
  synced: 0,
  pending: 0,
  errors: 0,
  conflicts: 0,
  notSynced: 0,
})

const recentProducts = ref<ProductMaster[]>([])

// =========================================================================
// Computed
// =========================================================================

const qualityDistribution = computed(() => {
  const total = quality.value.excellent + quality.value.good + quality.value.fair + quality.value.poor
  if (total === 0) return { excellent: 0, good: 0, fair: 0, poor: 0 }
  return {
    excellent: Math.round((quality.value.excellent / total) * 100),
    good: Math.round((quality.value.good / total) * 100),
    fair: Math.round((quality.value.fair / total) * 100),
    poor: Math.round((quality.value.poor / total) * 100),
  }
})

const completenessColor = computed(() => {
  const avg = quality.value.avgCompleteness
  if (avg >= 80) return 'text-green-600'
  if (avg >= 60) return 'text-yellow-600'
  if (avg >= 40) return 'text-orange-600'
  return 'text-red-600'
})

const completenessBarColor = computed(() => {
  const avg = quality.value.avgCompleteness
  if (avg >= 80) return 'bg-green-500'
  if (avg >= 60) return 'bg-yellow-500'
  if (avg >= 40) return 'bg-orange-500'
  return 'bg-red-500'
})

const syncTotal = computed(() =>
  syncStatus.value.synced + syncStatus.value.pending +
  syncStatus.value.errors + syncStatus.value.conflicts +
  syncStatus.value.notSynced
)

const hasSyncIssues = computed(() =>
  syncStatus.value.errors > 0 || syncStatus.value.conflicts > 0
)

/** Recent products table columns */
const recentProductColumns: DataTableColumn[] = [
  { key: 'product_name', label: 'Product', sortable: false },
  { key: 'product_code', label: 'Code', sortable: false, hideOnMobile: true },
  { key: 'status', label: 'Status', sortable: false },
  { key: 'completeness_score', label: 'Completeness', sortable: false, align: 'right', hideOnMobile: true },
  { key: 'modified', label: 'Modified', sortable: false, hideOnMobile: true },
]

// =========================================================================
// Quick Actions
// =========================================================================

interface QuickAction {
  label: string
  description: string
  icon: string
  action: () => void
  color: string
}

const quickActions: QuickAction[] = [
  {
    label: 'Create Product',
    description: 'Add a new product to your catalog',
    icon: 'plus',
    action: () => router.push('/products/new'),
    color: 'bg-primary-50 text-primary-700 hover:bg-primary-100',
  },
  {
    label: 'View Products',
    description: 'Browse and manage all products',
    icon: 'list',
    action: () => router.push('/products'),
    color: 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100',
  },
  {
    label: 'Run Setup Wizard',
    description: 'Configure your PIM environment',
    icon: 'wizard',
    action: () => router.push('/onboarding'),
    color: 'bg-violet-50 text-violet-700 hover:bg-violet-100',
  },
  {
    label: 'Settings',
    description: 'Manage PIM configuration',
    icon: 'settings',
    action: () => router.push('/settings'),
    color: 'bg-gray-50 text-gray-700 hover:bg-gray-100',
  },
]

// =========================================================================
// Data Fetching
// =========================================================================

async function loadDashboardData(): Promise<void> {
  isLoading.value = true
  error.value = null

  try {
    await Promise.all([
      loadProductStats(),
      loadRecentProducts(),
    ])
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load dashboard data'
  } finally {
    isLoading.value = false
  }
}

async function loadProductStats(): Promise<void> {
  try {
    // Fetch product counts by status
    const [totalCount, activeCount, draftCount, discontinuedCount] = await Promise.all([
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'] }).catch(() => 0),
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_status: 'Active' }).catch(() => 0),
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_status: 'Draft' }).catch(() => 0),
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_status: 'Discontinued' }).catch(() => 0),
    ])

    stats.value = {
      totalProducts: totalCount,
      activeProducts: activeCount,
      draftProducts: draftCount,
      discontinuedProducts: discontinuedCount,
      archivedProducts: Math.max(0, totalCount - activeCount - draftCount - discontinuedCount),
      totalVariants: 0,
    }

    // Fetch variant count separately
    const variantCount = await api.getCount('Product Variant').catch(() => 0)
    stats.value.totalVariants = variantCount

    // Compute quality overview from products list
    await loadQualityOverview()
    await loadSyncOverview()
  } catch {
    // Stats loading failed - show zeros
  }
}

async function loadQualityOverview(): Promise<void> {
  try {
    const products = await api.getList<{ name: string; custom_pim_completeness: number }>({
      doctype: 'Item',
      fields: ['name', 'custom_pim_completeness'],
      filters: { custom_pim_product_id: ['is', 'set'] },
      limit_page_length: 0,
    })

    if (products.length === 0) {
      quality.value = { avgCompleteness: 0, excellent: 0, good: 0, fair: 0, poor: 0 }
      return
    }

    let totalCompleteness = 0
    let excellent = 0
    let good = 0
    let fair = 0
    let poor = 0

    for (const product of products) {
      const score = product.custom_pim_completeness || 0
      totalCompleteness += score
      if (score >= 80) excellent++
      else if (score >= 60) good++
      else if (score >= 40) fair++
      else poor++
    }

    quality.value = {
      avgCompleteness: Math.round(totalCompleteness / products.length),
      excellent,
      good,
      fair,
      poor,
    }
  } catch {
    // Quality loading failed - show zeros
  }
}

async function loadSyncOverview(): Promise<void> {
  try {
    const [syncedCount, pendingCount, errorCount, conflictCount, notSyncedCount] = await Promise.all([
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_sync_status: 'Synced' }).catch(() => 0),
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_sync_status: 'Pending' }).catch(() => 0),
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_sync_status: 'Error' }).catch(() => 0),
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_sync_status: 'Conflict' }).catch(() => 0),
      api.getCount('Item', { custom_pim_product_id: ['is', 'set'], custom_pim_sync_status: 'Not Synced' }).catch(() => 0),
    ])

    syncStatus.value = {
      synced: syncedCount,
      pending: pendingCount,
      errors: errorCount,
      conflicts: conflictCount,
      notSynced: notSyncedCount,
    }
  } catch {
    // Sync loading failed - show zeros
  }
}

async function loadRecentProducts(): Promise<void> {
  try {
    const result = await api.callMethod<{
      products: ProductMaster[]
      total: number
      page: number
      page_size: number
    }>(PIM_API.products.list, {
      page: 1,
      page_size: 5,
      order_by: 'modified',
      order_dir: 'desc',
    })
    recentProducts.value = result.products || []
  } catch {
    // Recent products loading failed
    recentProducts.value = []
  }
}

// =========================================================================
// Helpers
// =========================================================================

function getStatusBadgeClass(status: ProductStatus): string {
  switch (status) {
    case 'Active':
      return 'bg-green-100 text-green-800'
    case 'Draft':
      return 'bg-amber-100 text-amber-800'
    case 'Discontinued':
      return 'bg-red-100 text-red-800'
    case 'Archived':
      return 'bg-gray-100 text-gray-700'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}

function getCompletenessBarClass(score: number): string {
  if (score >= 80) return 'bg-green-500'
  if (score >= 60) return 'bg-yellow-500'
  if (score >= 40) return 'bg-orange-500'
  return 'bg-red-500'
}

function formatDate(dateStr?: string): string {
  if (!dateStr) return '—'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return dateStr
  }
}

function handleRecentProductClick(row: Record<string, unknown>): void {
  if (row.name) {
    router.push(`/products/${row.name}`)
  }
}

// =========================================================================
// Lifecycle
// =========================================================================

onMounted(() => {
  loadDashboardData()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1>{{ t('nav.dashboard') }}</h1>
        <p class="mt-1 text-sm text-pim-muted">
          {{ t('app.subtitle') }}
        </p>
      </div>
      <div class="flex gap-3">
        <button class="btn-secondary" @click="loadDashboardData">
          <svg class="mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
        <button class="btn-primary" @click="router.push('/products/new')">
          <svg class="mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          {{ t('products.createProduct') }}
        </button>
      </div>
    </div>

    <!-- Error Banner -->
    <div
      v-if="error"
      class="flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-4"
    >
      <svg class="h-5 w-5 shrink-0 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-sm text-red-700">{{ error }}</p>
      <button class="ml-auto text-sm font-medium text-red-700 hover:underline" @click="loadDashboardData">
        {{ t('common.retry') }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex items-center justify-center py-16">
      <div class="flex flex-col items-center gap-3">
        <div class="h-8 w-8 animate-spin rounded-full border-2 border-primary-600 border-t-transparent" />
        <p class="text-sm text-pim-muted">{{ t('common.loading') }}</p>
      </div>
    </div>

    <template v-else>
      <!-- Product Statistics Cards -->
      <section>
        <h4 class="mb-3 text-pim-muted">Product Statistics</h4>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6">
          <!-- Total Products -->
          <div class="card">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-pim-muted">Total Products</p>
              <div class="rounded-lg bg-primary-50 p-2">
                <svg class="h-5 w-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
            </div>
            <p class="mt-3 text-3xl font-bold text-pim-text">{{ stats.totalProducts }}</p>
          </div>

          <!-- Active Products -->
          <div class="card">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-pim-muted">Active</p>
              <div class="rounded-lg bg-green-50 p-2">
                <svg class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <p class="mt-3 text-3xl font-bold text-green-600">{{ stats.activeProducts }}</p>
          </div>

          <!-- Draft Products -->
          <div class="card">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-pim-muted">Draft</p>
              <div class="rounded-lg bg-amber-50 p-2">
                <svg class="h-5 w-5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
            </div>
            <p class="mt-3 text-3xl font-bold text-amber-600">{{ stats.draftProducts }}</p>
          </div>

          <!-- Discontinued -->
          <div class="card">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-pim-muted">Discontinued</p>
              <div class="rounded-lg bg-red-50 p-2">
                <svg class="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>
              </div>
            </div>
            <p class="mt-3 text-3xl font-bold text-red-600">{{ stats.discontinuedProducts }}</p>
          </div>

          <!-- Archived -->
          <div class="card">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-pim-muted">Archived</p>
              <div class="rounded-lg bg-gray-50 p-2">
                <svg class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                </svg>
              </div>
            </div>
            <p class="mt-3 text-3xl font-bold text-gray-500">{{ stats.archivedProducts }}</p>
          </div>

          <!-- Variants -->
          <div class="card">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-pim-muted">Variants</p>
              <div class="rounded-lg bg-violet-50 p-2">
                <svg class="h-5 w-5 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <p class="mt-3 text-3xl font-bold text-violet-600">{{ stats.totalVariants }}</p>
          </div>
        </div>
      </section>

      <!-- Quality Overview + Sync Status (side by side) -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Quality Overview -->
        <section class="card">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="!text-lg">Quality Overview</h3>
            <span :class="['text-2xl font-bold', completenessColor]">
              {{ quality.avgCompleteness }}%
            </span>
          </div>

          <!-- Average Completeness Bar -->
          <div class="mb-6">
            <div class="mb-1 flex justify-between text-xs text-pim-muted">
              <span>Average Completeness</span>
              <span>{{ quality.avgCompleteness }}%</span>
            </div>
            <div class="h-3 overflow-hidden rounded-full bg-gray-100">
              <div
                :class="['h-full rounded-full transition-all duration-500', completenessBarColor]"
                :style="{ width: `${quality.avgCompleteness}%` }"
              />
            </div>
          </div>

          <!-- Quality Distribution -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2">
                <span class="h-3 w-3 rounded-full bg-green-500" />
                <span class="text-pim-text">Excellent (80-100%)</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-medium text-pim-text">{{ quality.excellent }}</span>
                <span class="w-12 text-right text-xs text-pim-muted">{{ qualityDistribution.excellent }}%</span>
              </div>
            </div>
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2">
                <span class="h-3 w-3 rounded-full bg-yellow-500" />
                <span class="text-pim-text">Good (60-79%)</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-medium text-pim-text">{{ quality.good }}</span>
                <span class="w-12 text-right text-xs text-pim-muted">{{ qualityDistribution.good }}%</span>
              </div>
            </div>
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2">
                <span class="h-3 w-3 rounded-full bg-orange-500" />
                <span class="text-pim-text">Fair (40-59%)</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-medium text-pim-text">{{ quality.fair }}</span>
                <span class="w-12 text-right text-xs text-pim-muted">{{ qualityDistribution.fair }}%</span>
              </div>
            </div>
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2">
                <span class="h-3 w-3 rounded-full bg-red-500" />
                <span class="text-pim-text">Poor (0-39%)</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-medium text-pim-text">{{ quality.poor }}</span>
                <span class="w-12 text-right text-xs text-pim-muted">{{ qualityDistribution.poor }}%</span>
              </div>
            </div>
          </div>

          <!-- Distribution bar (horizontal stacked) -->
          <div
            v-if="stats.totalProducts > 0"
            class="mt-4 flex h-2 overflow-hidden rounded-full bg-gray-100"
          >
            <div class="bg-green-500" :style="{ width: `${qualityDistribution.excellent}%` }" />
            <div class="bg-yellow-500" :style="{ width: `${qualityDistribution.good}%` }" />
            <div class="bg-orange-500" :style="{ width: `${qualityDistribution.fair}%` }" />
            <div class="bg-red-500" :style="{ width: `${qualityDistribution.poor}%` }" />
          </div>
        </section>

        <!-- Sync Status -->
        <section class="card">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="!text-lg">ERPNext Sync Status</h3>
            <span
              v-if="hasSyncIssues"
              class="inline-flex items-center gap-1 rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-800"
            >
              <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Issues detected
            </span>
            <span
              v-else-if="syncTotal > 0"
              class="inline-flex items-center gap-1 rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800"
            >
              <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              All synced
            </span>
          </div>

          <div class="space-y-4">
            <!-- Synced -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-green-50">
                  <svg class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-pim-text">Synced</p>
                  <p class="text-xs text-pim-muted">Up to date with ERPNext</p>
                </div>
              </div>
              <span class="text-lg font-semibold text-green-600">{{ syncStatus.synced }}</span>
            </div>

            <!-- Pending -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50">
                  <svg class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-pim-text">Pending</p>
                  <p class="text-xs text-pim-muted">Waiting to be synced</p>
                </div>
              </div>
              <span class="text-lg font-semibold text-blue-600">{{ syncStatus.pending }}</span>
            </div>

            <!-- Errors -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-red-50">
                  <svg class="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-pim-text">Errors</p>
                  <p class="text-xs text-pim-muted">Failed to sync</p>
                </div>
              </div>
              <span :class="['text-lg font-semibold', syncStatus.errors > 0 ? 'text-red-600' : 'text-pim-muted']">
                {{ syncStatus.errors }}
              </span>
            </div>

            <!-- Conflicts -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50">
                  <svg class="h-5 w-5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-pim-text">Conflicts</p>
                  <p class="text-xs text-pim-muted">Requires manual review</p>
                </div>
              </div>
              <span :class="['text-lg font-semibold', syncStatus.conflicts > 0 ? 'text-amber-600' : 'text-pim-muted']">
                {{ syncStatus.conflicts }}
              </span>
            </div>

            <!-- Not Synced -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-50">
                  <svg class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-pim-text">Not Synced</p>
                  <p class="text-xs text-pim-muted">PIM-only products</p>
                </div>
              </div>
              <span class="text-lg font-semibold text-pim-muted">{{ syncStatus.notSynced }}</span>
            </div>
          </div>
        </section>
      </div>

      <!-- Quick Actions -->
      <section>
        <h4 class="mb-3 text-pim-muted">Quick Actions</h4>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <button
            v-for="action in quickActions"
            :key="action.label"
            :class="[
              'card flex items-start gap-4 text-left transition-all hover:shadow-md',
              action.color,
            ]"
            @click="action.action()"
          >
            <!-- Plus icon -->
            <div v-if="action.icon === 'plus'" class="mt-0.5">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </div>
            <!-- List icon -->
            <div v-else-if="action.icon === 'list'" class="mt-0.5">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </div>
            <!-- Wizard icon -->
            <div v-else-if="action.icon === 'wizard'" class="mt-0.5">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <!-- Settings icon -->
            <div v-else class="mt-0.5">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <p class="font-medium">{{ action.label }}</p>
              <p class="mt-0.5 text-xs opacity-75">{{ action.description }}</p>
            </div>
          </button>
        </div>
      </section>

      <!-- Recent Products -->
      <section class="card">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="!text-lg">Recent Products</h3>
          <button
            class="text-sm font-medium text-primary-600 hover:text-primary-700"
            @click="router.push('/products')"
          >
            View all &rarr;
          </button>
        </div>

        <DataTable
          :columns="recentProductColumns"
          :rows="(recentProducts as unknown as Record<string, unknown>[])"
          row-key="name"
          :loading="false"
          :clickable="true"
          empty-message="No products yet. Create your first product to get started."
          @row-click="handleRecentProductClick"
        >
          <!-- Product name cell -->
          <template #cell-product_name="{ row }">
            <span class="font-medium text-pim-text">{{ row.product_name }}</span>
          </template>

          <!-- Product code cell -->
          <template #cell-product_code="{ row }">
            <code class="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-pim-muted">
              {{ row.product_code }}
            </code>
          </template>

          <!-- Status badge cell -->
          <template #cell-status="{ row }">
            <span
              :class="[
                'inline-flex rounded-full px-2 py-0.5 text-xs font-medium',
                getStatusBadgeClass(row.status as ProductStatus),
              ]"
            >
              {{ row.status }}
            </span>
          </template>

          <!-- Completeness cell -->
          <template #cell-completeness_score="{ row }">
            <div class="flex items-center gap-2">
              <div class="h-1.5 w-16 overflow-hidden rounded-full bg-gray-100">
                <div
                  :class="['h-full rounded-full', getCompletenessBarClass(Number(row.completeness_score || 0))]"
                  :style="{ width: `${row.completeness_score || 0}%` }"
                />
              </div>
              <span class="text-xs text-pim-muted">{{ row.completeness_score || 0 }}%</span>
            </div>
          </template>

          <!-- Modified date cell -->
          <template #cell-modified="{ row }">
            <span class="text-xs text-pim-muted">{{ formatDate(row.modified as string) }}</span>
          </template>
        </DataTable>
      </section>
    </template>
  </div>
</template>
