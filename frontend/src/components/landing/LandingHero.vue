<script setup lang="ts">
import fondo from '@/assets/images/hero-bg-city.jpg'
import { T } from '@/lib/textos'
</script>

<template>
  <section class="sobre-foto relative isolate flex min-h-[max(600px,100svh)] overflow-hidden bg-velo" aria-labelledby="hero-titulo">
    <img :src="fondo" alt="" class="absolute inset-0 -z-20 h-full w-full object-cover grayscale" width="1600" height="1193" fetchpriority="high" decoding="async" />
    <div class="absolute inset-0 -z-10 bg-velo/[0.88]" aria-hidden="true" />
    <div class="relative mx-auto flex w-full max-w-landing px-[15px] pt-barra">
      <div class="relative z-20">
        <h1 id="hero-titulo">{{ T.landing.hero.acento }} {{ T.landing.hero.titulo }}</h1>
      </div>
    </div>
  </section>
</template>
