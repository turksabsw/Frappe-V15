<script setup lang="ts">
/**
 * VariantManager.vue - Product variant management component.
 *
 * Features:
 * - Variant axis configuration (select attributes as axes)
 * - Value selection for each axis (e.g., Color: Red, Blue, Green)
 * - Preview of variant combinations before generation
 * - Generate variants action with result reporting
 * - Existing variant list/grid with status, SKU, completeness
 * - Delete variants
 * - Navigate to variant detail (ERPNext Item)
 */

import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProductStore } from '@/stores/product'
import { useFrappeAPI, PIM_API } from '@/composables/useFrappeAPI'
import type {
  ProductVariant,
  VariantAxisDefinition,
  VariantGenerationResult,
  PIMAttribute,
  FamilyVariantAttribute,
} from '@/types'

const props = defineProps<{
  parentProduct: string
  productFamily: string
}>()

const { t } = useI18n()
const store = useProductStore()
const api = useFrappeAPI()

// =========================================================================
// Local State
// =========================================================================

/** Whether the generation panel is expanded */
const showGenerator = ref(false)

/** Available variant axis attributes (from family or manual) */
const availableAxes = ref<PIMAttribute[]>([])

/** Loading state for axes */
const axesLoading = ref(false)

/** Configured axes for generation */
const configuredAxes = ref<VariantAxisConfig[]>([])

/** Generation result from the last generation */
const generationResult = ref<VariantGenerationResult | null>(null)

/** Whether generation is in progress */
const generating = ref(false)

/** Variant delete confirmation */
const deleteConfirmName = ref('')

/** Search within variants */
const variantSearch = ref('')

/** Interface for local axis configuration */
interface VariantAxisConfig {
  attribute: string
  attribute_name: string
  values: string[]
  inputValue: string
}

// =========================================================================
// Computed
// =========================================================================

/** Filtered variants based on search */
const filteredVariants = computed(() => {
  if (!variantSearch.value) return store.currentVariants
  const term = variantSearch.value.toLowerCase()
  return store.currentVariants.filter((v) =>
    v.variant_name.toLowerCase().includes(term) ||
    v.variant_code.toLowerCase().includes(term) ||
    (v.sku && v.sku.toLowerCase().includes(term)),
  )
})

/** Preview of variant combinations that would be generated */
const combinationPreview = computed(() => {
  const activeAxes = configuredAxes.value.filter((a) => a.values.length > 0)
  if (activeAxes.length === 0) return []

  // Generate cartesian product of all axis values
  const combinations = cartesianProduct(activeAxes.map((a) => a.values))
  return combinations.map((combo) => {
    const parts: Record<string, string> = {}
    activeAxes.forEach((axis, index) => {
      parts[axis.attribute_name] = combo[index]
    })
    return parts
  })
})

/** Total count of combinations that would be generated */
const combinationCount = computed(() => combinationPreview.value.length)

/** Whether generation can proceed */
const canGenerate = computed(() => {
  return configuredAxes.value.some((a) => a.values.length > 0) && !generating.value
})

// =========================================================================
// Helper Functions
// =========================================================================

/**
 * Compute cartesian product of arrays.
 */
function cartesianProduct(arrays: string[][]): string[][] {
  if (arrays.length === 0) return [[]]
  return arrays.reduce<string[][]>(
    (acc, curr) => acc.flatMap((a) => curr.map((b) => [...a, b])),
    [[]],
  )
}

