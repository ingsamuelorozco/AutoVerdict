<script setup lang="ts">
import { T } from '@/lib/textos'
defineProps<{ texto?: string }>()
</script>

<template>
  <span
    class="ml-1 inline-flex cursor-help items-center rounded-full border border-linea px-1.5 py-0 align-middle text-[10px] font-medium uppercase tracking-wide text-tenue"
    :title="texto || T.estimadoAyuda"
    tabindex="0"
    role="note"
    :aria-label="`${T.estimado}: ${texto || T.estimadoAyuda}`"
    >{{ T.estimado }}</span
  >
</template>
