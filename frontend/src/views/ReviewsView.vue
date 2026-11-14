<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useHead } from '@unhead/vue'
import { useDebounceFn } from '@vueuse/core'
import { Search, ShieldAlert } from 'lucide-vue-next'
import { api } from '@/lib/api'
import { useCarga } from '@/composables/useCarga'
import { useFormato } from '@/composables/useFormato'
import EstadoCarga from '@/components/EstadoCarga.vue'
import MedidorFiabilidad from '@/components/MedidorFiabilidad.vue'
import type { Alerta, Tarjeta } from '@/lib/tipos'

useHead({ title: 'Reviews honestas' })
const f = useFormato()
type Fila = Tarjeta & { etiqueta_fiabilidad: string; linea_veredicto: string; nivel_costo_mantenimiento: string; depreciacion_estimada: string; alertas: Alerta[] }
const q = ref('')
const marca = ref('')
const minimo = ref(1)
const maximo = ref(10)
const mant = ref('')
const dep = ref('')
const soloRojas = ref(false)
const { datos, cargando, error, ejecutar } = useCarga(() => api.get<{ total: number; resultados: Fila[] }>('/fiabilidad', {
  q: q.value, marca: marca.value ? [marca.value] : [], puntaje_min: minimo.value, puntaje_max: maximo.value,
  mantenimiento: mant.value ? [mant.value] : [], depreciacion: dep.value ? [dep.value] : [], solo_alertas_rojas: soloRojas.value, limite: 120,
}))
const buscar = useDebounceFn(ejecutar, 150)
onMounted(ejecutar)
watch([marca, minimo, maximo, mant, dep, soloRojas], ejecutar)
const MARCAS = ['Audi', 'BMW', 'BYD', 'Chery', 'Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes-Benz', 'Nissan', 'Peugeot', 'Renault', 'Subaru', 'Suzuki', 'Toyota', 'Volkswagen']
</script>

<template>
  <div class="contenedor py-10">
    <h1 class="text-4xl font-semibold">Reviews honestas</h1>
    <p class="mt-2 max-w-2xl text-tenue">Fallas documentadas con fuentes, costos de tenerlo y para quién no es cada carro. Opinión editorial rotulada como tal.</p>
    <label class="relative mt-6 block max-w-2xl">
      <span class="sr-only">Buscar review</span>
      <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-tenue" aria-hidden="true" />
      <input v-model="q" type="search" class="campo pl-9" placeholder="Busca un modelo: captiva, hilux, fiesta…" @input="buscar" />
    </label>
    <div class="mt-4 flex flex-wrap items-center gap-2 text-sm">
      <select v-model="marca" class="rounded-full border border-linea bg-superficie px-3 py-2" aria-label="Marca"><option value="">Todas las marcas</option><option v-for="m in MARCAS" :key="m">{{ m }}</option></select>
      <label class="flex items-center gap-1">Puntaje <input v-model.number="minimo" type="number" min="1" max="10" step="0.5" class="w-16 rounded-lg border border-linea bg-superficie px-2 py-1 num" aria-label="Puntaje mínimo" /> a <input v-model.number="maximo" type="number" min="1" max="10" step="0.5" class="w-16 rounded-lg border border-linea bg-superficie px-2 py-1 num" aria-label="Puntaje máximo" /></label>
      <select v-model="mant" class="rounded-full border border-linea bg-superficie px-3 py-2" aria-label="Costo de mantenimiento"><option value="">Mantenimiento: todos</option><option v-for="m in ['Bajo', 'Moderado', 'Alto', 'Muy Alto']" :key="m">{{ m }}</option></select>
      <select v-model="dep" class="rounded-full border border-linea bg-superficie px-3 py-2" aria-label="Retención de valor"><option value="">Reventa: todas</option><option v-for="m in ['Baja - Alta reventa', 'Media', 'Alta - Se desvaloriza rápido']" :key="m">{{ m }}</option></select>
      <label class="flex min-h-[44px] items-center gap-2"><input v-model="soloRojas" type="checkbox" class="h-4 w-4" /> Únicamente alertas rojas</label>
    </div>
    <div class="mt-8" aria-live="polite">
      <EstadoCarga :cargando="cargando && !datos" :error="error" :vacio="!!datos && !datos.total" @reintentar="ejecutar">
        <p class="mb-3 text-sm text-tenue num">{{ datos?.total }} reseñas</p>
        <ul class="grid gap-3 md:grid-cols-2">
          <li v-for="r in datos?.resultados" :key="r.id">
            <RouterLink :to="`/reviews/${r.slug}`" :class="['tarjeta flex items-center gap-4 p-4 hover:border-tinta', r.tiene_alerta_roja ? 'border-roja/60' : '']">
              <MedidorFiabilidad :puntaje="r.puntaje_fiabilidad" :tamano="96" :etiqueta="r.etiqueta_fiabilidad" />
              <div class="min-w-0">
                <p v-if="r.tiene_alerta_roja" class="mb-1 inline-flex items-center gap-1 rounded bg-roja px-2 py-0.5 text-xs font-semibold text-white"><ShieldAlert class="h-3 w-3" aria-hidden="true" /> Alerta roja</p>
                <h2 class="font-semibold">{{ r.marca }} {{ r.modelo }} {{ r.anio }}</h2>
                <p class="truncate text-xs text-tenue">{{ r.version }} · Mantenimiento {{ r.nivel_costo_mantenimiento }} · {{ f.dinero(r.precio_base_cop) }}</p>
                <p class="mt-1 line-clamp-2 text-sm">{{ r.linea_veredicto }}…</p>
              </div>
            </RouterLink>
          </li>
        </ul>
      </EstadoCarga>
    </div>
  </div>
</template>
