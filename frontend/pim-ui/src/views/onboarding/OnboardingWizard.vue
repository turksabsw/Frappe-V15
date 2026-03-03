<script setup lang="ts">
/**
 * OnboardingWizard - Multi-step onboarding container with step navigation.
 *
 * Orchestrates the SaaS onboarding flow:
 * - Loads and tracks onboarding state via the Pinia store
 * - Renders the active step component dynamically
 * - Manages step navigation (next, back, skip)
 * - Displays progress bar and step indicators
 * - Handles loading, error, and completion states
 */
import { computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useOnboardingStore } from '@/stores/onboarding'
import type { StepFormData, OnboardingStepName } from '@/types'

import CompanyInfoStep from './steps/CompanyInfoStep.vue'
import IndustryStep from './steps/IndustryStep.vue'
import ProductStructureStep from './steps/ProductStructureStep.vue'
import ChannelStep from './steps/ChannelStep.vue'
import WorkflowStep from './steps/WorkflowStep.vue'
import ComplianceStep from './steps/ComplianceStep.vue'
import TemplateReviewStep from './steps/TemplateReviewStep.vue'
import FirstDataStep from './steps/FirstDataStep.vue'

const router = useRouter()
const { t } = useI18n()
const store = useOnboardingStore()

/** Map backend step names to Vue components */
const stepComponents: Partial<Record<OnboardingStepName, ReturnType<typeof defineComponent>>> = {
  company_info: CompanyInfoStep,
  industry_selection: IndustryStep,
  product_structure: ProductStructureStep,
  channel_setup: ChannelStep,
  workflow_preferences: WorkflowStep,
  compliance_setup: ComplianceStep,
  template_applied: TemplateReviewStep,
  customization_review: TemplateReviewStep,
  first_data: FirstDataStep,
}

/** The currently active step component */
const activeComponent = computed(() => {
  const step = store.currentStep as OnboardingStepName
  return stepComponents[step] ?? null
})

/** Whether the current step is the template review / customization step */
const isReviewMode = computed(() => {
  return store.currentStep === 'customization_review'
})

/** Display label for the current step */
const currentStepLabel = computed(() => {
  return store.activeWizardStep?.title ?? ''
})

/** Display description for the current step */
const currentStepDescription = computed(() => {
  return store.activeWizardStep?.description ?? ''
})

/** Whether we should show navigation buttons */
const showNavigation = computed(() => {
  return !store.isCompleted && !store.isSkipped && store.currentStep !== 'not_started'
})

/** Whether the guided tour step is active (handled inline) */
const isGuidedTour = computed(() => {
  return store.currentStep === 'guided_tour'
})

// =========================================================================
// Lifecycle
// =========================================================================

onMounted(async () => {
  if (!store.initialized) {
    await store.startOnboarding()
  }
})

// Redirect to dashboard when onboarding completes
watch(
  () => store.isCompleted,
  (completed) => {
    if (completed) {
      router.push('/')
    }
  },
)

// Redirect if skipped
watch(
  () => store.isSkipped,
  (skipped) => {
    if (skipped) {
      router.push('/')
    }
  },
)

// =========================================================================
// Event Handlers
// =========================================================================

/**
 * Handle form data updates from step components (partial save).
 */
function handleStepUpdate(data: StepFormData): void {
  const step = store.currentStep as OnboardingStepName
  store.setLocalStepData(step, data)
}

/**
 * Handle step completion and advance to next step.
 */
async function handleNext(formData?: StepFormData): Promise<void> {
  await store.nextStep(formData)
}

/**
 * Handle backward navigation.
 */
async function handleBack(): Promise<void> {
  await store.prevStep()
}

/**
 * Skip the entire onboarding wizard.
 */
async function handleSkip(): Promise<void> {
  await store.skipOnboarding()
}

/**
 * Complete the guided tour and finish onboarding.
 */
async function handleFinishTour(): Promise<void> {
  await store.nextStep()
}

/**
 * Navigate to a specific completed step by clicking its indicator.
 */
