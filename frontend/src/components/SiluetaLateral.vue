<script setup lang="ts">
import { computed } from 'vue'
import { perfilLateral } from '@/lib/silueta'
import type { Medidas } from '@/lib/tipos'

const props = withDefaults(defineProps<{ medidas: Medidas; color?: string; claro?: boolean; etiqueta?: string }>(), { color: 'currentColor' })
const p = computed(() => perfilLateral(props.medidas))
const margen = 120
const vb = computed(() => `${-margen} ${-margen} ${props.medidas.largo_mm + 2 * margen} ${props.medidas.alto_mm + 2 * margen}`)
</script>

<template>
  <svg :viewBox="vb" class="h-full w-full" role="img" :aria-label="etiqueta || `Silueta esquemática de ${medidas.carroceria}`" preserveAspectRatio="xMidYMax meet">
    <g :transform="`translate(0 ${medidas.alto_mm}) scale(1 -1)`">
      <line :x1="-margen" :x2="medidas.largo_mm + margen" y1="0" y2="0" stroke="currentColor" stroke-opacity="0.25" stroke-width="12" />
      <path :d="p.cuerpo" :fill="color" :fill-opacity="claro ? 0.1 : 0.85" :stroke="color" stroke-width="18" stroke-linejoin="round" />
      <path :d="p.ventanas" :fill="claro ? color : 'rgb(var(--papel))'" :fill-opacity="claro ? 0.15 : 0.35" />
      <g v-for="(r, i) in p.ruedas" :key="i">
        <circle :cx="r.cx" :cy="r.cy" :r="r.r" fill="rgb(var(--tinta))" />
        <circle :cx="r.cx" :cy="r.cy" :r="r.r * 0.58" fill="rgb(var(--papel))" fill-opacity="0.85" />
      </g>
    </g>
  </svg>
</template>
