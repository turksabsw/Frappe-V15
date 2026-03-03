<script setup lang="ts">
/**
 * ProductDetail.vue - Product detail/edit view.
 *
 * Features:
 * - Tab navigation: General, Attributes, Variants, Media
 * - Form fields for core product information
 * - EAV attribute value editor with type-aware inputs
 * - Variant management integration (VariantManager component)
 * - Media gallery with upload/sort/delete
 * - Completeness score sidebar
 * - ERPNext sync status
 * - Create mode for new products
 * - Save/delete with confirmation
 */

import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useProductStore } from '@/stores/product'
import VariantManager from './VariantManager.vue'
import type {
  ProductMaster,
  ProductStatus,
  ProductAttributeValue,
  ProductMedia,
} from '@/types'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const store = useProductStore()

// =========================================================================
// Props & Route Params
// =========================================================================

const props = defineProps<{
  id: string
}>()

const isNewProduct = computed(() => props.id === 'new')

// =========================================================================
// Local State
// =========================================================================

/** Active tab */
const activeTab = ref<'general' | 'attributes' | 'variants' | 'media'>('general')

/** Form data (local copy for editing) */
const form = ref<Partial<ProductMaster>>({
  product_name: '',
  product_code: '',
  product_type: '',
  product_family: '',
  category: '',
  brand: '',
  status: 'Draft' as ProductStatus,
  short_description: '',
  long_description: '',
  has_variants: false,
})

/** Attribute values form data */
const attributeValues = ref<ProductAttributeValue[]>([])

/** Media items */
const mediaItems = ref<ProductMedia[]>([])

/** Whether form has unsaved changes */
const isDirty = ref(false)

/** Delete confirmation dialog */
const showDeleteConfirm = ref(false)

/** Save success flash message */
const saveSuccess = ref(false)

/** Tabs definition */
const tabs = computed(() => [
  { key: 'general' as const, label: 'General', icon: 'info' },
  { key: 'attributes' as const, label: 'Attributes', icon: 'attributes', count: attributeValues.value.length },
  { key: 'variants' as const, label: 'Variants', icon: 'variants', count: store.currentVariants.length, hidden: !form.value.has_variants && !isNewProduct.value },
  { key: 'media' as const, label: 'Media', icon: 'media', count: mediaItems.value.length },
])

/** Status options for the dropdown */
const statusOptions: { label: string; value: ProductStatus }[] = [
  { label: 'Draft', value: 'Draft' },
  { label: 'Active', value: 'Active' },
  { label: 'Discontinued', value: 'Discontinued' },
  { label: 'Archived', value: 'Archived' },
]

// =========================================================================
// Computed
// =========================================================================

const pageTitle = computed(() => {
  if (isNewProduct.value) return 'Create Product'
  return form.value.product_name || `Product: ${props.id}`
})

const completenessScore = computed(() => {
  return store.currentProduct?.completeness_score ?? 0
})

const completenessColor = computed(() => {
  const score = completenessScore.value
  if (score >= 80) return 'text-green-600'
  if (score >= 50) return 'text-amber-600'
  return 'text-red-600'
})

const completenessBarColor = computed(() => {
  const score = completenessScore.value
  if (score >= 80) return 'bg-green-500'
  if (score >= 50) return 'bg-amber-500'
  return 'bg-red-500'
})

const syncStatusDisplay = computed(() => {
  const product = store.currentProduct
  if (!product?.sync_status) return null
  return {
    status: product.sync_status,
    erp_item: product.erp_item,
    last_synced: product.last_synced,
  }
})

const syncStatusBadgeClass = computed(() => {
  switch (syncStatusDisplay.value?.status) {
    case 'Synced':
      return 'bg-green-100 text-green-800'
    case 'Pending':
      return 'bg-amber-100 text-amber-800'
    case 'Error':
      return 'bg-red-100 text-red-800'
    case 'Conflict':
      return 'bg-orange-100 text-orange-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
})

// =========================================================================
// Form Tracking
// =========================================================================

watch(form, () => {
  isDirty.value = true
}, { deep: true })

watch(attributeValues, () => {
  isDirty.value = true
}, { deep: true })

// =========================================================================
// Actions
// =========================================================================

function goBack(): void {
  if (isDirty.value) {
    if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
      router.push('/products')
    }
  } else {
    router.push('/products')
  }
}