function variantStatusBadge(status: string): string {
  switch (status) {
    case 'Active':
      return 'bg-green-100 text-green-800'
    case 'Draft':
      return 'bg-amber-100 text-amber-800'
    case 'Discontinued':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

function completenessColor(score: number | undefined): string {
  if (!score) return 'bg-gray-300'
  if (score >= 80) return 'bg-green-500'
  if (score >= 50) return 'bg-amber-500'
  return 'bg-red-500'
}

// =========================================================================
// Actions
// =========================================================================

/**
 * Fetch available variant axis attributes.
 * If the product has a family, get variant axes from the family.
 * Otherwise, list all attributes marked as variant axes.
 */
async function fetchAvailableAxes(): Promise<void> {
  axesLoading.value = true
  try {
    if (props.productFamily) {
      // Fetch variant axes from the family
      const result = await api.callMethod<FamilyVariantAttribute[]>(
        PIM_API.taxonomy.familyAttributes,
        { family: props.productFamily, variant_only: true },
      )
      // Convert to PIMAttribute-like structure
      availableAxes.value = result.map((va) => ({
        name: va.attribute,
        attribute_name: va.attribute,
        attribute_code: va.attribute,
        attribute_type: '',
        is_required: va.is_required || false,
        is_filterable: false,
        is_searchable: false,
        is_variant_axis: true,
        is_localizable: false,
        sort_order: va.sort_order,
        owner: '',
        creation: '',
        modified: '',
        modified_by: '',
        docstatus: 0,
        idx: 0,
      }))
    } else {
      // Fetch all attributes that can be variant axes
      const result = await api.getList<PIMAttribute>({
        doctype: 'PIM Attribute',
        filters: { is_variant_axis: 1 },
        fields: ['name', 'attribute_name', 'attribute_code', 'attribute_type', 'sort_order'],
        order_by: 'sort_order asc',
        limit_page_length: 50,
      })
      availableAxes.value = result
    }
  } catch {
    availableAxes.value = []
  } finally {
    axesLoading.value = false
  }
}

/**
 * Add an axis to the configuration.
 */
function addAxis(attr: PIMAttribute): void {
  // Don't add duplicates
  if (configuredAxes.value.some((a) => a.attribute === attr.name)) return

  configuredAxes.value.push({
    attribute: attr.name,
    attribute_name: attr.attribute_name,
    values: [],
    inputValue: '',
  })
}

/**
 * Remove an axis from configuration.
 */
function removeAxis(index: number): void {
  configuredAxes.value.splice(index, 1)
}

/**
 * Add a value to an axis.
 */
function addAxisValue(axisIndex: number): void {
  const axis = configuredAxes.value[axisIndex]
  const value = axis.inputValue.trim()
  if (value && !axis.values.includes(value)) {
    axis.values.push(value)
    axis.inputValue = ''
  }
}

/**
 * Handle Enter key on axis value input.
 */
function handleAxisValueKeydown(event: KeyboardEvent, axisIndex: number): void {
  if (event.key === 'Enter') {
    event.preventDefault()
    addAxisValue(axisIndex)
  }
}

/**
 * Remove a value from an axis.
 */
function removeAxisValue(axisIndex: number, valueIndex: number): void {
  configuredAxes.value[axisIndex].values.splice(valueIndex, 1)
}

/**
 * Generate variants based on configured axes.
 */
async function generateVariants(): Promise<void> {
  if (!canGenerate.value) return

  generating.value = true
  generationResult.value = null

  const axes: VariantAxisDefinition[] = configuredAxes.value
    .filter((a) => a.values.length > 0)
    .map((a) => ({
      attribute: a.attribute,
      values: a.values,
    }))

  const result = await store.generateVariants({
    parent_product: props.parentProduct,
    axes,
  })

  if (result) {
    generationResult.value = result
  }
  generating.value = false
}

/**
 * Confirm and delete a variant.
 */
function confirmDeleteVariant(name: string): void {
  deleteConfirmName.value = name
}

async function executeDeleteVariant(): Promise<void> {
  if (!deleteConfirmName.value) return
  try {
    await api.deleteDoc('Product Variant', deleteConfirmName.value)
    await store.fetchVariants(props.parentProduct)
  } catch {
    // Error handled by API composable
  }
  deleteConfirmName.value = ''
}

function cancelDeleteVariant(): void {
  deleteConfirmName.value = ''
}

// =========================================================================
// Lifecycle
// =========================================================================

onMounted(async () => {
  await Promise.all([
    store.fetchVariants(props.parentProduct),
    fetchAvailableAxes(),
  ])
})

// Re-fetch axes when family changes
watch(() => props.productFamily, () => {
  fetchAvailableAxes()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-medium text-pim-text">Variant Management</h3>
        <p class="text-sm text-pim-muted">
          {{ store.currentVariants.length }} variant{{ store.currentVariants.length !== 1 ? 's' : '' }} defined
        </p>
      </div>
      <button
        class="btn-primary inline-flex items-center gap-2 text-sm"
        @click="showGenerator = !showGenerator"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        {{ showGenerator ? 'Hide Generator' : 'Generate Variants' }}
      </button>
    </div>

    <!-- Variant Generator Panel -->
    <div v-if="showGenerator" class="card border-2 border-primary-100">
      <h4 class="mb-4 font-medium text-pim-text">Variant Generator</h4>
      <p class="mb-4 text-sm text-pim-muted">
        Define variant axes (e.g., Color, Size) and their values to automatically generate variant combinations.
      </p>

      <!-- Available axes -->
      <div class="mb-4">
        <label class="mb-2 block text-sm font-medium text-pim-text">Available Axes</label>
        <div v-if="axesLoading" class="text-sm text-pim-muted">
          {{ t('common.loading') }}
        </div>
        <div v-else-if="availableAxes.length === 0" class="text-sm text-pim-muted">
          No variant axes defined. Set attributes as variant axes in the Product Family or Attribute configuration.
        </div>
        <div v-else class="flex flex-wrap gap-2">
          <button
            v-for="attr in availableAxes"
            :key="attr.name"
            class="inline-flex items-center gap-1 rounded-lg border border-pim-border px-3 py-1.5 text-sm transition-colors hover:border-primary-300 hover:bg-primary-50"
            :class="{
              'border-primary-500 bg-primary-50 text-primary-700': configuredAxes.some(a => a.attribute === attr.name),
              'text-pim-text': !configuredAxes.some(a => a.attribute === attr.name),
            }"
            :disabled="configuredAxes.some(a => a.attribute === attr.name)"
            @click="addAxis(attr)"
          >
            <svg
              v-if="configuredAxes.some(a => a.attribute === attr.name)"
              class="h-3.5 w-3.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            {{ attr.attribute_name }}
          </button>
        </div>
      </div>

      <!-- Configured axes with value inputs -->
      <div v-if="configuredAxes.length > 0" class="space-y-4">
        <div
          v-for="(axis, axisIndex) in configuredAxes"
          :key="axis.attribute"
          class="rounded-lg border border-pim-border p-4"
        >
          <div class="mb-3 flex items-center justify-between">
            <h5 class="font-medium text-pim-text">{{ axis.attribute_name }}</h5>
            <button
              class="btn-ghost p-1 text-red-500 hover:text-red-700"
              title="Remove axis"
              @click="removeAxis(axisIndex)"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Value tags -->
          <div class="mb-2 flex flex-wrap gap-1.5">
            <span
              v-for="(value, valueIndex) in axis.values"
              :key="valueIndex"
              class="inline-flex items-center gap-1 rounded-full bg-primary-100 px-2.5 py-0.5 text-sm font-medium text-primary-800"
            >
              {{ value }}
              <button
                class="ml-0.5 text-primary-500 hover:text-primary-700"
                @click="removeAxisValue(axisIndex, valueIndex)"
              >
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </span>
          </div>

          <!-- Value input -->
          <div class="flex gap-2">
            <input
              v-model="axis.inputValue"
              type="text"
              class="input flex-1 text-sm"
              :placeholder="`Add ${axis.attribute_name} value (press Enter)`"
              @keydown="handleAxisValueKeydown($event, axisIndex)"
            />
            <button
              class="btn-secondary text-sm"
              :disabled="!axis.inputValue.trim()"
              @click="addAxisValue(axisIndex)"
            >
              Add
            </button>
          </div>
        </div>
      </div>

      <!-- Combination Preview -->
      <div v-if="combinationCount > 0" class="mt-4">
        <div class="mb-2 flex items-center justify-between">
          <h5 class="text-sm font-medium text-pim-text">
            Preview: {{ combinationCount }} combination{{ combinationCount !== 1 ? 's' : '' }}
          </h5>
        </div>
        <div class="max-h-48 overflow-auto rounded-lg border border-pim-border">
          <table class="w-full text-sm">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-3 py-2 text-left text-xs font-medium uppercase text-pim-muted">#</th>
                <th
                  v-for="axis in configuredAxes.filter(a => a.values.length > 0)"
                  :key="axis.attribute"
                  class="px-3 py-2 text-left text-xs font-medium uppercase text-pim-muted"
                >
                  {{ axis.attribute_name }}
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-pim-border">
              <tr v-for="(combo, index) in combinationPreview.slice(0, 50)" :key="index">
                <td class="px-3 py-1.5 text-pim-muted">{{ index + 1 }}</td>
                <td
                  v-for="(value, key) in combo"
                  :key="key"
                  class="px-3 py-1.5"
                >
                  {{ value }}
                </td>
              </tr>
            </tbody>
          </table>
          <p v-if="combinationCount > 50" class="border-t border-pim-border bg-gray-50 px-3 py-2 text-center text-xs text-pim-muted">
            Showing first 50 of {{ combinationCount }} combinations
          </p>
        </div>
      </div>

      <!-- Generate button -->
      <div class="mt-4 flex items-center gap-3">
        <button
          class="btn-primary"
          :disabled="!canGenerate"
          @click="generateVariants"
        >
          <svg
            v-if="generating"
            class="mr-2 inline-block h-4 w-4 animate-spin"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          {{ generating ? 'Generating...' : `Generate ${combinationCount} Variant${combinationCount !== 1 ? 's' : ''}` }}
        </button>
      </div>

      <!-- Generation Result -->
      <div v-if="generationResult" class="mt-4 rounded-lg border p-4" :class="generationResult.errors.length > 0 ? 'border-amber-200 bg-amber-50' : 'border-green-200 bg-green-50'">
        <div class="flex items-center gap-2">
          <svg
            v-if="generationResult.errors.length === 0"
            class="h-5 w-5 text-green-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else class="h-5 w-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <span class="font-medium" :class="generationResult.errors.length > 0 ? 'text-amber-800' : 'text-green-800'">
            {{ generationResult.created }} created, {{ generationResult.skipped }} skipped
          </span>
        </div>
        <ul v-if="generationResult.errors.length > 0" class="mt-2 list-inside list-disc text-sm text-amber-700">
          <li v-for="(err, i) in generationResult.errors" :key="i">{{ err }}</li>
        </ul>
      </div>
    </div>

    <!-- Existing Variants -->
    <div class="card">
      <div class="mb-4 flex items-center justify-between">
        <h4 class="font-medium text-pim-text">Existing Variants</h4>
        <!-- Search -->
        <div v-if="store.currentVariants.length > 0" class="relative w-64">
          <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="variantSearch"
            type="text"
            class="input w-full pl-10 text-sm"
            placeholder="Search variants..."
          />
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="store.currentVariants.length === 0" class="py-8 text-center">
        <svg class="mx-auto h-10 w-10 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p class="mt-2 text-sm text-pim-muted">No variants yet.</p>
        <p class="text-xs text-pim-muted">
          Use the variant generator above to create variant combinations.
        </p>
      </div>

      <!-- Variant grid -->
      <div v-else class="overflow-hidden rounded-lg border border-pim-border">
        <table class="w-full text-sm">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wider text-pim-muted">
                Variant
              </th>
              <th class="px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wider text-pim-muted">
                SKU
              </th>
              <th class="px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wider text-pim-muted">
                Status
              </th>
              <th class="px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wider text-pim-muted">
                Axis Values
              </th>
              <th class="px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wider text-pim-muted">
                Completeness
              </th>
              <th class="px-4 py-2.5 text-left text-xs font-medium uppercase tracking-wider text-pim-muted">
                Sync
              </th>
              <th class="px-4 py-2.5 text-right text-xs font-medium uppercase tracking-wider text-pim-muted">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-pim-border">
            <tr
              v-for="variant in filteredVariants"
              :key="variant.name"
              class="transition-colors hover:bg-gray-50"
            >
              <!-- Variant name/code -->
              <td class="px-4 py-3">
                <p class="font-medium text-pim-text">{{ variant.variant_name }}</p>
                <p class="text-xs text-pim-muted">{{ variant.variant_code }}</p>
              </td>

              <!-- SKU -->
              <td class="px-4 py-3 text-pim-muted">
                {{ variant.sku || '—' }}
              </td>

              <!-- Status -->
              <td class="px-4 py-3">
                <span
                  class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
                  :class="variantStatusBadge(variant.status)"
                >
                  {{ variant.status }}
                </span>
              </td>

              <!-- Axis values -->
              <td class="px-4 py-3">
                <div v-if="variant.axis_values && variant.axis_values.length > 0" class="flex flex-wrap gap-1">
                  <span
                    v-for="(av, i) in variant.axis_values"
                    :key="i"
                    class="inline-flex rounded bg-gray-100 px-1.5 py-0.5 text-xs text-pim-text"
                  >
                    {{ av.display_value || av.attribute_value }}
                  </span>
                </div>
                <span v-else class="text-xs text-pim-muted">—</span>
              </td>

              <!-- Completeness -->
              <td class="px-4 py-3">
                <div class="flex items-center gap-2">
                  <div class="h-1.5 w-16 rounded-full bg-gray-200">
                    <div
                      class="h-1.5 rounded-full transition-all"
                      :class="completenessColor(variant.completeness_score)"
                      :style="{ width: `${variant.completeness_score ?? 0}%` }"
                    />
                  </div>
                  <span class="text-xs text-pim-muted">{{ variant.completeness_score ?? 0 }}%</span>
                </div>
              </td>

              <!-- Sync status -->
              <td class="px-4 py-3">
                <span
                  v-if="variant.sync_status"
                  class="inline-flex rounded-full px-2 py-0.5 text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-800': variant.sync_status === 'Synced',
                    'bg-amber-100 text-amber-800': variant.sync_status === 'Pending',
                    'bg-red-100 text-red-800': variant.sync_status === 'Error',
                    'bg-gray-100 text-gray-800': variant.sync_status === 'Not Synced',
                  }"
                >
                  {{ variant.sync_status }}
                </span>
                <span v-else class="text-xs text-pim-muted">—</span>
              </td>

              <!-- Actions -->
              <td class="px-4 py-3 text-right">
                <div class="flex items-center justify-end gap-1">
                  <a
                    v-if="variant.erp_item"
                    :href="`/app/item/${variant.erp_item}`"
                    target="_blank"
                    class="btn-ghost p-1.5 text-primary-600 hover:text-primary-700"
                    title="Open in ERPNext"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                  <button
                    class="btn-ghost p-1.5 text-red-500 hover:text-red-700"
                    title="Delete variant"
                    @click="confirmDeleteVariant(variant.name)"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- No results for search -->
        <div
          v-if="filteredVariants.length === 0 && store.currentVariants.length > 0"
          class="border-t border-pim-border bg-gray-50 py-4 text-center text-sm text-pim-muted"
        >
          No variants match "{{ variantSearch }}"
        </div>
      </div>
    </div>

    <!-- Variant Delete Confirmation -->
    <Teleport to="body">
      <div
        v-if="deleteConfirmName"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
        @click.self="cancelDeleteVariant"
      >
        <div class="mx-4 w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
          <h3 class="text-lg font-semibold text-pim-text">Delete Variant</h3>
          <p class="mt-2 text-sm text-pim-muted">
            Are you sure you want to delete this variant? If it is synced to ERPNext, the linked Item will not be deleted.
          </p>
          <div class="mt-6 flex justify-end gap-3">
            <button class="btn-ghost" @click="cancelDeleteVariant">
              {{ t('common.cancel') }}
            </button>
            <button
              class="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
              @click="executeDeleteVariant"
            >
              {{ t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
