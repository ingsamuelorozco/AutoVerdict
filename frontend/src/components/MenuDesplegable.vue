<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ etiqueta: string; opciones: { to: string; texto: string }[]; activo?: boolean }>()
const abierto = ref(false)

function abrir() { abierto.value = true }
function cerrar() { abierto.value = false }
</script>

<template>
  <div class="relative flex items-stretch">
    <button type="button" @click="abierto ? cerrar() : abrir()">
      {{ etiqueta }}
    </button>
    <ul v-show="abierto">
      <li v-for="o in opciones" :key="o.to">
        <RouterLink :to="o.to">
          <span>{{ o.texto }}</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
