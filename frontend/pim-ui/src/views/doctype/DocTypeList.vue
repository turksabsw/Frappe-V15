<script setup lang="ts">
/**
 * DocTypeList – generic list view for any PIM DocType.
 * Same layout as Products: row click opens doc, columns Product/Name, Status, FAMILY, Completeness, ACTIONS.
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFrappeAPI } from '@/composables/useFrappeAPI'

const route = useRoute()
const router = useRouter()
const api = useFrappeAPI()

const doctype = computed(() => (route.params.doctype as string) || '')
const decodedDoctype = computed(() => decodeURIComponent(doctype.value))

interface ListRow {
  name: string
  modified?: string
  owner?: string
  status?: string
  product_family?: string
  family?: string
  completeness_score?: number
  product_code?: string
  collection_name?: string
  type_name?: string
  family_name?: string
  variant_name?: string
  [key: string]: unknown
}

const rows = ref<ListRow[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const totalCount = ref(0)
const page = ref(1)
const pageSize = ref(20)
const search = ref('')

/** Only request fields that exist on every Frappe doctype (others cause 417 for some doctypes) */
const LIST_FIELDS = ['name', 'modified', 'owner']

async function loadList(): Promise<void> {
  if (!decodedDoctype.value) return
  loading.value = true
  error.value = null
  try {
    const filters = search.value
      ? [['name', 'like', `%${search.value}%`] as [string, string, string]]
      : undefined
    const list = await api.getList<ListRow>({
      doctype: decodedDoctype.value,
      fields: LIST_FIELDS,
      filters,
      order_by: 'modified desc',
      limit_start: (page.value - 1) * pageSize.value,
      limit_page_length: pageSize.value,
    })
    rows.value = list || []
    totalCount.value = list?.length ?? 0
  } catch (e: unknown) {
    const msg = e && typeof e === 'object' && 'message' in e ? String((e as { message: string }).message) : 'Failed to load list'
    error.value = msg
    rows.value = []
  } finally {
    loading.value = false
  }
}

/** Row click: open doc in app (all doctypes use generic form with full Desk layout) */
function openRow(row: ListRow): void {
  router.push(`/doc/${encodeURIComponent(decodedDoctype.value)}/${encodeURIComponent(row.name)}`)
}

function openInDesk(e: Event, name: string): void {
  e.stopPropagation()
  const base = typeof window !== 'undefined' && (window as unknown as { __frappe_base_url?: string }).__frappe_base_url
  const baseUrl = base || 'http://localhost:8000'
  const slug = decodedDoctype.value.replace(/\s+/g, '-').toLowerCase()
  const url = `${baseUrl}/app/${slug}/${encodeURIComponent(name)}`
  window.open(url, '_blank')
}

/** Subtitle for Product column (code, type, family name – avoid repeating name) */
function rowSubtitle(row: ListRow): string {
  const s = (row.product_code ?? row.collection_name ?? row.type_name ?? row.family_name ?? row.variant_name) as string | undefined
  return s && s !== row.name ? s : ''
}

