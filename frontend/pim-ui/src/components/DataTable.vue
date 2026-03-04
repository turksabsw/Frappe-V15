<script setup lang="ts">
/**
 * DataTable - Reusable data table component with sorting, selection,
 * pagination, and custom cell rendering.
 *
 * Features:
 * - Column definitions with sortable headers
 * - Row selection via checkboxes (single & bulk)
 * - Pagination controls
 * - Loading and empty states
 * - Custom cell rendering via named slots
 * - Responsive design with horizontal scroll
 */
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'

export interface DataTableColumn {
  /** Unique key matching the data field */
  key: string
  /** Display label for the column header */
  label: string
  /** Whether the column is sortable */
  sortable?: boolean
  /** Column width (CSS value, e.g. '120px', '20%') */
  width?: string
  /** Text alignment */
  align?: 'left' | 'center' | 'right'
  /** Whether this column is hidden on small screens */
  hideOnMobile?: boolean
}

export interface DataTablePagination {
  /** Current page (1-based) */
  page: number
  /** Items per page */
  pageSize: number
  /** Total number of items */
  total: number
}

const props = withDefaults(
  defineProps<{
    /** Column definitions */
    columns: DataTableColumn[]
    /** Row data array */
    rows: Record<string, unknown>[]
    /** Unique row identifier field (defaults to 'name') */
    rowKey?: string
    /** Whether to show selection checkboxes */
    selectable?: boolean
    /** Set of selected row keys */
    selectedKeys?: Set<string>
    /** Whether the table is loading data */
    loading?: boolean
    /** Pagination configuration (omit for no pagination) */
    pagination?: DataTablePagination
    /** Currently sorted column key */
    sortKey?: string
    /** Sort direction */
    sortDirection?: 'asc' | 'desc'
    /** Empty state message */
    emptyMessage?: string
    /** Whether to use striped rows */
    striped?: boolean
    /** Whether rows are clickable */
    clickable?: boolean
  }>(),
  {
    rowKey: 'name',
    selectable: false,
    loading: false,
    sortDirection: 'desc',
    striped: false,
    clickable: false,
  },
)

const emit = defineEmits<{
  (e: 'sort', key: string, direction: 'asc' | 'desc'): void
  (e: 'select', key: string): void
  (e: 'select-all'): void
  (e: 'deselect-all'): void
  (e: 'page-change', page: number): void
  (e: 'page-size-change', size: number): void
  (e: 'row-click', row: Record<string, unknown>): void
}>()

const { t } = useI18n()

const pageSizeOptions = [10, 20, 50, 100]

// =========================================================================
// Computed
// =========================================================================

const allSelected = computed(() => {
  if (!props.selectable || !props.selectedKeys || props.rows.length === 0) {
    return false
  }
  return props.rows.every((row) =>
    props.selectedKeys!.has(String(row[props.rowKey])),
  )
})

const someSelected = computed(() => {
  if (!props.selectable || !props.selectedKeys || props.rows.length === 0) {
    return false
  }
  const hasAny = props.rows.some((row) =>
    props.selectedKeys!.has(String(row[props.rowKey])),
  )
  return hasAny && !allSelected.value
})

const totalPages = computed(() => {
  if (!props.pagination) return 1
  return Math.max(1, Math.ceil(props.pagination.total / props.pagination.pageSize))
})

const paginationStart = computed(() => {
  if (!props.pagination) return 0
  return (props.pagination.page - 1) * props.pagination.pageSize + 1
})

const paginationEnd = computed(() => {
  if (!props.pagination) return 0
  return Math.min(
    props.pagination.page * props.pagination.pageSize,
    props.pagination.total,
  )
})

const visiblePages = computed(() => {
  if (!props.pagination) return []
  const total = totalPages.value
  const current = props.pagination.page
  const pages: number[] = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push(-1) // ellipsis
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (current < total - 2) pages.push(-1) // ellipsis
    pages.push(total)
  }

  return pages
})

// =========================================================================
// Methods
// =========================================================================

function handleSort(column: DataTableColumn): void {
  if (!column.sortable) return

  let direction: 'asc' | 'desc' = 'asc'
  if (props.sortKey === column.key) {
    direction = props.sortDirection === 'asc' ? 'desc' : 'asc'
  }

  emit('sort', column.key, direction)
}

function handleSelectAll(): void {
  if (allSelected.value) {
    emit('deselect-all')
  } else {
    emit('select-all')
  }
}

function handleSelectRow(row: Record<string, unknown>): void {
  emit('select', String(row[props.rowKey]))
}

function handleRowClick(row: Record<string, unknown>): void {
  if (props.clickable) {
    emit('row-click', row)
  }
}

function handlePageChange(page: number): void {
  if (page >= 1 && page <= totalPages.value) {
    emit('page-change', page)
  }
}

function handlePageSizeChange(event: Event): void {
  const target = event.target as HTMLSelectElement
  emit('page-size-change', Number(target.value))
}

function getRowKey(row: Record<string, unknown>): string {
  return String(row[props.rowKey])
}

function isRowSelected(row: Record<string, unknown>): boolean {
  if (!props.selectedKeys) return false
  return props.selectedKeys.has(getRowKey(row))
}

function getColumnAlign(column: DataTableColumn): string {
  if (column.align === 'center') return 'text-center'
  if (column.align === 'right') return 'text-right'
  return 'text-left'
}

function getSortIcon(column: DataTableColumn): string {
  if (!column.sortable) return ''
  if (props.sortKey !== column.key) return '\u2195' // up-down arrows
  return props.sortDirection === 'asc' ? '\u2191' : '\u2193'
}
</script>

