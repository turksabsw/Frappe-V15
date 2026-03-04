<script setup lang="ts">
/**
 * ProductList.vue - Product management list view.
 *
 * Features:
 * - Grid/list view toggle
 * - Search with debounce
 * - Filter panel (status, family, completeness range)
 * - Sorting by multiple fields
 * - Pagination controls
 * - Bulk selection with batch actions
 * - Status badges and completeness indicators
 */

import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useProductStore } from '@/stores/product'
import type { ProductStatus } from '@/types'

const router = useRouter()
const { t } = useI18n()
const store = useProductStore()

// =========================================================================
// Local State
// =========================================================================

/** View mode: 'grid' or 'list' */
const viewMode = ref<'grid' | 'list'>('list')

/** Search input text (debounced before API call) */
const searchInput = ref('')

/** Whether the filter panel is visible */
const showFilters = ref(false)

/** Filter form values (local, applied on submit) */
const filterStatus = ref<ProductStatus | ''>('')
const filterFamily = ref('')
const filterCompletenessMin = ref<number | undefined>(undefined)
const filterCompletenessMax = ref<number | undefined>(undefined)

/** Sort configuration */
const sortField = ref('modified')
const sortDirection = ref<'asc' | 'desc'>('desc')

/** Confirmation dialog state for bulk/delete actions */
const showDeleteConfirm = ref(false)
const deleteTargetName = ref('')

/** Bulk action dropdown state */
const showBulkActions = ref(false)

// =========================================================================
// Sort Options
// =========================================================================

const sortOptions = [
  { label: 'Last Modified', value: 'modified' },
  { label: 'Created', value: 'creation' },
  { label: 'Product Name', value: 'product_name' },
  { label: 'Completeness', value: 'completeness_score' },
  { label: 'Status', value: 'status' },
]

const statusOptions: { label: string; value: ProductStatus | '' }[] = [
  { label: 'All Statuses', value: '' },
  { label: 'Draft', value: 'Draft' },
  { label: 'Active', value: 'Active' },
  { label: 'Discontinued', value: 'Discontinued' },
  { label: 'Archived', value: 'Archived' },
]

// =========================================================================
// Computed
// =========================================================================

const paginationInfo = computed(() => {
  const start = (store.currentPage - 1) * store.pageSize + 1
  const end = Math.min(store.currentPage * store.pageSize, store.totalCount)
  return { start, end }
})

const completenessColor = (score: number): string => {
  if (score >= 80) return 'bg-green-500'
  if (score >= 50) return 'bg-amber-500'
  return 'bg-red-500'
}

