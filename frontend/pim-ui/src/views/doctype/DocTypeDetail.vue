<script setup lang="ts">
/**
 * DocTypeDetail – form for any PIM DocType using Desk meta.
 * Fetches get_doctype_meta and doc; renders all fields (same as Frappe Desk), save/delete.
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFrappeAPI } from '@/composables/useFrappeAPI'

const LINK_DROPDOWN_LIMIT = 20

const route = useRoute()
const router = useRouter()
const api = useFrappeAPI()

const doctype = computed(() => decodeURIComponent((route.params.doctype as string) || ''))
const docName = computed(() => decodeURIComponent((route.params.name as string) || ''))

interface MetaField {
  fieldname: string
  label: string
  fieldtype: string
  options: string
  reqd: number
  read_only: number
  description?: string
}

interface ChildTableMeta {
  doctype: string
  fields: MetaField[]
}

interface DoctypeMeta {
  doctype: string
  fields: MetaField[]
  child_tables: Record<string, ChildTableMeta>
}

const meta = ref<DoctypeMeta | null>(null)
const doc = ref<Record<string, unknown> | null>(null)
const form = ref<Record<string, unknown>>({})
const loading = ref(true)
const error = ref<string | null>(null)
const saveLoading = ref(false)
const saveSuccess = ref(false)
const isDirty = ref(false)
const showDeleteConfirm = ref(false)

const SYSTEM_KEYS = new Set(['doctype', 'name', 'owner', 'creation', 'modified', 'modified_by', '__last_sync', '__unsaved', '__islocal', '__onload', '__run_link_triggers'])

/** Desk-style layout: tabs (Tab Break) -> sections (Section Break) -> fields + child tables in same section */
interface FormSection {
  label: string
  fields: MetaField[]
  tables: MetaField[]
  columnBreakIndex?: number
}
interface FormTab {
  label: string
  sections: FormSection[]
}

