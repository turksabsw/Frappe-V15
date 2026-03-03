import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/views/dashboard/Dashboard.vue'),
    meta: { title: 'Dashboard' },
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: () => import('@/views/onboarding/OnboardingWizard.vue'),
    meta: { title: 'Setup Wizard', layout: 'blank' },
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('@/views/products/ProductList.vue'),
    meta: { title: 'Products' },
  },
  {
    path: '/products/:id',
    name: 'product-detail',
    component: () => import('@/views/products/ProductDetail.vue'),
    meta: { title: 'Product Detail' },
    props: true,
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/settings/Settings.vue'),
    meta: { title: 'Settings' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} - Frappe PIM` : 'Frappe PIM'
  next()
})

export default router
