<script setup lang="ts">
import { useHead } from '@unhead/vue'
useHead({ title: 'Página no encontrada' })
</script>

<template>
  <div class="contenedor py-24 text-center">
    <p class="font-titulo text-7xl text-tenue">404</p>
    <h1 class="mt-4 text-3xl font-semibold">Esta página no existe</h1>
    <p class="mt-2 text-tenue">Quizá el vehículo cambió de nombre o el enlace está incompleto.</p>
    <div class="mt-8 flex justify-center gap-3"><RouterLink to="/buscar" class="boton-primario">Buscar vehículo</RouterLink><RouterLink to="/" class="boton-secundario">Ir al inicio</RouterLink></div>
  </div>
</template>
