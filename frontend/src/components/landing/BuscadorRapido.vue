<script setup lang="ts">
import { T } from '@/lib/textos'

defineProps<{ total?: number | null; marcas?: string[] }>()
const B = T.landing.buscador
</script>

<template>
  <section class="relative bg-[linear-gradient(to_bottom,rgb(var(--velo))_0_56px,transparent_56px)] px-4" aria-labelledby="buscador-titulo">
    <form class="mx-auto max-w-[940px] bg-papel px-[35px] dark:bg-superficie pb-[50px] pt-6 shadow-tarjeta" @submit.prevent>
      <div>
      <div class="flex items-baseline gap-4">
        <h2 id="buscador-titulo" class="text-[26px] leading-none">{{ B.titulo }}</h2>
        <RouterLink to="/buscar" class="text-[13px] font-normal text-acento-texto hover:underline">{{ B.avanzada }}</RouterLink>
      </div>
      <p><span class="num">{{ total ?? '—' }}</span> {{ B.disponibles }}</p>
      </div>
    </form>
  </section>
</template>
