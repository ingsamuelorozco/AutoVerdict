<script setup lang="ts">
import { computed, ref } from 'vue'
import { COLORES, TRAZOS, desplazamiento, frontal, perfilLateral, persona, planta } from '@/lib/silueta'
import { formatoNumero } from '@/composables/useFormato'
import { T } from '@/lib/textos'
import type { Medidas } from '@/lib/tipos'

type Auto = Medidas & { id: number; nombre: string; indice_garaje_etiqueta?: string; indice_rompemuelle_etiqueta?: string;
  indice_garaje_nivel?: number; indice_rompemuelle_nivel?: number }
const props = defineProps<{ autos: Auto[] }>()

const vista = ref<'lateral' | 'planta' | 'frontal'>('lateral')
const alinear = ref<'rueda' | 'frente' | 'centro'>('rueda')
const tope = ref(120)
const foco = ref<number | null>(null)
const PLAZA = { largo: 5000, ancho: 2400 }

const maxLargo = computed(() => Math.max(...props.autos.map((a) => a.largo_mm), PLAZA.largo))
const refAlineacion = computed(() =>
  alinear.value === 'rueda'
    ? Math.max(...props.autos.map((a) => a.voladizo_delantero_mm + a.distancia_entre_ejes_mm))
    : maxLargo.value,
)
const dx = (a: Auto) => (alinear.value === 'rueda' ? desplazamiento(a, 'rueda', refAlineacion.value) : desplazamiento(a, alinear.value, maxLargo.value))
const anchoMundo = computed(() => Math.max(...props.autos.map((a) => dx(a) + a.largo_mm), maxLargo.value) + 900)
const altoMax = computed(() => Math.max(...props.autos.map((a) => a.alto_mm), 1750) + 200)
const anchoMax = computed(() => Math.max(...props.autos.map((a) => a.ancho_con_espejos_mm || 2000), PLAZA.ancho) + 400)

const vbLateral = computed(() => `-700 ${-altoMax.value} ${anchoMundo.value + 700} ${altoMax.value + 120}`)
const vbPlanta = computed(() => `-300 ${-anchoMax.value / 2} ${Math.max(anchoMundo.value, PLAZA.largo + 600)} ${anchoMax.value}`)
const vbFrontal = computed(() => `${-anchoMax.value / 2 - 600} ${-altoMax.value} ${anchoMax.value + 1200} ${altoMax.value + 120}`)
const NIVELES = ['', 'No cabe / riesgo', 'Apretado / precaución', 'Justo / con cuidado', 'Holgado / sin problema']
const color = (i: number) => COLORES[i % COLORES.length]
const opac = (a: Auto) => (foco.value === null || foco.value === a.id ? 1 : 0.25)
</script>

