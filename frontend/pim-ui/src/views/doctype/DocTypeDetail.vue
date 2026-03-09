<script setup lang="ts">
/**
 * DocTypeDetail – Clean Flowbite form for any PIM DocType using Desk meta.
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
const isNew = computed(() => docName.value === 'new')

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
      currentSection = { label: (f.label || '').trim(), fields: [], tables: [] }
      currentTab.sections.push(currentSection)
    } else if (f.fieldtype === 'Column Break') {
      if (currentSection) currentSection.columnBreakIndex = currentSection.fields.length
    } else if (f.fieldtype === 'Table' || f.fieldtype === 'Table MultiSelect') {
      if (!currentTab) {
        currentTab = { label: 'Details', sections: [] }
        currentSection = { label: '', fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      if (!currentSection) {
        currentSection = { label: (f.label || '').trim(), fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      currentSection.tables.push(f)
    } else {
      if (!currentTab) {
        currentTab = { label: 'Details', sections: [] }
        currentSection = { label: '', fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      if (!currentSection) {
        currentSection = { label: '', fields: [], tables: [] }
        currentTab.sections.push(currentSection)
      }
      currentSection.fields.push(f)
    }
  }
  if (currentTab) tabs.push(currentTab)
  const tableFallback = meta.value?.fields?.filter((x) => ['Table', 'Table MultiSelect'].includes(x.fieldtype)) ?? []
  return tabs.length ? tabs : [{ label: 'Details', sections: [{ label: '', fields: mainFieldsFallback.value, tables: tableFallback }] }]
})

const mainFieldsFallback = computed(() => meta.value?.fields?.filter((f) => !['Table', 'Table MultiSelect', 'Tab Break', 'Section Break', 'Column Break'].includes(f.fieldtype)) ?? [])

const activeTabIndex = ref(0)

// Link field dropdown
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

/** Check if a section has any visible content */
function sectionHasContent(section: FormSection): boolean {
  return section.fields.length > 0 || section.tables.length > 0
}

