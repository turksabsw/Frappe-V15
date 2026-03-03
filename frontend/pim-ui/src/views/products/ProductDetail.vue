<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import type { ProductMaster } from '@/types'

const props = defineProps<{
  id: string
}>()

const router = useRouter()
const { t } = useI18n()

const product = ref<ProductMaster | null>(null)
const isLoading = ref(true)

onMounted(() => {
  isLoading.value = false
})

function goBack(): void {
  router.push('/products')
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center gap-4">
      <button class="btn-ghost" @click="goBack">
        &larr; {{ t('common.cancel') }}
      </button>
      <h1 v-if="product">{{ product.product_name }}</h1>
      <h1 v-else>Product: {{ props.id }}</h1>
    </div>

    <div v-if="isLoading" class="card py-8 text-center text-pim-muted">
      {{ t('common.loading') }}
    </div>

    <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div class="lg:col-span-2">
        <div class="card">
          <h3>Product Information</h3>
          <p class="mt-2 text-sm text-pim-muted">
            Product details will be loaded from the Frappe API.
          </p>
        </div>
      </div>

      <div class="space-y-4">
        <div class="card">
          <h4>Status</h4>
          <p class="mt-2 text-sm text-pim-muted">Draft</p>
        </div>

        <div class="card">
          <h4>Completeness</h4>
          <div class="mt-2">
            <div class="h-2 w-full rounded-full bg-gray-200">
              <div
                class="h-2 rounded-full bg-primary-600"
                :style="{ width: '0%' }"
              />
            </div>
            <p class="mt-1 text-sm text-pim-muted">0%</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
