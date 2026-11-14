<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useStorage } from '@vueuse/core'
import { ChevronDown, Pin, Plus, Printer, Share2, ShieldAlert, Trash2 } from 'lucide-vue-next'
import { api, FalloApi } from '@/lib/api'
import { useAjustes } from '@/stores/ajustes'
import { useComparador, MAX_COMPARAR } from '@/stores/comparador'
import { useFormato } from '@/composables/useFormato'
import { T } from '@/lib/textos'
import BarraFinanciera from '@/components/BarraFinanciera.vue'
import SelectorCascada from '@/components/SelectorCascada.vue'
import HuellaComparador from '@/components/HuellaComparador.vue'
import PanelReview from '@/components/PanelReview.vue'
import ImagenVehiculo from '@/components/ImagenVehiculo.vue'
import GraficoLineas from '@/components/GraficoLineas.vue'

useHead({ title: 'Comparador' })
const route = useRoute()
const router = useRouter()
const aj = useAjustes()
const comp = useComparador()
const f = useFormato()

interface Fila { clave: string; etiqueta: string; regla: string; unidad: string; valores: unknown[]; ganadores: number[]; aviso: string | null; delta: (number | null)[] | null; diferente: boolean }
interface Resultado {
  vehiculos: any[]
  categorias: { categoria: string; filas: Fila[] }[]
  marcador: Record<string, { total: number; por_categoria: Record<string, number> }>
  puntajes: { id: number; puntaje: number; perfil: string; aportes: { dimension: string; peso: number; valor_normalizado: number; aporte: number }[]; penalizacion_alerta_roja: number }[]
  reventa: { id: number; puntos: { anio: number; valor_cop: number }[] }[]
  ciudad: string
}
const datos = ref<Resultado | null>(null)
const cargando = ref(false)
const error = ref<string | null>(null)
const soloDiferencias = ref(false)
const colapsadas = useStorage<string[]>('av-categorias-colapsadas', [])
const slots = ref(2)
const resena = ref<string | null>(null)
const explicar = ref<number | null>(null)
const PERFILES = [
  { v: 'ahorrador', t: 'Ahorrador' }, { v: 'familiar', t: 'Familiar' }, { v: 'ciudad', t: 'Ciudad' },
  { v: 'carretera', t: 'Carretera y viajes' }, { v: 'rendimiento', t: 'Rendimiento' }, { v: 'fiabilidad', t: 'Fiabilidad ante todo' },
]
const DIM: Record<string, string> = { costo: 'Costo', eficiencia: 'Eficiencia', espacio: 'Espacio', desempeno: 'Desempeño', fiabilidad: 'Fiabilidad', seguridad: 'Seguridad', urbano: 'Uso urbano', equipamiento: 'Equipamiento', reventa: 'Reventa' }

function idsDeUrl(): number[] {
  return String(route.query.ids || '').split(',').map(Number).filter((n) => Number.isInteger(n) && n > 0).slice(0, MAX_COMPARAR)
}
onMounted(() => {
  const ids = idsDeUrl()
  if (ids.length) comp.reemplazar(ids)
  if (route.query.moneda === 'USD' || route.query.moneda === 'COP') aj.moneda = route.query.moneda
  if (route.query.trm) aj.fijarTrm(Number(route.query.trm))
  if (route.query.perfil) aj.perfil = String(route.query.perfil)
  slots.value = Math.max(2, comp.ids.length)
})
watch(() => [comp.ids.slice(), aj.ciudad, aj.perfil, comp.referencia, aj.trm], cargar, { deep: true })

async function cargar() {
  router.replace({ query: { ...(comp.ids.length ? { ids: comp.ids.join(',') } : {}), moneda: aj.moneda, trm: String(Math.round(aj.trm)), perfil: aj.perfil } })
  if (comp.ids.length < 2) { datos.value = null; return }
  cargando.value = true
  error.value = null
  try {
    datos.value = await api.post<Resultado>('/comparar', { ids: comp.ids, moneda: aj.moneda, trm: aj.trm, ciudad: aj.ciudad, perfil: aj.perfil, referencia_id: comp.referencia })
  } catch (e) {
    error.value = e instanceof FalloApi ? e.cuerpo.mensaje : String(e)
  } finally {
    cargando.value = false
  }
}
onMounted(cargar)

