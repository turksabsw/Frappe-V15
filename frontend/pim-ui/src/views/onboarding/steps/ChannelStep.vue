<script setup lang="ts">
/**
 * ChannelStep - Configure sales and distribution channels.
 *
 * Collects:
 * - Active channels (e-commerce, marketplace, retail, wholesale, etc.)
 * - Primary channel selection
 * - Marketplace integrations
 */
import { reactive, computed, watch } from 'vue'
import type { ChannelSetupData, StepFormData } from '@/types'

const props = defineProps<{
  data: Record<string, unknown>
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'update', data: StepFormData): void
  (e: 'next', data: StepFormData): void
  (e: 'back'): void
}>()

const AVAILABLE_CHANNELS = [
  { value: 'ecommerce', label: 'E-Commerce', description: 'Online store (Shopify, WooCommerce, etc.)' },
  { value: 'marketplace', label: 'Marketplace', description: 'Amazon, eBay, Etsy, etc.' },
  { value: 'retail', label: 'Retail / POS', description: 'Physical stores and point-of-sale' },
  { value: 'wholesale', label: 'Wholesale / B2B', description: 'Bulk sales to business customers' },
  { value: 'distributor', label: 'Distributor', description: 'Third-party distribution network' },
  { value: 'direct', label: 'Direct Sales', description: 'Sales team and direct outreach' },
] as const

const MARKETPLACE_OPTIONS = [
  { value: 'amazon', label: 'Amazon' },
  { value: 'ebay', label: 'eBay' },
  { value: 'etsy', label: 'Etsy' },
  { value: 'shopify', label: 'Shopify' },
  { value: 'woocommerce', label: 'WooCommerce' },
  { value: 'magento', label: 'Magento' },
] as const

const form = reactive<ChannelSetupData>({
  channels: (props.data.channels as string[]) ?? [],
  primary_channel: (props.data.primary_channel as string) ?? '',
  marketplace_integrations: (props.data.marketplace_integrations as string[]) ?? [],
})

/** Whether the marketplace channel is selected */
const hasMarketplace = computed(() => {
  return form.channels?.includes('marketplace') ?? false
})

/** Toggle a channel on/off */
function toggleChannel(channel: string): void {
  if (!form.channels) {
    form.channels = []
  }
  const idx = form.channels.indexOf(channel)
  if (idx >= 0) {
    form.channels.splice(idx, 1)
    // Clear primary if removed
    if (form.primary_channel === channel) {
      form.primary_channel = form.channels[0] ?? ''
    }
    // Clear marketplace integrations if marketplace removed
    if (channel === 'marketplace') {
      form.marketplace_integrations = []
    }
  } else {
    form.channels.push(channel)
    // Set as primary if first channel
    if (form.channels.length === 1) {
      form.primary_channel = channel
    }
  }
}

/** Toggle a marketplace integration */
function toggleMarketplace(marketplace: string): void {
  if (!form.marketplace_integrations) {
    form.marketplace_integrations = []
  }
  const idx = form.marketplace_integrations.indexOf(marketplace)
  if (idx >= 0) {
    form.marketplace_integrations.splice(idx, 1)
  } else {
    form.marketplace_integrations.push(marketplace)
  }
}

/** Check if a channel is selected */
function isChannelSelected(channel: string): boolean {
  return form.channels?.includes(channel) ?? false
}

/** Check if a marketplace is selected */
function isMarketplaceSelected(marketplace: string): boolean {
  return form.marketplace_integrations?.includes(marketplace) ?? false
}

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
    <!-- Channel Selection -->
    <div>
      <label class="mb-3 block text-sm font-medium text-pim-text">
        Which sales channels do you use?
      </label>
      <div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
        <button
          v-for="channel in AVAILABLE_CHANNELS"
          :key="channel.value"
          class="flex items-start gap-3 rounded-lg border p-3 text-left transition-all duration-200"
          :class="
            isChannelSelected(channel.value)
              ? 'border-primary-500 bg-primary-50'
              : 'border-pim-border hover:border-gray-300'
          "
          @click="toggleChannel(channel.value)"
        >
          <div
            class="mt-0.5 flex h-4 w-4 flex-shrink-0 items-center justify-center rounded border"
            :class="
              isChannelSelected(channel.value)
                ? 'border-primary-600 bg-primary-600'
                : 'border-pim-border'
            "
          >
            <svg
              v-if="isChannelSelected(channel.value)"
              class="h-3 w-3 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-pim-text">{{ channel.label }}</p>
            <p class="text-xs text-pim-muted">{{ channel.description }}</p>
          </div>
        </button>
      </div>
    </div>

    <!-- Primary Channel -->
    <div v-if="form.channels && form.channels.length > 1">
      <label class="mb-1.5 block text-sm font-medium text-pim-text" for="primary_channel">
        Primary Channel
      </label>
      <select
        id="primary_channel"
        v-model="form.primary_channel"
        class="w-full rounded-lg border border-pim-border bg-white px-3 py-2 text-sm text-pim-text focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
      >
        <option
          v-for="channel in AVAILABLE_CHANNELS.filter((c) => isChannelSelected(c.value))"
          :key="channel.value"
          :value="channel.value"
        >
          {{ channel.label }}
        </option>
      </select>
      <p class="mt-1 text-xs text-pim-muted">
        Product data will be optimized for this channel by default.
      </p>
    </div>

    <!-- Marketplace Integrations -->
    <div v-if="hasMarketplace">
      <label class="mb-2 block text-sm font-medium text-pim-text">
        Marketplace Integrations
      </label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="mp in MARKETPLACE_OPTIONS"
          :key="mp.value"
          class="rounded-full border px-3 py-1.5 text-sm transition-all duration-200"
          :class="
            isMarketplaceSelected(mp.value)
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-pim-border text-pim-muted hover:border-gray-300'
          "
          @click="toggleMarketplace(mp.value)"
        >
          {{ mp.label }}
        </button>
      </div>
    </div>

    <!-- Info callout -->
    <div class="flex items-start gap-2 rounded-lg bg-pim-surface p-3">
      <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-pim-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xs text-pim-muted">
        You can add or modify channels later in Settings. This helps us configure
        the right attribute sets and data quality rules for your needs.
      </p>
    </div>
  </div>
</template>
