<script setup lang="ts">
/**
 * WorkflowStep - Configure approval workflows and sync preferences.
 *
 * Collects:
 * - Whether product changes require approval
 * - Auto-sync to ERPNext toggle
 * - Sync direction (PIM Master, ERP Master, Bidirectional)
 * - Quality scoring toggle
 */
import { reactive, watch } from 'vue'
import type { WorkflowPreferencesData, StepFormData } from '@/types'

const props = defineProps<{
  data: Record<string, unknown>
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update', data: StepFormData): void
  (e: 'next', data: StepFormData): void
  (e: 'back'): void
}>()

const SYNC_DIRECTIONS = [
  {
    value: 'PIM Master',
    label: 'PIM Master',
    description: 'PIM is the source of truth. Changes flow from PIM to ERPNext.',
  },
  {
    value: 'ERP Master',
    label: 'ERP Master',
    description: 'ERPNext is the source of truth. Changes flow from ERPNext to PIM.',
  },
  {
    value: 'Bidirectional',
    label: 'Bidirectional',
    description: 'Changes sync both ways with conflict detection.',
  },
] as const

const form = reactive<WorkflowPreferencesData>({
  require_approval: (props.data.require_approval as boolean) ?? false,
  auto_sync_to_erp: (props.data.auto_sync_to_erp as boolean) ?? true,
  sync_direction: (props.data.sync_direction as WorkflowPreferencesData['sync_direction']) ?? 'PIM Master',
  enable_quality_scoring: (props.data.enable_quality_scoring as boolean) ?? true,
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
    <!-- Approval Workflow -->
    <div class="rounded-lg border border-pim-border p-4">
      <div class="flex items-start gap-3">
        <input
          id="require_approval"
          v-model="form.require_approval"
          type="checkbox"
          class="mt-0.5 h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
        />
        <div class="flex-1">
          <label class="block text-sm font-medium text-pim-text" for="require_approval">
            Require Approval for Product Changes
          </label>
          <p class="mt-0.5 text-xs text-pim-muted">
            Product updates will go through an approval workflow before becoming active.
            A PIM Manager must approve changes made by PIM Users.
          </p>
        </div>
      </div>
    </div>

    <!-- Quality Scoring -->
    <div class="rounded-lg border border-pim-border p-4">
      <div class="flex items-start gap-3">
        <input
          id="enable_quality_scoring"
          v-model="form.enable_quality_scoring"
          type="checkbox"
          class="mt-0.5 h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
        />
        <div class="flex-1">
          <label class="block text-sm font-medium text-pim-text" for="enable_quality_scoring">
            Enable Data Quality Scoring
          </label>
          <p class="mt-0.5 text-xs text-pim-muted">
            Automatically calculate completeness and quality scores for each product
            based on filled attributes, description quality, and image requirements.
          </p>
        </div>
      </div>
    </div>

    <!-- ERPNext Sync Section -->
    <div class="space-y-4">
      <h3 class="text-sm font-medium text-pim-text">ERPNext Integration</h3>

      <!-- Auto Sync Toggle -->
      <div class="rounded-lg border border-pim-border p-4">
        <div class="flex items-start gap-3">
          <input
            id="auto_sync_to_erp"
            v-model="form.auto_sync_to_erp"
            type="checkbox"
            class="mt-0.5 h-4 w-4 rounded border-pim-border text-primary-600 focus:ring-primary-500"
          />
          <div class="flex-1">
            <label class="block text-sm font-medium text-pim-text" for="auto_sync_to_erp">
              Auto-sync to ERPNext
            </label>
            <p class="mt-0.5 text-xs text-pim-muted">
              Automatically synchronize product data with ERPNext Item DocType
              when products are created or updated.
            </p>
          </div>
        </div>
      </div>

      <!-- Sync Direction -->
      <div v-if="form.auto_sync_to_erp">
        <label class="mb-2 block text-sm font-medium text-pim-text">
          Sync Direction
        </label>
        <div class="space-y-2">
          <label
            v-for="direction in SYNC_DIRECTIONS"
            :key="direction.value"
            class="flex cursor-pointer items-start gap-3 rounded-lg border border-pim-border px-4 py-3 transition-colors hover:bg-pim-surface"
            :class="{
              'border-primary-500 bg-primary-50': form.sync_direction === direction.value,
            }"
          >
            <input
              v-model="form.sync_direction"
              type="radio"
              :value="direction.value"
              class="mt-0.5 h-4 w-4 border-pim-border text-primary-600 focus:ring-primary-500"
            />
            <div>
              <p class="text-sm font-medium text-pim-text">{{ direction.label }}</p>
              <p class="text-xs text-pim-muted">{{ direction.description }}</p>
            </div>
          </label>
        </div>
      </div>
    </div>

    <!-- Info callout -->
    <div class="flex items-start gap-2 rounded-lg bg-pim-surface p-3">
      <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xs text-pim-muted">
        All workflow settings can be adjusted later in PIM Settings.
        The sync direction determines which system takes priority during conflicts.
      </p>
    </div>
  </div>
</template>
