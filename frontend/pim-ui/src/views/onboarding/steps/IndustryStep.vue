<script setup lang="ts">
/**
 * IndustryStep - Industry archetype selection step.
 *
 * Collects:
 * - Industry archetype (fashion, industrial, food, base)
 * - Estimated product count
 * - Whether the business uses product variants
 *
 * Integrates with the onboarding store to:
 * - Fetch available archetypes from backend
 * - Preview what each archetype creates
 * - Apply the selected template
 */
import { reactive, onMounted, ref, computed, watch } from 'vue'
import { useOnboardingStore } from '@/stores/onboarding'
import type { IndustrySelectionData, StepFormData, ArchetypeInfo } from '@/types'

const props = defineProps<{
  data: Record<string, unknown>
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update', data: StepFormData): void
  (e: 'next', data: StepFormData): void
  (e: 'back'): void
}>()

const store = useOnboardingStore()
const showPreview = ref(false)

const PRODUCT_COUNT_OPTIONS = [
  { value: '1-100', label: '1 - 100 products' },
  { value: '100-1000', label: '100 - 1,000 products' },
  { value: '1000-10000', label: '1,000 - 10,000 products' },
  { value: '10000+', label: '10,000+ products' },
] as const

/** Archetype display metadata with icons */
const ARCHETYPE_ICONS: Record<string, { icon: string; color: string }> = {
  fashion: { icon: '&#128087;', color: 'bg-pink-50 border-pink-200 hover:border-pink-400' },
  industrial: { icon: '&#9881;', color: 'bg-slate-50 border-slate-200 hover:border-slate-400' },
  food: { icon: '&#127828;', color: 'bg-amber-50 border-amber-200 hover:border-amber-400' },
  base: { icon: '&#128230;', color: 'bg-blue-50 border-blue-200 hover:border-blue-400' },
}

const form = reactive<IndustrySelectionData>({
  archetype: (props.data.archetype as string) ?? store.selectedArchetype ?? '',
  product_count_estimate: (props.data.product_count_estimate as string) ?? '',
  has_variants: (props.data.has_variants as boolean) ?? false,
})

/** Fetch archetypes on mount */
onMounted(async () => {
  if (store.archetypes.length === 0) {
    await store.fetchArchetypes()
  }
})

/** Get display info for an archetype */
function getArchetypeStyle(archetype: string): string {
  const style = ARCHETYPE_ICONS[archetype] ?? ARCHETYPE_ICONS.base
  return `${style.color} ${form.archetype === archetype ? 'ring-2 ring-primary-500 border-primary-500' : ''}`
}

function getArchetypeIcon(archetype: string): string {
  return ARCHETYPE_ICONS[archetype]?.icon ?? '&#128230;'
}

/** Selected archetype info */
const selectedArchetypeInfo = computed<ArchetypeInfo | null>(() => {
  return store.archetypes.find((a) => a.archetype === form.archetype) ?? null
})

/** Select an archetype and optionally preview it */
async function selectArchetype(archetype: string): Promise<void> {
  form.archetype = archetype
  showPreview.value = false
  await store.previewArchetype(archetype)
  showPreview.value = true
}

/** Emit form data changes */
watch(
  form,
  (newVal) => {
    emit('update', { ...newVal })
  },
  { deep: true },
)

function isValid(): boolean {
  return form.archetype.length > 0
}

function handleSubmit(): void {
  if (isValid()) {
    emit('next', { ...form })
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- Archetype Selection Grid -->
    <div>
      <label class="mb-3 block text-sm font-medium text-pim-text">
        Select your industry profile <span class="text-red-500">*</span>
      </label>
      <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <button
          v-for="archetype in store.archetypes"
          :key="archetype.archetype"
          class="flex items-start gap-3 rounded-lg border p-4 text-left transition-all duration-200"
          :class="getArchetypeStyle(archetype.archetype)"
          @click="selectArchetype(archetype.archetype)"
        >
          <span class="text-2xl" v-html="getArchetypeIcon(archetype.archetype)" />
          <div class="flex-1">
            <p class="font-medium text-pim-text">{{ archetype.label }}</p>
            <p class="mt-0.5 text-xs text-pim-muted">{{ archetype.description }}</p>
          </div>
          <div v-if="form.archetype === archetype.archetype" class="flex-shrink-0">
            <svg class="h-5 w-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </button>
      </div>
    </div>

    <!-- Archetype Preview -->
    <div
      v-if="showPreview && store.archetypePreview"
      class="rounded-lg border border-pim-border bg-pim-surface p-4"
    >
      <h3 class="mb-2 text-sm font-medium text-pim-text">
        What this template creates:
      </h3>
      <div class="grid grid-cols-2 gap-2 sm:grid-cols-3">
        <div
          v-for="(section, key) in store.archetypePreview.sections"
          :key="key"
          class="rounded-md bg-white p-2.5 text-center"
        >
          <p class="text-lg font-semibold text-primary-600">{{ section.count }}</p>
          <p class="text-xs text-pim-muted capitalize">{{ String(key).replace(/_/g, ' ') }}</p>
        </div>
      </div>
    </div>

    <!-- Product Count Estimate -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="product_count">
        How many products do you manage?
      </label>
      <select
        id="product_count"
        v-model="form.product_count_estimate"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
      >
        <option value="">Select a range</option>
        <option
          v-for="option in PRODUCT_COUNT_OPTIONS"
          :key="option.value"
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>
    </div>

    <!-- Variants Toggle -->
    <div class="flex items-center gap-3">
      <input
        id="has_variants"
        v-model="form.has_variants"
        type="checkbox"
        class="h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
      />
      <label class="text-sm text-pim-text" for="has_variants">
        My products have variants (e.g., size, color)
      </label>
    </div>

    <!-- Validation hint -->
    <p v-if="!isValid()" class="text-xs text-amber-600">
      Please select an industry profile to continue.
    </p>
  </div>
</template>
