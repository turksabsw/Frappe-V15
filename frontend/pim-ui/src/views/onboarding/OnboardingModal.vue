<script setup lang="ts">
/**
 * OnboardingModal - Non-dismissible modal wrapper for the onboarding wizard.
 *
 * Renders a full-screen overlay with a centered content panel, teleported to
 * the document body to ensure correct stacking context above all other UI.
 *
 * Non-dismissible behavior:
 * - No close button
 * - ESC key is intercepted and prevented via @keydown.esc.prevent
 * - Backdrop clicks do not close the modal
 * - Scroll is locked on the body while the modal is open
 *
 * Layout constraints:
 * - Max-width: 1100px (for the inner content panel)
 * - Max-height: 85vh (with internal overflow scrolling)
 * - Backdrop: semi-transparent with blur effect
 *
 * The default slot receives the wizard content (OnboardingWizard.vue).
 */
import { onMounted, onUnmounted, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    /** Whether the modal is visible */
    visible?: boolean
  }>(),
  {
    visible: true,
  },
)

// =========================================================================
// Body scroll lock
// =========================================================================

/** Lock body scrolling when the modal is open */
function lockBodyScroll(): void {
  document.body.style.overflow = 'hidden'
}

/** Restore body scrolling when the modal closes */
function unlockBodyScroll(): void {
  document.body.style.overflow = ''
}

onMounted(() => {
  if (props.visible) {
    lockBodyScroll()
  }
})

onUnmounted(() => {
  unlockBodyScroll()
})

watch(
  () => props.visible,
  (isVisible) => {
    if (isVisible) {
      lockBodyScroll()
    } else {
      unlockBodyScroll()
    }
  },
)

// =========================================================================
// Keyboard event handling
// =========================================================================

/**
 * Prevent ESC key from dismissing the modal.
 * The @keydown.esc.prevent on the overlay div handles inline prevention,
 * but we also add a document-level listener for comprehensive coverage.
 */
function handleKeydown(event: KeyboardEvent): void {
  if (event.key === 'Escape') {
    event.preventDefault()
    event.stopPropagation()
  }
}

onMounted(() => {
  if (props.visible) {
    document.addEventListener('keydown', handleKeydown, true)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown, true)
})

watch(
  () => props.visible,
  (isVisible) => {
    if (isVisible) {
      document.addEventListener('keydown', handleKeydown, true)
    } else {
      document.removeEventListener('keydown', handleKeydown, true)
    }
  },
)
</script>

<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="onboarding-modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="Onboarding Wizard"
      @keydown.esc.prevent
      @click.self.prevent
    >
      <!-- Modal content panel -->
      <div class="onboarding-modal-panel">
        <slot />
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.onboarding-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.onboarding-modal-panel {
  position: relative;
  width: 100%;
  max-width: 1100px;
  max-height: 85vh;
  overflow-y: auto;
  background-color: var(--pim-surface, #ffffff);
  border-radius: 1rem;
  box-shadow:
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(0, 0, 0, 0.05);
}
</style>
