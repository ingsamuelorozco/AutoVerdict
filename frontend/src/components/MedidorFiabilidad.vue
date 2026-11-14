<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{ puntaje: number; tamano?: number; etiqueta?: string | null }>(), { tamano: 180 })
const RANGOS = [
  { min: 8.5, palabra: 'Excelente', color: 'rgb(var(--mejor))' },
  { min: 7, palabra: 'Buena', color: 'rgb(var(--mejor))' },
  { min: 5.5, palabra: 'Aceptable', color: 'rgb(var(--acento))' },
  { min: 4, palabra: 'Baja', color: 'rgb(var(--ambar))' },
  { min: 0, palabra: 'Crítica', color: 'rgb(var(--roja))' },
]
const rango = computed(() => RANGOS.find((r) => props.puntaje >= r.min)!)
const R = 80
const largoArco = Math.PI * R
const avance = computed(() => (Math.max(0, Math.min(10, props.puntaje)) / 10) * largoArco)
</script>

<template>
  <figure class="inline-flex flex-col items-center" :style="{ width: `${tamano}px` }">
    <svg :viewBox="`0 0 200 115`" class="w-full" role="img" :aria-label="`Fiabilidad ${puntaje} de 10: ${etiqueta || rango.palabra}`">
      <path :d="`M 20 100 A ${R} ${R} 0 0 1 180 100`" fill="none" stroke="rgb(var(--linea))" stroke-width="16" stroke-linecap="round" />
      <path
        :d="`M 20 100 A ${R} ${R} 0 0 1 180 100`"
        fill="none"
        :stroke="rango.color"
        stroke-width="16"
        stroke-linecap="round"
        :stroke-dasharray="`${avance} ${largoArco}`"
        class="transition-all"
      />
      <text x="100" y="88" text-anchor="middle" class="fill-tinta font-titulo num" font-size="38" font-weight="600">
        {{ puntaje.toLocaleString('es-CO', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) }}
      </text>
      <text x="100" y="110" text-anchor="middle" class="fill-tenue" font-size="12">de 10</text>
    </svg>
    <figcaption class="mt-1 text-sm font-semibold" :style="{ color: rango.color }">{{ etiqueta || rango.palabra }}</figcaption>
  </figure>
</template>
