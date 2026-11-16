<script setup lang="ts">
import fondo from '@/assets/images/hero-bg-city.jpg'
import auto from '@/assets/images/hero-car.svg'
import HeroHotspot from '@/components/landing/HeroHotspot.vue'
import { T } from '@/lib/textos'

defineProps<{ versiones?: number | null; marcas?: number | null }>()
</script>

<template>
  <section class="sobre-foto relative isolate flex min-h-[max(600px,100svh)] overflow-hidden bg-velo" aria-labelledby="hero-titulo">
    <img :src="fondo" alt="" class="absolute inset-0 -z-20 h-full w-full object-cover grayscale" width="1600" height="1193" fetchpriority="high" decoding="async" />
    <div class="absolute inset-0 -z-10 bg-velo/[0.88]" aria-hidden="true" />
    <div class="relative mx-auto flex w-full max-w-landing items-center px-[15px] pt-barra">
      <div class="relative z-20 pt-16 lg:pl-[145px]">
        <h1 id="hero-titulo" class="whitespace-nowrap text-[38px] leading-none sm:text-[52px] lg:text-[64px] tracking-[-1px] text-tinta"><span class="text-acento-texto">{{ T.landing.hero.acento }}</span> {{ T.landing.hero.titulo }}</h1>
        <p class="mt-6 max-w-[310px] text-[15px] font-normal leading-[1.6] text-tinta">{{ T.sublema }}</p>
        <RouterLink to="/comparador" class="boton-acento mt-9 px-7">{{ T.landing.hero.boton }}</RouterLink>
      </div>
      <div class="absolute right-[140px] top-[33%] z-20 text-right">
        <p class="text-base font-bold uppercase tracking-[1px] text-acento-texto">{{ T.landing.hero.datoTitulo }}</p>
        <p class="mt-3 text-sm font-bold text-tinta"><span class="num">{{ versiones ?? '—' }}</span> versiones · <span class="num">{{ marcas ?? '—' }}</span> marcas</p>
      </div>
    </div>
    <div class="absolute bottom-0 right-[3%] z-10 w-[52%] max-w-[940px] translate-y-[7%]">
      <img :src="auto" :alt="T.landing.hero.autoAlt" class="block w-full" width="1000" height="450" decoding="async" />
      <HeroHotspot class="left-[58%] top-[38%]" :texto="T.landing.hero.hotspots[0]" />
      <HeroHotspot class="left-[22.5%] top-[92%]" :texto="T.landing.hero.hotspots[1]" />
    </div>
  </section>
</template>
