<script setup lang="ts">
import { nextTick, ref, useId } from 'vue'
import { onClickOutside } from '@vueuse/core'

defineProps<{ etiqueta: string; opciones: { to: string; texto: string }[]; activo?: boolean }>()
const abierto = ref(false)
const raiz = ref<HTMLElement | null>(null)
const id = useId()
const panel = ref<HTMLElement | null>(null)

let temporizador: ReturnType<typeof setTimeout> | undefined

function abrir() { clearTimeout(temporizador); abierto.value = true }
function cerrar() { clearTimeout(temporizador); abierto.value = false }
/** Solo el ratón abre al pasar por encima; en pantallas táctiles manda el toque. */
function alEntrar(e: PointerEvent) { if (e.pointerType === 'mouse') abrir() }
function alSalir(e: PointerEvent) { if (e.pointerType === 'mouse') temporizador = setTimeout(cerrar, 150) }
onClickOutside(raiz, cerrar)

function items() { return Array.from(panel.value?.querySelectorAll<HTMLElement>('[role="menuitem"]') ?? []) }
async function enfocar(i: number) {
  abrir()
  await nextTick()
  const lista = items()
  lista[(i + lista.length) % lista.length]?.focus()
}
function teclaBoton(e: KeyboardEvent) {
  if (e.key === 'ArrowDown') { e.preventDefault(); enfocar(0) }
  else if (e.key === 'ArrowUp') { e.preventDefault(); enfocar(-1) }
}
</script>

<template>
  <div ref="raiz" class="relative flex items-stretch" @pointerenter="alEntrar" @pointerleave="alSalir">
    <button type="button" aria-haspopup="menu" :aria-expanded="abierto" :aria-controls="id" @click="abierto ? cerrar() : abrir()" @keydown="teclaBoton">
      {{ etiqueta }}
    </button>
    <ul v-show="abierto" :id="id" ref="panel" role="menu" :aria-label="etiqueta">
      <li v-for="o in opciones" :key="o.to" role="none">
        <RouterLink :to="o.to" role="menuitem" tabindex="-1">
          <span>{{ o.texto }}</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
