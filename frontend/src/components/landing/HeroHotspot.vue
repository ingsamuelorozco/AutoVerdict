<script setup lang="ts">
import { Plus } from 'lucide-vue-next'

defineProps<{ texto: string }>()
</script>

<template>
  <span class="absolute">
    <button type="button" :aria-label="texto">
      <Plus aria-hidden="true" />
    </button>
  </span>
</template>
