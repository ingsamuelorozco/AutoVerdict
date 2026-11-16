<script setup lang="ts">
import { T } from '@/lib/textos'

const C = T.landing.caracteristicas
</script>

<template>
  <section class="relative isolate overflow-hidden bg-suave py-16 lg:py-seccion" aria-labelledby="caract-titulo">
    <h2 id="caract-titulo" class="sr-only">{{ C.titulo }}</h2>
    <div class="mx-auto grid">
    </div>
  </section>
</template>
