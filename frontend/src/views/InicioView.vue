<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useHead } from '@unhead/vue'
import { usePreferredReducedMotion } from '@vueuse/core'
import { ArrowRight, Calculator, Gauge, ParkingSquare, Shield, ShieldAlert, Wallet } from 'lucide-vue-next'
import { api } from '@/lib/api'
import { T } from '@/lib/textos'
import { useFormato } from '@/composables/useFormato'
import type { Tarjeta } from '@/lib/tipos'

useHead({ title: undefined, meta: [{ property: 'og:title', content: `${T.marca} · ${T.lema}` }, { property: 'og:description', content: T.sublema }] })
const f = useFormato()

interface Imagen { id: string; url: string; autor: string; licencia: string; url_origen: string; uso: string; descripcion: string }
const imagenes = ref<Imagen[]>([])
const actual = ref(0)
const fallidas = ref(new Set<string>())
const movimiento = usePreferredReducedMotion()
let temporizador: ReturnType<typeof setInterval> | undefined

const actualizados = ref<{ id: number; titulo: string; resumen: string; vale_la_pena: string; marca: string; modelo: string; anio_modelo: number; fecha_lanzamiento_colombia: string }[]>([])
const rojas = ref<(Tarjeta & { linea_veredicto: string })[]>([])

onMounted(async () => {
  const [imgs, act, fia] = await Promise.allSettled([
    api.get<Imagen[]>('/config/imagenes'),
    api.get<{ resultados: typeof actualizados.value }>('/actualizados'),
    api.get<{ resultados: typeof rojas.value }>('/fiabilidad', { solo_alertas_rojas: true, limite: 40 }),
  ])
  if (imgs.status === 'fulfilled') imagenes.value = imgs.value.filter((i) => i.uso === 'hero')
  if (act.status === 'fulfilled') actualizados.value = act.value.resultados.slice(0, 8)
  if (fia.status === 'fulfilled') {
    const vistos = new Set<string>()
    rojas.value = fia.value.resultados.filter((r) => !vistos.has(r.modelo) && vistos.add(r.modelo)).slice(0, 4)
  }
  temporizador = setInterval(() => {
    if (imagenes.value.length) actual.value = (actual.value + 1) % imagenes.value.length
  }, 6000)
})
onUnmounted(() => clearInterval(temporizador))
const visibles = computed(() => imagenes.value.filter((i) => !fallidas.value.has(i.id)))

const pasos = [
  { n: 1, t: 'Elige hasta 10 vehículos', d: 'Por marca, modelo, año y versión exacta.' },
  { n: 2, t: 'Analiza lo que importa', d: 'Ganadores automáticos, dimensiones reales y costo puesto en calle en COP y USD.' },
  { n: 3, t: 'Lee el veredicto sin filtro', d: 'Fallas conocidas, recalls y para quién no es, antes de pagar.' },
]
const herramientas = [
  { to: '/herramientas/credito', icono: Calculator, t: 'Crédito', d: 'Cuota real, intereses y el costo de alargar el plazo.' },
  { to: '/herramientas/seguro', icono: Shield, t: 'Seguro', d: 'SOAT oficial 2026 y rango del todo riesgo.' },
  { to: '/herramientas/costo-total', icono: Wallet, t: 'Costo total a 5 años', d: 'Cuánto te cuesta por mes y por kilómetro.' },
  { to: '/comparador', icono: ParkingSquare, t: 'Huella en garaje', d: 'Siluetas a escala contra una plaza de 5,00 × 2,40 m.' },
]
</script>

