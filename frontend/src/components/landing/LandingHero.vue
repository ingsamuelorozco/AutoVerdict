<script setup lang="ts">
import { T } from '@/lib/textos'
</script>

<template>
  <section class="sobre-foto relative isolate flex min-h-[max(600px,100svh)] overflow-hidden bg-velo" aria-labelledby="hero-titulo">
    <div class="relative mx-auto flex w-full">
      <div class="relative z-20">
        <h1 id="hero-titulo">{{ T.landing.hero.acento }} {{ T.landing.hero.titulo }}</h1>
      </div>
    </div>
  </section>
</template>
