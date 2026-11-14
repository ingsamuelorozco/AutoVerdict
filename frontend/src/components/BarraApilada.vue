<script setup lang="ts">
import { computed } from 'vue'

/** Barra apilada horizontal con patrón y etiqueta por segmento (no depende solo del color). */
const props = defineProps<{ componentes: Record<string, number>; formato: (v: number) => string; titulo: string }>()
const NOMBRES: Record<string, string> = {
  combustible: 'Combustible / energía', mantenimiento: 'Mantenimiento', seguro: 'Seguro todo riesgo', soat: 'SOAT',
  impuesto: 'Impuesto vehicular', tecnomecanica: 'Revisión técnico-mecánica', intereses: 'Intereses del crédito',
  depreciacion: 'Depreciación', tramites: 'Matrícula y trámites',
}
const COLORES = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9', '#D55E00', '#7F3C8D', '#8C8C8C', '#B8860B']
const partes = computed(() => {
  const ent = Object.entries(props.componentes).filter(([, v]) => v > 0)
  const total = ent.reduce((a, [, v]) => a + v, 0) || 1
  return ent.map(([k, v], i) => ({ k, nombre: NOMBRES[k] || k, v, pct: v / total, color: COLORES[i % COLORES.length], patron: i % 3 }))
})
</script>

<template>
  <figure>
    <svg viewBox="0 0 600 44" class="w-full" role="img" :aria-label="titulo" preserveAspectRatio="none">
      <defs>
        <pattern id="rayas" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="white" stroke-opacity="0.45" stroke-width="2" /></pattern>
        <pattern id="puntos" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.2" fill="white" fill-opacity="0.5" /></pattern>
      </defs>
      <g v-for="(p, i) in partes" :key="p.k">
        <rect :x="partes.slice(0, i).reduce((a, q) => a + q.pct * 600, 0)" y="0" :width="Math.max(p.pct * 600 - 1, 0)" height="44" :fill="p.color"><title>{{ p.nombre }}: {{ formato(p.v) }}</title></rect>
        <rect v-if="p.patron" :x="partes.slice(0, i).reduce((a, q) => a + q.pct * 600, 0)" y="0" :width="Math.max(p.pct * 600 - 1, 0)" height="44" :fill="p.patron === 1 ? 'url(#rayas)' : 'url(#puntos)'" />
      </g>
    </svg>
    <figcaption>
      <ul class="mt-6 grid gap-x-10 text-sm sm:grid-cols-2">
        <li v-for="p in partes" :key="p.k" class="flex items-center gap-3 border-b border-linea py-2">
          <span class="inline-block h-3 w-3 shrink-0" :style="{ background: p.color }" aria-hidden="true" />
          <span>{{ p.nombre }}</span>
          <span class="ml-auto whitespace-nowrap font-bold text-tinta num">{{ formato(p.v) }} <span class="font-light text-tenue">({{ Math.round(p.pct * 100) }}%)</span></span>
        </li>
      </ul>
    </figcaption>
  </figure>
</template>
