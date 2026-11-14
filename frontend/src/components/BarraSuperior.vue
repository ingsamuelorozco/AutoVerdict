<script setup lang="ts">
import { ref } from 'vue'
import { onClickOutside } from '@vueuse/core'
import { ChevronDown, GitCompare, Heart, Menu, Moon, Sun, X } from 'lucide-vue-next'
import { useAjustes } from '@/stores/ajustes'
import { useComparador } from '@/stores/comparador'
import { useFavoritos } from '@/stores/favoritos'
import { T } from '@/lib/textos'

const aj = useAjustes()
const comp = useComparador()
const fav = useFavoritos()
const herramientasAbierto = ref(false)
const lateralAbierto = ref(false)
const menuRef = ref<HTMLElement | null>(null)
onClickOutside(menuRef, () => (herramientasAbierto.value = false))

function cambiarTrm(e: Event) {
  const v = Number((e.target as HTMLInputElement).value.replace(/\./g, '').replace(',', '.'))
  aj.fijarTrm(Number.isFinite(v) && v > 0 ? v : null)
}
const principales = [
  { to: '/actualizados', texto: T.nav.actualizados },
  { to: '/buscar', texto: T.nav.buscar },
  { to: '/comparador', texto: T.nav.comparador },
]
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-linea bg-papel/90 backdrop-blur">
    <a href="#contenido" class="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:rounded focus:bg-tinta focus:px-3 focus:py-2 focus:text-papel">Saltar al contenido</a>
    <div class="contenedor flex h-16 items-center gap-4">
      <RouterLink to="/" class="flex items-center gap-2 font-titulo text-xl font-semibold" aria-label="AutoVerdict, inicio">
        <img src="/favicon.svg" alt="" class="h-7 w-7" width="28" height="28" />
        <span>{{ T.marca }}</span>
      </RouterLink>

      <nav class="mx-auto hidden items-center gap-1 lg:flex" aria-label="Secciones principales">
        <RouterLink v-for="l in principales" :key="l.to" :to="l.to" class="rounded-full px-4 py-2 text-sm font-medium hover:bg-linea/50" active-class="bg-tinta text-papel hover:bg-tinta">{{ l.texto }}</RouterLink>
      </nav>

      <div class="ml-auto hidden items-center gap-2 lg:flex">
        <RouterLink to="/reviews" class="rounded-full px-3 py-2 text-sm hover:bg-linea/50" active-class="font-semibold">{{ T.nav.reviews }}</RouterLink>
        <div ref="menuRef" class="relative">
          <button class="flex min-h-[44px] items-center gap-1 rounded-full px-3 text-sm hover:bg-linea/50" :aria-expanded="herramientasAbierto" aria-haspopup="menu" @click="herramientasAbierto = !herramientasAbierto">
            {{ T.nav.herramientas }} <ChevronDown class="h-4 w-4" aria-hidden="true" />
          </button>
          <div v-if="herramientasAbierto" class="tarjeta absolute right-0 mt-2 w-80 p-2 shadow-xl" role="menu">
            <RouterLink v-for="h in T.herramientas" :key="h.ruta" :to="h.ruta" role="menuitem" class="block rounded-xl p-3 hover:bg-linea/40" @click="herramientasAbierto = false">
              <span class="block text-sm font-medium">{{ h.titulo }}</span>
              <span class="block text-xs text-tenue">{{ h.desc }}</span>
            </RouterLink>
          </div>
        </div>
        <div class="flex items-center gap-1 rounded-full border border-linea p-1 text-xs" role="group" aria-label="Moneda">
          <button v-for="m in ['COP', 'USD'] as const" :key="m" :aria-pressed="aj.moneda === m" :class="['rounded-full px-2 py-1', aj.moneda === m ? 'bg-tinta text-papel' : '']" @click="aj.moneda = m; aj.guardar()">{{ m }}</button>
        </div>
        <label class="flex items-center gap-1 text-xs text-tenue" title="TRM editable: vacía el campo para volver a la oficial">
          TRM
          <input :value="Math.round(aj.trm)" inputmode="decimal" class="w-16 rounded-md border border-linea bg-superficie px-1 py-1 text-tinta num" aria-label="TRM en pesos por dólar" @change="cambiarTrm" />
        </label>
        <select v-model="aj.ciudad" class="rounded-full border border-linea bg-superficie px-2 py-2 text-xs" aria-label="Ciudad" @change="aj.guardar()">
          <option v-for="c in aj.ciudades" :key="c.id" :value="c.id">{{ c.nombre }}</option>
        </select>
        <button class="grid h-11 w-11 place-items-center rounded-full hover:bg-linea/50" :aria-label="aj.tema === 'oscuro' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro'" @click="aj.alternarTema()">
          <Sun v-if="aj.tema === 'oscuro'" class="h-5 w-5" aria-hidden="true" /><Moon v-else class="h-5 w-5" aria-hidden="true" />
        </button>
        <RouterLink to="/buscar?favoritos=1" class="relative grid h-11 w-11 place-items-center rounded-full hover:bg-linea/50" :aria-label="`Favoritos (${fav.ids.length})`">
          <Heart class="h-5 w-5" aria-hidden="true" />
          <span v-if="fav.ids.length" class="absolute right-1 top-1 rounded-full bg-roja px-1 text-[10px] text-white num">{{ fav.ids.length }}</span>
        </RouterLink>
        <RouterLink :to="{ path: '/comparador', query: comp.ids.length ? { ids: comp.ids.join(',') } : {} }" class="boton-primario h-10 min-h-0 px-4">
          <GitCompare class="h-4 w-4" aria-hidden="true" /> Comparar ({{ comp.ids.length }})
        </RouterLink>
      </div>

      <button class="ml-auto grid h-11 w-11 place-items-center rounded-full lg:hidden" aria-label="Abrir menú" @click="lateralAbierto = true"><Menu class="h-6 w-6" aria-hidden="true" /></button>
    </div>

    <div v-if="lateralAbierto" class="fixed inset-0 z-50 lg:hidden" role="dialog" aria-modal="true" aria-label="Menú">
      <div class="absolute inset-0 bg-black/40" @click="lateralAbierto = false" />
      <aside class="absolute right-0 top-0 flex h-full w-80 max-w-[85vw] flex-col gap-4 overflow-y-auto bg-papel p-5">
        <button class="ml-auto grid h-11 w-11 place-items-center" aria-label="Cerrar menú" @click="lateralAbierto = false"><X class="h-6 w-6" aria-hidden="true" /></button>
        <RouterLink to="/reviews" class="text-lg font-medium" @click="lateralAbierto = false">{{ T.nav.reviews }}</RouterLink>
        <p class="etiqueta">{{ T.nav.herramientas }}</p>
        <RouterLink v-for="h in T.herramientas" :key="h.ruta" :to="h.ruta" class="py-1" @click="lateralAbierto = false">{{ h.titulo }}</RouterLink>
        <p class="etiqueta">Ajustes</p>
        <div class="flex gap-2">
          <button v-for="m in ['COP', 'USD'] as const" :key="m" :class="['chip', aj.moneda === m ? 'chip-activo' : '']" @click="aj.moneda = m; aj.guardar()">{{ m }}</button>
        </div>
        <label class="text-sm">TRM <input :value="Math.round(aj.trm)" class="campo mt-1" inputmode="decimal" @change="cambiarTrm" /></label>
        <label class="text-sm">Ciudad
          <select v-model="aj.ciudad" class="campo mt-1" @change="aj.guardar()"><option v-for="c in aj.ciudades" :key="c.id" :value="c.id">{{ c.nombre }}</option></select>
        </label>
        <button class="boton-secundario" @click="aj.alternarTema()">Tema {{ aj.tema === 'oscuro' ? 'claro' : 'oscuro' }}</button>
        <RouterLink to="/buscar?favoritos=1" class="py-1" @click="lateralAbierto = false">Favoritos ({{ fav.ids.length }})</RouterLink>
      </aside>
    </div>
  </header>
</template>
