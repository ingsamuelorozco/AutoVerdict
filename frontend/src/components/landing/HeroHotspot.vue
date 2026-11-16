<script setup lang="ts">
import { ref } from 'vue'
import { Plus } from 'lucide-vue-next'

defineProps<{ texto: string }>()
const abierto = ref(false)
</script>

<template>
  <span class="group absolute z-10 -translate-x-1/2 -translate-y-1/2">
    <button type="button" class="grid h-[38px] w-[38px] place-items-center rounded-full bg-acento text-white transition-colors hover:bg-acento-hondo motion-safe:animate-pulso" :aria-label="texto" @click="abierto = !abierto" @blur="abierto = false">
      <Plus class="h-4 w-4" :stroke-width="3" aria-hidden="true" />
    </button>
    <span class="sobre-claro pointer-events-none absolute bottom-[calc(100%+12px)] left-1/2 -translate-x-1/2 whitespace-nowrap bg-papel px-3 py-2 text-xs font-bold text-tinta shadow-menu after:absolute after:left-1/2 after:top-full after:-translate-x-1/2 after:border-[6px] after:border-transparent after:border-t-papel after:content-[''] transition-opacity" :class="abierto ? 'opacity-100' : 'opacity-0 group-hover:opacity-100 group-focus-within:opacity-100'" aria-hidden="true">{{ texto }}</span>
  </span>
</template>
