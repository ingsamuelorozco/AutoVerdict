<script setup lang="ts">
import { T } from '@/lib/textos'
</script>

<template>
  <footer class="mt-24 border-t border-linea pb-24 pt-10 lg:pb-10">
    <div class="contenedor grid gap-8 text-sm md:grid-cols-3">
      <div>
        <p class="font-titulo text-lg font-semibold">{{ T.marca }}</p>
        <p class="mt-2 text-tenue">{{ T.lema }}.</p>
      </div>
      <nav class="grid gap-2" aria-label="Pie de página">
        <RouterLink to="/metodologia" class="hover:underline">Metodología y fuentes</RouterLink>
        <RouterLink to="/creditos" class="hover:underline">Créditos de fotos</RouterLink>
        <a :href="T.repo" class="hover:underline" target="_blank" rel="noopener">Repositorio en GitHub</a>
      </nav>
      <p class="text-xs leading-relaxed text-tenue"><strong class="text-tinta">Aviso legal.</strong> {{ T.avisoLegal }}</p>
    </div>
  </footer>
</template>
