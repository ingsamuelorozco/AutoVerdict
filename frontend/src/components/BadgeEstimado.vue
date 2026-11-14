<script setup lang="ts">
import { T } from '@/lib/textos'
defineProps<{ texto?: string }>()
</script>

<template>
  <span
    class="ml-1 inline-flex cursor-help items-center border border-linea px-1.5 py-0.5 align-middle text-[10px] font-bold uppercase leading-none tracking-[1px] text-tenue"
    :title="texto || T.estimadoAyuda"
    tabindex="0"
    role="note"
    :aria-label="`${T.estimado}: ${texto || T.estimadoAyuda}`"
    >{{ T.estimado }}</span
  >
</template>
