<script setup lang="ts">
import { T } from '@/lib/textos'

defineProps<{ total?: number | null; marcas?: string[] }>()
const B = T.landing.buscador
</script>

<template>
  <section class="relative px-4" aria-labelledby="buscador-titulo">
    <form class="mx-auto max-w-[940px] bg-papel shadow-tarjeta" @submit.prevent>
      <div>
        <h2 id="buscador-titulo">{{ B.titulo }}</h2>
      </div>
    </form>
  </section>
</template>
