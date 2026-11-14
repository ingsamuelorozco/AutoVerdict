<script setup lang="ts">
import { computed } from 'vue'
import { COLORES, TRAZOS } from '@/lib/silueta'

/** Gráfico de líneas SVG propio (depreciación, saldo de crédito). */
const props = withDefaults(
  defineProps<{
    series: { nombre: string; puntos: { x: number; y: number }[] }[]
    etiquetaX?: string
    formatoY?: (v: number) => string
    formatoX?: (v: number) => string
    alto?: number
    titulo: string
  }>(),
  { alto: 260, etiquetaX: '', formatoY: (v: number) => String(Math.round(v)), formatoX: (v: number) => String(v) },
)
const W = 640
const M = { t: 16, r: 16, b: 36, l: 72 }
const todos = computed(() => props.series.flatMap((s) => s.puntos))
const xs = computed(() => [Math.min(...todos.value.map((p) => p.x)), Math.max(...todos.value.map((p) => p.x))])
const ys = computed(() => [0, Math.max(...todos.value.map((p) => p.y), 1) * 1.05])
const sx = (x: number) => M.l + ((x - xs.value[0]) / (xs.value[1] - xs.value[0] || 1)) * (W - M.l - M.r)
const sy = (y: number) => props.alto - M.b - ((y - ys.value[0]) / (ys.value[1] - ys.value[0] || 1)) * (props.alto - M.t - M.b)
const marcasY = computed(() => [0, 0.25, 0.5, 0.75, 1].map((f) => ys.value[1] * f))
const marcasX = computed(() => [...new Set(todos.value.map((p) => p.x))].sort((a, b) => a - b))
const filtrosX = computed(() => (marcasX.value.length > 12 ? marcasX.value.filter((_, i) => i % Math.ceil(marcasX.value.length / 12) === 0) : marcasX.value))
</script>

<template>
  <figure>
    <svg :viewBox="`0 0 ${W} ${alto}`" class="w-full" role="img" :aria-label="titulo">
      <g v-for="m in marcasY" :key="m">
        <line :x1="M.l" :x2="W - M.r" :y1="sy(m)" :y2="sy(m)" stroke="rgb(var(--linea))" />
        <text :x="M.l - 8" :y="sy(m) + 4" text-anchor="end" font-size="11" class="fill-tenue num">{{ formatoY(m) }}</text>
      </g>
      <text v-for="x in filtrosX" :key="x" :x="sx(x)" :y="alto - 14" text-anchor="middle" font-size="11" class="fill-tenue num">{{ formatoX(x) }}</text>
      <text v-if="etiquetaX" :x="W - M.r" :y="alto - 1" text-anchor="end" font-size="10" class="fill-tenue">{{ etiquetaX }}</text>
      <g v-for="(s, i) in series" :key="s.nombre">
        <polyline :points="s.puntos.map((p) => `${sx(p.x)},${sy(p.y)}`).join(' ')" fill="none" :stroke="COLORES[i % COLORES.length]" stroke-width="2.5" :stroke-dasharray="TRAZOS[i % TRAZOS.length]" />
        <circle v-for="p in s.puntos.length <= 12 ? s.puntos : []" :key="p.x" :cx="sx(p.x)" :cy="sy(p.y)" r="3.5" :fill="COLORES[i % COLORES.length]">
          <title>{{ s.nombre }} · {{ formatoX(p.x) }}: {{ formatoY(p.y) }}</title>
        </circle>
      </g>
    </svg>
    <figcaption class="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs">
      <span v-for="(s, i) in series" :key="s.nombre" class="inline-flex items-center gap-2">
        <svg width="28" height="8" aria-hidden="true"><line x1="0" x2="28" y1="4" y2="4" :stroke="COLORES[i % COLORES.length]" stroke-width="2.5" :stroke-dasharray="TRAZOS[i % TRAZOS.length]" /></svg>
        {{ s.nombre }}
      </span>
    </figcaption>
    <div class="sr-only"><table>
      <caption>{{ titulo }}</caption>
      <tr><th>Serie</th><th v-for="x in marcasX" :key="x">{{ formatoX(x) }}</th></tr>
      <tr v-for="s in series" :key="s.nombre"><th>{{ s.nombre }}</th><td v-for="p in s.puntos" :key="p.x">{{ formatoY(p.y) }}</td></tr>
    </table></div>
  </figure>
</template>