function elegido(id: number) {
  comp.agregar(id)
  slots.value = Math.max(slots.value, comp.ids.length)
}
const vacios = computed(() => Math.max(0, slots.value - comp.ids.length))
const v = computed(() => datos.value?.vehiculos || [])
function formatear(fila: Fila, x: unknown): string {
  if (x === null || x === undefined) return '—'
  if (typeof x === 'boolean') return x ? 'Sí' : 'No'
  if (typeof x !== 'number') return String(x)
  if (fila.unidad === 'cop') return f.dinero(x)
  if (fila.unidad === '%') return `${f.numero(x, 1)} %`
  if (['km/l'].includes(fila.unidad)) return f.consumo(x)
  if (fila.clave === 'indice_garaje_nivel' || fila.clave === 'indice_rompemuelle_nivel') return ['', 'Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4'][x] || String(x)
  const dec = Number.isInteger(x) ? 0 : 1
  return `${f.numero(x, dec)}${fila.unidad ? ` ${fila.unidad}` : ''}`
}
function etiquetaNivel(fila: Fila, i: number): string | null {
  if (fila.clave === 'indice_garaje_nivel') return v.value[i]?.indice_garaje_etiqueta
  if (fila.clave === 'indice_rompemuelle_nivel') return v.value[i]?.indice_rompemuelle_etiqueta
  return null
}
const visible = (fila: Fila) => !soloDiferencias.value || fila.diferente
const alternarCat = (c: string) => (colapsadas.value = colapsadas.value.includes(c) ? colapsadas.value.filter((x) => x !== c) : [...colapsadas.value, c])
const autosHuella = computed(() => v.value.map((x) => ({ ...x, nombre: `${x.marca} ${x.modelo} ${x.anio}` })))
const seriesReventa = computed(() => (datos.value?.reventa || []).map((r) => ({
  nombre: (() => { const x = v.value.find((y) => y.id === r.id); return x ? `${x.marca} ${x.modelo}` : String(r.id) })(),
  puntos: [{ x: 0, y: v.value.find((y) => y.id === r.id)?.precio_base_cop || 0 }, ...r.puntos.map((p) => ({ x: p.anio, y: p.valor_cop }))],
})))
const copiado = ref(false)
async function compartir() { try { await navigator.clipboard.writeText(location.href); copiado.value = true; setTimeout(() => (copiado.value = false), 2000) } catch { /* */ } }
const imprimir = () => window.print()
const puntajeDe = (id: number) => datos.value?.puntajes.find((p) => p.id === id)
</script>

