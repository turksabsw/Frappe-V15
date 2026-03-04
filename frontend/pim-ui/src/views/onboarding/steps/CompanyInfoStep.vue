<script setup lang="ts">
/**
 * CompanyInfoStep - First onboarding step for company information.
 *
 * Collects:
 * - Company name (required)
 * - Company website
 * - Company size (required)
 * - Primary role (required)
 * - Existing systems (required, multi-select)
 * - Pain points (optional, multi-select)
 *
 * Integrates with the onboarding store to:
 * - Read/write step data via Pinia store
 * - Expose isValid for wizard navigation control
 */
import { reactive, watch, onMounted } from 'vue'
import { useOnboardingStore } from '@/stores/onboarding'
import type { CompanyInfoData, StepFormData, CompanySize, PrimaryRole } from '@/types'

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

const COMPANY_SIZES: readonly { value: CompanySize; label: string }[] = [
  { value: '1-10', label: '1 - 10 employees' },
  { value: '11-50', label: '11 - 50 employees' },
  { value: '51-200', label: '51 - 200 employees' },
  { value: '201-500', label: '201 - 500 employees' },
  { value: '501-1000', label: '501 - 1,000 employees' },
  { value: '1000+', label: '1,000+ employees' },
] as const

const PRIMARY_ROLES: readonly { value: PrimaryRole; label: string }[] = [
  { value: 'Product Manager', label: 'Product Manager' },
  { value: 'Catalog Manager', label: 'Catalog Manager' },
  { value: 'E-Commerce Manager', label: 'E-Commerce Manager' },
  { value: 'IT Administrator', label: 'IT Administrator' },
  { value: 'Marketing Manager', label: 'Marketing Manager' },
  { value: 'Operations Manager', label: 'Operations Manager' },
  { value: 'Business Owner', label: 'Business Owner' },
  { value: 'Other', label: 'Other' },
] as const

const EXISTING_SYSTEMS = [
  { value: 'excel', label: 'Excel / Spreadsheets' },
  { value: 'erp', label: 'ERP System (SAP, Oracle, etc.)' },
  { value: 'erpnext', label: 'ERPNext' },
  { value: 'legacy_pim', label: 'Legacy PIM System' },
  { value: 'custom_db', label: 'Custom Database' },
  { value: 'ecommerce', label: 'E-Commerce Platform' },
  { value: 'none', label: 'No Existing System' },
] as const

const PAIN_POINTS = [
  { value: 'data_inconsistency', label: 'Data inconsistency across channels' },
  { value: 'slow_time_to_market', label: 'Slow time-to-market for products' },
  { value: 'manual_data_entry', label: 'Too much manual data entry' },
  { value: 'poor_data_quality', label: 'Poor product data quality' },
  { value: 'channel_sync', label: 'Difficulty syncing across channels' },
  { value: 'compliance', label: 'Compliance & regulatory challenges' },
  { value: 'scalability', label: 'Cannot scale current process' },
] as const

/** Load initial data from store or props */
function getInitialData(): CompanyInfoData {
  const storeData = store.getWizardStepData('company_info')
  const source = storeData ?? props.data

  return {
    company_name: (source?.company_name as string) ?? '',
    company_website: (source?.company_website as string) ?? '',
    company_size: (source?.company_size as CompanySize) ?? ('' as CompanySize),
    primary_role: (source?.primary_role as PrimaryRole) ?? ('' as PrimaryRole),
    existing_systems: (source?.existing_systems as string[]) ?? [],
    pain_points: (source?.pain_points as string[]) ?? [],
  }
}

const form = reactive<CompanyInfoData>(getInitialData())

/** Sync initial data to store on mount */
onMounted(() => {
  store.setWizardStepData('company_info', { ...form })
})

/** Toggle a value in an array field */
function toggleArrayItem(field: 'existing_systems' | 'pain_points', value: string): void {
  const arr = form[field] ?? []
  const index = arr.indexOf(value)
  if (index >= 0) {
    arr.splice(index, 1)
  } else {
    arr.push(value)
  }
  form[field] = [...arr]
}

/** Emit form data changes to parent and sync to store */
watch(
  form,
  (newVal) => {
    const data = { ...newVal }
    store.setWizardStepData('company_info', data)
    emit('update', data)
  },
  { deep: true },
)

/** Whether the form has the minimum required data */
function isValid(): boolean {
  return (
    form.company_name.trim().length > 0 &&
    !!form.company_size &&
    !!form.primary_role &&
    form.existing_systems.length > 0
  )
}

function handleSubmit(): void {
  if (isValid()) {
    emit('next', { ...form })
  }
}

defineExpose({ isValid })
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

    <!-- Company Website -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="company_website">
        Website
      </label>
      <input
        id="company_website"
        v-model="form.company_website"
        type="url"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
        placeholder="https://www.example.com"
      />
    </div>

    <!-- Company Size -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="company_size">
        Company Size <span class="text-red-500">*</span>
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

    <!-- Primary Role -->
    <div>
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="primary_role">
        Your Primary Role <span class="text-red-500">*</span>
      </label>
      <select
        id="primary_role"
        v-model="form.primary_role"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
      >
        <option value="">Select your role</option>
        <option
          v-for="role in PRIMARY_ROLES"
          :key="role.value"
          :value="role.value"
        >
          {{ role.label }}
        </option>
      </select>
    </div>

    <!-- Existing Systems -->
    <div>
      <label class="mb-2 block text-sm font-medium text-pim-text">
        Current Systems <span class="text-red-500">*</span>
      </label>
      <p class="mb-2 text-xs text-pim-muted">
        What systems do you currently use to manage product data?
      </p>
      <div class="space-y-2">
        <label
          v-for="system in EXISTING_SYSTEMS"
          :key="system.value"
          class="flex cursor-pointer items-center gap-2.5 rounded-lg border border-pim-border px-3 py-2.5 transition-colors hover:bg-pim-surface"
          :class="{
            'border-primary-500 bg-primary-50': form.existing_systems.includes(system.value),
          }"
        >
          <input
            type="checkbox"
            :checked="form.existing_systems.includes(system.value)"
            class="h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
            @change="toggleArrayItem('existing_systems', system.value)"
          />
          <span class="text-sm text-pim-text">{{ system.label }}</span>
        </label>
      </div>
    </div>

    <!-- Pain Points -->
    <div>
      <label class="mb-2 block text-sm font-medium text-pim-text">
        Key Challenges
      </label>
      <p class="mb-2 text-xs text-pim-muted">
        What are your biggest product data management challenges? (optional)
      </p>
      <div class="space-y-2">
        <label
          v-for="point in PAIN_POINTS"
          :key="point.value"
          class="flex cursor-pointer items-center gap-2.5 rounded-lg border border-pim-border px-3 py-2.5 transition-colors hover:bg-pim-surface"
          :class="{
            'border-primary-500 bg-primary-50': (form.pain_points ?? []).includes(point.value),
          }"
        >
          <input
            type="checkbox"
            :checked="(form.pain_points ?? []).includes(point.value)"
            class="h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
            @change="toggleArrayItem('pain_points', point.value)"
          />
          <span class="text-sm text-pim-text">{{ point.label }}</span>
        </label>
      </div>
    </div>

    <!-- Validation hint -->
    <p v-if="!isValid()" class="text-xs text-amber-600">
      Please fill in company name, size, role, and select at least one existing system.
    </p>
  </div>
</template>