const statusBadgeClass = (status: string): string => {
  switch (status) {
    case 'Active':
      return 'bg-green-100 text-green-800'
    case 'Draft':
      return 'bg-amber-100 text-amber-800'
    case 'Discontinued':
      return 'bg-gray-100 text-gray-800'
    case 'Archived':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

// =========================================================================
// Search Debounce
// =========================================================================

let searchTimeout: ReturnType<typeof setTimeout> | null = null

watch(searchInput, (value: string) => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  searchTimeout = setTimeout(() => {
    store.search(value)
  }, 300)
})

// =========================================================================
// Actions
// =========================================================================

function viewProduct(name: string): void {
  router.push(`/products/${name}`)
}

function createProduct(): void {
  router.push('/products/new')
}

function applyFilters(): void {
  store.applyFilters({
    status: filterStatus.value || undefined,
    product_family: filterFamily.value || undefined,
    completeness_min: filterCompletenessMin.value,
    completeness_max: filterCompletenessMax.value,
  })
  showFilters.value = false
}

function clearFilters(): void {
  filterStatus.value = ''
  filterFamily.value = ''
  filterCompletenessMin.value = undefined
  filterCompletenessMax.value = undefined
  store.clearFilters()
  showFilters.value = false
}

function handleSort(field: string): void {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
  store.sortBy(sortField.value, sortDirection.value)
}

function handleSortSelect(event: Event): void {
  const target = event.target as HTMLSelectElement
  sortField.value = target.value
  store.sortBy(sortField.value, sortDirection.value)
}

function toggleSortDirection(): void {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  store.sortBy(sortField.value, sortDirection.value)
}

function handlePageSizeChange(event: Event): void {
  const target = event.target as HTMLSelectElement
  store.setPageSize(Number(target.value))
}

function confirmDelete(name: string): void {
  deleteTargetName.value = name
  showDeleteConfirm.value = true
}

async function executeDelete(): Promise<void> {
  if (deleteTargetName.value) {
    await store.deleteProduct(deleteTargetName.value)
    showDeleteConfirm.value = false
    deleteTargetName.value = ''
  }
}

function cancelDelete(): void {
  showDeleteConfirm.value = false
  deleteTargetName.value = ''
}

async function bulkSetStatus(status: ProductStatus): Promise<void> {
  const names = Array.from(store.selectedProducts)
  if (names.length > 0) {
    await store.bulkUpdate(names, 'status', status)
  }
  showBulkActions.value = false
}

async function bulkDelete(): Promise<void> {
  const names = Array.from(store.selectedProducts)
  for (const name of names) {
    await store.deleteProduct(name)
  }
  store.deselectAll()
  showBulkActions.value = false
}

// =========================================================================
// Lifecycle
// =========================================================================

onMounted(async () => {
  await Promise.all([
    store.fetchProducts(),
    store.fetchFamilies(),
  ])
})
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-pim-text">{{ t('nav.products') }}</h1>
        <p class="mt-1 text-sm text-pim-muted">
          {{ store.totalCount }} product{{ store.totalCount !== 1 ? 's' : '' }} total
        </p>
      </div>
      <button
        class="btn-primary inline-flex items-center gap-2"
        @click="createProduct"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        {{ t('common.create') }}
      </button>
    </div>

    <!-- Toolbar: Search, Filters, View Toggle, Sort -->
    <div class="card">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <!-- Search -->
        <div class="relative flex-1">
          <svg
            class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-pim-muted"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="searchInput"
            type="text"
            class="input w-full pl-10"
            :placeholder="t('common.search') + ' products...'"
          />
        </div>

        <!-- Actions row -->
        <div class="flex items-center gap-2">
          <!-- Filter toggle -->
          <button
            class="btn-ghost relative inline-flex items-center gap-1"
            :class="{ 'text-primary-600': showFilters || store.activeFilterCount > 0 }"
            @click="showFilters = !showFilters"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filters
            <span
              v-if="store.activeFilterCount > 0"
              class="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-primary-600 text-[10px] font-bold text-white"
            >
              {{ store.activeFilterCount }}
            </span>
          </button>

          <!-- Sort select -->
          <div class="flex items-center gap-1">
            <select
              :value="sortField"
              class="input py-1.5 text-sm"
              @change="handleSortSelect"
            >
              <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
            <button
              class="btn-ghost p-1.5"
              :title="sortDirection === 'asc' ? 'Sort ascending' : 'Sort descending'"
              @click="toggleSortDirection"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  v-if="sortDirection === 'asc'"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"
                />
                <path
                  v-else
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4"
                />
              </svg>
            </button>
          </div>

          <!-- View mode toggle -->
          <div class="flex rounded-lg border border-pim-border">
            <button
              class="rounded-l-lg px-2.5 py-1.5 text-sm transition-colors"
              :class="viewMode === 'list' ? 'bg-primary-50 text-primary-700' : 'text-pim-muted hover:text-pim-text'"
              @click="viewMode = 'list'"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </button>
            <button
              class="rounded-r-lg px-2.5 py-1.5 text-sm transition-colors"
              :class="viewMode === 'grid' ? 'bg-primary-50 text-primary-700' : 'text-pim-muted hover:text-pim-text'"
              @click="viewMode = 'grid'"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Filter Panel (collapsible) -->
      <div v-if="showFilters" class="mt-4 border-t border-pim-border pt-4">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <!-- Status filter -->
          <div>
            <label class="mb-1 block text-sm font-medium text-pim-text">Status</label>
            <select v-model="filterStatus" class="input w-full">
              <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
          </div>

          <!-- Family filter -->
          <div>
            <label class="mb-1 block text-sm font-medium text-pim-text">Product Family</label>
            <select v-model="filterFamily" class="input w-full">
              <option value="">All Families</option>
              <option v-for="family in store.families" :key="family.name" :value="family.name">
                {{ family.family_name }}
              </option>
            </select>
          </div>

          <!-- Completeness Min -->
          <div>
            <label class="mb-1 block text-sm font-medium text-pim-text">Min Completeness %</label>
            <input
              v-model.number="filterCompletenessMin"
              type="number"
              class="input w-full"
              placeholder="0"
              min="0"
              max="100"
            />
          </div>

          <!-- Completeness Max -->
          <div>
            <label class="mb-1 block text-sm font-medium text-pim-text">Max Completeness %</label>
            <input
              v-model.number="filterCompletenessMax"
              type="number"
              class="input w-full"
              placeholder="100"
              min="0"
              max="100"
            />
          </div>
        </div>

        <div class="mt-4 flex items-center gap-2">
          <button class="btn-primary text-sm" @click="applyFilters">
            Apply Filters
          </button>
          <button class="btn-ghost text-sm" @click="clearFilters">
            Clear All
          </button>
        </div>
      </div>
    </div>

    <!-- Bulk Actions Bar -->
    <div
      v-if="store.hasSelection"
      class="flex items-center gap-3 rounded-lg border border-primary-200 bg-primary-50 px-4 py-3"
    >
      <span class="text-sm font-medium text-primary-700">
        {{ store.selectedCount }} selected
      </span>
      <div class="relative">
        <button
          class="btn-secondary text-sm"
          @click="showBulkActions = !showBulkActions"
        >
          Bulk Actions
          <svg class="ml-1 inline-block h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          v-if="showBulkActions"
          class="absolute left-0 top-full z-10 mt-1 w-48 rounded-lg border border-pim-border bg-white py-1 shadow-lg"
        >
          <button
            class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50"
            @click="bulkSetStatus('Active')"
          >
            Set Active
          </button>
          <button
            class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50"
            @click="bulkSetStatus('Draft')"
          >
            Set Draft
          </button>
          <button
            class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50"
            @click="bulkSetStatus('Archived')"
          >
            Archive
          </button>
          <hr class="my-1 border-pim-border" />
          <button
            class="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50"
            @click="bulkDelete"
          >
            Delete Selected
          </button>
        </div>
      </div>
      <button
        class="btn-ghost text-sm text-pim-muted"
        @click="store.deselectAll"
      >
        Clear Selection
      </button>
    </div>

    <!-- Error State -->
    <div
      v-if="store.error"
      class="rounded-lg border border-red-200 bg-red-50 p-4"
    >
      <div class="flex items-center gap-2">
        <svg class="h-5 w-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-sm font-medium text-red-800">{{ store.error }}</p>
      </div>
      <button class="mt-2 text-sm font-medium text-red-700 underline" @click="store.fetchProducts()">
        {{ t('common.retry') }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="store.listLoading" class="flex items-center justify-center py-12">
      <div class="flex items-center gap-3">
        <svg class="h-5 w-5 animate-spin text-primary-600" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        <span class="text-pim-muted">{{ t('common.loading') }}</span>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="store.products.length === 0 && !store.error"
      class="card py-12 text-center"
    >
      <svg class="mx-auto h-12 w-12 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
      </svg>
      <h3 class="mt-4 text-lg font-medium text-pim-text">No products found</h3>
      <p class="mt-2 text-sm text-pim-muted">
        {{ store.activeFilterCount > 0 ? 'Try adjusting your filters or search terms.' : 'Get started by creating your first product.' }}
      </p>
      <div class="mt-6">
        <button
          v-if="store.activeFilterCount > 0"
          class="btn-secondary mr-2"
          @click="clearFilters"
        >
          Clear Filters
        </button>
        <button class="btn-primary" @click="createProduct">
          Create Product
        </button>
      </div>
    </div>

    <!-- Product List View -->
    <div v-else-if="viewMode === 'list'" class="card overflow-hidden p-0">
      <!-- Table header -->
      <div class="flex items-center gap-4 border-b border-pim-border bg-gray-50 px-4 py-3 text-xs font-medium uppercase tracking-wider text-pim-muted">
        <div class="w-8">
          <input
            type="checkbox"
            class="rounded border-gray-300"
            :checked="store.allPageSelected"
            @change="store.toggleSelectAll()"
          />
        </div>
        <div class="min-w-0 flex-1">
          <button class="inline-flex items-center gap-1 hover:text-pim-text" @click="handleSort('product_name')">
            Product
            <svg v-if="sortField === 'product_name'" class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sortDirection === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
            </svg>
          </button>
        </div>
        <div class="hidden w-32 md:block">
          <button class="inline-flex items-center gap-1 hover:text-pim-text" @click="handleSort('status')">
            Status
            <svg v-if="sortField === 'status'" class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sortDirection === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
            </svg>
          </button>
        </div>
        <div class="hidden w-32 lg:block">Family</div>
        <div class="w-28">
          <button class="inline-flex items-center gap-1 hover:text-pim-text" @click="handleSort('completeness_score')">
            Completeness
            <svg v-if="sortField === 'completeness_score'" class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sortDirection === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
            </svg>
          </button>
        </div>
        <div class="w-20 text-right">Actions</div>
      </div>

      <!-- Table rows -->
      <div class="divide-y divide-pim-border">
        <div
          v-for="product in store.products"
          :key="product.name"
          class="flex cursor-pointer items-center gap-4 px-4 py-3 transition-colors hover:bg-gray-50"
          @click="viewProduct(product.name)"
        >
          <!-- Checkbox -->
          <div class="w-8" @click.stop>
            <input
              type="checkbox"
              class="rounded border-gray-300"
              :checked="store.selectedProducts.has(product.name)"
              @change="store.toggleSelection(product.name)"
            />
          </div>

          <!-- Product info -->
          <div class="min-w-0 flex-1">
            <p class="truncate font-medium text-pim-text">{{ product.product_name }}</p>
            <p class="truncate text-sm text-pim-muted">{{ product.product_code }}</p>
          </div>

          <!-- Status badge -->
          <div class="hidden w-32 md:block">
            <span
              class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
              :class="statusBadgeClass(product.status)"
            >
              {{ product.status }}
            </span>
          </div>

          <!-- Family -->
          <div class="hidden w-32 truncate text-sm text-pim-muted lg:block">
            {{ product.product_family || '—' }}
          </div>

          <!-- Completeness bar -->
          <div class="w-28">
            <div class="flex items-center gap-2">
              <div class="h-1.5 flex-1 rounded-full bg-gray-200">
                <div
                  class="h-1.5 rounded-full transition-all"
                  :class="completenessColor(product.completeness_score)"
                  :style="{ width: `${product.completeness_score}%` }"
                />
              </div>
              <span class="text-xs text-pim-muted">{{ product.completeness_score }}%</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="w-20 text-right" @click.stop>
            <button
              class="btn-ghost p-1 text-red-500 hover:text-red-700"
              title="Delete"
              @click="confirmDelete(product.name)"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Grid View -->
    <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div
        v-for="product in store.products"
        :key="product.name"
        class="card cursor-pointer transition-shadow hover:shadow-md"
        @click="viewProduct(product.name)"
      >
        <!-- Card header with checkbox -->
        <div class="mb-3 flex items-start justify-between">
          <div class="min-w-0 flex-1" @click.stop>
            <input
              type="checkbox"
              class="rounded border-gray-300"
              :checked="store.selectedProducts.has(product.name)"
              @change="store.toggleSelection(product.name)"
            />
          </div>
          <span
            class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
            :class="statusBadgeClass(product.status)"
          >
            {{ product.status }}
          </span>
        </div>

        <!-- Product placeholder image -->
        <div class="mb-3 flex h-32 items-center justify-center rounded-lg bg-gray-100">
          <svg class="h-10 w-10 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </div>

        <!-- Product info -->
        <h4 class="truncate font-medium text-pim-text">{{ product.product_name }}</h4>
        <p class="mt-0.5 truncate text-sm text-pim-muted">{{ product.product_code }}</p>

        <!-- Family -->
        <p v-if="product.product_family" class="mt-1 truncate text-xs text-pim-muted">
          {{ product.product_family }}
        </p>

        <!-- Completeness -->
        <div class="mt-3 flex items-center gap-2">
          <div class="h-1.5 flex-1 rounded-full bg-gray-200">
            <div
              class="h-1.5 rounded-full transition-all"
              :class="completenessColor(product.completeness_score)"
              :style="{ width: `${product.completeness_score}%` }"
            />
          </div>
          <span class="text-xs text-pim-muted">{{ product.completeness_score }}%</span>
        </div>

        <!-- Card actions -->
        <div class="mt-3 flex justify-end" @click.stop>
          <button
            class="btn-ghost p-1 text-red-500 hover:text-red-700"
            title="Delete"
            @click="confirmDelete(product.name)"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div
      v-if="store.totalCount > 0"
      class="flex flex-col items-center justify-between gap-4 sm:flex-row"
    >
      <!-- Info -->
      <div class="text-sm text-pim-muted">
        Showing {{ paginationInfo.start }}–{{ paginationInfo.end }} of {{ store.totalCount }}
      </div>

      <!-- Page controls -->
      <div class="flex items-center gap-2">
        <button
          class="btn-ghost px-3 py-1.5 text-sm"
          :disabled="!store.hasPrevPage"
          @click="store.prevPage()"
        >
          Previous
        </button>

        <span class="text-sm text-pim-muted">
          Page {{ store.currentPage }} of {{ store.totalPages }}
        </span>

        <button
          class="btn-ghost px-3 py-1.5 text-sm"
          :disabled="!store.hasNextPage"
          @click="store.nextPage()"
        >
          Next
        </button>
      </div>

      <!-- Page size -->
      <div class="flex items-center gap-2">
        <label class="text-sm text-pim-muted">Per page:</label>
        <select
          :value="store.pageSize"
          class="input py-1 text-sm"
          @change="handlePageSizeChange"
        >
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <Teleport to="body">
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
        @click.self="cancelDelete"
      >
        <div class="mx-4 w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
          <h3 class="text-lg font-semibold text-pim-text">Delete Product</h3>
          <p class="mt-2 text-sm text-pim-muted">
            Are you sure you want to delete this product? This action cannot be undone.
          </p>
          <div class="mt-6 flex justify-end gap-3">
            <button class="btn-ghost" @click="cancelDelete">
              {{ t('common.cancel') }}
            </button>
            <button
              class="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
              @click="executeDelete"
            >
              {{ t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
