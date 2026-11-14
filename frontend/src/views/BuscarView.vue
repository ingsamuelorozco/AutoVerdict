<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useDebounceFn } from '@vueuse/core'
import { LayoutGrid, List, Search, SlidersHorizontal, Share2 } from 'lucide-vue-next'
import { api } from '@/lib/api'
import { useCarga } from '@/composables/useCarga'
import { useAjustes } from '@/stores/ajustes'
import { useFavoritos } from '@/stores/favoritos'
import EstadoCarga from '@/components/EstadoCarga.vue'
import TarjetaVehiculo from '@/components/TarjetaVehiculo.vue'
import type { Paginado, Tarjeta } from '@/lib/tipos'

useHead({ title: 'Buscar vehículo' })
const route = useRoute()
const router = useRouter()
const aj = useAjustes()
const fav = useFavoritos()

const MULTI = ['marca', 'segmento', 'carroceria', 'combustible', 'transmision', 'traccion', 'adas', 'pais'] as const
const SIMPLE = ['q', 'precio_min', 'precio_max', 'anio_min', 'anio_max', 'plazas', 'despeje_min', 'baul_min', 'consumo_min', 'fiabilidad_min', 'sort', 'page'] as const
type Filtros = Record<(typeof MULTI)[number], string[]> & Record<(typeof SIMPLE)[number], string>
function desdeUrl(): Filtros {
  const q = route.query
  const f = {} as Filtros
  MULTI.forEach((k) => (f[k] = ([] as string[]).concat((q[k] as string | string[]) || [])))
  SIMPLE.forEach((k) => (f[k] = (q[k] as string) || ''))
  if (!f.sort) f.sort = 'puntaje'
  return f
}
const filtros = ref<Filtros>(desdeUrl())
const vista = ref<'grid' | 'lista'>('grid')
const panel = ref(false)
const soloFavoritos = computed(() => route.query.favoritos === '1')

const OPC = {
  marca: ['Audi', 'BMW', 'BYD', 'Chery', 'Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes-Benz', 'Nissan', 'Peugeot', 'Renault', 'Subaru', 'Suzuki', 'Toyota', 'Volkswagen'],
  carroceria: ['Sedán', 'Hatchback', 'SUV', 'Pickup', 'Coupé', 'Convertible'],
  segmento: ['Hatchback A', 'Hatchback B', 'Hatchback C', 'Sedán B', 'Sedán C', 'Sedán D', 'SUV Subcompacta', 'SUV Compacta', 'SUV Mediana', 'SUV Grande', 'Pickup Compacta', 'Pickup Mediana', 'Pickup Grande', 'Deportivo'],
  combustible: ['Gasolina Corriente', 'Gasolina Extra', 'Diésel', 'Híbrido Ligero MHEV', 'Híbrido Completo HEV', 'Híbrido Enchufable PHEV', '100% Eléctrico BEV'],
  transmision: ['Manual', 'Automática', 'CVT', 'Doble embrague', 'Reductora'],
  traccion: ['Delantera', 'Trasera', 'AWD', '4x4'],
  adas: ['Frenado autónomo de emergencia', 'Control crucero adaptativo', 'Asistente de mantenimiento de carril', 'Monitoreo de punto ciego', 'Cámara 360'],
  pais: ['Brasil', 'México', 'Colombia', 'Japón', 'Corea del Sur', 'China', 'India', 'Alemania', 'Estados Unidos', 'Tailandia', 'Argentina'],
}
const ORDENES = [
  { v: 'puntaje', t: 'Puntaje AutoVerdict' }, { v: 'precio_calle', t: 'Precio en calle: menor' }, { v: 'precio_calle_desc', t: 'Precio en calle: mayor' },
  { v: 'potencia', t: 'Potencia' }, { v: 'consumo', t: 'Consumo' }, { v: 'fiabilidad', t: 'Fiabilidad' }, { v: 'despeje', t: 'Despeje' }, { v: 'recientes', t: 'Más recientes' },
]
const factorMoneda = computed(() => (aj.moneda === 'USD' ? aj.trm : 1))

