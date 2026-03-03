<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import type { OnboardingStep } from '@/types'

const router = useRouter()
const { t } = useI18n()

const currentStepIndex = ref(0)

const steps = ref<OnboardingStep[]>([
  {
    id: 'company_info',
    title: 'Company Information',
    description: 'Tell us about your company',
    component: 'CompanyInfoStep',
    isCompleted: false,
    isActive: true,
    isFutureStep: false,
  },
  {
    id: 'industry_selection',
    title: 'Industry Profile',
    description: 'Select your industry to get a tailored setup',
    component: 'IndustrySelectionStep',
    isCompleted: false,
    isActive: false,
    isFutureStep: true,
  },
  {
    id: 'product_structure',
    title: 'Product Structure',
    description: 'Configure how your products are organized',
    component: 'ProductStructureStep',
    isCompleted: false,
    isActive: false,
    isFutureStep: true,
  },
  {
    id: 'review',
    title: 'Review & Apply',
    description: 'Review your configuration and apply the template',
    component: 'ReviewStep',
    isCompleted: false,
    isActive: false,
    isFutureStep: true,
  },
])

const currentStep = computed(() => steps.value[currentStepIndex.value])
const isFirstStep = computed(() => currentStepIndex.value === 0)
const isLastStep = computed(() => currentStepIndex.value === steps.value.length - 1)
const progressPercent = computed(
  () => ((currentStepIndex.value + 1) / steps.value.length) * 100
)

function nextStep(): void {
  if (currentStepIndex.value < steps.value.length - 1) {
    steps.value[currentStepIndex.value].isCompleted = true
    steps.value[currentStepIndex.value].isActive = false
    currentStepIndex.value++
    steps.value[currentStepIndex.value].isActive = true
    steps.value[currentStepIndex.value].isFutureStep = false
  }
}

function prevStep(): void {
  if (currentStepIndex.value > 0) {
    steps.value[currentStepIndex.value].isActive = false
    steps.value[currentStepIndex.value].isFutureStep = true
    currentStepIndex.value--
    steps.value[currentStepIndex.value].isActive = true
    steps.value[currentStepIndex.value].isCompleted = false
  }
}

function finishOnboarding(): void {
  steps.value[currentStepIndex.value].isCompleted = true
  router.push('/')
}

function skipOnboarding(): void {
  router.push('/')
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-pim-bg p-4">
    <div class="w-full max-w-2xl">
      <div class="mb-8 text-center">
        <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-600 text-xl font-bold text-white">
          P
        </div>
        <h1>{{ t('onboarding.welcome') }}</h1>
        <p class="mt-2 text-pim-muted">
          Set up your product management workspace in a few steps.
        </p>
      </div>

      <!-- Progress bar -->
      <div class="mb-8">
        <div class="mb-2 flex justify-between text-sm text-pim-muted">
          <span>Step {{ currentStepIndex + 1 }} of {{ steps.length }}</span>
          <span>{{ Math.round(progressPercent) }}%</span>
        </div>
        <div class="h-2 w-full rounded-full bg-gray-200">
          <div
            class="h-2 rounded-full bg-primary-600 transition-all duration-300"
            :style="{ width: `${progressPercent}%` }"
          />
        </div>
      </div>

      <!-- Step indicators -->
      <div class="mb-8 flex justify-between">
        <div
          v-for="(step, index) in steps"
          :key="step.id"
          class="flex items-center gap-2"
          :class="{ 'flex-1': index < steps.length - 1 }"
        >
          <div
            class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full text-sm font-medium"
            :class="{
              'bg-primary-600 text-white': step.isActive,
              'bg-green-500 text-white': step.isCompleted,
              'bg-gray-200 text-pim-muted': step.isFutureStep && !step.isCompleted,
            }"
          >
            <span v-if="step.isCompleted">&#10003;</span>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div v-if="index < steps.length - 1" class="h-px flex-1 bg-gray-200" />
        </div>
      </div>

      <!-- Current step content -->
      <div class="card">
        <h2>{{ currentStep.title }}</h2>
        <p class="mt-1 text-sm text-pim-muted">{{ currentStep.description }}</p>

        <div class="mt-6 min-h-[200px]">
          <p class="text-pim-muted">
            Step content for "{{ currentStep.title }}" will be implemented in subsequent subtasks.
          </p>
        </div>
      </div>

      <!-- Navigation buttons -->
      <div class="mt-6 flex items-center justify-between">
        <button
          v-if="!isFirstStep"
          class="btn-secondary"
          @click="prevStep"
        >
          {{ t('onboarding.back') }}
        </button>
        <button
          v-else
          class="btn-ghost"
          @click="skipOnboarding"
        >
          {{ t('onboarding.skip') }}
        </button>

        <button
          v-if="!isLastStep"
          class="btn-primary"
          @click="nextStep"
        >
          {{ t('onboarding.next') }}
        </button>
        <button
          v-else
          class="btn-primary"
          @click="finishOnboarding"
        >
          {{ t('onboarding.finish') }}
        </button>
      </div>
    </div>
  </div>
</template>
