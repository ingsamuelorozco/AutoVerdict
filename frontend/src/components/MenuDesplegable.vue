<script setup lang="ts">
import { ref } from 'vue'
import { onClickOutside } from '@vueuse/core'

defineProps<{ etiqueta: string; opciones: { to: string; texto: string }[]; activo?: boolean }>()
const abierto = ref(false)
const raiz = ref<HTMLElement | null>(null)

function abrir() { abierto.value = true }
function cerrar() { abierto.value = false }
onClickOutside(raiz, cerrar)
</script>

<template>
  <div ref="raiz" class="relative flex items-stretch">
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