function statusBadgeClass(status: string | undefined): string {
  if (!status) return 'bg-gray-100 text-gray-800'
  switch (status) {
    case 'Active': case 'Published': return 'bg-green-100 text-green-800'
    case 'Draft': return 'bg-amber-100 text-amber-800'
    case 'Discontinued': case 'Archived': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

function completenessColor(score: number | undefined): string {
  if (score == null) return 'bg-gray-200'
  if (score >= 80) return 'bg-green-500'
  if (score >= 50) return 'bg-amber-500'
  return 'bg-red-500'
}

onMounted(() => loadList())
watch([doctype, page, pageSize], () => loadList())
</script>

<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <h1 class="text-2xl font-semibold text-pim-text">
        {{ decodedDoctype }}
      </h1>
      <div class="flex items-center gap-2">
        <input
          v-model="search"
          type="search"
          placeholder="Search by name..."
          class="rounded-md border border-pim-border px-3 py-2 text-sm"
          @keyup.enter="loadList"
        />
        <button
          type="button"
          class="btn-primary rounded-md px-4 py-2 text-sm"
          @click="loadList"
        >
          Search
        </button>
      </div>
    </div>

    <p v-if="error" class="rounded-lg bg-red-50 p-4 text-sm text-red-700">
      {{ error }}
    </p>

    <div v-else-if="loading" class="flex justify-center py-12">
      <span class="text-pim-muted">Loading...</span>
    </div>

    <!-- Table: same columns as Product list – checkbox, Product, Status, FAMILY, Completeness, ACTIONS -->
    <div v-else class="overflow-hidden rounded-lg border border-pim-border bg-white shadow">
      <!-- Header row -->
      <div class="flex items-center gap-4 border-b border-pim-border bg-gray-50 px-4 py-3 text-xs font-medium uppercase tracking-wider text-pim-muted">
        <div class="w-8" />
        <div class="min-w-0 flex-1">Product</div>
        <div class="hidden w-32 md:block">Status</div>
        <div class="hidden w-32 truncate lg:block">Family</div>
        <div class="w-28">Completeness</div>
        <div class="w-24 text-right">Actions</div>
      </div>

      <!-- Rows: clickable, open on row click -->
      <div class="divide-y divide-pim-border">
        <div
          v-for="row in rows"
          :key="row.name"
          class="flex cursor-pointer items-center gap-4 px-4 py-3 transition-colors hover:bg-gray-50"
          @click="openRow(row)"
        >
          <div class="w-8 flex-shrink-0" @click.stop>
            <input type="checkbox" class="rounded border-gray-300" :checked="false" @change.prevent="">
          </div>

          <div class="min-w-0 flex-1">
            <p class="truncate font-medium text-pim-text">{{ row.name }}</p>
            <p v-if="rowSubtitle(row)" class="truncate text-sm text-pim-muted">{{ rowSubtitle(row) }}</p>
          </div>

          <div class="hidden w-32 flex-shrink-0 md:block">
            <span
              v-if="row.status"
              class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
              :class="statusBadgeClass(row.status)"
            >
              {{ row.status }}
            </span>
            <span v-else class="text-sm text-pim-muted">–</span>
          </div>

          <div class="hidden w-32 flex-shrink-0 truncate text-sm text-pim-muted lg:block">
            {{ (row.product_family ?? row.family) || '–' }}
          </div>

          <div class="w-28 flex-shrink-0">
            <div class="flex items-center gap-2">
              <div class="h-1.5 flex-1 rounded-full bg-gray-200">
                <div
                  class="h-1.5 rounded-full transition-all"
                  :class="completenessColor(row.completeness_score)"
                  :style="{ width: `${row.completeness_score ?? 0}%` }"
                />
              </div>
              <span class="text-xs text-pim-muted">{{ row.completeness_score ?? 0 }}%</span>
            </div>
          </div>

          <div class="w-24 flex-shrink-0 text-right" @click.stop>
            <button
              type="button"
              class="text-sm text-pim-muted hover:text-pim-text hover:underline"
              @click="openInDesk($event, row.name)"
            >
              Open in Desk
            </button>
          </div>
        </div>
      </div>

      <div v-if="rows.length === 0 && !loading" class="px-4 py-8 text-center text-pim-muted">
        No records found.
      </div>
    </div>

    <div class="flex items-center justify-between text-sm text-pim-muted">
      <span>Showing {{ rows.length }} records</span>
      <div class="flex gap-2">
        <button
          type="button"
          class="rounded border border-pim-border px-3 py-1 hover:bg-gray-50 disabled:opacity-50"
          :disabled="page <= 1"
          @click="page--; loadList()"
        >
          Previous
        </button>
        <span>Page {{ page }}</span>
        <button
          type="button"
          class="rounded border border-pim-border px-3 py-1 hover:bg-gray-50 disabled:opacity-50"
          :disabled="rows.length < pageSize"
          @click="page++; loadList()"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
