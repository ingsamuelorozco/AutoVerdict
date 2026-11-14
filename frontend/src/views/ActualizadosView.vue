<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useHead } from '@unhead/vue'
import { ChevronDown, GitCompare } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { api } from '@/lib/api'
import { useCarga } from '@/composables/useCarga'
import { useFormato } from '@/composables/useFormato'
import { useComparador } from '@/stores/comparador'
import EstadoCarga from '@/components/EstadoCarga.vue'
import SliderAntesDespues from '@/components/SliderAntesDespues.vue'
import ImagenVehiculo from '@/components/ImagenVehiculo.vue'
import BadgeEstimado from '@/components/BadgeEstimado.vue'
import type { Tarjeta } from '@/lib/tipos'

useHead({ title: 'Vehículos actualizados' })
interface Cambio { categoria: string; elemento: string; antes: string; ahora: string; impacto: string }
interface Act { id: number; marca: string; modelo: string; anio_modelo: number; tipo: string; categorias: string[]; fecha_lanzamiento_colombia: string;
  titulo: string; resumen: string; cambios: Cambio[]; delta_precio_cop: number | null; vale_la_pena: string; razon_veredicto: string;
  vehiculos: Tarjeta[]; anterior: Tarjeta | null; segmento: string }
const TIPOS = ['Restyling o facelift', 'Nueva generación', 'Actualización mecánica', 'Actualización de equipamiento', 'Actualización tecnológica']
const CATEGORIAS = ['Estética', 'Funcional', 'Tecnología', 'Seguridad', 'Mecánica', 'Eficiencia']
const tipos = ref<string[]>([])
const cats = ref<string[]>([])
const marca = ref('')
const vista = ref<'tarjetas' | 'linea'>('tarjetas')
const abiertos = ref(new Set<number>())
const f = useFormato()
const comp = useComparador()
const router = useRouter()

const { datos, cargando, error, ejecutar } = useCarga(() => api.get<{ resultados: Act[] }>('/actualizados', { tipo: tipos.value, categoria: cats.value, marca: marca.value ? [marca.value] : [] }))
onMounted(ejecutar)
const alternar = (lista: string[], v: string) => { const i = lista.indexOf(v); if (i >= 0) lista.splice(i, 1); else lista.push(v); ejecutar() }
const marcas = computed(() => [...new Set((datos.value?.resultados || []).map((a) => a.marca))].sort())
const porMes = computed(() => {
  const g = new Map<string, Act[]>()
  for (const a of datos.value?.resultados || []) {
    const k = new Date(`${a.fecha_lanzamiento_colombia}T12:00:00`).toLocaleDateString('es-CO', { month: 'long', year: 'numeric' })
    g.set(k, [...(g.get(k) || []), a])
  }
  return [...g.entries()]
})
function compararConAnterior(a: Act) {
  if (!a.anterior) return
  comp.agregar(a.anterior.id)
  comp.agregar(a.vehiculos[0].id)
  router.push({ path: '/comparador', query: { ids: comp.ids.join(',') } })
}
const agrupados = (a: Act) => CATEGORIAS.map((c) => [c, a.cambios.filter((x) => x.categoria === c)] as const).filter(([, l]) => l.length)
</script>

