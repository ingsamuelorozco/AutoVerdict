<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useHead } from '@unhead/vue'
import { ArrowRight, ShieldAlert } from 'lucide-vue-next'
import LandingHero from '@/components/landing/LandingHero.vue'
import BuscadorRapido from '@/components/landing/BuscadorRapido.vue'
import SeccionCaracteristicas from '@/components/landing/SeccionCaracteristicas.vue'
import { api } from '@/lib/api'
import { T } from '@/lib/textos'
import { useFormato } from '@/composables/useFormato'
import type { Tarjeta } from '@/lib/tipos'

useHead({ title: undefined, meta: [{ property: 'og:title', content: `${T.marca} · ${T.lema}` }, { property: 'og:description', content: T.sublema }] })
const f = useFormato()

interface Imagen { id: string; url: string; autor: string; licencia: string; url_origen: string; uso: string; descripcion: string }
const imagenes = ref<Imagen[]>([])
const fallidas = ref(new Set<string>())

const actualizados = ref<{ id: number; titulo: string; resumen: string; vale_la_pena: string; marca: string; modelo: string; anio_modelo: number; fecha_lanzamiento_colombia: string }[]>([])
const rojas = ref<(Tarjeta & { linea_veredicto: string })[]>([])
/** Resumen del catálogo para el hero y el buscador rápido. */
const totalVersiones = ref<number | null>(null)
const marcas = ref<string[]>([])

onMounted(async () => {
  const [imgs, act, fia, cat, mar] = await Promise.allSettled([
    api.get<Imagen[]>('/config/imagenes'),
    api.get<{ resultados: typeof actualizados.value }>('/actualizados'),
    api.get<{ resultados: typeof rojas.value }>('/fiabilidad', { solo_alertas_rojas: true, limite: 40 }),
    api.get<{ total: number }>('/vehiculos', { size: 1 }),
    api.get<{ marca: string; versiones: number }[]>('/catalogo/marcas'),
  ])
  if (cat.status === 'fulfilled') totalVersiones.value = cat.value.total
  if (mar.status === 'fulfilled') marcas.value = mar.value.map((m) => m.marca)
  if (imgs.status === 'fulfilled') imagenes.value = imgs.value.filter((i) => i.uso === 'hero')
  if (act.status === 'fulfilled') actualizados.value = act.value.resultados.slice(0, 8)
  if (fia.status === 'fulfilled') {
    const vistos = new Set<string>()
    rojas.value = fia.value.resultados.filter((r) => !vistos.has(r.modelo) && vistos.add(r.modelo)).slice(0, 4)
  }
})
const visibles = computed(() => imagenes.value.filter((i) => !fallidas.value.has(i.id)))
/** La banda de cierre usa una foto fija distinta a la primera del hero. */
const fotoCierre = computed(() => visibles.value[visibles.value.length - 1])

</script>

<template>
  <LandingHero :versiones="totalVersiones" :marcas="marcas.length || null" />
  <BuscadorRapido :total="totalVersiones" :marcas="marcas" />
  <SeccionCaracteristicas />

  <!-- Recién actualizados: tarjetas tipo revista con filete -->
  <section v-if="actualizados.length" class="contenedor seccion" aria-labelledby="recien">
    <div class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <p class="etiqueta">Novedades</p>
        <h2 id="recien" class="titulo-seccion mt-3">Recién actualizados</h2>
      </div>
      <RouterLink to="/actualizados" class="enlace-texto">Ver todos <ArrowRight class="h-4 w-4" aria-hidden="true" /></RouterLink>
    </div>
    <div class="-mx-4 mt-10 flex snap-x gap-6 overflow-x-auto px-4 pb-4 sm:mx-0 sm:px-0">
      <RouterLink v-for="a in actualizados" :key="a.id" :to="`/actualizados#act-${a.id}`" class="tarjeta-plana flex w-80 shrink-0 snap-start flex-col p-6 transition-colors hover:border-tinta">
        <p class="etiqueta">{{ a.marca }} · {{ f.fecha(a.fecha_lanzamiento_colombia) }}</p>
        <h3 class="mt-3 text-xl">{{ a.titulo }}</h3>
        <p class="mt-3 line-clamp-3 text-sm text-tenue">{{ a.resumen }}</p>
        <p class="mt-auto border-t border-linea pt-4 text-sm"><span class="etiqueta mr-2">¿Vale la pena?</span><span class="text-tinta">{{ a.vale_la_pena }}</span></p>
      </RouterLink>
    </div>
  </section>

  <!-- Alertas rojas: puntaje como cifra protagonista -->
  <section v-if="rojas.length" class="banda-suave" aria-labelledby="rojas">
    <div class="contenedor seccion">
      <p class="etiqueta flex items-center gap-2"><ShieldAlert class="h-4 w-4 text-roja" aria-hidden="true" /> Fiabilidad</p>
      <h2 id="rojas" class="titulo-seccion mt-3">Alertas rojas</h2>
      <p class="entradilla">Los modelos con peor fiabilidad documentada. Nuestra promesa: decirlo antes de que pagues.</p>
      <div class="mt-10 grid gap-6 md:grid-cols-2">
        <RouterLink v-for="r in rojas" :key="r.id" :to="`/reviews/${r.slug}`" class="tarjeta group flex items-stretch transition-colors hover:border-tinta">
          <div class="flex w-28 shrink-0 flex-col items-center justify-center border-r border-linea p-4 text-center sm:w-36">
            <span class="text-display-sm text-roja num">{{ f.numero(r.puntaje_fiabilidad, 1) }}</span>
            <span class="etiqueta mt-1">de 10</span>
          </div>
          <div class="flex min-w-0 flex-col p-6">
            <h3 class="text-xl">{{ r.marca }} {{ r.modelo }}</h3>
            <p class="mb-4 mt-2 line-clamp-3 text-sm text-tenue">{{ r.linea_veredicto }}…</p>
            <span class="enlace-texto mt-auto">Leer review <ArrowRight class="h-4 w-4" aria-hidden="true" /></span>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>

  <!-- Banda de cierre con fotografía -->
  <section class="sobre-foto relative isolate overflow-hidden bg-black" aria-labelledby="cierre">
    <img v-if="fotoCierre" :src="fotoCierre.url" alt="" loading="lazy" decoding="async" class="absolute inset-0 -z-10 h-full w-full object-cover" @error="fallidas.add(fotoCierre.id)" />
    <div class="absolute inset-0 -z-10 bg-black/60" />
    <div class="contenedor flex flex-col items-center py-20 text-center lg:py-28">
      <h2 id="cierre" class="max-w-3xl text-display-sm lg:text-display-md">Antes de firmar, compáralo</h2>
      <p class="mt-4 max-w-xl text-lg text-cuerpo">Hasta 10 versiones lado a lado, con precio puesto en calle y fiabilidad.</p>
      <RouterLink to="/buscar" class="boton-primario mt-10 !bg-transparent hover:!bg-white">Buscar vehículo <ArrowRight class="h-4 w-4" aria-hidden="true" /></RouterLink>
    </div>
  </section>
</template>
