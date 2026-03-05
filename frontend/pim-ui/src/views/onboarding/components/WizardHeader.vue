<script setup lang="ts">
/**
 * WizardHeader - Onboarding wizard header with progress bar and step info.
 *
 * Displays:
 * - Step counter (e.g., "Step 3 of 12")
 * - Progress percentage
 * - Animated progress bar
 * - Current step title and description
 * - Clickable step indicators for completed steps
 *
 * Used at the top of the split-panel wizard layout to give users
 * clear visual feedback about their position in the 12-step flow.
 */
import { computed } from 'vue'
import type { WizardStepConfig, StepStatus } from '@/types'

// ============================================================================
// Props
// ============================================================================

export interface WizardHeaderProps {
  /** Current step number (1-12) */
  currentStep: number
  /** Total number of steps */
  totalSteps: number
  /** Progress percentage (0-100) */
  progressPercent: number
  /** Current step title */
  stepTitle: string
  /** Current step description */
  stepDescription?: string
  /** All wizard steps with their current status */
  steps: Array<WizardStepConfig & { status: StepStatus }>
}

const props = withDefaults(defineProps<WizardHeaderProps>(), {
  stepDescription: '',
})

// ============================================================================
// Emits
// ============================================================================

const emit = defineEmits<{
  /** Emitted when a completed step indicator is clicked */
  (e: 'step-click', stepNumber: number): void
}>()

// ============================================================================
// Computed
// ============================================================================

/** Formatted step counter label */
const stepCounterLabel = computed(() => {
  return `Step ${props.currentStep} of ${props.totalSteps}`
})

/** Formatted progress label */
const progressLabel = computed(() => {
  return `${Math.round(props.progressPercent)}%`
})

/** Progress bar width style */
const progressBarStyle = computed(() => ({
  width: `${props.progressPercent}%`,
}))

// ============================================================================
// Handlers
// ============================================================================

/**
 * Handle click on a step indicator.
 * Only emits for completed or skipped steps (allows jumping back).
 */
function handleStepClick(step: WizardStepConfig & { status: StepStatus }): void {
  if (step.status === 'completed' || step.status === 'skipped') {
    emit('step-click', step.number)
  }
}

/**
 * Get CSS classes for a step indicator based on its status.
 */
function getStepIndicatorClasses(step: WizardStepConfig & { status: StepStatus }): Record<string, boolean> {
  return {
    'bg-primary-600 text-white shadow-md': step.status === 'active',
    'bg-green-500 text-white cursor-pointer hover:bg-green-600': step.status === 'completed',
    'bg-amber-400 text-white cursor-pointer hover:bg-amber-500': step.status === 'skipped',
    'bg-gray-200 text-pim-muted cursor-default': step.status === 'pending',
    'bg-red-400 text-white': step.status === 'error',
  }
}

/**
 * Whether a step indicator should be disabled (not clickable).
 */
function isStepDisabled(step: WizardStepConfig & { status: StepStatus }): boolean {
  return step.status === 'pending' || step.status === 'active'
}

/**
 * Get connector line classes between step indicators.
 */
function getConnectorClasses(index: number): string {
  const step = props.steps[index]
  if (step?.status === 'completed' || step?.status === 'skipped') {
    return 'bg-green-400'
  }
  return 'bg-gray-200'
}
</script>

<template>
  <div class="wizard-header">
    <!-- Progress Counter Row -->
    <div class="mb-2 flex items-center justify-between text-sm text-pim-muted">
      <span class="font-medium">{{ stepCounterLabel }}</span>
      <span>{{ progressLabel }}</span>
    </div>

    <!-- Progress Bar -->
    <div class="mb-4 h-2 w-full overflow-hidden rounded-full bg-gray-200">
      <div
        class="h-2 rounded-full bg-primary-600 transition-all duration-500 ease-out"
        :style="progressBarStyle"
      />
    </div>

    <!-- Step Indicators (visible on desktop, hidden on mobile) -->
    <div class="mb-4 hidden items-center justify-between sm:flex">
      <template v-for="(step, index) in steps" :key="step.id">
        <!-- Step Dot -->
        <button
          class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full text-xs font-medium transition-all duration-200"
          :class="getStepIndicatorClasses(step)"
          :disabled="isStepDisabled(step)"
          :title="step.title"
          :aria-label="`Step ${step.number}: ${step.title} (${step.status})`"
          :aria-current="step.status === 'active' ? 'step' : undefined"
          @click="handleStepClick(step)"
        >
          <!-- Checkmark for completed steps -->
          <svg
            v-if="step.status === 'completed'"
            class="h-3.5 w-3.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          </svg>
          <!-- Dash for skipped steps -->
          <svg
            v-else-if="step.status === 'skipped'"
            class="h-3.5 w-3.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 12h14" />
          </svg>
          <!-- Step number for active/pending/error -->
          <span v-else>{{ step.number }}</span>
        </button>

        <!-- Connector Line -->
        <div
          v-if="index < steps.length - 1"
          class="mx-0.5 h-px flex-1 transition-colors duration-200"
          :class="getConnectorClasses(index)"
        />
      </template>
    </div>

    <!-- Step Title and Description -->
    <div class="mb-2">
      <h2 class="text-xl font-semibold text-pim-text">{{ stepTitle }}</h2>
      <p v-if="stepDescription" class="mt-1 text-sm text-pim-muted">
        {{ stepDescription }}
      </p>
    </div>
  </div>
</template>
