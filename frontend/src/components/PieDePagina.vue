<script setup lang="ts">
import { T } from '@/lib/textos'

const columnas = [
  { titulo: 'Explorar', enlaces: [{ to: '/buscar', t: T.nav.buscar }, { to: '/comparador', t: T.nav.comparador }, { to: '/actualizados', t: T.nav.actualizados }, { to: '/reviews', t: T.nav.reviews }] },
  { titulo: T.nav.herramientas, enlaces: T.herramientas.map((h) => ({ to: h.ruta, t: h.titulo })) },
  { titulo: 'Transparencia', enlaces: [{ to: '/metodologia', t: 'Metodología y fuentes' }, { to: '/creditos', t: 'Créditos de fotos' }] },
]
</script>

<template>
  <footer class="bg-papel pb-24 text-sm text-tenue lg:pb-0">
    <div class="franja-m" aria-hidden="true" />
    <div class="contenedor grid gap-x-6 gap-y-10 py-16 sm:grid-cols-2 lg:grid-cols-4">
      <div>
        <p class="text-lg font-bold uppercase tracking-[1px] text-tinta">{{ T.marca }}</p>
        <p class="mt-3 max-w-xs">{{ T.lema }}.</p>
      </div>
      <nav v-for="c in columnas" :key="c.titulo" :aria-label="c.titulo">
        <p class="etiqueta !text-tinta">{{ c.titulo }}</p>
        <ul class="mt-4 grid gap-3">
          <li v-for="e in c.enlaces" :key="e.to"><RouterLink :to="e.to" class="transition-colors hover:text-tinta">{{ e.t }}</RouterLink></li>
          <li v-if="c.titulo === 'Transparencia'"><a :href="T.repo" class="transition-colors hover:text-tinta" target="_blank" rel="noopener">Repositorio en GitHub</a></li>
        </ul>
      </nav>
    </div>
    <div class="border-t border-linea">
      <p class="contenedor py-6 text-xs leading-relaxed tracking-[0.5px] text-apagado"><strong class="text-tenue">Aviso legal.</strong> {{ T.avisoLegal }}</p>
    </div>
  </footer>
</template>
