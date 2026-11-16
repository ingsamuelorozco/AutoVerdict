<script setup lang="ts">
import fondo from '@/assets/images/features-bg-snow-road.jpg'
import autoCenital from '@/assets/images/car-top-view.png'
import ItemCaracteristica from '@/components/landing/ItemCaracteristica.vue'
import { T } from '@/lib/textos'

const C = T.landing.caracteristicas
</script>

<template>
  <section class="relative isolate overflow-hidden bg-suave py-16 lg:py-seccion" aria-labelledby="caract-titulo">
    <img :src="fondo" alt="" class="absolute inset-0 -z-10 h-full w-full object-cover opacity-[0.07] grayscale dark:opacity-[0.04]" width="1600" height="1063" loading="lazy" decoding="async" />
    <h2 id="caract-titulo" class="sr-only">{{ C.titulo }}</h2>
    <div class="mx-auto grid max-w-landing items-center gap-12 px-[15px] md:grid-cols-2 lg:grid-cols-[1fr_300px_1fr] lg:gap-10">
      <ul class="grid gap-10 lg:order-1">
        <ItemCaracteristica v-for="i in C.izquierda" :key="i.titulo" v-bind="i" lado="izquierda" />
      </ul>
      <div class="relative order-first mx-auto flex h-[340px] w-[260px] sm:h-[420px] sm:w-[300px] md:col-span-2 lg:order-2 lg:col-span-1 items-center justify-center">
        <span class="absolute left-1/2 top-[45%] h-[300px] w-[300px] sm:h-[360px] sm:w-[360px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-elevada/50" aria-hidden="true" />
        <span class="absolute left-1/2 top-[45%] h-[260px] w-[260px] sm:h-[310px] sm:w-[310px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-elevada" aria-hidden="true" />
        <span class="absolute left-1/2 top-[45%] h-[224px] w-[224px] sm:h-[270px] sm:w-[270px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-acento" aria-hidden="true" />
        <img :src="autoCenital" :alt="C.autoAlt" class="relative h-[280px] w-auto sm:h-[340px] drop-shadow-[0_18px_16px_rgb(0_0_0/0.22)]" width="630" height="900" loading="lazy" decoding="async" />
      </div>
      <ul class="grid gap-10 lg:order-3">
        <ItemCaracteristica v-for="i in C.derecha" :key="i.titulo" v-bind="i" lado="derecha" />
      </ul>
    </div>
  </section>
</template>