/**
 * Populate the local form from the loaded product.
 */
function populateForm(product: ProductMaster): void {
  form.value = {
    product_name: product.product_name,
    product_code: product.product_code,
    product_type: product.product_type || '',
    product_family: product.product_family || '',
    category: product.category || '',
    brand: product.brand || '',
    status: product.status,
    short_description: product.short_description || '',
    long_description: product.long_description || '',
    has_variants: product.has_variants || false,
    variant_based_on: product.variant_based_on || '',
  }
  attributeValues.value = product.attribute_values ? [...product.attribute_values] : []
  mediaItems.value = product.media ? [...product.media] : []
  isDirty.value = false
}

async function saveProduct(): Promise<void> {
  const productData: Partial<ProductMaster> = {
    ...form.value,
    attribute_values: attributeValues.value,
    media: mediaItems.value,
  }

  let result: ProductMaster | null = null

  if (isNewProduct.value) {
    result = await store.createProduct(productData)
    if (result) {
      isDirty.value = false
      saveSuccess.value = true
      setTimeout(() => { saveSuccess.value = false }, 3000)
      router.replace(`/products/${result.name}`)
    }
  } else {
    result = await store.updateProduct(props.id, productData)
    if (result) {
      populateForm(result)
      saveSuccess.value = true
      setTimeout(() => { saveSuccess.value = false }, 3000)
    }
  }
}

function confirmDeleteProduct(): void {
  showDeleteConfirm.value = true
}

async function executeDelete(): Promise<void> {
  const success = await store.deleteProduct(props.id)
  if (success) {
    showDeleteConfirm.value = false
    router.push('/products')
  }
}

function cancelDelete(): void {
  showDeleteConfirm.value = false
}

// =========================================================================
// Attribute Value Helpers
// =========================================================================

function getAttributeDisplayValue(attr: ProductAttributeValue): string {
  if (attr.display_value) return attr.display_value
  if (attr.value_text) return attr.value_text
  if (attr.value_int !== undefined && attr.value_int !== null) return String(attr.value_int)
  if (attr.value_float !== undefined && attr.value_float !== null) return String(attr.value_float)
  if (attr.value_boolean !== undefined && attr.value_boolean !== null) return attr.value_boolean ? 'Yes' : 'No'
  if (attr.value_date) return attr.value_date
  if (attr.value_datetime) return attr.value_datetime
  if (attr.value_link) return attr.value_link
  if (attr.value_long_text) return attr.value_long_text.substring(0, 100) + '...'
  return '—'
}

function updateAttributeValue(index: number, field: string, value: unknown): void {
  const updated = [...attributeValues.value]
  updated[index] = { ...updated[index], [field]: value }
  attributeValues.value = updated
}

function removeAttributeValue(index: number): void {
  attributeValues.value.splice(index, 1)
}

function addAttributeValue(): void {
  attributeValues.value.push({
    attribute: '',
    value_type: 'String',
    value_text: '',
  })
}

// =========================================================================
// Media Helpers
// =========================================================================

function setPrimaryMedia(index: number): void {
  mediaItems.value = mediaItems.value.map((item, i) => ({
    ...item,
    is_primary: i === index,
  }))
}

function removeMedia(index: number): void {
  mediaItems.value.splice(index, 1)
}

// =========================================================================
// Lifecycle
// =========================================================================

onMounted(async () => {
  if (!isNewProduct.value) {
    const product = await store.fetchProduct(props.id)
    if (product) {
      populateForm(product)
      await store.fetchVariants(props.id)
    }
  }
  await store.fetchFamilies()
})

