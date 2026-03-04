<script setup lang="ts">
/**
 * OnboardingWizard - Multi-step onboarding container with split-panel layout.
 *
 * Orchestrates the 12-step SaaS onboarding flow:
 * - Fullscreen modal overlay via OnboardingModal wrapper
 * - Split-panel layout: 55% form panel / 45% live preview panel
 * - 12-step dynamic component routing with animated transitions
 * - Real-time preview updates via useLivePreview composable
 * - Form validation via useStepValidation composable
 * - State management via useOnboardingWizard composable
 * - Responsive: single panel on mobile with preview toggle
 */
import { computed, onMounted, ref, watch, type Component } from 'vue'
import { useRouter } from 'vue-router'

// Composables
import { useOnboardingWizard } from './composables/useOnboardingWizard'
import { useStepValidation } from './composables/useStepValidation'
import { useLivePreview } from './composables/useLivePreview'

// Shared components
import OnboardingModal from './OnboardingModal.vue'
import WizardHeader from './components/WizardHeader.vue'
import WizardFooter from './components/WizardFooter.vue'
import LivePreviewPanel from './components/LivePreviewPanel.vue'
import WizardStepTransition from './components/WizardStepTransition.vue'

// Types
import type {
  WizardStepId,
  StepFormData,
  StepFormDataMap,
  WizardDirection,
} from '@/types'
import { getStepId } from '@/types'

// Step components (eager import for existing steps)
import CompanyInfoStep from './steps/CompanyInfoStep.vue'
import IndustryStep from './steps/IndustryStep.vue'
import ProductStructureStep from './steps/ProductStructureStep.vue'
import AttributeConfigStep from './steps/AttributeConfigStep.vue'
import TaxonomyStep from './steps/TaxonomyStep.vue'
import ChannelStep from './steps/ChannelStep.vue'
import LocalizationStep from './steps/LocalizationStep.vue'
import WorkflowStep from './steps/WorkflowStep.vue'
import ComplianceStep from './steps/ComplianceStep.vue'
import SummaryLaunchStep from './steps/SummaryLaunchStep.vue'

// ============================================================================
// Setup
// ============================================================================

const router = useRouter()
const wizard = useOnboardingWizard()
const validation = useStepValidation()
const livePreview = useLivePreview()

// ============================================================================
// 12-Step Component Registry
// ============================================================================

/**
 * Map wizard step IDs to their Vue components.
 *
 * Existing steps are imported eagerly. Future steps (phase 6) will
 * be added as they are implemented — unmapped steps show a placeholder.
 */
const stepComponents: Partial<Record<WizardStepId, Component>> = {
  company_info: CompanyInfoStep,
  industry_selection: IndustryStep,
  product_structure: ProductStructureStep,
  attribute_config: AttributeConfigStep,
  taxonomy: TaxonomyStep,
  channel_setup: ChannelStep,
  localization: LocalizationStep,
  workflow_preferences: WorkflowStep,
  // quality_scoring: QualityScoringStep,     // Phase 6 — not yet implemented
  // integrations: IntegrationsStep,          // Phase 6 — not yet implemented
  compliance: ComplianceStep,
  summary_launch: SummaryLaunchStep,
}

// ============================================================================
// Navigation Direction
// ============================================================================

/** Direction of the current step transition (for slide animation) */
const direction = ref<WizardDirection>('forward')

// ============================================================================
// Computed
// ============================================================================

/** The currently active step component, or null for unmapped steps */
const activeStepComponent = computed<Component | null>(() => {
  const stepId = wizard.currentStepId.value
  if (!stepId) return null
  return stepComponents[stepId] ?? null
})

/** Current step ID as a string key for transition animations */
const currentStepKey = computed(() => {
  return wizard.currentStepId.value ?? 'loading'
})

/** Whether to show the wizard content (not completed/skipped) */
const showWizard = computed(() => {
  return (
    !wizard.isCompleted.value &&
    wizard.onboardingStatus.value !== 'skipped'
  )
})

/** Current form data for the active step */
const currentFormData = computed<StepFormData | null>(() => {
  const stepId = wizard.currentStepId.value
  if (!stepId) return null
  return wizard.getLocalFormData(stepId)
})

/** Preview panel title (step title or default) */
const previewTitle = computed(() => {
  return wizard.currentStepConfig.value?.title ?? 'Preview'
})

// ============================================================================
// Lifecycle
// ============================================================================

onMounted(async () => {
  await wizard.initialize()

  // Initialize validation and preview for the current step
  if (wizard.currentStepId.value) {
    const stepId = wizard.currentStepId.value
    const data = wizard.getLocalFormData(stepId)
    validation.setActiveStep(stepId, data)
    livePreview.updatePreview(stepId, data)
  }
})

