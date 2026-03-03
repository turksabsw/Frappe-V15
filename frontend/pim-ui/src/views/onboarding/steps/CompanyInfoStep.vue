<script setup lang="ts">
/**
 * CompanyInfoStep - First onboarding step for company information.
 *
 * Collects:
 * - Company name (required)
 * - Industry vertical
 * - Company size
 * - Country
 * - Currency
 * - Website URL
 */
import { reactive, watch } from 'vue'
import type { CompanyInfoData, StepFormData } from '@/types'

const props = defineProps<{
  data: Record<string, unknown>
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update', data: StepFormData): void
  (e: 'next', data: StepFormData): void
  (e: 'back'): void
}>()

const COMPANY_SIZES = [
  { value: 'small', label: 'Small (1-50 employees)' },
  { value: 'medium', label: 'Medium (51-200 employees)' },
  { value: 'large', label: 'Large (201-1000 employees)' },
  { value: 'enterprise', label: 'Enterprise (1000+ employees)' },
] as const

const form = reactive<CompanyInfoData>({
  company_name: (props.data.company_name as string) ?? '',
  industry: (props.data.industry as string) ?? '',
  company_size: (props.data.company_size as CompanyInfoData['company_size']) ?? undefined,
  country: (props.data.country as string) ?? '',
  currency: (props.data.currency as string) ?? '',
  website: (props.data.website as string) ?? '',
})

/** Emit form data changes to parent for draft persistence */
watch(
  form,
  (newVal) => {
    emit('update', { ...newVal })
  },
  { deep: true },
)

/** Whether the form has the minimum required data */
function isValid(): boolean {
  return form.company_name.trim().length > 0
}

function handleSubmit(): void {
  if (isValid()) {
    emit('next', { ...form })
  }
}
</script>

<template>
  <div class="space-y-5">
    <!-- Company Name -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="company_name">
        Company Name <span class="text-red-500">*</span>
      </label>
      <input
        id="company_name"
        v-model="form.company_name"
        type="text"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
        placeholder="Enter your company name"
      />
    </div>

    <!-- Industry -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="industry">
        Industry
      </label>
      <input
        id="industry"
        v-model="form.industry"
        type="text"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
        placeholder="e.g., Fashion, Electronics, Food & Beverage"
      />
    </div>

    <!-- Company Size -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="company_size">
        Company Size
      </label>
      <select
        id="company_size"
        v-model="form.company_size"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
      >
        <option value="">Select company size</option>
        <option
          v-for="size in COMPANY_SIZES"
          :key="size.value"
          :value="size.value"
        >
          {{ size.label }}
        </option>
      </select>
    </div>

    <!-- Country & Currency (side by side) -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div>
        <label class="mb-1.5 block text-sm font-medium text-pim-text" for="country">
          Country
        </label>
        <input
          id="country"
          v-model="form.country"
          type="text"
          class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          placeholder="e.g., United States"
        />
      </div>
      <div>
        <label class="mb-1.5 block text-sm font-medium text-pim-text" for="currency">
          Currency
        </label>
        <input
          id="currency"
          v-model="form.currency"
          type="text"
          class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          placeholder="e.g., USD"
        />
      </div>
    </div>

    <!-- Website -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="website">
        Website
      </label>
      <input
        id="website"
        v-model="form.website"
        type="url"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
        placeholder="https://www.example.com"
      />
    </div>

    <!-- Validation hint -->
    <p v-if="!isValid()" class="text-xs text-amber-600">
      Please enter your company name to continue.
    </p>
  </div>
</template>
