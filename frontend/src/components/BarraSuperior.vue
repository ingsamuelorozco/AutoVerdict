<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { onClickOutside } from '@vueuse/core'
import { ChevronDown, GitCompare, Heart, Menu, Moon, SlidersHorizontal, Sun, X } from 'lucide-vue-next'
import { useAjustes } from '@/stores/ajustes'
import { useComparador } from '@/stores/comparador'
import { useFavoritos } from '@/stores/favoritos'
import { T } from '@/lib/textos'

const aj = useAjustes()
const comp = useComparador()
const fav = useFavoritos()
const route = useRoute()
/** En la portada la barra flota transparente sobre el hero; en el resto queda fija arriba. */
const enInicio = computed(() => route.path === '/')
const herramientasAbierto = ref(false)
const lateralAbierto = ref(false)
const menuRef = ref<HTMLElement | null>(null)
onClickOutside(menuRef, () => (herramientasAbierto.value = false))
const ajustesAbierto = ref(false)
const ajustesRef = ref<HTMLElement | null>(null)
onClickOutside(ajustesRef, () => (ajustesAbierto.value = false))

function cambiarTrm(e: Event) {
  const v = Number((e.target as HTMLInputElement).value.replace(/\./g, '').replace(',', '.'))
  aj.fijarTrm(Number.isFinite(v) && v > 0 ? v : null)
}
const principales = [
  { to: '/', texto: T.navCorto.inicio },
  { to: '/actualizados', texto: T.navCorto.actualizados },
  { to: '/buscar', texto: T.navCorto.buscar },
  { to: '/comparador', texto: T.navCorto.comparador },
  { to: '/reviews', texto: T.navCorto.reviews },
]
</script>