<template>
  <div class="contenedor py-10">
    <h1 class="text-4xl font-semibold">Vehículos actualizados</h1>
    <p class="mt-2 max-w-2xl text-tenue">Qué cambió en cada modelo y si vale la pena el nuevo o conviene el anterior más barato.</p>

    <div class="mt-6 flex flex-wrap gap-2" role="group" aria-label="Tipo de actualización">
      <button v-for="t in TIPOS" :key="t" :class="['chip', tipos.includes(t) ? 'chip-activo' : '']" :aria-pressed="tipos.includes(t)" @click="alternar(tipos, t)">{{ t }}</button>
    </div>
    <div class="mt-2 flex flex-wrap items-center gap-2" role="group" aria-label="Categoría de cambio">
      <button v-for="c in CATEGORIAS" :key="c" :class="['chip', cats.includes(c) ? 'chip-activo' : '']" :aria-pressed="cats.includes(c)" @click="alternar(cats, c)">{{ c }}</button>
      <select v-model="marca" class="ml-auto rounded-full border border-linea bg-superficie px-3 py-2 text-sm" aria-label="Marca" @change="ejecutar">
        <option value="">Todas las marcas</option><option v-for="m in marcas" :key="m">{{ m }}</option>
      </select>
      <div class="flex gap-1" role="group" aria-label="Vista">
        <button :class="['chip', vista === 'tarjetas' ? 'chip-activo' : '']" @click="vista = 'tarjetas'">Tarjetas</button>
        <button :class="['chip', vista === 'linea' ? 'chip-activo' : '']" @click="vista = 'linea'">Línea de tiempo</button>
      </div>
    </div>

    <div class="mt-8">
      <EstadoCarga :cargando="cargando" :error="error" :vacio="!!datos && !datos.resultados.length" mensaje-vacio="No hay actualizaciones con esos filtros." @reintentar="ejecutar">
        <div v-if="vista === 'tarjetas'" class="grid gap-6 lg:grid-cols-2">
          <article v-for="a in datos?.resultados" :id="`act-${a.id}`" :key="a.id" class="tarjeta flex flex-col p-5">
            <SliderAntesDespues v-if="a.anterior" :etiqueta-antes="`${a.anterior.anio} ${a.anterior.version}`" :etiqueta-despues="`${a.vehiculos[0].anio} ${a.vehiculos[0].version}`">
              <template #antes><ImagenVehiculo :medidas="a.anterior" :nombre="`${a.marca} ${a.modelo} anterior`" /></template>
              <template #despues><ImagenVehiculo :medidas="a.vehiculos[0]" :nombre="`${a.marca} ${a.modelo} nuevo`" /></template>
            </SliderAntesDespues>
            <div class="mt-4 flex flex-wrap gap-1">
              <span class="chip min-h-0 py-0.5 text-xs">{{ a.tipo }}</span>
              <span v-for="c in a.categorias" :key="c" class="rounded-full bg-linea/60 px-2 py-0.5 text-xs">{{ c }}</span>
            </div>
            <h2 class="mt-3 text-xl font-semibold">{{ a.titulo }}</h2>
            <p class="mt-1 line-clamp-2 text-sm text-tenue">{{ a.resumen }}</p>
            <dl class="mt-4 grid grid-cols-2 gap-3 text-sm">
              <div><dt class="text-tenue">Diferencia de precio</dt><dd class="font-semibold num">{{ a.delta_precio_cop == null ? '—' : (a.delta_precio_cop > 0 ? '+' : '') + f.dinero(a.delta_precio_cop) }}<BadgeEstimado /></dd></div>
              <div><dt class="text-tenue">¿Vale la pena?</dt><dd :class="['font-semibold', a.vale_la_pena === 'Compra el nuevo' ? 'text-mejor' : a.vale_la_pena === 'El anterior es mejor negocio' ? 'text-ambar' : '']">{{ a.vale_la_pena }}</dd></div>
            </dl>
            <p class="mt-2 text-sm">{{ a.razon_veredicto }}</p>
            <button class="mt-4 flex min-h-[44px] items-center justify-between rounded-xl border border-linea px-3 text-sm" :aria-expanded="abiertos.has(a.id)" @click="abiertos.has(a.id) ? abiertos.delete(a.id) : abiertos.add(a.id)">
              Cambios por categoría <ChevronDown :class="['h-4 w-4 transition', abiertos.has(a.id) ? 'rotate-180' : '']" aria-hidden="true" />
            </button>
            <div v-if="abiertos.has(a.id)" class="mt-3 grid gap-3 text-sm">
              <div v-for="[cat, lista] in agrupados(a)" :key="cat">
                <p class="etiqueta">{{ cat }}</p>
                <ul class="mt-1 grid gap-2">
                  <li v-for="c in lista" :key="c.elemento" class="rounded-lg bg-papel p-2">
                    <strong>{{ c.elemento }}:</strong> {{ c.antes }} → <strong>{{ c.ahora }}</strong>
                    <p class="text-xs text-tenue">{{ c.impacto }}</p>
                  </li>
                </ul>
              </div>
            </div>
            <div class="mt-4 flex flex-wrap gap-2">
              <RouterLink :to="`/vehiculo/${a.vehiculos[0].slug}`" class="boton-secundario">Ver ficha</RouterLink>
              <button v-if="a.anterior" class="boton-primario" @click="compararConAnterior(a)"><GitCompare class="h-4 w-4" aria-hidden="true" /> Comparar con la versión anterior</button>
            </div>
          </article>
        </div>
        <ol v-else class="relative border-l border-linea pl-6">
          <li v-for="[mes, lista] in porMes" :key="mes" class="mb-8">
            <span class="absolute -left-1.5 mt-1.5 h-3 w-3 rounded-full bg-tinta" aria-hidden="true" />
            <h2 class="text-lg font-semibold capitalize">{{ mes }}</h2>
            <ul class="mt-2 grid gap-2">
              <li v-for="a in lista" :key="a.id"><a :href="`#act-${a.id}`" class="hover:underline" @click="vista = 'tarjetas'">{{ a.titulo }}</a> <span class="text-sm text-tenue">· {{ a.vale_la_pena }}</span></li>
            </ul>
          </li>
        </ol>
      </EstadoCarga>
    </div>
  </div>
</template>
