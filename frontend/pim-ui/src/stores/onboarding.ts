/**
 * Pinia store for onboarding wizard state management.
 *
 * Manages the SaaS onboarding flow including:
 * - Step navigation and persistence across sessions
 * - Form data collection per step (partial save support)
 * - Industry archetype selection and template application
 * - Progress tracking and completion state
 *
 * Communicates with the backend via:
 * - frappe_pim.pim.api.onboarding (primary API)
 * - PIM Onboarding State DocType controller APIs
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useFrappeAPI, PIM_API } from '@/composables/useFrappeAPI'
import {
  STEP_DATA_FIELDS,
  type OnboardingStepName,
  type OnboardingStateSummary,
  type StepFormData,
  type ArchetypeInfo,
  type ArchetypePreviewResponse,
  type TemplateApplicationResult,
  type AvailableArchetypesResponse,
  type OnboardingWizardStep,
} from '@/types'

/** Steps that are visible in the UI wizard (excluding internal states) */
const WIZARD_STEPS: OnboardingStepName[] = [
  'company_info',
  'industry_selection',
  'product_structure',
  'channel_setup',
  'workflow_preferences',
  'compliance_setup',
  'template_applied',
  'customization_review',
  'first_data',
  'guided_tour',
]

/** Human-readable labels for each wizard step */
const STEP_LABELS: Partial<Record<OnboardingStepName, { title: string; description: string }>> = {
  company_info: {
    title: 'Company Information',
    description: 'Tell us about your company',
  },
  industry_selection: {
    title: 'Industry Profile',
    description: 'Select your industry to get a tailored setup',
  },
  product_structure: {
    title: 'Product Structure',
    description: 'Configure how your products are organized',
  },
  channel_setup: {
    title: 'Sales Channels',
    description: 'Set up your distribution channels',
  },
  workflow_preferences: {
    title: 'Workflow Preferences',
    description: 'Configure approval and sync workflows',
  },
  compliance_setup: {
    title: 'Compliance',
    description: 'Set up regulatory compliance requirements',
  },
  template_applied: {
    title: 'Apply Template',
    description: 'Review and apply your industry template',
  },
  customization_review: {
    title: 'Customization',
    description: 'Review and customize your configuration',
  },
  first_data: {
    title: 'First Product',
    description: 'Create your first product to test the setup',
  },
  guided_tour: {
    title: 'Guided Tour',
    description: 'Quick tour of key features',
  },
}

