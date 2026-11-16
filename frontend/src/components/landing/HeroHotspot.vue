<script setup lang="ts">
import { Plus } from 'lucide-vue-next'

defineProps<{ texto: string }>()
</script>

<template>
  <span class="absolute z-10 -translate-x-1/2 -translate-y-1/2">
    <button type="button" class="grid h-[38px] w-[38px] place-items-center rounded-full bg-acento text-white transition-colors hover:bg-acento-hondo" :aria-label="texto">
      <Plus class="h-4 w-4" :stroke-width="3" aria-hidden="true" />
    </button>
  </span>
</template>
