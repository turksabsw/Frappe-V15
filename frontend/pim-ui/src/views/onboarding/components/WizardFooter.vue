<script setup lang="ts">
/**
 * WizardFooter - Navigation buttons for the onboarding wizard.
 *
 * Renders Back, Next, Skip, and Finish buttons with conditional visibility:
 * - Back button: hidden on step 1, shown on all other steps
 * - Skip button: shown only for skippable steps (9-11) after step 8
 * - Next button: shown on steps 1-11 (non-final steps)
 * - Finish/Launch button: shown on step 12 (final step)
 * - Loading spinner on primary button during API operations
 *
 * Also includes a "Skip Entire Wizard" link for users who want to
 * bypass onboarding entirely (shown on the first step only).
 */

// ============================================================================
// Props
// ============================================================================

export interface WizardFooterProps {
  /** Whether the wizard is on the first step */
  isFirstStep: boolean
  /** Whether the wizard is on the last step */
  isLastStep: boolean
  /** Whether the current step can be skipped */
  canSkipStep: boolean
  /** Whether an API operation is in progress */
  loading: boolean
  /** Whether template application is in progress */
  isApplying?: boolean
  /** Label for the primary (Next) button — overrides default */
  nextLabel?: string
  /** Label for the Back button — overrides default */
  backLabel?: string
  /** Label for the Skip button — overrides default */
  skipLabel?: string
  /** Whether the primary button should be disabled (e.g., validation failed) */
  nextDisabled?: boolean
}

const props = withDefaults(defineProps<WizardFooterProps>(), {
  isApplying: false,
  nextLabel: '',
  backLabel: '',
  skipLabel: '',
  nextDisabled: false,
})

// ============================================================================
// Emits
// ============================================================================

const emit = defineEmits<{
  /** Navigate to the next step */
  (e: 'next'): void
  /** Navigate to the previous step */
  (e: 'back'): void
  /** Skip the current step (skippable steps only) */
  (e: 'skip'): void
  /** Skip the entire onboarding wizard */
  (e: 'skip-all'): void
}>()

// ============================================================================
// Computed Labels
// ============================================================================

/** Resolved label for the primary action button */
function getPrimaryLabel(): string {
  if (props.nextLabel) return props.nextLabel
  if (props.isLastStep) return 'Launch PIM'
  return 'Continue'
}

/** Resolved label for the back button */
function getBackLabel(): string {
  if (props.backLabel) return props.backLabel
  return 'Back'
}

/** Resolved label for the skip button */
function getSkipLabel(): string {
  if (props.skipLabel) return props.skipLabel
  return 'Skip this step'
}

/** Whether any action is in progress */
function isDisabled(): boolean {
  return props.loading || props.isApplying
}
</script>

<template>
  <div class="wizard-footer mt-6 flex items-center justify-between">
    <!-- Left Side: Back Button or Skip-All Link -->
    <div class="flex items-center gap-3">
      <!-- Back Button (hidden on first step) -->
      <button
        v-if="!isFirstStep"
        class="btn-secondary"
        :disabled="isDisabled()"
        @click="emit('back')"
      >
        <svg
          class="mr-1.5 h-4 w-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        {{ getBackLabel() }}
      </button>

      <!-- Skip Entire Wizard link (shown on first step only) -->
      <button
        v-if="isFirstStep"
        class="btn-ghost text-sm text-pim-muted hover:text-pim-text"
        :disabled="isDisabled()"
        @click="emit('skip-all')"
      >
        Skip setup for now
      </button>
    </div>

    <!-- Right Side: Skip Step + Primary Button -->
    <div class="flex items-center gap-3">
      <!-- Skip Step Button (only for skippable steps) -->
      <button
        v-if="canSkipStep"
        class="btn-ghost text-sm"
        :disabled="isDisabled()"
        @click="emit('skip')"
      >
        {{ getSkipLabel() }}
      </button>

      <!-- Skip All link (non-first steps, subtle placement) -->
      <button
        v-if="!isFirstStep"
        class="btn-ghost text-xs text-pim-muted hover:text-pim-text"
        :disabled="isDisabled()"
        @click="emit('skip-all')"
      >
        Skip all
      </button>

      <!-- Primary Action Button: Next or Launch -->
      <button
        class="btn-primary"
        :disabled="isDisabled() || nextDisabled"
        @click="emit('next')"
      >
        <!-- Loading spinner -->
        <span
          v-if="loading || isApplying"
          class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
          aria-hidden="true"
        />
        {{ getPrimaryLabel() }}
        <!-- Forward arrow (not shown on last step) -->
        <svg
          v-if="!isLastStep && !loading && !isApplying"
          class="ml-1.5 h-4 w-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <!-- Rocket icon on last step -->
        <svg
          v-if="isLastStep && !loading && !isApplying"
          class="ml-1.5 h-4 w-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 003.46-1.25 11.33 11.33 0 01-3.46 1.25zm0 0a14.9 14.9 0 01-3.46 1.25m0 0a14.98 14.98 0 01-3.46-1.25m3.46 1.25v4.8m0-4.8a6 6 0 01-5.84-7.38m5.84 7.38a6 6 0 005.84-7.38"
          />
        </svg>
      </button>
    </div>
  </div>
</template>
