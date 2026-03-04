<script setup lang="ts">
/**
 * AttributeConfigStep - Attribute configuration step (Step 4).
 *
 * Collects:
 * - Attribute groups review (toggle groups on/off from template)
 * - Key attributes from template (toggle individual attributes)
 * - Removed template attributes list
 * - Custom attribute definitions (name, label, type, group)
 *
 * Reads the selected industry template preview from the store to
 * pre-populate attribute groups and attributes. Users can:
 * - Enable/disable entire attribute groups
 * - Enable/disable individual attributes within groups
 * - Add custom attributes with name, type, and optional group
 *
 * Integrates with the onboarding store to:
 * - Read template preview for attribute groups
 * - Read/write step data via Pinia store
 * - Expose isValid for wizard navigation control
 */
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useOnboardingStore } from '@/stores/onboarding'
import type {
  AttributeConfigData,
  AttributeGroupSelection,
  AttributeSelection,
  CustomAttributeDefinition,
  StepFormData,
} from '@/types'

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

/** Attribute type options for custom attributes */
const ATTRIBUTE_TYPES: readonly { value: string; label: string; description: string }[] = [
  { value: 'text', label: 'Text', description: 'Single-line text value' },
  { value: 'textarea', label: 'Long Text', description: 'Multi-line text content' },
  { value: 'number', label: 'Number', description: 'Numeric value (integer or decimal)' },
  { value: 'select', label: 'Select', description: 'Choose from predefined options' },
  { value: 'multiselect', label: 'Multi-Select', description: 'Choose multiple options' },
  { value: 'boolean', label: 'Yes / No', description: 'Boolean toggle value' },
  { value: 'date', label: 'Date', description: 'Calendar date value' },
  { value: 'url', label: 'URL', description: 'Web link or URL' },
  { value: 'image', label: 'Image', description: 'Image upload or URL' },
] as const

/** Custom attribute form state */
const newAttribute = reactive<{
  name: string
  label: string
  type: string
  group: string
  required: boolean
}>({
  name: '',
  label: '',
  type: 'text',
  group: '',
  required: false,
})

/** Whether the custom attribute form is expanded */
const showAddForm = ref(false)

/** Load initial data from store or props */
function getInitialData(): AttributeConfigData {
  const storeData = store.getWizardStepData('attribute_config')
  const source = storeData ?? props.data

  return {
    attribute_groups: (source?.attribute_groups as AttributeGroupSelection[]) ?? [],
    removed_template_attrs: (source?.removed_template_attrs as string[]) ?? [],
    custom_attributes: (source?.custom_attributes as CustomAttributeDefinition[]) ?? [],
  }
}

const form = reactive<AttributeConfigData>(getInitialData())

/** Build attribute groups from template preview if form is empty */
function buildGroupsFromTemplate(): void {
  if (form.attribute_groups && form.attribute_groups.length > 0) return

  const preview = store.templatePreview
  if (!preview || !preview.attribute_groups) return

  // Build default groups from template preview attribute_groups list
  const groups: AttributeGroupSelection[] = preview.attribute_groups.map((groupName) => ({
    name: groupName.toLowerCase().replace(/[^a-z0-9]+/g, '_'),
    label: groupName,
    enabled: true,
    attributes: [],
  }))

  // If we have no attributes yet, populate with sensible defaults per group
  form.attribute_groups = groups
}

/** Sync initial data to store on mount */
onMounted(() => {
  // Try to build groups from template preview if not already populated
  buildGroupsFromTemplate()
  store.setWizardStepData('attribute_config', { ...form })
})

/** Toggle an entire attribute group on/off */
function toggleGroup(groupIndex: number): void {
  if (!form.attribute_groups) return
  const group = form.attribute_groups[groupIndex]
  if (!group) return

  group.enabled = !group.enabled

  // When disabling a group, track removed template attributes
  if (!group.enabled) {
    const templateAttrs = group.attributes
      .filter((a) => a.from_template)
      .map((a) => a.name)

    const removed = form.removed_template_attrs ?? []
    for (const attrName of templateAttrs) {
      if (!removed.includes(attrName)) {
        removed.push(attrName)
      }
    }
    form.removed_template_attrs = [...removed]
  } else {
    // When re-enabling, remove from removed list
    const removed = form.removed_template_attrs ?? []
    const templateAttrNames = group.attributes
      .filter((a) => a.from_template)
      .map((a) => a.name)
    form.removed_template_attrs = removed.filter((r) => !templateAttrNames.includes(r))
  }

  // Update all attributes in the group
  group.attributes.forEach((attr) => {
    attr.enabled = group.enabled
  })

  // Trigger reactivity
  form.attribute_groups = [...form.attribute_groups]
}

