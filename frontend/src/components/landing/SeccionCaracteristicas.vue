<script setup lang="ts">
import fondo from '@/assets/images/features-bg-snow-road.jpg'
import { T } from '@/lib/textos'

const C = T.landing.caracteristicas
</script>

<template>
  <section class="relative isolate overflow-hidden bg-suave py-16 lg:py-seccion" aria-labelledby="caract-titulo">
    <img :src="fondo" alt="" class="absolute inset-0 -z-10 h-full w-full object-cover opacity-[0.07] grayscale" width="1600" height="1063" decoding="async" />
    <h2 id="caract-titulo" class="sr-only">{{ C.titulo }}</h2>
    <div class="mx-auto grid">
    </div>
  </section>
</template>
