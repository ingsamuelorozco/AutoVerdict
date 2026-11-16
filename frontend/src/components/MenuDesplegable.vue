<script setup lang="ts">
import { ref, useId } from 'vue'
import { onClickOutside } from '@vueuse/core'

defineProps<{ etiqueta: string; opciones: { to: string; texto: string }[]; activo?: boolean }>()
const abierto = ref(false)
const raiz = ref<HTMLElement | null>(null)
const id = useId()

let temporizador: ReturnType<typeof setTimeout> | undefined

function abrir() { clearTimeout(temporizador); abierto.value = true }
function cerrar() { clearTimeout(temporizador); abierto.value = false }
/** Solo el ratón abre al pasar por encima; en pantallas táctiles manda el toque. */
function alEntrar(e: PointerEvent) { if (e.pointerType === 'mouse') abrir() }
function alSalir(e: PointerEvent) { if (e.pointerType === 'mouse') temporizador = setTimeout(cerrar, 150) }
onClickOutside(raiz, cerrar)
</script>

<template>
  <div ref="raiz" class="relative flex items-stretch" @pointerenter="alEntrar" @pointerleave="alSalir">
    <button type="button" aria-haspopup="menu" :aria-expanded="abierto" :aria-controls="id" @click="abierto ? cerrar() : abrir()">
      {{ etiqueta }}
    </button>
    <ul v-show="abierto" :id="id" role="menu" :aria-label="etiqueta">
      <li v-for="o in opciones" :key="o.to" role="none">
        <RouterLink :to="o.to" role="menuitem" tabindex="-1">
          <span>{{ o.texto }}</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
