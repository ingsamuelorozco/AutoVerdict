<script setup lang="ts">
import { ref } from 'vue'

/** Control deslizante antes/después sobre dos capas (imagen o silueta). */
defineProps<{ etiquetaAntes: string; etiquetaDespues: string }>()
const pos = ref(50)
</script>

<template>
  <div class="relative aspect-[16/9] select-none overflow-hidden border border-linea">
    <div class="absolute inset-0"><slot name="despues" /></div>
    <div class="absolute inset-0" :style="{ clipPath: `inset(0 ${100 - pos}% 0 0)` }"><slot name="antes" /></div>
    <div class="pointer-events-none absolute inset-y-0 w-0.5 bg-white" :style="{ left: `${pos}%` }" />
    <span class="insignia absolute left-3 top-3 bg-black text-white">{{ etiquetaAntes }}</span>
    <span class="insignia absolute right-3 top-3 bg-black text-white">{{ etiquetaDespues }}</span>
    <input v-model.number="pos" type="range" min="0" max="100" class="absolute inset-x-0 bottom-2 mx-auto w-2/3 accent-white" :aria-label="`Comparar ${etiquetaAntes} y ${etiquetaDespues}`" />
  </div>
</template>