/** Toggle an individual attribute within a group */
function toggleAttribute(groupIndex: number, attrIndex: number): void {
  if (!form.attribute_groups) return
  const group = form.attribute_groups[groupIndex]
  if (!group) return

  const attr = group.attributes[attrIndex]
  if (!attr) return

  attr.enabled = !attr.enabled

  // Track removed template attributes
  if (attr.from_template) {
    const removed = form.removed_template_attrs ?? []
    if (!attr.enabled) {
      if (!removed.includes(attr.name)) {
        removed.push(attr.name)
      }
    } else {
      const idx = removed.indexOf(attr.name)
      if (idx >= 0) {
        removed.splice(idx, 1)
      }
    }
    form.removed_template_attrs = [...removed]
  }

  // Check if all attributes in the group are enabled/disabled
  const allEnabled = group.attributes.every((a) => a.enabled)
  const allDisabled = group.attributes.every((a) => !a.enabled)
  if (allEnabled) {
    group.enabled = true
  } else if (allDisabled) {
    group.enabled = false
  }

  // Trigger reactivity
  form.attribute_groups = [...form.attribute_groups]
}

/** Auto-generate attribute name from label */
function generateAttrName(label: string): string {
  return label
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, '_')
    .replace(/^_+|_+$/g, '')
}

/** Update attribute name when label changes */
function handleLabelInput(): void {
  if (!newAttribute.name || newAttribute.name === generateAttrName(newAttribute.label.slice(0, -1))) {
    newAttribute.name = generateAttrName(newAttribute.label)
  }
}

/** Add a custom attribute */
function addCustomAttribute(): void {
  const label = newAttribute.label.trim()
  if (!label) return

  const name = newAttribute.name.trim() || generateAttrName(label)
  const customs = form.custom_attributes ?? []

  // Check for duplicate names
  if (customs.some((a) => a.name === name)) return

  customs.push({
    name,
    label,
    type: newAttribute.type || 'text',
    group: newAttribute.group || undefined,
    required: newAttribute.required,
  })

  form.custom_attributes = [...customs]

  // Reset form
  newAttribute.name = ''
  newAttribute.label = ''
  newAttribute.type = 'text'
  newAttribute.group = ''
  newAttribute.required = false
  showAddForm.value = false
}

/** Remove a custom attribute */
function removeCustomAttribute(name: string): void {
  const customs = form.custom_attributes ?? []
  const index = customs.findIndex((a) => a.name === name)
  if (index >= 0) {
    customs.splice(index, 1)
    form.custom_attributes = [...customs]
  }
}

/** Handle Enter key in custom attribute label input */
function handleAttrKeydown(event: KeyboardEvent): void {
  if (event.key === 'Enter') {
    event.preventDefault()
    addCustomAttribute()
  }
}

/** Available group names for custom attribute assignment */
const availableGroups = computed<string[]>(() => {
  const groups = (form.attribute_groups ?? [])
    .filter((g) => g.enabled)
    .map((g) => g.label)
  return groups
})

/** Count of enabled template attributes */
const enabledTemplateCount = computed(() => {
  let count = 0
  for (const group of form.attribute_groups ?? []) {
    count += group.attributes.filter((a) => a.enabled && a.from_template).length
  }
  return count
})

/** Count of removed template attributes */
const removedCount = computed(() => {
  return (form.removed_template_attrs ?? []).length
})

/** Count of custom attributes */
const customCount = computed(() => {
  return (form.custom_attributes ?? []).length
})

/** Total attribute count */
const totalAttributeCount = computed(() => {
  return enabledTemplateCount.value + customCount.value
})

/** Emit form data changes to parent and sync to store */
watch(
  form,
  (newVal) => {
    const data = { ...newVal }
    store.setWizardStepData('attribute_config', data)
    emit('update', data)
  },
  { deep: true },
)

