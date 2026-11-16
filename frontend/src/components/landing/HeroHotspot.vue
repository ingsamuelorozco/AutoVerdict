<script setup lang="ts">
import { Plus } from 'lucide-vue-next'

defineProps<{ texto: string }>()
</script>

<template>
  <span class="group absolute z-10 -translate-x-1/2 -translate-y-1/2">
    <button type="button" class="grid h-[38px] w-[38px] place-items-center rounded-full bg-acento text-white transition-colors hover:bg-acento-hondo" :aria-label="texto">
      <Plus class="h-4 w-4" :stroke-width="3" aria-hidden="true" />
    </button>
    <span class="pointer-events-none absolute bottom-[calc(100%+12px)] left-1/2 -translate-x-1/2 whitespace-nowrap opacity-0 transition-opacity group-hover:opacity-100 group-focus-within:opacity-100" aria-hidden="true">{{ texto }}</span>
  </span>
</template>
