<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useHead } from '@unhead/vue'
import { usePreferredReducedMotion } from '@vueuse/core'
import { ArrowRight, Calculator, ParkingSquare, Shield, ShieldAlert, Wallet } from 'lucide-vue-next'
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
const fotoActual = computed(() => visibles.value[actual.value % (visibles.value.length || 1)])
/** La banda de cierre usa una foto fija distinta a la primera del hero. */
const fotoCierre = computed(() => visibles.value[visibles.value.length - 1])

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
  <!-- Banda hero: la fotografía a sangre completa es la banda; sin marco ni degradado decorativo -->
  <section class="sobre-foto relative isolate min-h-[calc(100vh-4rem)] overflow-hidden bg-black lg:min-h-[86vh]">
    <template v-for="(img, i) in visibles" :key="img.id">
      <img
        :src="img.url"
        :alt="img.descripcion"
        :loading="i === 0 ? 'eager' : 'lazy'"
        :fetchpriority="i === 0 ? 'high' : 'auto'"
        decoding="async"
        :class="['absolute inset-0 -z-10 h-full w-full object-cover transition-opacity duration-[1500ms]', i === actual % visibles.length ? 'opacity-100' : 'opacity-0', movimiento === 'no-preference' ? 'kenburns' : '']"
        @error="fallidas.add(img.id)"
      />
    </template>
    <!-- Velo de legibilidad sobre la foto (no es un fondo decorativo) -->
    <div class="absolute inset-0 -z-10 bg-gradient-to-t from-black via-black/55 to-black/30 lg:bg-gradient-to-r lg:from-black/85 lg:via-black/45 lg:to-transparent" />
    <div class="contenedor flex min-h-[calc(100vh-4rem)] flex-col justify-end pb-16 pt-24 lg:min-h-[86vh]">
      <div class="franja-m-corta" aria-hidden="true" />
      <p class="etiqueta mt-6">Colombia · {{ new Date().getFullYear() }}</p>
      <h1 class="mt-4 max-w-5xl text-[44px] leading-none sm:text-[64px] lg:text-display-xl">{{ T.lema }}</h1>
      <p class="mt-6 max-w-xl text-lg text-cuerpo">{{ T.sublema }}</p>
      <div class="mt-10 flex flex-col gap-4 sm:flex-row">
        <RouterLink to="/comparador" class="boton-solido">Comparar vehículos <ArrowRight class="h-4 w-4" aria-hidden="true" /></RouterLink>
        <RouterLink to="/reviews" class="boton-primario !bg-transparent hover:!bg-white">Buscar reviews honestas</RouterLink>
      </div>
      <div class="mt-12 flex flex-wrap items-center justify-between gap-4">
        <div v-if="visibles.length > 1" class="flex gap-2" role="group" aria-label="Fotografías del encabezado">
          <button v-for="(img, i) in visibles" :key="img.id" class="group/p flex h-11 items-center" :aria-label="`Ver foto ${i + 1} de ${visibles.length}`" :aria-current="i === actual % visibles.length" @click="actual = i">
            <span :class="['block h-0.5 w-10 transition-colors', i === actual % visibles.length ? 'bg-white' : 'bg-white/30 group-hover/p:bg-white/60']" />
          </button>
        </div>
        <p v-if="fotoActual" class="text-xs tracking-[0.5px] text-apagado">
          Foto: <a :href="fotoActual.url_origen" class="underline hover:text-white" target="_blank" rel="noopener">{{ fotoActual.autor }}</a>, {{ fotoActual.licencia }} · <RouterLink to="/creditos" class="underline hover:text-white">créditos</RouterLink>
        </p>
      </div>
    </div>
  </section>

  <!-- Cómo funciona: celdas de dato sobre lienzo -->
  <section class="contenedor seccion" aria-labelledby="como">
    <p class="etiqueta">El método</p>
    <h2 id="como" class="titulo-seccion mt-3">Cómo funciona</h2>
    <ol class="mt-10 grid gap-px border border-linea bg-linea md:grid-cols-3">
      <li v-for="p in pasos" :key="p.n" class="celda-dato lg:p-10">
        <span class="text-display-md text-apagado num" aria-hidden="true">0{{ p.n }}</span>
        <h3 class="mt-6 text-2xl">{{ p.t }}</h3>
        <p class="mt-3 text-tenue">{{ p.d }}</p>
      </li>
    </ol>
  </section>

  <!-- Herramientas: rejilla de tarjetas sobre banda suave -->
  <section class="banda-suave" aria-labelledby="herr">
    <div class="contenedor seccion">
      <p class="etiqueta">Calculadoras</p>
      <h2 id="herr" class="titulo-seccion mt-3 max-w-3xl">Herramientas que no verás en otros sitios</h2>
      <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <RouterLink v-for="h in herramientas" :key="h.to" :to="h.to" class="tarjeta group flex flex-col p-6 transition-colors hover:border-tinta lg:p-8">
          <component :is="h.icono" class="h-8 w-8 text-tinta" :stroke-width="1.5" aria-hidden="true" />
          <h3 class="mt-8 text-2xl">{{ h.t }}</h3>
          <p class="mb-8 mt-2 text-tenue">{{ h.d }}</p>
          <span class="enlace-texto mt-auto">Abrir <ArrowRight class="h-4 w-4" aria-hidden="true" /></span>
        </RouterLink>
      </div>
    </div>
  </section>

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

<style scoped>
@keyframes kenburns { from { transform: scale(1.02) } to { transform: scale(1.1) translate(-1%, -1%) } }
.kenburns { animation: kenburns 14s ease-in-out infinite alternate; }
</style>