const formTabs = computed<FormTab[]>(() => {
  const m = meta.value
  if (!m?.fields) return []
  const tabs: FormTab[] = []
  let currentTab: FormTab | null = null
  let currentSection: FormSection | null = null
  for (const f of m.fields) {
    if (f.fieldtype === 'Tab Break') {
      if (currentTab) tabs.push(currentTab)
      currentTab = { label: (f.label || 'Tab').trim() || 'Details', sections: [] }
      currentSection = null
    } else if (f.fieldtype === 'Section Break') {
      if (!currentTab) currentTab = { label: 'Details', sections: [] }
      currentSection = { label: (f.label || 'Section').trim() || 'Details', fields: [], tables: [] }
      currentTab.sections.push(currentSection)
    } else if (f.fieldtype === 'Column Break') {
      if (currentSection) currentSection.columnBreakIndex = currentSection.fields.length
    } else if (f.fieldtype === 'Table' || f.fieldtype === 'Table MultiSelect') {
      if (!currentTab) {
        currentTab = { label: 'Details', sections: [] }
        currentSection = { label: 'Details', fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      if (!currentSection) {
        currentSection = { label: (f.label || 'Table').trim() || 'Details', fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      currentSection.tables.push(f)
    } else {
      if (!currentTab) {
        currentTab = { label: 'Details', sections: [] }
        currentSection = { label: 'Details', fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      if (!currentSection) {
        currentSection = { label: 'Details', fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      currentSection.fields.push(f)
    }
  }
  if (currentTab) tabs.push(currentTab)
  const tableFallback = meta.value?.fields?.filter((x) => ['Table', 'Table MultiSelect'].includes(x.fieldtype)) ?? []
  return tabs.length ? tabs : [{ label: 'Details', sections: [{ label: 'Details', fields: mainFieldsFallback.value, tables: tableFallback }] }]
})

const mainFieldsFallback = computed(() => meta.value?.fields?.filter((f) => !['Table', 'Table MultiSelect', 'Tab Break', 'Section Break', 'Column Break'].includes(f.fieldtype)) ?? [])

const activeTabIndex = ref(0)

// Link field dropdown (Desk-style: searchable list + Create new + Advanced search)
const linkDropdownOpen = ref<string | null>(null)
const linkOptions = ref<Record<string, string[]>>({})
const linkSearchLoading = ref<Record<string, boolean>>({})
const linkSearchQuery = ref<Record<string, string>>({})
let linkSearchTimer: ReturnType<typeof setTimeout> | null = null

type LinkOptionRow = { name: string }

async function fetchLinkOptions(fieldname: string, linkedDoctype: string, query: string): Promise<void> {
  if (!linkedDoctype?.trim()) return
  linkSearchLoading.value = { ...linkSearchLoading.value, [fieldname]: true }
  try {
    const search = query?.trim()
    const filters = search ? ([['name', 'like', '%' + search + '%']] as [string, string, string][]) : undefined
    const list = await api.getList<LinkOptionRow>({
      doctype: linkedDoctype,
      fields: ['name'],
      limit_page_length: LINK_DROPDOWN_LIMIT,
      order_by: 'name asc',
      filters,
    })
    linkOptions.value = { ...linkOptions.value, [fieldname]: list.map((r) => r.name) }
  } catch {
    linkOptions.value = { ...linkOptions.value, [fieldname]: [] }
  } finally {
    linkSearchLoading.value = { ...linkSearchLoading.value, [fieldname]: false }
  }
}

function openLinkDropdown(f: MetaField): void {
  if (f.fieldtype !== 'Link' || !f.options?.trim()) return
  linkDropdownOpen.value = f.fieldname
  const current = (form.value[f.fieldname] as string) ?? ''
  linkSearchQuery.value = { ...linkSearchQuery.value, [f.fieldname]: current }
  fetchLinkOptions(f.fieldname, f.options.trim(), current)
}

function getLinkSearchQuery(fieldname: string): string {
  return linkSearchQuery.value[fieldname] ?? (form.value[fieldname] as string) ?? ''
}

function setLinkSearchQuery(fieldname: string, value: string): void {
  linkSearchQuery.value = { ...linkSearchQuery.value, [fieldname]: value }
  if (linkSearchTimer) clearTimeout(linkSearchTimer)
  linkSearchTimer = setTimeout(() => {
    const f = meta.value?.fields?.find((x) => x.fieldname === fieldname)
    if (f?.fieldtype === 'Link' && f.options?.trim()) fetchLinkOptions(fieldname, f.options.trim(), value)
    linkSearchTimer = null
  }, 250)
}

function closeLinkDropdown(): void {
  linkDropdownOpen.value = null
}

function selectLinkOption(fieldname: string, value: string): void {
  setFormValue(fieldname, value)
  linkSearchQuery.value = { ...linkSearchQuery.value, [fieldname]: value }
  closeLinkDropdown()
}

function openCreateNewDoc(linkedDoctype: string): void {
  const slug = linkedDoctype.replace(/\s+/g, '-').toLowerCase()
  window.open(`http://localhost:8000/app/${slug}/new`, '_blank')
  closeLinkDropdown()
}

function openAdvancedSearch(linkedDoctype: string): void {
  const slug = linkedDoctype.replace(/\s+/g, '-').toLowerCase()
  window.open(`http://localhost:8000/app/${slug}`, '_blank')
  closeLinkDropdown()
}

function getLinkOptions(fieldname: string): string[] {
  return linkOptions.value[fieldname] ?? []
}

function isLinkDropdownOpen(fieldname: string): boolean {
  return linkDropdownOpen.value === fieldname
}

function listPath(): string {
  return `/list/${encodeURIComponent(doctype.value)}`
}

function openInDesk(): void {
  const baseUrl = 'http://localhost:8000'
  const slug = doctype.value.replace(/\s+/g, '-').toLowerCase()
  window.open(`${baseUrl}/app/${slug}/${encodeURIComponent(docName.value)}`, '_blank')
}

function setFormValue(key: string, value: unknown): void {
  form.value[key] = value
  isDirty.value = true
}

function getChildRows(fieldname: string): Record<string, unknown>[] {
  const v = form.value[fieldname]
  if (Array.isArray(v)) return v as Record<string, unknown>[]
  return []
}

function setChildRow(fieldname: string, index: number, row: Record<string, unknown>): void {
  const arr = [...getChildRows(fieldname)]
  arr[index] = row
  form.value[fieldname] = arr
  isDirty.value = true
}

function addChildRow(fieldname: string): void {
  const childMeta = meta.value?.child_tables?.[fieldname]
  if (!childMeta) return
  const row: Record<string, unknown> = { doctype: childMeta.doctype }
  for (const f of childMeta.fields) row[f.fieldname] = f.fieldtype === 'Check' ? 0 : ''
  const arr = [...getChildRows(fieldname), row]
  form.value[fieldname] = arr
  isDirty.value = true
}

function removeChildRow(fieldname: string, index: number): void {
  const arr = getChildRows(fieldname).filter((_, i) => i !== index)
  form.value[fieldname] = arr
  isDirty.value = true
}

function setChildCell(fieldname: string, rowIndex: number, col: string, value: unknown): void {
  const arr = getChildRows(fieldname)
  const row = { ...arr[rowIndex], [col]: value }
  setChildRow(fieldname, rowIndex, row)
}

function selectOptions(f: MetaField): string[] {
  if (f.fieldtype !== 'Select' || !f.options) return []
  return f.options.split('\n').map((s) => s.trim()).filter(Boolean)
}

function datetimeLocalValue(val: unknown): string {
  if (typeof val !== 'string') return ''
  const d = new Date(val)
  if (Number.isNaN(d.getTime())) return ''
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

async function load(): Promise<void> {
  if (!doctype.value || !docName.value) return
  loading.value = true
  error.value = null
  try {
    const [metaRes, docData] = await Promise.all([
      api.callMethod<DoctypeMeta>('frappe_pim.pim.api.doctype_meta.get_doctype_meta', { doctype: doctype.value }),
      api.getDoc<Record<string, unknown>>(doctype.value, docName.value),
    ])
    meta.value = metaRes
    doc.value = docData
    form.value = JSON.parse(JSON.stringify(docData))
    isDirty.value = false
  } catch (e: unknown) {
    const msg = e && typeof e === 'object' && 'message' in e ? String((e as { message: string }).message) : 'Failed to load'
    error.value = msg
    meta.value = null
    doc.value = null
    form.value = {}
  } finally {
    loading.value = false
  }
}

async function save(): Promise<void> {
  if (!doctype.value || !docName.value || !meta.value) return
  saveLoading.value = true
  error.value = null
  try {
    const payload: Record<string, unknown> = {}
    for (const [k, v] of Object.entries(form.value)) {
      if (SYSTEM_KEYS.has(k)) continue
      if (meta.value.child_tables?.[k] && Array.isArray(v)) {
        const childDoctype = meta.value.child_tables[k].doctype
        payload[k] = (v as Record<string, unknown>[]).map((row) => ({ ...row, doctype: row.doctype ?? childDoctype }))
      } else {
        payload[k] = v
      }
    }
    await api.updateDoc(doctype.value, docName.value, payload)
    doc.value = { ...doc.value, ...payload } as Record<string, unknown>
    isDirty.value = false
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 3000)
  } catch (e: unknown) {
    error.value = e && typeof e === 'object' && 'message' in e ? String((e as { message: string }).message) : 'Save failed'
  } finally {
    saveLoading.value = false
  }
}

function confirmDelete(): void { showDeleteConfirm.value = true }

async function deleteDoc(): Promise<void> {
  if (!doctype.value || !docName.value) return
  saveLoading.value = true
  error.value = null
  try {
    await api.deleteDoc(doctype.value, docName.value)
    router.push(listPath())
  } catch (e: unknown) {
    error.value = e && typeof e === 'object' && 'message' in e ? String((e as { message: string }).message) : 'Delete failed'
  } finally {
    saveLoading.value = false
    showDeleteConfirm.value = false
  }
}

function goBack(): void {
  if (isDirty.value && !confirm('Unsaved changes. Leave anyway?')) return
  router.push(listPath())
}

onMounted(() => load())
watch([doctype, docName], () => {
  activeTabIndex.value = 0
  load()
})
</script>

<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <button type="button" class="rounded-md border border-pim-border bg-white px-3 py-2 text-sm text-pim-muted hover:bg-gray-50 hover:text-pim-text" @click="goBack">
          ← Back to list
        </button>
        <div>
          <h1 class="text-2xl font-bold text-pim-text">{{ doctype }}: {{ docName }}</h1>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <span v-if="saveSuccess" class="text-sm font-medium text-green-600">Saved</span>
        <span v-if="isDirty" class="text-xs text-amber-600">Unsaved changes</span>
        <button type="button" class="rounded-md border border-pim-border bg-white px-3 py-2 text-sm text-pim-muted hover:bg-gray-50" @click="openInDesk">Open in Desk</button>
        <button type="button" class="text-red-600 hover:text-red-700" @click="confirmDelete">Delete</button>
        <button type="button" class="inline-flex items-center gap-2 rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50" :disabled="saveLoading || !isDirty" @click="save">
          <svg v-if="saveLoading" class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" /><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" /></svg>
          Save
        </button>
      </div>
    </div>

    <div v-if="error" class="rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-800">{{ error }}</div>
    <div v-if="loading" class="flex justify-center py-12 text-pim-muted">Loading...</div>

    <div v-else-if="meta && doc" class="space-y-6">
      <!-- Tabs (Desk-style: Details, Basic Info, Pricing & Stock, etc.) -->
      <div class="rounded-lg border border-pim-border bg-white shadow">
        <div class="border-b border-pim-border px-4">
          <nav class="-mb-px flex gap-6 overflow-x-auto">
            <button
              v-for="(tab, ti) in formTabs"
              :key="ti"
              type="button"
              class="whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium transition-colors"
              :class="activeTabIndex === ti ? 'border-primary-600 text-primary-600' : 'border-transparent text-pim-muted hover:border-gray-300 hover:text-pim-text'"
              @click="activeTabIndex = ti"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>
        <!-- Active tab content: sections with titles -->
        <div v-for="(section, si) in (formTabs[activeTabIndex]?.sections ?? [])" :key="si" class="border-b border-pim-border last:border-b-0">
          <h3 class="border-b border-gray-100 bg-gray-50 px-6 py-3 text-sm font-semibold uppercase tracking-wider text-pim-muted">
            {{ section.label }}
          </h3>
          <div class="p-6" :class="section.columnBreakIndex != null ? 'grid grid-cols-1 gap-4 md:grid-cols-2' : 'grid grid-cols-1 gap-4 sm:grid-cols-2'">
            <template v-for="f in section.fields" :key="f.fieldname">
              <!-- Read only -->
              <div v-if="f.read_only" class="sm:col-span-2">
                <label class="mb-1 block text-sm font-medium text-pim-muted">{{ f.label }}</label>
                <p class="text-sm text-pim-text">{{ form[f.fieldname] ?? '–' }}</p>
              </div>
              <!-- Check -->
              <div v-else-if="f.fieldtype === 'Check'" class="flex items-center gap-2 sm:col-span-2">
                <input :id="'f-' + f.fieldname" type="checkbox" :checked="form[f.fieldname] === true || form[f.fieldname] === 1" class="h-4 w-4 rounded border-pim-border text-primary-600" @change="setFormValue(f.fieldname, ($event.target as HTMLInputElement).checked)">
                <label :for="'f-' + f.fieldname" class="text-sm font-medium text-pim-text">{{ f.label }} <span v-if="f.reqd" class="text-red-500">*</span></label>
              </div>
              <!-- Text / Small Text / Text Editor -->
              <div v-else-if="['Text', 'Small Text', 'Text Editor'].includes(f.fieldtype)" class="sm:col-span-2">
                <label class="mb-1 block text-sm font-medium text-pim-text">{{ f.label }} <span v-if="f.reqd" class="text-red-500">*</span></label>
                <textarea :value="form[f.fieldname]" class="w-full rounded-md border border-pim-border px-3 py-2 text-sm" rows="4" @input="setFormValue(f.fieldname, ($event.target as HTMLTextAreaElement).value)" />
              </div>
              <!-- Select -->
              <div v-else-if="f.fieldtype === 'Select'">
                <label class="mb-1 block text-sm font-medium text-pim-text">{{ f.label }} <span v-if="f.reqd" class="text-red-500">*</span></label>
                <select :value="form[f.fieldname]" class="w-full rounded-md border border-pim-border px-3 py-2 text-sm" @change="setFormValue(f.fieldname, ($event.target as HTMLSelectElement).value)">
                  <option value="">–</option>
                  <option v-for="opt in selectOptions(f)" :key="opt" :value="opt">{{ opt }}</option>
                </select>
              </div>
              <!-- Date -->
              <div v-else-if="f.fieldtype === 'Date'">
                <label class="mb-1 block text-sm font-medium text-pim-text">{{ f.label }} <span v-if="f.reqd" class="text-red-500">*</span></label>
                <input :value="typeof form[f.fieldname] === 'string' ? (form[f.fieldname] as string).slice(0, 10) : ''" type="date" class="w-full rounded-md border border-pim-border px-3 py-2 text-sm" @input="setFormValue(f.fieldname, ($event.target as HTMLInputElement).value)">
              </div>
              <!-- Datetime -->
              <div v-else-if="f.fieldtype === 'Datetime'">
                <label class="mb-1 block text-sm font-medium text-pim-text">{{ f.label }} <span v-if="f.reqd" class="text-red-500">*</span></label>
                <input :value="datetimeLocalValue(form[f.fieldname])" type="datetime-local" class="w-full rounded-md border border-pim-border px-3 py-2 text-sm" @input="setFormValue(f.fieldname, ($event.target as HTMLInputElement).value)">
              </div>
              <!-- Link (searchable dropdown like Frappe Desk: list + Create new + Advanced search) -->
              <div v-else-if="f.fieldtype === 'Link' && f.options" class="relative">
                <label class="mb-1 block text-sm font-medium text-pim-text">{{ f.label }} <span v-if="f.reqd" class="text-red-500">*</span></label>
                <input
                  type="text"
                  :value="isLinkDropdownOpen(f.fieldname) ? getLinkSearchQuery(f.fieldname) : (form[f.fieldname] ?? '')"
                  class="w-full rounded-md border border-pim-border px-3 py-2 text-sm"
                  placeholder="Search or select..."
                  @focus="openLinkDropdown(f)"
                  @input="setLinkSearchQuery(f.fieldname, ($event.target as HTMLInputElement).value)"
                  @blur="setTimeout(closeLinkDropdown, 180)"
                />
                <div
                  v-if="isLinkDropdownOpen(f.fieldname)"
                  class="absolute left-0 right-0 top-full z-20 mt-1 max-h-60 overflow-auto rounded-md border border-pim-border bg-white py-1 shadow-lg"
                >
                  <div v-if="linkSearchLoading[f.fieldname]" class="px-3 py-4 text-center text-sm text-pim-muted">Loading...</div>
                  <template v-else>
                    <button
                      v-for="opt in getLinkOptions(f.fieldname)"
                      :key="opt"
                      type="button"
                      class="block w-full px-3 py-2 text-left text-sm text-pim-text hover:bg-gray-100"
                      @mousedown.prevent="selectLinkOption(f.fieldname, opt)"
                    >
                      {{ opt }}
                    </button>
                    <div class="border-t border-pim-border">
                      <button type="button" class="block w-full px-3 py-2 text-left text-sm text-primary-600 hover:bg-gray-50" @mousedown.prevent="openCreateNewDoc(f.options)">
                        + Create a new {{ f.options }}
                      </button>
                      <button type="button" class="block w-full px-3 py-2 text-left text-sm text-pim-muted hover:bg-gray-50" @mousedown.prevent="openAdvancedSearch(f.options)">
                        Q Advanced search
                      </button>
                    </div>
                  </template>
                </div>
              </div>
              <!-- Data / else -->
              <div v-else>
                <label class="mb-1 block text-sm font-medium text-pim-text">{{ f.label }} <span v-if="f.reqd" class="text-red-500">*</span></label>
                <input :value="form[f.fieldname]" type="text" class="w-full rounded-md border border-pim-border px-3 py-2 text-sm" @input="setFormValue(f.fieldname, ($event.target as HTMLInputElement).value)">
              </div>
            </template>
          </div>
          <!-- Child tables belonging to this section (only in current tab) -->
          <div v-for="tf in section.tables" :key="tf.fieldname" class="border-t border-gray-100 px-6 py-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-sm font-semibold text-pim-text">{{ tf.label }}</h4>
              <button type="button" class="rounded-md bg-primary-600 px-3 py-1.5 text-sm text-white hover:bg-primary-700" @click="addChildRow(tf.fieldname)">+ Add row</button>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-pim-border text-sm">
                <thead class="bg-gray-50">
                  <tr>
                    <th v-for="cf in (meta?.child_tables?.[tf.fieldname]?.fields ?? [])" :key="cf.fieldname" class="px-3 py-2 text-left font-medium text-pim-muted">{{ cf.label }}</th>
                    <th class="w-16 px-3 py-2 text-right font-medium text-pim-muted">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-pim-border bg-white">
                  <tr v-for="(row, ri) in getChildRows(tf.fieldname)" :key="ri">
                    <td v-for="cf in (meta?.child_tables?.[tf.fieldname]?.fields ?? [])" :key="cf.fieldname" class="px-3 py-2">
                      <input v-if="cf.fieldtype === 'Check'" type="checkbox" :checked="row[cf.fieldname] === true || row[cf.fieldname] === 1" class="rounded border-pim-border" @change="setChildCell(tf.fieldname, ri, cf.fieldname, ($event.target as HTMLInputElement).checked)">
                      <input v-else :value="row[cf.fieldname]" type="text" class="w-full rounded border border-pim-border px-2 py-1 text-sm" @input="setChildCell(tf.fieldname, ri, cf.fieldname, ($event.target as HTMLInputElement).value)">
                    </td>
                    <td class="px-3 py-2 text-right">
                      <button type="button" class="text-red-600 hover:underline" @click="removeChildRow(tf.fieldname, ri)">Remove</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p v-if="getChildRows(tf.fieldname).length === 0" class="py-4 text-center text-pim-muted text-sm">No rows. Click "+ Add row" to add.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete confirm -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="showDeleteConfirm = false">
      <div class="w-full max-w-sm rounded-lg bg-white p-6 shadow">
        <p class="text-pim-text">Delete this document? This cannot be undone.</p>
        <div class="mt-4 flex justify-end gap-2">
          <button type="button" class="rounded-md border border-pim-border px-4 py-2 text-sm hover:bg-gray-50" @click="showDeleteConfirm = false">Cancel</button>
          <button type="button" class="rounded-md bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700 disabled:opacity-50" :disabled="saveLoading" @click="deleteDoc">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>