export const useOnboardingStore = defineStore('onboarding', () => {
  // =========================================================================
  // State
  // =========================================================================

  /** Backend onboarding state summary */
  const state = ref<OnboardingStateSummary | null>(null)

  /** Whether the store has been initialized (first load) */
  const initialized = ref(false)

  /** Loading state for API operations */
  const loading = ref(false)

  /** Error from the last API operation */
  const error = ref<string | null>(null)

  /** Available industry archetypes */
  const archetypes = ref<ArchetypeInfo[]>([])

  /** Currently selected archetype identifier */
  const selectedArchetype = ref<string | null>(null)

  /** Preview data for the selected archetype */
  const archetypePreview = ref<ArchetypePreviewResponse | null>(null)

  /** Template application result */
  const templateResult = ref<TemplateApplicationResult | null>(null)

  /** Form data collected per step (local draft before save) */
  const stepFormData = ref<Partial<Record<OnboardingStepName, StepFormData>>>({})

  // =========================================================================
  // Computed
  // =========================================================================

  /** Current step name from backend state */
  const currentStep = computed<OnboardingStepName | 'not_started'>(() => {
    return state.value?.current_step ?? 'not_started'
  })

  /** Whether onboarding is completed */
  const isCompleted = computed(() => state.value?.is_completed ?? false)

  /** Whether onboarding was skipped */
  const isSkipped = computed(() => state.value?.is_skipped ?? false)

  /** Whether onboarding needs to be shown (not completed and not skipped) */
  const needsOnboarding = computed(() => {
    if (!initialized.value) return false
    return !isCompleted.value && !isSkipped.value
  })

  /** Progress percentage (0-100) */
  const progressPercent = computed(() => state.value?.progress_percent ?? 0)

  /** Whether a template has been applied */
  const templateApplied = computed(() => state.value?.template_applied ?? false)

  /** Current step index within WIZARD_STEPS (0-based) */
  const currentStepIndex = computed(() => {
    const step = currentStep.value
    if (step === 'not_started' || step === 'pending' || step === 'completed') return -1
    return WIZARD_STEPS.indexOf(step)
  })

  /** Whether the user is on the first wizard step */
  const isFirstStep = computed(() => currentStepIndex.value <= 0)

  /** Whether the user is on the last wizard step */
  const isLastStep = computed(() => currentStepIndex.value >= WIZARD_STEPS.length - 1)

  /** Total number of wizard steps */
  const totalSteps = computed(() => WIZARD_STEPS.length)

  /** UI-ready wizard steps with completion status */
  const wizardSteps = computed<OnboardingWizardStep[]>(() => {
    const stepDetails = state.value?.steps ?? []
    const activeIndex = currentStepIndex.value

    return WIZARD_STEPS.map((stepName, index) => {
      const detail = stepDetails.find((s) => s.name === stepName)
      const meta = STEP_LABELS[stepName]

      return {
        id: stepName,
        title: meta?.title ?? stepName,
        description: meta?.description ?? '',
        component: stepNameToComponent(stepName),
        isCompleted: detail?.is_completed ?? false,
        isActive: index === activeIndex,
        isFutureStep: index > activeIndex,
        hasDataField: !!STEP_DATA_FIELDS[stepName],
      }
    })
  })

  /** The currently active wizard step object */
  const activeWizardStep = computed<OnboardingWizardStep | null>(() => {
    if (currentStepIndex.value < 0) return null
    return wizardSteps.value[currentStepIndex.value] ?? null
  })

  /** Form data for the current step (from local draft or backend state) */
  const currentStepData = computed<StepFormData | null>(() => {
    const step = currentStep.value as OnboardingStepName
    return stepFormData.value[step] ?? state.value?.current_step_data ?? null
  })

  // =========================================================================
  // Actions
  // =========================================================================

  const api = useFrappeAPI()

  /**
   * Initialize the onboarding store by loading state from the backend.
   * Should be called once on app startup.
   */
  async function initialize(): Promise<void> {
    if (initialized.value) return
    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<OnboardingStateSummary>(
        PIM_API.onboarding.getState,
      )
      state.value = result
      selectedArchetype.value = result.selected_archetype ?? null

      // Populate step form data from backend if resuming
      if (result.current_step_data) {
        const step = result.current_step as OnboardingStepName
        stepFormData.value[step] = result.current_step_data as StepFormData
      }

      initialized.value = true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load onboarding state'
    } finally {
      loading.value = false
    }
  }

  /**
   * Start or resume the onboarding wizard.
   * Creates a new onboarding state if none exists.
   */
  async function startOnboarding(): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<OnboardingStateSummary>(
        PIM_API.onboarding.start,
      )
      state.value = result
      selectedArchetype.value = result.selected_archetype ?? null
      initialized.value = true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to start onboarding'
    } finally {
      loading.value = false
    }
  }

  /**
   * Save form data for the current step (partial save / draft).
   * Does not advance to the next step.
   */
  async function saveCurrentStepData(formData: StepFormData): Promise<void> {
    const step = currentStep.value
    if (step === 'not_started' || step === 'pending' || step === 'completed') return

    // Update local draft immediately for responsive UI
    stepFormData.value[step] = formData

    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<OnboardingStateSummary>(
        PIM_API.onboarding.saveStepData,
        {
          step,
          form_data: JSON.stringify(formData),
          advance: false,
        },
      )
      state.value = result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to save step data'
    } finally {
      loading.value = false
    }
  }

  /**
   * Advance to the next step, optionally saving form data first.
   */
  async function nextStep(formData?: StepFormData): Promise<void> {
    const step = currentStep.value
    if (step === 'not_started' || step === 'completed') return

    // Save local draft if provided
    if (formData && step !== 'pending') {
      stepFormData.value[step] = formData
    }

    loading.value = true
    error.value = null

    try {
      const params: Record<string, unknown> = {}
      if (formData) {
        params.form_data = JSON.stringify(formData)
      }

      const result = await api.callMethod<OnboardingStateSummary>(
        PIM_API.onboarding.complete,
        params,
      )
      state.value = result
      selectedArchetype.value = result.selected_archetype ?? null

      // Load step data for the new current step if resuming
      if (result.current_step_data) {
        const newStep = result.current_step as OnboardingStepName
        stepFormData.value[newStep] = result.current_step_data as StepFormData
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to advance step'
    } finally {
      loading.value = false
    }
  }

  /**
   * Go back to the previous step using save_step_data with advance=false.
   * This only moves the UI back - backend state navigates backwards.
   */
  async function prevStep(): Promise<void> {
    const idx = currentStepIndex.value
    if (idx <= 0) return

    const prevStepName = WIZARD_STEPS[idx - 1]

    loading.value = true
    error.value = null

    try {
      // Save current step data, then navigate to previous step on backend
      const result = await api.callMethod<OnboardingStateSummary>(
        PIM_API.onboarding.saveStepData,
        {
          step: prevStepName,
          form_data: JSON.stringify(stepFormData.value[prevStepName] ?? {}),
          advance: false,
        },
      )
      state.value = result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to navigate back'
    } finally {
      loading.value = false
    }
  }

  /**
   * Skip the onboarding wizard entirely.
   */
  async function skipOnboarding(): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<OnboardingStateSummary>(
        PIM_API.onboarding.skip,
      )
      state.value = result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to skip onboarding'
    } finally {
      loading.value = false
    }
  }

  /**
   * Reset the onboarding to initial state.
   */
  async function resetOnboarding(): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<OnboardingStateSummary>(
        PIM_API.onboarding.reset,
      )
      state.value = result
      selectedArchetype.value = null
      archetypePreview.value = null
      templateResult.value = null
      stepFormData.value = {}
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to reset onboarding'
    } finally {
      loading.value = false
    }
  }

  /**
   * Load available industry archetypes from the backend.
   */
  async function fetchArchetypes(): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<AvailableArchetypesResponse>(
        PIM_API.onboarding.getArchetypes,
      )
      archetypes.value = result.archetypes
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load archetypes'
    } finally {
      loading.value = false
    }
  }

  /**
   * Preview what an archetype template will create.
   */
  async function previewArchetype(archetype: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<ArchetypePreviewResponse>(
        PIM_API.onboarding.preview,
        { archetype },
      )
      archetypePreview.value = result
      selectedArchetype.value = archetype
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to preview archetype'
    } finally {
      loading.value = false
    }
  }

  /**
   * Apply the selected archetype template.
   */
  async function applyArchetypeTemplate(
    archetype: string,
    dryRun = false,
  ): Promise<TemplateApplicationResult | null> {
    loading.value = true
    error.value = null

    try {
      const result = await api.callMethod<TemplateApplicationResult>(
        PIM_API.onboarding.applyTemplate,
        { archetype, dry_run: dryRun },
      )
      templateResult.value = result

      // Refresh onboarding state after template application
      if (!dryRun && result.success) {
        const updatedState = await api.callMethod<OnboardingStateSummary>(
          PIM_API.onboarding.getState,
        )
        state.value = updatedState
      }

      return result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to apply template'
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Update local form data for a specific step without persisting to backend.
   * Useful for tracking form state as the user fills out fields.
   */
  function setLocalStepData(step: OnboardingStepName, data: StepFormData): void {
    stepFormData.value[step] = data
  }

  /**
   * Get the local form data for a specific step.
   */
  function getLocalStepData(step: OnboardingStepName): StepFormData | null {
    return stepFormData.value[step] ?? null
  }

  /**
   * Clear the current error.
   */
  function clearError(): void {
    error.value = null
  }

  // =========================================================================
  // Helpers
  // =========================================================================

  /** Convert a step name to its Vue component name */
  function stepNameToComponent(step: OnboardingStepName): string {
    return step
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join('') + 'Step'
  }

  return {
    // State
    state,
    initialized,
    loading,
    error,
    archetypes,
    selectedArchetype,
    archetypePreview,
    templateResult,
    stepFormData,

    // Computed
    currentStep,
    isCompleted,
    isSkipped,
    needsOnboarding,
    progressPercent,
    templateApplied,
    currentStepIndex,
    isFirstStep,
    isLastStep,
    totalSteps,
    wizardSteps,
    activeWizardStep,
    currentStepData,

    // Actions
    initialize,
    startOnboarding,
    saveCurrentStepData,
    nextStep,
    prevStep,
    skipOnboarding,
    resetOnboarding,
    fetchArchetypes,
    previewArchetype,
    applyArchetypeTemplate,
    setLocalStepData,
    getLocalStepData,
    clearError,
  }
})
