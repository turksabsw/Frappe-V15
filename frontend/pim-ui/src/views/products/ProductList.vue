<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import type { ProductMaster } from '@/types'

const router = useRouter()
const { t } = useI18n()

const products = ref<ProductMaster[]>([])
const isLoading = ref(false)
const searchQuery = ref('')

function viewProduct(id: string): void {
  router.push(`/products/${id}`)
}

function createProduct(): void {
  router.push('/products/new')
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1>{{ t('nav.products') }}</h1>
      <button class="btn-primary" @click="createProduct">
        {{ t('common.create') }}
      </button>
    </div>

    <div class="card">
      <div class="mb-4">
        <input
          v-model="searchQuery"
          type="text"
          class="input"
          :placeholder="t('common.search')"
        />
      </div>

      <div v-if="isLoading" class="py-8 text-center text-pim-muted">
        {{ t('common.loading') }}
      </div>

      <div v-else-if="products.length === 0" class="py-8 text-center text-pim-muted">
        {{ t('common.noResults') }}
      </div>

      <div v-else class="divide-y divide-pim-border">
        <div
          v-for="product in products"
          :key="product.name"
          class="flex cursor-pointer items-center justify-between py-3 transition-colors hover:bg-gray-50"
          @click="viewProduct(product.name)"
        >
          <div>
            <p class="font-medium">{{ product.product_name }}</p>
            <p class="text-sm text-pim-muted">{{ product.product_code }}</p>
          </div>
          <div class="flex items-center gap-4">
            <span
              class="rounded-full px-2 py-1 text-xs font-medium"
              :class="{
                'bg-green-100 text-green-800': product.status === 'Active',
                'bg-amber-100 text-amber-800': product.status === 'Draft',
                'bg-gray-100 text-gray-800': product.status === 'Discontinued',
                'bg-red-100 text-red-800': product.status === 'Archived',
              }"
            >
              {{ product.status }}
            </span>
            <span class="text-sm text-pim-muted">
              {{ product.completeness_score }}%
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