const { datos, cargando, error, ejecutar } = useCarga(async () => {
  const p: Record<string, unknown> = { ...filtros.value, size: 24, page: Number(filtros.value.page) || 1 }
  for (const k of ['precio_min', 'precio_max'] as const) if (filtros.value[k]) p[k] = Number(filtros.value[k]) * factorMoneda.value
  if (soloFavoritos.value) {
    if (!fav.ids.length) return { total: 0, page: 1, size: 24, paginas: 0, resultados: [], sugerencia: 'Aún no tienes favoritos: marca el corazón en cualquier tarjeta.' }
    p.ids = fav.ids
  }
  return api.get<Paginado<Tarjeta>>('/vehiculos', p as never)
})

function aUrl() {
  const q: Record<string, string | string[]> = {}
  for (const [k, v] of Object.entries(filtros.value)) if ((Array.isArray(v) && v.length) || (!Array.isArray(v) && v && !(k === 'sort' && v === 'puntaje'))) q[k] = v
  router.replace({ query: q })
}
const recargar = useDebounceFn(() => { filtros.value.page = ''; aUrl() }, 300)
watch(() => route.query, () => { filtros.value = desdeUrl(); ejecutar() })
onMounted(ejecutar)
const alternar = (k: (typeof MULTI)[number], v: string) => { const l = filtros.value[k]; const i = l.indexOf(v); if (i >= 0) l.splice(i, 1); else l.push(v); recargar() }
const pagina = (n: number) => { filtros.value.page = String(n); aUrl() }
const copiado = ref(false)
async function compartir() { try { await navigator.clipboard.writeText(location.href); copiado.value = true; setTimeout(() => (copiado.value = false), 2000) } catch { /* sin portapapeles */ } }
const nFiltros = computed(() => MULTI.reduce((a, k) => a + filtros.value[k].length, 0) + SIMPLE.filter((k) => !['q', 'sort', 'page'].includes(k) && filtros.value[k]).length)
</script>

