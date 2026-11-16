<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { ArrowLeft } from 'lucide-vue-next'
import { api } from '@/lib/api'
import { useCarga } from '@/composables/useCarga'
import { useFormato } from '@/composables/useFormato'
import EstadoCarga from '@/components/EstadoCarga.vue'
import ImagenVehiculo from '@/components/ImagenVehiculo.vue'
import TarjetaVehiculo from '@/components/TarjetaVehiculo.vue'
import type { Paginado, Tarjeta } from '@/lib/tipos'

/** Un modelo (p. ej., Mazda 2 Sedán) con pestañas de año y, debajo, sus versiones de ese año. */
const route = useRoute()
const router = useRouter()
const f = useFormato()
const marca = computed(() => String(route.query.marca ?? ''))
const modelo = computed(() => String(route.query.modelo ?? ''))
const nombre = computed(() => `${marca.value} ${modelo.value}`.trim())
useHead({ title: nombre })

const { datos, cargando, error, ejecutar } = useCarga(() =>
  api.get<Paginado<Tarjeta>>('/vehiculos', { marca: marca.value, modelo: modelo.value, size: 100 }),
)
watch([marca, modelo], ejecutar, { immediate: true })

const anios = computed(() => [...new Set((datos.value?.resultados ?? []).map((v) => v.anio))].sort((a, b) => b - a))
/** Año activo: el de la URL si existe para este modelo; si no, el más reciente. */
const anio = computed(() => {
  const pedido = Number(route.query.anio)
  return anios.value.includes(pedido) ? pedido : anios.value[0]
})
const versiones = computed(() =>
  (datos.value?.resultados ?? []).filter((v) => v.anio === anio.value).sort((a, b) => a.precio_total_en_calle_cop - b.precio_total_en_calle_cop),
)
const muestra = computed(() => versiones.value[0])
const rango = computed(() => {
  const p = versiones.value.map((v) => v.precio_total_en_calle_cop)
  return p.length ? [Math.min(...p), Math.max(...p)] : null
})
function elegir(a: number) {
  router.replace({ query: { ...route.query, anio: String(a) } })
}
function volver() {
  if (window.history.state?.back) router.back()
  else router.push('/buscar')
}
</script>

<template>
  <div class="contenedor pagina">
    <button type="button" class="enlace-texto" @click="volver"><ArrowLeft class="h-4 w-4" aria-hidden="true" /> Volver a la búsqueda</button>

    <EstadoCarga :cargando="cargando" :error="error" :vacio="!!datos && !datos.total" :filas="3" @reintentar="ejecutar">
      <template #vacio>
        <h1 class="titulo-pagina mt-8">Modelo no encontrado</h1>
        <p class="entradilla">No tenemos versiones de «{{ nombre }}». <RouterLink to="/buscar" class="underline">Buscar otro vehículo</RouterLink>.</p>
      </template>

      <div v-if="muestra" class="mt-8 grid items-center gap-10 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)]">
        <ImagenVehiculo :medidas="muestra" :nombre="nombre" :imagen-id="muestra.imagen_id" credito />
        <div>
          <p class="etiqueta">{{ muestra.segmento }} · {{ muestra.carroceria }}</p>
          <h1 class="titulo-pagina mt-3">{{ nombre }}</h1>
          <p class="entradilla">
            <span class="num">{{ datos?.total }}</span> versiones entre {{ anios[anios.length - 1] }} y {{ anios[0] }}.
            Elige el año para ver las versiones de ese modelo.
          </p>
          <p v-if="rango" class="mt-6 num">
            <span class="etiqueta block">En calle en {{ anio }}</span>
            <span class="mt-1 block text-2xl font-bold text-tinta">
              {{ f.dinero(rango[0]) }}<template v-if="rango[1] !== rango[0]"> – {{ f.dinero(rango[1]) }}</template>
            </span>
          </p>
        </div>
      </div>

      <div v-if="anios.length" class="mt-14 flex flex-wrap gap-x-8 border-b border-linea" role="tablist" aria-label="Año del modelo">
        <button
          v-for="a in anios"
          :key="a"
          type="button"
          role="tab"
          :aria-selected="a === anio"
          :class="['pestana num', a === anio ? 'pestana-activa' : '']"
          @click="elegir(a)"
        >
          {{ a }}
        </button>
      </div>

      <section v-if="versiones.length" class="mt-10" :aria-label="`Versiones ${anio}`">
        <p class="etiqueta mb-6 num">{{ versiones.length }} {{ versiones.length === 1 ? 'versión' : 'versiones' }} en {{ anio }}</p>
        <div class="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
          <TarjetaVehiculo v-for="v in versiones" :key="v.id" :v="v" />
        </div>
      </section>
    </EstadoCarga>
  </div>
</template>
