<script setup lang="ts">
import fondo from '@/assets/images/features-bg-snow-road.jpg'
import autoCenital from '@/assets/images/car-top-view.svg'
import ItemCaracteristica from '@/components/landing/ItemCaracteristica.vue'
import { T } from '@/lib/textos'

const C = T.landing.caracteristicas
</script>

<template>
  <section class="relative isolate overflow-hidden bg-suave py-16 lg:py-seccion" aria-labelledby="caract-titulo">
    <img :src="fondo" alt="" class="absolute inset-0 -z-10 h-full w-full object-cover opacity-[0.07] grayscale" width="1600" height="1063" loading="lazy" decoding="async" />
    <h2 id="caract-titulo" class="sr-only">{{ C.titulo }}</h2>
    <div class="mx-auto grid max-w-landing items-center gap-12 px-[15px] lg:grid-cols-[1fr_300px_1fr] lg:gap-10">
      <ul class="grid gap-10">
        <ItemCaracteristica v-for="i in C.izquierda" :key="i.titulo" v-bind="i" lado="izquierda" />
      </ul>
      <div class="relative mx-auto flex h-[420px] w-[300px] items-center justify-center">
        <span class="absolute left-1/2 top-[45%] h-[300px] w-[300px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-elevada/50" aria-hidden="true" />
        <span class="absolute left-1/2 top-[45%] h-[240px] w-[240px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-elevada" aria-hidden="true" />
        <img :src="autoCenital" :alt="C.autoAlt" class="relative h-[400px] w-auto drop-shadow-[0_18px_16px_rgb(0_0_0/0.18)]" width="200" height="440" loading="lazy" decoding="async" />
      </div>
      <ul class="grid gap-10">
        <ItemCaracteristica v-for="i in C.derecha" :key="i.titulo" v-bind="i" lado="derecha" />
      </ul>
    </div>
  </section>
</template>
