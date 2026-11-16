<script setup lang="ts">
import fondo from '@/assets/images/hero-bg-city.jpg'
import { T } from '@/lib/textos'

defineProps<{ versiones?: number | null; marcas?: number | null }>()
</script>

<template>
  <section class="sobre-foto relative isolate flex min-h-[max(600px,100svh)] overflow-hidden bg-velo" aria-labelledby="hero-titulo">
    <img :src="fondo" alt="" class="absolute inset-0 -z-20 h-full w-full object-cover grayscale" width="1600" height="1193" fetchpriority="high" decoding="async" />
    <div class="absolute inset-0 -z-10 bg-velo/[0.88]" aria-hidden="true" />
    <div class="relative mx-auto flex w-full max-w-landing items-center px-[15px] pt-barra">
      <div class="relative z-20 pt-16 lg:pl-[145px]">
        <h1 id="hero-titulo" class="whitespace-nowrap text-[64px] leading-none tracking-[-1px] text-tinta"><span class="text-acento-texto">{{ T.landing.hero.acento }}</span> {{ T.landing.hero.titulo }}</h1>
        <p class="mt-6 max-w-[310px] text-[15px] font-normal leading-[1.6] text-tinta">{{ T.sublema }}</p>
        <RouterLink to="/comparador" class="boton-acento mt-9 px-7">{{ T.landing.hero.boton }}</RouterLink>
      </div>
      <div>
        <p class="text-base font-bold uppercase tracking-[1px] text-acento-texto">{{ T.landing.hero.datoTitulo }}</p>
        <p class="mt-3 text-sm font-bold text-tinta"><span class="num">{{ versiones ?? '—' }}</span> versiones · <span class="num">{{ marcas ?? '—' }}</span> marcas</p>
      </div>
    </div>
  </section>
</template>