// Redirect to dashboard when onboarding completes
watch(
  () => wizard.isCompleted.value,
  (completed) => {
    if (completed) {
      router.push('/')
    }
  },
)

// Redirect when skipped
watch(
  () => wizard.onboardingStatus.value,
  (status) => {
    if (status === 'skipped') {
      router.push('/')
    }
  },
)

// Update validation and preview when the active step changes
watch(
  () => wizard.currentStepId.value,
  (stepId) => {
    if (stepId) {
      const data = wizard.getLocalFormData(stepId)
      validation.setActiveStep(stepId, data)
      livePreview.updatePreview(stepId, data)
    }
  },
)

// ============================================================================
// Event Handlers
// ============================================================================

/**
 * Handle form data updates from step components (real-time tracking).
 * Updates local state, runs validation, and refreshes the live preview.
 */
function handleStepUpdate(data: StepFormData): void {
  const stepId = wizard.currentStepId.value
  if (!stepId) return

  // Update local form data
  wizard.setLocalFormData(stepId, data as StepFormDataMap[typeof stepId])

  // Validate in real-time
  validation.validateStep(stepId, data as StepFormDataMap[typeof stepId])

  // Update live preview
  livePreview.updatePreview(stepId, data as StepFormDataMap[typeof stepId])
}

/**
 * Handle next step navigation from the footer button.
 * Validates the current step before advancing.
 */
async function handleNext(): Promise<void> {
  const stepId = wizard.currentStepId.value
  if (!stepId) return

  const formData = wizard.getLocalFormData(stepId)

  // Validate before advancing
  const result = validation.validateStep(stepId, formData)
  if (!result.valid) return

  direction.value = 'forward'
  await wizard.goToNext(formData ?? undefined)
}

/**
 * Handle next step from step component emit.
 * The step already validated internally when it emits @next.
 */
async function handleStepNext(formData?: StepFormData): Promise<void> {
  direction.value = 'forward'
  await wizard.goToNext(formData)
}

/**
 * Handle backward navigation.
 */
async function handleBack(): Promise<void> {
  direction.value = 'backward'
  await wizard.goToPrev()
}

/**
 * Skip the current step (only for skippable steps 9-11).
 */
async function handleSkipStep(): Promise<void> {
  direction.value = 'forward'
  await wizard.skipCurrentStep()
}

/**
 * Skip the entire onboarding wizard.
 */
async function handleSkipAll(): Promise<void> {
  await wizard.skipEntireOnboarding()
}

/**
 * Handle clicking a completed step indicator to jump back.
 * Emitted by WizardHeader with the step number (1-based).
 */
function handleStepClick(stepNumber: number): void {
  const targetId = getStepId(stepNumber)
  if (!targetId) return

  direction.value =
    stepNumber < wizard.currentStepNumber.value ? 'backward' : 'forward'
  wizard.goToStep(targetId)
}
</script>

