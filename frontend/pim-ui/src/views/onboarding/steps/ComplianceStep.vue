<script setup lang="ts">
/**
 * ComplianceStep - Configure regulatory compliance requirements.
 *
 * Collects:
 * - Required regulatory standards
 * - Certification requirements
 * - Safety warning preferences
 */
import { reactive, watch } from 'vue'
import type { ComplianceSetupData, StepFormData } from '@/types'

const props = defineProps<{
  data: Record<string, unknown>
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update', data: StepFormData): void
  (e: 'next', data: StepFormData): void
  (e: 'back'): void
}>()

const REGULATORY_STANDARDS = [
  { value: 'ce', label: 'CE Marking', description: 'European conformity for health, safety, and environment' },
  { value: 'fda', label: 'FDA', description: 'US Food and Drug Administration regulations' },
  { value: 'reach', label: 'REACH', description: 'EU regulation on chemicals and their safe use' },
  { value: 'rohs', label: 'RoHS', description: 'Restriction of hazardous substances in electronics' },
  { value: 'iso9001', label: 'ISO 9001', description: 'Quality management systems' },
  { value: 'iso14001', label: 'ISO 14001', description: 'Environmental management systems' },
  { value: 'gots', label: 'GOTS', description: 'Global Organic Textile Standard' },
  { value: 'oeko_tex', label: 'OEKO-TEX', description: 'Textile product safety testing and certification' },
] as const

const CERTIFICATION_OPTIONS = [
  { value: 'organic', label: 'Organic' },
  { value: 'fair_trade', label: 'Fair Trade' },
  { value: 'kosher', label: 'Kosher' },
  { value: 'halal', label: 'Halal' },
  { value: 'vegan', label: 'Vegan' },
  { value: 'cruelty_free', label: 'Cruelty-Free' },
  { value: 'recycled', label: 'Recycled Materials' },
  { value: 'energy_star', label: 'Energy Star' },
] as const

const form = reactive<ComplianceSetupData>({
  regulatory_standards: (props.data.regulatory_standards as string[]) ?? [],
  certifications_required: (props.data.certifications_required as string[]) ?? [],
  enable_safety_warnings: (props.data.enable_safety_warnings as boolean) ?? false,
})

/** Toggle a regulatory standard */
function toggleStandard(standard: string): void {
  if (!form.regulatory_standards) {
    form.regulatory_standards = []
  }
  const idx = form.regulatory_standards.indexOf(standard)
  if (idx >= 0) {
    form.regulatory_standards.splice(idx, 1)
  } else {
    form.regulatory_standards.push(standard)
  }
}

/** Toggle a certification */
function toggleCertification(cert: string): void {
  if (!form.certifications_required) {
    form.certifications_required = []
  }
  const idx = form.certifications_required.indexOf(cert)
  if (idx >= 0) {
    form.certifications_required.splice(idx, 1)
  } else {
    form.certifications_required.push(cert)
  }
}

/** Check if a standard is selected */
function isStandardSelected(standard: string): boolean {
  return form.regulatory_standards?.includes(standard) ?? false
}

/** Check if a certification is selected */
function isCertSelected(cert: string): boolean {
  return form.certifications_required?.includes(cert) ?? false
}

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
    <!-- Regulatory Standards -->
    <div>
      <label class="mb-3 block text-sm font-medium text-pim-text">
        Applicable Regulatory Standards
      </label>
      <p class="mb-3 text-xs text-pim-muted">
        Select standards that apply to your products. This will add required compliance
        fields and quality rules.
      </p>
      <div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
        <button
          v-for="standard in REGULATORY_STANDARDS"
          :key="standard.value"
          class="flex items-start gap-3 rounded-lg border p-3 text-left transition-all duration-200"
          :class="
            isStandardSelected(standard.value)
              ? 'border-primary-500 bg-primary-50'
              : 'border-pim-border hover:border-gray-300'
          "
          @click="toggleStandard(standard.value)"
        >
          <div
            class="mt-0.5 flex h-4 w-4 flex-shrink-0 items-center justify-center rounded border"
            :class="
              isStandardSelected(standard.value)
                ? 'border-primary-600 bg-primary-600'
                : 'border-pim-border'
            "
          >
            <svg
              v-if="isStandardSelected(standard.value)"
              class="h-3 w-3 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-pim-text">{{ standard.label }}</p>
            <p class="text-xs text-pim-muted">{{ standard.description }}</p>
          </div>
        </button>
      </div>
    </div>

    <!-- Certifications -->
    <div>
      <label class="mb-2 block text-sm font-medium text-pim-text">
        Product Certifications
      </label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="cert in CERTIFICATION_OPTIONS"
          :key="cert.value"
          class="rounded-full border px-3 py-1.5 text-sm transition-all duration-200"
          :class="
            isCertSelected(cert.value)
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-pim-border text-pim-muted hover:border-gray-300'
          "
          @click="toggleCertification(cert.value)"
        >
          {{ cert.label }}
        </button>
      </div>
    </div>

    <!-- Safety Warnings -->
    <div class="rounded-lg border border-pim-border p-4">
      <div class="flex items-start gap-3">
        <input
          id="enable_safety_warnings"
          v-model="form.enable_safety_warnings"
          type="checkbox"
          class="mt-0.5 h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
        />
        <div class="flex-1">
          <label class="block text-sm font-medium text-pim-text" for="enable_safety_warnings">
            Enable Safety Warnings
          </label>
          <p class="mt-0.5 text-xs text-pim-muted">
            Require safety warning attributes for applicable products
            (e.g., choking hazards, allergen information, chemical warnings).
          </p>
        </div>
      </div>
    </div>

    <!-- Info callout -->
    <div class="flex items-start gap-2 rounded-lg bg-amber-50 p-3">
      <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xs text-amber-700">
        Compliance requirements create mandatory quality rules. Products missing
        required compliance data will have reduced quality scores. You can skip this
        step if compliance is not relevant to your products.
      </p>
    </div>
  </div>
</template>