<template>
  <header :class="['sobre-foto top-0 z-40 w-full', enInicio ? 'absolute inset-x-0 bg-transparent' : 'sticky bg-velo']">
    <a href="#contenido" class="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:bg-tinta focus:px-3 focus:py-2 focus:text-papel">Saltar al contenido</a>
    <div class="flex h-barra items-stretch pl-4 lg:pl-6">
      <RouterLink to="/" class="mr-10 flex shrink-0 items-center gap-2.5 text-xl font-bold uppercase tracking-[0.5px] text-tinta" aria-label="AutoVerdict, inicio">
        <img src="/favicon.svg" alt="" class="h-[30px] w-[30px]" width="30" height="30" />
        <span>{{ T.marca }}</span>
      </RouterLink>

      <nav class="hidden items-stretch gap-7 nav:flex" aria-label="Secciones principales">
        <RouterLink v-for="l in principales" :key="l.to" :to="l.to" class="enlace-barra" active-class="enlace-barra-activo">{{ l.texto }}<span class="enlace-barra-mas" aria-hidden="true">+</span></RouterLink>
        <div ref="menuRef" class="relative flex items-stretch">
          <button class="enlace-nav gap-1" :aria-expanded="herramientasAbierto" aria-haspopup="menu" @click="herramientasAbierto = !herramientasAbierto">
            {{ T.nav.herramientas }} <ChevronDown :class="['h-4 w-4 transition-transform', herramientasAbierto ? 'rotate-180' : '']" aria-hidden="true" />
          </button>
          <div v-if="herramientasAbierto" class="absolute left-0 top-full w-96 border border-t-0 border-linea bg-papel" role="menu">
            <div class="franja-m" aria-hidden="true" />
            <RouterLink v-for="h in T.herramientas" :key="h.ruta" :to="h.ruta" role="menuitem" class="block border-b border-linea px-6 py-4 transition-colors last:border-b-0 hover:bg-superficie" @click="herramientasAbierto = false">
              <span class="block text-sm font-bold uppercase tracking-[1px] text-tinta">{{ h.titulo }}</span>
              <span class="mt-1 block text-sm text-tenue">{{ h.desc }}</span>
            </RouterLink>
          </div>
        </div>
      </nav>

      <div class="ml-auto hidden h-full items-center gap-2 nav:flex">
        <!-- Ajustes regionales agrupados en un solo panel para despejar la barra -->
        <div ref="ajustesRef" class="relative flex h-full items-center">
          <button class="flex h-11 items-center gap-2 px-3 text-xs font-bold uppercase tracking-[1px] text-tinta transition-colors hover:bg-superficie" :aria-expanded="ajustesAbierto" aria-haspopup="dialog" aria-label="Moneda, TRM y ciudad" @click="ajustesAbierto = !ajustesAbierto">
            <SlidersHorizontal class="h-4 w-4" aria-hidden="true" /> {{ aj.moneda }}
          </button>
          <div v-if="ajustesAbierto" class="absolute right-0 top-full grid w-80 gap-5 border border-t-0 border-linea bg-papel p-6" role="dialog" aria-label="Ajustes regionales">
            <div>
              <p class="etiqueta">Moneda</p>
              <div class="mt-2 flex border border-linea" role="group" aria-label="Moneda">
                <button v-for="m in ['COP', 'USD'] as const" :key="m" :aria-pressed="aj.moneda === m" :class="['h-11 flex-1 text-xs font-bold tracking-maquinado transition-colors', aj.moneda === m ? 'bg-tinta text-papel' : 'text-tenue hover:text-tinta']" @click="aj.moneda = m; aj.guardar()">{{ m }}</button>
              </div>
            </div>
            <label class="etiqueta block" title="TRM editable: vacía el campo para volver a la oficial">
              TRM (pesos por dólar)
              <input :value="Math.round(aj.trm)" inputmode="decimal" class="campo mt-2 num" aria-label="TRM en pesos por dólar" @change="cambiarTrm" />
              <span class="mt-2 block text-xs font-light normal-case tracking-normal text-apagado">Vacía el campo para volver a la oficial.</span>
            </label>
            <label class="etiqueta block">
              Ciudad
              <select v-model="aj.ciudad" class="campo mt-2 normal-case tracking-normal" aria-label="Ciudad" @change="aj.guardar()">
                <option v-for="c in aj.ciudades" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </label>
          </div>
        </div>
        <button class="grid h-11 w-11 place-items-center rounded-full text-tinta transition-colors hover:bg-superficie" :aria-label="aj.tema === 'oscuro' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro'" @click="aj.alternarTema()">
          <Sun v-if="aj.tema === 'oscuro'" class="h-5 w-5" aria-hidden="true" /><Moon v-else class="h-5 w-5" aria-hidden="true" />
        </button>
        <RouterLink to="/buscar?favoritos=1" class="relative grid h-11 w-11 place-items-center rounded-full text-tinta transition-colors hover:bg-superficie" :aria-label="`Favoritos (${fav.ids.length})`">
          <Heart class="h-5 w-5" aria-hidden="true" />
          <span v-if="fav.ids.length" class="absolute right-0.5 top-0.5 grid h-4 min-w-4 place-items-center rounded-full bg-tinta px-1 text-[10px] font-bold text-papel num">{{ fav.ids.length }}</span>
        </RouterLink>
        <RouterLink :to="{ path: '/comparador', query: comp.ids.length ? { ids: comp.ids.join(',') } : {} }" class="boton-primario ml-2 min-h-[40px] px-5">
          <GitCompare class="h-4 w-4" aria-hidden="true" /> Comparar ({{ comp.ids.length }})
        </RouterLink>
      </div>

      <button class="ml-auto mr-2 grid h-11 w-11 place-items-center self-center text-tinta nav:hidden" aria-label="Abrir menú" @click="lateralAbierto = true"><Menu class="h-6 w-6" aria-hidden="true" /></button>
    </div>

    <!-- Menú móvil: hoja a pantalla completa con la franja M arriba -->
    <div v-if="lateralAbierto" class="fixed inset-0 z-50 flex flex-col overflow-y-auto bg-papel nav:hidden" role="dialog" aria-modal="true" aria-label="Menú">
      <div class="franja-m shrink-0" aria-hidden="true" />
      <div class="contenedor flex h-16 shrink-0 items-center justify-between border-b border-linea">
        <span class="text-lg font-bold uppercase tracking-[1px] text-tinta">{{ T.marca }}</span>
        <button class="grid h-11 w-11 place-items-center text-tinta" aria-label="Cerrar menú" @click="lateralAbierto = false"><X class="h-6 w-6" aria-hidden="true" /></button>
      </div>
      <div class="contenedor flex flex-col pb-10">
        <RouterLink v-for="l in principales" :key="l.to" :to="l.to" class="border-b border-linea py-5 text-2xl font-bold uppercase text-tinta" @click="lateralAbierto = false">{{ l.texto }}</RouterLink>
        <p class="etiqueta mt-8">{{ T.nav.herramientas }}</p>
        <RouterLink v-for="h in T.herramientas" :key="h.ruta" :to="h.ruta" class="border-b border-linea py-4 text-tinta" @click="lateralAbierto = false">{{ h.titulo }}</RouterLink>
        <RouterLink to="/buscar?favoritos=1" class="border-b border-linea py-4 text-tinta" @click="lateralAbierto = false">Favoritos ({{ fav.ids.length }})</RouterLink>
        <p class="etiqueta mt-8">Ajustes</p>
        <div class="mt-3 grid grid-cols-2 gap-4">
          <div class="col-span-2 flex border border-linea" role="group" aria-label="Moneda">
            <button v-for="m in ['COP', 'USD'] as const" :key="m" :aria-pressed="aj.moneda === m" :class="['h-12 flex-1 text-sm font-bold tracking-maquinado', aj.moneda === m ? 'bg-tinta text-papel' : 'text-tenue']" @click="aj.moneda = m; aj.guardar()">{{ m }}</button>
          </div>
          <label class="text-sm">TRM <input :value="Math.round(aj.trm)" class="campo mt-1 num" inputmode="decimal" @change="cambiarTrm" /></label>
          <label class="text-sm">Ciudad
            <select v-model="aj.ciudad" class="campo mt-1" @change="aj.guardar()"><option v-for="c in aj.ciudades" :key="c.id" :value="c.id">{{ c.nombre }}</option></select>
          </label>
          <button class="boton-secundario col-span-2" @click="aj.alternarTema()">Tema {{ aj.tema === 'oscuro' ? 'claro' : 'oscuro' }}</button>
        </div>
      </div>
    </div>
  </header>
</template>
