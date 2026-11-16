<script setup lang="ts">
import { T } from '@/lib/textos'

defineProps<{ total?: number | null; marcas?: string[] }>()
const B = T.landing.buscador
</script>

<template>
  <section class="relative bg-[linear-gradient(to_bottom,rgb(var(--velo))_0_56px,transparent_56px)] px-4" aria-labelledby="buscador-titulo">
    <form class="mx-auto max-w-[940px] bg-papel px-[35px] pb-[50px] pt-6 shadow-tarjeta" @submit.prevent>
      <div>
        <h2 id="buscador-titulo">{{ B.titulo }}</h2>
      </div>
    </form>
  </section>
</template>
