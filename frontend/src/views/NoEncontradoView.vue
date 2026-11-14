<script setup lang="ts">
import { useHead } from '@unhead/vue'
useHead({ title: 'Página no encontrada' })
</script>

<template>
  <div class="contenedor flex min-h-[70vh] flex-col items-center justify-center py-24 text-center">
    <div class="franja-m-corta" aria-hidden="true" />
    <p class="mt-8 text-[120px] font-bold leading-none text-tinta num lg:text-[180px]">404</p>
    <h1 class="mt-6 text-display-sm">Esta página no existe</h1>
    <p class="mt-4 text-lg text-tenue">Quizá el vehículo cambió de nombre o el enlace está incompleto.</p>
    <div class="mt-10 flex flex-col justify-center gap-4 sm:flex-row"><RouterLink to="/buscar" class="boton-primario">Buscar vehículo</RouterLink><RouterLink to="/" class="boton-secundario">Ir al inicio</RouterLink></div>
  </div>
</template>
