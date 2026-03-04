<script setup lang="ts">
/**
 * ProductStructureStep - Configure product organization preferences.
 *
 * Collects:
 * - Whether to use Product Families (hierarchical grouping)
 * - Whether to use Categories (navigation taxonomy)
 * - Number of variant levels
 * - SKU generation preferences
 */
import { reactive, watch } from 'vue'
import type { ProductStructureData, StepFormData } from '@/types'

const props = defineProps<{
  data: Record<string, unknown>
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update', data: StepFormData): void
  (e: 'next', data: StepFormData): void
  (e: 'back'): void
}>()

const VARIANT_LEVEL_OPTIONS = [
  { value: 0, label: 'No variants', description: 'Simple products only' },
  { value: 1, label: '1 level', description: 'e.g., Size OR Color' },
  { value: 2, label: '2 levels', description: 'e.g., Size AND Color' },
  { value: 3, label: '3 levels', description: 'e.g., Size, Color, and Material' },
] as const

const form = reactive<ProductStructureData>({
  use_families: (props.data.use_families as boolean) ?? true,
  use_categories: (props.data.use_categories as boolean) ?? true,
  variant_levels: (props.data.variant_levels as number) ?? 1,
  use_sku_generation: (props.data.use_sku_generation as boolean) ?? false,
  sku_pattern: (props.data.sku_pattern as string) ?? '',
})

/** Emit form data changes */
watch(
  form,
  (newVal) => {
    emit('update', { ...newVal })
  },
  { deep: true },
)

function handleSubmit(): void {
  emit('next', { ...form })
}
</script>

<template>
  <div class="space-y-6">
    <!-- Product Families Toggle -->
    <div class="rounded-lg border border-pim-border p-4">
      <div class="flex items-start gap-3">
        <input
          id="use_families"
          v-model="form.use_families"
          type="checkbox"
          class="mt-0.5 h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
        />
        <div class="flex-1">
          <label class="block text-sm font-medium text-pim-text" for="use_families">
            Use Product Families
          </label>
          <p class="mt-0.5 text-xs text-pim-muted">
            Group products by shared attributes. Families define which attributes a product needs
            and support inheritance through a hierarchy (e.g., Apparel &rarr; Tops &rarr; T-Shirts).
          </p>
        </div>
      </div>
    </div>

    <!-- Categories Toggle -->
    <div class="rounded-lg border border-pim-border p-4">
      <div class="flex items-start gap-3">
        <input
          id="use_categories"
          v-model="form.use_categories"
          type="checkbox"
          class="mt-0.5 h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
        />
        <div class="flex-1">
          <label class="block text-sm font-medium text-pim-text" for="use_categories">
            Use Categories
          </label>
          <p class="mt-0.5 text-xs text-pim-muted">
            Organize products in a navigation taxonomy. Categories define where products appear
            for customers (e.g., Women &rarr; Clothing &rarr; Dresses).
          </p>
        </div>
      </div>
    </div>

    <!-- Variant Levels -->
    <div>
      <label class="mb-2 block text-sm font-medium text-pim-text">
        Product Variant Levels
      </label>
      <div class="space-y-2">
        <label
          v-for="option in VARIANT_LEVEL_OPTIONS"
          :key="option.value"
          class="flex cursor-pointer items-center gap-3 rounded-lg border border-pim-border px-4 py-3 transition-colors hover:bg-pim-surface"
          :class="{
            'border-primary-500 bg-primary-50': form.variant_levels === option.value,
          }"
        >
          <input
            v-model="form.variant_levels"
            type="radio"
            :value="option.value"
            class="h-4 w-4 border-pim-border text-primary-600 focus:ring-primary-500"
          />
          <div>
            <p class="text-sm font-medium text-pim-text">{{ option.label }}</p>
            <p class="text-xs text-pim-muted">{{ option.description }}</p>
          </div>
        </label>
      </div>
    </div>

    <!-- SKU Generation -->
    <div class="rounded-lg border border-pim-border p-4">
      <div class="flex items-start gap-3">
        <input
          id="use_sku_generation"
          v-model="form.use_sku_generation"
          type="checkbox"
          class="mt-0.5 h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
        />
        <div class="flex-1">
          <label class="block text-sm font-medium text-pim-text" for="use_sku_generation">
            Auto-generate SKU codes
          </label>
          <p class="mt-0.5 text-xs text-pim-muted">
            Automatically generate SKU codes based on a naming pattern.
          </p>
        </div>
      </div>

      <!-- SKU Pattern (shown when enabled) -->
      <div v-if="form.use_sku_generation" class="mt-3 pl-7">
        <label class="mb-1 block text-xs font-medium text-pim-text" for="sku_pattern">
          SKU Pattern
        </label>
        <input
          id="sku_pattern"
          v-model="form.sku_pattern"
          type="text"
          class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          placeholder="e.g., {FAMILY}-{TYPE}-####"
        />
        <p class="mt-1 text-xs text-pim-muted">
          Use {FAMILY}, {TYPE}, {CATEGORY}, and #### for sequential numbers.
        </p>
      </div>
    </div>
  </div>
</template>