/** Step 4 has no hard required fields — always valid (user can accept defaults) */
function isValid(): boolean {
  return true
}

function handleSubmit(): void {
  if (isValid()) {
    emit('next', { ...form })
  }
}

defineExpose({ isValid })
</script>

<template>
  <div class="space-y-6">
    <!-- Summary Stats -->
    <div class="grid grid-cols-3 gap-3">
      <div class="rounded-lg border border-pim-border bg-pim-surface p-3 text-center">
        <p class="text-lg font-semibold text-primary-600">{{ totalAttributeCount }}</p>
        <p class="text-xs text-pim-muted">Total Attributes</p>
      </div>
      <div class="rounded-lg border border-pim-border bg-pim-surface p-3 text-center">
        <p class="text-lg font-semibold text-primary-600">{{ customCount }}</p>
        <p class="text-xs text-pim-muted">Custom Added</p>
      </div>
      <div class="rounded-lg border border-pim-border bg-pim-surface p-3 text-center">
        <p class="text-lg font-semibold text-amber-600">{{ removedCount }}</p>
        <p class="text-xs text-pim-muted">Removed</p>
      </div>
    </div>

    <!-- Attribute Groups from Template -->
    <div v-if="(form.attribute_groups ?? []).length > 0">
      <label class="mb-3 block text-sm font-medium text-pim-text">
        Attribute Groups
      </label>
      <p class="mb-3 text-xs text-pim-muted">
        These groups come from your industry template. Toggle groups or individual attributes to customize.
      </p>

      <div class="space-y-3">
        <div
          v-for="(group, gIdx) in form.attribute_groups"
          :key="group.name"
          class="rounded-lg border border-pim-border"
        >
          <!-- Group Header -->
          <div
            class="flex cursor-pointer items-center justify-between px-4 py-3 transition-colors hover:bg-pim-surface"
            @click="toggleGroup(gIdx)"
          >
            <div class="flex items-center gap-3">
              <div
                class="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded border transition-colors"
                :class="
                  group.enabled
                    ? 'border-primary-600 bg-primary-600'
                    : 'border-pim-border bg-white'
                "
              >
                <svg
                  v-if="group.enabled"
                  class="h-3.5 w-3.5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-pim-text">{{ group.label }}</p>
                <p class="text-xs text-pim-muted">
                  {{ group.attributes.filter((a) => a.enabled).length }} / {{ group.attributes.length }} attributes enabled
                </p>
              </div>
            </div>
            <span
              class="text-xs font-medium"
              :class="group.enabled ? 'text-green-600' : 'text-pim-muted'"
            >
              {{ group.enabled ? 'Enabled' : 'Disabled' }}
            </span>
          </div>

          <!-- Group Attributes -->
          <div
            v-if="group.enabled && group.attributes.length > 0"
            class="border-t border-pim-border px-4 py-2"
          >
            <div class="space-y-1">
              <label
                v-for="(attr, aIdx) in group.attributes"
                :key="attr.name"
                class="flex cursor-pointer items-center gap-2.5 rounded px-2 py-1.5 transition-colors hover:bg-pim-surface"
              >
                <input
                  type="checkbox"
                  :checked="attr.enabled"
                  class="h-3.5 w-3.5 rounded border-pim-border text-primary-600 focus:ring-primary-500"
                  @change="toggleAttribute(gIdx, aIdx)"
                />
                <span class="flex-1 text-xs text-pim-text">{{ attr.label }}</span>
                <span class="text-[10px] text-pim-muted">{{ attr.type }}</span>
                <span
                  v-if="attr.from_template"
                  class="rounded bg-blue-50 px-1.5 py-0.5 text-[10px] text-blue-600"
                >
                  template
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Template Groups Info -->
    <div
      v-else
      class="rounded-lg border border-dashed border-pim-border p-4 text-center"
    >
      <p class="text-sm text-pim-muted">
        No attribute groups from template. Add custom attributes below or go back
        to select an industry profile.
      </p>
    </div>

    <!-- Custom Attributes Section -->
    <div>
      <div class="mb-3 flex items-center justify-between">
        <div>
          <label class="block text-sm font-medium text-pim-text">
            Custom Attributes
          </label>
          <p class="text-xs text-pim-muted">
            Add attributes not covered by the template.
          </p>
        </div>
        <button
          v-if="!showAddForm"
          type="button"
          class="rounded-lg border border-primary-500 bg-primary-50 px-3 py-1.5 text-xs font-medium text-primary-700 transition-colors hover:bg-primary-100"
          @click="showAddForm = true"
        >
          + Add Attribute
        </button>
      </div>

      <!-- Add Custom Attribute Form -->
      <div
        v-if="showAddForm"
        class="mb-3 rounded-lg border border-primary-200 bg-primary-50/30 p-4"
      >
        <div class="space-y-3">
          <!-- Label & Name -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-medium text-pim-text" for="attr_label">
                Label <span class="text-red-500">*</span>
              </label>
              <input
                id="attr_label"
                v-model="newAttribute.label"
                type="text"
                class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                placeholder="e.g., Shelf Life"
                @input="handleLabelInput"
                @keydown="handleAttrKeydown"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium text-pim-text" for="attr_name">
                System Name
              </label>
              <input
                id="attr_name"
                v-model="newAttribute.name"
                type="text"
                class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text placeholder-pim-muted focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                placeholder="Auto-generated"
              />
            </div>
          </div>

          <!-- Type & Group -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-medium text-pim-text" for="attr_type">
                Type
              </label>
              <select
                id="attr_type"
                v-model="newAttribute.type"
                class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                <option
                  v-for="t in ATTRIBUTE_TYPES"
                  :key="t.value"
                  :value="t.value"
                >
                  {{ t.label }}
                </option>
              </select>
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium text-pim-text" for="attr_group">
                Group
              </label>
              <select
                id="attr_group"
                v-model="newAttribute.group"
                class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                <option value="">No group</option>
                <option
                  v-for="g in availableGroups"
                  :key="g"
                  :value="g"
                >
                  {{ g }}
                </option>
              </select>
            </div>
          </div>

          <!-- Required Toggle -->
          <label class="flex cursor-pointer items-center gap-2">
            <input
              v-model="newAttribute.required"
              type="checkbox"
              class="h-3.5 w-3.5 rounded border-pim-border text-primary-600 focus:ring-primary-500"
            />
            <span class="text-xs text-pim-text">Required attribute</span>
          </label>

          <!-- Actions -->
          <div class="flex justify-end gap-2">
            <button
              type="button"
              class="rounded-lg border border-pim-border bg-white px-3 py-1.5 text-xs font-medium text-pim-text transition-colors hover:bg-pim-surface"
              @click="showAddForm = false"
            >
              Cancel
            </button>
            <button
              type="button"
              class="rounded-lg border border-primary-500 bg-primary-600 px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-primary-700 disabled:opacity-50"
              :disabled="!newAttribute.label.trim()"
              @click="addCustomAttribute"
            >
              Add Attribute
            </button>
          </div>
        </div>
      </div>

      <!-- Custom Attribute List -->
      <div v-if="(form.custom_attributes ?? []).length > 0" class="space-y-2">
        <div
          v-for="attr in form.custom_attributes"
          :key="attr.name"
          class="flex items-center justify-between rounded-lg border border-pim-border px-3 py-2"
        >
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium text-pim-text">{{ attr.label }}</span>
            <span class="rounded bg-gray-100 px-1.5 py-0.5 text-[10px] text-pim-muted">
              {{ attr.type }}
            </span>
            <span
              v-if="attr.group"
              class="rounded bg-blue-50 px-1.5 py-0.5 text-[10px] text-blue-600"
            >
              {{ attr.group }}
            </span>
            <span
              v-if="attr.required"
              class="rounded bg-amber-50 px-1.5 py-0.5 text-[10px] text-amber-600"
            >
              required
            </span>
          </div>
          <button
            type="button"
            class="text-pim-muted transition-colors hover:text-red-500"
            @click="removeCustomAttribute(attr.name)"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Info callout -->
    <div class="flex items-start gap-2 rounded-lg bg-pim-surface p-3">
      <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xs text-pim-muted">
        Attributes define the data fields for your products. You can always add, remove,
        or modify attributes later in Settings. Template attributes provide a starting
        point based on your industry.
      </p>
    </div>
  </div>
</template>