<template>
  <section class="tarjeta p-6 lg:p-8" aria-labelledby="huella-titulo">
    <div class="flex flex-wrap items-center gap-x-6 gap-y-3">
      <h3 id="huella-titulo" class="text-2xl uppercase">Huella dimensional</h3>
      <div class="flex gap-6" role="tablist" aria-label="Vista">
        <button v-for="v in (['lateral', 'planta', 'frontal'] as const)" :key="v" role="tab" :aria-selected="vista === v" :class="['pestana', vista === v ? 'pestana-activa' : '']" @click="vista = v">{{ v === 'planta' ? 'Planta' : v === 'lateral' ? 'Lateral' : 'Frontal' }}</button>
      </div>
      <label v-if="vista !== 'frontal'" class="ml-auto flex items-center gap-2 text-sm">Alinear por
        <select v-model="alinear" class="campo-mini">
          <option value="rueda">Rueda trasera</option><option value="frente">Frente</option><option value="centro">Centro</option>
        </select>
      </label>
      <label v-if="vista === 'lateral'" class="flex items-center gap-2 text-sm">Tope
        <input v-model.number="tope" type="range" min="100" max="150" step="5" aria-label="Altura del tope en milímetros" />
        <span class="w-14 num">{{ tope }} mm</span>
      </label>
    </div>

    <div class="mt-6 overflow-hidden border border-linea bg-papel text-tinta">
      <svg v-if="vista === 'lateral'" :viewBox="vbLateral" class="h-auto w-full" role="img" aria-label="Siluetas laterales superpuestas a escala">
        <g transform="scale(1 -1)">
          <line x1="-700" :x2="anchoMundo" y1="0" y2="0" stroke="currentColor" stroke-opacity="0.4" stroke-width="10" />
          <rect :x="anchoMundo - 600" y="0" width="420" :height="tope" fill="rgb(var(--ambar))" fill-opacity="0.6" rx="60"><title>Tope de {{ tope }} mm</title></rect>
          <g transform="translate(-350 0)" fill="currentColor" fill-opacity="0.35"><path :d="persona()" /><title>Persona de 1,75 m</title></g>
          <g v-for="(a, i) in autos" :key="a.id" :transform="`translate(${dx(a)} 0)`" :opacity="opac(a)" tabindex="0" :aria-label="`${a.nombre}: largo ${a.largo_mm} mm, alto ${a.alto_mm} mm, despeje ${a.distancia_libre_suelo_mm} mm`"
             @mouseenter="foco = a.id" @mouseleave="foco = null" @focus="foco = a.id" @blur="foco = null">
            <path :d="perfilLateral(a).cuerpo" fill="none" :stroke="color(i)" stroke-width="16" :stroke-dasharray="TRAZOS[i % TRAZOS.length].split(' ').map((n) => Number(n) * 4).join(' ')" stroke-linejoin="round" />
            <circle v-for="(r, j) in perfilLateral(a).ruedas" :key="j" :cx="r.cx" :cy="r.cy" :r="r.r" fill="none" :stroke="color(i)" stroke-width="12" />
          </g>
        </g>
      </svg>
      <svg v-else-if="vista === 'planta'" :viewBox="vbPlanta" class="h-auto w-full" role="img" aria-label="Huellas en planta sobre una plaza de 5,00 por 2,40 metros">
        <rect x="-100" :y="-PLAZA.ancho / 2" :width="PLAZA.largo" :height="PLAZA.ancho" fill="none" stroke="currentColor" stroke-opacity="0.5" stroke-width="20" stroke-dasharray="80 50" />
        <text x="-60" :y="-PLAZA.ancho / 2 - 50" font-size="120" class="fill-tenue">Plaza 5,00 × 2,40 m</text>
        <g v-for="(a, i) in autos" :key="a.id" :transform="`translate(${dx(a) - 100} 0)`" :opacity="opac(a)" tabindex="0" :aria-label="`${a.nombre}: ancho con espejos ${a.ancho_con_espejos_mm} mm`"
           @mouseenter="foco = a.id" @mouseleave="foco = null" @focus="foco = a.id" @blur="foco = null">
          <rect v-bind="planta(a).cuerpo" fill="none" :stroke="color(i)" stroke-width="16" :stroke-dasharray="TRAZOS[i % TRAZOS.length].split(' ').map((n) => Number(n) * 4).join(' ')" />
          <rect v-for="(e, j) in planta(a).espejos" :key="`e${j}`" v-bind="e" :fill="color(i)" />
          <rect v-for="(r, j) in planta(a).ruedas" :key="`r${j}`" v-bind="r" :fill="color(i)" fill-opacity="0.35" />
        </g>
      </svg>
      <svg v-else :viewBox="vbFrontal" class="h-auto w-full" role="img" aria-label="Vistas frontales superpuestas a escala">
        <g transform="scale(1 -1)">
          <line :x1="-anchoMax / 2 - 600" :x2="anchoMax / 2 + 600" y1="0" y2="0" stroke="currentColor" stroke-opacity="0.4" stroke-width="10" />
          <g :transform="`translate(${-anchoMax / 2 - 300} 0)`" fill="currentColor" fill-opacity="0.35"><path :d="persona()" /></g>
          <g v-for="(a, i) in autos" :key="a.id" :opacity="opac(a)" @mouseenter="foco = a.id" @mouseleave="foco = null">
            <path :d="frontal(a).cuerpo" fill="none" :stroke="color(i)" stroke-width="14" :stroke-dasharray="TRAZOS[i % TRAZOS.length].split(' ').map((n) => Number(n) * 4).join(' ')" />
            <path :d="frontal(a).espejos" :fill="color(i)" />
            <rect v-for="(r, j) in frontal(a).ruedas" :key="j" v-bind="r" :fill="color(i)" fill-opacity="0.4" />
          </g>
        </g>
      </svg>
    </div>
    <p class="mt-3 text-xs tracking-[0.5px] text-apagado">{{ T.siluetaAviso }} Referencias: suelo, tope ajustable, persona de 1,75 m y plaza de 5,00 × 2,40 m.</p>

    <ul class="mt-6 grid gap-px border border-linea bg-linea sm:grid-cols-2">
      <li v-for="(a, i) in autos" :key="a.id" class="flex flex-wrap items-center gap-x-3 gap-y-1 bg-suave px-4 py-3 text-sm" @mouseenter="foco = a.id" @mouseleave="foco = null">
        <svg width="34" height="10" aria-hidden="true"><line x1="0" x2="34" y1="5" y2="5" :stroke="color(i)" stroke-width="3" :stroke-dasharray="TRAZOS[i % TRAZOS.length]" /></svg>
        <span class="min-w-0 flex-1 truncate font-bold text-tinta">{{ a.nombre }}</span>
        <span class="text-xs" :title="NIVELES[a.indice_rompemuelle_nivel || 0]">⛰ {{ a.indice_rompemuelle_etiqueta }}</span>
        <span class="text-xs" :title="NIVELES[a.indice_garaje_nivel || 0]">🅿 {{ a.indice_garaje_etiqueta }}</span>
        <span class="sr-only">Largo {{ formatoNumero(a.largo_mm) }} mm</span>
      </li>
    </ul>
    <div class="sr-only"><table>
      <caption>Medidas de los vehículos comparados</caption>
      <tr><th>Vehículo</th><th>Largo</th><th>Alto</th><th>Ancho con espejos</th><th>Despeje</th><th>Índice Rompemuelle</th><th>Índice de Garaje</th></tr>
      <tr v-for="a in autos" :key="a.id"><td>{{ a.nombre }}</td><td>{{ a.largo_mm }} mm</td><td>{{ a.alto_mm }} mm</td><td>{{ a.ancho_con_espejos_mm }} mm</td><td>{{ a.distancia_libre_suelo_mm }} mm</td><td>{{ a.indice_rompemuelle_etiqueta }}</td><td>{{ a.indice_garaje_etiqueta }}</td></tr>
    </table></div>
  </section>
</template>