<template>
  <div class="contenedor py-10">
    <h1 class="text-4xl font-semibold">{{ soloFavoritos ? 'Tus favoritos' : 'Buscar vehículo' }}</h1>
    <div class="mt-6 flex flex-wrap items-center gap-2">
      <label class="relative min-w-[16rem] flex-1">
        <span class="sr-only">Buscar por marca, modelo o versión</span>
        <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-tenue" aria-hidden="true" />
        <input v-model="filtros.q" type="search" class="campo pl-9" placeholder="Ej.: corolla cross, captiva, eléctrico…" @input="recargar" />
      </label>
      <button class="boton-secundario lg:hidden" :aria-expanded="panel" @click="panel = !panel"><SlidersHorizontal class="h-4 w-4" aria-hidden="true" /> Filtros ({{ nFiltros }})</button>
      <select v-model="filtros.sort" class="campo w-auto" aria-label="Ordenar por" @change="recargar"><option v-for="o in ORDENES" :key="o.v" :value="o.v">{{ o.t }}</option></select>
      <div class="flex" role="group" aria-label="Vista">
        <button :class="['grid h-11 w-11 place-items-center rounded-l-full border border-linea', vista === 'grid' ? 'bg-tinta text-papel' : '']" aria-label="Cuadrícula" @click="vista = 'grid'"><LayoutGrid class="h-4 w-4" aria-hidden="true" /></button>
        <button :class="['grid h-11 w-11 place-items-center rounded-r-full border border-linea', vista === 'lista' ? 'bg-tinta text-papel' : '']" aria-label="Lista" @click="vista = 'lista'"><List class="h-4 w-4" aria-hidden="true" /></button>
      </div>
      <button class="boton-secundario" @click="compartir"><Share2 class="h-4 w-4" aria-hidden="true" /> {{ copiado ? 'Enlace copiado' : 'Compartir' }}</button>
    </div>

    <div class="mt-6 grid gap-8 lg:grid-cols-[16rem_1fr]">
      <aside :class="['grid content-start gap-5 text-sm', panel ? '' : 'hidden lg:grid']" aria-label="Filtros">
        <fieldset v-for="k in (['marca', 'carroceria', 'segmento', 'combustible', 'transmision', 'traccion', 'adas', 'pais'] as const)" :key="k">
          <legend class="etiqueta mb-2">{{ { marca: 'Marca', carroceria: 'Carrocería', segmento: 'Segmento', combustible: 'Combustible', transmision: 'Transmisión', traccion: 'Tracción', adas: 'ADAS incluidas', pais: 'País de origen' }[k] }}</legend>
          <div class="flex flex-wrap gap-1">
            <button v-for="o in OPC[k]" :key="o" :class="['chip min-h-[32px] text-xs', filtros[k].includes(o) ? 'chip-activo' : '']" :aria-pressed="filtros[k].includes(o)" @click="alternar(k, o)">{{ o }}</button>
          </div>
        </fieldset>
        <fieldset>
          <legend class="etiqueta mb-2">Precio base ({{ aj.moneda }})</legend>
          <div class="flex gap-2"><input v-model="filtros.precio_min" class="campo" inputmode="numeric" placeholder="Mín." aria-label="Precio mínimo" @input="recargar" /><input v-model="filtros.precio_max" class="campo" inputmode="numeric" placeholder="Máx." aria-label="Precio máximo" @input="recargar" /></div>
        </fieldset>
        <fieldset>
          <legend class="etiqueta mb-2">Año</legend>
          <div class="flex gap-2"><input v-model="filtros.anio_min" class="campo" inputmode="numeric" placeholder="Desde" aria-label="Año desde" @input="recargar" /><input v-model="filtros.anio_max" class="campo" inputmode="numeric" placeholder="Hasta" aria-label="Año hasta" @input="recargar" /></div>
        </fieldset>
        <label>Plazas mínimas <input v-model="filtros.plazas" class="campo mt-1" inputmode="numeric" @input="recargar" /></label>
        <label>Despeje mínimo (mm) <input v-model="filtros.despeje_min" class="campo mt-1" inputmode="numeric" @input="recargar" /></label>
        <label>Baúl mínimo (L) <input v-model="filtros.baul_min" class="campo mt-1" inputmode="numeric" @input="recargar" /></label>
        <label>Consumo real mínimo (km/l) <input v-model="filtros.consumo_min" class="campo mt-1" inputmode="decimal" @input="recargar" /></label>
        <label>Fiabilidad mínima: <strong class="num">{{ filtros.fiabilidad_min || 1 }}</strong>
          <input v-model="filtros.fiabilidad_min" type="range" min="1" max="10" step="0.5" class="mt-1 w-full" @change="recargar" />
        </label>
        <button class="boton-secundario" @click="router.replace({ query: {} })">Limpiar filtros</button>
      </aside>

      <section aria-live="polite">
        <p v-if="datos" class="mb-4 text-sm text-tenue num">{{ datos.total }} versiones</p>
        <EstadoCarga :cargando="cargando" :error="error" :vacio="!!datos && !datos.total" :filas="6" @reintentar="ejecutar">
          <template #vacio><p class="text-sm text-tenue">{{ datos?.sugerencia }}</p></template>
          <div :class="vista === 'grid' ? 'grid gap-4 sm:grid-cols-2 xl:grid-cols-3' : 'grid gap-3'">
            <TarjetaVehiculo v-for="v in datos?.resultados" :key="v.id" :v="v" :lista="vista === 'lista'" />
          </div>
          <nav v-if="datos && datos.paginas > 1" class="mt-8 flex flex-wrap justify-center gap-1" aria-label="Paginación">
            <button v-for="n in datos.paginas" :key="n" :class="['chip num', n === datos.page ? 'chip-activo' : '']" :aria-current="n === datos.page ? 'page' : undefined" @click="pagina(n)">{{ n }}</button>
          </nav>
        </EstadoCarga>
      </section>
    </div>
  </div>
</template>