<template>
  <BarraFinanciera />
  <div class="contenedor py-8">
    <div class="flex flex-wrap items-center gap-3">
      <h1 class="text-4xl font-semibold">Comparador</h1>
      <div class="ml-auto flex flex-wrap items-center gap-2 no-imprimir">
        <label class="flex items-center gap-2 text-sm">Perfil
          <select v-model="aj.perfil" class="rounded-full border border-linea bg-superficie px-3 py-2" @change="aj.guardar()"><option v-for="p in PERFILES" :key="p.v" :value="p.v">{{ p.t }}</option></select>
        </label>
        <label class="flex items-center gap-2 text-sm"><input v-model="soloDiferencias" type="checkbox" class="h-4 w-4" /> Mostrar solo diferencias</label>
        <button class="boton-secundario" @click="compartir"><Share2 class="h-4 w-4" aria-hidden="true" /> {{ copiado ? 'Copiado' : 'Compartir' }}</button>
        <button class="boton-secundario" @click="imprimir"><Printer class="h-4 w-4" aria-hidden="true" /> PDF / Imprimir</button>
      </div>
    </div>

    <!-- Selección -->
    <div class="mt-6 flex snap-x gap-4 overflow-x-auto pb-2 no-imprimir">
      <div v-for="n in vacios" :key="`s${n}`" class="tarjeta w-64 shrink-0 snap-start p-4">
        <p class="etiqueta mb-3">Vehículo {{ comp.ids.length + n }}</p>
        <SelectorCascada @elegido="elegido" />
      </div>
      <button
        class="tarjeta grid w-48 shrink-0 snap-start place-items-center border-dashed p-4 text-sm disabled:opacity-40"
        :disabled="comp.ids.length + vacios >= MAX_COMPARAR"
        :title="comp.ids.length + vacios >= MAX_COMPARAR ? T.maximo10 : ''"
        @click="slots++"
      ><span class="flex flex-col items-center gap-2"><Plus class="h-6 w-6" aria-hidden="true" /> Añadir vehículo para comparar</span></button>
    </div>

    <p v-if="comp.ids.length < 2" class="mt-8 text-tenue">Elige al menos dos vehículos para ver la comparación.</p>
    <div v-if="cargando && !datos" class="esqueleto mt-8 h-96" aria-busy="true" />
    <p v-if="error" class="mt-8 text-roja" role="alert">{{ error }}</p>

    <template v-if="datos && v.length >= 2">
      <!-- Marcador -->
      <section class="mt-8" aria-labelledby="marcador">
        <h2 id="marcador" class="text-2xl font-semibold">Marcador y Puntaje AutoVerdict</h2>
        <div class="mt-4 flex snap-x gap-3 overflow-x-auto pb-2">
          <div v-for="(x, i) in v" :key="x.id" class="tarjeta w-60 shrink-0 snap-start p-4">
            <p class="truncate text-sm font-medium">{{ x.marca }} {{ x.modelo }}</p>
            <p class="font-titulo text-4xl num">{{ puntajeDe(x.id)?.puntaje }}<span class="text-base text-tenue">/100</span></p>
            <p class="text-sm text-tenue num">{{ datos.marcador[x.id]?.total || 0 }} filas ganadas</p>
            <button class="mt-2 text-xs underline" :aria-expanded="explicar === i" @click="explicar = explicar === i ? null : i">Ver qué sumó y qué restó</button>
            <ul v-if="explicar === i" class="mt-2 grid gap-1 text-xs">
              <li v-for="a in puntajeDe(x.id)?.aportes" :key="a.dimension" class="flex justify-between"><span>{{ DIM[a.dimension] }} ({{ Math.round(a.peso * 100) }}%)</span><span class="num">+{{ f.numero(a.aporte, 1) }}</span></li>
              <li v-if="puntajeDe(x.id)?.penalizacion_alerta_roja" class="flex justify-between text-roja"><span>Alerta roja</span><span class="num">−{{ f.numero(puntajeDe(x.id)!.penalizacion_alerta_roja, 1) }}</span></li>
            </ul>
          </div>
        </div>
      </section>

      <HuellaComparador class="mt-8" :autos="autosHuella" />

      <!-- Tabla -->
      <section class="mt-8" aria-labelledby="tabla-titulo">
        <h2 id="tabla-titulo" class="sr-only">Tabla comparativa</h2>
        <div class="max-h-[80vh] snap-x overflow-auto rounded-2xl border border-linea">
          <table class="min-w-full border-separate border-spacing-0 text-sm" :aria-busy="cargando">
            <thead class="sticky top-0 z-20 bg-superficie">
              <tr>
                <th scope="col" class="sticky left-0 z-30 w-48 min-w-[11rem] border-b border-linea bg-superficie p-3 text-left align-bottom">
                  <span class="etiqueta">{{ datos.ciudad }} · {{ aj.moneda }}</span>
                </th>
                <th v-for="x in v" :key="x.id" scope="col" class="min-w-[220px] snap-start border-b border-l border-linea p-3 text-left align-top font-normal">
                  <ImagenVehiculo :medidas="x" :nombre="`${x.marca} ${x.modelo}`" class="!aspect-[3/1]" />
                  <RouterLink :to="`/vehiculo/${x.slug}`" class="mt-2 block font-semibold hover:underline">{{ x.marca }} {{ x.modelo }} {{ x.anio }}</RouterLink>
                  <p class="text-xs text-tenue">{{ x.version }}</p>
                  <p v-if="x.tiene_alerta_roja" class="mt-1 flex items-center gap-1 rounded-md bg-roja/15 px-2 py-1 text-xs font-semibold text-roja"><ShieldAlert class="h-3.5 w-3.5" aria-hidden="true" /> Alerta roja de fiabilidad</p>
                  <div class="mt-2 flex flex-wrap gap-1 no-imprimir">
                    <button class="chip min-h-[32px] text-xs" @click="resena = x.slug">Ver Review Honesta</button>
                    <button :class="['chip min-h-[32px] text-xs', comp.referencia === x.id ? 'chip-activo' : '']" :aria-pressed="comp.referencia === x.id" @click="comp.referencia = comp.referencia === x.id ? null : x.id"><Pin class="h-3 w-3" aria-hidden="true" /> Referencia</button>
                    <button class="chip min-h-[32px] text-xs" :aria-label="`Quitar ${x.marca} ${x.modelo}`" @click="comp.quitar(x.id)"><Trash2 class="h-3 w-3" aria-hidden="true" /></button>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody v-for="cat in datos.categorias" :key="cat.categoria">
              <tr>
                <th :colspan="v.length + 1" scope="colgroup" class="sticky left-0 border-b border-linea bg-papel p-0 text-left">
                  <button class="flex min-h-[44px] w-full items-center gap-2 px-3 font-titulo text-base font-semibold" :aria-expanded="!colapsadas.includes(cat.categoria)" @click="alternarCat(cat.categoria)">
                    <ChevronDown :class="['h-4 w-4 transition', colapsadas.includes(cat.categoria) ? '-rotate-90' : '']" aria-hidden="true" /> {{ cat.categoria }}
                    <span class="ml-2 text-xs font-normal text-tenue">({{ v.map((x) => `${x.modelo}: ${datos!.marcador[x.id]?.por_categoria[cat.categoria] || 0}`).join(' · ') }})</span>
                  </button>
                </th>
              </tr>
              <template v-if="!colapsadas.includes(cat.categoria)">
                <tr v-for="fila in cat.filas.filter(visible)" :key="fila.clave" class="hover:bg-linea/20">
                  <th scope="row" class="sticky left-0 z-10 border-b border-linea bg-superficie p-3 text-left font-normal text-tenue">
                    {{ fila.etiqueta }}
                    <span v-if="fila.aviso" class="mt-1 block text-xs text-ambar">{{ fila.aviso }}</span>
                  </th>
                  <td v-for="(x, i) in fila.valores" :key="i" :class="['border-b border-l border-linea p-3 text-right num', fila.ganadores.includes(v[i].id) ? 'font-bold' : '']">
                    <span v-if="fila.ganadores.includes(v[i].id) && fila.ganadores.length < fila.valores.length" class="mr-2 inline-flex items-center gap-1 text-[10px] font-semibold tracking-wider text-mejor">
                      <span class="h-2 w-2 rounded-full bg-mejor" aria-hidden="true" />{{ T.mejor }}
                    </span>
                    {{ etiquetaNivel(fila, i) || formatear(fila, x) }}
                    <span v-if="fila.delta && comp.referencia && v[i].id !== comp.referencia && fila.delta[i] !== null" :class="['block text-xs font-normal', (fila.delta[i] || 0) > 0 ? 'text-acento' : 'text-tenue']">Δ {{ (fila.delta[i] || 0) > 0 ? '+' : '' }}{{ fila.unidad === 'cop' ? f.dinero(fila.delta[i]) : f.numero(fila.delta[i], 1) }}</span>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
        <p class="mt-2 text-xs text-tenue">MEJOR marca el mejor valor de cada fila (todos los empatados). Las filas informativas no tienen ganador. Costos con tarifas de {{ datos.ciudad }}; seguro, crédito y TCO son estimaciones.</p>
      </section>

      <section class="tarjeta mt-8 p-5" aria-labelledby="reventa-titulo">
        <h2 id="reventa-titulo" class="text-xl font-semibold">Curva de valor residual</h2>
        <GraficoLineas class="mt-4" titulo="Valor estimado del vehículo por año" :series="seriesReventa" etiqueta-x="años" :formato-y="(y: number) => f.millones(y)" :formato-x="(x: number) => `${x}`" />
      </section>
    </template>
  </div>
  <PanelReview :slug="resena" @cerrar="resena = null" />
</template>
