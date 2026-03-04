<script setup lang="ts">
/**
 * ComplianceListPreview - Live preview for Step 11 (Compliance).
 *
 * Renders a compliance checklist showing:
 * - Enabled compliance standards with descriptions
 * - Certification tracking toggle status
 * - Total standards count badge
 * - Visual checklist with enable/disable indicators
 *
 * Updates in real time as the user configures compliance settings.
 * Receives transformed preview data from useLivePreview composable.
 */
import { computed } from 'vue'
import type { ComplianceListPreviewData, ComplianceStandardPreview } from '@/types'

// ============================================================================
// Props
// ============================================================================

const props = defineProps<{
  data: ComplianceListPreviewData
}>()

// ============================================================================
// Display Helpers
// ============================================================================

/** Compliance standard category colors keyed by standard ID */
const STANDARD_META: Record<string, {
  category: string
  color: string
  bgColor: string
}> = {
  iso_9001: { category: 'Quality', color: 'text-blue-600', bgColor: 'bg-blue-50' },
  iso_14001: { category: 'Environmental', color: 'text-green-600', bgColor: 'bg-green-50' },
  gdpr: { category: 'Data Privacy', color: 'text-purple-600', bgColor: 'bg-purple-50' },
  reach: { category: 'Chemical Safety', color: 'text-orange-600', bgColor: 'bg-orange-50' },
  rohs: { category: 'Safety', color: 'text-red-600', bgColor: 'bg-red-50' },
  ce_marking: { category: 'Conformity', color: 'text-indigo-600', bgColor: 'bg-indigo-50' },
  fda: { category: 'Health & Safety', color: 'text-teal-600', bgColor: 'bg-teal-50' },
  textile_labeling: { category: 'Labeling', color: 'text-pink-600', bgColor: 'bg-pink-50' },
  cpsia: { category: 'Consumer Safety', color: 'text-amber-600', bgColor: 'bg-amber-50' },
  prop65: { category: 'Warning', color: 'text-yellow-600', bgColor: 'bg-yellow-50' },
}

/** Default standard metadata */
const DEFAULT_STANDARD = {
  category: 'Standard',
  color: 'text-gray-600',
  bgColor: 'bg-gray-50',
}

/** Whether there is any compliance data to display */
const hasContent = computed(() => {
  return props.data.standards.length > 0 || props.data.certification_tracking
})

/** Get metadata for a compliance standard */
function getStandardMeta(id: string): { category: string; color: string; bgColor: string } {
  return STANDARD_META[id] ?? DEFAULT_STANDARD
}
</script>

<template>
  <div class="space-y-4">
    <!-- Summary Badge -->
    <div v-if="hasContent" class="flex items-center justify-center">
      <span
        class="inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium"
        :class="data.total_standards > 0 ? 'bg-indigo-50 text-indigo-700' : 'bg-gray-50 text-gray-600'"
      >
        <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        {{ data.total_standards }} Compliance {{ data.total_standards === 1 ? 'Standard' : 'Standards' }}
      </span>
    </div>

    <!-- Standards Checklist -->
    <div v-if="data.standards.length > 0" class="rounded-xl border border-gray-200 bg-white shadow-sm">
      <div class="border-b border-gray-100 px-4 py-3">
        <h4 class="text-xs font-medium uppercase tracking-wider text-pim-muted">
          Active Standards
        </h4>
      </div>

      <div class="divide-y divide-gray-50">
        <div
          v-for="standard in data.standards"
          :key="standard.id"
          class="flex items-start gap-3 px-4 py-3"
        >
          <!-- Check Icon -->
          <div
            class="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded"
            :class="standard.enabled ? 'bg-green-100' : 'bg-gray-100'"
          >
            <svg
              v-if="standard.enabled"
              class="h-3 w-3 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
            <div v-else class="h-1.5 w-1.5 rounded-full bg-gray-300" />
          </div>

          <!-- Standard Info -->
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium text-pim-text">
                {{ standard.label }}
              </span>
              <span
                class="rounded-full px-2 py-0.5 text-[10px] font-medium"
                :class="[getStandardMeta(standard.id).bgColor, getStandardMeta(standard.id).color]"
              >
                {{ getStandardMeta(standard.id).category }}
              </span>
            </div>
            <p class="mt-0.5 text-xs text-pim-muted">
              {{ standard.description }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Certification Tracking -->
    <div
      v-if="hasContent"
      class="rounded-lg border bg-white p-4"
      :class="data.certification_tracking ? 'border-green-200' : 'border-gray-100'"
    >
      <div class="flex items-center gap-3">
        <!-- Icon -->
        <div
          class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg"
          :class="data.certification_tracking ? 'bg-green-100' : 'bg-gray-100'"
        >
          <svg
            class="h-4.5 w-4.5"
            :class="data.certification_tracking ? 'text-green-600' : 'text-gray-400'"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>

        <!-- Info -->
        <div class="flex-1">
          <h3
            class="text-sm font-medium"
            :class="data.certification_tracking ? 'text-pim-text' : 'text-gray-400'"
          >
            Certification Tracking
          </h3>
          <p class="text-xs text-pim-muted">
            {{ data.certification_tracking
              ? 'Track certification expiry dates and renewal reminders'
              : 'Certification tracking is not enabled'
            }}
          </p>
        </div>

        <!-- Toggle Visual -->
        <div
          class="h-5 w-9 flex-shrink-0 rounded-full transition-colors"
          :class="data.certification_tracking ? 'bg-green-400' : 'bg-gray-200'"
        >
          <div
            class="h-5 w-5 rounded-full bg-white shadow-sm transition-transform"
            :class="data.certification_tracking ? 'translate-x-4' : 'translate-x-0'"
          />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-if="!hasContent"
      class="flex flex-col items-center justify-center py-8 text-center"
    >
      <svg
        class="mb-2 h-8 w-8 text-gray-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="1.5"
          d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
        />
      </svg>
      <p class="text-sm text-pim-muted">Configure compliance standards to see the checklist</p>
    </div>
  </div>
</template>
