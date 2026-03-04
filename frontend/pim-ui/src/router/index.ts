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
  {
    path: '/list/:doctype',
    name: 'doctype-list',
    component: () => import('@/views/doctype/DocTypeList.vue'),
    meta: { title: 'List' },
    props: true,
  },
  {
    path: '/doc/:doctype/:name',
    name: 'doctype-detail',
    component: () => import('@/views/doctype/DocTypeDetail.vue'),
    meta: { title: 'Detail' },
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  let title = to.meta.title as string | undefined

  // Dynamic title for product detail
  if (to.name === 'product-detail' && to.params.id === 'new') {
    title = 'Create Product'
  }
  // Dynamic title for doctype list
  if (to.name === 'doctype-list' && to.params.doctype) {
    title = decodeURIComponent(to.params.doctype as string)
  }
  // Dynamic title for doctype detail
  if (to.name === 'doctype-detail' && to.params.name) {
    title = decodeURIComponent(to.params.name as string)
  }

  document.title = title ? `${title} - Frappe PIM` : 'Frappe PIM'
  next()
})

export default router