function handleStepClick(index: number): void {
  const step = store.wizardSteps[index]
  if (step && step.isCompleted && !step.isActive) {
    // Navigate backward to a completed step
    const targetStep = step.id as OnboardingStepName
    store.setLocalStepData(targetStep, store.getLocalStepData(targetStep) ?? {})
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-pim-bg p-4">
    <div class="w-full max-w-3xl">
      <!-- Header -->
      <div class="mb-8 text-center">
        <div
          class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-600 text-xl font-bold text-white"
        >
          P
        </div>
        <h1 class="text-2xl font-bold text-pim-text">
          {{ t('onboarding.welcome') }}
        </h1>
        <p class="mt-2 text-pim-muted">
          Set up your product management workspace in a few steps.
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="store.loading && !store.initialized" class="flex flex-col items-center py-12">
        <div class="mb-4 h-8 w-8 animate-spin rounded-full border-4 border-primary-600 border-t-transparent" />
        <p class="text-pim-muted">Loading your onboarding progress...</p>
      </div>

      <!-- Main Wizard Content -->
      <template v-else-if="!store.isCompleted && !store.isSkipped">
        <!-- Progress Bar -->
        <div class="mb-6">
          <div class="mb-2 flex justify-between text-sm text-pim-muted">
            <span>Step {{ store.currentStepIndex + 1 }} of {{ store.totalSteps }}</span>
            <span>{{ Math.round(store.progressPercent) }}%</span>
          </div>
          <div class="h-2 w-full rounded-full bg-gray-200">
            <div
              class="h-2 rounded-full bg-primary-600 transition-all duration-500 ease-out"
              :style="{ width: `${store.progressPercent}%` }"
            />
          </div>
        </div>

        <!-- Step Indicators -->
        <div class="mb-8 flex items-center justify-between">
          <template v-for="(step, index) in store.wizardSteps" :key="step.id">
            <button
              class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full text-sm font-medium transition-all duration-200"
              :class="{
                'bg-primary-600 text-white shadow-md': step.isActive,
                'bg-green-500 text-white cursor-pointer hover:bg-green-600': step.isCompleted && !step.isActive,
                'bg-gray-200 text-pim-muted cursor-default': step.isFutureStep && !step.isCompleted,
              }"
              :disabled="step.isFutureStep && !step.isCompleted"
              :title="step.title"
              @click="handleStepClick(index)"
            >
              <svg
                v-if="step.isCompleted && !step.isActive"
                class="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span v-else>{{ index + 1 }}</span>
            </button>
            <div
              v-if="index < store.wizardSteps.length - 1"
              class="mx-1 h-px flex-1 transition-colors duration-200"
              :class="step.isCompleted ? 'bg-green-400' : 'bg-gray-200'"
            />
          </template>
        </div>

        <!-- Error Banner -->
        <div
          v-if="store.error"
          class="mb-4 flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3"
        >
          <svg class="h-5 w-5 flex-shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p class="flex-1 text-sm text-red-700">{{ store.error }}</p>
          <button
            class="text-sm font-medium text-red-600 hover:text-red-800"
            @click="store.clearError()"
          >
            Dismiss
          </button>
        </div>

        <!-- Step Content Card -->
        <div class="card">
          <!-- Step Header -->
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-pim-text">{{ currentStepLabel }}</h2>
            <p class="mt-1 text-sm text-pim-muted">{{ currentStepDescription }}</p>
          </div>

          <!-- Guided Tour (inline, no separate component) -->
          <div v-if="isGuidedTour" class="space-y-6">
            <div class="rounded-lg border border-primary-200 bg-primary-50 p-6">
              <h3 class="mb-3 text-lg font-medium text-primary-900">Welcome to PIM!</h3>
              <p class="mb-4 text-sm text-primary-700">
                Your product management workspace is ready. Here are the key areas:
              </p>
              <ul class="space-y-3 text-sm text-primary-700">
                <li class="flex items-start gap-2">
                  <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                  <span><strong>Dashboard</strong> - Overview of your products and completeness scores</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                  <span><strong>Products</strong> - Create and manage product information</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                  <span><strong>Settings</strong> - Manage product types, families, and attributes</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Dynamic Step Component -->
          <component
            v-else-if="activeComponent"
            :is="activeComponent"
            :data="store.currentStepData ?? {}"
            :review-mode="isReviewMode"
            :loading="store.loading"
            @update="handleStepUpdate"
            @next="handleNext"
            @back="handleBack"
          />

          <!-- Fallback for unmapped steps -->
          <div v-else class="py-8 text-center text-pim-muted">
            <p>Step content is being prepared...</p>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div v-if="showNavigation" class="mt-6 flex items-center justify-between">
          <div>
            <button
              v-if="!store.isFirstStep"
              class="btn-secondary"
              :disabled="store.loading"
              @click="handleBack"
            >
              {{ t('onboarding.back') }}
            </button>
            <button
              v-else
              class="btn-ghost"
              :disabled="store.loading"
              @click="handleSkip"
            >
              {{ t('onboarding.skip') }}
            </button>
          </div>

          <div class="flex items-center gap-3">
            <button
              v-if="!store.isFirstStep"
              class="btn-ghost text-sm"
              :disabled="store.loading"
              @click="handleSkip"
            >
              {{ t('onboarding.skip') }}
            </button>

            <button
              v-if="isGuidedTour"
              class="btn-primary"
              :disabled="store.loading"
              @click="handleFinishTour"
            >
              <span v-if="store.loading" class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              {{ t('onboarding.finish') }}
            </button>
            <button
              v-else-if="!store.isLastStep"
              class="btn-primary"
              :disabled="store.loading"
              @click="handleNext(store.currentStepData ?? undefined)"
            >
              <span v-if="store.loading" class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              {{ t('onboarding.next') }}
            </button>
            <button
              v-else
              class="btn-primary"
              :disabled="store.loading"
              @click="handleNext(store.currentStepData ?? undefined)"
            >
              <span v-if="store.loading" class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              {{ t('onboarding.finish') }}
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