async function load(): Promise<void> {
  if (!doctype.value || !docName.value) return
  loading.value = true
  error.value = null
  try {
    if (isNew.value) {
      // New document mode: only load meta, form starts empty
      const metaRes = await api.callMethod<DoctypeMeta>('frappe_pim.pim.api.doctype_meta.get_doctype_meta', { doctype: doctype.value })
      meta.value = metaRes
      doc.value = null
      // Build empty form from meta fields with defaults
      const empty: Record<string, unknown> = {}
      for (const f of metaRes.fields ?? []) {
        if (['Section Break', 'Column Break', 'Tab Break', 'HTML'].includes(f.fieldtype)) continue
        empty[f.fieldname] = f.fieldtype === 'Check' ? 0 : ''
      }
      form.value = empty
      isDirty.value = false
    } else {
      const [metaRes, docData] = await Promise.all([
        api.callMethod<DoctypeMeta>('frappe_pim.pim.api.doctype_meta.get_doctype_meta', { doctype: doctype.value }),
        api.getDoc<Record<string, unknown>>(doctype.value, docName.value),
      ])
      meta.value = metaRes
      doc.value = docData
      form.value = JSON.parse(JSON.stringify(docData))
      isDirty.value = false
    }
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
  if (!doctype.value || !meta.value) return
  saveLoading.value = true
  error.value = null
  try {
    const payload: Record<string, unknown> = { doctype: doctype.value }
    for (const [k, v] of Object.entries(form.value)) {
      if (SYSTEM_KEYS.has(k)) continue
      if (meta.value.child_tables?.[k] && Array.isArray(v)) {
        const childDoctype = meta.value.child_tables[k].doctype
        payload[k] = (v as Record<string, unknown>[]).map((row) => ({ ...row, doctype: row.doctype ?? childDoctype }))
      } else {
        payload[k] = v
      }
    }

    if (isNew.value) {
      // Create new document
      const created = await api.createDoc<Record<string, unknown>>(doctype.value, payload)
      doc.value = created
      isDirty.value = false
      saveSuccess.value = true
      setTimeout(() => { saveSuccess.value = false }, 3000)
      // Navigate to the saved document
      router.replace(`/doc/${encodeURIComponent(doctype.value)}/${encodeURIComponent(created.name as string)}`)
    } else {
      await api.updateDoc(doctype.value, docName.value, payload)
      doc.value = { ...doc.value, ...payload } as Record<string, unknown>
      isDirty.value = false
      saveSuccess.value = true
      setTimeout(() => { saveSuccess.value = false }, 3000)
    }
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
  <div class="mx-auto max-w-5xl space-y-6">
    <!-- Page Header -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <button
          type="button"
          class="inline-flex items-center rounded-lg border border-gray-300 bg-white p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-900 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
          @click="goBack"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ doctype }}</p>
          <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
            {{ isNew ? 'New ' + doctype : docName }}
          </h1>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <!-- Save flash -->
        <Transition name="fade">
          <span v-if="saveSuccess" class="inline-flex items-center gap-1 text-sm font-medium text-green-600 dark:text-green-400">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Saved
          </span>
        </Transition>

        <!-- Dirty indicator -->
        <span v-if="isDirty" class="rounded-full bg-amber-100 px-2.5 py-0.5 text-xs font-medium text-amber-800 dark:bg-amber-900 dark:text-amber-300">
          Unsaved
        </span>

        <!-- Open in Desk (only for existing docs) -->
        <button
          v-if="!isNew"
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
          @click="openInDesk"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          Desk
        </button>

        <!-- Delete (only for existing docs) -->
        <button
          v-if="!isNew"
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg border border-red-300 bg-white px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 dark:border-red-800 dark:bg-gray-800 dark:text-red-400 dark:hover:bg-red-900/20"
          @click="confirmDelete"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Delete
        </button>

        <!-- Save -->
        <button
          type="button"
          class="inline-flex items-center gap-2 rounded-lg bg-primary-700 px-5 py-2.5 text-sm font-medium text-white hover:bg-primary-800 focus:outline-none focus:ring-4 focus:ring-primary-300 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
          :disabled="saveLoading || (!isNew && !isDirty)"
          @click="save"
        >
          <svg v-if="saveLoading" class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          Save
        </button>
      </div>
    </div>

    <!-- Error Banner -->
    <div v-if="error" class="flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20" role="alert">
      <svg class="h-5 w-5 shrink-0 text-red-500 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-sm font-medium text-red-800 dark:text-red-300">{{ error }}</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-16">
      <div class="flex flex-col items-center gap-3">
        <div class="h-8 w-8 animate-spin rounded-full border-4 border-primary-600 border-t-transparent" />
        <span class="text-sm text-gray-500 dark:text-gray-400">Loading document...</span>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else-if="meta && (doc || isNew)" class="space-y-6">
      <!-- Tab Navigation -->
      <div v-if="formTabs.length > 1" class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex gap-1">
          <button
            v-for="(tab, ti) in formTabs"
            :key="ti"
            type="button"
            class="rounded-t-lg px-4 py-3 text-sm font-medium transition-colors"
            :class="
              activeTabIndex === ti
                ? 'border-b-2 border-primary-600 text-primary-600 dark:text-primary-500'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            "
            @click="activeTabIndex = ti"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <!-- Sections -->
      <template v-for="(section, si) in (formTabs[activeTabIndex]?.sections ?? [])" :key="si">
        <div v-if="sectionHasContent(section)" class="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
          <!-- Section Header -->
          <div v-if="section.label" class="border-b border-gray-200 px-6 py-4 dark:border-gray-700">
            <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ section.label }}</h3>
          </div>

          <!-- Section Fields -->
          <div v-if="section.fields.length > 0" class="p-6">
            <div :class="section.columnBreakIndex != null ? 'grid grid-cols-1 gap-5 md:grid-cols-2' : 'grid grid-cols-1 gap-5 sm:grid-cols-2'">
              <template v-for="f in section.fields" :key="f.fieldname">
                <!-- Read only -->
                <div v-if="f.read_only" class="sm:col-span-1">
                  <label class="mb-2 block text-sm font-medium text-gray-500 dark:text-gray-400">{{ f.label }}</label>
                  <p class="text-sm text-gray-900 dark:text-white">{{ form[f.fieldname] ?? '–' }}</p>
                </div>

                <!-- Check -->
                <div v-else-if="f.fieldtype === 'Check'" class="flex items-center gap-3 sm:col-span-2">
                  <input
                    :id="'f-' + f.fieldname"
                    type="checkbox"
                    :checked="form[f.fieldname] === true || form[f.fieldname] === 1"
                    class="h-4 w-4 rounded border-gray-300 bg-gray-100 text-primary-600 focus:ring-2 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 dark:focus:ring-primary-600"
                    @change="setFormValue(f.fieldname, ($event.target as HTMLInputElement).checked)"
                  >
                  <label :for="'f-' + f.fieldname" class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ f.label }}
                    <span v-if="f.reqd" class="text-red-500">*</span>
                  </label>
                </div>

                <!-- Text / Small Text / Text Editor -->
                <div v-else-if="['Text', 'Small Text', 'Text Editor'].includes(f.fieldtype)" class="sm:col-span-2">
                  <label :for="'f-' + f.fieldname" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">
                    {{ f.label }}
                    <span v-if="f.reqd" class="text-red-500">*</span>
                  </label>
                  <textarea
                    :id="'f-' + f.fieldname"
                    :value="form[f.fieldname]"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-primary-500 dark:focus:ring-primary-500"
                    rows="4"
                    :placeholder="f.description || `Enter ${f.label.toLowerCase()}`"
                    @input="setFormValue(f.fieldname, ($event.target as HTMLTextAreaElement).value)"
                  />
                </div>

                <!-- Select -->
                <div v-else-if="f.fieldtype === 'Select'">
                  <label :for="'f-' + f.fieldname" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">
                    {{ f.label }}
                    <span v-if="f.reqd" class="text-red-500">*</span>
                  </label>
                  <select
                    :id="'f-' + f.fieldname"
                    :value="form[f.fieldname]"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-primary-500 dark:focus:ring-primary-500"
                    @change="setFormValue(f.fieldname, ($event.target as HTMLSelectElement).value)"
                  >
                    <option value="">Select {{ f.label.toLowerCase() }}</option>
                    <option v-for="opt in selectOptions(f)" :key="opt" :value="opt">{{ opt }}</option>
                  </select>
                </div>

                <!-- Date -->
                <div v-else-if="f.fieldtype === 'Date'">
                  <label :for="'f-' + f.fieldname" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">
                    {{ f.label }}
                    <span v-if="f.reqd" class="text-red-500">*</span>
                  </label>
                  <input
                    :id="'f-' + f.fieldname"
                    :value="typeof form[f.fieldname] === 'string' ? (form[f.fieldname] as string).slice(0, 10) : ''"
                    type="date"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-primary-500 dark:focus:ring-primary-500"
                    @input="setFormValue(f.fieldname, ($event.target as HTMLInputElement).value)"
                  >
                </div>

                <!-- Datetime -->
                <div v-else-if="f.fieldtype === 'Datetime'">
                  <label :for="'f-' + f.fieldname" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">
                    {{ f.label }}
                    <span v-if="f.reqd" class="text-red-500">*</span>
                  </label>
                  <input
                    :id="'f-' + f.fieldname"
                    :value="datetimeLocalValue(form[f.fieldname])"
                    type="datetime-local"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-primary-500 dark:focus:ring-primary-500"
                    @input="setFormValue(f.fieldname, ($event.target as HTMLInputElement).value)"
                  >
                </div>

                <!-- Link (searchable dropdown) -->
                <div v-else-if="f.fieldtype === 'Link' && f.options" class="relative">
                  <label :for="'f-' + f.fieldname" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">
                    {{ f.label }}
                    <span v-if="f.reqd" class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <input
                      :id="'f-' + f.fieldname"
                      type="text"
                      :value="isLinkDropdownOpen(f.fieldname) ? getLinkSearchQuery(f.fieldname) : (form[f.fieldname] ?? '')"
                      class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 pe-10 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-primary-500 dark:focus:ring-primary-500"
                      :placeholder="`Search ${f.label.toLowerCase()}...`"
                      autocomplete="off"
                      @focus="openLinkDropdown(f)"
                      @input="setLinkSearchQuery(f.fieldname, ($event.target as HTMLInputElement).value)"
                      @blur="setTimeout(closeLinkDropdown, 180)"
                    />
                    <!-- Link icon -->
                    <div class="pointer-events-none absolute inset-y-0 end-0 flex items-center pe-3">
                      <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                  </div>

                  <!-- Dropdown -->
                  <div
                    v-if="isLinkDropdownOpen(f.fieldname)"
                    class="absolute left-0 right-0 top-full z-20 mt-1 max-h-56 overflow-auto rounded-lg border border-gray-200 bg-white shadow-lg dark:border-gray-600 dark:bg-gray-700"
                  >
                    <!-- Loading -->
                    <div v-if="linkSearchLoading[f.fieldname]" class="flex items-center justify-center px-4 py-6">
                      <div class="h-5 w-5 animate-spin rounded-full border-2 border-primary-600 border-t-transparent" />
                    </div>

                    <template v-else>
                      <!-- Options -->
                      <ul class="py-1">
                        <li v-for="opt in getLinkOptions(f.fieldname)" :key="opt">
                          <button
                            type="button"
                            class="block w-full px-4 py-2 text-left text-sm text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                            @mousedown.prevent="selectLinkOption(f.fieldname, opt)"
                          >
                            {{ opt }}
                          </button>
                        </li>
                        <li v-if="getLinkOptions(f.fieldname).length === 0" class="px-4 py-3 text-center text-sm text-gray-500 dark:text-gray-400">
                          No results found
                        </li>
                      </ul>

                      <!-- Actions -->
                      <div class="border-t border-gray-200 p-2 dark:border-gray-600">
                        <button
                          type="button"
                          class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-primary-600 hover:bg-gray-100 dark:text-primary-400 dark:hover:bg-gray-600"
                          @mousedown.prevent="openCreateNewDoc(f.options)"
                        >
                          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                          </svg>
                          Create new {{ f.options }}
                        </button>
                      </div>
                    </template>
                  </div>
                </div>

                <!-- Data / Int / Float / default -->
                <div v-else>
                  <label :for="'f-' + f.fieldname" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">
                    {{ f.label }}
                    <span v-if="f.reqd" class="text-red-500">*</span>
                  </label>
                  <input
                    :id="'f-' + f.fieldname"
                    :value="form[f.fieldname]"
                    :type="f.fieldtype === 'Int' ? 'number' : f.fieldtype === 'Float' || f.fieldtype === 'Currency' || f.fieldtype === 'Percent' ? 'number' : 'text'"
                    :step="f.fieldtype === 'Float' || f.fieldtype === 'Currency' || f.fieldtype === 'Percent' ? '0.01' : undefined"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-primary-500 dark:focus:ring-primary-500"
                    :placeholder="f.description || `Enter ${f.label.toLowerCase()}`"
                    @input="setFormValue(f.fieldname, ($event.target as HTMLInputElement).value)"
                  >
                </div>
              </template>
            </div>
          </div>

          <!-- Child Tables in this section -->
          <template v-for="tf in section.tables" :key="tf.fieldname">
            <div class="border-t border-gray-200 dark:border-gray-700">
              <div class="flex items-center justify-between px-6 py-4">
                <h4 class="text-sm font-semibold text-gray-900 dark:text-white">{{ tf.label }}</h4>
                <button
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                  @click="addChildRow(tf.fieldname)"
                >
                  <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Add Row
                </button>
              </div>

              <!-- Table -->
              <div class="overflow-x-auto">
                <table v-if="getChildRows(tf.fieldname).length > 0" class="w-full text-left text-sm text-gray-500 dark:text-gray-400">
                  <thead class="bg-gray-50 text-xs uppercase text-gray-700 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                      <th class="w-10 px-4 py-3 text-center">#</th>
                      <th v-for="cf in (meta?.child_tables?.[tf.fieldname]?.fields ?? [])" :key="cf.fieldname" class="px-4 py-3">
                        {{ cf.label }}
                      </th>
                      <th class="w-16 px-4 py-3 text-center">
                        <span class="sr-only">Actions</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                    <tr v-for="(row, ri) in getChildRows(tf.fieldname)" :key="ri" class="bg-white dark:bg-gray-800">
                      <td class="px-4 py-2.5 text-center text-xs text-gray-400">{{ ri + 1 }}</td>
                      <td v-for="cf in (meta?.child_tables?.[tf.fieldname]?.fields ?? [])" :key="cf.fieldname" class="px-4 py-2">
                        <input
                          v-if="cf.fieldtype === 'Check'"
                          type="checkbox"
                          :checked="row[cf.fieldname] === true || row[cf.fieldname] === 1"
                          class="h-4 w-4 rounded border-gray-300 bg-gray-100 text-primary-600 focus:ring-2 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
                          @change="setChildCell(tf.fieldname, ri, cf.fieldname, ($event.target as HTMLInputElement).checked)"
                        >
                        <select
                          v-else-if="cf.fieldtype === 'Select'"
                          :value="row[cf.fieldname]"
                          class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-2.5 py-1.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                          @change="setChildCell(tf.fieldname, ri, cf.fieldname, ($event.target as HTMLSelectElement).value)"
                        >
                          <option value="">–</option>
                          <option v-for="opt in selectOptions(cf)" :key="opt" :value="opt">{{ opt }}</option>
                        </select>
                        <input
                          v-else
                          :value="row[cf.fieldname]"
                          type="text"
                          class="block w-full rounded-lg border border-gray-300 bg-gray-50 px-2.5 py-1.5 text-sm text-gray-900 focus:border-primary-500 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                          @input="setChildCell(tf.fieldname, ri, cf.fieldname, ($event.target as HTMLInputElement).value)"
                        >
                      </td>
                      <td class="px-4 py-2 text-center">
                        <button
                          type="button"
                          class="rounded-lg p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-900/20 dark:hover:text-red-400"
                          title="Remove row"
                          @click="removeChildRow(tf.fieldname, ri)"
                        >
                          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>

                <!-- Empty table state -->
                <div v-else class="px-6 py-8 text-center">
                  <svg class="mx-auto h-8 w-8 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                  <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">No rows yet</p>
                </div>
              </div>
            </div>
          </template>
        </div>
      </template>
    </div>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50"
        @click.self="showDeleteConfirm = false"
      >
        <div class="mx-4 w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">
              <svg class="h-5 w-5 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Document</h3>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Are you sure you want to delete <span class="font-medium text-gray-900 dark:text-white">{{ docName }}</span>? This action cannot be undone.
              </p>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              @click="showDeleteConfirm = false"
            >
              Cancel
            </button>
            <button
              type="button"
              class="rounded-lg bg-red-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-4 focus:ring-red-300 disabled:opacity-50 dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-800"
              :disabled="saveLoading"
              @click="deleteDoc"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