<template>
  <section class="relative isolate min-h-[78vh] overflow-hidden bg-gradient-to-br from-[#26231c] via-[#17150f] to-[#0c0b08] text-[#f4f1ea]">
    <template v-for="(img, i) in visibles" :key="img.id">
      <img
        :src="img.url"
        :alt="img.descripcion"
        :loading="i === 0 ? 'eager' : 'lazy'"
        :fetchpriority="i === 0 ? 'high' : 'auto'"
        decoding="async"
        :class="['absolute inset-0 -z-10 h-full w-full object-cover transition-opacity duration-[1500ms]', i === actual % visibles.length ? 'opacity-60' : 'opacity-0', movimiento === 'no-preference' ? 'kenburns' : '']"
        @error="fallidas.add(img.id)"
      />
    </template>
    <div class="absolute inset-0 -z-10 bg-gradient-to-t from-black/80 via-black/30 to-black/40" />
    <svg class="absolute bottom-0 right-0 -z-10 w-2/3 opacity-10" viewBox="0 0 400 120" aria-hidden="true"><path d="M10 100 L60 90 L120 60 L240 55 L300 75 L380 80 L390 100 Z" fill="currentColor" /></svg>
    <div class="contenedor flex min-h-[78vh] flex-col justify-end pb-16 pt-24">
      <p class="etiqueta !text-[#f4f1ea]/70">Colombia · {{ new Date().getFullYear() }}</p>
      <h1 class="mt-3 max-w-4xl text-5xl font-semibold leading-[1.02] sm:text-7xl">{{ T.lema }}</h1>
      <p class="mt-5 max-w-2xl text-lg text-[#f4f1ea]/80">{{ T.sublema }}</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <RouterLink to="/comparador" class="boton bg-[#f4f1ea] text-[#17150f] hover:opacity-90">Comparar vehículos <ArrowRight class="h-4 w-4" aria-hidden="true" /></RouterLink>
        <RouterLink to="/reviews" class="boton border border-[#f4f1ea]/40 hover:border-[#f4f1ea]">Buscar reviews honestas</RouterLink>
      </div>
      <p v-if="visibles.length" class="mt-10 text-xs text-[#f4f1ea]/50">
        Foto: <a :href="visibles[actual % visibles.length].url_origen" class="underline" target="_blank" rel="noopener">{{ visibles[actual % visibles.length].autor }}</a>, {{ visibles[actual % visibles.length].licencia }} · <RouterLink to="/creditos" class="underline">créditos</RouterLink>
      </p>
    </div>
  </section>

  <section class="contenedor mt-20" aria-labelledby="como">
    <h2 id="como" class="text-3xl font-semibold">Cómo funciona</h2>
    <ol class="mt-8 grid gap-6 md:grid-cols-3">
      <li v-for="p in pasos" :key="p.n" class="tarjeta p-6">
        <span class="font-titulo text-5xl text-tenue num">0{{ p.n }}</span>
        <h3 class="mt-4 text-xl font-semibold">{{ p.t }}</h3>
        <p class="mt-2 text-tenue">{{ p.d }}</p>
      </li>
    </ol>
  </section>

  <section class="contenedor mt-20" aria-labelledby="herr">
    <h2 id="herr" class="text-3xl font-semibold">Herramientas que no verás en otros sitios</h2>
    <div class="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <RouterLink v-for="h in herramientas" :key="h.to" :to="h.to" class="tarjeta group p-6 transition hover:border-tinta">
        <component :is="h.icono" class="h-7 w-7" aria-hidden="true" />
        <h3 class="mt-4 text-lg font-semibold">{{ h.t }}</h3>
        <p class="mt-1 text-sm text-tenue">{{ h.d }}</p>
        <span class="mt-4 inline-flex items-center gap-1 text-sm font-medium">Abrir <ArrowRight class="h-4 w-4 transition group-hover:translate-x-1" aria-hidden="true" /></span>
      </RouterLink>
    </div>
  </section>

  <section v-if="actualizados.length" class="contenedor mt-20" aria-labelledby="recien">
    <div class="flex items-end justify-between">
      <h2 id="recien" class="text-3xl font-semibold">Recién actualizados</h2>
      <RouterLink to="/actualizados" class="text-sm underline">Ver todos</RouterLink>
    </div>
    <div class="mt-6 flex snap-x gap-4 overflow-x-auto pb-4">
      <RouterLink v-for="a in actualizados" :key="a.id" :to="`/actualizados#act-${a.id}`" class="tarjeta w-72 shrink-0 snap-start p-5 hover:border-tinta">
        <p class="etiqueta">{{ a.marca }} · {{ f.fecha(a.fecha_lanzamiento_colombia) }}</p>
        <h3 class="mt-2 font-semibold">{{ a.titulo }}</h3>
        <p class="mt-2 line-clamp-2 text-sm text-tenue">{{ a.resumen }}</p>
        <p class="mt-3 text-sm font-medium">¿Vale la pena? {{ a.vale_la_pena }}</p>
      </RouterLink>
    </div>
  </section>

  <section v-if="rojas.length" class="contenedor mt-20" aria-labelledby="rojas">
    <h2 id="rojas" class="flex items-center gap-2 text-3xl font-semibold"><ShieldAlert class="h-8 w-8 text-roja" aria-hidden="true" /> Alertas rojas</h2>
    <p class="mt-2 max-w-2xl text-tenue">Los modelos con peor fiabilidad documentada. Nuestra promesa: decirlo antes de que pagues.</p>
    <div class="mt-6 grid gap-4 md:grid-cols-2">
      <RouterLink v-for="r in rojas" :key="r.id" :to="`/reviews/${r.slug}`" class="tarjeta flex gap-4 border-roja/40 p-5 hover:border-roja">
        <Gauge class="h-8 w-8 shrink-0 text-roja" aria-hidden="true" />
        <div>
          <h3 class="font-semibold">{{ r.marca }} {{ r.modelo }} <span class="text-roja num">· {{ f.numero(r.puntaje_fiabilidad, 1) }}/10</span></h3>
          <p class="mt-1 text-sm text-tenue">{{ r.linea_veredicto }}…</p>
        </div>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
@keyframes kenburns { from { transform: scale(1.02) } to { transform: scale(1.12) translate(-1%, -1%) } }
.kenburns { animation: kenburns 14s ease-in-out infinite alternate; }
</style>