<template>
  <OnboardingModal :visible="true">
    <!-- Loading State -->
    <div
      v-if="wizard.loading.value && !wizard.initialized.value"
      class="flex h-full flex-col items-center justify-center"
    >
      <div
        class="mb-4 h-8 w-8 animate-spin rounded-full border-4 border-primary-600 border-t-transparent"
      />
      <p class="text-pim-muted">Loading your onboarding progress...</p>
    </div>

    <!-- Main Wizard Layout: Split-Panel -->
    <template v-else-if="showWizard">
      <div class="flex h-full w-full flex-col lg:flex-row">
        <!-- ============================================================ -->
        <!-- LEFT PANEL: Form (55% on desktop, full width on mobile)      -->
        <!-- ============================================================ -->
        <div class="flex w-full flex-col overflow-hidden lg:w-[55%]">
          <!-- Wizard Header: Progress bar, step indicators, title -->
          <div class="flex-shrink-0 border-b border-gray-200 px-6 py-4">
            <WizardHeader
              :current-step="wizard.currentStepNumber.value"
              :total-steps="wizard.totalSteps.value"
              :progress-percent="wizard.progressPercent.value"
              :step-title="wizard.currentStepConfig.value?.title ?? ''"
              :step-description="wizard.currentStepConfig.value?.description ?? ''"
              :steps="wizard.wizardSteps.value"
              @step-click="handleStepClick"
            />
          </div>

          <!-- Error Banner -->
          <div
            v-if="wizard.error.value"
            class="mx-6 mt-4 flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3"
          >
            <svg
              class="h-5 w-5 flex-shrink-0 text-red-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p class="flex-1 text-sm text-red-700">{{ wizard.error.value }}</p>
            <button
              class="text-sm font-medium text-red-600 hover:text-red-800"
              @click="wizard.clearError()"
            >
              Dismiss
            </button>
          </div>

          <!-- Step Content (with slide transition) -->
          <div class="flex-1 overflow-y-auto px-6 py-6">
            <WizardStepTransition
              :direction="direction"
              :step-key="currentStepKey"
            >
              <!-- Dynamic Step Component -->
              <component
                v-if="activeStepComponent"
                :is="activeStepComponent"
                :data="currentFormData ?? {}"
                :loading="wizard.loading.value"
                @update="handleStepUpdate"
                @next="handleStepNext"
                @back="handleBack"
              />

              <!-- Placeholder for unmapped steps (future phase 6 components) -->
              <div
                v-else
                class="flex flex-col items-center justify-center py-12 text-center"
              >
                <svg
                  class="mb-3 h-10 w-10 text-gray-300"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                  />
                </svg>
                <p class="text-sm font-medium text-pim-muted">
                  {{ wizard.currentStepConfig.value?.title ?? 'Step' }} is being
                  prepared...
                </p>
                <p class="mt-1 text-xs text-gray-400">
                  This step will be available soon.
                </p>
              </div>
            </WizardStepTransition>
          </div>

          <!-- Wizard Footer: Navigation buttons -->
          <div class="flex-shrink-0 border-t border-gray-200 px-6 py-4">
            <WizardFooter
              :is-first-step="wizard.isFirstStep.value"
              :is-last-step="wizard.isLastStep.value"
              :can-skip-step="wizard.canSkipCurrentStep.value"
              :loading="wizard.loading.value"
              :is-applying="wizard.isApplying.value"
              :next-disabled="!validation.isValid.value"
              @next="handleNext"
              @back="handleBack"
              @skip="handleSkipStep"
              @skip-all="handleSkipAll"
            />
          </div>
        </div>

        <!-- ============================================================ -->
        <!-- RIGHT PANEL: Live Preview (45% on desktop, mobile overlay)   -->
        <!-- ============================================================ -->
        <LivePreviewPanel
          :step-title="previewTitle"
          :has-preview="livePreview.hasPreview.value"
          :loading="wizard.loading.value"
        >
          <!-- Preview content slot: step-specific preview components
               will be added in Phase 7 (Preview Components).
               For now, render a formatted preview data summary. -->
          <div
            v-if="livePreview.previewData.value"
            class="space-y-4"
          >
            <!-- Structured preview data display -->
            <div
              v-for="(value, key) in livePreview.previewData.value"
              :key="key"
              class="rounded-lg border border-gray-100 bg-white p-3"
            >
              <dt class="mb-1 text-xs font-medium uppercase tracking-wider text-pim-muted">
                {{ String(key).replace(/_/g, ' ') }}
              </dt>
              <dd class="text-sm text-pim-text">
                <template v-if="Array.isArray(value)">
                  <span v-if="value.length === 0" class="text-gray-400">None</span>
                  <div v-else class="flex flex-wrap gap-1">
                    <span
                      v-for="(item, idx) in value.slice(0, 8)"
                      :key="idx"
                      class="rounded-full bg-primary-50 px-2 py-0.5 text-xs text-primary-700"
                    >
                      {{ typeof item === 'object' ? (item as Record<string, unknown>).name ?? (item as Record<string, unknown>).label ?? JSON.stringify(item) : item }}
                    </span>
                    <span
                      v-if="value.length > 8"
                      class="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-500"
                    >
                      +{{ value.length - 8 }} more
                    </span>
                  </div>
                </template>
                <template v-else-if="typeof value === 'boolean'">
                  <span :class="value ? 'text-green-600' : 'text-gray-400'">
                    {{ value ? 'Yes' : 'No' }}
                  </span>
                </template>
                <template v-else-if="typeof value === 'object' && value !== null">
                  <span class="text-xs text-gray-500">{{ Object.keys(value).length }} items</span>
                </template>
                <template v-else>
                  <span :class="{ 'text-gray-400': !value }">
                    {{ value || 'Not set' }}
                  </span>
                </template>
              </dd>
            </div>
          </div>
        </LivePreviewPanel>
      </div>
    </template>

    <!-- Completion Redirect (transient state before redirect) -->
    <div
      v-else
      class="flex h-full flex-col items-center justify-center"
    >
      <div
        class="mb-4 h-8 w-8 animate-spin rounded-full border-4 border-green-500 border-t-transparent"
      />
      <p class="text-pim-muted">Setting up your workspace...</p>
    </div>
  </OnboardingModal>
</template>