<template>
  <div class="data-table-wrapper">
    <!-- Table container with horizontal scroll -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-pim-border">
        <!-- Header -->
        <thead class="bg-gray-50">
          <tr>
            <!-- Selection checkbox header -->
            <th
              v-if="selectable"
              class="w-12 px-3 py-3"
            >
              <input
                type="checkbox"
                :checked="allSelected"
                :indeterminate="someSelected"
                class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                @change="handleSelectAll"
              />
            </th>

            <!-- Column headers -->
            <th
              v-for="column in columns"
              :key="column.key"
              :class="[
                'px-4 py-3 text-xs font-semibold uppercase tracking-wider text-pim-muted',
                getColumnAlign(column),
                column.sortable ? 'cursor-pointer select-none hover:text-pim-text' : '',
                column.hideOnMobile ? 'hidden md:table-cell' : '',
              ]"
              :style="column.width ? { width: column.width } : undefined"
              @click="handleSort(column)"
            >
              <span class="inline-flex items-center gap-1">
                {{ column.label }}
                <span v-if="column.sortable" class="text-xs">
                  {{ getSortIcon(column) }}
                </span>
              </span>
            </th>
          </tr>
        </thead>

        <!-- Body -->
        <tbody class="divide-y divide-pim-border bg-pim-surface">
          <!-- Loading state -->
          <tr v-if="loading">
            <td
              :colspan="(selectable ? 1 : 0) + columns.length"
              class="px-4 py-12 text-center"
            >
              <div class="flex flex-col items-center gap-2">
                <div class="h-6 w-6 animate-spin rounded-full border-2 border-primary-600 border-t-transparent" />
                <span class="text-sm text-pim-muted">{{ t('common.loading') }}</span>
              </div>
            </td>
          </tr>

          <!-- Empty state -->
          <tr v-else-if="rows.length === 0">
            <td
              :colspan="(selectable ? 1 : 0) + columns.length"
              class="px-4 py-12 text-center"
            >
              <div class="flex flex-col items-center gap-2">
                <svg class="h-12 w-12 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
                <span class="text-sm text-pim-muted">
                  {{ emptyMessage || t('common.noResults') }}
                </span>
              </div>
            </td>
          </tr>

          <!-- Data rows -->
          <template v-else>
            <tr
              v-for="row in rows"
              :key="getRowKey(row)"
              :class="[
                'transition-colors',
                striped ? 'even:bg-gray-50/50' : '',
                clickable ? 'cursor-pointer hover:bg-primary-50/50' : '',
                isRowSelected(row) ? 'bg-primary-50' : 'hover:bg-gray-50',
              ]"
              @click="handleRowClick(row)"
            >
              <!-- Selection checkbox -->
              <td
                v-if="selectable"
                class="w-12 px-3 py-3"
                @click.stop
              >
                <input
                  type="checkbox"
                  :checked="isRowSelected(row)"
                  class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  @change="handleSelectRow(row)"
                />
              </td>

              <!-- Data cells -->
              <td
                v-for="column in columns"
                :key="column.key"
                :class="[
                  'px-4 py-3 text-sm',
                  getColumnAlign(column),
                  column.hideOnMobile ? 'hidden md:table-cell' : '',
                ]"
              >
                <!-- Named slot for custom cell rendering -->
                <slot
                  :name="`cell-${column.key}`"
                  :row="row"
                  :value="row[column.key]"
                  :column="column"
                >
                  <!-- Default rendering -->
                  <span class="text-pim-text">
                    {{ row[column.key] ?? '—' }}
                  </span>
                </slot>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div
      v-if="pagination && !loading && rows.length > 0"
      class="flex items-center justify-between border-t border-pim-border px-4 py-3"
    >
      <!-- Showing X to Y of Z -->
      <div class="flex items-center gap-4 text-sm text-pim-muted">
        <span>
          Showing {{ paginationStart }} to {{ paginationEnd }}
          of {{ pagination.total }}
        </span>

        <!-- Page size selector -->
        <div class="flex items-center gap-2">
          <label for="page-size" class="sr-only">Per page</label>
          <select
            id="page-size"
            :value="pagination.pageSize"
            class="input !w-auto !py-1 text-xs"
            @change="handlePageSizeChange"
          >
            <option
              v-for="size in pageSizeOptions"
              :key="size"
              :value="size"
            >
              {{ size }} / page
            </option>
          </select>
        </div>
      </div>

      <!-- Page navigation -->
      <nav class="flex items-center gap-1">
        <!-- Previous -->
        <button
          class="btn-ghost !px-2 !py-1 text-xs"
          :disabled="pagination.page <= 1"
          @click="handlePageChange(pagination.page - 1)"
        >
          {{ t('common.previous') }}
        </button>

        <!-- Page numbers -->
        <template v-for="(page, idx) in visiblePages" :key="idx">
          <span v-if="page === -1" class="px-1 text-pim-muted">&hellip;</span>
          <button
            v-else
            :class="[
              'inline-flex h-8 w-8 items-center justify-center rounded-lg text-xs font-medium transition-colors',
              page === pagination.page
                ? 'bg-primary-600 text-white'
                : 'text-pim-muted hover:bg-gray-100 hover:text-pim-text',
            ]"
            @click="handlePageChange(page)"
          >
            {{ page }}
          </button>
        </template>

        <!-- Next -->
        <button
          class="btn-ghost !px-2 !py-1 text-xs"
          :disabled="pagination.page >= totalPages"
          @click="handlePageChange(pagination.page + 1)"
        >
          {{ t('common.next') }}
        </button>
      </nav>
    </div>
  </div>
</template>
