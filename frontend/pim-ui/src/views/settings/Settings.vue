<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="space-y-6">
    <h1>{{ t('nav.settings') }}</h1>

    <div class="card">
      <h3>General Settings</h3>
      <p class="mt-2 text-sm text-pim-muted">
        PIM settings will be loaded from the Frappe backend API.
      </p>
    </div>

    <div class="card">
      <h3>ERPNext Integration</h3>
      <p class="mt-2 text-sm text-pim-muted">
        Sync configuration and status will be displayed here.
      </p>
    </div>
  </div>
</template>