onBeforeUnmount(() => {
  store.clearCurrentProduct()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button class="btn-ghost p-2" @click="goBack">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <div>
          <h1 class="text-2xl font-bold text-pim-text">{{ pageTitle }}</h1>
          <p v-if="!isNewProduct" class="mt-0.5 text-sm text-pim-muted">
            {{ form.product_code }}
          </p>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <!-- Save success flash -->
        <span
          v-if="saveSuccess"
          class="text-sm font-medium text-green-600"
        >
          Saved successfully
        </span>

        <!-- Dirty indicator -->
        <span
          v-if="isDirty"
          class="text-xs text-amber-600"
        >
          Unsaved changes
        </span>

        <!-- Delete button (existing product only) -->
        <button
          v-if="!isNewProduct"
          class="btn-ghost text-red-500 hover:text-red-700"
          @click="confirmDeleteProduct"
        >
          {{ t('common.delete') }}
        </button>

        <!-- Save button -->
        <button
          class="btn-primary inline-flex items-center gap-2"
          :disabled="store.saveLoading"
          @click="saveProduct"
        >
          <svg
            v-if="store.saveLoading"
            class="h-4 w-4 animate-spin"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          {{ t('common.save') }}
        </button>
      </div>
    </div>

    <!-- Error Banner -->
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
    </div>

    <!-- Loading State -->
    <div v-if="store.detailLoading && !isNewProduct" class="flex items-center justify-center py-12">
      <div class="flex items-center gap-3">
        <svg class="h-5 w-5 animate-spin text-primary-600" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        <span class="text-pim-muted">{{ t('common.loading') }}</span>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-4">
      <!-- Left Column: Tabs & Content -->
      <div class="lg:col-span-3">
        <!-- Tab Navigation -->
        <div class="border-b border-pim-border">
          <nav class="-mb-px flex gap-6">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              v-show="!tab.hidden"
              class="border-b-2 px-1 py-3 text-sm font-medium transition-colors"
              :class="
                activeTab === tab.key
                  ? 'border-primary-600 text-primary-600'
                  : 'border-transparent text-pim-muted hover:border-gray-300 hover:text-pim-text'
              "
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
              <span
                v-if="tab.count !== undefined && tab.count > 0"
                class="ml-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs"
              >
                {{ tab.count }}
              </span>
            </button>
          </nav>
        </div>

        <!-- Tab: General Information -->
        <div v-if="activeTab === 'general'" class="mt-6 space-y-6">
          <!-- Core Fields -->
          <div class="card">
            <h3 class="mb-4 text-lg font-medium text-pim-text">Basic Information</h3>
            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
              <!-- Product Name -->
              <div class="md:col-span-2">
                <label class="mb-1 block text-sm font-medium text-pim-text">
                  Product Name <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.product_name"
                  type="text"
                  class="input w-full"
                  placeholder="Enter product name"
                />
              </div>

              <!-- Product Code -->
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">
                  Product Code <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.product_code"
                  type="text"
                  class="input w-full"
                  placeholder="e.g., PROD-001"
                  :disabled="!isNewProduct"
                />
              </div>

              <!-- Status -->
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">Status</label>
                <select v-model="form.status" class="input w-full">
                  <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>

              <!-- Product Type -->
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">Product Type</label>
                <input
                  v-model="form.product_type"
                  type="text"
                  class="input w-full"
                  placeholder="Select product type"
                />
              </div>

              <!-- Product Family -->
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">Product Family</label>
                <select v-model="form.product_family" class="input w-full">
                  <option value="">No family</option>
                  <option v-for="family in store.families" :key="family.name" :value="family.name">
                    {{ family.family_name }}
                  </option>
                </select>
              </div>

              <!-- Category -->
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">Category</label>
                <input
                  v-model="form.category"
                  type="text"
                  class="input w-full"
                  placeholder="Select category"
                />
              </div>

              <!-- Brand -->
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">Brand</label>
                <input
                  v-model="form.brand"
                  type="text"
                  class="input w-full"
                  placeholder="Enter brand"
                />
              </div>
            </div>
          </div>

          <!-- Descriptions -->
          <div class="card">
            <h3 class="mb-4 text-lg font-medium text-pim-text">Descriptions</h3>
            <div class="space-y-4">
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">Short Description</label>
                <textarea
                  v-model="form.short_description"
                  class="input w-full"
                  rows="2"
                  placeholder="Brief product description"
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-pim-text">Long Description</label>
                <textarea
                  v-model="form.long_description"
                  class="input w-full"
                  rows="6"
                  placeholder="Detailed product description"
                />
              </div>
            </div>
          </div>

          <!-- Variant Configuration -->
          <div class="card">
            <h3 class="mb-4 text-lg font-medium text-pim-text">Variant Configuration</h3>
            <div class="flex items-center gap-3">
              <label class="relative inline-flex cursor-pointer items-center">
                <input
                  v-model="form.has_variants"
                  type="checkbox"
                  class="peer sr-only"
                />
                <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-primary-600 peer-checked:after:translate-x-full peer-checked:after:border-white" />
              </label>
              <span class="text-sm text-pim-text">This product has variants</span>
            </div>
            <p v-if="form.has_variants" class="mt-2 text-sm text-pim-muted">
              Configure variants in the Variants tab. You can define variant axes (e.g., Color, Size) and generate combinations.
            </p>
          </div>
        </div>

        <!-- Tab: Attributes -->
        <div v-if="activeTab === 'attributes'" class="mt-6 space-y-4">
          <div class="card">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-lg font-medium text-pim-text">Attribute Values</h3>
              <button class="btn-secondary text-sm" @click="addAttributeValue">
                <svg class="mr-1 inline-block h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Add Attribute
              </button>
            </div>

            <!-- Empty state -->
            <div v-if="attributeValues.length === 0" class="py-8 text-center">
              <svg class="mx-auto h-10 w-10 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <p class="mt-2 text-sm text-pim-muted">No attribute values defined yet.</p>
              <p class="text-xs text-pim-muted">
                Attributes are inherited from the product family, or you can add them manually.
              </p>
            </div>

            <!-- Attribute value rows -->
            <div v-else class="space-y-3">
              <div
                v-for="(attr, index) in attributeValues"
                :key="index"
                class="flex items-start gap-3 rounded-lg border border-pim-border p-3"
              >
                <!-- Attribute name -->
                <div class="min-w-0 flex-1">
                  <label class="mb-1 block text-xs font-medium text-pim-muted">Attribute</label>
                  <input
                    :value="attr.attribute"
                    type="text"
                    class="input w-full text-sm"
                    placeholder="Attribute name"
                    @input="updateAttributeValue(index, 'attribute', ($event.target as HTMLInputElement).value)"
                  />
                </div>

                <!-- Value type -->
                <div class="w-28">
                  <label class="mb-1 block text-xs font-medium text-pim-muted">Type</label>
                  <select
                    :value="attr.value_type"
                    class="input w-full text-sm"
                    @change="updateAttributeValue(index, 'value_type', ($event.target as HTMLSelectElement).value)"
                  >
                    <option value="String">Text</option>
                    <option value="Integer">Integer</option>
                    <option value="Float">Decimal</option>
                    <option value="Boolean">Boolean</option>
                    <option value="Date">Date</option>
                    <option value="JSON">JSON</option>
                  </select>
                </div>

                <!-- Value input (type-aware) -->
                <div class="min-w-0 flex-1">
                  <label class="mb-1 block text-xs font-medium text-pim-muted">Value</label>
                  <!-- Text value -->
                  <input
                    v-if="attr.value_type === 'String' || !attr.value_type"
                    :value="attr.value_text"
                    type="text"
                    class="input w-full text-sm"
                    placeholder="Enter value"
                    @input="updateAttributeValue(index, 'value_text', ($event.target as HTMLInputElement).value)"
                  />
                  <!-- Integer value -->
                  <input
                    v-else-if="attr.value_type === 'Integer'"
                    :value="attr.value_int"
                    type="number"
                    class="input w-full text-sm"
                    placeholder="0"
                    @input="updateAttributeValue(index, 'value_int', Number(($event.target as HTMLInputElement).value))"
                  />
                  <!-- Float value -->
                  <input
                    v-else-if="attr.value_type === 'Float'"
                    :value="attr.value_float"
                    type="number"
                    step="0.01"
                    class="input w-full text-sm"
                    placeholder="0.00"
                    @input="updateAttributeValue(index, 'value_float', Number(($event.target as HTMLInputElement).value))"
                  />
                  <!-- Boolean value -->
                  <select
                    v-else-if="attr.value_type === 'Boolean'"
                    :value="attr.value_boolean ? 'true' : 'false'"
                    class="input w-full text-sm"
                    @change="updateAttributeValue(index, 'value_boolean', ($event.target as HTMLSelectElement).value === 'true')"
                  >
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                  </select>
                  <!-- Date value -->
                  <input
                    v-else-if="attr.value_type === 'Date'"
                    :value="attr.value_date"
                    type="date"
                    class="input w-full text-sm"
                    @input="updateAttributeValue(index, 'value_date', ($event.target as HTMLInputElement).value)"
                  />
                  <!-- JSON value -->
                  <textarea
                    v-else-if="attr.value_type === 'JSON'"
                    :value="attr.value_json"
                    class="input w-full text-sm"
                    rows="2"
                    placeholder="{}"
                    @input="updateAttributeValue(index, 'value_json', ($event.target as HTMLTextAreaElement).value)"
                  />
                  <!-- Fallback -->
                  <input
                    v-else
                    :value="getAttributeDisplayValue(attr)"
                    type="text"
                    class="input w-full text-sm"
                    @input="updateAttributeValue(index, 'value_text', ($event.target as HTMLInputElement).value)"
                  />
                </div>

                <!-- Unit -->
                <div class="w-20">
                  <label class="mb-1 block text-xs font-medium text-pim-muted">Unit</label>
                  <input
                    :value="attr.unit"
                    type="text"
                    class="input w-full text-sm"
                    placeholder="e.g., kg"
                    @input="updateAttributeValue(index, 'unit', ($event.target as HTMLInputElement).value)"
                  />
                </div>

                <!-- Remove button -->
                <div class="flex items-end pb-0.5">
                  <button
                    class="btn-ghost p-1.5 text-red-500 hover:text-red-700"
                    title="Remove attribute"
                    @click="removeAttributeValue(index)"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Variants -->
        <div v-if="activeTab === 'variants'" class="mt-6">
          <VariantManager
            v-if="!isNewProduct"
            :parent-product="props.id"
            :product-family="form.product_family || ''"
          />
          <div v-else class="card py-8 text-center">
            <p class="text-sm text-pim-muted">
              Save the product first to manage variants.
            </p>
          </div>
        </div>

        <!-- Tab: Media -->
        <div v-if="activeTab === 'media'" class="mt-6 space-y-4">
          <div class="card">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-lg font-medium text-pim-text">Product Media</h3>
              <button class="btn-secondary text-sm">
                <svg class="mr-1 inline-block h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Upload
              </button>
            </div>

            <!-- Empty state -->
            <div v-if="mediaItems.length === 0" class="py-8 text-center">
              <svg class="mx-auto h-10 w-10 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p class="mt-2 text-sm text-pim-muted">No media uploaded yet.</p>
              <p class="text-xs text-pim-muted">
                Upload images, videos, or documents for this product.
              </p>
            </div>

            <!-- Media grid -->
            <div v-else class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
              <div
                v-for="(item, index) in mediaItems"
                :key="index"
                class="group relative rounded-lg border border-pim-border p-2"
                :class="{ 'ring-2 ring-primary-500': item.is_primary }"
              >
                <!-- Media thumbnail -->
                <div class="flex h-32 items-center justify-center rounded bg-gray-50">
                  <svg
                    v-if="item.media_type === 'Image'"
                    class="h-8 w-8 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <svg
                    v-else-if="item.media_type === 'Video'"
                    class="h-8 w-8 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  <svg
                    v-else
                    class="h-8 w-8 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>

                <!-- Media info -->
                <div class="mt-2">
                  <p class="truncate text-xs font-medium text-pim-text">
                    {{ item.title || item.file }}
                  </p>
                  <p class="text-xs text-pim-muted">{{ item.media_type }}</p>
                </div>

                <!-- Primary badge -->
                <span
                  v-if="item.is_primary"
                  class="absolute right-1 top-1 rounded bg-primary-600 px-1.5 py-0.5 text-[10px] font-bold text-white"
                >
                  Primary
                </span>

                <!-- Hover actions -->
                <div class="absolute inset-x-0 bottom-0 flex justify-center gap-1 rounded-b-lg bg-white/90 p-1 opacity-0 transition-opacity group-hover:opacity-100">
                  <button
                    v-if="!item.is_primary"
                    class="rounded px-2 py-1 text-xs text-primary-600 hover:bg-primary-50"
                    @click="setPrimaryMedia(index)"
                  >
                    Set Primary
                  </button>
                  <button
                    class="rounded px-2 py-1 text-xs text-red-600 hover:bg-red-50"
                    @click="removeMedia(index)"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Sidebar -->
      <div class="space-y-4">
        <!-- Completeness Card -->
        <div class="card">
          <h4 class="text-sm font-medium text-pim-text">Completeness</h4>
          <div class="mt-3">
            <div class="flex items-end gap-2">
              <span class="text-3xl font-bold" :class="completenessColor">
                {{ completenessScore }}%
              </span>
            </div>
            <div class="mt-2 h-2 w-full rounded-full bg-gray-200">
              <div
                class="h-2 rounded-full transition-all"
                :class="completenessBarColor"
                :style="{ width: `${completenessScore}%` }"
              />
            </div>
          </div>
        </div>

        <!-- Status Card -->
        <div class="card">
          <h4 class="text-sm font-medium text-pim-text">Product Status</h4>
          <div class="mt-2">
            <span
              class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
              :class="{
                'bg-green-100 text-green-800': form.status === 'Active',
                'bg-amber-100 text-amber-800': form.status === 'Draft',
                'bg-gray-100 text-gray-800': form.status === 'Discontinued',
                'bg-red-100 text-red-800': form.status === 'Archived',
              }"
            >
              {{ form.status }}
            </span>
          </div>
        </div>

        <!-- ERPNext Sync Card -->
        <div v-if="syncStatusDisplay" class="card">
          <h4 class="text-sm font-medium text-pim-text">ERPNext Sync</h4>
          <div class="mt-2 space-y-2">
            <div class="flex items-center gap-2">
              <span
                class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
                :class="syncStatusBadgeClass"
              >
                {{ syncStatusDisplay.status }}
              </span>
            </div>
            <div v-if="syncStatusDisplay.erp_item" class="text-xs text-pim-muted">
              <span class="font-medium">ERP Item:</span> {{ syncStatusDisplay.erp_item }}
            </div>
            <div v-if="syncStatusDisplay.last_synced" class="text-xs text-pim-muted">
              <span class="font-medium">Last synced:</span> {{ syncStatusDisplay.last_synced }}
            </div>
          </div>
        </div>

        <!-- Quick Info Card -->
        <div v-if="!isNewProduct && store.currentProduct" class="card">
          <h4 class="text-sm font-medium text-pim-text">Details</h4>
          <div class="mt-2 space-y-2 text-xs text-pim-muted">
            <div>
              <span class="font-medium">Created:</span>
              {{ store.currentProduct.creation }}
            </div>
            <div>
              <span class="font-medium">Modified:</span>
              {{ store.currentProduct.modified }}
            </div>
            <div>
              <span class="font-medium">Owner:</span>
              {{ store.currentProduct.owner }}
            </div>
          </div>
        </div>

        <!-- Variants Summary Card -->
        <div v-if="!isNewProduct && form.has_variants" class="card">
          <h4 class="text-sm font-medium text-pim-text">Variants</h4>
          <div class="mt-2">
            <p class="text-2xl font-bold text-pim-text">
              {{ store.currentVariants.length }}
            </p>
            <p class="text-xs text-pim-muted">variant{{ store.currentVariants.length !== 1 ? 's' : '' }} defined</p>
            <button
              class="mt-2 text-xs font-medium text-primary-600 hover:text-primary-700"
              @click="activeTab = 'variants'"
            >
              Manage variants &rarr;
            </button>
          </div>
        </div>
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
            Are you sure you want to delete "{{ form.product_name }}"? This will also delete all associated variants and attribute values. This action cannot be undone.
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
